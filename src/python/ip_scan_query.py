'''
ip_scan_query.py

This module implements all network quering related
actions, include:

- Class
    1. Query (single quering)
    2. MultiprocessQuery (quering with multiprocess)
    3. SkipList (check if skip ipaddress)
'''

import concurrent.futures
import ipaddress
import select
import socket
import subprocess
import struct
import time

import numpy as np

import self_dns
from ip_scan_result import Result

class Query(object):
    '''
    This class does quering in a single process
    '''
    def __init__(self, port_num:int, start_ip=None, end_ip=None):

        if type(start_ip) != type(end_ip):
            raise ValueError("IP range has to be None or integers")
    
        if start_ip is None:
            start_ip = ipaddress.IPv4Address('0.0.0.0')
            end_ip   = ipaddress.IPv4Address('255.255.255.255')
        else:
            start_ip = ipaddress.IPv4Address(start_ip)
            end_ip   = ipaddress.IPv4Address(end_ip)

        self.__ip_range = range(int(start_ip), int(end_ip))

        self.__prepare_socket_factory(port_num)

        self.hostname    = "email-jxm959-case-edu.ipl.eecs.case.edu"
        self.ip_address  = "198.168.2.16"
        self.__packet    = self_dns.make_dns_packet()
        self.__udp_spoofing(port_num)

        self.output_object = Result()


    def __prepare_socket_factory(self, port_num:int) -> None:
        '''
        factory function for building a pair of UDP socket,
        input socket is non-blocking
        '''
        self.__output_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.__input_socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.__input_socket.setblocking(0)

        self.__input_socket.bind(('', port_num))

    def __udp_spoofing(self, port_number:int):
        '''
        rewrite the UDP header to that the response will be
        sent to another socket
        '''
        destination_port = 53
        length = 8 + len(self.__packet)

        udp_header = struct.pack("!4H", port_number, destination_port, length, 0)
        self.__packet = udp_header + self.__packet


    def __set_dig_option(self, tcp=False, trace=False) -> None:
        '''
        set the dig command options
        '''
        self.tcp_option   = "tcp"   if tcp   else "notcp"
        self.trace_option = "trace" if trace else "notrace"

    
    def __launch_query(self, ip_address:ipaddress.IPv4Address) -> None:
        '''
        send one packet to the ip_address
        '''
        # self.__output_socket.sendto(self.__packet, (str(ip_address), 53))

        self.__output_socket.sendto(self.__packet, (str("8.8.8.8"), 53))
        self.__output_socket.sendto(self.__packet, (str("114.114.114.114"), 53))


    def __read_from_socket(self, timeout=2):
        '''
        selecting/polling the socket until timeout
        '''
        while(True):
            try:
                [read], write, expt = select.select([self.__input_socket],[],[], timeout)
                data = read.recv(1000)

                print("I get these: %d"%(len(data)))
                
            except (KeyboardInterrupt, ValueError):
                break

        
    def launch_query(self, range_=None) -> Result:
        '''
        Nothing exciting, just a loop
        '''
        skip_list = SkipList()
        
        ip_range = self.__ip_range if not range_ else range_
            
        try:
            for ip in ip_range:
                if skip_list.is_valid(ipaddress.IPv4Address(ip)):
                    self.__launch_query(ipaddress.IPv4Address(ip))

            self.__read_from_socket()

        except KeyboardInterrupt:
            pass

        return self.output_object


    # def check_stdoutput(self, output_string:str) -> str:
    #     '''
    #     check if the output is what we want
    #     '''
    #     if output_string:

    #         if ";; ANSWER SECTION:" not in output_string and self.trace_option != "trace":
    #             return "Execution OK, Not Returning Answer"

    #         if "IN A" in output_string and self.ip_address not in output_string:
    #             return "Execution OK, Returning Wrong Answer"

    #         if self.ip_address in output_string:
    #             return "Execution OK, Answer OK"

    #     else:
    #         return "Unknown Error"

    def __del__(self):
        self.__output_socket.close()

        self.__input_socket.close()


class MultiprocessQuery(object):
    
    def __init__(self, start_ip:str, end_ip:str, process_num=4):
        self.process_num = process_num
        assert start_ip and end_ip, "start ip and end ip should not be empty"

        start_ip = int(ipaddress.IPv4Address(start_ip))
        end_ip   = int(ipaddress.IPv4Address(end_ip))

        # split ip intervals for each workers
        breakpoints = self.__assign_jobs(start_ip, end_ip, process_num)

        self.job_assignment = [
            {
                "port_num" : 2048 + i,
                "start_ip" : int(breakpoints[i]), 
                "end_ip"   : int(breakpoints[i+1]), 
            } 
            for i in range(len(breakpoints)-1)]

        self.empty_result = Result()        


    @staticmethod
    def query_wrapper(kwargs):
        '''
        A simple wrapper for Query object. This is to be used
        by the process pool (to be pickled, possibly)
        '''
        query_obj = Query(**kwargs)
        return query_obj.launch_query()


    def __assign_jobs(self, start_ip:int, end_ip:int, workers:int) -> [int]:
        '''
        try to assign jobs to processes
        '''
        step_length = (end_ip - start_ip + 1) // workers
        remaining   = (end_ip - start_ip + 1) % workers
        breakpoints = [start_ip,]
        
        while len(breakpoints) < workers + 1:

            if len(breakpoints) <= remaining:
                next_point = breakpoints[-1] + step_length + 1
            else:
                next_point = breakpoints[-1] + step_length
            breakpoints.append(next_point)

        return breakpoints


    def run(self):
        '''
        execute the jobs concurrently and write the results to
        a csv file
        '''
        with concurrent.futures.ProcessPoolExecutor(self.process_num) as master:
            job_query = [master.submit(MultiprocessQuery.query_wrapper, arg) 
                        for arg in self.job_assignment]
            
            for outputs in concurrent.futures.as_completed(job_query):
                self.empty_result += outputs.result()

            self.empty_result.flush()



class SkipList(object):

    skip_list = \
        [
            ipaddress.IPv4Network("0.0.0.0/8"),
            ipaddress.IPv4Network("10.0.0.0/8"),
            ipaddress.IPv4Network("100.64.0.0/10"),
            ipaddress.IPv4Network("127.0.0.0/8"),
            ipaddress.IPv4Network("169.254.0.0/16"),
            ipaddress.IPv4Network("172.16.0.0/12"),
            ipaddress.IPv4Network("192.0.0.0/24"),
            ipaddress.IPv4Network("192.0.2.0/24"),
            ipaddress.IPv4Network("192.88.99.0/24"),
            ipaddress.IPv4Network("192.168.0.0/16"),
            ipaddress.IPv4Network("198.18.0.0/15"),
            ipaddress.IPv4Network("198.51.100.0/24"),
            ipaddress.IPv4Network("203.0.113.0/24"),
            ipaddress.IPv4Network("224.0.0.0/4"),
            ipaddress.IPv4Network("240.0.0.0/4"),
            ipaddress.IPv4Network("255.255.255.255")
        ] 

    def remove_address(self, ip_address:ipaddress.IPv4Address):
        '''
        remove an address from the skip list
        '''
        try:
            SkipList.skip_list.remove(str(ip_address))
        except ValueError:
            pass


    def is_valid(self, ip_address:ipaddress.IPv4Address):
        '''
        check if an address is in skip list
        '''
        for tricky_ip in SkipList.skip_list:
            if ip_address in ipaddress.IPv4Network(tricky_ip):
                return False
        return True


if __name__ == "__main__":

    # time_a = time.time()

    # mq = MultiprocessQuery(start_ip="129.22.104.25", end_ip="129.22.104.35")
    # mq.run()

    # print("Time Elapsed: %6.2f seconds"%(time.time() - time_a))
    q = Query(2048)
    q.launch_query(["8.8.8.8", "114.114.114.114"])
