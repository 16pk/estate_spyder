# -*- coding: utf-8 -*-
# __author__ = 'LiuHJ'
# __project__ = 'estate_spyder'
import logging
import time
import json
import os
import os.path
import pandas as pd
from . import CONFIG
from .query import get_soup

logger = logging.getLogger(__name__)
URL = CONFIG['url']['5i5j']


def check_next_page(soup):
    page_soup = soup.find(class_='pageBox')
    next_page = page_soup.find(text='下一页', name='a')
    if next_page is not None:
        return True, URL + next_page['href']
    else:
        return False, ''


def get_onsale_urls_by_xiaoqu(xiaoqu_id, sess):
    has_next_page = True
    onsale_urls = []
    crt_url = f'{URL}/xq-ershoufang/{xiaoqu_id}/'
    while has_next_page:
        logger.info(f'Surfing {crt_url} ...')
        soup = get_soup(crt_url, sess)
        sell_soup_list = soup.find(class_='list-con-box').find_all(class_='listImg')
        onsale_urls += [URL + x.a['href'] for x in sell_soup_list]
        has_next_page, crt_url = check_next_page(soup)
        time.sleep(1.9)
    return onsale_urls


def get_onsale_info(soup):
    info_dict = {}
    title_tag = soup.find(class_='house-tit')
    info_dict['标题'] = str(title_tag.string)
    labels = title_tag.next_sibling.next_sibling.string.replace('：', '|').split('|')
    info_dict['标签'] = labels[0]
    info_dict['id'] = labels[2]
    overview = soup.find(class_='content fr')
    tag_total = overview.find('p', text='售价(万)')
    info_dict['总价'] = float(tag_total.previous_sibling.previous_sibling.string)
    tag_unit = overview.find('p', text='单价(万/m²)')
    info_dict['单价'] = float(tag_unit.previous_sibling.previous_sibling.string)
    tag = overview.find('span', text='小区：')
    info_dict['小区'] = str(tag.next_sibling.string)
    tag = overview.find('span', text='朝向：')
    if tag is not None:
        info_dict['朝向'] = str(tag.next_sibling.string)
    tag = overview.find('span', text='装修：')
    if tag is not None:
        info_dict['装修'] = str(tag.next_sibling.string)
    base_info = soup.find(class_='saleinfo')
    for x in base_info.find_all('li'):
        info_key = str(x.contents[0].string)
        info_dict[info_key] = str(x.contents[1].string)
    info_dict['建筑面积'] = float(info_dict['建筑面积'][:-3])
    if '建筑年代' in info_dict:
        info_dict['建筑年代'] = int(info_dict['建筑年代'][:-1])
    return info_dict


def fetch_photos(soup, sess, folder):
    tag_now_list = soup.find_all(class_='tag-now')
    has_photo = False
    for tag_now in tag_now_list:
        if tag_now.find(class_='titleinfo').contents[1] == '房源图片':
            has_photo = True
            break
    if not has_photo:
        return
    photo_tag = tag_now.find_all(lambda x: x.has_attr('href'))
    photo_links = [x['href'] for x in photo_tag]
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
        target_folder = os.path.join(path, '5i5j', f"{estate_infos[-1]['id']}")
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
            fetch_photos(crt_soup, sess, target_folder)
        time.sleep(5.3)
    return pd.DataFrame(estate_infos)
