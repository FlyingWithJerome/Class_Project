
# include "Query.h"

Query::Query()
:isOnDuty(false), IPAddressBegin("0.0.0.0"), IPAddressEnd("255.255.255.255")
{
    this->masterSocket = socket(AF_INET, SOCK_DGRAM, 0);

    this->rawPacket    = Query::makePacket();
}

Query::Query(std::string startIPAddress, std::string endIPAddress)
:isOnDuty(false), IPAddressBegin(startIPAddress), IPAddressEnd(endIPAddress)
{
    this->masterSocket = socket(AF_INET, SOCK_DGRAM, 0);

    this->rawPacket    = Query::makePacket();
}

Query::~Query()
{
    close(this->masterSocket);

    delete [] this->rawPacket;
}

std::vector<int> Query::launchQuery()
{
    this->isOnDuty = true;

    this->singleProcessSingleThreadQuery(this->IPAddressBegin, this->IPAddressEnd);

    this->isOnDuty = false;
}

char* Query::makePacket()
{
    Packet p = Packet();

    p.setQuestion("case.edu");

    int length = 0;
    
    char* rawPacket = p.pack(length);

    for(int i=0; i < length; i++)
    {
        std::cout<<rawPacket[i]<<" ";
    }
    std::cout<<std::endl;

    return rawPacket;
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

    for(unsigned long IPAddress = beginInt; IPAddress <= endInt; IPAddress++)
    {
        boost::asio::ip::address_v4 currentIP = boost::asio::ip::address_v4(IPAddress);

        sockaddr_in *addressObject = new sockaddr_in();

        *addressObject = Query::addressObjectFactory(currentIP.to_string().c_str(), 53);

        int addressLength = sizeof(sockaddr_in);

        sendto(this->masterSocket, this->rawPacket, 1000, 0, (struct sockaddr*)addressObject, addressLength);

        delete addressObject;
    }
}
