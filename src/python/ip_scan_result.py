'''
ip_scan_result.py

This implement the result object, which collects the result from queries and
output to a csv
'''

import glob
import os

import MySQLdb
import _mysql_exceptions

def merge_files(final_output:str, file_pattern:str):
    '''
    merge all the files into one single output
    '''
    file_lists = glob.glob(file_pattern)

    with open(final_output, "w") as file_output:

        for file_index in range(len(file_lists)):
            with open(file_lists[file_index], "r") as single_input:
                if file_index != 0:   
                    single_input.__next__() 

                for line in single_input:
                    file_output.write(line)

            os.remove(file_lists[file_index])

class Result(object):

    def __init__(self, threshold=20, output_file=None):

        self.__output_file = output_file if output_file else "dns_output.csv"
        self.__result_list = []
        self.__threshold   = threshold

        self.__file_existed = False

        self.__database = MySQLdb.connect("localhost", "root", "", "dns_scan_records")
        self.__database.autocommit(True)
        self.__master_cursor = self.__database.cursor()
        self.__master_cursor.execute("TRUNCATE TABLE result")

    def append_result(self, list_of_result:list) -> None:
        '''
        append results to the output list, waiting to be flushed
        '''
        self.__result_list.append(
            {
                "IP address"        : list_of_result[0],
                "DNS Packet Length" : list_of_result[1],
                "Response Status"   : list_of_result[2],
                "Time"              : list_of_result[3]
            }
        )

        query = '''INSERT INTO result
        (
            ip_address,
            packet_length,
            response_status,
            response_time
        )
        VALUES
        (
            "{ip}",
            {pack_len},
            "{status}",
            "{time_}"
        )
        '''.format(
            ip       = list_of_result[0],
            pack_len = list_of_result[1],
            status   = list_of_result[2],
            time_    = list_of_result[3]
        )
        try:
            self.__master_cursor.execute(query) 
        except _mysql_exceptions.IntegrityError:
            self.__database.rollback()

        if len(self.__result_list) == self.__threshold:
            self.__flush()
            self.__result_list.clear()


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
        header = ["IP address", "DNS Packet Length", "Response Status", "Time"]

        if not self.__file_existed:
            with open(self.__output_file, "w") as out:
                out.write(",".join(header) + "\n")
                
                for members in self.__result_list:
                    out.write(",".join([members["IP address"], members["DNS Packet Length"], members["Response Status"], members["Time"]]) + "\n")

                self.__file_existed = True

        else:
            with open(self.__output_file, "a") as out:
                for members in self.__result_list:
                    out.write(",".join([members["IP address"], members["DNS Packet Length"], members["Response Status"], members["Time"]]) + "\n")

    def __del__(self):
        self.__database.close()

        if len(self.__result_list) > 0:
            self.__flush()

