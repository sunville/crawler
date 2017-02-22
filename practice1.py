# -*- coding: utf-8 -*-

import sys
import requests

html_path = 'http://xlzd.me'
resp = requests.get(html_path)
'''
#模拟header发送请求
headers = {'User-Agent': 'my custom user agent', 'Cookie': 'haha'}
requests.get(html_path, headers=headers)
#禁止重定向
r = requests.get('http://xlzd.me', allow_redirects=False)
#设定等待时间
r = requests.get('http://xlzd.me', timeout＝3)
#套代理
proxies = {
  "http": "http://192.168.31.1:3128",
  "https": "http://10.10.1.10:1080",
}
requests.get("http://xlzd.me", proxies=proxies)
#会话对象
session = requests.Session()
session.post('http://xlzd.me/login', data={'user': 'xlzd', 'pass': 'mypassword'})
####登录成功则可以发布文章了
session.put('http://xlzd.me/new', data={'title': 'title of article', 'data': 'content'


print resp.status_code
resp = requests.head(html_path)
index = 0
https://xlzd.me/query?name=xlzd&&lang=python
r = requests.get("http://xlzd.me/query", params={"name":"xlzd", "lang": "python"})
print r.url


for item in resp.__dict__.keys():
	
	if item == '_content':
		html_name ='Web Crawler with Python - 09.怎样通过爬虫找出我和轮子哥、四万姐之间的最短关系'
		file_path = '/Users/tony/Desktop/reptile/'+html_name+'.html'
		Html_file = open(file_path,'w')
		exec('Html_file.write(resp.%s)' % item)
		Html_file.close()

	index = index + 1
	sys.stdout.write(str(index)+' '+item+' : ')
	sys.stdout.flush()
	exec('print resp.%s\n\n') % item
#r = requests.post("http://xlzd.me/login", data = {"user":"xlzd", "pass": "mypassword"})
#r = requests.put("http://xlzd.me/post", data = {"title":"article"})
'''
