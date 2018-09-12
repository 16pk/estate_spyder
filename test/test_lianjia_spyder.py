#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/11
"""
import logging
from estate_spyder.query import create_session
from estate_spyder.lianjia_spyder import fetch_onsales_by_xiaoqu

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s]-%(thread)d-%(levelname)s(%(name)s): %(message)s - %(filename)s:%(lineno)d')
    xiaoqu_id = [5011000010254, 5011000012609]
    sess = create_session()
    infos = fetch_onsales_by_xiaoqu(xiaoqu_id[1], sess, '../estate_details')
    print(infos)

