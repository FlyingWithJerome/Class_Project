'''
server_side_listener.py

listen the query from the client and record the valid
sender
'''

import atexit
import csv

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import socket

from threading import Thread

import ipaddress
import select
import struct

import scapy.all as network

import ip_scan_packet

class ServerSiderListener(Thread):

    def __init__(self, logger="server_logger.csv"):
        Thread.__init__(self)

        if not logger.endswith("csv"):
            raise ValueError("should end with csv")

        self.__logger_name = logger
        self.__raw_logger  = open("server_logger.csv", "w")

        header = ["IP Address", "Status"]
        self.__csv_handler = csv.DictWriter(self.__raw_logger, fieldnames=header)
        self.__csv_handler.writeheader()

        self.__input_socket  = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.__input_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, True)
        self.__input_socket.setblocking(0)
        self.__input_socket.bind(("", 53))

        # self.daemon = True

    @staticmethod
    def get_question_section(packet:bytes) -> str:

        # beautiful_dns = ip_scan_packet.read_dns_response(packet)
        # return beautiful_dns["Queries"][0]
        beautiful_dns = network.IP(packet)

        return beautiful_dns[network.DNS][network.DNSQR].qname.decode()


    @staticmethod
    def get_source_address(packet:bytes) -> str:
        '''
        find the source address of an IP packet
        '''
        ip_header = struct.unpack('!BBHHHBBHII', packet[:20])
        source_ip = struct.pack("!I", ip_header[8])

        return str(ipaddress.IPv4Address(socket.inet_ntoa(source_ip)))

    def run(self):
        self.__listen()

    def __listen(self):
        is_working = True
        while(is_working):
            try:
                [read], write, expt = select.select([self.__input_socket],[],[], 1)
                data = read.recv(1000)
                source   = ServerSiderListener.get_source_address(data[:20])
                question = ServerSiderListener.get_question_section(data)

                if not "yumi" in question:
                    continue
                question_ip = str(question.split(".")[0])
                print("question IP:", question_ip)
                if question_ip.split("-") == source.split("."):
                    self.__csv_handler.writerow(
                        {
                        "IP Address" : ".".join(question_ip.split("-")),
                        "Status"     : "Open Resolver"
                        }
                    )
                else:
                    self.__csv_handler.writerow(
                        {
                        "IP Address" : ".".join(question_ip.split("-")),
                        "Status"     : "Forwarder"
                        }
                    )
    
            except (ValueError, TypeError, IndexError) as e:
                print(e)
                pass
            except KeyboardInterrupt:
                is_working = False
        
        # self.__finalize()

    def finalize(self):
        print("finalizing...")
        # with open(self.__logger_name, "w") as file_output:
        #     file_output.write(self.__raw_logger.getvalue())
        
        self.__raw_logger.close()
        self.__input_socket.close()

if __name__ == "__main__":
    try:
        listener_a = ServerSiderListener()
        atexit.register(listener_a.finalize)
        listener_a.start()
    except KeyboardInterrupt:
        pass

