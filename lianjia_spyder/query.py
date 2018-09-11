# -*- coding: utf-8 -*-
# __author__ = 'LiuHJ'
# __project__ = 'estate_spyder'

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def create_session():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
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
