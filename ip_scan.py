import socket
import ipaddress
import subprocess
import sys

SKIP_LIST = [int(ipaddress.IPv4Address("0.0.0.0")),
		range(int(ipaddress.IPv4Address("192.168.0.1")),int(ipaddress.IPv4Address("192.168.255.255"))),
		int(ipaddress.IPv4Address("127.0.0.1"))]

def call_dig(server:int) -> str:
	print("dig case.edu @{}".format(str(ipaddress.IPv4Address(server))).split())
	return subprocess.check_call("dig case.edu @{}".format(str(ipaddress.IPv4Address(server))).split())


#16777217
def main() -> None:
	start_ip = int(ipaddress.IPv4Address(sys.argv[1]))
	end_ip = int(ipaddress.IPv4Address(sys.argv[2]))
	for num in range(start_ip,end_ip):
		flag = True
		for banned in SKIP_LIST:
			if isinstance(banned,range) and num in banned:
				flag = False
				break
			elif num == banned:
				flag = False
				break
		if (flag):
			try:
				print(call_dig(num))
			except:
				print("Failed!")
	


if __name__ == "__main__":
	main()

