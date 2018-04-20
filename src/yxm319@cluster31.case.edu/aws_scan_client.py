import sys
import socket
import time
from scapy.all import DNS
from scapy.all import DNSQR
from scapy.all import IP
from scapy.all import UDP
from scapy.all import send
import ip_scan_packet as self_dns

host = '18.188.87.197'
port = 53

if __name__ == '__main__':
    out_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP);

    out_packet = self_dns.make_dns_packet("test.dns");

    start = time.time();

    count = 0;
    try:
        while True:
            out_socket.sendto(out_packet,(host,port));
            count = count + 1;
            now = time.time();
            if((now-start)>1):
                start = now;
                print("Packet sent in last second: ",count);
                count = 0;
    except Exception as e:
        print(e);
        out_socket.close();