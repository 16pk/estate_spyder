#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/3
"""
import logging
import requests
import time
from bs4 import BeautifulSoup
import json

logger = logging.getLogger(__name__)

URL = 'https://sh.lianjia.com'


def create_session():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    sess = requests.Session()
    sess.headers = headers
    return sess


def check_next_page(soup):
    page_soup = soup.find(class_='page-box fr')
    page_info = json.loads(page_soup.div['page-data'])
    if page_info['curPage'] < page_info['totalPage']:
        return True, page_info['curPage'] + 1
    else:
        return False, -1


def get_selling_urls(xiaoqu_id, sess=None):
    if sess is None:
        sess = create_session()
    has_next_page = True
    page_no = 1
    selling_urls = []
    while has_next_page:
        if page_no == 1:
            crt_url = f'{URL}/ershoufang/c{xiaoqu_id}/'
        else:
            crt_url = f'{URL}/ershoufang/pg{page_no}c{xiaoqu_id}/'
        try:
            resp = sess.get(crt_url)
            resp.raise_for_status()
        except requests.HTTPError:
            continue
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        sell_soup_list = soup.find(class_='sellListContent').find_all(class_='title')
        crt_selling_urls = [x.a['href'] for x in sell_soup_list]
        selling_urls += crt_selling_urls
        has_next_page, page_no = check_next_page(soup)
        time.sleep(4.3)
    return selling_urls


KEY_MAPPING = {'房屋户型': 'hu_xing', '所在楼层': 'lou_ceng', '建筑面积': 'size', '户型结构': 'hu_xing_jie_gou', '套内面积': 'inner_size',
               '建筑类型': 'jian_zhu_lei_xing', '房屋朝向': 'orientation', '建筑结构': 'jian_zhu_jie_gou', '装修情况': 'zhuang_xiu',
               '梯户比例': 'ti_hu_ratio', '配备电梯': 'has_elevator', '产权年限': 'chan_quan_nian_xian'}


def get_selling_details(url, sess=None):
    if sess is None:
        sess = create_session()
    try:
        resp = sess.get(url)
        resp.raise_for_status()
    except requests.HTTPError:
        return
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    info_dict = {'url': url}
    info_dict['title'] = str(soup.find(class_='sellDetailHeader').find(class_='main').string)
    overview = soup.find(class_='overview').find(class_='content')
    info_dict['community'] = str(overview.find(class_='communityName').a.string)
    info_dict['price'] = float(overview.find(class_='total').string)
    info_dict['unitPrice'] = float(overview.find(class_='unitPriceValue').contents[0])
    info_dict['lianjia_id'] = str(overview.find(class_='houseRecord').find(class_='info').contents[0])
    base_info = soup.find(class_='introContent').find(class_='content')
    for x in base_info.find_all('li'):
        info_key = KEY_MAPPING[str(x.span.string)]
        info_dict[info_key] = str(x.contents[1])
    return info_dict


if __name__ == '__main__':
    xiaoqu_id = [5011000010254, 5011000012609]
    sess = create_session()
    urls = get_selling_urls(xiaoqu_id[1], sess)
    print(len(urls))
    estate_info = get_selling_details(urls[2], sess)
    print(estate_info)
