
import numpy as np
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

if __name__ == '__main__':
	data_count = 0;
	data = [];

	with open('cap.txt','r') as f:
		for line in f:
			if 'Actual Stats:' in line:
				ePos = line.index('pps')-1;
				sPos = ePos;
				for i in range(ePos,0,-1):
					if(line[i] == '['):
						sPos = i+1;
						break;
				#print(data_count)
				data.append(float("".join(line[sPos:ePos].split('\'')))) ;
				data_count = data_count + 1;

	
	plt.plot(list(range(0,data_count)),data);
	plt.xlabel('Time (s)');
	plt.ylabel('Packets sending rate (pkt/s)');
	plt.title('Packets sending rate change with time');
	plt.savefig("cap_fig.png");
	print(data);
