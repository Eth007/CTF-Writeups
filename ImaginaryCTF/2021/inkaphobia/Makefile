NAME := inkaphobia
BUILD_PRODUCTS := inkaphobia
SIDE_PRODUCTS :=
DIST := inkaphobia libc.so.6
ADMIN_DIST := ${DIST} flag.txt

include ../../util/Makefile.base

inkaphobia : inkaphobia.c
	gcc inkaphobia.c -o inkaphobia -no-pie -Wl,-z,relro,-z,now
