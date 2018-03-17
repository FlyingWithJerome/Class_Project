#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <ctime>

#ifndef _DNS_SCAN_PACKET
#define _DNS_SCAN_PACKET
#define DEFAULT_QUERY_ADDRESS "email-jxm959-case-edu.ipl.eecs.case.edu"
#define DEFAULT_QUERY_DNS "8.8.8.8" 

class Packet
{
public:
	Packet();
	Packet(char* inputString);
	int setQuestion(char *);				// Set the question web address
	int setServer(char *);					// Set the server to ask for DNS response
	std::vector<std::string> getAnswerIP();	// Get the answer section of IP
	char * pack();							// Get the packet to be sent

private:
	char[1000]	packetData;
	char[100]	questionAddress;
	int			questionCount;
	char[20]	serverIP;
	int			serverCount;

	bool	QR;		// 0 for query, 1 for response
	int		OpCode;	// operation code, see RFC 1035
	bool	AA;		// Authoritative Answer, 0 is not, 1 is authoritative
	bool	TC;		// Truncated, 0 is not truncated, 1 is truncated
	bool	RD;		// Recursion desired, 0 is not desired
	bool	RA;		// Recursion available, 0 is not available
	bool	Z;		//---
	bool	AD;		// Authencated data
	bool	CD;		// Checking disabled
	int		Rcode;	// Return code
};
#endif