#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import threading
import time

requests.packages.urllib3.disable_warnings()

def file_read(path):
	with open(path,'r') as f:
		contents = f.readlines()
	return contents

def file_write(path,content):
	with open(path,'a+',encoding='utf-8') as f:
		f.write(content+'\n')
	return content

def connect(url):
	i = 2
	while i != 0:
		if 'https://' in url or 'http://' in url:
			try:
				response = requests.get(url=url,headers=HEADERS,proxies=PROXIES,verify=False,timeout=60,allow_redirects=False)
				return url
			except Exception as e:
				i = i - 1
				error = str(e)
				time.sleep(1)
		else:
			url = 'https://' + url
			try:
				response = requests.get(url=url,headers=HEADERS,proxies=PROXIES,verify=False,timeout=60,allow_redirects=False)
				return url
			except:
				url = url.replace('https://','http://')
				try:
					response = requests.get(url=url,headers=HEADERS,proxies=PROXIES,timeout=60,allow_redirects=False)
					return url
				except Exception as e:
					url = url.replace('http://','')
					i = i - 1
					error = str(e)
					time.sleep(1)
	print(url,'----- 连接出错！')
	file_write('log.txt',url+' ----- 连接出错 ----- '+error)
	return ''

def poc(url):
	print(url)

def pl(url,se):
	se.acquire()
	url = connect(url)
	if url != '':
		if url.endswith('/') == False:
			url = url + '/'
		poc(url)
	se.release()


if __name__ == '__main__':

	ap = argparse.ArgumentParser()
	ap.add_argument('-u','--url',help='xx.com or http://xx.com')
	ap.add_argument('-f','--file',help='file path')
	ap.add_argument('-p','--proxy',help='http://127.0.0.1:8080')
	ap.add_argument('-t','--thread',help='xiancheng 1',type=int,default=1)
	args = vars(ap.parse_args())

	HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Accept-Encoding':'gzip, deflate','Content-Type':'application/x-www-form-urlencoded','X-Forwarded-For':'1.1.1.1','Connection':'close'}

	if args['proxy'] != None:
		PROXIES = {'http':args['proxy'],'https':args['proxy']}
	else:
		PROXIES = {}

	if args['file'] != None:
		se = threading.BoundedSemaphore(args['thread'])
		for u in file_read(args['file']):
			t = threading.Thread(target=pl,args=(u.replace('\n',''),se,))
			t.start()

	if args['url'] != None:
		url = connect(args['url'])
		if url != '':
			if url.endswith('/') == False:
				url = url + '/'
			poc(url)
