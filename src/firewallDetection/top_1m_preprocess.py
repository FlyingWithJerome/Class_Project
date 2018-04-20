
import concurrent.future
import sys
import csv
import subprocess

def wrapper(webname:[str]) -> [[str, str, str],]:
    results = []
    for name in webname:
        try:
            nameserver_str = subprocess.check_output(["dig",name,"NS","+short"]).decode().split("\n")[0]
            if nameserver_str:
                nameserver_ip = subprocess.check_output(["dig",shell_output1,"+short"]).decode().split("\n")[0]\
                if nameserver_ip:
                    results.append([name, nameserver_str, nameserver_ip])
                    
        except subprocess.CalledProcessError:
            pass

    return results

if __name__ == '__main__':
    namelist = [];
    with open('top-1m.csv','r') as csvfile, open('top-3m.csv','w') as csvwrite:
        csvreader = csv.reader(csvfile);
        csvwriter = csv.writer(csvwrite);
        for row in csvreader:
            namelist.append(row[1]);

        order = 1;
        for name in namelist:
            try:
                print("Trying1:", name);
                shell_output1 = (subprocess.check_output(["dig",name,"NS","+short"]).decode()).split("\n")[0];
                print("Trying2:", shell_output1)
                if (shell_output1):
                    shell_output2 = (subprocess.check_output(["dig",shell_output1,"+short"]).decode()).split("\n")[0];
                    csvwriter.writerow([str(order),name,shell_output1,shell_output2]);
                    order = order + 1;
                    print("Order ",order," success!");
                pass;
            except Exception as e:
                print(type(e));



