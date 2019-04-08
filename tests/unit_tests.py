# -*- coding: utf-8 -*-
"""
Unit tests for the html-extractor library.
"""

import logging
import os
import sys
# https://docs.pytest.org/en/latest/

import html_extractor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


MOCK_PAGES = { \
'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/': 'die-partei.net.luebeck.html', \
'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html': 'bmjv.de.konsum.html', \
}
# '': '', \


TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def load_mock_page(url):
    '''load mock page from samples'''
    with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
        htmlstring = inputf.read()
    return htmlstring

def test_trim():
    '''test string trimming'''
    assert html_extractor.trim('	Test  ') == 'Test'
    assert html_extractor.trim('\t\tTest  Test\r\n') == 'Test Test'

def test_main():
    '''test extraction from HTML'''
    url = 'https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/'
    result = html_extractor.process_record(load_mock_page(url), url, '0000')
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result
    url = 'https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html'
    result = html_extractor.process_record(load_mock_page(url), url, '0000')
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result



if __name__ == '__main__':
    test_trim()
    test_main()