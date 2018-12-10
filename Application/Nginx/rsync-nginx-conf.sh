#!/bin/bash
#For backup NGINX Conf DIR,then copy that rsync to anther Server

USER=domain01
IPADDR=10.10.253.252
datetoday=`date +%Y%m%d`
datetime=`date +%Y%m%d%H%M%S`

if [[ ! -d /data/nginx/$datetoday/ ]];then
        mkdir -p /data/nginx/$datetoday/
fi

cd /usr/local/
tar jcf /data/nginx/${datetoday}/`hostname`-$datetime.tar.bz2 nginx/conf >/dev/null 2>&1
sleep 2
cd /data/nginx/
rsync -aR --remove-source-files --password-file=/etc/rsync.pa ${datetoday}/`hostname`-$datetime.tar.bz2 $USER@$IPADDR::nginx/`hostname`
