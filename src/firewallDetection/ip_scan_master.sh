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
        pfcount -i eth0 -f "src 129.22.150.112 and udp" >> cap.txt 2>&1
    #    tcpdump -i eth0 -B 40960 src 129.22.150.112 and udp > cap.txt
    else
        sudo pfcount -i eth0 -f "src 129.22.150.112 and udp" >> cap.txt 2>&1
    #    sudo tcpdump -i eth0 -B 40960 src 129.22.150.112 and udp > cap.txt
    fi
}

python_execution &
tcp_dump &
wait -n

python3 ip_scan_draw_fig.py
kill 0