#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/11
"""
import logging
from estate_spyder.query import create_session, get_soup
from estate_spyder.lianjia_spyder import get_onsale_info, get_onsale_urls_by_xiaoqu

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s]-%(thread)d-%(levelname)s(%(name)s): %(message)s - %(filename)s:%(lineno)d')
    xiaoqu_id = [5011000010254, 5011000012609]
    sess = create_session()
    urls = get_onsale_urls_by_xiaoqu(xiaoqu_id[1], sess)
    print(len(urls))
    for url in urls:
        page_soup = get_soup(url, sess)
        estate_info = get_onsale_info(page_soup)
        break
    print(estate_info)
