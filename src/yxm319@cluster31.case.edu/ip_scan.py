# -*- coding: utf-8 -*-
#!/bin/python3

'''
ip_scan.py

This is used to query all IPv4 address for DNS resolution
Quering is conducted in ip_scan_query.py
Result formatting is conducted in ip_scan_result.py
'''
import atexit
import smtplib
import argparse
import time


from email.message import EmailMessage
from email.header import Header
from email.mime.text import MIMEText

from ip_scan_query import MultiprocessQuery
from ip_scan_result import merge_files

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

    return parser.parse_args()


def send_mail_notice():

    with open("mail_notice.txt") as configure:
        try:
            [user, passwd, receiver] = configure.readlines()
        except:
            return

    message = [
        "Subject: =?utf-8?b?U2VucGFpLCDjgbLjgajjgaTjgYrjga3jgYzjgYTjgZTjgajjgYzjgYLjgovjgpPjgafjgZk=?=",
        "From: {}".format(user),
        "Scanning Finished! Check your error message or csv output"
    ]

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user, passwd)
    server.sendmail(user, receiver, "\r\n".join(message))
    server.quit()

def main_entry():
    '''
    The entry of the scanner
    '''

    options = parse_arguments()

    start_ip = getattr(options, "Start IP Address")
    end_ip   = getattr(options, "End IP Address")
    process_num  = getattr(options, "Number of Processes")

    args = \
    {
        "start_ip"   : start_ip[0],
        "end_ip"     : end_ip[0],
        "process_num": process_num
    }

    time_a = time.time()

    query_object = MultiprocessQuery(**args)
    query_object.run()

    print("END Time Elapsed: %6.2f seconds"%(time.time() - time_a))

    print("Merging Outputs...")
    merge_files("scan_output.csv", "dns_result_*.csv")


if __name__ == "__main__":
    main_entry()
