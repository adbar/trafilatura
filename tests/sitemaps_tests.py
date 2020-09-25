"""
Unit tests for sitemaps parsing.
"""

import logging
import os
import sys

from trafilatura import sitemaps

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def test_extraction():
    '''Test simple link extraction'''
    # fixing partial URLs
    assert sitemaps.fix_relative_urls('example.org', 'https://example.org/test.html') == 'https://example.org/test.html'
    assert sitemaps.fix_relative_urls('example.org', '/test.html') == 'http://example.org/test.html'
    # parsing a file
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemapurls, linklist = sitemaps.extract_sitemap_links(teststring, 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org')
    assert sitemapurls == [] and len(linklist) == 84
    # nested sitemaps
    filepath = os.path.join(RESOURCES_DIR, 'sitemap2.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemapurls, linklist = sitemaps.extract_sitemap_links(teststring, 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org')
    assert len(sitemapurls) == 2 and linklist == []
    # invalid
    assert sitemaps.extract_sitemap_links('<html>\n</html>', 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org') == ([], [])


def test_robotstxt():
    '''Check if sitemaps can be found over robots.txt'''
    assert sitemaps.find_robots_sitemaps('https://httpbin.org/') == []
    assert sitemaps.extract_robots_sitemaps('# test') == []
    assert sitemaps.extract_robots_sitemaps('sitemap: https://example.org/sitemap.xml') == ['https://example.org/sitemap.xml']


if __name__ == '__main__':
    test_extraction()
    test_robotstxt()
