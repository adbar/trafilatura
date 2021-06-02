# pylint:disable-msg=W1401
"""
Unit tests for the spidering part of the trafilatura library.
"""

import logging
import sys

from collections import deque

from trafilatura import spider
from trafilatura.settings import DEFAULT_CONFIG

# language detection
try:
    import cld3
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_redirections():
    "Test redirection detection."
    _, _, baseurl = spider.probe_alternative_homepage('1234')
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
    todo, known_links = deque(), set()
    base_url = 'https://example.org'
    htmlstring = '<html><body><a href="https://example.org/page1"/><a href="https://example.org/page1/"/><a href="https://test.org/page1"/></body></html>'
    # 1 internal link in total
    todo, known_links = spider.process_links(htmlstring, base_url, known_links, todo)
    assert len(todo) == 1 and len(known_links) == 1
    # same with URL already seen + todo is None
    todo = None
    todo, known_links = spider.process_links(htmlstring, base_url, known_links, todo)
    assert len(todo) == 0 and len(known_links) == 1
    # test navigation links
    htmlstring = '<html><body><a href="https://example.org/tag/number1"/><a href="https://example.org/page2"/></body></html>'
    todo, known_links = spider.process_links(htmlstring, base_url, known_links, todo)
    assert todo[0] == 'https://example.org/tag/number1' and len(known_links) == 3
    # test language
    htmlstring = '<html><body><a href="https://example.org/en/page1"/></body></html>'
    todo, known_links = spider.process_links(htmlstring, base_url, known_links, todo, language='en')
    assert 'https://example.org/en/page1' in todo and len(known_links) == 4
    htmlstring = '<html><body><a href="https://example.org/en/page2"/></body></html>'
    todo, known_links = spider.process_links(htmlstring, base_url, known_links, todo, language='de')
    # wrong language, doesn't get stored anywhere (?)
    assert 'https://example.org/en/page2' not in todo and len(known_links) == 4
    # test queue evaluation
    todo = deque()
    assert spider.is_still_navigation(todo) is False
    todo.append('https://example.org/en/page1')
    assert spider.is_still_navigation(todo) is False
    todo.append('https://example.org/tag/1')
    assert spider.is_still_navigation(todo) is True


def test_crawl_page():
    "Test page-by-page processing."
    todo, known_links = deque(['https://httpbin.org/links/2/2']), set()
    base_url, i = 'https://httpbin.org', 0
    todo, known_urls, i, _ = spider.crawl_page(i, base_url, todo, known_links)
    assert sorted(todo) == ['https://httpbin.org/links/2/0', 'https://httpbin.org/links/2/1']
    assert len(known_urls) == 3 and i == 1
    # initial page
    todo, known_links, i, _ = spider.crawl_page(0, 'https://httpbin.org', deque(['https://httpbin.org/html']),  set(), initial=True)
    assert len(todo) == 0 and len(known_links) == 1 and i == 1
    # test language detection
    if LANGID_FLAG is True:
        todo, known_links = deque(['https://httpbin.org/html']), set()
        ## TODO: find a better page
        todo, known_links, i, _ = spider.crawl_page(i, 'https://httpbin.org', todo, known_links, lang='de')
        assert len(todo) == 0 and len(known_links) == 1 and i == 2


def test_crawl_logic():
    "Test functions related to crawling sequence and consistency."
    todo, known_links, base_url, i, rules = spider.init_crawl('https://httpbin.org/html', None, None)
    assert todo == deque([]) and known_links == {'https://httpbin.org/html'} and base_url == 'https://httpbin.org' and i == 1
    known_links = 'https://test.org'
    assert spider.is_known_link('https://test.org', known_links) is True
    assert spider.is_known_link('http://test.org', known_links) is True
    assert spider.is_known_link('http://test.org/', known_links) is True
    assert spider.is_known_link('https://test.org/', known_links) is True
    # delay between requests
    assert spider.get_crawl_delay(rules, None) == 0
    assert spider.get_crawl_delay(rules, DEFAULT_CONFIG) == 2.0


if __name__ == '__main__':
    test_redirections()
    test_meta_redirections()
    test_process_links()
    test_crawl_page()
    test_crawl_logic()
