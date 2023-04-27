"""
Unit tests for sitemaps parsing.
"""

import logging
import os
import sys

from courlan import get_hostinfo
from trafilatura import sitemaps
from trafilatura.utils import decode_response, is_similar_domain

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def test_search():
    '''Test search for sitemaps'''
    assert sitemaps.sitemap_search('12345') == []
    assert sitemaps.sitemap_search('12345.xml.gz') == []
    assert sitemaps.sitemap_search('https://1.net/sitemap.xml.gz') == []
    assert sitemaps.sitemap_search('https://bogusdomain.net/') == []


def test_extraction():
    '''Test simple link extraction'''
    # link handling
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    sitemap = sitemaps.SitemapObject(baseurl, "", domain, url)
    assert sitemaps.handle_link(url, sitemap) == (url, '0')

    sitemap = sitemaps.SitemapObject('https://example.org', "", 'example.org', 'https://example.org/sitemap.xml')
    assert sitemaps.handle_link('https://mydomain', sitemap) == ('https://mydomain', '0')

    sitemap = sitemaps.SitemapObject('https://example.org', "", 'example.org', 'https://example.org/sitemap.xml')
    assert sitemaps.handle_link('https://mydomain.wordpress.com/1', sitemap) == ('https://mydomain.wordpress.com/1', 'link')

    sitemap = sitemaps.SitemapObject('https://programtalk.com', "", 'programtalk.com', 'https://programtalk.com/sitemap.xml')
    assert sitemaps.handle_link('http://programtalk.com/java-api-usage-examples/org.apache.xml.security.stax.securityEvent.SecurityEvent', sitemap) == ('http://programtalk.com/java-api-usage-examples/org.apache.xml.security.stax.securityEvent.SecurityEvent', 'link')

    # similar domain names
    assert not is_similar_domain('kleins-weindepot.de', 'eurosoft.net')
    assert is_similar_domain('kleins-weindepot.de', 'weindepot.info')
    assert is_similar_domain('airport-frankfurt.de', 'frankfurt-airport.com')

    # subdomain vs. domain: de.sitemaps.org / sitemaps.org
    url = 'https://de.sitemaps.org/1'
    sitemap_url = 'https://de.sitemaps.org/sitemap.xml'
    domain, baseurl = get_hostinfo(sitemap_url)
    sitemap = sitemaps.SitemapObject(baseurl, "", domain, sitemap_url)
    assert sitemaps.handle_link(url, sitemap) == (url, 'link')

    # diverging domains
    url = 'https://www.software.info/1'
    sitemap_url = 'https://example.org/sitemap.xml'
    domain, baseurl = get_hostinfo(sitemap_url)
    sitemap = sitemaps.SitemapObject(baseurl, "", domain, sitemap_url)
    assert sitemaps.handle_link(url, sitemap) == (url, '0')

    # don't take this one?
    #url = 'https://subdomain.sitemaps.org/1'
    #sitemap_url = 'https://www.sitemaps.org/sitemap.xml'
    #domain, baseurl = get_hostinfo(sitemap_url)
    #assert sitemaps.handle_link(url, sitemap_url, domain, baseurl, None) == (url, '0')

    # safety belts
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml.gz', b'\x1f\x8bABC') is False
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml', 'ABC') is False
    assert sitemaps.is_plausible_sitemap('http://test.org/sitemap.xml', '<!DOCTYPE html><html><body/></html>') is False
    assert sitemaps.is_plausible_sitemap('http://test.org/sitemap', '<!DOCTYPE html><html><body/></html>') is False
    # invalid
    sitemap = sitemaps.SitemapObject(baseurl, domain, '<html>\n</html>', url)
    assert sitemaps.extract_sitemap_links(sitemap) == ([], [])

    # parsing a file
    url, domain, baseurl = 'http://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'http://www.sitemaps.org'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml')
    with open(filepath) as f:
        teststring = f.read()
    assert sitemaps.is_plausible_sitemap('http://sitemaps.org/sitemap.xml', teststring) is True
    sitemap = sitemaps.SitemapObject(baseurl, teststring, domain, sitemap_url)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(sitemap)
    assert len(sitemapurls) == 0 and len(linklist) == 84
    # hreflang
    assert sitemaps.extract_sitemap_langlinks(sitemap) == ([], [])

    # nested sitemaps
    url, domain, baseurl = 'http://www.example.com/sitemap.xml', 'example.com', 'http://www.example.com'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap2.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemap = sitemaps.SitemapObject(baseurl, teststring, domain, url)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(sitemap)
    assert sitemapurls == ['http://www.example.com/sitemap1.xml.gz', 'http://www.example.com/sitemap2.xml.gz'] and linklist == []

    # hreflang
    sitemap = sitemaps.SitemapObject('https://test.org/', '<?xml version="1.0" encoding="UTF-8"?><urlset><url><loc>http://www.test.org/english/page.html</loc></url></urlset>', 'test.org', 'https://test.org/sitemap', target_lang='en')
    assert sitemaps.process_sitemap(sitemap) == ([], ['http://www.test.org/english/page.html'])
    filepath = os.path.join(RESOURCES_DIR, 'sitemap-hreflang.xml')
    with open(filepath) as f:
        teststring = f.read()
    sitemap = sitemaps.SitemapObject(baseurl, teststring, domain, url, target_lang='de')
    sitemapsurls, linklist = sitemaps.extract_sitemap_langlinks(sitemap)
    assert sitemapsurls == ['http://www.example.com/sitemap-de.xml.gz']
    assert len(linklist) > 0

    # GZ-compressed sitemaps
    url, domain, baseurl = 'https://www.sitemaps.org/sitemap.xml', 'sitemaps.org', 'https://www.sitemaps.org'
    filepath = os.path.join(RESOURCES_DIR, 'sitemap.xml.gz')
    with open(filepath, 'rb') as f:
        teststring = f.read()
    teststring = decode_response(teststring)
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml.gz', teststring) is True
    sitemap = sitemaps.SitemapObject(baseurl, teststring, domain, url)
    sitemapurls, linklist = sitemaps.extract_sitemap_links(sitemap)
    assert len(sitemapurls) == 0 and len(linklist) == 84

    # check contents
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap.xml.gz?value=1', teststring) is True

    # TXT links
    content = 'Tralala\nhttps://test.org/1\nhttps://test.org/2'
    assert sitemaps.is_plausible_sitemap('http://example.org/sitemap', content) is True
    sitemap = sitemaps.SitemapObject('https://test.org/', 'Tralala\nhttps://test.org/1\nhttps://test.org/2', 'test.org', 'https://test.org/sitemap')
    assert sitemaps.process_sitemap(sitemap) == ([], ['https://test.org/1', 'https://test.org/2'])

    # TXT links + language
    sitemap = sitemaps.SitemapObject('https://test.org/', 'Tralala\nhttps://test.org/en/1\nhttps://test.org/en/2\nhttps://test.org/es/3', 'test.org', 'https://test.org/sitemap', target_lang='en')
    assert sitemaps.process_sitemap(sitemap) == ([], ['https://test.org/en/1', 'https://test.org/en/2'])


def test_robotstxt():
    '''Check if sitemaps can be found over robots.txt'''
    assert sitemaps.find_robots_sitemaps('https://http.org') == []
    baseurl = 'https://httpbun.org'
    assert sitemaps.find_robots_sitemaps(baseurl) == []
    assert sitemaps.extract_robots_sitemaps('# test', baseurl) == []
    assert sitemaps.extract_robots_sitemaps('# test'*10000, baseurl) == []
    assert sitemaps.extract_robots_sitemaps('sitemap: https://example.org/sitemap.xml', baseurl) == ['https://example.org/sitemap.xml']


if __name__ == '__main__':
    test_search()
    test_extraction()
    test_robotstxt()
