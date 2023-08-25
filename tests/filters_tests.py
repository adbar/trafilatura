# pylint:disable-msg=I1101,W1401
"""
Unit tests for the trafilatura's text filters and cache.
"""

# language detection
try:
    import py3langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False


from lxml import etree, html

import trafilatura.filters
from trafilatura import extract
from trafilatura.core import Extractor
from trafilatura.filters import (check_html_lang, duplicate_test,
                                 language_filter)
from trafilatura.lru import LRUCache
from trafilatura.metadata import Document
from trafilatura.settings import DEFAULT_CONFIG

ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

DEFAULT_OPTIONS = Extractor(*[False]*11)
DEFAULT_OPTIONS.config = DEFAULT_CONFIG

SAMPLE_META = Document()


def test_filters():
    '''Test content filtering'''
    if LANGID_FLAG is True:
        # main text
        assert language_filter('Hier ist ein Text auf Deutsch', '', 'de', SAMPLE_META)[0] is False
        assert language_filter('Hier ist ein Text auf Deutsch', '', 'en', SAMPLE_META)[0] is True
        # comments
        assert language_filter('Hier ist ein Text.', 'Die Kommentare sind aber etwas länger.', 'de', SAMPLE_META)[0] is False
        # lang detection on the content
        doc = html.fromstring('<html><body><article><p>How many ages hence/Shall this our lofty scene be acted over,/In states unborn and accents yet unknown!</p></article></body></html>')
        assert extract(doc, config=ZERO_CONFIG, target_language='de') is None
        assert extract(doc, config=ZERO_CONFIG, target_language='en') is not None
    else:
        # no detection
        assert language_filter('Hier ist ein Text.', '', 'en', SAMPLE_META)[0] is False
    # test URL blacklist
    assert extract('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>', output_format='xml', url_blacklist={'https://example.org'}) is None
    ## recursion limit
    my_p = '<p>abc</p>'
    doc = html.fromstring('<html><body>' + my_p*50 + '</body></html>')
    assert extract(doc, max_tree_size=500) is not None
    doc = html.fromstring('<html><body>' + my_p*501 + '</body></html>')
    assert extract(doc, max_tree_size=500) is None
    my_p = '<p><hi rend="#i">abc</hi></p>'
    doc = html.fromstring('<html><body>' + my_p*501 + '</body></html>')
    assert extract(doc, include_formatting=True, max_tree_size=500) is None
    doc = html.fromstring('<html><body>' + my_p*499 + '</body></html>')
    assert extract(doc, include_formatting=True, max_tree_size=500) is not None
    ## deduplication
    doc = html.fromstring('<html><body>' + my_p*50 + '</body></html>')
    trafilatura.filters.LRU_TEST = LRUCache(maxsize=2)
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is None
    # paragraph level
    trafilatura.filters.LRU_TEST = LRUCache(maxsize=2)
    my_p = etree.fromstring('<p>' + 'abc'*50 + '</p>')
    options = DEFAULT_OPTIONS
    options.dedup = True
    assert trafilatura.htmlprocessing.process_node(my_p, options) is not None
    assert trafilatura.htmlprocessing.process_node(my_p, options) is not None
    assert trafilatura.htmlprocessing.process_node(my_p, options) is not None
    assert trafilatura.htmlprocessing.process_node(my_p, options) is None
    # HTML lang filter
    # no lang
    assert check_html_lang(html.fromstring('<html><body></body></html>'), target_language='en') is True
    # text + lang
    my_p = '<p>In sleep a king, but waking no such matter.</p>'
    if LANGID_FLAG is True:
        assert extract(html.fromstring('<html lang="en-US"><body>' + my_p*50 + '</body></html>'), no_fallback=True, target_language='en') is not None
        assert extract(html.fromstring('<html lang="en-US"><body>' + my_p*50 + '</body></html>'), no_fallback=True, target_language='de') is None
        # caught
        assert extract(html.fromstring('<html lang="de-DE"><body>' + my_p*50 + '</body></html>'), no_fallback=False, target_language='de') is None
    else:
        # not caught, HTML tag used
        assert extract(html.fromstring('<html lang="de-DE"><body>' + my_p*50 + '</body></html>'), no_fallback=False, target_language='de') is not None
    assert check_html_lang(html.fromstring('<html lang="de_DE, en_US"><body></body></html>'), target_language='de') is True
    assert check_html_lang(html.fromstring('<html lang="de_DE, en_US"><body></body></html>'), target_language='en') is True
    assert check_html_lang(html.fromstring('<html lang="de_DE, en_US"><body></body></html>'), target_language='de', strict=True) is True
    assert check_html_lang(html.fromstring('<html lang="de_DE, en_US"><body></body></html>'), target_language='en', strict=True) is True
    assert check_html_lang(html.fromstring('<html><head><meta http-equiv="content-language" content="en"></head><body></body></html>'), target_language='en') is True
    assert check_html_lang(html.fromstring('<html><head><meta http-equiv="content-language" content="en"></head><body></body></html>'), target_language='de') is False
    assert check_html_lang(html.fromstring('<html><head><meta http-equiv="content-language" content="DE"></head><body></body></html>'), target_language='de') is True
    # html lang attribute superseded by og:locale
    assert check_html_lang(html.fromstring('<html lang="en-US"><head><meta property="og:locale" content="de_DE" /></head><body></body></html>'), target_language='de') is True
    assert check_html_lang(html.fromstring('<html lang="en-US"><head><meta property="og:locale" content="de_DE" /></head><body></body></html>'), target_language='en') is False
    assert check_html_lang(html.fromstring('<html lang="en"><body></body></html>'), target_language='it', strict=True) is False
    assert check_html_lang(html.fromstring('<html lang="en"><body></body></html>'), target_language='it', strict=False) is True
    assert check_html_lang(html.fromstring('<html lang="en-US"><head><meta property="og:locale" content="de_DE" /></head><body></body></html>'), target_language='de', strict=False) is True
    assert check_html_lang(html.fromstring('<html lang="en-US"><head><meta property="og:locale" content="de_DE" /></head><body></body></html>'), target_language='de', strict=True) is True


def test_lrucache():
    '''test basic duplicate detection'''
    lru_test = LRUCache(maxsize=2)
    trafilatura.filters.LRU_TEST = lru_test
    my_body = etree.Element('body')
    ### element too short
    #my_element = html.fromstring('<p>AAAA BBBB</p>')
    #my_body.append(my_element)
    #put_in_cache(my_body)
    #assert duplicate_test(my_element, DEFAULT_CONFIG) is False
    ### cached element
    my_element = html.fromstring('<p>AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB</p>')
    my_body.append(my_element)
    assert duplicate_test(my_element, DEFAULT_CONFIG) is False
    assert duplicate_test(my_element, DEFAULT_CONFIG) is False
    assert duplicate_test(my_body, DEFAULT_CONFIG) is False
    assert duplicate_test(my_element, DEFAULT_CONFIG) is True
    other_body = etree.Element('body')
    other_element = html.fromstring('<p>CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD</p>')
    other_body.append(other_element)
    assert duplicate_test(other_body, DEFAULT_CONFIG) is False
    assert duplicate_test(other_element, DEFAULT_CONFIG) is False
    assert duplicate_test(other_body, DEFAULT_CONFIG) is False
    assert duplicate_test(other_element, DEFAULT_CONFIG) is True
    yet_another_body = etree.Element('body')
    yet_another_element = html.fromstring('<p>EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF</p>')
    yet_another_body.append(yet_another_element)
    assert duplicate_test(yet_another_body, DEFAULT_CONFIG) is False
    assert duplicate_test(yet_another_body, DEFAULT_CONFIG) is False
    assert duplicate_test(yet_another_body, DEFAULT_CONFIG) is False
    # 2 elements in cache, original element has been cleared?
    # print(LRU_TEST.maxsize, LRU_TEST.full)
    assert duplicate_test(other_element, DEFAULT_CONFIG) is True
    assert duplicate_test(yet_another_element, DEFAULT_CONFIG) is True
    assert duplicate_test(my_element, DEFAULT_CONFIG) is False
    # clear the cache
    lru_test.clear()
    assert duplicate_test(other_element, DEFAULT_CONFIG) is False
    # get wrong key
    assert lru_test.get('tralala') == -1


if __name__ == '__main__':
    test_filters()
    test_lrucache()
