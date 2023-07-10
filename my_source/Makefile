CC=gcc
CFLAGS += -Wall -Wextra -Wpedantic -Wmissing-prototypes -Wredundant-decls \
  -Wshadow -Wpointer-arith -mavx2 -mbmi2 -mpopcnt -maes \
  -march=native -mtune=native -O3 -fomit-frame-pointer

DEPS = params.h ntt.h reduce.h ntt.c reduce.c


all:
	$(CC) $(CFLAGS) main.c ntt.c reduce.c -o ntt_run

clean:
	rm -f *.o
