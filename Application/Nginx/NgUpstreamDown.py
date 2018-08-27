#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'

"""
Created by PyCharm.
File:               NgUpstreamDown.py
Create Date:        2018/07/13
Create Time:        16:59
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module '' and '' is required, using pip
    install them.
    ```
    pip install 
    ```
    On OSX this function requires root privileges.
    # python NgUpstreamDown.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """

import urllib2

from urllib2 import HTTPError, URLError

import datetime

import smtplib

from email.mime.text import MIMEText

import ast


class NgDownServer(object):

    def __init__(self, urls):
        self.url = urls

    def main(self):
        _now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        _all_html = ''
        for u in self.url:
            try:
                response = urllib2.urlopen(u)
            except (HTTPError, URLError):
                print('\nPlease check out your Ng status url,i can not connect to it!!!\n')
                exit(1)

            # Get the str,and set to json.
            _get_json = ast.literal_eval(response.read())["servers"]["server"]
            body = ''
            if _get_json:
                for s in _get_json:
                    upstream = s["upstream"]
                    ip = s["name"]
                    status = s["status"]
                    ty = s["type"]
                    values = '''
                    <tr bgcolor="#FF0000">
                        <td>{upstream}</td>
                        <td>{ip}</td>
                        <td>{status}</td>
                        <td>{type}</td>
                    </tr>
                    '''.format(upstream=upstream, ip=ip, status=status, type=ty)
                    body += values

                _module_html = '''
                <h3>This NGINX upstream down status URL: </h3>  
                <h3>{ngurl}</h3>
                <h4>Build time @{time}</h4>
                <table style="background-color:white" cellspacing="0" cellpadding="3" border="1">
                    <tbody>
                        <tr bgcolor="#C0C0C0">
                            <th>Upstream</th>
                            <th>Name</th>
                            <th>Status</th>
                            <th>Check type</th>
                        </tr>
                        {body}
                    </tbody>
                </table>                    
                '''.format(ngurl=u, body=body, time=_now_time)
                _all_html += _module_html
            else:
                exit(0)
        return _all_html


class MailAction(object):
    def __init__(self, server_host, server_port, from_user, from_user_password, send_to_user):
        self.server_host = server_host
        self.server_port = server_port
        self.from_user = from_user
        self.from_user = from_user
        self.from_user_password = from_user_password
        self.send_to_user = send_to_user
        self.mail_server = None

    def mail_auth(self):
        self.mail_server = smtplib.SMTP(self.server_host, self.server_port)
        if True:
            try:
                self.mail_server.login(self.from_user, self.from_user_password)
            except Exception, e:
                print str(e)
                exit('Mail Auth False')
        else:
            print 'mail server connect failed!'
            exit('Mail Connect False')

    def send_html_mail(self, data):
        context = data
        msg = MIMEText(context, 'html', 'utf-8')
        msg['From'] = self.from_user
        msg['To'] = self.send_to_user
        msg['Subject'] = u'NGINX upstream check status'
        self.mail_server.sendmail(self.from_user, self.send_to_user.split(','), msg.as_string())
        if not True:
            print 'Send mail failed!'
        self.mail_server.quit()


if __name__ == '__main__':
    url01 = 'http://111.111.111.111:56789/status_upstream?format=json&status=down'
    url02 = 'http://222.222.222.222:56789/status_upstream?format=json&status=down'
    NgDown = NgDownServer((url01, url02))
    Data = NgDown.main()
    domain = 'xx.smtp.com'
    port = 25
    user = 'user'
    password = 'xxxx'
    send_to_user = 'user'
    Mail_Server = MailAction(domain, port, user, password, send_to_user)
    Mail_Server.mail_auth()
    Mail_Server.send_html_mail(Data)