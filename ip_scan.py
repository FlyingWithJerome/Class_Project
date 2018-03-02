import socket
import ipaddress
import subprocess
import sys

SKIP_LIST = [int(ipaddress.IPv4Address("0.0.0.0")),
		range(int(ipaddress.IPv4Address("192.168.0.1")),int(ipaddress.IPv4Address("192.168.255.255"))),
		int(ipaddress.IPv4Address("127.0.0.1"))]


def make_dns_packet():
	'''
	make a customize udp packet (for dns query, carries a message to
	system admins)
	'''
	pass

def make_datagram_socket() -> socket.socket:
	'''
	make a udp socket with our options. 
	'''
	pass

def send_packet(packet, ip_address:ip_address.IPv4Address) -> None:
	'''
	send a dns packet to the server and wait for response.
	'''
	pass

def multiprocess_scan(start_ip:int, end_ip:int, process_num:int) -> None:
	'''
	scan the IPv4 address space from [start_ip] to [end_ip]
	with [process_num] of processes simultaneously
	'''
	pass


#====================== Private Methods ====================================

def _check_skip_policy(ip_address:int) -> bool:
	pass




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

