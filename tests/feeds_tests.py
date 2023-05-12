"""
Unit tests for feeds reading and parsing.
"""

import logging
import os
import sys

from unittest.mock import patch

from trafilatura import cli, feeds


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')

XMLDECL = '<?xml version="1.0" encoding="utf-8"?>\n'


def test_atom_extraction():
    '''Test link extraction from an Atom feed'''
    assert feeds.extract_links(None, 'example.org', 'https://example.org', '') == []
    assert len(feeds.extract_links('<html></html>', 'example.org', 'https://example.org', '')) == 0
    filepath = os.path.join(RESOURCES_DIR, 'feed1.atom')
    with open(filepath) as f:
        teststring = f.read()
    assert len(feeds.extract_links(teststring, 'example.org', 'https://example.org', '')) > 0
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link type="application/atom+xml" rel="self" href="https://www.dwds.de/api/feed/themenglossar/Corona"/>',
                'dwds.de',
                'https://www.dwds.de',
                '',
            )
        )
        == 0
    )
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link rel="self" href="http://example.org/article1/"/>',
                'example.org',
                'http://example.org/',
                'http://example.org',
            )
        )
        == 0
    )
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link type="application/atom+xml" rel="self" href="123://api.exe"/>',
                'example.org',
                'https://example.org',
                '',
            )
        )
        == 0
    )
    assert feeds.extract_links(
        f'{XMLDECL}<link href="http://example.org/article1/"rest"/>',
        'example.org',
        'http://example.org/',
        'http://example.org',
    ) == ['http://example.org/article1/']


def test_rss_extraction():
    '''Test link extraction from a RSS feed'''
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link>http://example.org/article1/</link>',
                'example.org',
                'http://example.org/',
                '',
            )
        )
        == 1
    )
    # CDATA
    assert feeds.extract_links(
        f'{XMLDECL}<link><![CDATA[http://example.org/article1/]]></link>',
        'example.org',
        'http://example.org/',
        '',
    ) == ['http://example.org/article1/']
    # spaces
    assert len(feeds.extract_links(XMLDECL + '<link>\r\n    https://www.ak-kurier.de/akkurier/www/artikel/108815-sinfonisches-blasorchester-spielt-1500-euro-fuer-kinder-in-drk-krankenhaus-kirchen-ein    </link>', 'ak-kurier.de', 'https://www.ak-kurier.de/', '')) == 1
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link>http://example.org/</link>',
                'example.org',
                'http://example.org',
                'http://example.org',
            )
        )
        == 0
    )
    assert (
        len(
            feeds.extract_links(
                f'{XMLDECL}<link>https://example.org</link>',
                'example.org',
                'http://example.org/',
                '',
            )
        )
        == 0
    )
    assert feeds.extract_links(
        f'{XMLDECL}<link>/api/feed/themenglossar/Corona</link>',
        'www.dwds.de',
        'https://www.dwds.de',
        'https://www.dwds.de',
    ) == ['https://www.dwds.de/api/feed/themenglossar/Corona']
    filepath = os.path.join(RESOURCES_DIR, 'feed2.rss')
    with open(filepath) as f:
        teststring = f.read()
    assert len(feeds.extract_links(teststring, 'example.com', 'https://example.org', '')) > 0


def test_json_extraction():
    '''Test link extraction from a JSON feed'''
    # find link
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/json" title="JSON Feed" href="https://www.jsonfeed.org/feed.json" />></meta><body/></html>', 'jsonfeed.org', 'https://www.jsonfeed.org')) == 1
    # extract data
    filepath = os.path.join(RESOURCES_DIR, 'feed.json')
    with open(filepath) as f:
        teststring = f.read()
    links = feeds.extract_links(teststring, 'npr.org', 'https://npr.org', '')
    assert len(links) == 25
    # id as a backup
    links = feeds.extract_links(r'{"version":"https:\/\/jsonfeed.org\/version\/1","items":[{"id":"https://www.example.org/1","title":"Test"}]}', 'example.org', 'https://example.org', '')
    assert len(links) == 1


def test_feeds_helpers():
    '''Test helper functions for feed extraction'''
    # nothing useful
    assert len(feeds.determine_feed('', 'example.org', 'https://example.org')) == 0
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/rss+xml" title="Feed"/></meta><body/></html>', 'example.org', 'https://example.org')) == 0
    # useful
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/rss+xml" title="Feed" href="https://example.org/blog/feed/"/></meta><body/></html>', 'example.org', 'https://example.org')) == 1
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/atom+xml" title="Feed" href="https://example.org/blog/feed/"/></meta><body/></html>', 'example.org', 'https://example.org')) == 1
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" title="Feed" href="https://example.org/blog/feed/" type="application/atom+xml"/></meta><body/></html>', 'example.org', 'https://example.org')) == 1
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" title="Feed" href="https://example.org/blog/atom/"/></meta><body/></html>', 'example.org', 'https://example.org')) == 1
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" href="https://www.theguardian.com/international/rss" title="RSS" type="application/rss+xml"></meta><body/></html>', 'example.org', 'https://example.org')) == 1
    # no comments wanted
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/rss+xml" title="Feed" href="https://example.org/blog/comments-feed/"/></meta><body/></html>', 'example.org', 'https://example.org')) == 0
    # invalid links
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" href="12345tralala" title="RSS" type="application/rss+xml"></meta><body/></html>', 'example.org', 'https://example.org')) == 0
    # detecting in <a>-elements
    assert feeds.determine_feed('<html><body><a href="https://example.org/feed.xml"><body/></html>', 'example.org', 'https://example.org') == ['https://example.org/feed.xml']
    assert feeds.determine_feed('<html><body><a href="https://example.org/feed.atom"><body/></html>', 'example.org', 'https://example.org') == ['https://example.org/feed.atom']
    assert feeds.determine_feed('<html><body><a href="https://example.org/rss"><body/></html>', 'example.org', 'https://example.org') == ['https://example.org/rss']
    # feed discovery
    assert feeds.find_feed_urls('http://') == []
    assert feeds.find_feed_urls('https://httpbun.org/status/404') == []
    # Feedburner/Google links
    assert feeds.handle_link_list(['https://feedproxy.google.com/ABCD'], 'example.org', 'https://example.org') == ['https://feedproxy.google.com/ABCD']
    # override failed checks
    assert feeds.handle_link_list(['https://feedburner.com/kat/1'], 'example.org', 'https://example.org') == ['https://feedburner.com/kat/1']
    # diverging domain names
    assert feeds.handle_link_list(['https://www.software.info/1'], 'example.org', 'https://example.org') == []


def test_cli_behavior():
    '''Test command-line interface with respect to feeds'''
    testargs = ['', '--list', '--feed', 'https://httpbun.org/xml']
    with patch.object(sys, 'argv', testargs):
        assert cli.main() is None


if __name__ == '__main__':
    test_atom_extraction()
    test_rss_extraction()
    test_json_extraction()
    test_feeds_helpers()
    test_cli_behavior()
