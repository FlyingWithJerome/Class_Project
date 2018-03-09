'''
ip_scan_result.py

This implement the result object, which collects the result from queries and
output to a csv
'''

import csv

class Result(object):

    def __init__(self, output_file=None):

        self.output_file = output_file if output_file else "dns_output.csv"
        self.result_list = []

    def append_result(self, list_of_result:list) -> None:
        '''
        append results to the output list, waiting to be flushed
        '''
        self.result_list.append(
            {
                "IP address"    : list_of_result[0],
                "TCP Connection": list_of_result[1].startswith("tcp"),
                "Trace"         : list_of_result[2].startswith("trace"),
                "Result"        : list_of_result[3]
            }
        )

    def __add__(self, another):
        assert isinstance(another, Result), "both of them should be Result object"
        self.result_list += another.result_list

        return self

    def __iadd__(self, another):
        assert isinstance(another, Result), "both of them should be Result object" 
        self.result_list += another.result_list

        return self

    def flush(self) -> None:
        '''
        flush the output to the csv file
        '''
        header = ["IP address", "TCP Connection", "Trace", "Result"]
   
        with open(self.output_file, "w") as out:
            self.output_csv = csv.DictWriter(out, fieldnames=header)
            self.output_csv.writeheader()
            self.output_csv.writerows(self.result_list)

