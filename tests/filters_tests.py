# pylint:disable-msg=I1101,W1401
"""
Unit tests for the trafilatura's text filters.
"""

from lxml import html

from trafilatura import extract
from trafilatura.metadata import Document
from trafilatura.settings import DEFAULT_CONFIG, Extractor
from trafilatura.utils import LANGID_FLAG, check_html_lang, language_filter


ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

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
    options = Extractor()
    options.max_tree_size = 500
    my_p = '<p>abc</p>'
    doc = html.fromstring('<html><body>' + my_p*50 + '</body></html>')
    assert extract(doc, options=options) is not None
    doc = html.fromstring('<html><body>' + my_p*501 + '</body></html>')
    assert extract(doc, options=options) is None

    options.formatting = True
    my_p = '<p><hi rend="#i">abc</hi></p>'
    doc = html.fromstring('<html><body>' + my_p*501 + '</body></html>')
    assert extract(doc, options=options) is None
    doc = html.fromstring('<html><body>' + my_p*499 + '</body></html>')
    assert extract(doc, options=options) is not None

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



def test_prune_xpath():
    '''test xpath pruning (parameter in extract and bare_extraction)'''
    #create example html
    def doc():
        my_p = '<p>abc</p>'
        return html.fromstring('<html><body>' + my_p*50 + '</body></html>')

    def doc2():
        my_p = '<p>abc</p>'
        my_h1 = '<h1>ABC</h1>'
        return html.fromstring('<html><body>' + my_h1 + my_p*50 + '</body></html>')

    def doc3():
        my_p = '<p>abc</p>'
        my_h1 = '<h1>ABC</h1>'
        my_h2 = '<h2>42</h2>'
        return html.fromstring('<html><body>' + my_h1 + my_h2 + my_p*50 + '</body></html>')

    #test xpath pruning
    assert extract(doc(), prune_xpath='//p') == ''
    assert extract(doc2(), prune_xpath='//p') == 'ABC'
    assert extract(doc2(), prune_xpath=['//p', '//h1']) == ''
    assert extract(doc3(), prune_xpath=['//p', '//h1']) == '42'
    # sanity check
    assert extract(doc()) != ''
    assert extract(doc2()) != ''
    assert extract(doc3()) != ''


if __name__ == '__main__':
    test_filters()
    test_prune_xpath()
