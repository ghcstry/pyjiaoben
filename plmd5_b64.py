#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base64
import os

fname = input('输入要加密的内容的文件路径：')
if os.path.exists(fname) == False:
	print('文件不存在！！！')
	exit()
with open(fname,'r') as f:
	for ma in f:
		ma = ma.replace('\n','').encode()
		with open('jiami.csv','a+') as w:
			w.write(hashlib.md5(ma).hexdigest()+','+ma.decode()+','+base64.b64encode(ma).decode()+'\n')
