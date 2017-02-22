
# -*- coding: utf-8 -*-

import requests
import js2xml
from lxml import etree

headers ={
	#这边cookie替换成你的cookie
	'Cookie':'login_sid_t=ceba54a3086a80bdec2dc22d2d0587d5; _s_tentry=passport.weibo.com; Apache=4125769459642.4697.1444527509373; SINAGLOBAL=4125769459642.4697.1444527509373; appkey=; __gads=ID=b6ae295d02bcae1a:T=1468635297:S=ALNI_MYB5EOXPbMN9HROknhEt7n3Og_YVw; ULV=1475856396248:1:1:1:4125769459642.4697.1444527509373:; SSOLoginState=1480733730; UOR=,,login.sina.com.cn; SCF=AqghO-qv-TWiNcRwdPsnZCCSKaZehnx3ZDi8A8LPf-iac6rQQ6ncuI7VJ98dcSKNKC8Gg1ryc6JcYgrltp0Brr0.; SUB=_2A251r3fjDeRxGedJ6VIS8izEyTmIHXVW3e4rrDV8PUJbmtBeLUahkW-Z-mVuHKYCRhmfombYNXNll3kDTg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWMv4EMIHEOVxoePKL6VBLz5JpX5o2p5NHD95QpS0z7e0zE1hzfWs4Dqc_xi--Xi-zRiK.ci--NiK.fiKyhi--Ni-8hi-8hi--Xi-zRiKn7i--NiKLWiKnXi--Ri-zNi-8si--NiK.Ni-zXi--ci-88i-isi--Xi-zRiKyF; SUHB=09P8ouxMalahMr; ALF=1519128100; CONTENT-HONGBAO-G0=f3391d9b622236764fef74867cec89b9; _T_WM=88ba1d0357b31c7192a108ced780dc3c',
	'User-Agent':'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
}

def getuid():
	url = "http://chunjie.hongbao.weibo.com/hongbao2017/h5index"
	z = requests.get(url,headers=headers)
	if z.status_code == 200:
		# 这边是查找所有的ouid
		alluid = etree.HTML(z.content).xpath('//div[@class="m-auto-box"]/@action-data')
		return alluid

def getst(url):
	z = requests.get(url,headers=headers)
	jscode = etree.HTML(z.content).xpath("//script[contains(., 'weibo')]/text()")[0].replace(u'<!--拆包页-->','')
	parsed_js  = js2xml.parse(jscode)
	st = parsed_js.xpath('//property[@name="st"]/string/text()')[0]
	return st

# 抢红包
def tj(url,uid,st,tjheaders):
	#生成需要发送的data
	data = {
		'groupid':'1000110',
		'uid':uid,
		'share':'1',
		'st':st
	}
	# 这里使用了post,headers增加了Referer
	z = requests.post(url,data=data,headers=tjheaders)
	#把得到的结果以json形式展示
	_ = z.json()
	#如果json中有“ok”,表示提交成功了，否则返回报错信息
	if _.has_key('ok'):
		print _['data']['error_msg']
	else:
		print _['errMsg']

if __name__ == '__main__':
	# 得到所有的uid
	uids = getuid()
	for uid in uids:
		#生成红包页面的url
		url = 'http://hongbao.weibo.com/h5/aboutyou?groupid=1000110&ouid=%s' %uid
		#获取st
		st = getst(url)
		#生成点击“抢红包”页面的url
		tjurl = 'http://hongbao.weibo.com/aj_h5/lottery?uid=%s&groupid=1000110&wm=' %uid
		# 添加Referer，如果不添加会报错
		headers['Referer'] = url
		tjheaders = headers
		try:
			# 点击“抢红包”
			tj(tjurl,uid,st,tjheaders)
		except:
			pass
