import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

time_list = [];
num_list = [];
with open('scan_output.csv','r') as file:
    title = file.readline();
    line = file.readline()
    while len(line):
        line = line.split(',')
        time = float(line[3])
        time = int(time)
        if(time in time_list):
            pos = time_list.index(time)
            num_list[pos] = num_list[pos] + 1
        else:
            time_list.append(time)
            num_list.append(1)
        line = file.readline()
    # for i in range(len(time_list)):
    #     print(time_list[i],"  ",num_list[i])
    overall = list(zip(time_list,num_list))
    overall.sort(key=lambda x:x[0])

    plt.plot([x[0] for x in overall],[x[1] for x in overall])
    
    plt.savefig('scan_output.png')