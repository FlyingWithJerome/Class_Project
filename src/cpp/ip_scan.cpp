
#include "ip_scan.h"

Query::Query()
{
    this -> packet_for_everyone = DNSPacket();
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

Query::DNSPacket Query::make_dns_packet()
{
    std::string message = "For research use@Case Western Reserve, contact jxm959@case.edu";

    Query::DNSPacket sent_packet = DNSPacket();

    return sent_packet;
}


bool Query::is_working(sockaddr_in dns_server) const
{
    return this->send_request(dns_server);
}


bool Query::send_request(sockaddr_in dns_server) const
{

    sockaddr_in self_bind = Query::address_object_factory("192.168.0.7", 1053);

    if(bind(outbound_socket, (struct sockaddr*)&self_bind, sizeof(self_bind)) < 0)
    {

        printf("%s\n", strerror(errno));

        printf("Bind FAILED\n");

        return false;
    }

    if(connect(outbound_socket, (struct sockaddr*)&dns_server, sizeof(dns_server)) < 0)
    {
        printf("Connect FAILED\n");

        return false;
    }

    DNSPacket out_packet = DNSPacket();

    char true_packet[sizeof(out_packet) + 1];

    memcpy(true_packet, &out_packet, sizeof(out_packet));

    true_packet[sizeof(out_packet)] = 0x0;

    if(send(outbound_socket, &true_packet, sizeof(out_packet) + 1, 0) < 0)
    {
        printf("Send FAILED\n");

        return false;
    }

    printf("packet size %d\n", sizeof(Query::DNSPacket));

    return true and listen_and_check_result();
}


bool Query::listen_and_check_result() const
{
    char recv_buffer[1024];

    recv(outbound_socket, recv_buffer, sizeof(Query::DNSPacket), 0);

    if(strlen(recv_buffer))

        printf("%s\n", recv_buffer);

    return true;
}


sockaddr_in Query::address_object_factory(const char* ip_address, int port)
{
    struct sockaddr_in address_object;

    address_object.sin_addr.s_addr = inet_addr(ip_address);

    address_object.sin_family = AF_INET;

    address_object.sin_port = htons(port);

    return address_object;
}


int main()
{
    Query query = Query();

    sockaddr_in dest = Query::address_object_factory("8.8.8.8", 53);

    query.is_working(dest);

    return 0;
}

