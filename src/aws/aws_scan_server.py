import sys
import socket
import time
import scapy
import ip_scan_packet as self_dns

host = ''
port = 53

if __name__ == '__main__':
    in_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP);

    in_socket.bind((host,port));

    start = time.time();

    count = 0;
    while True:
        data = in_socket.recv(1024);
        dns_packet = DNS(data);
        qname = dns_packet[DNSQR].qname.decode();

        if(qname == 'test.dns'):
            count = count + 1;
            now = time.time();
            if((now-start)>1):
                start = now;
                print("Packet rcvd in last second: ",count);
                count = 0;
