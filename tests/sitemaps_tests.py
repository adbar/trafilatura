"""
Unit tests for sitemaps parsing.
"""

import logging
import os
import sys

from courlan import get_hostinfo

import trafilatura
from trafilatura import sitemaps
from trafilatura.utils import decode_file, is_similar_domain

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def test_search():
    '''Test search for sitemaps'''
    assert not sitemaps.sitemap_search('12345')
    assert not sitemaps.sitemap_search('12345.xml.gz')
    assert not sitemaps.sitemap_search('https://1.net/sitemap.xml.gz')
    assert not sitemaps.sitemap_search('https://bogusdomain.net/')


def test_extraction():
    '''Test simple link extraction'''
    # link handling
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.handle_link(url)
    assert len(sitemap.sitemap_urls) == 1 and not sitemap.urls

    # same URL
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    sitemap = sitemaps.SitemapObject(baseurl, domain, [url])
    sitemap.current_url = url
    sitemap.handle_link(url)
    assert len(sitemap.sitemap_urls) == 1 and not sitemap.urls

    sitemap = sitemaps.SitemapObject('https://example.org', 'example.org', ['https://example.org/sitemap.xml'])
    sitemap.handle_link('https://mydomain')
    assert len(sitemap.sitemap_urls) == 1 and not sitemap.urls

    sitemap = sitemaps.SitemapObject('https://example.org', 'example.org', ['https://example.org/sitemap.xml'])
    sitemap.handle_link('https://mydomain.wordpress.com/1')
    assert len(sitemap.sitemap_urls) == 1 and sitemap.urls == ['https://mydomain.wordpress.com/1']

    sitemap = sitemaps.SitemapObject('https://programtalk.com', 'programtalk.com', ['https://programtalk.com/sitemap.xml'])
    sitemap.handle_link('http://programtalk.com/java-api-usage-examples/org.apache.xml.security.stax.securityEvent.SecurityEvent')
    assert len(sitemap.sitemap_urls) == 1 and sitemap.urls == ['http://programtalk.com/java-api-usage-examples/org.apache.xml.security.stax.securityEvent.SecurityEvent']

    # similar domain names
    assert not is_similar_domain('kleins-weindepot.de', 'eurosoft.net')
    assert is_similar_domain('kleins-weindepot.de', 'weindepot.info')
    assert is_similar_domain('airport-frankfurt.de', 'frankfurt-airport.com')

    # subdomain vs. domain: de.sitemaps.org / sitemaps.org
    url = 'https://de.sitemaps.org/1'
    sitemap_url = 'https://de.sitemaps.org/sitemap.xml'
    domain, baseurl = get_hostinfo(sitemap_url)
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.handle_link(url)
    assert not sitemap.sitemap_urls and sitemap.urls == [url]

    # diverging domains
    url = 'https://www.software.info/1'
    sitemap_urls = ['https://example.org/sitemap.xml']
    domain, baseurl = get_hostinfo(sitemap_urls[0])
    sitemap = sitemaps.SitemapObject(baseurl, domain, sitemap_urls)
    sitemap.handle_link(url)
    assert len(sitemap.sitemap_urls) == 1 and not sitemap.urls

    # don't take this one?
    #url = 'https://subdomain.sitemaps.org/1'
    #sitemap_url = 'https://www.sitemaps.org/sitemap.xml'
    #domain, baseurl = get_hostinfo(sitemap_url)
    #sitemap.handle_link(url)  #  (url, '0')

    # safety belts
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml.gz', b'\x1f\x8bABC') is False
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml', 'ABC') is False
    assert sitemaps.is_plausible_sitemap('http://test.org/sitemap.xml', '<!DOCTYPE html><html><body/></html>') is False
    assert sitemaps.is_plausible_sitemap('http://test.org/sitemap', '<!DOCTYPE html><html><body/></html>') is False
    # invalid
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.content = '<html>\n</html>'
    sitemap.extract_sitemap_links()
    assert not sitemap.sitemap_urls and not sitemap.urls

    # parsing a file
    url, domain, baseurl = 'http://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'http://www.sitemaps.org'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml')
    with open(filepath, "r", encoding="utf-8") as f:
        teststring = f.read()
    assert sitemaps.is_plausible_sitemap('http://sitemaps.org/sitemap.xml', teststring) is True
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.content = teststring
    sitemap.extract_sitemap_links()
    assert not sitemap.sitemap_urls and len(sitemap.urls) == 84
    # hreflang
    sitemap.urls = []
    sitemap.extract_sitemap_langlinks()
    assert not sitemap.sitemap_urls and not sitemap.urls

    # nested sitemaps
    url, domain, baseurl = 'http://www.example.com/sitemap.xml', 'example.com', 'http://www.example.com'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap2.xml')
    with open(filepath, "r", encoding="utf-8") as f:
        teststring = f.read()
    sitemap = sitemaps.SitemapObject(baseurl, domain, [url])
    sitemap.content = teststring
    sitemap.extract_sitemap_links()
    assert sitemap.sitemap_urls == ['http://www.example.com/sitemap.xml', 'http://www.example.com/sitemap1.xml.gz', 'http://www.example.com/sitemap2.xml.gz'] and not sitemap.urls

    # hreflang
    sitemap = sitemaps.SitemapObject('https://test.org/', 'test.org', [], 'en')
    sitemap.content = '<?xml version="1.0" encoding="UTF-8"?><urlset><url><loc>http://www.test.org/english/page.html</loc></url></urlset>'
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == ([], ['http://www.test.org/english/page.html'])
    filepath = os.path.join(RESOURCES_DIR, 'sitemap-hreflang.xml')
    with open(filepath, "r", encoding="utf-8") as f:
        teststring = f.read()
    sitemap = sitemaps.SitemapObject(baseurl, domain, [], 'de')
    sitemap.content = teststring
    sitemap.extract_sitemap_langlinks()
    assert sitemap.sitemap_urls == ['http://www.example.com/sitemap-de.xml.gz']
    assert len(sitemap.urls) > 0

    # GZ-compressed sitemaps
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml.gz')
    with open(filepath, 'rb') as f:
        teststring = f.read()
    teststring = decode_file(teststring)
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml.gz', teststring) is True
    sitemap = sitemaps.SitemapObject(baseurl, domain, [url])
    sitemap.content = teststring
    sitemap.extract_sitemap_links()
    assert len(sitemap.sitemap_urls) == 1 and len(sitemap.urls) == 84

    # check contents
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml.gz?value=1', teststring) is True

    # TXT links
    content = 'Tralala\nhttps://test.org/1\nhttps://test.org/2'
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap', content) is True
    sitemap = sitemaps.SitemapObject('https://test.org/', 'test.org', [])
    sitemap.content = 'Tralala\nhttps://test.org/1\nhttps://test.org/2'
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == ([], ['https://test.org/1', 'https://test.org/2'])

    # TXT links + language
    sitemap = sitemaps.SitemapObject('https://test.org/', 'test.org', [], 'en')
    sitemap.content = 'Tralala\nhttps://test.org/en/1\nhttps://test.org/en/2\nhttps://test.org/es/3'
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == ([], ['https://test.org/en/1', 'https://test.org/en/2'])


def test_robotstxt():
    '''Check if sitemaps can be found over robots.txt'''
    assert not sitemaps.find_robots_sitemaps('https://http.org')
    baseurl = 'https://httpbun.com'
    assert not sitemaps.find_robots_sitemaps(baseurl)
    assert not sitemaps.extract_robots_sitemaps('# test', baseurl)
    assert not sitemaps.extract_robots_sitemaps('# test'*10000, baseurl)
    assert sitemaps.extract_robots_sitemaps('sitemap: https://example.org/sitemap.xml', baseurl) == ['https://example.org/sitemap.xml']


def test_whole():
    "Test whole process."
    trafilatura.settings.MAX_SITEMAPS_SEEN = 1
    results = sitemaps.sitemap_search("https://www.sitemaps.org", target_lang="de")
    assert len(results) == 8


if __name__ == '__main__':
    test_search()
    test_extraction()
    test_robotstxt()
    test_whole()
