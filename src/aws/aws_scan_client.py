import sys
import socket
import time
from scapy.all import DNS
from scapy.all import DNSQR
from scapy.all import IP
from scapy.all import UDP
from scapy.all import send

host = '18.188.87.197'
port = 53

if __name__ == '__main__':
    #out_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP);

    out_packet = IP(dst=host)/UDP()/DNS(qd=DNSQR(qname='test.dns',qtype="A"));

    start = time.time();

    count = 0;
    while True:
        send(out_packet,count=1024,verbose=False);
        count = count + 1;
        now = time.time();
        if((now-start)>1):
            start = now;
            print("Packet sent in last second: ",count);
            count = 0;
