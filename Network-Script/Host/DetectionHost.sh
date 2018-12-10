#!/bin/bash
# bruce.jikun@gmail.com 2018/11/20 16:18


read -p "Show me the target network: (Ex:192.168.0.1/24)" ips ;

fping -4 -q -a $ips -g > alivehost.txt
fping -4 -q -u $ips -g > deadhost.txt
