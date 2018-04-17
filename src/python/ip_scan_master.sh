#!/bin/bash

start_ip=$1 
end_ip=$2 
processes=$3
tmux=$4

python_execution(){
    if [ "$tmux" == "tmux" ]; then
        python3 ip_scan.py ${start_ip} ${end_ip} ${processes}
    else
        sudo python3 ip_scan.py ${start_ip} ${end_ip} ${processes}
    fi
}


tcp_dump(){
    rm -f cap.txt
    if [ "$tmux" == "tmux" ]; then
        ./gulp -i eth0 -d | tcpdump -i eth0 -B 40960 src 129.22.150.112 and udp > cap.txt
    else
        sudo ./gulp -i eth0 -d | tcpdump -i eth0 -B 40960 src 129.22.150.112 and udp > cap.txt
    fi
}

python_execution & 
tcp_dump &
wait -n

kill 0
