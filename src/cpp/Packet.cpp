#include "Packet.h"

Packet::Packet()
{
	memset(packetData,0,sizeof(packetData));
	memset(questionAddress,0,sizeof(questionAddress));
	memset(serverIP,0,sizeof(serverIP));
	Query	= 0;
	OpCode	= 0;// Standard Query
	AA		= 0;
	TC		= 0;
	RD		= 1;// Desired to be quried recursively
	RA		= 0;
	Z		= 0;// Reserved
	AD		= 0;
	CD		= 0;
	Rcode	= 0;
}

Packet::Packet(char * inputString)
{
	memcpy(packetData,inputString,strlen(inputString));
	memset(questionAddress,0,sizeof(questionAddress));
	memset(serverIP,0,sizeof(serverIP));
}

int Packet::setQuestion(char * input)
{
	int len = 0;
	if(len = strlen(input))
	{
		memcpy(questionAddress,input,len)
		questionCount ++;
	}
	return len;
}

int Packet::setServer(char * input)
{
	int len = 0;
	if(len = strlen(input))
	{
		memcpy(serverIP,input,len)
		serverCount ++;
	}
	return len;
}

char* Packet::pack()
{
	char * currentPos = packetData;
	std::srand(std::time(nullptr));
	int randomVariable = std::rand();
	int transactionID = randomVariable % 0xffff;// Randomly select transaction ID;

	//Write in transaction ID
	*(currentPos++) = transactionID / 0xff;
	*(currentPos++) = transactionID % 0xff;

	//Write in Flags
	*(currentPos++) = (QR<<7)|(OpCode<<3)|(AA<<2)|(TC<<1)|(RD);
	*(currentPos++) = (RA<<7)|(Z<<6)|(AD<<5)|(CD<<4)|(Rcode);

	//Write in Question count
	*(currentPos++) = 0;
	*(currentPos++) = questionCount;

	//Write in Answer RR
	*(currentPos++) = 0;
	*(currentPos++) = 0;

	//Write in Authority RR
	*(currentPos++) = 0;
	*(currentPos++) = 0;

	//Write in Additional RR
	*(currentPos++) = 0;
	*(currentPos++) = 0;

	//Write in Name to query
	*(currentPos) = '.';
	int addressLength = strlen(questionAddress);
	memcpy(currentPos+1,questionAddress,addressLength)

	int count = 0;
	int lastPos = 0;
	for(int i = 0;i<=addressLength;i++)
	{
		if(currentPos[i]=='.'||currentPos==0)
			if(count)
			{
				currentPos[lastPos] = count;
				count = 0;
				lastPos = i;
			}
			else
				lastPos = i;
		else
			count ++;
	}

	currentPos += addressLength;

	//Write in Type A
	*(currentPos++) = 0;
	*(currentPos++) = 1;

	//Write in Class IN
	*(currentPos++) = 0;
	*(currentPos++) = 1;

	return packetData;
}