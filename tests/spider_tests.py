# pylint:disable-msg=W1401
"""
Unit tests for the spidering part of the trafilatura library.
"""

import logging
import sys

from collections import deque

import pytest

from courlan import UrlStore

from trafilatura import spider
from trafilatura.settings import DEFAULT_CONFIG

# language detection
try:
    import py3langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_redirections():
    "Test redirection detection."
    _, _, baseurl = spider.probe_alternative_homepage('xyz')
    assert baseurl is None
    _, _, baseurl = spider.probe_alternative_homepage('https://httpbin.org/gzip')
    assert baseurl == 'https://httpbin.org'
    #_, _, baseurl = spider.probe_alternative_homepage('https://httpbin.org/redirect-to?url=https%3A%2F%2Fhttpbin.org%2Fhtml&status_code=302')


def test_meta_redirections():
    "Test redirection detection using meta tag."
    htmlstring, homepage = '<html></html>', 'https://httpbin.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage
    htmlstring, homepage = '<html>REDIRECT!</html>', 'https://httpbin.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="0; url=1234"/></html>', 'https://httpbin.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 is None and homepage2 is None
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="0; url=https://httpbin.org/status/200"/></html>', 'http://test.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == '' and homepage2 == 'https://httpbin.org/status/200'


def test_process_links():
    "Test link extraction procedures."
    base_url = 'https://example.org'
    htmlstring = '<html><body><a href="https://example.org/page1"/><a href="https://example.org/page1/"/><a href="https://test.org/page1"/></body></html>'
    # 1 internal link in total
    spider.process_links(htmlstring, base_url)
    assert len(spider.URL_STORE.find_known_urls(base_url)) == 1
    assert len(spider.URL_STORE.find_unvisited_urls(base_url)) == 1
    # same with content already seen
    spider.process_links(htmlstring, base_url)
    assert len(spider.URL_STORE.find_unvisited_urls(base_url)) == 1 and len(spider.URL_STORE.find_known_urls(base_url)) == 1
    # test navigation links
    htmlstring = '<html><body><a href="https://example.org/tag/number1"/><a href="https://example.org/page2"/></body></html>'
    spider.process_links(htmlstring, base_url)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert todo[0] == 'https://example.org/tag/number1' and len(known_links) == 3
    # test language
    htmlstring = '<html><body><a href="https://example.org/en/page1"/></body></html>'
    spider.process_links(htmlstring, base_url, language='en')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert 'https://example.org/en/page1' in todo and len(known_links) == 4
    htmlstring = '<html><body><a href="https://example.org/en/page2"/></body></html>'
    spider.process_links(htmlstring, base_url, language='de')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    # wrong language, doesn't get stored anywhere (?)
    assert 'https://example.org/en/page2' not in todo and len(known_links) == 4
    # test queue evaluation
    todo = deque()
    assert spider.is_still_navigation(todo) is False
    todo.append('https://example.org/en/page1')
    assert spider.is_still_navigation(todo) is False
    todo.append('https://example.org/tag/1')
    assert spider.is_still_navigation(todo) is True


def test_crawl_logic():
    "Test functions related to crawling sequence and consistency."
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    # erroneous webpage
    with pytest.raises(ValueError):
        base_url, i, known_num, rules, is_on = spider.init_crawl('xyz', None, None)
    assert len(spider.URL_STORE.urldict) == 0
    # already visited
    base_url, i, known_num, rules, is_on = spider.init_crawl('https://httpbin.org/html', None, ['https://httpbin.org/html'])
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    # normal webpage
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    base_url, i, known_num, rules, is_on = spider.init_crawl('https://httpbin.org/html', None, None)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert todo == [] and known_links == ['https://httpbin.org/html'] and base_url == 'https://httpbin.org' and i == 1
    # delay between requests
    assert spider.get_crawl_delay(None) == 5
    assert spider.get_crawl_delay(rules) == 5
    assert spider.get_crawl_delay(rules, default=2.0) == 2.0


def test_crawl_page():
    "Test page-by-page processing."
    base_url = 'https://httpbin.org'
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(['https://httpbin.org/links/2/2'])
    is_on, known_num, visited_num = spider.crawl_page(0, 'https://httpbin.org')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert sorted(todo) == ['https://httpbin.org/links/2/0', 'https://httpbin.org/links/2/1']
    assert len(known_links) == 3 and visited_num == 1
    # initial page
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(['https://httpbin.org/html'])
    # if LANGID_FLAG is True:
    is_on, known_num, visited_num = spider.crawl_page(0, 'https://httpbin.org', initial=True, lang='de')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(todo) == 0 and len(known_links) == 1 and visited_num == 1
    ## TODO: find a better page for language tests



if __name__ == '__main__':
    test_redirections()
    test_meta_redirections()
    test_process_links()
    test_crawl_logic()
    test_crawl_page()

