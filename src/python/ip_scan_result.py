'''
ip_scan_result.py

This implement the result object, which collects the result from queries and
output to a csv
'''

import csv

class Result(object):

    def __init__(self, threshold=100, output_file=None):

        self.__output_file = output_file if output_file else "dns_output.csv"
        self.__result_list = []
        self.__threshold   = threshold

        self.__file_existed = False

    def append_result(self, list_of_result:list) -> None:
        '''
        append results to the output list, waiting to be flushed
        '''
        self.__result_list.append(
            {
                "IP address"       : list_of_result[0],
                "DNS Packet Length": list_of_result[1],
                "Status"           : list_of_result[2],
            }
        )

        if len(self.__output_file) == self.__threshold:
            self.__flush()
            del self.__result_list[:]


    def __add__(self, another):
        assert isinstance(another, Result), "both of them should be Result object"
        self.__result_list += another.__result_list

        return self

    def __iadd__(self, another):
        assert isinstance(another, Result), "both of them should be Result object" 
        self.__result_list += another.__result_list

        return self

    def __flush(self) -> None:
        '''
        flush the output to the csv file
        '''
        header = ["IP address", "DNS Packet Length", "Status"]

        if not self.__file_existed:
            with open(self.__output_file, "w") as out:
                output_csv = csv.DictWriter(out, fieldnames=header)
                output_csv.writeheader()
                output_csv.writerows(self.__result_list)

                self.__file_existed = True

        else:
            with open(self.__output_file, "a") as out:
                output_csv = csv.DictWriter(out, fieldnames=header)
                output_csv.writeheader()
                output_csv.writerows(self.__result_list)

    def __del__(self):
        if len(self.__result_list) > 0:
            self.__flush()

