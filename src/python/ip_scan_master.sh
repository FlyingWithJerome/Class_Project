#!/bin/bash

python_execution(){
    sudo python3 ip_scan.py 8.8.8.0 8.8.80.255 5
}


tcp_dump(){
    sudo tcpdump -i eth0 -B 40960 src 129.22.150.112 and udp and dst port 53 > cap.txt
}

python_execution & 
tcp_dump &
wait -n

kill 0