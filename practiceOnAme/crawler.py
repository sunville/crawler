#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import codecs
from bs4 import BeautifulSoup
import os

URL = "https://amentranslations.wordpress.com/catalogue/diao-ye-zong-%E5%87%8B%E5%8F%B6%E6%A3%95/"
DIR = "/Users/tony/Desktop/reptile/practiceOnAme/diao_ye_zong/"
Headers = {
	'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def get_lyrics_urls(url,Headers):
	html = requests.get(url,headers = Headers)
	urls = []
	soup = BeautifulSoup(html.content,"lxml")
	soup = soup.find("div",{"class":"entry-content"})
	
	for div in soup.find_all("div"):
		div.decompose()
	for link in soup.find_all("a"):
		item = {}
		item['url'] = link.get('href')
		item['name'] = link.getText()
		urls.append(item)
	return urls


def get_lyrics(url):
	html = requests.get(url,headers=Headers)
	soup = BeautifulSoup(html.content,"lxml")
	lyrics = soup.find("div",{"class":"entry-content"})
	for div in lyrics.find_all("div"):
		div.decompose()
	return lyrics


def touch(path):
	try:
		with codecs.open(path, 'a', encoding="utf-8") as f:
			os.utime(path, None)
	except IOError:
		print "IOError happened"


def main():
	urls = get_lyrics_urls(URL,Headers)

	for item in urls:
		name = item['name'] + ".html"
		name = name.replace('/',u'／')

		directory = DIR + name
		if not os.path.exists(directory):
			touch(directory)
			try:
				with codecs.open(directory, 'wb') as fp:
					url = item['url']
					lyrics = get_lyrics(url)
					fp.write(lyrics.prettify().encode('utf-8'))
			except IOError:
				print "IOError happened"


if __name__ == '__main__':
	main()