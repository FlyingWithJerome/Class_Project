#include <cstdio>
#include <cstdlib>

#ifndef _DNS_SCAN_PACKET
#define _DNS_SCAN_PACKET
#define DEFAULT_QUERY_ADDRESS "email-jxm959-case-edu.ipl.eecs.case.edu"
#define DEFAULT_QUERY_DNS "8.8.8.8" 

class Packet
{
public:
	Packet(char* IPAddress=DEFAULT_QUERY_DNS, char* queryAddress=DEFAULT_QUERY_ADDRESS);
	Packet(char* inputString);
	setQuestion(char *);	// Set the question web address
	setServer(char *);		// Set the server to ask for DNS response

private:


};
#endif