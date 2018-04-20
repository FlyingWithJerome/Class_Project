import sys
import csv
import socket
import threading
from scapy.all import DNS
import ip_scan_packet as self_dns
class Sender(threading.Thread):
    def __init__(self, website_list:list, threadName):
        threading.Thread.__init__(self);
        self.website_list = website_list;

    def run(self):
        out_socket = socket.socket(socket.AF_INET, 
            socket.SOCK_DGRAM, socket.IPPROTO_UDP);
        

class Receiver(threading.Thread):
    def __init__(self, website_list:list, threadName):
       threading.Thread.__init__(self);
       self.website_list = website_list;
    def run(self):
        

if __name__ == '__main__':
    namelist = [];
    with open('top-1m.csv','r') as csvfile:
        csvreader = csv.reader(csvfile);
        for row in csvreader:
            namelist.append(row[1]);


