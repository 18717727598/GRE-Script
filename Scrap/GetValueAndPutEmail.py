#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'


"""
Created by PyCharm.
File:               GetValueAndPutEmail.py.py
Create Date:        2019/01/28
Create Time:        15:11
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module '' and '' is required, using pip
    install them.
    ```
    pip install *.py
    ```
    On OSX this function requires root privileges.
    # python PyZabbixApiBasicGetUseage.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """


from urllib.request import urlopen

from bs4 import BeautifulSoup

import smtplib

from email.mime.text import MIMEText

import datetime


class GetContent(object):

    def __init__(self, url):
        self.url = url

    def main(self):
        html = urlopen(self.url)
        pagecode = BeautifulSoup(html, "html.parser")
        gettarget = pagecode.findAll("td")
        # print(gettarget[4].get_text())
        result = gettarget[4].get_text()
        return result

    def gethtml(self):
        nowtime = datetime.datetime.now()
        timenow = str(nowtime).split('.')[0]

        value = '''
            <tr>
                <th>{object_name}</th>
                <th>{Lag}</th>
            </tr>
            '''.format(object_name="openruntime-commmon", Lag=result)

        html_data = '''
                <h2>Data Acquisition Sources : Kafka Manager</h2>
                <h4>Time : {time}</h4>
                <p>
                    <a href={KM_url}>KM_URL</a>
                    </p>
                <table border="1">
                    <tr>
                        <th>object_name</th>
                        <th>Lag</th>
                    </tr>
                    {value}
                </table>
                '''.format(time=timenow, KM_url=self.url, value=value)
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
            except Exception as e:
                print(str(e))
                exit('Mail Auth False')
        else:
            print('mail server connect failed!')
            exit('Mail Connect False')

    def Send_Html_Mail(self, data):
        context = data
        msg = MIMEText(context, 'html', 'utf-8')
        msg['From'] = self.from_user
        msg['To'] = self.send_to_user
        msg['Subject'] = u'Attention Please!! openruntime-commmon Lag warning!!'
        data = self.mail_server.sendmail(self.from_user, self.send_to_user.split(','), msg.as_string())
        if not True:
            print('Send mail failed!')
        self.mail_server.quit()

if __name__ == '__main__':
    target = "http://10.10.128.178:8888/clusters/nightroverreplace-openruntime/consumers/openruntime-commmon" \
             "/topic/openruntime-commmon/type/KF"
    content = GetContent(target)
    result = content.main()
    gethtml = content.gethtml()
    print('The result is ' + result)

    server_host = 'mail.domain.com'
    server_port = 25
    from_user = 'zabbix_report@domain.com'
    from_user_password = 'password'
    send_to_user = 'kun.ji01@domain.com'
    Mail_Server = Mail_Action(server_host, server_port, from_user, from_user_password, send_to_user)
    if int(result) == 0:
        # mail登录验证
        Mail_Server.Mail_Auth()
        # 发送数据
        Mail_Server.Send_Html_Mail(gethtml)
    else:
        exit(0)
