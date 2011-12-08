CC = clang
LIBS = -lm `pkg-config sndfile --libs`
CFLAGS = -std=c99 -O2 -Wall -Wextra $(LIBS)

all: pcm32-wav-test

pcm32-wav-test: pcm32-wav-test.c
