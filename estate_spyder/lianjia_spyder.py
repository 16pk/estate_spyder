#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/3
"""
import logging
import time
import json
import os
import os.path
import pandas as pd
from . import CONFIG
from .query import get_soup

logger = logging.getLogger(__name__)
URL = CONFIG['url']['lianjia']


def check_next_page(soup):
    page_soup = soup.find(class_='page-box fr')
    page_info = json.loads(page_soup.div['page-data'])
    if page_info['curPage'] < page_info['totalPage']:
        return True, page_info['curPage'] + 1
    else:
        return False, -1


def get_onsale_urls_by_xiaoqu(xiaoqu_id, sess):
    has_next_page = True
    page_no = 1
    onsale_urls = []
    while has_next_page:
        if page_no == 1:
            crt_url = f'{URL}/ershoufang/c{xiaoqu_id}/'
        else:
            crt_url = f'{URL}/ershoufang/pg{page_no}c{xiaoqu_id}/'
        logger.info(f'Surfing {crt_url} ...')
        soup = get_soup(crt_url, sess)
        sell_soup_list = soup.find(class_='sellListContent').find_all(class_='title')
        onsale_urls += [x.a['href'] for x in sell_soup_list]
        has_next_page, page_no = check_next_page(soup)
        time.sleep(1.9)
    return onsale_urls


def get_onsale_info(soup):
    info_dict = {}
    info_dict['标题'] = str(soup.find(class_='sellDetailHeader').find(class_='main').string)
    overview = soup.find(class_='overview').find(class_='content')
    info_dict['小区'] = str(overview.find(class_='communityName').a.string)
    info_dict['总价'] = float(overview.find(class_='total').string)
    info_dict['单价'] = float(overview.find(class_='unitPriceValue').contents[0])
    info_dict['年份'] = overview.find(class_='area').find(class_='subInfo').string.split('年')[0]
    info_dict['lianjia_id'] = str(overview.find(class_='houseRecord').find(class_='info').contents[0])
    base_info = soup.find(class_='introContent').find(class_='content')
    for x in base_info.find_all('li'):
        info_key = str(x.span.string)
        info_dict[info_key] = str(x.contents[1])
    info_dict['建筑面积'] = float(info_dict['建筑面积'][:-2])
    return info_dict


def fetch_photos(soup, sess, folder):
    photo_tag = soup.find(class_='housePic')
    if photo_tag is None:
        os.rmdir(folder)
        return
    photo_links = [x.get('src') for x in photo_tag.find_all('img')]
    for link in photo_links:
        filename = os.path.join(folder, link.split('/')[-1])
        req = sess.get(link)
        if req.status_code == 200:
            with open(filename, 'wb') as fid:
                fid.write(req.content)


def fetch_onsales_by_xiaoqu(xiaoqu_id, sess, path='estate_details'):
    urls = get_onsale_urls_by_xiaoqu(xiaoqu_id, sess)
    estate_infos = []
    for url in urls:
        logger.info(f'Surfing {url} ...')
        crt_soup = get_soup(url, sess)
        crt_info = get_onsale_info(crt_soup)
        crt_info['url'] = url
        estate_infos.append(crt_info)
        target_folder = os.path.join(path, 'lianjia', f"lianjia_{estate_infos[-1]['lianjia_id']}")
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
            fetch_photos(crt_soup, sess, target_folder)
        time.sleep(5.3)
    return pd.DataFrame(estate_infos)
