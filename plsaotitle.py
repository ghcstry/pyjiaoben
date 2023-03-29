#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import threading
import re

requests.packages.urllib3.disable_warnings()

def log(log):
	with open('titlelog.txt','a+',encoding='utf-8') as f:
		f.write(log+'\n')
	return log

def bt(url):
	if 'https://' in url or 'http://' in url:
		try:
			response = requests.get(url=url,headers=HEADERS,proxies=PROXIES,timeout=60,verify=False)
		except Exception as e:
			print(url,'----- 无法连接！')
			log(url+' ----- 无法连接 ----- '+str(e))
			return False
	else:
		url = 'https://' + url
		try:
			response = requests.get(url=url,headers=HEADERS,proxies=PROXIES,timeout=60,verify=False)
		except:
			url = url.replace('https://','http://')
			try:
				response = requests.get(url=url,headers=HEADERS,proxies=PROXIES,timeout=60)
			except Exception as e:
				url = url.replace('http://','')
				print(url,'----- 无法连接！')
				log(url+' ----- 无法连接 ----- '+str(e))
				return False
	try:
		server = response.headers['Server']
	except:
		server = ''
	try:
		xpb = response.headers['X-Powered-By']
	except:
		xpb = ''
	try:
		if response.encoding != 'ISO-8859-1' and response.encoding != None:
			content = response.content.decode(response.encoding)
		elif requests.utils.get_encodings_from_content(str(response.content)) != []:
			content = response.content.decode(requests.utils.get_encodings_from_content(str(response.content))[0])
		else:
			content = response.content.decode('utf-8')
		if content == '':
			title = '！返回内容为空！'
			print(log(url+' ----- '+str(response.status_code)+' ----- '+title+' | '+server+' : '+xpb))
			return False
	except:
		if response.content == b'':
			title = '！返回内容为空，未知编码！'
		else:
			title = '！网页解码出错！'
		print(log(url+' ----- '+str(response.status_code)+' ----- '+title+' | '+server+' : '+xpb))
		return False
	try:
		title = re.search('<title.*>.*</title>',content,re.I).group()
	except:
		try:
			title = re.search('<title.*>.*</title>',content.replace('\n',''),re.I).group()
		except:
			title = '！标题匹配失败！'
			print(log(url+' ----- '+str(response.status_code)+' ----- '+title+' | '+server+' : '+xpb))
			return False
	try:
		title = re.sub('<title.*?>|</title>|\r|\t','',title,flags=re.I)
	except:
		title = '！获取标题错误！'
	print(log(url+' ----- '+str(response.status_code)+' ----- '+title+' | '+server+' : '+xpb))

def pl(url,se):
	se.acquire()
	bt(url)
	se.release()

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('-u','--url',help='xx.com or http://xx.com')
	ap.add_argument('-f','--file',help='file path')
	ap.add_argument('-p','--proxy',help='http://127.0.0.1:8080')
	ap.add_argument('-t','--thread',help='xiancheng 10',type=int,default=10)
	args = vars(ap.parse_args())
	HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Accept-Encoding':'gzip, deflate','Content-Type':'application/x-www-form-urlencoded','X-Forwarded-For':'1.1.1.1','Connection':'close'}
	if args['proxy'] != None:
		PROXIES = {'http':args['proxy'],'https':args['proxy']}
	else:
		PROXIES = {}
	if args['file'] != None:
		se = threading.BoundedSemaphore(args['thread'])
		with open(args['file'],'r') as f:
			for u in f:
				t = threading.Thread(target=pl,args=(u.replace('\n',''),se,))
				t.start()
	if args['url'] != None:
		bt(args['url'])
