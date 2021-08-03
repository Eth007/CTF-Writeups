#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/mman.h>

void dorng(long seed) {
  long num;
  char buf[512];
  for (int i=0; i<6; i++) {
    printf("Enter max value: ");
    fgets(buf, 16, stdin);
    num = atol(buf);
    if (num < 128 && num > 0) {
      printf("Random number: %ld\n", seed%num);
    }
    else {
      printf("Go away.\n");
      exit(0);
    }
  }
}

int main() {
  int r;
  char buf[512];
  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);
  mprotect(&puts+1456736+1000,12288, PROT_READ | PROT_EXEC);
  printf("Welcome to my RNG service!\n");
  srand(time(0));
  r = rand();
  dorng((long) &r);
  printf("Thanks for visiting our RNG! What's your name?\n");
  fgets(buf, 512, stdin);
  printf("Thanks for coming, ");
  printf(buf);
}

