#!/bin/bash
# bruce.jikun@gmail.com 2019/01/02 11:04


for i in $(ls /proc | grep "^[0-9]" | awk '$0>100'); do
	awk '/Swap:/{a=a+$2}END{print '"$i"',a/1024"M"}' /proc/$i/smaps 2>/dev/null
done | sort -k2nr | head