# include "Query.h"
# include "Packet.h"

int main()
{
    int test_socket = socket(AF_INET, SOCK_DGRAM, 0);
    
    Packet p = Packet();
    p.setQuestion("case.edu");

    char* rawPacket = p.pack();

    sockaddr_in target = Query::addressObjectFactory("8.8.8.8", 53);

    sendto(test_socket, rawPacket, 1000, NULL, (struct sockaddr *)&target, sizeof(target));

}