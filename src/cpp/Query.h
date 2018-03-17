// Importing system libraries
# include <fcntl.h> 
# include <unistd.h>
# include <arpa/inet.h>
# include <sys/mman.h> 
# include <sys/wait.h>
# include <sys/socket.h>
# include <sys/types.h>

// Importing C++/C libraries
# include <iostream>
# include <thread>
# include <vector>
# include <cmath>
# include <string>

// Importing boost library
# include <boost/asio/ip/address_v4.hpp>
# include <boost/algorithm/string.hpp>

// Importing Mi's packet
# include "Packet.h"

// Macros
# define _NEWLINE_

# define SEND(target) \
_NEWLINE_ sendto(this->masterSocket, this->rawPacket, \
_NEWLINE_ 1000, 0, (struct sockaddr*)&target, sizeof(target))


class Query
{
    public:
    // Constructors
        Query();

        Query(std::string startIPAddress, std::string endIPAddress);

    // Destructors
        ~Query();

    // Public methods (start jobs, abort jobs, etc)
        std::vector<int> launchQuery();

        void             abortQuery();

        void             writeToFile(std::string fileName);

    // Public getters
        bool             isWorking() const;
    
    // Public setters
        void             setProcessNumbers();

    // Static methods
        static char*             makePacket();

        static sockaddr_in       addressObjectFactory(const char* ip_address, int port);

        static unsigned long int addressToInt(std::string ipAddress);


    private:

        void singleProcessMultithreadQuery (std::string startIPAddress, std::string endIPAddress);

        void singleProcessSingleThreadQuery (std::string startIPAddress, std::string endIPAddress);

        std::vector<int> splitJobAssignments(int start, int end, int numberOfWorkers);

        int masterSocket;

        int threadNumber;

        std::string IPAddressBegin;

        std::string IPAddressEnd;

        bool isOnDuty;

        char* rawPacket;
};