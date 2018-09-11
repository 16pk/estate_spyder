#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/3
"""
import logging
import time
from datetime import datetime
import json
from . import CONFIG
from .query import get_soup

logger = logging.getLogger(__name__)
URL = CONFIG['url']['lianjia']
KEY_MAPPING = {'房屋户型': 'hu_xing', '所在楼层': 'lou_ceng', '建筑面积': 'size', '户型结构': 'hu_xing_jie_gou', '套内面积': 'inner_size',
               '建筑类型': 'jian_zhu_lei_xing', '房屋朝向': 'orientation', '建筑结构': 'jian_zhu_jie_gou', '装修情况': 'zhuang_xiu',
               '梯户比例': 'ti_hu_ratio', '配备电梯': 'has_elevator', '产权年限': 'chan_quan_nian_xian'}


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
        soup = get_soup(crt_url, sess)
        sell_soup_list = soup.find(class_='sellListContent').find_all(class_='title')
        onsale_urls += [x.a['href'] for x in sell_soup_list]
        has_next_page, page_no = check_next_page(soup)
        time.sleep(4.3)
    return onsale_urls


def get_onsale_info(page_soup):
    info_dict = {'queryTime': datetime.utcnow()}
    info_dict['title'] = str(page_soup.find(class_='sellDetailHeader').find(class_='main').string)
    overview = page_soup.find(class_='overview').find(class_='content')
    info_dict['community'] = str(overview.find(class_='communityName').a.string)
    info_dict['price'] = float(overview.find(class_='total').string)
    info_dict['unitPrice'] = float(overview.find(class_='unitPriceValue').contents[0])
    info_dict['lianjia_id'] = str(overview.find(class_='houseRecord').find(class_='info').contents[0])
    base_info = page_soup.find(class_='introContent').find(class_='content')
    for x in base_info.find_all('li'):
        info_key = KEY_MAPPING[str(x.span.string)]
        info_dict[info_key] = str(x.contents[1])
    return info_dict


# todo: 抓图片，因为成交后就看不到图片了
def fetch_photos(page_soup, folder):
    photo_tag = page_soup.find(class_='housePic')
    photo_links = [x.get('src') for x in photo_tag.find_all('img')]
    pass
