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
    title, _, _, _, _, _ = scrape('<html><head><title>Test Title</title></head><body></body></html>')
    assert title == 'Test Title'
    title, _, _, _, _, _ = scrape('<html><body><h1>First</h1><h1>Second</h1></body></html>')
    assert title == 'First'
    title, _, _, _, _, _ = scrape('<html><body><h2>First</h2><h1>Second</h1></body></html>')
    assert title == 'Second'
    title, _, _, _, _, _ = scrape('<html><body><h2>First</h2><h2>Second</h2></body></html>')
    assert title == 'First'


def test_authors():
    '''Test the extraction of author names'''
    _, author, _, _, _, _ = scrape('<html><body><a href="" rel="author">Jenny Smith</a></body></html>')
    assert author == 'Jenny Smith'


def test_url():
    '''Test the extraction of author names'''
    _, _, url, _, _, _ = scrape('<html><head><meta property="og:url" content="https://example.org"/></head><body></body></html>')
    assert url == 'https://example.org'
    _, _, url, _, _, _ = scrape('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>')
    assert url == 'https://example.org'


def test_dates():
    '''Simple tests for date extraction (most of the tests are carried out externally for htmldate module)'''
    _, _, _, date, _, _ = scrape('<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>')
    assert date == '2017-09-01'
    _, _, _, date, _, _ = scrape('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    assert date == '2017-09-01'


def test_meta():
    '''Test extraction out of meta-elements'''
    title, author, _, _, description, site_name = scrape('<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/><meta property="og:site_name" content="My first site"/></head><body></body></html>')
    assert title == 'Open Graph Title'
    assert author == 'Jenny Smith'
    assert description == 'This is an Open Graph description'
    assert site_name == 'My first site'


if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()
    test_url()
