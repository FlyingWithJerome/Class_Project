'''
client_side_sender.py

this module simply takes a csv log of valid DNS resovlers
and keep send packets to them
'''

import csv
import socket
import struct
import sys
import time

import ip_scan_packet

class ClientSideSender(object):

    def __init__(self, log=""):

        if not log:
            raise ValueError("Should provide a log directory")
        else:
            self.__file_handler = open(log, "r")
        
        self.__csv_handler   = csv.DictReader(self.__file_handler)
        self.__outbound_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__outbound_sock.bind(("", 2048))
        self.__outbound_sock.setblocking(0)

        self.__cleaned = False 

    def __cleanup(self):
        '''
        close all open sources
        '''
        self.__file_handler.close()
        self.__outbound_sock.close()

        self.__cleaned = True

    def start(self):
        self.__send_to_server()

    def __send_to_server(self):
        for entry in self.__csv_handler:
            if entry["Response Status"] == "No Error":
                ip_address = entry["IP address"]
            else:
                continue

            question = ClientSideSender.translate_name(ip_address=ip_address)
            packet   = ip_scan_packet.make_dns_packet(question)

            self.__outbound_sock.sendto(packet, (ip_address, 53))
            time.sleep(0.002)# limit speed to 500 pps
            print("IP", ip_address, "Done...")
        
        self.__cleanup()

    # @staticmethod
    # def spoof_header(packet) -> bytes:
    #     '''
    #     rewrite the UDP header so that the response will be
    #     sent to another socket
    #     '''
    #     length = 8 + len(packet)
    #     udp_header = struct.pack("!4H", 2048, 53, length, 0)

    #     return udp_header + packet

    @staticmethod
    def translate_name(basename="yumi.ipl.eecs.case.edu", ip_address="0.0.0.0"):
        return "-".join(ip_address.split(".")) + "." + basename

    def __del__(self):
        if not self.__cleaned:
            self.__cleanup()

if __name__ == "__main__":
    client = ClientSideSender(log=sys.argv[1])
    client.start()