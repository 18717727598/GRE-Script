#!/bin/bash
# bruce.jikun@gmail.com 2018/12/03 11:02

#For CentOS6.X
read -p "Show me the host names: (Ex: sh-jaas-jenkins-all-online-01)" hostnames ;
oldhostname=`hostname`
realip=`ip a | grep inet | grep brd | awk -F ' ' '{print $2}' | awk -F '/' '{print $1}'`

sed -i '/HOSTNAME/d' /etc/sysconfig/network
echo -e "HOSTNAME=$hostnames" >> /etc/sysconfig/network
sed -i "/$oldhostname/d" /etc/hosts
echo -e "$realip    $hostnames" >> /etc/hosts
hostname $hostnames
