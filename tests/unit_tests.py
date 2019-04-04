# -*- coding: utf-8 -*-
"""
Unit tests for the htmldate library.
"""

import logging
import os
import sys
# https://docs.pytest.org/en/latest/

import textract

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


MOCK_PAGES = { \
'http://blog.python.org/2016/12/python-360-is-now-available.html': 'blog.python.org.html', \
}
# 


TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def load_mock_page(url):
    '''load mock page from samples'''
    with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
        htmlstring = inputf.read()
    return htmlstring


if __name__ == '__main__':
    load_mock_page()
