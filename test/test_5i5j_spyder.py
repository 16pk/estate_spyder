# -*- coding: utf-8 -*-
# __author__ = 'LiuHJ'
# __project__ = 'estate_spyder'
import logging
from estate_spyder.query import create_session, get_soup
from estate_spyder.woaiwojia_spyder import fetch_onsales_by_xiaoqu, get_onsale_info, get_onsale_urls_by_xiaoqu, fetch_photos

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s]-%(thread)d-%(levelname)s(%(name)s): %(message)s - %(filename)s:%(lineno)d')
    sess = create_session()
    xiaoqu_id = [380170, 423303, 378510]
    # urls = get_onsale_urls_by_xiaoqu(xiaoqu_id[1], sess)
    # print(len(urls))
    # url = 'https://sh.5i5j.com/ershoufang/40645553.html'
    # soup = get_soup(url, sess)
    # infos = get_onsale_info(soup)
    # fetch_photos(soup, sess, '../estate_details')
    infos = fetch_onsales_by_xiaoqu(xiaoqu_id[2], sess, '../estate_details')
    print(infos)