#!/bin/bash
#nightrover123@163.com, 2019/04/08 AM11:15



read -p "Please input your target DIR: " dir ;


cd ${dir}
#Get all dir names and write to GetAllDIR.txt
ls -lht | awk -F ' ' '{print $NF}' | sed 1d > /tmp/GetAllDIR.txt

while read dirnames; do
	#Get all dir names of single dir,and write to txt
	ls -lht ${dirnames} | awk -F ' ' '{print $NF}' | sed 1d > /tmp/SingleDIR.txt
	tn=`cat /tmp/SingleDIR.txt | wc -l`
	#if tn > 5,do that
	if [[ ${tn} -gt 5 ]]; then
		sed -i '1,5d' /tmp/SingleDIR.txt
		while read singledirs; do
			rm -rf ${dirnames}/${singledirs}
		done < /tmp/SingleDIR.txt
	fi
done < /tmp/GetAllDIR.txt