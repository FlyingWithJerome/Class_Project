'''
ip_scan_query.py

This module implements all network quering related
actions, include:

- Class
    1. Query (single quering)
    2. MultiprocessQuery (quering with multiprocessing)
    3. SkipList (check if skip ipaddress)
    4. Listener (listens the results)
'''

import concurrent.futures
import ipaddress
import queue
import select
import socket
import struct
import time
import multiprocessing

import ip_scan_packet
from ip_scan_result import Result
from ip_scan_monitor import Monitor

_BEGIN_SIGNAL = 1
_END_SIGNAL   = 2


def _get_source_address(packet:bytes) -> int:
    '''
    find the source address of an IP packet
    '''
    ip_header = struct.unpack('!BBHHHBBHII', packet[:20])
    source_ip = struct.pack("!I", ip_header[8])

    return socket.inet_ntoa(source_ip)

def query_wrapper(kwargs):
    '''
    A simple wrapper for Query object. This is to be used
    by the process pool (to be pickled, possibly)
    '''
    query_obj = Query(**kwargs)
    return query_obj.launch_query()

def collect_wrapper(kwargs):
    '''
    A simple wrapper for Query object. This is to be used
    by the process pool (to be pickled, possibly)
    '''
    collect_obj = Listener(**kwargs)
    return collect_obj.listen()

def monitor_wrapper(kwargs):
    '''
    A simple wrapper for Query object. This is to be used
    by the process pool (to be pickled, possibly)
    '''
    monitor_obj = Monitor(**kwargs)
    return monitor_obj.sniff_sniff()


class Query(object):
    '''
    This class does quering in a single process
    '''
    def __init__(self, port_num:int, queue_:"return from pipe", start_ip=None, end_ip=None):

        if type(start_ip) != type(end_ip):
            raise ValueError("IP range has to be None or integers")
    
        if start_ip is None:
            start_ip = ipaddress.IPv4Address('0.0.0.0')
            end_ip   = ipaddress.IPv4Address('255.255.255.255')
        else:
            start_ip = ipaddress.IPv4Address(start_ip)
            end_ip   = ipaddress.IPv4Address(end_ip)

        fake_network = [net for net in ipaddress.summarize_address_range(start_ip, end_ip)]

        skip_list = SkipList()
        for net in skip_list.skip_list:
            if fake_network[0].overlaps(net):
                self.__queue.put(_END_SIGNAL)
                exit(-1)

        self.__ip_range = range(int(start_ip), int(end_ip))        

        self.__prepare_socket_factory(port_num)

        self.__packet    = ip_scan_packet.make_dns_packet("one-email-yxm319-case-edu.yumi.ipl.eecs.case.edu")
        self.__udp_spoofing(port_num)

        self.__start_from = ipaddress.IPv4Address(start_ip)
        self.__end_to     = ipaddress.IPv4Address(end_ip) - 1

        self.__queue = queue_

        self.__start_time = time.time()


    def __prepare_socket_factory(self, port_num:int) -> None:
        '''
        factory function for building a pair of UDP socket,
        input socket is non-blocking
        '''
        self.__output_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)    
        self.__output_socket.setblocking(0)

    def __udp_spoofing(self, port_number:int) -> None:
        '''
        rewrite the UDP header so that the response will be
        sent to another socket
        '''
        destination_port = 53
        length = 8 + len(self.__packet)

        udp_header = struct.pack("!4H", port_number, destination_port, length, 0)
        self.__packet = udp_header + self.__packet

    
    def __launch_query(self, ip_address:ipaddress.IPv4Address) -> None:
        '''
        send one packet to the ip_address
        '''
        self.__output_socket.sendto(self.__packet, (str(ip_address), 53))

        
    def launch_query(self, range_=None) -> None:
        '''
        Nothing exciting, just a loop
        '''
        
        ip_range = self.__ip_range if not range_ else range_
            
        try:
            self.__queue.put(_BEGIN_SIGNAL)
            for ip in ip_range:
                # if skip_list.is_valid(ipaddress.IPv4Address(ip)):
                self.__launch_query(ipaddress.IPv4Address(ip))

        except KeyboardInterrupt:
            pass

        self.__queue.put(_END_SIGNAL)

    def __del__(self):
        self.__output_socket.close()

        print("Send {} packets from {} to {} for {:4.2f} s".format(int(self.__end_to)-int(self.__start_from),
            str(self.__start_from),
            str(self.__end_to),
            time.time()-self.__start_time))



class Listener(object):

    def __init__(self, port_number:int, queue_:"return from queue", lock_:"process lock", start_ip=None, end_ip=None):

        self.__input_socket  = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.__input_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, True)

        self.__input_socket.setblocking(0)
        self.__input_socket.bind(('', port_number))

        self.__output_object = Result(output_file="dns_result_{}.csv".format(port_number))

        self.__queue = queue_
        self.__lock  = lock_

        self.__port_num = port_number

        start_ip = ipaddress.IPv4Address(start_ip)
        end_ip   = ipaddress.IPv4Address(end_ip)

        self.__ip_range = range(int(start_ip), int(end_ip))
        
        self.__start_from = str(ipaddress.IPv4Address(start_ip))
        self.__end_to     = str(ipaddress.IPv4Address(end_ip) - 1)

        self.__find_result = 0
        self.__had_cleaned = False
        self.__start_time = time.time()


    def __filter(self, IPaddress:ipaddress.IPv4Network) -> bool:
        '''
        check if the returning message is meaningful
        False: meaningless
        True: meaningful
        '''
        skip = [ipaddress.IPv4Network("129.22.151.0/24"),]
        for meaningless in skip:
            if IPaddress in meaningless:
                return False

        return int(IPaddress) in self.__ip_range


    def __read_from_socket(self, timeout=20) -> None:
        '''
        selecting/polling the socket until timeout
        '''
        while(True):
            try:
                signal = self.__queue.get_nowait()
                if signal == _BEGIN_SIGNAL:
                    break

            except queue.Empty:
                pass

        query_ends = False

        while(True):
            try:
                [read], write, expt = select.select([self.__input_socket],[],[], timeout)
                data = read.recv(1000)
                source = _get_source_address(data)
                
                if self.__filter(ipaddress.IPv4Address(source)):
                    dns_length = len(data) - 28
                    
                    try:
                        status     = ip_scan_packet.read_dns_response(data[28:])["RCode"]

                        self.__output_object.append_result([str(source), str(dns_length), status, str(time.time())])
                    except struct.error:
                        self.__output_object.append_result([str(source), str(dns_length), "Unpack ERROR", str(time.time())])
                    start_time = time.time()
                    self.__find_result += 1

                if not query_ends:
                    signal = self.__queue.get_nowait()
                    if signal == _END_SIGNAL:
                        start_time = time.time()
                    # print("Permit to exit")
                    query_ends = True

                time_now = time.time()

                if query_ends:
                    if (time_now - start_time) > timeout:
                        raise ValueError("BREAK")

            except (KeyboardInterrupt, ValueError):
                if query_ends:
                    self.__clean_up()
                    break
                else: 
                    pass

            except queue.Empty:
                pass

    def listen(self) -> None:
        '''
        begin to listen when receive the signals
        '''   
        self.__read_from_socket()

    def __clean_up(self) -> None:
        '''
        replace __del__ method (not reliable in multiprocess)
        '''
        self.__input_socket.close()
        del self.__output_object
        self.__lock.acquire()
        try:
            print("Listener Range {} -> {} (Bind to port {})\n".format(self.__start_from, self.__end_to, self.__port_num),
                "---------------------------------\n",
                "Find {} valid resolvers\n".format(self.__find_result),
                "---------------------------------\n",
                "Listener Life: %6.2f s\n"%(time.time()-self.__start_time),
                "==================================\n")
            self.__had_cleaned = True

        finally:
            self.__lock.release()
            

    def __del__(self):
        if not self.__had_cleaned:
            self.__clean_up()


class MultiprocessQuery(object):
    
    def __init__(self, start_ip:str, end_ip:str, process_num=4):
        self.process_num = process_num
        assert start_ip and end_ip, "start ip and end ip should not be empty"

        start_ip = int(ipaddress.IPv4Address(start_ip))
        end_ip   = int(ipaddress.IPv4Address(end_ip))

        # split ip intervals for each workers
        breakpoints = self.__assign_jobs(start_ip, end_ip, process_num)

        self.__job_query     = []
        self.__job_collector = []

        lock = multiprocessing.Lock()

        for i in range(len(breakpoints)-1):
            smart_manager = multiprocessing.Manager()
            signal_queue   = smart_manager.Queue()

            self.__job_query.append(
                {
                "port_num" : 2048 + i,
                "queue_"   : signal_queue,
                "start_ip" : int(breakpoints[i]), 
                "end_ip"   : int(breakpoints[i+1])
                })
            self.__job_collector.append(
                {
                "port_number" : 2048 + i,
                "queue_"      : signal_queue,
                "lock_"       : lock,
                "start_ip"    : int(breakpoints[i]), 
                "end_ip"      : int(breakpoints[i+1])
                })


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
        objects = []

        for i in range(len(self.__job_collector)):
            objects.append(multiprocessing.Process(target=collect_wrapper, args=(self.__job_collector[i],)))
            objects.append(multiprocessing.Process(target=query_wrapper, args=(self.__job_query[i],)))

        # monitor_job = multiprocessing.Process(target=monitor_wrapper, args=({},))
        # monitor_job.start()

        for jobs in objects:
            jobs.start()

        for jobs in objects:
            jobs.join()

        # monitor_job.join()


        # for jobs in objects:
        #     jobs.terminate()

    



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
