.PHONY: all clean

all: ip_scan

ip_scan: ip_scan.cpp ip_scan.h
	g++ -std=c++0x ip_scan.cpp -g -o ip_scan.o

clean:
	rm -f *.o