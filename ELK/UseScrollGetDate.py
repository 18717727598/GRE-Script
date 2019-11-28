#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'nightrover123@163.com'

"""
Created by PyCharm.
File:               xxx.py
Create Time:        Fri Nov  1 15:32:59 CST 2019
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module '' and '' is required, using pip
    install them.
    ```
    pip install psutil prettytable
    ```
    On OSX this function requires root privileges.
    # python portStatistics.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """


from elasticsearch import Elasticsearch

import subprocess


class SearchElk(object):

    def __init__(self, elkserver, index):
        self.elkserver = elkserver
        self.index = index

    def GetTotal(self):
        es = Elasticsearch(self.elkserver, timeout=120)

        # This data could be find in Kibana -- inspect -- request,but note the true need add "",like this: "true"
        data = {
            # The default size was set to 10000,you can change it in es
            "size": 10000,
            "sort": [
                {
                    "@timestamp": {
                        "order": "asc",
                        "unmapped_type": "boolean"
                    }
                }
            ],
            "_source": {
                "excludes": []
            },
            "stored_fields": [
                "*"
            ],
            "script_fields": {},
            "docvalue_fields": [
                {
                    "field": "@timestamp",
                    "format": "date_time"
                }
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": "message: \"createShortParam,request:\"",
                                "analyze_wildcard": "true",
                                "default_field": "*"
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": 1572537600000,
                                    "lte": 1573055999999,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            }
        }

        res = es.search(
            index=self.index,
            body=data,
        )

        print('The total result is ' + str(res['hits']['total']))


    def main(self):
        es = Elasticsearch(self.elkserver, timeout=120)

        data = {
            "version": "true",
            "size": 10000,
            "sort": [
                {
                    "@timestamp": {
                        "order": "asc",
                        "unmapped_type": "boolean"
                    }
                }
            ],
            "_source": {
                "excludes": []
            },
            "stored_fields": [
                "*"
            ],
            "script_fields": {},
            "docvalue_fields": [
                {
                    "field": "@timestamp",
                    "format": "date_time"
                }
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": "message: \"createShortParam,request:\"",
                                "analyze_wildcard": "true",
                                "default_field": "*"
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": 1572537600000,
                                    "lte": 1573055999999,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            }
        }

        return_fields = [
            '_scroll_id',
            'hits.hits._source.@timestamp',
            'hits.hits._source.message'
        ]

        # When use scroll ,the first time will have a scroll id,note this.
        res = es.search(
            index=self.index,
            body=data,
            filter_path=return_fields,
            search_type="query_then_fetch",
            scroll="4m"
        )

        # Export zh_CN.UTF-8.
        # If do not set LANG="zh_CN.UTF-8;export",may be have UnicodeEncodeError: 'ascii' codec can't encode characters
        # Some times This configuration does not work. i give up.
        # subprocess.call(['LANG="zh_CN.UTF-8";export'],shell=True)

        # Get the first scroll date,in high version of ES,the first time will return scroll id and data!
        for hit in res['hits']['hits']:
            # print(hit)
            # May be you can use 'ab' ,it may be fix the problem of 'UnicodeEncodeError: 'ascii' codec can't encode characters'
            # If ues ab, need this: f.write(str(hit).encode('utf8'))
            with open('/tmp/es.log', 'a') as f:
                try:
                    f.write(str(hit))
                    f.write("\n")
                except Exception as f:
                    pass
                    #print(f)


        scrollid = res["_scroll_id"]

        # Do not use 'scroll_size = len(res['hits']['hits'])' ,becaus in low version of ES,the first time has no data,just scroll!
        scroll_size = 1
        #scroll_size = len(res['hits']['hits'])
        # print(scroll_size)

        try:
            while(scroll_size > 0):
                response = es.scroll(scroll_id=scrollid, scroll="4m", filter_path=return_fields)

                for hit in response['hits']['hits']:
                    # print(hit)
                    with open('/tmp/es.log', 'a') as f:
                        try:
                            f.write(str(hit))
                            # f.write(str(hit).encode('utf8'))
                            f.write("\n")
                        except Exception as f:
                             print(f)

                scrollid = response["_scroll_id"]
                scroll_size = len(response['hits']['hits'])

        except KeyError as e:
            print('I got all data,enjoy it')


if __name__ == '__main__':
    elkserver = "http://10.16.252.4:9200"
    index = "logstash-nightroverreplace-sdp-tomcat-online-*"
    getcontent = SearchElk(elkserver, index)
    getcontent.GetTotal()
    getcontent.main()
