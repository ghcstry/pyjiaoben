#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import base64
import math
import re

requests.packages.urllib3.disable_warnings()
vip = input('是否是vip？(y/n)：')
fofa_token = input('请输入fofa_token：')
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0','Cookie':'fofa_token='+fofa_token}
proxies={}#{'https':'http://127.0.0.1:8080','http':'http://127.0.0.1:8080'}
while 1:
	strs = input('请输入关键词：')
	if strs == 'exit':
		break
	strs = base64.b64encode(strs.encode()).decode()
	#country="US" && host=".gov" && ".jsp"
	url = 'https://fofa.info/result?qbase64=%s' % (strs)
	try:
		response = requests.get(url=url,headers=headers,verify=False,timeout=60,proxies=proxies)
		num = re.search('共 .*? 条',response.content.decode()).group()
		print(num)
		num = int(num.replace('共 ','').replace(' 条',''))
		if num >= 60 and vip == 'n':
			pages = 3
		else:
			pages = math.ceil(num/20)
		for i in range(1,pages+1):
			url = 'https://fofa.info/result?qbase64=%s&page=%i&page_size=20' % (strs,i)
			response = requests.get(url=url,headers=headers,verify=False,timeout=60,proxies=proxies)
			hrefs = re.findall('><a href="http.*?" target="_blank">',response.content.decode())
			for href in hrefs:
				href = href.replace('><a href="','').replace('" target="_blank">','')
				print(href)
				with open('fofaurls.txt','a+',encoding='utf-8') as f:
					f.write(href+'\n')
	except Exception as e:
		print(str(e))
