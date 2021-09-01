#include <stdio.h>

char rooNobooli[1024] = "jctf{why_w0uld_ANYONE_like_rev_it's_so_frustrating!!!}";
char roocursion[1024] = "placeholder";
char rooYay[8192] = "placeholder";

void rooVoid(void) {
  __asm__(
    "syscall\n"
    "ret\n"
    "pop %rdi\n"
    "ret\n"
    "pop %rsi\n"
    "ret\n"
    "pop %rdx\n"
    "ret\n"
    "pop %rcx\n"
    "ret\n"
    "pop %rbx\n"
    "ret\n"
    "pop %rax\n"
    "ret\n"
    "movq %rdi, (%rsi)\n"
    "ret\n"
    "cmpq %rdi, %rsi\n"
    "cmoveq %rdx, %rax\n"
    "ret\n"
    "movzbl (%rdx), %ecx\n"
    "ret\n"
    "movq %rcx, %rsi\n"
    "ret\n"
    "movq %rcx, %rdi\n"
    "ret\n"
    "pop %rsp\n"
    "ret\n"
  );
}

int main() {
  char buf[0];

  memcpy(buf, roocursion, 1024);

  return;
}

void rooScientist(char* buf, int count) {
  char* a;
  for (int i=0; i<count; i++) {
    a = buf+i;
    if (i%2==0) {
      *a = *a ^ '\x42';
    }
    else {
      *a = *a ^ (char) 42;
    }
  }
}
