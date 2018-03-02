#include <cstdio> // For stdin, stdout
#include <cstdlib>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string>
#include <wchar.h>


#ifndef IP_SCAN_
#define IP_SCAN_

class Query
{
public:
    Query();
    ~Query();

    void set_target(const std::string target); //set the website to be queried

    bool is_working(sockaddr_in dns_server) const; //check if a dns server is working

private:

    struct packet
    {
        uint16_t transaction_id = 0xffff;
        uint16_t control 	    = 0x0001;
        uint16_t q_counts       = 0x0100;
        uint16_t ans_counts     = 0x0000;
        uint16_t auth_counts    = 0x0000;
        uint16_t add_counts     = 0x0100;
        char query           = 0x0c;
        char target[10]      = "case.edu";
        // uint8_t ending          = 0x00;
        uint16_t type_          = 0x0100;
        uint16_t class_         = 0x0100;
        char message[50]     = "Fuck you";
    };

    int outbound_socket;

    int inbound_socket;

    packet packet_for_everyone;

    packet make_dns_packet();

    bool send_request(sockaddr_in dns_server) const;

    void do_with_multithreading(const int thread_num) const;

    bool listen_and_check_result(const std::string& result) const;



};

#endif