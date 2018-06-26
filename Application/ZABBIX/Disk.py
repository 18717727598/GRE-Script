#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'


"""
thanks to LongLinKang.He write the pyzabbix_disk.py . And this scripts copy form that.just for backup use.
Created by PyCharm.
File:               pyzabbix_Disk.py
Create Date:        2018/06/22
Create Time:        10:26
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module 'pyzabbix' and '' is required, using pip
    install them.
    ```
    pip install pyzabbix_Disk.py
    ```
    On OSX this function requires root privileges.
    # python PyZabbixApiBasicGetUseage.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """



from pyzabbix import ZabbixAPI
import datetime
import smtplib
from email.mime.text import MIMEText
import json
import string

class Zapi(object):

    def __init__(self,zaurl,zauser,zapass):
        self.zaurl = zaurl
        self.zauser = zauser
        self.zapass = zapass

    def za_login(self):
        self.auth = ZabbixAPI(zaurl)
        self.auth.login(zauser,zapass)
        return self.auth


    #Get all host info into a dict
    def get_all_host(self):
        allhosts = {}
        getallhost = self.auth.host.get(output=['hostid','host'])
        # print(getallhost)
        for i in getallhost:
            getkeys = i['hostid']
            allhosts[getkeys] = i['host']
        # print(allhosts)
        return allhosts


    def get_data(self):
        nowtime = datetime.datetime.now()
        timenow = str(nowtime).split('.')[0]
        allhostdict = self.get_all_host()
        #/boot and / is mount dir,of cause you can change it to other item as you need
        itemlist = ['vfs.fs.size[/boot,pfree]','vfs.fs.size[/,pfree]']
        disk_data = ''

        for _key in itemlist:
            items = self.auth.item.get(hostids=allhostdict.keys(),search={'key_': _key})
            # print(iterms)
            for item in items:
                diskname = item['key_'].split(',')[0].split('[')[-1]
                diskvalue = item['lastvalue']
                host_id = item['hostid']
                # print(diskname,diskvalue,host_id)
		#float(80) is pfree num
                if float(diskvalue) < float(80) and float(diskvalue) != float(0):
                    diskvalue_value = float(100) - float(diskvalue)
                    host_ip_data = self.auth.hostinterface.get(hostids=host_id,
                                                                   output=['ip']
                                                                   )

                    host_ip = [item['ip'] for item in host_ip_data]
                    value = '''
                        <tr>
                            <th>{hostname}</th>
                            <th>{host_ip}</th>
                            <th>{partition}</th>
                            <th>{partition_used}</th>
                        </tr>
                        '''.format(hostname=allhostdict[host_id], host_ip=str(host_ip[0]), partition=diskname,
                                   partition_used=str(round(diskvalue_value, 2)) + '%')
                    disk_data += value

        html_data = '''
                <h2>数据采集来源:zabbix</h2>
                <h4>数据采集时间:{time}</h4>
                <p>
                    <a href={zabbix_url}>zabbix登录链接</a>
                    </p>
                <table border="1">
        		    <tr>
        		        <th>HostName</th>
        		        <th>Host_IP</th>
        		        <th>Partition</th>
        		        <th>Partition_Used</th>
        		    </tr>
        		    {disk_data}
        		</table>
                '''.format(time=timenow, zabbix_url=self.zaurl, disk_data=disk_data)
        return html_data


class Mail_Action(object):
    def __init__(self, server_host, server_port, from_user, from_user_password, send_to_user):
        self.server_host = server_host
        self.server_port = server_port
        self.from_user = from_user
        self.from_user = from_user
        self.from_user_password = from_user_password
        self.send_to_user = send_to_user
        self.mail_server = None

    def Mail_Auth(self):
        self.mail_server = smtplib.SMTP(self.server_host, self.server_port)
        if True:
            try:
                self.mail_server.login(self.from_user, self.from_user_password)
            except (Exception), e:
                print str(e)
                exit('Mail Auth False')
        else:
            print 'mail server connect failed!'
            exit('Mail Connect False')

    def Send_Html_Mail(self, data):
        context = data
        msg = MIMEText(context, 'html', 'utf-8')
        msg['From'] = self.from_user
        msg['To'] = self.send_to_user
        msg['Subject'] = u'服务器磁盘分区使用率超过20%机器列表'
        data = self.mail_server.sendmail(self.from_user, self.send_to_user.split(','), msg.as_string())
        if not True:
            print 'Send mail failed!'
        self.mail_server.quit()


if __name__ == '__main__':
    zaurl = "http://jack.zabbixvmware.com"
    zauser = "Admin"
    zapass = "zabbix"
    pz = Zapi(zaurl,zauser,zapass)
    try:
        pz.za_login()
        if not True:
            print 'Zabbix auth is failed!'
    except (Exception), e:
        print str(e)
        exit('Zabbix Auth False')
        # 获取数据
    Data = pz.get_data()

    # 邮件相关
    server_host = 'smtp.163.com'
    server_port = 25
    from_user = 'xxx@163.com'
    from_user_password = 'xxx'
    send_to_user = 'xxx@163.com'
    Mail_Server = Mail_Action(server_host, server_port, from_user, from_user_password, send_to_user)
    # mail登录验证
    Mail_Server.Mail_Auth()
    # 发送数据
    Mail_Server.Send_Html_Mail(Data)
