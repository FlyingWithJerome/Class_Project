#!/bin/python3

'''
ip_scan.py

This is used to query all IPv4 address for DNS resolution
Quering is conducted in ip_scan_query.py
Result formatting is conducted in ip_scan_result.py
'''

import argparse
import time

from ip_scan_query import MultiprocessQuery


def parse_arguments():
    '''
    This function helps to parse argument
    from the command line
    '''
    parser = argparse.ArgumentParser(description='Argument Parser for DNS Scanner')
    parser.add_argument("Start IP Address", type=str, nargs=1, 
                        help="The leftmost bound for the scanning range (smallest)")

    parser.add_argument("End IP Address", type=str, nargs=1, 
                        help="The rightmost bound for the scanning range (largest)")

    parser.add_argument("Number of Processes", type=int, nargs="?", default=4, 
                        help="The number of concurrently working processes, default to be 4")

    parser.add_argument("TCP Connection", type=str, nargs="?", default="notcp", 
                        help="Whether to connect with TCP")

    parser.add_argument("Trace Switch", type=str, nargs="?", default="notrace", 
                        help="Whether to resolve from root")

    return parser.parse_args()

def main_entry():
    '''
    The entry of the scanner
    '''
    options = parse_arguments()

    start_ip = getattr(options, "Start IP Address")
    end_ip   = getattr(options, "End IP Address")

    tcp_switch   = getattr(options, "TCP Connection").startswith("tcp")
    trace_switch = getattr(options, "Trace Switch").startswith("trace")
    process_num  = getattr(options, "Number of Processes")

    args = \
    {
        "start_ip"   : start_ip[0],
        "end_ip"     : end_ip[0],
        "tcp"        : tcp_switch,
        "trace"      : trace_switch,
        "process_num": process_num
    }

    time_a = time.time()

    query_object = MultiprocessQuery(**args)
    query_object.run()

    print("Time Elapsed: %6.2f seconds"%(time.time() - time_a))

if __name__ == "__main__":
    main_entry()
