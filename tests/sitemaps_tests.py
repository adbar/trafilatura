"""
Unit tests for sitemaps parsing.
"""

import logging
import os
import sys
from unittest.mock import patch

import pytest
from courlan import get_hostinfo

import trafilatura
from trafilatura import sitemaps
from trafilatura.deduplication import is_similar_domain
from trafilatura.utils import decode_file

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

pytestmark = pytest.mark.usefixtures("mock_network")

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, "resources")


def test_search():
    """Test search for sitemaps"""
    assert not sitemaps.sitemap_search("12345")
    assert not sitemaps.sitemap_search("12345.xml.gz")
    assert not sitemaps.sitemap_search("https://1.net/sitemap.xml.gz")
    assert not sitemaps.sitemap_search("https://bogusdomain.net/")


def test_extraction():
    """Test simple link extraction"""
    # link handling
    url, domain, baseurl = "https://www.sitemaps.org/sitemap.xml", "sitemaps.org", "https://www.sitemaps.org"
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.handle_link(url)
    assert len(sitemap.sitemap_urls) == 1
    assert not sitemap.urls

    # same URL
    url, domain, baseurl = "https://www.sitemaps.org/sitemap.xml", "sitemaps.org", "https://www.sitemaps.org"
    sitemap = sitemaps.SitemapObject(baseurl, domain, [url])
    sitemap.current_url = url
    sitemap.handle_link(url)
    assert len(sitemap.sitemap_urls) == 1
    assert not sitemap.urls

    # malformed link
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", ["https://example.org/sitemap.xml"])
    sitemap.handle_link("http://[::1")
    assert len(sitemap.sitemap_urls) == 1
    assert not sitemap.urls

    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", ["https://example.org/sitemap.xml"])
    sitemap.handle_link("https://mydomain")
    assert len(sitemap.sitemap_urls) == 1
    assert not sitemap.urls

    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", ["https://example.org/sitemap.xml"])
    sitemap.handle_link("https://mydomain.wordpress.com/1")
    assert len(sitemap.sitemap_urls) == 1
    assert sitemap.urls == ["https://mydomain.wordpress.com/1"]

    sitemap = sitemaps.SitemapObject("https://programtalk.com", "programtalk.com", ["https://programtalk.com/sitemap.xml"])
    sitemap.handle_link(
        "http://programtalk.com/java-api-usage-examples/org.apache.xml.security.stax.securityEvent.SecurityEvent"
    )
    assert len(sitemap.sitemap_urls) == 1
    assert sitemap.urls == [
        "http://programtalk.com/java-api-usage-examples/org.apache.xml.security.stax.securityEvent.SecurityEvent"
    ]

    # similar domain names
    assert not is_similar_domain("kleins-weindepot.de", "eurosoft.net")
    assert is_similar_domain("kleins-weindepot.de", "weindepot.info")
    assert is_similar_domain("airport-frankfurt.de", "frankfurt-airport.com")

    # subdomain vs. domain: de.sitemaps.org / sitemaps.org
    url = "https://de.sitemaps.org/1"
    sitemap_url = "https://de.sitemaps.org/sitemap.xml"
    domain, baseurl = get_hostinfo(sitemap_url)
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.handle_link(url)
    assert not sitemap.sitemap_urls
    assert sitemap.urls == [url]

    # diverging domains
    url = "https://www.software.info/1"
    sitemap_urls = ["https://example.org/sitemap.xml"]
    domain, baseurl = get_hostinfo(sitemap_urls[0])
    sitemap = sitemaps.SitemapObject(baseurl, domain, sitemap_urls)
    sitemap.handle_link(url)
    assert len(sitemap.sitemap_urls) == 1
    assert not sitemap.urls

    # don't take this one?
    # url = 'https://subdomain.sitemaps.org/1'
    # sitemap_url = 'https://www.sitemaps.org/sitemap.xml'
    # domain, baseurl = get_hostinfo(sitemap_url)
    # sitemap.handle_link(url)  #  (url, '0')

    # safety belts
    assert sitemaps.is_plausible_sitemap("http://example.org/sitemap.xml.gz", None) is False
    assert sitemaps.is_plausible_sitemap("http://example.org/sitemap.xml.gz", b"\x1f\x8bABC") is False
    assert sitemaps.is_plausible_sitemap("http://example.org/sitemap.xml", "ABC") is False
    assert sitemaps.is_plausible_sitemap("http://test.org/sitemap.xml", "<!DOCTYPE html><html><body/></html>") is False
    assert sitemaps.is_plausible_sitemap("http://test.org/sitemap", "<!DOCTYPE html><html><body/></html>") is False
    # invalid
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.content = "<html>\n</html>"
    sitemap.extract_sitemap_links()
    assert not sitemap.sitemap_urls
    assert not sitemap.urls

    # parsing a file
    url, domain, baseurl = "http://www.sitemaps.org/sitemap.xml", "sitemaps.org", "http://www.sitemaps.org"
    filepath = os.path.join(RESOURCES_DIR, "sitemap.xml")
    with open(filepath, encoding="utf-8") as f:
        teststring = f.read()
    assert sitemaps.is_plausible_sitemap("http://sitemaps.org/sitemap.xml", teststring) is True
    sitemap = sitemaps.SitemapObject(baseurl, domain, [])
    sitemap.content = teststring
    sitemap.extract_sitemap_links()
    assert not sitemap.sitemap_urls
    assert len(sitemap.urls) == 84
    # hreflang
    sitemap.urls = []
    sitemap.extract_sitemap_langlinks()
    assert not sitemap.sitemap_urls
    assert not sitemap.urls

    # nested sitemaps
    url, domain, baseurl = "http://www.example.com/sitemap.xml", "example.com", "http://www.example.com"
    filepath = os.path.join(RESOURCES_DIR, "sitemap2.xml")
    with open(filepath, encoding="utf-8") as f:
        teststring = f.read()
    sitemap = sitemaps.SitemapObject(baseurl, domain, [url])
    sitemap.content = teststring
    sitemap.extract_sitemap_links()
    assert sitemap.sitemap_urls == [
        "http://www.example.com/sitemap.xml",
        "http://www.example.com/sitemap1.xml.gz",
        "http://www.example.com/sitemap2.xml.gz",
    ]
    assert not sitemap.urls

    # hreflang
    sitemap = sitemaps.SitemapObject("https://test.org/", "test.org", [], "en")
    sitemap.content = (
        '<?xml version="1.0" encoding="UTF-8"?><urlset><url><loc>http://www.test.org/english/page.html</loc></url></urlset>'
    )
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == ([], ["http://www.test.org/english/page.html"])
    filepath = os.path.join(RESOURCES_DIR, "sitemap-hreflang.xml")
    with open(filepath, encoding="utf-8") as f:
        teststring = f.read()
    sitemap = sitemaps.SitemapObject(baseurl, domain, [], "de")
    sitemap.content = teststring
    sitemap.extract_sitemap_langlinks()
    assert sitemap.sitemap_urls == ["http://www.example.com/sitemap-de.xml.gz"]
    assert len(sitemap.urls) > 0

    # target_lang is escaped: a regex-hostile value stays inert
    sitemap = sitemaps.SitemapObject(baseurl, domain, [], "de)|(.")
    sitemap.content = teststring
    sitemap.extract_sitemap_langlinks()
    assert not sitemap.sitemap_urls
    assert not sitemap.urls

    # GZ-compressed sitemaps
    url, domain, baseurl = "https://www.sitemaps.org/sitemap.xml", "sitemaps.org", "https://www.sitemaps.org"
    filepath = os.path.join(RESOURCES_DIR, "sitemap.xml.gz")
    with open(filepath, "rb") as f:
        teststring = f.read()
    teststring = decode_file(teststring)
    assert sitemaps.is_plausible_sitemap("http://example.org/sitemap.xml.gz", teststring) is True
    sitemap = sitemaps.SitemapObject(baseurl, domain, [url])
    sitemap.content = teststring
    sitemap.extract_sitemap_links()
    assert len(sitemap.sitemap_urls) == 1
    assert len(sitemap.urls) == 84

    # check contents
    assert sitemaps.is_plausible_sitemap("http://example.org/sitemap.xml.gz?value=1", teststring) is True

    # TXT links
    content = "Tralala\nhttps://test.org/1\nhttps://test.org/2"
    assert sitemaps.is_plausible_sitemap("http://example.org/sitemap", content) is True
    sitemap = sitemaps.SitemapObject("https://test.org/", "test.org", [])
    sitemap.content = "Tralala\nhttps://test.org/1\nhttps://test.org/2"
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == ([], ["https://test.org/1", "https://test.org/2"])

    # TXT links + language
    sitemap = sitemaps.SitemapObject("https://test.org/", "test.org", [], "en")
    sitemap.content = "Tralala\nhttps://test.org/en/1\nhttps://test.org/en/2\nhttps://test.org/es/3"
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == ([], ["https://test.org/en/1", "https://test.org/en/2"])

    # XML sitemap with matching hreflang links: return after the langlink pass
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", [], "de")
    sitemap.current_url = "https://example.org/sitemap.xml"
    sitemap.content = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        "<url><loc>https://example.org/page</loc>"
        '<xhtml:link rel="alternate" hreflang="de" href="https://example.org/de/page"/>'
        "</url></urlset>"
    )
    sitemap.process()
    assert sitemap.urls == ["https://example.org/de/page"]


def test_robotstxt():
    """Check if sitemaps can be found over robots.txt"""
    assert not sitemaps.find_robots_sitemaps("https://http.org")
    baseurl = "https://httpbun.com"
    assert not sitemaps.find_robots_sitemaps(baseurl)
    assert not sitemaps.extract_robots_sitemaps("# test", baseurl)
    assert not sitemaps.extract_robots_sitemaps("# test" * 10000, baseurl)
    assert sitemaps.extract_robots_sitemaps("sitemap: https://example.org/sitemap.xml", baseurl) == [
        "https://example.org/sitemap.xml"
    ]
    assert sitemaps.extract_robots_sitemaps("sitemap: http://[::1\nsitemap: /sitemap.xml", baseurl) == [
        "https://httpbun.com/sitemap.xml"
    ]


def test_sitemap_index_with_target_lang():
    "Regression: with target_lang, sitemaps processed while others are queued must keep their links."
    pages = {
        "https://example.org/robots.txt": "Sitemap: https://example.org/sitemap_index.xml\n",
        "https://example.org/sitemap_index.xml": (
            '<?xml version="1.0" encoding="UTF-8"?><sitemapindex>'
            "<sitemap><loc>https://example.org/sub1.xml</loc></sitemap>"
            "<sitemap><loc>https://example.org/sub2.xml</loc></sitemap>"
            "</sitemapindex>"
        ),
        "https://example.org/sub1.xml": (
            '<?xml version="1.0" encoding="UTF-8"?><urlset>'
            "<url><loc>https://example.org/de/a1.html</loc></url>"
            "<url><loc>https://example.org/de/a2.html</loc></url></urlset>"
        ),
        "https://example.org/sub2.xml": (
            '<?xml version="1.0" encoding="UTF-8"?><urlset>'
            "<url><loc>https://example.org/de/b1.html</loc></url>"
            "<url><loc>https://example.org/de/b2.html</loc></url></urlset>"
        ),
    }
    expected = [
        "https://example.org/de/a1.html",
        "https://example.org/de/a2.html",
        "https://example.org/de/b1.html",
        "https://example.org/de/b2.html",
    ]
    with (
        patch.object(sitemaps, "fetch_url", lambda url, *a, **kw: pages.get(url)),
        patch.object(sitemaps, "is_live_page", lambda u, c: True),
        patch.object(sitemaps, "sleep", lambda s: None),
    ):
        assert sorted(sitemaps.sitemap_search("https://example.org")) == expected
        assert sorted(sitemaps.sitemap_search("https://example.org", target_lang="de")) == expected


def test_lang_filter_before_cleaning():
    "Language-root URLs with trailing slashes must be filtered even if cleaning strips the slash."
    sitemap = sitemaps.SitemapObject("https://www.sitemaps.org", "sitemaps.org", [], target_lang="de")
    sitemap.handle_link("https://www.sitemaps.org/da/")
    sitemap.handle_link("https://www.sitemaps.org/da/faq.html")
    assert not sitemap.urls
    sitemap.handle_link("https://www.sitemaps.org/de/faq.html")
    assert sitemap.urls == ["https://www.sitemaps.org/de/faq.html"]


def test_guess_order():
    "Without robots.txt hints, the most common sitemap location must be tried first."
    fetched = []

    def fake_fetch(url, *a, **kw):
        fetched.append(url)

    with (
        patch.object(sitemaps, "fetch_url", fake_fetch),
        patch.object(sitemaps, "is_live_page", lambda u, c: True),
        patch.object(sitemaps, "sleep", lambda s: None),
    ):
        sitemaps.sitemap_search("https://example.org")
    assert fetched[0] == "https://example.org/robots.txt"
    assert fetched[1] == "https://example.org/sitemap.xml"


def test_whole():
    "Test whole process."
    results = sitemaps.sitemap_search("https://www.sitemaps.org", target_lang="de", max_sitemaps=1)
    assert len(results) == 8

    trafilatura.settings.MAX_SITEMAPS_SEEN = 1
    results = sitemaps.sitemap_search("https://www.sitemaps.org", target_lang="de")
    assert len(results) == 8


@pytest.mark.parametrize("prefix", ["", "sm:", "site-map:"])
@pytest.mark.parametrize("declaration", ["", '<?xml version="1.0" encoding="UTF-8"?>'])
@pytest.mark.parametrize("index", [False, True])
def test_sitemap_namespaces(prefix, declaration, index):
    """Namespace prefixes do not change page or nested sitemap discovery."""
    root, child = ("sitemapindex", "sitemap") if index else ("urlset", "url")
    namespace = f'xmlns{":" + prefix[:-1] if prefix else ""}="http://www.sitemaps.org/schemas/sitemap/0.9"'
    url = "https://example.org/nested.xml" if index else "https://example.org/page"
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", [])
    sitemap.current_url = "https://example.org/sitemap.xml"
    sitemap.content = (
        f"{declaration}<{prefix}{root} {namespace}>"
        f"<{prefix}{child}><{prefix}loc><![CDATA[{url}]]></{prefix}loc></{prefix}{child}>"
        f"</{prefix}{root}>"
    )
    sitemap.process()
    assert (sitemap.sitemap_urls, sitemap.urls) == (([url], []) if index else ([], [url]))


def test_sitemap_namespace_scope():
    """Ignore extension locations even when a prefix is rebound locally."""
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", [])
    sitemap.current_url = "https://example.org/sitemap.xml"
    sitemap.content = (
        '<s:urlset xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="urn:image">'
        "<s:url><s:loc>https://example.org/page</s:loc>"
        "<image:loc>https://example.org/image</image:loc>"
        '<s:loc xmlns:s="urn:other">https://example.org/other</s:loc>'
        "</s:url></s:urlset>"
    )
    sitemap.process()
    assert sitemap.urls == ["https://example.org/page"]


@pytest.mark.parametrize("location", ["&external;", "https://example.org/&external;", "https://example.org/<nested/>"])
def test_sitemap_locations_do_not_expand_entities(location):
    """Location extraction does not resolve entities or concatenate child markup."""
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", [])
    sitemap.content = (
        '<!DOCTYPE urlset [<!ENTITY external SYSTEM "file:///not-a-sitemap-resource">]>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{location}</loc></url></urlset>"
    )
    sitemap.extract_sitemap_links()
    assert not sitemap.urls


def test_sitemap_namespace_link_limit(monkeypatch):
    """Namespaced extraction keeps the existing maximum-location bound."""
    monkeypatch.setattr(sitemaps, "MAX_LINKS", 1)
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", [])
    sitemap.content = (
        '<s:urlset xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">'
        "<s:url><s:loc>https://example.org/first?a=1&amp;b=2</s:loc></s:url>"
        "<s:url><s:loc>https://example.org/second</s:loc></s:url></s:urlset>"
    )
    sitemap.extract_sitemap_links()
    assert sitemap.urls == ["https://example.org/first?a=1&b=2"]


@pytest.mark.parametrize("content", ["", "not an XML document"])
def test_sitemap_xml_without_a_root_is_ignored(content):
    """Malformed input cannot yield a sitemap location."""
    sitemap = sitemaps.SitemapObject("https://example.org", "example.org", [])
    sitemap.content = content
    sitemap.extract_sitemap_links()
    assert sitemap.urls == []
    assert sitemap.sitemap_urls == []
