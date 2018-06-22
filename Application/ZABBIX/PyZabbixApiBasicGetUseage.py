#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'


"""
Created by PyCharm.
File:               PyZabbixApiBasicGetUseage.py
Create Date:        2018/06/22
Create Time:        10:26
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module 'pyzabbix' and '' is required, using pip
    install them.
    ```
    pip install pyzabbix
    ```
    On OSX this function requires root privileges.
    # python PyZabbixApiBasicGetUseage.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """



from pyzabbix import ZabbixAPI



class Zapi(object):

    def __init__(self,zaurl,zauser,zapass):
        self.zaurl = zaurl
        self.zauser = zauser
        self.zapass = zapass

    def za_login(self):
        self.auth = ZabbixAPI(zaurl)
        self.auth.login(zauser,zapass)
        return self.auth

    def print_ver(self):
        print("Connected to Zabbix API Version %s" % self.auth.apiinfo.version())

    #Get all host info
    def get_all_host(self):
        for h in self.auth.host.get(output="extend"):
            #print(h) this will print all of the hosts info
            print(h)
            #follow will print all hosts xxxx
            print(h['available'])


    #Only get need info
    def get_iter(self):
        for h in self.auth.host.get(output=['hostid','host']):
            print(h)




if __name__ == '__main__':
    zaurl = "http://jack.zabbixvmware.com"
    zauser = "Admin"
    zapass = "zabbix"
    pz = Zapi(zaurl,zauser,zapass)
    pz.za_login()
    pz.print_ver()
    pz.get_iter()