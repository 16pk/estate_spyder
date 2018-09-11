#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/3
"""
import logging
import configparser
import os.path

logging.getLogger(__name__).addHandler(logging.NullHandler())
CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))
