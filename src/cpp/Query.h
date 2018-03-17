// Importing system libraries
# include <fcntl.h> 
# include <sys/mman.h> 
# include <unistd.h>
# include <sys/wait.h>
# include <sys/socket.h>

// Importing C++/C libraries
# include <iostream>
# include <thread>
# include <vector>


class Query
{
    public:
    // Constructors
        Query();
        Query(int processNumber);
        Query(int startIPAddress, int endIPAddress, int processNumber);

    // Destructors
        ~Query()

    // Public methods (start jobs, abort jobs, etc)
        vector<int> launchQuery();
        void        writeToFile(std::string fileName);
        void        abortQuery();
        bool        isWorking();
        

    private:
        char* makePacket();


}