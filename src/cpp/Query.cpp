
# include "Query.h"

Query::Query()
:isOnDuty(false), IPAddressBegin("0.0.0.0"), IPAddressEnd("255.255.255.255")
{
    this->masterSocket = socket(AF_INET, SOCK_DGRAM, 0);

    this->rawPacket     = new char[1000];

    this->packetManager = new Packet();

    this->writePacket();
}

Query::Query(std::string startIPAddress, std::string endIPAddress)
:isOnDuty(false), IPAddressBegin(startIPAddress), IPAddressEnd(endIPAddress)
{
    this->masterSocket = socket(AF_INET, SOCK_DGRAM, 0);

    if(this->masterSocket < 0)
    {
        std::cout<<"FAILED to make a socket\n"<<std::endl;

        std::cout<<"Reason: "<<strerror(errno)<<std::endl;
    }

    this->rawPacket     = new char[1000];

    this->packetManager = new Packet();

    this->writePacket();
}

Query::~Query()
{
    close(this->masterSocket);

    if(this->rawPacket)

        delete [] this->rawPacket;

    this->rawPacket = NULL;

    if(this->packetManager)

        delete this->packetManager;

    this->packetManager = NULL;
}

void Query::writePacket()
{
    char* name = "case.edu";

    this->packetManager->setQuestion(name);

    std::pair<char*, int> packetInfo = this->packetManager->pack();

    std::copy(packetInfo.first, packetInfo.first + packetInfo.second, this->rawPacket);

    this->packetLength = packetInfo.second;
}

std::vector<int> Query::launchQuery()
{
    this->isOnDuty = true;

    this->singleProcessSingleThreadQuery(this->IPAddressBegin, this->IPAddressEnd);

    this->isOnDuty = false;
}

bool Query::isWorking() const
{
    return this->isOnDuty;
}

std::vector<int> Query::splitJobAssignments(int start, int end, int numberOfWorkers)
{
    std::vector<int> jobAssignment = std::vector<int>();

    int stepLength = (end - start) / numberOfWorkers;

    int remaining  = (end - start) % numberOfWorkers;

    jobAssignment.push_back(start);

    while(jobAssignment.size() < (numberOfWorkers + 1))
    {
        jobAssignment.push_back(stepLength + int(jobAssignment.size() <= remaining));
    }
    return jobAssignment;
}

sockaddr_in Query::addressObjectFactory(const char* ip_address, int port)
{
    struct sockaddr_in address_object;

    address_object.sin_addr.s_addr = inet_addr(ip_address);

    address_object.sin_family      = AF_INET;

    address_object.sin_port        = htons(port);

    return address_object;
}

unsigned long int Query::addressToInt(std::string ipAddress)
{
    std::vector<std::string> tokens;

    boost::split(tokens, ipAddress, boost::is_any_of("."));

    return stoi(tokens[0]) * pow(2, 24) + 
           stoi(tokens[1]) * pow(2, 16) +
           stoi(tokens[2]) * pow(2, 8)  +
           stoi(tokens[3]);

}

void Query::singleProcessSingleThreadQuery (std::string startIPAddress, std::string endIPAddress)
{
    unsigned long beginInt = boost::asio::ip::address_v4::from_string(startIPAddress).to_ulong();

    unsigned long endInt   = boost::asio::ip::address_v4::from_string(endIPAddress).to_ulong();

    sockaddr_in addressObject = Query::addressObjectFactory(startIPAddress.c_str(), 53);

    if(connect(this->masterSocket, (struct sockaddr*)&addressObject, sizeof(addressObject))<0)

        printf("connection fail\n");

    if(send(this->masterSocket, this->rawPacket, 1000, 0) < 0)

        printf("send fail\n");

    // for(unsigned long IPAddress = beginInt; IPAddress <= endInt; IPAddress++)
    // {
    //     printf("%d %d\n", IPAddress-beginInt, IPAddress-endInt);

    //     boost::asio::ip::address_v4 currentIP = boost::asio::ip::address_v4(IPAddress);

    //     addressObject.sin_addr.s_addr = inet_addr(currentIP.to_string().c_str());

    //     int addressLength = sizeof(sockaddr_in);

    //     sendto(this->masterSocket, this->rawPacket, 1000, 0, (struct sockaddr*)&addressObject, addressLength);
    // }
    printf("Done\n");
}
