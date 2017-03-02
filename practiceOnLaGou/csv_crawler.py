#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodecsv as csv
import requests
import json
import time
import codecs
import os

global page
page = 1

REQUEST_URL = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'


def download_json(url,POST_DATA):
	r = requests.post(url,data=POST_DATA,headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4',
        'Cookie': 'user_trace_token=20170226193129-41ce0fcd7d6e4355b9e2fb8189da8fed; LGUID=20170226193130-1e2f8576-fc17-11e6-8dcc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=4A3745C108594AE553C95E27594B4F1C; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FlabelWords%3Dlabel; TG-TRACK-CODE=index_search; SEARCH_ID=0d2a41cce279489a9941f0797bde2697; _ga=GA1.2.2085845228.1488108693; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1488108693; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1488388441; LGSID=20170302010615-61799a6c-fea1-11e6-a6ad-525400f775ce; LGRID=20170302011345-6d511a93-fea2-11e6-a6ad-525400f775ce'
    })
	return r.json()


def parse_json(json_obj) :
	Recruitment = json_obj['content']['positionResult']['result']
	Recruitment_list = []
	for wr in Recruitment:
		job = {
			'companyShortName': wr['companyShortName'],
			'positionName': wr['positionName'],
			'salary': wr['salary']
		}
		Recruitment_list.append(job)
	return Recruitment_list



def main():
	url = REQUEST_URL
	global page
	data = {
		'first': 'true',
		'pn': '1',
		'kd': 'Python' 
		}
	with open('../practiceOnLaGou/result.csv', 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, encoding='utf-8')
		csvwriter.writerow((u'公司名称',u'职位',u'薪水'));
		while page < 3:
			time.sleep(1)
			json_obj = download_json(url, data)
			Recruitment = parse_json(json_obj)
			
			for job in Recruitment:
				csvwriter.writerow((job['companyShortName'],job['positionName'],job['salary']))
			page += 1
			data['first'] = 'false'
			data['pn'] = str(page)

	os.system('iconv -f UTF-8 -t GB18030 result.csv > result_xls.csv')


if __name__ == '__main__':
	main()