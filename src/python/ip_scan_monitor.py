'''
ip_scan_monitor.py

This module monitors the outgoing traffic from certain ports
It can also generate a graph for visualization
'''

import scapy.all
import matplotlib
import numpy

import matplotlib.pyplot as plt
plt.switch_backend('agg')


class Monitor(object):

    def __init__(self):

        self.__sent_rate     = 0
        self.__timeval       = 1

        self.__self_ip       = "129.22.150.112"
        self.__result_list   = []

    def __sniff_callback(self, packet):
        if 2048 <= packet[scapy.all.UDP].sport <= 2058:
            self.__sent_rate += 1

    def __sniff(self):
        while(True):
            scapy.all.sniff(filter="udp", iface="eth0", prn=self.__sniff_callback, timeout=self.__timeval)
            self.__result_list.append(self.__sent_rate)

            if all(m == 0 for m in self.__result_list[-10:]): break

            self.__sent_rate = 0

        self.__generate_graph()

        print("Monitor Exiting...")

    def sniff_sniff(self):
        return self.__sniff()

    def __generate_graph(self):
        with plt.style.context('ggplot', after_reset=True):

            title_font = {"fontname":"Helvetica", "fontsize":14}
            body_font  = {"fontname":"Helvetica"}

            plt.title("Packet Sent Rate Change \n(Avg Rate: %d Packet/Sec, Max Rate: %d Packet/Sec)"\
            %(int(numpy.average(self.__result_list[:-10])), int(max(self.__result_list))), **title_font)


            plt.xlabel("Timeline (sec)", **body_font)
            plt.ylabel("Packet Sent Rate (packet/sec)", **body_font)

            plt.plot(list(range(len(self.__result_list))), self.__result_list, label="DNS Packet Sent Rate In eth0 Interface (packet/sec)")
            plt.legend(loc='upper right')

            plt.savefig("sent_rate.png", dpi=300)
