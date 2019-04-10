#!/bin/bash
# bruce.jikun@gmail.com 2019/01/16


# This scripts can fix the log, and the log dir like that:
# [root@sh-saas-uc-tagcoresrv-online-02 service]# tree
# .
# ├── service.log
# ├── service.log.2018-12-17
# ├── service.log.2018-12-18
# ├── service.log.2018-12-19
# ├── service.log.2018-12-20
# ├── service.log.2018-12-21
# ├── service.log.2018-12-22


# 0 directories, 31 files


#Define something
targetdir="/data/applogs/saas/uc/tag/core/service/"
keepdays="30"
logname="service.log"
needtar=`date -d "yesterday" +%Y-%m-%d`

#Now play

cd ${targetdir}

#Delete 1 weeks ago log file
find ${targetdir} -type f -mtime +${keepdays} -delete


#bzip log file
tar jcf ${logname}.${needtar}.tar.bz2 ${logname}.${needtar}
sleep 3
rm -rf ${logname}.${needtar}