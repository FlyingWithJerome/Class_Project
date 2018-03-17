
# include "Query.h"

Query::Query()
:isOnDuty(false), IPAddressBegin(0), IPAddressEnd((int)pow(2, 32))
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
    this->masterSocket.close()
}

std::vector<int> Query::launchQuery()
{
    this->isOnDuty = true;
}

bool Query::isWorking()
{
    return this->isOnDuty
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

unsigned int Query::addressToInt(std::string ipAddress)
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
    sockaddr_in begin = Query::addressObjectFactory(startIPAddress.c_str(), 53);

    sockaddr_in end   = Query::addressObjectFactory(endIPAddress.c_str(),   53);


}
