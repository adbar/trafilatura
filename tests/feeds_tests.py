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



def test_atom_extraction():
    '''Test link extraction from an Atom feed'''
    filepath = os.path.join(RESOURCES_DIR, 'feed1.atom')
    with open(filepath) as f:
        teststring = f.read()
    assert len(feeds.extract_links(teststring)) > 0
    assert len(feeds.extract_links('<link type="application/atom+xml" rel="self" href="https://www.dwds.de/api/feed/themenglossar/Corona"/>')) == 0


def test_rss_extraction():
    '''Test link extraction from a RSS feed'''
    filepath = os.path.join(RESOURCES_DIR, 'feed2.rss')
    with open(filepath) as f:
        teststring = f.read()
    assert len(feeds.extract_links(teststring)) > 0


def test_feeds_helpers():
    '''Test helper functions for feed extraction'''
    assert feeds.validate_url('http://example.org/article1/') is True
    assert feeds.validate_url('') is False
    assert feeds.validate_url('http://example.org/') is False
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/rss+xml" title="Feed" href="https://example.org/blog/feed/"/></meta><body/></html>')) == 1
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/atom+xml" title="Feed" href="https://example.org/blog/feed/"/></meta><body/></html>')) == 1
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" href="https://www.theguardian.com/international/rss" title="RSS" type="application/rss+xml"></meta><body/></html>')) == 1
    # no comments wanted
    assert len(feeds.determine_feed('<html><meta><link rel="alternate" type="application/rss+xml" title="Feed" href="https://example.org/blog/comments-feed/"/></meta><body/></html>')) == 0


def test_cli_behavior():
    '''Test command-line interface with respect to feeds'''
    testargs = ['', '--list', '--feed', 'https://httpbin.org/xml']
    with patch.object(sys, 'argv', testargs):
        assert cli.main() is None


if __name__ == '__main__':
   test_atom_extraction()
   test_rss_extraction()
   test_feeds_helpers()
   test_cli_behavior()
