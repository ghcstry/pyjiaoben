#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

host = 'smtp.office365.com'
smtpobj = smtplib.SMTP(host)
smtpobj.connect(host, 587)
smtpobj.ehlo()
smtpobj.starttls()
sender = 'send@outlook.com'
smtpobj.login(sender,'password')
content = '''
<p>这是定期安全检查，仅在你最近没有使用安全代码的情况下进行。你无需在每次登录时都提供一个代码。</p>
<p>保持帐户相关安全信息的正确和最新十分重要。我们不会使用该信息向你发送垃圾邮件或将其用于任何销售目的。它仅用于在帐户出现问题时验证你的身份。</p>
<p>谢谢!</p>
<Img sRC="https://res.cdn.office.net/assets/mail/pwa/v1/pngs/apple-touch-icon.png">
'''
message = MIMEText(content,'html','utf-8')
message['Subject'] = Header('安全检查','utf-8')
try:
	smtpobj.sendmail(sender,'receive@gmail.com',message.as_string())
	print('发送成功！')
except Exception as e:
	print(str(e))
smtpobj.close()
