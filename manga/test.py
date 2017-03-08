#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import codecs
import os
from PIL import Image
from lxml import etree

MANGA_URL = "http://www.tazhe.com"
MANGA_INDEX_URL = "http://www.tazhe.com/mh/9170/"

Headers = {
	'Cookie':'bdshare_firstime=1488287655175; qtmhhis=2017-2-4-14-29-32%5E%5E%u6781%u9ED1%u7684%u5E03%u4F26%u5E0C%u5C14%u7279%5E%5E%u7B2C181%u8BDD%5E%5E2%5E%5E1747033%5E%5E9170_ShG_; Hm_lvt_d01e14f14b939b0db9ad1607a9b968b1=1488287656; Hm_lpvt_d01e14f14b939b0db9ad1607a9b968b1=1488608972',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def get_all_pages(url):
	html = requests.get(url, headers=Headers)
	indices_names = []
	for link in etree.HTML(html.content).xpath('//div[@id="play_0"]//ul//li//a'):
		item = {}
		item['name'] = link.text.strip()
		item['url'] = link.xpath('@href')[0]
		indices_names.append(item)
	return indices_names


def download_manga(directory,url):



def main():
	indices_names = get_all_pages(MANGA_INDEX_URL);

	PATH = u'/Users/tony/Desktop/Brynhildr_in_the_Darkness/'

	for item in indices_names:
		name = item['name']
		directory = PATH + name
		if not os.path.exists(directory):
			os.makedirs(directory)
		url = MANGA_URL + item['url']
		download_manga(directory,url)



if __name__ == '__main__':
	main()