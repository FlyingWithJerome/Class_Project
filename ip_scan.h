#include <cstdio> // For stdin, stdout
#include <cstdlib>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <pthread.h>

#include <string>



#ifndef IP_SCAN_
#define IP_SCAN_

class Query
{
public:
    Query();
    ~Query();

    void set_target(const std::string target); //set the website to be queried

    bool is_working(const std::string dns_server) const; //check if a dns server is working

private:

    int outbound_socket;

    int inbound_socket;

    std::string packet_for_everyone;

    std::string make_dns_packet();

    bool send_request(const std::string dns_server) const;

    void do_with_multithreading(const int thread_num) const;

    bool listen_and_check_result(const std::string& result) const;



};

Query::Query()
{
    // this -> packet_for_everyone = make_dns_packet();
    this -> outbound_socket     = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    this -> inbound_socket      = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
}

Query::~Query()
{

}

#endif