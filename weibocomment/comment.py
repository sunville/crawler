#!/usr/bin/env python
# -*- coding: utf-8 -*-
#get SNH48-汪束 all comments
#https://m.weibo.cn/u/5491330253
#评论列表 A
#https://m.weibo.cn/api/comments/show?id=4141483370455347&page=1
#https://m.weibo.cn/api/comments/show?id={weibo_id}&page={index}
#微博列表 B
#https://m.weibo.cn/api/container/getIndex?type=uid&value=5491330253&containerid=1076035491330253&page=1
#https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}&page={page}
#个人主页信息 C
#https://m.weibo.cn/api/container/getIndex?type=uid&value=5491330253&containerid=1005055491330253
#https://m.weibo.cn/api/container/getIndex?type=uid&value={usr_id}
# visit C to get B, visit B to get A
#https://m.weibo.cn/api/container/getIndex?type=uid&value=5491330253&containerid=1005055491330253
import requests
import time
import codecs

headers={
	'Cookie':'_T_WM=289d2f7510223212daa1a7e6dd71367c; ALF=1505492251; SCF=AqghO-qv-TWiNcRwdPsnZCCSKaZehnx3ZDi8A8LPf-iaZE8RZjKzbaojzoVEPLM-3vfWmZfqAhfThv8NeHS-d88.; SUB=_2A250kABMDeRhGedJ6VIS8izEyTmIHXVUeqAErDV6PUJbktAKLVnhkW0Zal04dWb1IxDrmZMf8e6ea7OcIQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWMv4EMIHEOVxoePKL6VBLz5JpX5o2p5NHD95QpS0z7e0zE1hzfWs4Dqc_xi--Xi-zRiK.ci--NiK.fiKyhi--Ni-8hi-8hi--Xi-zRiKn7i--NiKLWiKnXi--Ri-zNi-8si--NiK.Ni-zXi--ci-88i-isi--Xi-zRiKyF; SUHB=0XDkJyZohieuN0; SSOLoginState=1502900252; M_WEIBOCN_PARAMS=fid%3D1005055491330253%26uicode%3D10000011',
	'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25'
}


def get_comments(wb_id):
	#max (total pages)
	#total_number (total comments)
	#data (comment contents)
	#hot_data (only response when page=1)
	#hot_total_number (only response when page=1)
	Data = []
	url = 'https://m.weibo.cn/api/comments/show?id={id}'.format(id=wb_id)
	page_url = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'
	Resp = requests.get(url, headers=headers)
	page_max_num = Resp.json()['max']
	for i in range(1, page_max_num, 1):
		p_url = page_url.format(id=wb_id, page=i)
		resp = requests.get(p_url, headers=headers)
		resp_data = resp.json()
		data = resp_data.get('data')
		for d in data:
			review_id = d['id']
			like_counts = d['like_counts']
			source = d['source']
			username = d['user']['screen_name']
			image = d['user']['profile_image_url']
			verified = d['user']['verified']
			verified_type = d['user']['verified_type']
			profile_url = d['user']['profile_url']
			comment = d['text']
		time.sleep(1)


def wb_basic_elements(wb_id):
	Data = []
	url = 'https://m.weibo.cn/api/comments/show?id={id}'.format(id=wb_id)
	page_url = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'
	Resp = requests.get(url, headers=headers)
	return Data


def mblog_list(uid, oid):
	Mblog_list = []
	Mpic_list = []
	base_url = 'https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}'
	page_url = 'https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}&page={page}'
	url = base_url.format(oid=oid, uid=uid)
	resp = requests.get(url, headers=headers)
	resp.encoding = 'gbk'
	response = resp.json()
	total = response['cardlistInfo']['total'] # all wb elements !! not equal to actual weibo counts
	page_num = int(int(total) / 10) + 1 # pages amount
	for i in range(1, page_num + 1, 1):
		p_url = page_url.format(oid=oid, uid=uid, page=i)
		page_resp = requests.get(p_url, headers=headers)
		page_data = page_resp.json()
		cards = page_data['cards']
		for card in cards:
			if 'mblog' in card:
				mblog = card['mblog']
				created_at = mblog['created_at']
				if len(created_at) == 5:
					created_at = '2017-' + created_at
				id = mblog['id']
				text = mblog['text']
				reposts_count = mblog['reposts_count']
				comments_count = mblog['comments_count']
				attitudes_count = mblog['attitudes_count']
				mblog_data = {'created_at': created_at, 'id': id, 'text': text, 'reposts_count': reposts_count,
								  'comments_count': comments_count, 'attitudes_count': attitudes_count}
				Mblog_list.append(mblog_data)
				if 'pics' in mblog:
					pics = mblog['pics']
					for index,pic in enumerate(pics):
						pic_url = {'url':pic['url'], 'created_at':created_at, 'index':str(index)}
						Mpic_list.append(pic_url)
				# print(' ' * 10, mblog_data)
		#time.sleep(1)
	return Mblog_list,Mpic_list


def usr_info(usr_id):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={usr_id}'.format(usr_id=usr_id)
    resp = requests.get(url, headers=headers)
    jsondata = resp.json()
    uid = jsondata.get('userInfo').get('toolbar_menus')[0].get('params').get('uid')
    fid = jsondata.get('userInfo').get('toolbar_menus')[1].get('actionlog').get('fid')
    oid = jsondata.get('userInfo').get('toolbar_menus')[2].get('params').get('menu_list')[0].get('actionlog').get('oid')
    cardid = jsondata.get('userInfo').get('toolbar_menus')[1].get('actionlog').get('cardid')
    containerid = jsondata.get('tabsInfo').get('tabs')[1].get('containerid')
    Info = {'uid': uid, 'fid': fid,
            'cardid': cardid, 'containerid': containerid, 'oid': oid}
    # print(Info)
    return Info


if __name__ == '__main__':
	#Info = {'uid': uid, 'fid': fid,
    #        'cardid': cardid, 'containerid': containerid, 'oid': oid}
	Info = usr_info('5491330253')
	Mblog_list,Mpic_list = mblog_list(Info['uid'],Info['containerid'])
# mblog_data = {'index':i ,'created_at': created_at, 'id': id, 'text': text, 'reposts_count': 
# reposts_count,'comments_count': comments_count, 'attitudes_count': attitudes_count}
	# with codecs.open('wangshu.txt','wb',encoding='utf-8') as fp:
	# 	fp.write(u'created_at\treposts_count\tcomments_count\tattitudes_count\ttext\n')
	# 	for item in reversed(Mblog_list):
	# 		fp.write(u'{created_at}\t{reposts_count}\t{comments_count}\t{attitudes_count}\t{text}\n'\
	# 			.format(created_at=item['created_at'],reposts_count=item['reposts_count'],\
	# 				comments_count=item['comments_count'],attitudes_count=item['attitudes_count'],\
	# 				text=item['text']))
	for pic in Mpic_list:
		r = requests.get(pic['url'],stream=True)
		path = 'pic/' + pic['created_at'] + '_' + pic['index']
		if r.status_code == 200:
			with open(path ,'wb') as f:
				for chunk in r:
					f.write(chunk)
