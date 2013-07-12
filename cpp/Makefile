CC = g++
PROG = sample
CXXFLAGS = -g -O2 -Wall
#LDLIBS += -L/usr/lib/daqmw -lSock
LDLIBS += -L/usr/lib64/daqmw -lSock

OBJS += sample.o

all: $(PROG)

$(PROG): $(OBJS)

sample.o: sample.cpp SitcpRbcp.h

clean:
	rm -f *.o $(PROG)
