import subprocess
import csv

import random

def main():
    with open("scan_output_17-19.csv") as file_handler:
        our_table = csv.DictReader(file_handler)
        our_table = list(our_table)

        for _ in range(100):
            random_index = random.randrange(0, 10000)

            ip_address = our_table[random_index]["IP address"]

            try:
                result = subprocess.check_output("fpdns -D {}".format(ip_address).split())
                print(result)

            except subprocess.CalledProcessError:
                print("fpdns is fucked!!!!")


if __name__ == "__main__":
    main()