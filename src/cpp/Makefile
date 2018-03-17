
.PHONY: all clean

all: main

GLOBAL = -lboost_system -o

CPP_LIST = main.cpp Query.cpp Packet.cpp

main: Query.cpp Query.h Packet.cpp Packet.h main.cpp
	g++ $(CPP_LIST) $(GLOBAL) main

clean:
	rm -rf main
