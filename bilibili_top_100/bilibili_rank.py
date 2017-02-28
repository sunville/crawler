#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
练习爬取bilibili三日内排行前100
"""

import requests
import codecs
from bs4 import BeautifulSoup

BILIBILI_RANK_URL = "https://www.bilibili.com/ranking"
BILIBILI_URL = "http://www.bilibili.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2\
    924.87 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Upgrade-Insecure-Requests': '1'
}


def download_url(url):
    html = requests.get(url, headers=headers).content
    return html


def parse_html(html):
    soup = BeautifulSoup(html)
    video_list = soup.find('ul', attrs={'class': 'rank-list'})
    video_elements = []

    for video in video_list.find_all('li'):
        video_item = {}

        video_number = video.find('div', attrs={'class': 'num'}).getText()
        video_item['Rank'] = video_number

        video_link = BILIBILI_URL + video.find('a')['href']
        video_item['Link'] = video_link

        video_name = video.find('div', attrs={'class': 'title'}).getText()
        video_item['Name'] = video_name

        video_elements.append(video_item)

    return video_elements


def main():
    html = download_url(BILIBILI_RANK_URL)
    video_elements = parse_html(html)
    with codecs.open('/Users/tony/Desktop/reptile/bilibili_top_100/TOP100_3_days', 'wb', encoding='utf-8') as fp:
        for video in video_elements:
            fp.write(u'排名{Rank}: {Name}\n 链接: {Link}\n').format(Rank=video['Rank'], Name=video['Name'], Link=video['Link'])


if __name__ == '__main__':
    main()
