#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬取豆瓣电影top250 －－ 练习
"""


import requests
import codecs
from bs4 import BeautifulSoup

DOWNLOAD_ROUTE = "https://movie.douban.com/top250"


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html)

    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})

    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):

        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        # movie_name = detail.find('a').getText()
        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_ROUTE + next_page['href']
    return movie_name_list, None


def main():
    url = DOWNLOAD_ROUTE
    index = 1
    with codecs.open('/Users/tony/Desktop/reptile/practiceOnDouBan/TOP250', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            for movie in movies:
                # fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))
                fp.write(u'{index}. {movie}\n'.format(index=index, movie=movie))
                index += 1


if __name__ == '__main__':
    main()


