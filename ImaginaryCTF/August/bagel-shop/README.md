# heaps-of-fun
**Category:** Pwn
**Difficulty:** Hard
**Author:** Eth007

## Description

Time for some generic heap!

## Distribution

- `heaps_of_fun`
- `libc-2.27.so`
- `ld-2.27.so`
- `Makefile`

## Deploy notes

- Run with `flag.txt`, libc, ld

## Solution

Get a leak from a fastbin, then tcache poison to overwrite `__free_hook` with `system()`, write `/bin/sh` into a chunk, and free the chunk to get a shell.
