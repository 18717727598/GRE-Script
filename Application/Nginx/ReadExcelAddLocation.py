#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bruce.jikun@gmail.com'


"""
Created by PyCharm.
File:               ReadExcelAddLocation.py
Create Date:        2018/06/14
Create Time:        15:37
Note:

    excel表格规范如下：
    表格的location部分比如：/ec/mgr/membership/queryAutoTagList ， 会同时增加10.16.168.208:8080和10.16.165.44:8080两台后端服务器转发
    如果有多个location对应不同的ip,用新增表格的方式。
    1，IP及port部分，无需合并单元格，每个IP独占一个单元格，脚本会依次读取
    2，表名固定为Sheet1
    3，Excel文件名字参照这个格式： 20180612Location.xlsx

    Usage:
    Using user as you want in Linux/Windows system.
    The python module 'xlrd'  is required, using pip
    install them.
    ```
    pip install xlrd
    ```
    On OSX this function requires root privileges.
    # python ReadExcelAddLocation.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """

import datetime
import os
import zipfile
import xlrd
import shutil



#define something
nowTime = datetime.datetime.now().strftime('%Y%m%d-%H%M')
baseport = '8080'
print("Start the engine.\n\nStart time at %s,and all upstreams port was set to 8080\n\n" % nowTime)
CWD_DIR = '/tmp'
base_DIR = '/usr/local/nginx/conf'
back_DIR = '/data/backup'


# Backup and compress DIR
os.chdir(CWD_DIR)
print("Change the CWD to %s\n" % CWD_DIR)

def zip_file(sourceDIR):
    os.chdir(base_DIR)
    for filenames in [x for x in os.listdir(sourceDIR)]:
        # print(filenames)
        aszip = zipfile.ZipFile(sourceDIR+nowTime+'.zip',mode='a')
        aszip.write(sourceDIR+'/'+filenames,compress_type=None)
        aszip.close()
    print("The %s DIR was backup Done!\n" % sourceDIR)
    if os.path.isdir(back_DIR):
        shutil.move(sourceDIR + nowTime + '.zip', back_DIR)
    else:
        os.mkdir('/data/backup', 0755)
        shutil.move(sourceDIR + nowTime + '.zip', back_DIR)




def halfnewfile():
    shutil.copyfile('%s/vhost.d/saas-ec.internal.domain.com.conf' % base_DIR,'%s/saas-ec.internal.domain.com.conf' % CWD_DIR)
    os.chdir(CWD_DIR)
    #Count the line number
    with open('saas-ec.internal.domain.com.conf','r') as f:
        tmpnum = len(f.readlines())
        neednum = int(tmpnum) - 1

    with open('saas-ec.internal.domain.com.conf','r') as f:
        try:
            os.remove('tmp.conf')
        except OSError,e:
            pass
        finally:
            #Copy lines to other file
            for i in range(0, neednum):
                filecontent = f.readline()
                with open('tmp.conf','a') as t:
                    t.write(filecontent)



def completefile(sourceexcel):
    print("Start read from Excel files...\n")
    os.chdir(CWD_DIR)
    #Read the Excel files
    excelfile = xlrd.open_workbook(sourceexcel)
    exsheet1 = excelfile.sheet_by_name('Sheet1')
    #get the location name from the first col,and get values begin from location
    locationco = exsheet1.col_values(0)[1:]

    while '' in locationco:
        locationco.remove('')

    #get the proxy_pass name
    proxynu = []
    for i in locationco:
        proxynu.append(i.replace('/','_'))
    ipcols = exsheet1.col_values(1)

    allip = [x for x in ipcols if '1' in x]
    # print(locationco)
    # print(allip)
    print("Read from the Excel file Done.\n\nWish the Excel was correct，or you will need use backup files!\n")

#Add the new location to vhost.d files
    for x in locationco:
        newcontent = '''location %s {
                proxy_redirect off;
                proxy_set_header Host $host:$server_port;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_http_version 1.1;
                proxy_set_header Connection "";
                proxy_next_upstream http_500 http_502 http_503 http_504 error timeout invalid_header;
                proxy_pass http://%s;
                }
        ''' % (x, proxynu[locationco.index(x)])

        with open('tmp.conf','a') as f:
            f.write(newcontent)


    with open('tmp.conf','a') as f:
        f.write('}')

    #Copy the complete file to source file
    shutil.copyfile('tmp.conf','%s/vhost.d/saas-ec.internal.domain.com.conf' % base_DIR)

    #Add the upstreams files
    os.chdir('%s/upstreams' % base_DIR)
    if len(allip) == 1:
        for x in proxynu:
            newupstreams = '''upstream %s {
            server %s:%s weight=10;
            keepalive 128;
            check interval=3000 rise=2 fall=5 timeout=1000 type=tcp;
            }
            ''' % (x,allip[0],baseport)
            with open('upstream_domain'+x+'.conf','a') as f:
                f.write(newupstreams)


    if len(allip) == 2:
        for x in proxynu:
            newupstreams = '''upstream %s {
            server %s:%s weight=10;
            server %s:%s weight=10;
            keepalive 128;
            check interval=3000 rise=2 fall=5 timeout=1000 type=tcp;
            }
            ''' % (x,allip[0],baseport,allip[1],baseport)
            with open('upstream_domain'+x+'.conf','a') as f:
                f.write(newupstreams)

    if len(allip) == 3:
        for x in proxynu:
            newupstreams = '''upstream %s {
            server %s:%s weight=10;
            server %s:%s weight=10;
            server %s:%s weight=10;
            keepalive 128;
            check interval=3000 rise=2 fall=5 timeout=1000 type=tcp;
            }
            ''' % (x,allip[0],baseport,allip[1],baseport,allip[2],baseport)
            with open('upstream_domain'+x+'.conf','a') as f:
                f.write(newupstreams)

    if len(allip) == 4:
        for x in proxynu:
            newupstreams = '''upstream %s {
            server %s:%s weight=10;
            server %s:%s weight=10;
            server %s:%s weight=10;
            server %s:%s weight=10;
            keepalive 128;
            check interval=3000 rise=2 fall=5 timeout=1000 type=tcp;
            }
            ''' % (x,allip[0],baseport,allip[1],baseport,allip[2],baseport,allip[3],baseport)
            with open('upstream_domain'+x+'.conf','a') as f:
                f.write(newupstreams)

    if len(allip) == 5:
        for x in proxynu:
            newupstreams = '''upstream %s {
            server %s:%s weight=10;
            server %s:%s weight=10;
            server %s:%s weight=10;
            server %s:%s weight=10;
            server %s:%s weight=10;
            keepalive 128;
            check interval=3000 rise=2 fall=5 timeout=1000 type=tcp;
            }
            ''' % (x,allip[0],baseport,allip[1],baseport,allip[2],baseport,allip[3],baseport,allip[4],baseport)
            with open('upstream_domain'+x+'.conf','a') as f:
                f.write(newupstreams)



if __name__ == '__main__':
    sourceexcel = raw_input('Show me the Excel :  ')
    zip_file('vhost.d')
    zip_file('upstreams')
    halfnewfile()
    completefile(sourceexcel)
    print("All Done! Now use nginx -t check it.\n")
