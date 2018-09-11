# -*- coding: utf-8 -*-
# __author__ = 'LiuHJ'
# __project__ = 'estate_spyder'

import logging
import requests
from bs4 import BeautifulSoup

from . import CONFIG

logger = logging.getLogger(__name__)


def create_session():
    headers = {'User-Agent': CONFIG['request'].get('userAgent')}
    sess = requests.Session()
    sess.headers = headers
    return sess


def get_soup(url, sess=None):
    if sess is None:
        sess = create_session()
    resp = sess.get(url)
    resp.raise_for_status()
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup
