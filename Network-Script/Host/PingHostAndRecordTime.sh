#!/bin/bash
#nightrover123@163.com, Fri Sep 27 17:32:49 CST 2019


ping -i 0.2  10.16.168.90 | awk '{ print $0"\t" strftime("%H:%M:%S",systime()) }'