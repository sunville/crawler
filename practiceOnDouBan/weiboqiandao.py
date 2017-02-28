#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
微博超级话题签到
"""

import requests
# from bs4 import BeautifulSoup

WEIBO_PROFILE_ROUTE = "http://www.weibo.com/p/1005051720322825/myfollow?relate=interested#place"
WEIBO_BUTTON = "http://weibo.com/p/aj/general/button"
WEIBO_INTEREST = "?ajwvr=6&api=http://i.huati.weibo.com/aj/supercheckin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD\
%BE%E5%88%B0&status=0&id="
SUFFIX = "&location=page_100808_super_index"


headers = {
    'Cookie': 'login_sid_t=ceba54a3086a80bdec2dc22d2d0587d5; _s_tentry=passport.weibo.com; YF-Page-G0=0dccd34751f51\
    84c59dfe559c12ac40a; Apache=4125769459642.4697.1444527509373; SINAGLOBAL=4125769459642.4697.1444527509373; YF-V\
    5-G0=e2def7ce19d3add53399b18462da454a; WBStore=562d07f6f00c6c6e|undefined; appkey=; TC-V5-G0=ac3bb62966dad84daf\
    a780689a4f7fc3; __gads=ID=b6ae295d02bcae1a:T=1468635297:S=ALNI_MYB5EOXPbMN9HROknhEt7n3Og_YVw; TC-Page-G0=9183dd\
    4bc08eff0c7e422b0d2f4eeaec; ULV=1475856396248:1:1:1:4125769459642.4697.1444527509373:; YF-Ugrow-G0=3a02f95fa8b3\
    c9dc73c74bc9f2ca4fc6; WBtopGlobal_register_version=c689c52160d0ea3b; _T_WM=88ba1d0357b31c7192a108ced780dc3c; wb_\
    g_upvideo_1720322825=1; UOR=,,login.sina.com.cn; SCF=AqghO-qv-TWiNcRwdPsnZCCSKaZehnx3ZDi8A8LPf-iaqViKGZ_d2cvGS9z\
    QWcvNiav4hTAkvn9hZ2CuKaru7j8.; SUB=_2A251qoGkDeRxGedJ6VIS8izEyTmIHXVWwfRsrDV8PUJbmtBeLRbnkW9i5QSQtZkTxv7yJ2yuUTp\
    zqdN20Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWMv4EMIHEOVxoePKL6VBLz5JpX5K2hUgL.Fo2Neo50eozReo-2dJLoIf2LxKBLB\
    onL1KqLxKML1K-L12eLxKMLB-eLB-eLxKBLBonL1h5LxKML1-2L1hBLxKnLBoMLB-qLxKML1KMLBoBLxKqLB--LB.qLxKBLBonL12zt; SUHB=0TP\
    UYq3d8kVGDZ; SSOLoginState=1487860212; un=19690501@qq.com; wvr=6',

    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.\
    0.2883.95 Safari/537.36'
}


def download_page(url):
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html)
    interests_list_soup = soup.find_all('li', attrs={'class': 'S_bg1'})
    interests_link_list = []

    for interest_li in interests_list_soup:
        detail = interest_li.find('div', attrs={'class': 'title'})
        interests_href = detail.find('a')['href']
        interests_id = interests_href[3:-12]
        interests_link_list.append(interests_id)

    return interests_link_list


def main():
    session = requests.Session()
    session.post('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)', data={})
    html = download_page(WEIBO_PROFILE_ROUTE)
    print html
    interests_id_list = parse_html(html)
    # interests_id_dic = {
    #     u'东方project': '1008080487013080224918ec707ae4a44afd2e',
    #     u'汪束': '100808122339c0988c9e0f2bc80cf78535c15d',
    #     u'祁静': '1008085ddf9d14db08045671c5c061d4da4218',
    #     u'曾艳芬': '100808a473fd8a93ee54443cca14bea11a8251',
    #     u'冯薪朵': '1008080f6421ae0a077187fcc7cc01fd4f4645',
    #     u'林思意': '100808d0c6c41e3c19537765aaf34b2e550e54',
    #     u'鞠婧祎': '1008086f1b7983ba4fca7456e28317e78127ed',
    #     u'杨冰怡': '10080818779a6837bc266c6d76e62febfe02f1',
    #     u'陆婷': '1008081774e0904c29efe3190815720ccffa6c'
    # }

    # for key in interests_id_dic.keys():
    for key in interests_id_list:
        interest_check_url = WEIBO_BUTTON+WEIBO_INTEREST+interests_id_dic[key]+SUFFIX
        print requests.get(interest_check_url, headers=headers).content


if __name__ == '__main__':
    main()
