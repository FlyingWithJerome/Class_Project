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

// Macros


class Query
{
    public:
    // Constructors
        Query();

        Query(int startIPAddress, int endIPAddress);

    // Destructors
        ~Query();

    // Public methods (start jobs, abort jobs, etc)
        std::vector<int> launchQuery();

        void             abortQuery();

        void             writeToFile(std::string fileName);

    // Public getters
        bool             isWorking();
    
    // Public setters
        void             setProcessNumbers();

    // Static methods
        static char*        makePacket();

        static sockaddr_in  addressObjectFactory(const char* ip_address, int port);

        static unsigned int addressToInt(std::string ipAddress);


    private:

        void singleProcessMultithreadQuery (int startIPAddress, int endIPAddress);

        void singleProcessSingleThreadQuery(int startIPAddress, int endIPAddress);

        std::vector<int> splitJobAssignments(int start, int end, int numberOfWorkers);

        int masterSocket;

        int threadNumber;

        int IPAddressBegin;

        int IPAddressEnd;

        bool isOnDuty;

        char* rawPacket;


};