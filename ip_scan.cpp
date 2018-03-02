
#include "ip_scan.h"

Query::Query()
{
    this -> packet_for_everyone = make_dns_packet();
    this -> outbound_socket     = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    this -> inbound_socket      = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    if(outbound_socket < 0)
        printf("Create FAILED\n");
}

Query::~Query()
{
    close(outbound_socket);

    close(inbound_socket);
}

Query::packet Query::make_dns_packet()
{
    std::string message = "For research use@Case Western Reserve, contact jxm959@case.edu";

    Query::packet sent_packet = Query::packet();

    return sent_packet;
}

bool Query::is_working(sockaddr_in dns_server) const
{
    return this->send_request(dns_server);
}

bool Query::send_request(sockaddr_in dns_server) const
{
    if(bind(outbound_socket, (struct sockaddr*)&dns_server, sizeof(dns_server)) < 0)
        printf("Bind FAILED\n");

    if(connect(outbound_socket, (struct sockaddr*)&dns_server, sizeof(dns_server)) < 0)
        printf("Connect FAILED\n");

    if(send(outbound_socket, &packet_for_everyone, 1000, NULL) < 0)
        printf("Send FAILED\n");


    return false;
}

int main()
{
    Query query = Query();

    struct sockaddr_in dest;
    dest.sin_addr.s_addr = inet_addr("8.8.8.8");
    dest.sin_family = AF_INET;
    dest.sin_port = htons(53);

    query.is_working(dest);

    return 0;
}

