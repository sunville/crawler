#!/usr/bin/env python2

# -*- coding: utf-8 -*-

import requests
import json
import time
import codecs

global page
page = 1

REQUEST_URL = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'


def download_json(url,POST_DATA):
	r = requests.post(url,data=POST_DATA,headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4',
        'Cookie': 'YOUR_COOKIE_HERE'
    })
	return r.json()


def parse_json(json_obj) :
	Recruitment = json_obj['content']['positionResult']['result']
	Recruitment_list = []
	for wr in Recruitment:
		Recruitment_list.append(wr['companyShortName'])
		Recruitment_list.append(wr['positionName'])
		Recruitment_list.append(wr['salary'])
	return Recruitment_list



def main():
	url = REQUEST_URL
	global page
	data = {
		'first': 'true',
		'pn': '1',
		'kd': 'Python' 
		}
	with codecs.open('/Users/tony/Desktop/reptile/practicOnLaGou/result.txt', 'wb', encoding='utf-8') as fp:
		while page < 3:
			time.sleep(3)
			json_obj = download_json(url, data)
			Recruitment = parse_json(json_obj)
			fp.write(u'{Recruitment}\n'.format(Recruitment='\n'.join(Recruitment)))
			# strings = json.dumps(json_obj).decode(encoding='utf-8',errors='strict')
			# fp.write(u'{strings}'.format(strings=strings))
			page += 1
			data['first'] = 'false'
			data['pn'] = str(page)



if __name__ == '__main__':
	main()