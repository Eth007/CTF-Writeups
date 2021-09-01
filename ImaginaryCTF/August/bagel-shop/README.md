# bagel-shop
**Category:** Pwn
**Difficulty:** Medium/Hard
**Author:** Eth007

## Description

"I love using the pwn to pwn the pwn" - Max49, 2021

## Distribution 
(https://imaginaryctf.org/r/C6AA-bagel-shop.zip)

- `vuln`
- `libc-2.27.so`
- `ld-2.27.so`
- `Makefile`
- `Dockerfile`
- `docker-compose.yml`
- `nc puzzler7.imaginaryctf.org 31337` (might not work anymore)

## Deploy notes

- Run with `flag.txt`, libc and ld are patchelf'ed

## Solution

Leak libc by getting an unsorted bin chunk with overwriting `tcache_perthread_struct` with tcache poisoning, then tcache poisoning again to overwrite `__free_hook` with `system` and `free("/bin/sh")`
