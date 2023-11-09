"""
Unit tests for feeds reading and parsing.
"""

import logging
import os
import sys
from unittest.mock import patch

from courlan import get_hostinfo
from trafilatura import cli, feeds

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, "resources")

XMLDECL = '<?xml version="1.0" encoding="utf-8"?>\n'


def test_atom_extraction():
    """Test link extraction from an Atom feed"""
    params = feeds.FeedParameters("https://example.org", "example.org", "")
    assert not feeds.extract_links(None, params)
    assert len(feeds.extract_links("<html></html>", params)) == 0

    filepath = os.path.join(RESOURCES_DIR, "feed1.atom")
    with open(filepath, "r", encoding="utf-8") as f:
        teststring = f.read()
    assert len(feeds.extract_links(teststring, params)) > 0

    params = feeds.FeedParameters("https://www.dwds.de", "dwds.de", "")
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link type="application/atom+xml" rel="self" href="https://www.dwds.de/api/feed/themenglossar/Corona"/>',
                params,
            )
        )
        == 0
    )

    params = feeds.FeedParameters(
        "http://example.org", "example.org", "http://example.org"
    )
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link rel="self" href="http://example.org/article1/"/>',
                params,
            )
        )
        == 0
    )

    params = feeds.FeedParameters("https://example.org", "example.org", "")
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link type="application/atom+xml" rel="self" href="123://api.exe"/>',
                params,
            )
        )
        == 0
    )

    params = feeds.FeedParameters(
        "http://example.org/", "example.org", "http://example.org"
    )
    assert feeds.extract_links(
        f'{XMLDECL}<link href="http://example.org/article1/"rest"/>', params
    ) == [
        "http://example.org/article1/"
    ]  # TODO: remove slash?


def test_rss_extraction():
    """Test link extraction from a RSS feed"""
    params = feeds.FeedParameters("http://example.org/", "example.org", "")
    assert (
        len(
            feeds.extract_links(
                f"{XMLDECL}<link>http://example.org/article1/</link>", params
            )
        )
        == 1
    )
    # CDATA
    assert feeds.extract_links(
        f"{XMLDECL}<link><![CDATA[http://example.org/article1/]]></link>", params
    ) == [
        "http://example.org/article1/"
    ]  # TODO: remove slash?

    # spaces
    params = feeds.FeedParameters("https://www.ak-kurier.de/", "ak-kurier.de", "")
    assert (
        len(
            feeds.extract_links(
                XMLDECL
                + "<link>\r\n    https://www.ak-kurier.de/akkurier/www/artikel/108815-sinfonisches-blasorchester-spielt-1500-euro-fuer-kinder-in-drk-krankenhaus-kirchen-ein    </link>",
                params,
            )
        )
        == 1
    )

    params = feeds.FeedParameters(
        "http://example.org", "example.org", "http://example.org"
    )
    assert (
        len(feeds.extract_links(f"{XMLDECL}<link>http://example.org/</link>", params))
        == 0
    )

    params = feeds.FeedParameters("http://example.org", "example.org", "")
    assert (
        len(feeds.extract_links(f"{XMLDECL}<link>https://example.org</link>", params))
        == 0
    )

    params = feeds.FeedParameters(
        "https://www.dwds.de", "dwds.de", "https://www.dwds.de"
    )
    assert feeds.extract_links(
        f"{XMLDECL}<link>/api/feed/themenglossar/Corona</link>", params
    ) == ["https://www.dwds.de/api/feed/themenglossar/Corona"]

    params = feeds.FeedParameters("https://example.org", "example.org", "")
    filepath = os.path.join(RESOURCES_DIR, "feed2.rss")
    with open(filepath, "r", encoding="utf-8") as f:
        teststring = f.read()
    assert len(feeds.extract_links(teststring, params)) > 0


def test_json_extraction():
    """Test link extraction from a JSON feed"""
    # find link
    params = feeds.FeedParameters("https://www.jsonfeed.org", "jsonfeed.org", "")
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" type="application/json" title="JSON Feed" href="https://www.jsonfeed.org/feed.json" />></meta><body/></html>',
                params,
            )
        )
        == 1
    )

    # extract data
    filepath = os.path.join(RESOURCES_DIR, "feed.json")
    with open(filepath, "r", encoding="utf-8") as f:
        teststring = f.read()
    params = feeds.FeedParameters("https://npr.org", "npr.org", "")
    links = feeds.extract_links(teststring, params)
    assert len(links) == 25

    # id as a backup
    params = feeds.FeedParameters("https://example.org", "example.org", "")
    links = feeds.extract_links(
        r'{"version":"https:\/\/jsonfeed.org\/version\/1","items":[{"id":"https://www.example.org/1","title":"Test"}]}',
        params,
    )
    assert len(links) == 1


def test_feeds_helpers():
    """Test helper functions for feed extraction"""
    params = feeds.FeedParameters(
        "https://example.org", "example.org", "https://example.org"
    )
    domainname, baseurl = get_hostinfo("https://example.org")
    assert domainname == params.domain and baseurl == params.base

    # nothing useful
    assert len(feeds.determine_feed("", params)) == 0
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" type="application/rss+xml" title="Feed"/></meta><body/></html>',
                params,
            )
        )
        == 0
    )
    # useful
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" type="application/rss+xml" title="Feed" href="https://example.org/blog/feed/"/></meta><body/></html>',
                params,
            )
        )
        == 1
    )
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" type="application/atom+xml" title="Feed" href="https://example.org/blog/feed/"/></meta><body/></html>',
                params,
            )
        )
        == 1
    )
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" title="Feed" href="https://example.org/blog/feed/" type="application/atom+xml"/></meta><body/></html>',
                params,
            )
        )
        == 1
    )
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" title="Feed" href="https://example.org/blog/atom/"/></meta><body/></html>',
                params,
            )
        )
        == 1
    )
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" href="https://www.theguardian.com/international/rss" title="RSS" type="application/rss+xml"></meta><body/></html>',
                params,
            )
        )
        == 1
    )
    # no comments wanted
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" type="application/rss+xml" title="Feed" href="https://example.org/blog/comments-feed/"/></meta><body/></html>',
                params,
            )
        )
        == 0
    )

    # invalid links
    params = feeds.FeedParameters(
        "example.org", "example.org", "https://example.org"
    )  # fix
    assert (
        len(
            feeds.determine_feed(
                '<html><meta><link rel="alternate" href="12345tralala" title="RSS" type="application/rss+xml"></meta><body/></html>',
                params,
            )
        )
        == 0
    )

    # detecting in <a>-elements
    params = feeds.FeedParameters(
        "https://example.org", "example.org", "https://example.org"
    )
    assert feeds.determine_feed(
        '<html><body><a href="https://example.org/feed.xml"><body/></html>', params
    ) == ["https://example.org/feed.xml"]
    assert feeds.determine_feed(
        '<html><body><a href="https://example.org/feed.atom"><body/></html>', params
    ) == ["https://example.org/feed.atom"]
    assert feeds.determine_feed(
        '<html><body><a href="https://example.org/rss"><body/></html>', params
    ) == ["https://example.org/rss"]
    # feed discovery
    assert not feeds.find_feed_urls("http://")
    assert not feeds.find_feed_urls("https://httpbun.org/status/404")
    # Feedburner/Google links
    assert feeds.handle_link_list(["https://feedproxy.google.com/ABCD"], params) == [
        "https://feedproxy.google.com/ABCD"
    ]
    # override failed checks
    assert feeds.handle_link_list(["https://feedburner.com/kat/1"], params) == [
        "https://feedburner.com/kat/1"
    ]
    # diverging domain names
    assert not feeds.handle_link_list(["https://www.software.info/1"], params)


def test_cli_behavior():
    """Test command-line interface with respect to feeds"""
    testargs = ["", "--list", "--feed", "https://httpbun.org/xml"]
    with patch.object(sys, "argv", testargs):
        assert cli.main() is None


if __name__ == "__main__":
    test_atom_extraction()
    test_rss_extraction()
    test_json_extraction()
    test_feeds_helpers()
    test_cli_behavior()
