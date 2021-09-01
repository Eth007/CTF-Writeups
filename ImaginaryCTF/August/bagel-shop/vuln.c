#include <stdio.h>
#include <stdlib.h>

char *mem[16];

void banner()
{
    FILE *fptr;
    char c;
    fptr = fopen("max49.txt", "r");
    c = fgetc(fptr);
    while (c != EOF)
    {
        putchar(c);
        c = fgetc(fptr);
    }
    fclose(fptr);
    return 0;
}

int main() {
  char c;
  int index;
  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);
  banner();
  puts("Welcome to Eth007's bagel shop!");
  puts("Sponsored by the one and only Max49!");
  for (int i=0; i<19; i++) {
    puts("(c)reate a bagel 🥯");
    puts("(e)at a bagel 😋");
    puts("(v)iew a bagel 👀");
    puts("(d)ecorate a bagel ✏️");
    scanf("%c%*c", &c);
    if (c=='c') {
      puts("Where should I store your bagel?");
      scanf("%d%*c", &index);
      if ((index < 0) || (index > 15)) {exit(0);}
      mem[index] = malloc(128);
    }
    else if (c=='e') {
      puts("Which bagel do you want to eat?");
      scanf("%d%*c", &index);
      if ((index < 0) || (index > 15)) {exit(0);}
      free(mem[index]);
    }
    else if (c=='v') {
      puts("Which bagel do you want to view?");
      scanf("%d%*c", &index);
      if ((index < 0) || (index > 15)) {exit(0);}
      puts(mem[index]);
      puts(":rooPOG: Nice bagel!");
    }
    else if (c=='d') {
      puts("Which bagel do you want to decorate?");
      scanf("%d%*c", &index);
      if ((index < 0) || (index > 15)) {exit(0);}
      puts("What do you want to write on the bagel?");
      fgets(mem[index], 128, stdin);
    }
  }
}
