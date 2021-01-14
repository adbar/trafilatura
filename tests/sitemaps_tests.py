"""
Unit tests for sitemaps parsing.
"""

import logging
import os
import sys

from trafilatura import sitemaps
from trafilatura.utils import decode_response, fix_relative_urls

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def test_search():
    '''Test search for sitemaps'''
    assert sitemaps.sitemap_search('12345') == []
    assert sitemaps.sitemap_search('12345.xml.gz') == []
    assert sitemaps.sitemap_search('https://1.net/sitemap.xml.gz') == []
    

def test_extraction():
    '''Test simple link extraction'''
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    # fixing partial URLs
    assert fix_relative_urls('https://example.org', 'https://example.org/test.html') == 'https://example.org/test.html'
    assert fix_relative_urls('https://example.org', '/test.html') == 'https://example.org/test.html'
    assert fix_relative_urls('https://example.org', 'test.html') == 'https://example.org/test.html'
    # link handling
    assert sitemaps.handle_link(url, url, domain, baseurl, None) == (url, '0')
    assert sitemaps.handle_link('https://mydomain.wordpress.com/1', 'https://example.org/sitemap.xml', 'example.org', 'https://example.org', None) == ('https://mydomain.wordpress.com/1', 'link')
    # safety belts
    assert sitemaps.check_sitemap('http://example.org/sitemap.xml.gz', b'\x1f\x8bABC') is None
    assert sitemaps.check_sitemap('http://example.org/sitemap.xml', 'ABC') is None
    # parsing a file
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml')
    with open(filepath) as f:
        teststring = f.read()
    contents = sitemaps.check_sitemap('http://example.org/sitemap.xml', teststring)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(contents, url, domain, baseurl, None)
    assert len(sitemapurls) == 0 and len(linklist) == 84
    # hreflang
    assert sitemaps.extract_sitemap_langlinks(teststring, url, domain, baseurl, None) == ([], [])
    # nested sitemaps
    url, domain, baseurl = 'http://www.example.com/sitemap.xml', 'example.com', 'http://www.example.com'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap2.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemapurls, linklist = sitemaps.extract_sitemap_links(teststring, url, domain, baseurl, None)
    assert len(sitemapurls) == 2 and linklist == []
    # invalid
    assert sitemaps.extract_sitemap_links('<html>\n</html>', url, domain, baseurl, None) == ([], [])
    # hreflang
    filepath = os.path.join(RESOURCES_DIR, 'sitemap-hreflang.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemapsurls, linklist = sitemaps.extract_sitemap_langlinks(teststring, url, domain, baseurl, target_lang='de')
    assert sitemapsurls == ['http://www.example.com/sitemap-de.xml.gz']
    assert len(linklist) > 0
    # GZ-compressed sitemaps
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml.gz')
    with open(filepath, 'rb') as f:
        teststring = f.read()
    teststring = decode_response(teststring)
    contents = sitemaps.check_sitemap('http://example.org/sitemap.xml.gz', teststring)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(contents, url, domain, baseurl, None)
    assert len(sitemapurls) == 0 and len(linklist) == 84
    # check contents
    assert sitemaps.check_sitemap('http://example.org/sitemap.xml.gz?value=1', teststring) is not None
    # TXT links
    assert sitemaps.process_sitemap('https://test.org/sitemap', 'test.org', 'https://test.org/', 'Tralala\nhttps://test.org/1\nhttps://test.org/2') == ([], ['https://test.org/1', 'https://test.org/2'])


def test_robotstxt():
    '''Check if sitemaps can be found over robots.txt'''
    assert sitemaps.find_robots_sitemaps('https://http.org/', 'https://http.org') == []
    baseurl = 'https://httpbin.org'
    assert sitemaps.find_robots_sitemaps('https://httpbin.org/', baseurl) == []
    assert sitemaps.extract_robots_sitemaps('# test', baseurl) == []
    assert sitemaps.extract_robots_sitemaps('# test'*10000, baseurl) == []
    assert sitemaps.extract_robots_sitemaps('sitemap: https://example.org/sitemap.xml', baseurl) == ['https://example.org/sitemap.xml']


if __name__ == '__main__':
    test_search()
    test_extraction()
    test_robotstxt()
