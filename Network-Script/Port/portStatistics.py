#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
This script was writen by
https://github.com/DingGuodong/LinuxBashShellScriptForOps/blob/master/functions/net/tcp/port/portStatistics.py
And i just modify it.
thanks to DingGuodong.
 """


import psutil

import prettytable

import subprocess

import time


class PortStatistics(object):

    def __init__(self, ports):
        self.port = ports

    def totalcon(self):
        print('Now count all connect info: ')
        status_list = ["LISTEN", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "LAST_ACK", "SYN_SENT"]
        status_temp = []

        net_connections = psutil.net_connections()
        for key in net_connections:
            status_temp.append(key.status)

        for status in status_list:
            print status, status_temp.count(status)
        print('\n')

    def main(self):
        starttime = time.time()

        port = int(self.port)
        # print(isinstance(port, int))

        # define data structure for each connection, each ip is unique unit
        ipaddress = {
            'ipaddress': None,
            'counts': 0,
            'stat': {
                'established': 0,
                'time_wait': 0,
                'others': 0
            }
        }

        # define data structure for statistics
        statistics = {
            'portIsUsed': False,
            'portUsedCounts': 0,
            'portPeerList': [
                {
                    'ipaddress': None,
                    'counts': 0,
                    'stat': {
                        'established': 0,
                        'time_wait': 0,
                        'others': 0
                    },
                },
            ]
        }

        tmp_portPeerList = list()
        portPeerSet = set()
        netstat = psutil.net_connections()
        # print(netstat)

        # get all ip address only for statistics data
        for i, sconn in enumerate(netstat):

            # print sconn.laddr
            # print port + 'after print sconn.laddr'
            if port in sconn.laddr:
                # print port + 'if port in sconn.laddr:'
                statistics['portIsUsed'] = True
                if len(sconn.raddr) != 0:
                    statistics['portUsedCounts'] += 1
                    ipaddress['ipaddress'] = sconn.raddr[0]
                    tmp_portPeerList.append(
                        str(ipaddress))  # dict() list() set() is unhashable type, collections.Counter

        for ip in tmp_portPeerList:
            portPeerSet.add(str(ip))  # remove duplicated ip address using set()

        for member in portPeerSet:
            statistics['portPeerList'].append(eval(member))

        # add statistics data for each ip address
        for sconn in netstat:
            if port in sconn.laddr:
                if len(sconn.raddr) != 0:
                    for i, item in enumerate(statistics['portPeerList']):
                        if item['ipaddress'] == sconn.raddr[0]:
                            statistics['portPeerList'][i]['counts'] += 1
                            if sconn.status == 'ESTABLISHED':
                                statistics['portPeerList'][i]['stat']['established'] += 1
                            elif sconn.status == 'TIME_WAIT':
                                statistics['portPeerList'][i]['stat']['time_wait'] += 1
                            else:
                                statistics['portPeerList'][i]['stat']['others'] += 1

        # print statistics result using prettytable
        if statistics['portIsUsed']:
            print "Total connections of port %s is %d." % (port, statistics['portUsedCounts'])
            table = prettytable.PrettyTable()
            table.field_names = ["Total Counts", "Remote IP Address", "Established Conns", "Time_wait Conns",
                                 "Others Conns"]
            for i, ip in enumerate(statistics['portPeerList']):
                if ip['ipaddress'] is not None:
                    table.add_row([ip['counts'], ip['ipaddress'], ip['stat']['established'], ip['stat']['time_wait'],
                                   ip['stat']['others']])
            print table.get_string(sortby=table.field_names[0], reversesort=True)
        else:
            print statistics['portIsUsed']
            print 'port %s has no connections, please make sure port is listen or in use.' % port

        endtime = time.time()
        print "Elapsed time: %s seconds." % (endtime - starttime)


if __name__ == '__main__':

    # Get total connection
    y = PortStatistics(18)
    y.totalcon()

    time.sleep(3)

    # Get top 3 of ESTABLISHED connection
    # print('Get top 3 of ESTABLISHED connection')
    # p = subprocess.Popen(
    #     "netstat -na | grep ESTABLISHED | awk '{print $4}' | awk -F ':' '{print $2}' | sort | uniq -c | sort -rn | head -n 3 | awk '{print $2}'",
    #     stdout=subprocess.PIPE, shell=True)
    # result = p.communicate()[0].split('\n')
    # for n in result:
    #     if n:
    #         # print(n)
    #         l = PortStatistics(n)
    #         l.main()
    # print('\n')


    # time.sleep(3)

    # Get top 3 of TIME_WAIT connection
    print('Get top 3 of TIME_WAIT connection')
    u = subprocess.Popen(
        "netstat -na | grep TIME_WAIT | awk '{print $4}' | awk -F ':' '{print $2}' \
        | sort | uniq -c | sort -rn | head -n 3 | awk '{print $2}'",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    tre = u.communicate()[0].split('\n')
    for n in tre:
        if n:
            # print n
            l = PortStatistics(n)
            l.main()