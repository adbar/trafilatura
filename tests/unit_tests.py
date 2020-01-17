"""
Unit tests for the kontext library.
"""


import logging
import sys

from os import path

try:
    import cchardet as chardet
except ImportError:
    import chardet

from lxml import html

from kontext import scrape


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = path.abspath(path.dirname(__file__))


MOCK_PAGES = {
'http://blog.python.org/2016/12/python-360-is-now-available.html': 'blog.python.org.html',
'https://creativecommons.org/about/': 'creativecommons.org.html',
'https://www.creativecommons.at/faircoin-hackathon': 'creativecommons.at.faircoin.html',
'https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/': 'blog.wordpress.com.diverse.html',
'https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/': 'netzpolitik.org.abmahnungen.html',
'https://www.befifty.de/home/2017/7/12/unter-uns-montauk': 'befifty.montauk.html',
}


def load_mock_page(url):
    '''Load mock page from samples'''
    try:
        with open(path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = chardet.detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    return htmlstring


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
    meta_returned = scrape('<html><head><meta itemprop="author" content="Jenny Smith"/></head><body></body></html>')
    assert meta_returned.author == 'Jenny Smith'
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
    meta_returned = scrape('<html><head><meta name="dc.title" content="Open Graph Title"/><meta name="dc.creator" content="Jenny Smith"/><meta name="dc.description" content="This is an Open Graph description"/></head><body></body></html>')
    assert meta_returned.title == 'Open Graph Title'
    assert meta_returned.author == 'Jenny Smith'
    assert meta_returned.description == 'This is an Open Graph description'


def test_catstags():
    '''Test extraction of categories and tags'''
    meta_returned = scrape('<html><body><p class="entry-categories"><a href="https://example.org/category/cat1/">Cat1</a>, <a href="https://example.org/category/cat2/">Cat2</a></p></body></html>')
    assert meta_returned.categories == ['Cat1', 'Cat2']
    meta_returned = scrape('<html><body><p class="entry-tags"><a href="https://example.org/tags/tag1/">Tag1</a>, <a href="https://example.org/tags/tag2/">Tag2</a></p></body></html>')
    assert meta_returned.tags == ['Tag1', 'Tag2']


def test_pages():
    '''Test on real web pages'''
    meta_returned = scrape(load_mock_page('http://blog.python.org/2016/12/python-360-is-now-available.html'))
    assert meta_returned.title == 'Python 3.6.0 is now available!'
    assert meta_returned.description == 'Python 3.6.0 is now available! Python 3.6.0 is the newest major release of the Python language, and it contains many new features and opti...'
    # author = span class="post-author"
    meta_returned = scrape(load_mock_page('https://en.blog.wordpress.com/2019/06/19/want-to-see-a-more-diverse-wordpress-contributor-community-so-do-we/'))
    assert meta_returned.title == 'Want to See a More Diverse WordPress Contributor Community? So Do We.'
    assert meta_returned.description == 'More diverse speakers at WordCamps means a more diverse community contributing to WordPress — and that results in better software for everyone.'
    assert meta_returned.sitename == 'The WordPress.com Blog'
    meta_returned = scrape(load_mock_page('https://creativecommons.org/about/'))
    assert meta_returned.title == 'What we do - Creative Commons'
    assert meta_returned.description == 'What is Creative Commons? Creative Commons helps you legally share your knowledge and creativity to build a more equitable, accessible, and innovative world. We unlock the full potential of the internet to drive a new era of development, growth and productivity. With a network of staff, board, and affiliates around the world, Creative Commons provides … Read More "What we do"'
    assert meta_returned.sitename == 'Creative Commons'
    # date None
    meta_returned = scrape(load_mock_page('https://www.creativecommons.at/faircoin-hackathon'))
    assert meta_returned.title == 'FairCoin hackathon beim Sommercamp'
    # url='/faircoin-hackathon'
    # print(meta_returned)
    meta_returned = scrape(load_mock_page('https://netzpolitik.org/2016/die-cider-connection-abmahnungen-gegen-nutzer-von-creative-commons-bildern/'))
    assert meta_returned.title == 'Die Cider Connection: Abmahnungen gegen Nutzer von Creative-Commons-Bildern'
    assert meta_returned.author == 'Markus Reuter'
    assert meta_returned.description == 'Seit Dezember 2015 verschickt eine Cider Connection zahlreiche Abmahnungen wegen fehlerhafter Creative-Commons-Referenzierungen. Wir haben recherchiert und legen jetzt das Netzwerk der Abmahner offen.'
    assert meta_returned.sitename == 'netzpolitik.org'
    # cats + tags
    meta_returned = scrape(load_mock_page('https://www.befifty.de/home/2017/7/12/unter-uns-montauk'))
    assert meta_returned.title == 'Das vielleicht schönste Ende der Welt: Montauk'
    assert meta_returned.author == 'Beate Finken'
    assert meta_returned.description == 'Ein Strand, ist ein Strand, ist ein Strand Ein Strand, ist ein Strand, ist ein Strand. Von wegen! In Italien ist alles wohl organisiert, Handtuch an Handtuch oder Liegestuhl an Liegestuhl. In der Karibik liegt man unter Palmen im Sand und in Marbella dominieren Beton und eine kerzengerade Promenade'
    assert meta_returned.sitename == 'BeFifty'
    assert meta_returned.categories == ['Travel', 'Amerika']


if __name__ == '__main__':
    test_titles()
    test_authors()
    test_dates()
    test_meta()
    test_url()
    test_catstags()
    test_pages()
