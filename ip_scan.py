import socket
import ipaddress
import subprocess
import struct
import sys

SKIP_LIST = [int(ipaddress.IPv4Address("0.0.0.0")),
		range(int(ipaddress.IPv4Address("192.168.0.1")),int(ipaddress.IPv4Address("192.168.255.255"))),
		int(ipaddress.IPv4Address("127.0.0.1"))]


def make_dns_packet():
	'''
	make a customize udp packet (for dns query, carries a message to
	system admins)
	'''
	message = "For a Research @Case Western Reserve, Plz Contact jxm959@case.edu"
	message = bytes(message, "ASCII")


	transaction_id = 0xffff # 2 byte short
	control 	   = 0x0100
	q_counts       = 0x0001
	ans_counts     = 0x0000
	auth_counts    = 0x0000
	add_counts     = 0x0000 # 2 byte short
	query          = 0x0c
	type_          = 0x0001 # 2 byte short (A)
	class_         = 0x0001 # 2 byte short (IN)

	query_website  = bytes("case.edu", "ASCII")

	format_= "!hh4h"





def make_datagram_sockets() -> (socket.socket, socket.socket):
	'''
	make a pair of udp socket with our options
	1. send dns queries
	2. listen responses. 
	'''
	send_socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Produce a UDP DGRAM socket
	recv_socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Produce a UDP DGRAM socket
	# send_socket_instance.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,     255) # Set the TTL to 255

	return send_socket_instance, recv_socket_instance




def listen_and_check_response(in_socket: socket.socket, out_socket: socket.socket, packet, ip_address:ip_address.IPv4Address) -> bool:
	'''
	listen to the server side response and check whether it is a legal &
	valid response
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

