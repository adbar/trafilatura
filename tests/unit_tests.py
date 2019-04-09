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
'http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/': 'kulinariaathome.com.mandelplätzchen.html', \
'https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/': 'denkanstoos.com.2012.html', \
'http://bunterepublik.wordpress.com/2012/04/13/schwafelrunde-ohne-ritter/': 'bunterepublik.com.schwafelrunde.html', \
}
# '': '', \


TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def load_mock_page(url):
    '''load mock page from samples'''
    with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
        htmlstring = inputf.read()
    result = html_extractor.process_record(htmlstring, url, '0000')
    return result

def test_trim():
    '''test string trimming'''
    assert html_extractor.trim('	Test  ') == 'Test'
    assert html_extractor.trim('\t\tTest  Test\r\n') == 'Test Test'

def test_main():
    '''test extraction from HTML'''
    result = load_mock_page('https://die-partei.net/luebeck/2012/05/31/das-ministerium-fur-club-kultur-informiert/')
    assert 'Impressum' not in result and 'Die GEMA dreht völlig am Zeiger!' in result

    result = load_mock_page('https://www.bmjv.de/DE/Verbraucherportal/KonsumImAlltag/TransparenzPreisanpassung/TransparenzPreisanpassung_node.html')
    assert 'Impressum' not in result and 'Anbieter von Fernwärme haben innerhalb ihres Leitungsnetzes ein Monopol' in result

    result = load_mock_page('https://denkanstoos.wordpress.com/2012/04/11/denkanstoos-april-2012/')
    assert result is None

    result = load_mock_page('http://bunterepublik.wordpress.com/2012/04/13/schwafelrunde-ohne-ritter/')
    assert 'Abgelegt unter' not in result and 'Nächster Beitrag' not in result and 'Die Schwafelrunde' in result and 'zusammen.' in result


    #result = load_mock_page('http://kulinariaathome.wordpress.com/2012/12/08/mandelplatzchen/')
    #print(result)
    #assert 'Gefällt mir' not in result and 'Trotz sorgfältiger inhaltlicher Kontrolle' not in result and '200 g Zucker' in result and 'Ein Backblech mit Backpapier auslegen.' in result




if __name__ == '__main__':
    test_trim()
    test_main()