'''
ip_scan_monitor.py

This module monitors the outgoing traffic from certain ports
It can also generate a graph for visualization
'''

import scapy.all
import matplotlib

import matplotlib.pyplot as plt
plt.switch_backend('agg')


class Monitor(object):

    def __init__(self):

        self.__sent_rate     = 0
        self.__timeval       = 1

        self.__self_ip       = "129.22.150.112"

        self.__invalid_count = 0
        self.__result_list   = []

    def __sniff_callback(self, packet):
        if scapy.all.IP in packet and scapy.all.UDP in packet and packet[scapy.all.IP].src == self.__self_ip:
            self.__sent_rate += 1

    def sniff_sniff(self):
        while(True):
            scapy.all.sniff(iface="eth0", prn=self.__sniff_callback, timeout=self.__timeval)

            if self.__sent_rate == 0:
                self.__invalid_count += 1

            else:
                self.__invalid_count = 0

            self.__result_list.append(self.__sent_rate)

            if self.__invalid_count == 10:
                break

            self.__sent_rate = 0

        self.__generate_graph()

        exit()

    def __generate_graph(self):
        with plt.style.context('ggplot', after_reset=True):

            plt.title("The packet sent rate changes")
            plt.xlabel("Timeline (sec)")
            plt.ylabel("Packet Sent Rate (packet/sec)")

            plt.plot(list(range(len(self.__result_list))), self.__result_list, label="Packet sent rate")
            plt.legend(loc='upper right')
            
            plt.savefig("sent_rate.png", dpi=300)
