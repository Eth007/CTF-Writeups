# merinthophobia
**Category:** Rev
**Difficulty:** Medium
**Author:** Eth007

## Description

Reversing is so hard! If anyone has any tips for people who hate rev but like pwn, please reach out to me.

(The flag fits the regex ictf{[^}]+})


## Distribution 
(https://imaginaryctf.org/r/D729-merinthophobia)

- `merinthophobia`

## Deploy notes

- none

## Solution

Extract the ropchain after it's unxored using GDB, then recognize patterns to figure out that the ropchain is just reading in characters and then comparing each character to a hardcoded address in memory.
