"""
Unit tests for sitemaps parsing.
"""

import logging
import os
import sys

from trafilatura import sitemaps
from trafilatura.utils import fix_relative_urls

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def test_extraction():
    '''Test simple link extraction'''
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    # fixing partial URLs
    assert fix_relative_urls('https://example.org', 'https://example.org/test.html') == 'https://example.org/test.html'
    assert fix_relative_urls('https://example.org', '/test.html') == 'https://example.org/test.html'
    # link handling
    # assert sitemaps.handle_link(url, domain, url) == (url, '0')
    # parsing a file
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml')
    with open(filepath) as f:
        teststring = f.read()
    contents = sitemaps.check_sitemap('http://example.org/sitemap.xml', teststring)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(contents, url, domain, baseurl)
    assert len(sitemapurls) == 0 and len(linklist) == 84
    # hreflang
    assert sitemaps.extract_sitemap_langlinks(teststring, url, domain, baseurl) == ([], [])
    # nested sitemaps
    filepath = os.path.join(RESOURCES_DIR, 'sitemap2.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemapurls, linklist = sitemaps.extract_sitemap_links(teststring, url, domain, baseurl)
    assert len(sitemapurls) == 2 and linklist == []
    # invalid
    assert sitemaps.extract_sitemap_links('<html>\n</html>', url, domain, baseurl) == ([], [])
    # hreflang
    filepath = os.path.join(RESOURCES_DIR, 'sitemap-hreflang.xml')
    with open(filepath) as f:
        teststring = f.read()
    _, linklist = sitemaps.extract_sitemap_langlinks(teststring, url, domain, baseurl, target_lang='de')
    assert len(linklist) > 0
    # GZ-compressed sitemaps
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml.gz')
    with open(filepath, 'rb') as f:
        teststring = f.read()
    contents = sitemaps.check_sitemap('http://example.org/sitemap.xml.gz', teststring)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(contents, url, domain, baseurl)
    assert len(sitemapurls) == 0 and len(linklist) == 84
    # check contents
    assert sitemaps.check_sitemap('http://example.org/sitemap.xml', teststring) is None
    assert sitemaps.check_sitemap('http://example.org/sitemap.xml.gz?value=1', teststring) is not None


def test_robotstxt():
    '''Check if sitemaps can be found over robots.txt'''
    baseurl = 'https://httpbin.org'
    assert sitemaps.find_robots_sitemaps('https://httpbin.org/', baseurl) == []
    assert sitemaps.extract_robots_sitemaps('# test', baseurl) == []
    assert sitemaps.extract_robots_sitemaps('sitemap: https://example.org/sitemap.xml', baseurl) == ['https://example.org/sitemap.xml']


if __name__ == '__main__':
    test_extraction()
    test_robotstxt()
