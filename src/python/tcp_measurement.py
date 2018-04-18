'''
This module measures the DNS resolution with TCP
on genuine open resolvers
'''
import csv
import subprocess

# import scapy.all as network

def load_from_server_log(filename="server_logger.csv"):
    with open(filename) as file_handler:
        reader = csv.DictReader(file_handler)
        
        for lines in reader:
            if lines["Status"] == "Open Resolver":
                yield lines["IP Address"]


def check_all_mode(ip_address:str) -> None:
    try:
        print("-----------------------------------")
        print("On IP Address {}".format(ip_address))
        for mode in ("one", "medium", "oversize", "jumbo"):
            print_wrapper("check on mode {}...".format(mode), status="OK")
            result =\
            subprocess.check_output(
                "dig {}.yumi.ipl.eecs.case.edu @{}"\
                .format(mode, ip_address)\
                .split(" ")
            ).decode()
            check_dig_output(result, mode=mode)
    
    except subprocess.CalledProcessError as e:
        print_wrapper("dig return code is {}".format(e.returncode), status="FAILED")
        


def check_dig_output(output, mode="one"):
    split_lines = output.split("\n")
    mode_string = "[Mode: {}]".format(mode)
    if "status: NOERROR" in output:
        print_wrapper(mode_string+"dig return code is 0", status="OK")
    
    if mode == "one":
        ip_address_range = ["198.168.2.16"] #??????????????????????????

    elif mode == "medium":
        ip_address_range = ["192.168.2.{}".format(num) for num in range(1, 9)]

    elif mode == "oversize":
        ip_address_range = ["192.168.0.{}".format(num) for num in range(1, 33)]

    elif mode == "jumbo":
        ip_address_range = ["192.168.3.{}".format(num) for num in range(1, 129)]

    records_num = len(ip_address_range)

    try:
        for index, lines in enumerate(split_lines):
            if ";; ANSWER SECTION:" in lines:
                for lines in split_lines[index+1: index+records_num+1]:
                    if lines.split()[-1] in ip_address_range:
                        ip_address_range.remove(lines.split()[-1])

                if len(ip_address_range) == 0:
                    print_wrapper(mode_string+"Has Enough Records ({} records)".format(records_num), status="OK")
                
                else:
                    print_wrapper(mode_string+"Does not have enough Records ({} out of {} records)"\
                    .format(len(ip_address_range) - records_num, records_num), status="OK")
                return

        print_wrapper(mode_string+"Illegal Output (Has no Answer Section)", status="FAILED")

    except (ValueError, TypeError, IndexError) as e:
        print(e)
        print_wrapper(mode_string+"Cannot recognize the output?????? (wtf is this)", status="FAILED")

    


def print_wrapper(msg, status="OK"):
    reset = '\033[0m'
    red   = '\033[31m'
    green = '\033[32m'

    if status == "OK":
        print("{}{:60} ------- [OK]{}".format(green, msg, reset))
    elif status == "FAILED":
        print("{}{:60} ------- [FAILED]{}".format(red, msg, reset))


if __name__ == "__main__":
    for line in load_from_server_log():
        check_all_mode(line)