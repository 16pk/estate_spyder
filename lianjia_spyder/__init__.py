#!/usr/bin/env python
# encoding: utf-8
"""
@author: hongjian.liu
@date:   2018/9/3
"""
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s]-%(thread)d-%(levelname)s(%(name)s): %(message)s - %(filename)s:%(lineno)d')