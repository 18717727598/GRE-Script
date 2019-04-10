#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'windco'

import sys
import requests
import json

upstream_check_url = 'http://127.0.0.1:56789/status_upstream?format=json'


def Get_Upstream():
	upstream_list = []
	zabbix_data = {}
	try:
		r=requests.get(upstream_check_url)
	except(Exception), e:
		print str(e)
		exit('Connect url error!')
	
	context = r.json()
	upstream_list_data = context['servers']['server']
	if upstream_list_data:
		for item in upstream_list_data:
			# print json.dumps(item, sort_keys=True, indent=4)
			item_dict= {
				'{#NGINX_UPSTREAM_NAME}': item['upstream'],
				'{#NGINX_UPSTREAM_IP}': item['name'],
				'{#NGINX_UPSTREAM_TYPE}': item['type'],
				'{#NGINX_UPSTREAM_STATUS}': item['status'],
			}
			upstream_list.append(item_dict)
	zabbix_data['data'] = upstream_list
	return zabbix_data
	
def Check_Status(upstream_ip):
	code = None #定义返回值,1为up,0为down
	_data = Get_Upstream()['data']
	upstream_ip_list = [_item['{#NGINX_UPSTREAM_IP}'] for _item in _data]
	if upstream_ip not in upstream_ip_list:  #这里考虑到upstream name被更改或清除的情况
		code = 1
	else:
		for _i in _data:
			if _i['{#NGINX_UPSTREAM_IP}'] == upstream_ip:
				if _i['{#NGINX_UPSTREAM_STATUS}'] == 'down':
					code = 0
				elif _i['{#NGINX_UPSTREAM_STATUS}'] == 'up':
					code = 1
				else:
					code = 1
				break
			else:
				continue
	return code
	
	
if __name__ == '__main__':
	if sys.argv[1] == 'discovery_data':  #获取zabbix自动发现key规范的数据
		zabbix_data = Get_Upstream()
		print json.dumps(zabbix_data, sort_keys=True, indent=4)
	else:  #zabbix传过来的值
		code =Check_Status(sys.argv[1])  #这里的sys.argv[1]为zabbix传过来的第一个值，即upstream名
		print code
	
'''
{"servers": {
  "total": 2,
  "generation": 285,
  "server": [
    {"index": 306, "upstream": "scloud-dc-internal-domain-com", "name": "10.16.146.136:8080", "status": "down", "rise": 0, "fall": 118188, "type": "http", "port": 0},
    {"index": 307, "upstream": "scloud-dc-internal-domain-com", "name": "10.16.150.23:8080", "status": "down", "rise": 0, "fall": 118324, "type": "http", "port": 0},
  ]
}}
'''
