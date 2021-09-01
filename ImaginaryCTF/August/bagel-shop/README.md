# bagel-shop
**Category:** Pwn
**Difficulty:** Medium/Hard
**Author:** Eth007

## Description

"I love using the pwn to pwn the pwn" - Max49, 2021

## Distribution 
(https://imaginaryctf.org/r/C6AA-bagel-shop.zip)
- `heaps_of_fun`
- `libc-2.27.so`
- `ld-2.27.so`
- `Makefile`
- `Dockerfile`
- `docker-compose.yml`
- `nc puzzler7.imaginaryctf.org 31337` (might not work anymore)

## Deploy notes

- Run with `flag.txt`, libc and ld are patchelf'ed

## Solution

Leak heap with double free, then leak libc by getting an unsorted bin chunk with overwriting `tcache_perthread_struct` with tcache poisoning, then tcache poisoning again to overwrite `__free_hook` with `system` and `free("/bin/sh")`

Alternate (possibly easier) solution was to leak heap, then tcache poison to get `malloc` to return a heap address that had a libc address in it (I heard that a pointer to `stderr` was lying around on the heap) then proceed as above.
