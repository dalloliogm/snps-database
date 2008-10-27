# Make file for Pairwise, Permute  and Convert

CC = gcc
CFLAGS =  -O2 -pedantic
LIB = -lm

OBJ = tools.o seqtools.o pairlk.o

all: pairwise convert permute

pairwise: $(OBJ) pairwise.o header.h
	$(CC) $(CFLAGS) -o pairwise $(OBJ) pairwise.o $(LIB)

convert: tools.o seqtools.o convert.c header.h
	$(CC) $(CFLAGS) -o convert tools.o seqtools.o convert.c $(LIB)

permute: tools.o seqtools.o permute.c header.h
	$(CC) $(CFLAGS) -o permute tools.o seqtools.o permute.c $(LIB)

pairwise.o: $(OBJ) pairwise.c header.h
	$(CC) $(CFLAGS) -c -o pairwise.o pairwise.c

tools.o: tools.c header.h
	$(CC) $(CFLAGS) -c -o tools.o tools.c

seqtools.o: seqtools.c header.h
	$(CC) $(CFLAGS) -c -o seqtools.o seqtools.c 

pairlk.o: pairlk.c 
	$(CC) $(CFLAGS) -c -o pairlk.o pairlk.c
