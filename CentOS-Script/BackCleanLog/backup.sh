#!/bin/sh

logs_dir='
/data/applogs/saas/
'
rsync_server="root@ftp.internal.hsmob.com::saas"
department="jcpt"
hostname=`hostname`
pass_file="/usr/local/script/rsync.pass"
rsync="/usr/bin/rsync  -zrRtopg --bwlimit=5120 --password-file=$pass_file --remove-source-files "

for dir in $logs_dir;
do
    echo "start backup:$dir"
    #echo "find $dir -type f -print0"
    find $dir -mtime +7 -type f -print0 | while read -d '' -r file; do
        echo "/bin/nice -n 19 $rsync $file  $rsync_server/$department/$hostname/"
        /bin/nice -n 19 $rsync $file  $rsync_server/$department/$hostname/
    done
    echo "end backup:$dir"
    echo 
done
