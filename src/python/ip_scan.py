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
	message = "Tell me, senpai!\0"
	message = bytes(message, "ASCII")

	transaction_id = 0xffff # 2 byte short
	control 	   = 0x0100
	q_counts       = 0x0001
	ans_counts     = 0x0000
	auth_counts    = 0x0000
	add_counts     = 0x0000 # 2 byte short
	type_          = 0x0001 # 2 byte short (A)
	class_         = 0x0001 # 2 byte short (IN)
	query_website  = bytes("\4case\3edu\0", "ASCII")

	format_= "!HH4H%ds2H%ds"%(len(query_website), len(message))

	header = struct.pack("!6H", transaction_id, control, q_counts, ans_counts, auth_counts, add_counts)

	question_section = struct.pack("!%ds2H"%len(query_website), query_website, type_, class_)

	return header + question_section


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



def listen_and_check_response(in_socket: socket.socket, out_socket: socket.socket, packet, ip_address:ipaddress.IPv4Address) -> bool:
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

	out_sock, in_sock = make_datagram_sockets()

	out_sock.bind(("192.168.0.7", 1053))

	out_sock.connect(("8.8.8.8", 53))

	packet = make_dns_packet()

	out_sock.send(packet)
	


if __name__ == "__main__":
	main()

