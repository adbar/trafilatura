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
    meta_returned = scrape('<html><head><title>Test Title</title></head><body></body></html>')
    assert meta_returned.title == 'Test Title'
    meta_returned = scrape('<html><body><h1>First</h1><h1>Second</h1></body></html>')
    assert meta_returned.title == 'First'
    meta_returned = scrape('<html><body><h2>First</h2><h1>Second</h1></body></html>')
    assert meta_returned.title == 'Second'
    meta_returned = scrape('<html><body><h2>First</h2><h2>Second</h2></body></html>')
    assert meta_returned.title == 'First'


def test_authors():
    '''Test the extraction of author names'''
    meta_returned = scrape('<html><body><a href="" rel="author">Jenny Smith</a></body></html>')
    assert meta_returned.author == 'Jenny Smith'
    meta_returned = scrape('<html><body><span class="author">Jenny Smith</span></body></html>')
    assert meta_returned.author == 'Jenny Smith'
    meta_returned = scrape('<html><body><a class="author">Jenny Smith</a></body></html>')
    assert meta_returned.author == 'Jenny Smith'
    meta_returned = scrape('<html><body><address class="author">Jenny Smith</address></body></html>')
    assert meta_returned.author == 'Jenny Smith'
    meta_returned = scrape('<html><body><author>Jenny Smith</author></body></html>')
    assert meta_returned.author == 'Jenny Smith'


def test_url():
    '''Test the extraction of author names'''
    meta_returned = scrape('<html><head><meta property="og:url" content="https://example.org"/></head><body></body></html>')
    assert meta_returned.url == 'https://example.org'
    meta_returned = scrape('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>')
    assert meta_returned.url == 'https://example.org'


def test_dates():
    '''Simple tests for date extraction (most of the tests are carried out externally for htmldate module)'''
    meta_returned = scrape('<html><head><meta property="og:published_time" content="2017-09-01"/></head><body></body></html>')
    assert meta_returned.date == '2017-09-01'
    meta_returned = scrape('<html><head><meta property="og:url" content="https://example.org/2017/09/01/content.html"/></head><body></body></html>')
    print(meta_returned)
    assert meta_returned.date == '2017-09-01'


def test_meta():
    '''Test extraction out of meta-elements'''
    meta_returned = scrape('<html><head><meta property="og:title" content="Open Graph Title"/><meta property="og:author" content="Jenny Smith"/><meta property="og:description" content="This is an Open Graph description"/><meta property="og:site_name" content="My first site"/></head><body></body></html>')
    assert meta_returned.title == 'Open Graph Title'
    assert meta_returned.author == 'Jenny Smith'
    assert meta_returned.description == 'This is an Open Graph description'
    assert meta_returned.sitename == 'My first site'


def test_catstags():
    '''Test extraction of categories and tags'''
    meta_returned = scrape('<html><body><p class="entry-categories"><a href="https://example.org/category/cat1/">Cat1</a>, <a href="https://example.org/category/cat2/">Cat2</a></p></body></html>')
    assert meta_returned.categories == ['Cat1', 'Cat2']
    meta_returned = scrape('<html><body><p class="entry-tags"><a href="https://example.org/tags/tag1/">Tag1</a>, <a href="https://example.org/tags/tag2/">Tag2</a></p></body></html>')
    assert meta_returned.tags == ['Tag1', 'Tag2']


if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()
    test_url()
    test_catstags()
