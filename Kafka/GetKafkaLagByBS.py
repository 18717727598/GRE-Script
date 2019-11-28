#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'nightrover123@163.com'

"""
Created by PyCharm.
File:               xxx.py
Create Time:        Fri Nov  1 15:32:59 CST 2019
Note:
    Get Lag from the Kafka manager.
    And get it.return it.
 """


from urllib.request import urlopen

from bs4 import BeautifulSoup



class GetContent(object):

    def __init__(self, url):
        self.url = url

    def main(self):
        html = urlopen(self.url)
        pagecode = BeautifulSoup(html, "html.parser")
        gettarget = pagecode.findAll("td")
        result = gettarget[1].get_text()

        # print(result)
        if '-' in result:
            result = 0
        return str(result)


if __name__ == '__main__':
    target = "http://10.10.128.178:8888/clusters/nightroverreplace-openruntime/" \
             "consumers/openruntime-vip/topic/openruntime-vip/type/KF"
    content = GetContent(target)
    result = content.main()
    print(result.replace(',',''))
