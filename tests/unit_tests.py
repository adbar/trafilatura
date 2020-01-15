"""
Unit tests for the kontext library.
"""


import logging
import sys

from kontext import scrape
from lxml import html



logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_titles():
    '''Test the extraction of titles'''
    title, _, _, _ = scrape('<html><head><title>Test Title</title></head><body></body></html>')
    assert title == 'Test Title'


def test_authors():
    '''Test the extraction of author names'''
    _, author, _, _ = scrape('<html><body><a href="" rel="author">Jenny Smith</a></body></html>')
    assert author == 'Jenny Smith'


def test_dates():
    '''Simple tests for date extraction (most of the tests are carried out externally for htmldate module)'''
    _, _, date, _ = scrape('<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>')
    assert date == '2017-09-01'


def test_meta():
    '''Test extraction out of meta-elements'''
    title, author, _, description = scrape('<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/></head><body></body></html>')
    assert title == 'Open Graph Title'
    assert author == 'Jenny Smith'
    assert description == 'This is an Open Graph description'


if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()