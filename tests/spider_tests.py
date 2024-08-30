# pylint:disable-msg=W1401
"""
Unit tests for the spidering part of the trafilatura library.
"""

import logging
import sys

from collections import deque

import pytest

from courlan import UrlStore

from trafilatura import spider  # for global variables

# from trafilatura.utils import LANGID_FLAG


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_redirections():
    "Test redirection detection."
    _, _, baseurl = spider.probe_alternative_homepage("xyz")
    assert baseurl is None
    _, _, baseurl = spider.probe_alternative_homepage(
        "https://httpbun.com/redirect-to?url=https://example.org"
    )
    assert baseurl == "https://example.org"
    # _, _, baseurl = spider.probe_alternative_homepage('https://httpbin.org/redirect-to?url=https%3A%2F%2Fhttpbin.org%2Fhtml&status_code=302')


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
        # relative URL
        # ('<html><meta http-equiv="refresh" content="0; url=/html"/></html>', 'http://test.org/', 'http://test.org/html'),
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
    assert (
        len(spider.URL_STORE.find_unvisited_urls(base_url)) == 1
        and len(spider.URL_STORE.find_known_urls(base_url)) == 1
    )

    # test navigation links
    url1 = "https://example.org/tag/number1"
    url2 = "https://example.org/page2"
    htmlstring = f'<html><body><a href="{url1}"/><a href="{url2}"/></body></html>'
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(known_links) == 3
    assert len(todo) == 3 and todo[0] == url1

    # test cleaning and language
    url = "https://example.org/en/page1/?"
    target = "https://example.org/en/page1/"
    htmlstring = f'<html><body><a href="{url}"/></body></html>'
    params = spider.CrawlParameters(base_url, lang="en")
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(known_links) == 4
    assert len(todo) == 4 and target in todo  # TODO: remove slash?

    # test rejection of URLs out of scope
    url = "https://example.org/section2/page2"
    htmlstring = f'<html><body><a href="{url}"/></body></html>'
    params = spider.CrawlParameters("https://example.org/section1/")
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert url not in todo and len(known_links) == 4

    # wrong language
    url = "https://example.org/en/page2"
    htmlstring = f'<html><body><a href="{url}"/></body></html>'
    params = spider.CrawlParameters(base_url, lang="de")
    spider.process_links(htmlstring, params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert url not in todo and len(known_links) == 4

    # invalid links
    params = spider.CrawlParameters(base_url)
    htmlstring = '<html><body><a href="#anchor"/><a href="mailto:user@example.org"/><a href="tel:1234567890"/></body></html>'
    spider.process_links(htmlstring, params)
    assert len(known_links) == 4 and len(todo) == 4

    # not crawlable
    htmlstring = '<html><body><a href="https://example.org/login"/></body></html>'
    spider.process_links(htmlstring, params)
    assert len(known_links) == 4 and len(todo) == 4

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
    assert params.i == 0 and params.known_num == 0 and params.is_on
    assert params.lang is None and params.rules is None

    # already visited
    params = spider.init_crawl(url, known=[url])
    assert params.base == "https://httpbun.com"
    assert params.i == 0 and params.known_num == 1
    assert not params.is_on
    assert not spider.URL_STORE.find_unvisited_urls(params.base)
    assert spider.URL_STORE.find_known_urls(params.base) == ["https://httpbun.com/html"]

    # normal webpage
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    params = spider.init_crawl(url)
    assert (
        not spider.URL_STORE.find_unvisited_urls(params.base)
        and [url] == spider.URL_STORE.find_known_urls(params.base)
        and params.base == "https://httpbun.com"
        and params.i == 1
        and not params.is_on
    )

    # delay between requests
    assert spider.URL_STORE.get_crawl_delay("https://httpbun.com") == 5
    assert spider.URL_STORE.get_crawl_delay("https://httpbun.com", default=2.0) == 2.0

    # existing todo
    params = spider.init_crawl(url, todo=[url, "http://irrelevant.com"])
    assert not spider.URL_STORE.find_unvisited_urls(params.base)
    assert params.base == "https://httpbun.com" and params.i == 0 and not params.is_on

    # new todo
    params = spider.init_crawl(url, todo=["https://httpbun.com/links/1/1"])
    assert params.base == "https://httpbun.com"
    assert spider.URL_STORE.find_unvisited_urls(params.base) == [
        "https://httpbun.com/links/1/1"
    ]
    assert params.i == 0 and params.is_on and params.known_num == 2


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
    assert params.i == 1 and params.is_on and params.known_num == 3

    # prune path
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/links/2/2"])
    params = spider.CrawlParameters(base_url, prune_xpath="//a")
    params = spider.crawl_page(params)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)

    assert len(todo) == 0 and params.i == 1

    # prune path with initial page
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/links/2/2"])
    params = spider.CrawlParameters(base_url, prune_xpath="//a")
    params = spider.crawl_page(params, initial=True)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)

    assert len(todo) == 0 and params.i == 1

    # initial page
    spider.URL_STORE = UrlStore(compressed=False, strict=False)
    spider.URL_STORE.add_urls(["https://httpbun.com/html"])
    params = spider.CrawlParameters(base_url, lang="de")
    # if LANGID_FLAG is True:
    params = spider.crawl_page(params, initial=True)
    todo = spider.URL_STORE.find_unvisited_urls(base_url)
    known_links = spider.URL_STORE.find_known_urls(base_url)
    assert len(todo) == 0 and len(known_links) == 1 and params.i == 1
    ## TODO: find a better page for language tests


def test_focused_crawler():
    "Test the whole focused crawler mechanism."
    spider.URL_STORE = UrlStore()
    todo, known_links = spider.focused_crawler(
        "https://httpbun.com/links/2/2", max_seen_urls=2
    )
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
    assert rules and rules.can_fetch("*", "https://example.org/1")

    rules = spider.parse_robots(robots_url, "User-agent: *\nDisallow: /")
    assert rules and not rules.can_fetch("*", "https://example.org/1")

    rules = spider.parse_robots(robots_url, "User-agent: *\nDisallow: /private")
    assert rules and not rules.can_fetch("*", "https://example.org/private")
    assert rules.can_fetch("*", "https://example.org/public")

    rules = spider.parse_robots(robots_url, "Allow: *\nUser-agent: *\nCrawl-delay: 10")
    assert rules and rules.crawl_delay("*") == 10

    # rules = spider.parse_robots(robots_url, "User-agent: *\nAllow: /public")
    # assert rules is not None and rules.can_fetch("*", "https://example.org/public")
    # assert not rules.can_fetch("*", "https://example.org/private")


if __name__ == "__main__":
    test_redirections()
    test_meta_redirections()
    test_process_links()
    test_crawl_logic()
    test_crawl_page()
    test_focused_crawler()
    test_robots()
