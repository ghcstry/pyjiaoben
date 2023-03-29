#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os,time

def down_file(fileurl,folder,filename):
	fname = folder + filename
	if os.path.exists(fname):
		print(filename,'  ---已存在')
	else:
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Accept-Encoding':'gzip, deflate','X-Forwarded-For':'1.1.1.1','Connection':'close'}
		requests.packages.urllib3.disable_warnings()
		for i in range(0,3):
			with open(fname,'wb') as f:
				try:
					f.write(requests.get(fileurl,headers=headers,verify=False,timeout=60).content)
					print(filename,'  ---已下载')
					return True
				except:
					print(filename,'  ---下载出错，尝试重新下载')
					os.remove(fname)
					time.sleep(2)
		print(fileurl + '  ---下载出错三次，请检查文件链接是否正常！in ' + folder)

if __name__ == '__main__':
	folder = 'files/'
	if os.path.exists(folder) == False:
		os.makedirs(folder)
	fileurl = 'https://yuming/*.png.jpg.mp3.mp4.pdf.doc...'
	filename = 'xx.png...'
	down_file(fileurl,folder,filename)
