# include "Query.h"
# include "Packet.h"

int main()
{
    // int test_socket = socket(AF_INET, SOCK_DGRAM, 0);
    
    // Packet p = Packet();

    // p.setQuestion("rcm.amazon.com");

    // int packetLength = 0;

    // char* rawPacket = p.pack(packetLength);

    // sockaddr_in target = Query::addressObjectFactory("129.22.4.33", 53);

    Query q = Query("8.8.8.8", "8.8.8.255");

    q.launchQuery();
}