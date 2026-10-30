# pylint:disable-msg=W1401
"""
Unit tests for the spidering part of the trafilatura library.
"""

import logging
import sys
from collections import deque
from unittest.mock import patch
from urllib.robotparser import RobotFileParser

import pytest
from courlan import UrlStore

from trafilatura import spider  # for global variables
from trafilatura.utils import Response

# from trafilatura.utils import LANGID_FLAG


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

pytestmark = pytest.mark.usefixtures("mock_network")


def test_redirections():
    "Test redirection detection."
    _, _, baseurl = spider.probe_alternative_homepage("xyz")
    assert baseurl is None
    _, _, baseurl = spider.probe_alternative_homepage("https://httpbun.com/redirect-to?url=https://example.org")
    assert baseurl == "https://example.org"
    # meta-refresh to an unreachable target -> failed redirect -> all None
    assert spider.probe_alternative_homepage("https://example.com/refresh-home") == (None, None, None)


def test_meta_redirections():
    "Test redirection detection using meta tag."

    tests = [
        # empty
        ('"refresh"', "https://httpbun.com/", "https://httpbun.com/"),
        ("<html></html>", "https://httpbun.com/", "https://httpbun.com/"),
        # unusable
        ("<html>REDIRECT!</html>", "https://httpbun.com/", "https://httpbun.com/"),
        # malformed
        (
            '<html><meta http-equiv="refresh" content="3600\n&lt;meta http-equiv=" content-type=""></html>',
            "https://httpbun.com/",
            "https://httpbun.com/",
        ),
        # wrong URL
        (
            '<html><meta http-equiv="refresh" content="0; url=1234"/></html>',
            "https://httpbun.com/",
            None,
        ),
        # normal
        (
            '<html><meta http-equiv="refresh" content="0; url=https://httpbun.com/html"/></html>',
            "http://test.org/",
            "https://httpbun.com/html",
        ),
        # no "url=" prefix
        (
            '<html><meta http-equiv="refresh" content="0; https://httpbun.com/html"/></html>',
            "http://test.org/",
            "https://httpbun.com/html",
        ),
        # relative URLs, resolved against the page
        (
            '<html><meta http-equiv="refresh" content="0; url=/html"/></html>',
            "https://httpbun.com/status/404",
            "https://httpbun.com/html",
        ),
        (
            '<html><meta http-equiv="refresh" content="0; url=200"/></html>',
            "https://httpbun.com/status/404",
            "https://httpbun.com/status/200",
        ),
    ]

    for htmlstring, homepage, expected_homepage in tests:
        htmlstring2, homepage2 = spider.refresh_detection(htmlstring, homepage)
        assert homepage2 == expected_homepage
        if expected_homepage:
            if expected_homepage == homepage:
                assert htmlstring2 == htmlstring
            else:
                assert htmlstring2 != htmlstring


def test_process_links():
    "Test link extraction procedures."
    base_url = "https://example.org"
    params = spider.CrawlParameters(base_url)
    htmlstring = '<html><body><a href="https://example.org/page1"/><a href="https://example.org/page1/"/><a href="https://test.org/page1"/></body></html>'

    # 1 internal link in total
    spider.process_links(htmlstring, params)
    assert len(spider.URL_STORE.find_known_urls(base_url)) == 1
    assert len(spider.URL_STORE.find_unvisited_urls(base_url)) == 1

    # same with content already seen
    spider.process_links(htmlstring, params)
    assert len(spider.URL_STORE.find_unvisited_urls(base_url)) == 1
    assert len(spider.URL_STORE.find_known_urls(base_url)) == 1

    # test navigation links
    url1 = "https://example.org/tag/number1"
    url2 = "https://example.org/page2"
    htmlstring = f'<html><body><a href="{url1}"/><a href="{url2}"/></body></html>'
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(known_links) == 3
    assert len(todo) == 3
    assert todo[0] == url1

    # malformed relative link
    spider.process_links('<html><body><a href="//[::1"/></body></html>', params)
    assert len(spider.URL_STORE.find_known_urls(base_url)) == 3

    # test cleaning and language
    url = "https://example.org/en/page1/?"
    target = "https://example.org/en/page1/"
    htmlstring = f'<html><body><p>This is an English page.</p><a href="{url}"/></body></html>'
    params = spider.CrawlParameters(base_url, lang="en")
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(known_links) == 4
    assert len(todo) == 4
    assert target in todo

    # test rejection of URLs out of scope
    url = "https://example.org/section2/page2"
    htmlstring = f'<html><body><a href="{url}"/></body></html>'
    params = spider.CrawlParameters("https://example.org/section1/")
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert url not in todo
    assert len(known_links) == 4

    # wrong language
    url = "https://example.org/en/page2"
    htmlstring = f'<html><body><a href="{url}"/></body></html>'
    params = spider.CrawlParameters(base_url, lang="de")
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert url not in todo
    assert len(known_links) == 4

    # invalid links
    params = spider.CrawlParameters(base_url)
    htmlstring = '<html><body><a href="#anchor"/><a href="mailto:user@example.org"/><a href="tel:1234567890"/></body></html>'
    spider.process_links(htmlstring, params)
    assert len(known_links) == 4
    assert len(todo) == 4

    # not crawlable
    htmlstring = '<html><body><a href="https://example.org/login"/></body></html>'
    spider.process_links(htmlstring, params)
    assert len(known_links) == 4
    assert len(todo) == 4

    # test queue evaluation
    todo = deque()
    assert spider.is_still_navigation(todo) is False
    todo.append("https://example.org/en/page1")
    assert spider.is_still_navigation(todo) is False
    todo.append("https://example.org/tag/1")
    assert spider.is_still_navigation(todo) is True


def test_crawl_logic():
    "Test functions related to crawling sequence and consistency."
    url = "https://httpbun.com/html"
    spider.URL_STORE = UrlStore(compressed=False, strict=False)

    # erroneous webpage
    with pytest.raises(ValueError):
        params = spider.CrawlParameters("xyz")
    assert len(spider.URL_STORE.urldict) == 0

    # empty request
    params = spider.CrawlParameters("https://example.org")
    spider.process_response(None, params)
    assert len(spider.URL_STORE.urldict) == 0
    assert params.start == params.base == params.ref == "https://example.org"
    assert params.i == 0
    assert params.known_num == 0
    assert params.is_on
    assert params.lang is None
    assert params.rules is None

    # already visited
    params = spider.init_crawl(url, known=[url])
    assert params.base == "https://httpbun.com"
    assert params.i == 0
    assert params.known_num == 1
    assert not params.is_on
    assert not spider.URL_STORE.find_unvisited_urls(params.base)
    assert spider.URL_STORE.find_known_urls(params.base) == ["https://httpbun.com/html"]

    # normal webpage
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    params = spider.init_crawl(url)
    assert not spider.URL_STORE.find_unvisited_urls(params.base)
    assert [url] == spider.URL_STORE.find_known_urls(params.base)
    assert params.base == "https://httpbun.com"
    assert params.i == 1
    assert not params.is_on

    # delay between requests
    assert spider.URL_STORE.get_crawl_delay("https://httpbun.com") == 5
    assert spider.URL_STORE.get_crawl_delay("https://httpbun.com", default=2.0) == 2.0

    # existing todo
    params = spider.init_crawl(url, todo=[url, "http://irrelevant.com"])
    assert not spider.URL_STORE.find_unvisited_urls(params.base)
    assert params.base == "https://httpbun.com"
    assert params.i == 0
    assert not params.is_on

    # new todo
    params = spider.init_crawl(url, todo=["https://httpbun.com/links/1/1"])
    assert params.base == "https://httpbun.com"
    assert spider.URL_STORE.find_unvisited_urls(params.base) == ["https://httpbun.com/links/1/1"]
    assert params.i == 0
    assert params.is_on
    assert params.known_num == 2


def test_crawl_page():
    "Test page-by-page processing."
    base_url = "https://httpbun.com"

    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/links/2/2"])
    params = spider.CrawlParameters(base_url)
    params = spider.crawl_page(params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert sorted(todo) == [
        "https://httpbun.com/links/2/0",
        "https://httpbun.com/links/2/1",
    ]
    assert params.i == 1
    assert params.is_on
    assert params.known_num == 3

    # prune path
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/links/2/2"])
    params = spider.CrawlParameters(base_url, prune_xpath="//a")
    params = spider.crawl_page(params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)

    assert len(todo) == 0
    assert params.i == 1

    # prune path with initial page
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/links/2/2"])
    params = spider.CrawlParameters(base_url, prune_xpath="//a")
    params = spider.crawl_page(params, initial=True)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)

    assert len(todo) == 0
    assert params.i == 1

    # initial page
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/html"])
    params = spider.CrawlParameters(base_url, lang="de")
    # if LANGID_FLAG is True:
    params = spider.crawl_page(params, initial=True)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(todo) == 0
    assert len(known_links) == 1
    assert params.i == 1
    ## TODO: find a better page for language tests


def test_error_pages():
    "Links found on responses other than 200 must not reach the crawl frontier."
    spider.URL_STORE = UrlStore()
    base_url = "https://error-pages.org"
    html = b'<html><body><a href="/from-error">x</a></body></html>'
    params = spider.CrawlParameters(base_url)

    for status in (404, 500):
        spider.process_response(Response(html, status, f"{base_url}/missing"), params)
    # the URL of the error page is recorded, its links are not queued
    assert spider.URL_STORE.find_known_urls(base_url) == [f"{base_url}/missing"]
    assert spider.URL_STORE.find_unvisited_urls(base_url) == []

    spider.process_response(Response(html, 200, f"{base_url}/found"), params)
    assert spider.URL_STORE.find_unvisited_urls(base_url) == [f"{base_url}/from-error"]

    # a homepage with an error status counts as unreachable
    with patch.object(spider, "fetch_response", return_value=Response(html, 404, f"{base_url}/")):
        assert spider.probe_alternative_homepage(f"{base_url}/") == (None, None, None)
    with patch.object(spider, "fetch_response", return_value=Response(html, 200, f"{base_url}/")):
        assert spider.probe_alternative_homepage(f"{base_url}/")[2] == base_url


def test_scheme_upgrade():
    "An http crawl of a site redirecting to https must follow the upgrade and keep its links."
    spider.URL_STORE = UrlStore()
    links = "".join(f'<a href="https://scheme-upgrade.org/p{i}.html">x</a>' for i in range(3))
    html = f"<html><body>{links}</body></html>"

    def fake_fetch_response(url, *, decode=False, config=None, **kw):
        return Response(html.encode(), 200, url.replace("http://", "https://"))

    with (
        patch.object(spider, "fetch_response", fake_fetch_response),
        patch.object(spider, "get_rules", lambda *a, **kw: None),
        patch.object(spider, "sleep", lambda s: None),
    ):
        _todo, known_links = spider.focused_crawler("http://scheme-upgrade.org", max_seen_urls=10)
    assert sorted(known_links) == [
        "https://scheme-upgrade.org/",
        "https://scheme-upgrade.org/p0.html",
        "https://scheme-upgrade.org/p1.html",
        "https://scheme-upgrade.org/p2.html",
    ]


def test_host_redirect():
    "A homepage redirecting to another host keeps the crawl on the start host, links resolved against the start URL."
    spider.URL_STORE = UrlStore()
    html = '<html><body><a href="/p1.html">x</a><a href="https://other-host.org/p2.html">y</a></body></html>'

    def fake_fetch_response(url, *, decode=False, config=None, **kw):
        return Response(html.encode(), 200, "https://other-host.org/")

    with (
        patch.object(spider, "fetch_response", fake_fetch_response),
        patch.object(spider, "get_rules", lambda *a, **kw: None),
    ):
        params = spider.init_crawl("http://host-redirect.org")
    assert params.base == "http://host-redirect.org"
    assert spider.URL_STORE.find_unvisited_urls(params.base) == ["http://host-redirect.org/p1.html"]


def test_is_same_site():
    "Besides a scheme upgrade, only a leading www may differ after a redirect."
    assert spider.is_same_site("http://Example.org:8080", "https://www.example.org:8080")
    assert not spider.is_same_site("https://example.org", "https://www2.example.org")
    assert not spider.is_same_site("https://example.org", "https://www.example.org:8443")
    assert not spider.is_same_site("https://example.org", "http://example.org")


def test_www_redirect():
    "A homepage redirect between the bare domain and its www twin moves the crawl to the redirected host."
    for start, homepage in [
        ("https://twin-redirect.org", "https://www.twin-redirect.org/"),
        ("https://www.twin-redirect.org", "https://twin-redirect.org/"),
        ("http://twin-redirect.org", "https://www.twin-redirect.org/"),
        ("http://www.twin-redirect.org", "https://twin-redirect.org/"),
    ]:
        spider.URL_STORE = UrlStore()
        base = homepage.rstrip("/")
        html = f'<html><body><a href="{base}/p1.html">x</a><a href="/p2.html">y</a></body></html>'
        with (
            patch.object(spider, "fetch_response", return_value=Response(html.encode(), 200, homepage)),
            patch.object(spider, "get_rules", return_value=None),
        ):
            params = spider.init_crawl(start)
        assert params.base == params.ref == base
        todo = spider.URL_STORE.find_unvisited_urls(params.base)
        assert f"{base}/p1.html" in todo
        assert f"{base}/p2.html" in todo

    # the crawl stays within the directory of the start URL
    spider.URL_STORE = UrlStore()
    html = '<html><body><a href="https://www.twin-redirect.org/blog/p1.html">x</a><a href="https://www.twin-redirect.org/about">y</a></body></html>'
    with (
        patch.object(
            spider, "fetch_response", return_value=Response(html.encode(), 200, "https://www.twin-redirect.org/blog/")
        ),
        patch.object(spider, "get_rules", return_value=None),
    ):
        params = spider.init_crawl("https://twin-redirect.org/blog/")
    assert params.base == "https://www.twin-redirect.org"
    assert params.ref == "https://www.twin-redirect.org/blog"
    todo = spider.URL_STORE.find_unvisited_urls(params.base)
    assert "https://www.twin-redirect.org/blog/p1.html" in todo
    assert "https://www.twin-redirect.org/about" not in todo


def test_www_redirect_keeps_rules_and_homepage():
    "After a redirect to the www twin, robots.txt rules follow the new base and the homepage is not queued again."
    spider.URL_STORE = UrlStore()
    rules = RobotFileParser()
    rules.parse(["User-agent: *", "Crawl-delay: 7"])
    homepage = "https://www.twin-rules.org/"
    html = f'<html><body><a href="{homepage}p1.html">x</a></body></html>'
    with (
        patch.object(spider, "fetch_response", return_value=Response(html.encode(), 200, homepage)),
        patch.object(spider, "get_rules", return_value=rules),
    ):
        params = spider.init_crawl("https://twin-rules.org")
    assert params.base == "https://www.twin-rules.org"
    assert spider.URL_STORE.get_crawl_delay(params.base) == 7
    assert homepage not in spider.URL_STORE.find_unvisited_urls(params.base)


def test_focused_crawler():
    "Test the whole focused crawler mechanism."
    spider.URL_STORE = UrlStore()
    _todo, known_links = spider.focused_crawler("https://httpbun.com/links/2/2", max_seen_urls=2)
    assert len(known_links) > 0
    ## fails on Github Actions
    # assert sorted(known_links) == ['https://httpbun.com/links/2/0', 'https://httpbun.com/links/2/1', 'https://httpbun.com/links/2/2']
    # assert len(todo) == 1 and todo[0].startswith('https://httpbun.com/links/2')


def test_robots():
    "Test robots.txt parsing"
    assert spider.get_rules("1234") is None

    robots_url = "https://example.org/robots.txt"

    assert spider.parse_robots(robots_url, None) is None
    assert spider.parse_robots(robots_url, 123) is None
    assert spider.parse_robots(robots_url, b"123") is None

    rules = spider.parse_robots(robots_url, "Allow: *")
    assert rules
    assert rules.can_fetch("*", "https://example.org/1")

    rules = spider.parse_robots(robots_url, "User-agent: *\nDisallow: /")
    assert rules
    assert not rules.can_fetch("*", "https://example.org/1")

    rules = spider.parse_robots(robots_url, "User-agent: *\nDisallow: /private")
    assert rules
    assert not rules.can_fetch("*", "https://example.org/private")
    assert rules.can_fetch("*", "https://example.org/public")

    rules = spider.parse_robots(robots_url, "Allow: *\nUser-agent: *\nCrawl-delay: 10")
    assert rules
    assert rules.crawl_delay("*") == 10

    # rules = spider.parse_robots(robots_url, "User-agent: *\nAllow: /public")
    # assert rules is not None and rules.can_fetch("*", "https://example.org/public")
    # assert not rules.can_fetch("*", "https://example.org/private")
