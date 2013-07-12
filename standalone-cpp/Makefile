CC = g++
PROG = sample
CXXFLAGS = -g -O2 -Wall

OBJS += $(PROG).o
OBJS += Sock.o

all: $(PROG)

$(PROG): $(OBJS)

sample.o: sample.cpp SitcpRbcp.h

clean:
	rm -f *.o $(PROG)
