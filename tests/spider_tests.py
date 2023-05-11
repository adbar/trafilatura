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
    _, _, baseurl = spider.probe_alternative_homepage('https://httpbun.org/redirect-to?url=https://httpbin.org')
    assert baseurl == 'https://httpbin.org'
    #_, _, baseurl = spider.probe_alternative_homepage('https://httpbin.org/redirect-to?url=https%3A%2F%2Fhttpbin.org%2Fhtml&status_code=302')


def test_meta_redirections():
    "Test redirection detection using meta tag."
    # empty
    htmlstring, homepage = '"refresh"', 'https://httpbun.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage
    htmlstring, homepage = '<html></html>', 'https://httpbun.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage

    # unusable
    htmlstring, homepage = '<html>REDIRECT!</html>', 'https://httpbun.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage

    # malformed
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="3600\n&lt;meta http-equiv=" content-type=""></html>', 'https://httpbun.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 == htmlstring and homepage2 == homepage

    # wrong URL
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="0; url=1234"/></html>', 'https://httpbun.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 is None and homepage2 is None

    # normal
    htmlstring, homepage = '<html><meta http-equiv="refresh" content="0; url=https://httpbun.org/html"/></html>', 'http://test.org/'
    htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
    assert htmlstring2 is not None and homepage2 == 'https://httpbun.org/html'


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
    # test cleaning and language
    htmlstring = '<html><body><a href="https://example.org/en/page1/?"/></body></html>'
    spider.process_links(htmlstring, base_url, language='en')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert 'https://example.org/en/page1/' in todo and len(known_links) == 4
    # wrong language
    htmlstring = '<html><body><a href="https://example.org/en/page2"/></body></html>'
    spider.process_links(htmlstring, base_url, language='de')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
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
    base_url, i, known_num, rules, is_on = spider.init_crawl('https://httpbun.org/html', None, ['https://httpbun.org/html'])
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    # normal webpage
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    base_url, i, known_num, rules, is_on = spider.init_crawl('https://httpbun.org/html', None, None)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert todo == [] and known_links == ['https://httpbun.org/html'] and base_url == 'https://httpbun.org' and i == 1
    # delay between requests
    assert spider.URL_STORE.get_crawl_delay('https://httpbun.org') == 5
    assert spider.URL_STORE.get_crawl_delay('https://httpbun.org', default=2.0) == 2.0


def test_crawl_page():
    "Test page-by-page processing."
    base_url = 'https://httpbun.org'
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(['https://httpbun.org/links/2/2'])
    is_on, known_num, visited_num = spider.crawl_page(0, 'https://httpbun.org')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert sorted(todo) == ['https://httpbun.org/links/2/0', 'https://httpbun.org/links/2/1']
    assert len(known_links) == 3 and visited_num == 1
    # initial page
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(['https://httpbun.org/html'])
    # if LANGID_FLAG is True:
    is_on, known_num, visited_num = spider.crawl_page(0, 'https://httpbun.org', initial=True, lang='de')
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(todo) == 0 and len(known_links) == 1 and visited_num == 1
    ## TODO: find a better page for language tests


def test_focused_crawler():
    "Test the whole focused crawler mechanism."
    spider.URL_STORE = UrlStore()
    todo, known_links = spider.focused_crawler("https://httpbun.org/links/1/1", max_seen_urls=1)
    ## TODO: check this on Github actions:
    # assert sorted(known_links) == ['https://httpbun.org/links/1/0', 'https://httpbun.org/links/1/1']
    # assert sorted(todo) == ['https://httpbun.org/links/1/0']


if __name__ == '__main__':
    test_redirections()
    test_meta_redirections()
    test_process_links()
    test_crawl_logic()
    test_crawl_page()
    test_focused_crawler()
