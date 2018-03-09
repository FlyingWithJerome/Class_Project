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
import subprocess
import time

import numpy as np

from ip_scan_result import Result

class Query(object):
    '''
    This class does quering in a single process
    '''
    def __init__(self, start_ip=None, end_ip=None, tcp=False, trace=False):

        if type(start_ip) != type(end_ip):
            raise ValueError("IP range has to be None or integers")
    
        if start_ip is None:
            start_ip = ipaddress.IPv4Address('0.0.0.0')
            end_ip   = ipaddress.IPv4Address('255.255.255.255')
        else:
            start_ip = ipaddress.IPv4Address(start_ip)
            end_ip   = ipaddress.IPv4Address(end_ip)

        self.ip_range = range(int(start_ip), int(end_ip) + 1)

        self.set_dig_option(tcp=tcp, trace=trace)

        self.hostname    = "email-jxm959-case-edu.ipl.eecs.case.edu"
        self.ip_address  = "198.168.2.16"
        self.dig_command = "dig {}".format(self.hostname)

        self.output_object = Result()


    def set_dig_option(self, tcp=False, trace=False) -> None:
        '''
        set the dig command options
        '''
        self.tcp_option   = "tcp"   if tcp   else "notcp"
        self.trace_option = "trace" if trace else "notrace"

    
    def run_dig(self, ip_address:ipaddress.IPv4Address) -> None:
        '''
        the place where dig is executed
        '''
        command_line = self.dig_command + " @{} +{} +{} +time=2"
        command_line = command_line.format(str(ip_address),
                                            self.tcp_option,
                                            self.trace_option)
        
        try:
            raw_output = subprocess.check_output(command_line.split())
            status     = self.check_stdoutput(str(raw_output))

        except subprocess.CalledProcessError as error:
            status = "Execute FAILED, Return Code %d"%(error.returncode)

        self.output_object.append_result([ip_address, 
                                   self.tcp_option,
                                   self.trace_option,
                                   status])

        
    def run_dig_iteratively(self):
        '''
        Nothing exciting, just a loop
        '''
        # skip_list = SkipList()
        # skip_list.remove_address("127.0.0.0/8")
        try:
            for ip in self.ip_range:
                # if skip_list.should_skip(ipaddress.IPv4Address(ip)):
                self.run_dig(ipaddress.IPv4Address(ip))

        except KeyboardInterrupt:
            pass

        return self.output_object


    def check_stdoutput(self, output_string:str) -> str:
        '''
        check if the output is what we want
        '''
        if output_string:

            if ";; ANSWER SECTION:" not in output_string and self.trace_option != "trace":
                return "Execute OK, Not Returning Answer"

            if "IN A" in output_string and self.ip_address not in output_string:
                return "Execute OK, Returning Wrong Answer"

            if self.ip_address in output_string:
                return "Execute OK, Answer OK"

        else:
            return "Unknown Error"


class MultiprocessQuery(object):
    
    def __init__(self, start_ip:str, end_ip:str, process_num=4):
        self.process_num = process_num
        assert start_ip and end_ip, "start ip and end ip should not be empty"

        start_ip = int(ipaddress.IPv4Address(start_ip))
        end_ip   = int(ipaddress.IPv4Address(end_ip))

        self.job_assignment = np.array_split(np.array(range(start_ip, end_ip + 1)), process_num)
        self.job_assignment = [
                                {
                                "start_ip" : int(job[0]), 
                                "end_ip"   : int(job[-1]), 
                                "tcp"      :True, 
                                "trace"    :True
                                } 
                                for job in self.job_assignment]

        self.empty_result = Result()


    @staticmethod
    def query_wrapper(kwargs):
        '''
        A simple wrapper for Query object. This is to be used
        by the process pool (to be pickled, possibly)
        '''
        query_obj = Query(**kwargs)
        return query_obj.run_dig_iteratively()


    def run(self):
        '''
        execute the jobs concurrently
        '''
        with concurrent.futures.ProcessPoolExecutor(self.process_num) as master:
            job_query = [master.submit(MultiprocessQuery.query_wrapper, arg) 
                        for arg in self.job_assignment]
            
            for outputs in concurrent.futures.as_completed(job_query):
                self.empty_result += outputs.result()

            self.empty_result.flush()



class SkipList(object):

    def __init__(self):
        self.skip_list = \
            [
                "0.0.0.0/8",
                "10.0.0.0/8",
                "100.64.0.0/10",
                "127.0.0.0/8",
                "169.254.0.0/16",
                "172.16.0.0/12",
                "192.0.0.0/24",
                "192.0.2.0/24",
                "192.88.99.0/24",
                "192.168.0.0/16",
                "198.18.0.0/15",
                "198.51.100.0/24",
                "203.0.113.0/24",
                "224.0.0.0/4",
                "240.0.0.0/4",
                "255.255.255.255"
            ] 

    def remove_address(self, ip_address:ipaddress.IPv4Address):
        '''
        remove an address from the skip list
        '''
        try:
            self.skip_list.remove(str(ip_address))
        except ValueError:
            pass


    def should_skip(self, ip_address:ipaddress.IPv4Address):
        '''
        check if an address in skip
        '''
        for tricky_ip in self.skip_list:
            if ip_address in ipaddress.IPv4Network(tricky_ip):
                print(tricky_ip)
                return True

        return False


if __name__ == "__main__":

    time_a = time.time()

    mq = MultiprocessQuery(start_ip="129.22.104.25", end_ip="129.22.104.35")
    mq.run()

    print("Time Elapsed: %6.2f seconds"%(time.time() - time_a))
