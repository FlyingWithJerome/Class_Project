import sys
import csv
import socket
import time
import threading 
#from threading import Thread
#from queue import queue
from scapy.all import DNS,DNSQR
import ip_scan_packet as self_dns


class Sender(threading.Thread):
    def __init__(self, website_list:list,transport_socket:socket.socket,threadName='Sender'):
        threading.Thread.__init__(self);
        self.website_list = website_list;
        self.transport_socket = transport_socket;

    def run(self):
        remaining = length;
        start = time.time();
        last_remaining = remaining;
        while remaining:
            out_packet = self_dns.make_dns_packet(self.website_list[length-remaining]);
            self.transport_socket.sendto(out_packet,('8.8.8.8',53));
            remaining = remaining - 1;
            now = time.time()
            if((now-start)>1):
                start = now;
                print("Packet sent in last second:",last_remaining-remaining);
                remaining = last_remaining;
        print("***Packet sending complete.***");

class Receiver(threading.Thread):
    def __init__(self, website_list:list, transport_socket ,threadName='Receiver'):
       threading.Thread.__init__(self);
       self.website_list = website_list;
       self.transport_socket = transport_socket;
    def run(self):
        success = 0;
        remaining = length;
        start = time.time();
        last_remaining = remaining;
        while remaining:
            dns_packet = self.transport_socket.recv(1536);
            dns_packet = DNS(dns_packet);
            qname = dns_packet[DNSQR].qname.decode();
            if qname in self.website_list:
                remaining = remaining - 1;

            now = time.time();
            if((now-start)>1):
                start = now;
                print("Packet rcvd in last second:", last_remaining-remaining);
                remaining = last_remaining;
        print("Packet all recvd");


if __name__ == '__main__':
    namelist = [];
    global length;
    try:
        length = int(sys.argv[1]);
    except:
        length = 10000;
        pass;

    transport_socket = socket.socket(socket.AF_INET, 
        socket.SOCK_DGRAM, socket.IPPROTO_UDP);
    transport_socket.bind(('',2048));

    with open('top-1m.csv','r') as csvfile:
        csvreader = csv.reader(csvfile);
        for row in csvreader:
            namelist.append(row[1]);

    SendingThread = Sender(namelist,transport_socket,"Sender");
    ReceivingThread = Receiver(namelist,transport_socket,"Receiver");

    SendingThread.start();
    ReceivingThread.start();

    threads = [];
    threads.append(SendingThread);
    threads.append(ReceivingThread);

    for t in threads:
        t.join();

    print("Sending complete");