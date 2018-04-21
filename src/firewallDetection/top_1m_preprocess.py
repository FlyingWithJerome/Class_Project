
import concurrent.futures
import sys
import csv
import subprocess

def wrapper(webname:[str]) -> [[str, str, str],]:
    results = set()
    for name in webname:
        try:
            nameserver_str = subprocess.check_output(["dig",name,"NS","+short"]).decode().split("\n")[0]
            if nameserver_str:
                nameserver_ip = subprocess.check_output(["dig",nameserver_str,"+short"]).decode().split("\n")[0]
                if nameserver_ip:
                    results.add((name, nameserver_str, nameserver_ip))

        except subprocess.CalledProcessError:
            pass

    return tuple(results)

if __name__ == '__main__':
    namelist = [];
    with open('top-1m.csv','r') as csvfile, open('top-3m.csv','w') as csvwrite:
        csvreader = csv.reader(csvfile);
        csvwriter = csv.writer(csvwrite);
        for row in csvreader:
            namelist.append(row[1]);
        
        namelist = namelist[:100]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #    everything = [
        #        wrapper(namelist[i:i+int(len(namelist)/10)]) )
        #    ]
            res_list = []
            for i in range(0, len(namelist), int(len(namelist)/10)):
                res = executor.submit(wrapper, namelist[i:i+int(len(namelist)/10)])
                res_list.append(res)

            for members in res_list:
               csvwriter.writerows(members.result())


        # order = 1;
        # for name in namelist:
        #     try:
        #         print("Trying1:", name);
        #         shell_output1 = (subprocess.check_output(["dig",name,"NS","+short"]).decode()).split("\n")[0];
        #         print("Trying2:", shell_output1)
        #         if (shell_output1):
        #             shell_output2 = (subprocess.check_output(["dig",shell_output1,"+short"]).decode()).split("\n")[0];
        #             csvwriter.writerow([str(order),name,shell_output1,shell_output2]);
        #             order = order + 1;
        #             print("Order ",order," success!");
        #         pass;
        #     except Exception as e:
        #         print(type(e));



