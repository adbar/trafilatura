# -*- coding: utf-8 -*-
"""
Unit tests for the html-extractor library.
"""

import logging
import os
import sys
# https://docs.pytest.org/en/latest/

import html-extractor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


MOCK_PAGES = { \
'https://die-partei.net/sh/': 'die-partei.net.sh.html', \
}
# '': '', \


TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def load_mock_page(url):
    '''load mock page from samples'''
    with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
        htmlstring = inputf.read()
    return htmlstring

def test_main():
    '''test extraction from HTML'''
    assert html-extractor.process_record(load_mock_page('https://die-partei.net/sh/'), 'https://die-partei.net/sh/', '0000') is not None


if __name__ == '__main__':
    test_main()