from pwn import *
import random

elf = ELF("./merinthophobia")
rop = ROP(elf)

elf.write(elf.symbols["rooYay"], b"}"*4096)

elf.save("./merinthophobia")


payload = b""

def wrap(s, n):
  return list(map(''.join, zip(*[iter(s+"\x00"*(n-len(s)%n))]*n)))

def g(*args):
  a = list(args)
  if a[-1] != "ret":
    a.append("ret")
  return p64(rop.find_gadget(a)[0])

def pad(s):
  return s + "\x00"*(len(s)%8)

def www(addr: int, content: int):
  global payload
  payload += g("pop rdi")
  payload += p64(content)
  payload += g("pop rsi")
  payload += p64(addr)
  payload += p64(next(elf.search(b"\x48\x89\x3E\xC3", executable=True))) # write what where gadget

def pr(content):
  global payload
  for i, s in enumerate(wrap(content, 8)):
    www(elf.symbols["rooNobooli"]+512+(i*8), u64(pad(s)))
  payload += g("pop rdi")
  payload += p64(1)
  payload += g("pop rsi")
  payload += p64(elf.symbols["rooNobooli"]+512)
  payload += g("pop rdx")
  payload += p64(len(content))
  payload += g("pop rax")
  payload += p64(1)
  payload += g("syscall")

def r(loc):
  global payload
  payload += g("pop rdi")
  payload += p64(0)
  payload += g("pop rsi")
  payload += p64(loc)
  payload += g("pop rdx")
  payload += p64(64)
  payload += g("pop rax")
  payload += p64(0)
  payload += g("syscall")

def end():
  global payload
  payload += g("pop rdi")
  payload += p64(0)
  payload += g("pop rax")
  payload += p64(60)
  payload += g("syscall")

def cmp(loc, target: int):
  global payload
  if target == ord("}"):
    return
  print(bytes([target]), hex(next(elf.search(bytes([target])))))
  payload += g("pop rdx")
  payload += p64(next(elf.search(bytes([target]))))
  payload += p64(next(elf.search(b"\x0f\xb6\x0a\xc3", executable=True))) # read byte at [rdx] into rcx
  payload += p64(next(elf.search(b"\x48\x89\xce\xc3", executable=True))) # mov rsi, rcx
  payload += g("pop rdx")
  payload += p64(loc)
  payload += p64(next(elf.search(b"\x0f\xb6\x0a\xc3", executable=True))) # read byte at [rdx] into rcx
  payload += p64(next(elf.search(b"\x48\x89\xcf\xc3", executable=True))) # mov rdi, rcx
  payload += g("pop rdx")
  payload += p64(0)
  payload += g("pop rax")
  payload += p64(60)
  payload += p64(next(elf.search(b"\x48\x39\xfe\x48\x0f\x44\xc2\xc3", executable=True))) # if rdi==rsi, make rax=rdx
  payload += g("pop rdi")
  payload += p64(0)
  payload += g("syscall")

inp = elf.symbols["rooNobooli"]+42

pr("What is the flag?\n")
r(inp)

flag = b"ictf{pwnrev_1s_c00l}"
#flag = b"ictf"
checks = []

for i,n in enumerate(flag):
  checks.append([inp+i,n])

random.shuffle(checks)

print(checks)

for check in checks:
  cmp(check[0], check[1])

pr("Congrats! You got the flag!\n")
end()

print(payload)

elf.write(elf.symbols["rooYay"], xor(payload, "\x42\x2a"))

loader = b"A"*8

loader += g("pop rdi")
loader += p64(elf.symbols["rooYay"])
loader += g("pop rsi")
loader += p64(4096)
loader += p64(elf.symbols["rooScientist"])
loader += g("pop rsp")
loader += p64(elf.symbols["rooYay"])

elf.write(elf.symbols["roocursion"], loader)

elf.save("./merinthophobia")

print(len(payload))
print(checks)
