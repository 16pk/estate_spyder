# -*- coding: utf-8 -*-
# __author__ = 'LiuHJ'
# __project__ = 'estate_spyder'
import logging
import pandas as pd
from datetime import datetime
from estate_spyder.query import create_session
from estate_spyder.lianjia_spyder import fetch_onsales_by_xiaoqu

xiaoqu_info = {'5011000012609': '玉兰香苑(二期)', \
               '5011102207601': '玉兰香苑(一期)', \
               '5011102207610': '玉兰香苑(三期)', \
               '5011102207585': '玉兰香苑(四期)', \
               '5011000010254': '益丰新村'}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s]-%(thread)d-%(levelname)s(%(name)s): %(message)s - %(filename)s:%(lineno)d')
    sess = create_session()
    onsale_infos = []
    for id, title in xiaoqu_info.items():
        logging.info(f'Fetch {title} information...')
        onsale_infos.append(fetch_onsales_by_xiaoqu(id, sess, 'estate_details'))
    pd.concat(onsale_infos).to_excel(f"estate_details/lianjia_stats_{datetime.now().strftime('%Y%m%d')}.xlsx")
