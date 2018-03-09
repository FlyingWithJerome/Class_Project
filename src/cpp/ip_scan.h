#include <cstdio> // For stdin, stdout
#include <cstdlib>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string>
#include <cerrno>


#ifndef IP_SCAN_
#define IP_SCAN_

class Query
{
public:

    Query();

    ~Query();

    void set_target(const std::string target); //set the website to be queried

    bool is_working(sockaddr_in dns_server) const; //check if a dns server is working

    static sockaddr_in address_object_factory(const char* ip_address, int port);

private:

    struct DNSPacket
    {
        uint16_t transaction_id = htons(0xffff);
        uint16_t control 	    = htons(0x0100);
        uint16_t q_counts       = htons(0x0001);
        uint16_t ans_counts     = htons(0x0000);
        uint16_t auth_counts    = htons(0x0000);
        uint16_t add_counts     = htons(0x0001);
        char target[10]         = "4case3edu";
        uint16_t type_          = htons(0x0100);
        uint16_t class_         = htons(0x0100);
        char message[17]        = "Tell me, senpai!";
    };

    int outbound_socket;

    int inbound_socket;

    DNSPacket packet_for_everyone;

    DNSPacket make_dns_packet();

    bool send_request(sockaddr_in dns_server) const;

    void do_with_multithreading(const int thread_num) const;

    bool listen_and_check_result() const;

};

#endif