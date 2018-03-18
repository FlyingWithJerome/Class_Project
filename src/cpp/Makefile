
.PHONY: all clean

all: main

GLOBAL = -std=c++0x -lboost_system -g -o

CPP_LIST = main.cpp Query.cpp Packet.cpp

main: Query.cpp Query.h Packet.cpp Packet.h main.cpp
	g++ $(CPP_LIST) $(GLOBAL) main

clean:
	rm -rf main
