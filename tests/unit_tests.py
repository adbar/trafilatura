# pylint:disable-msg=W1401
"""
Unit tests for the trafilatura library.
"""

import logging
import os
import sys

from unittest.mock import patch

# import pytest
# https://docs.pytest.org/en/latest/


from lxml import etree, html

try:
    import cchardet as chardet
except ImportError:
    import chardet

# language detection
try:
    import cld3
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

import trafilatura.filters
import trafilatura.htmlprocessing
from trafilatura.core import baseline, bare_extraction, extract, handle_formatting, handle_image, handle_paragraphs, handle_quotes, handle_table, handle_textelem, process_record, sanitize_tree, trim
from trafilatura.lru import LRUCache
from trafilatura.filters import check_html_lang, duplicate_test, textfilter
from trafilatura.metadata import METADATA_LIST
from trafilatura.settings import DEFAULT_CONFIG

from trafilatura import utils, xml

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
SAMPLE_META = dict.fromkeys(METADATA_LIST)

ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

MOCK_PAGES = {
'http://exotic_tags': 'exotic_tags.html',
}


def load_mock_page(url, xml_flag=False, langcheck=None, tei_output=False):
    '''load mock page from samples'''
    try:
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = chardet.detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    output_format = 'txt'
    if xml_flag is True:
        output_format = 'xml'
    if tei_output is True:
        output_format = 'tei'
    result = extract(htmlstring, url,
                     record_id='0000',
                     no_fallback=False,
                     output_format=output_format,
                     target_language=langcheck)
    return result


def test_trim():
    '''test string trimming'''
    assert trim('	Test  ') == 'Test'
    assert trim('\t\tTest  Test\r\n') == 'Test Test'
    my_elem = etree.Element('body')
    my_elem.text = 'Test Text'
    assert textfilter(my_elem) is False
    # my_elem.text = 'Tags: Arbeit, Urlaub'
    my_elem.text = 'Instagram'
    assert textfilter(my_elem) is True
    my_elem.text = '\t\t'
    assert textfilter(my_elem) is True
    # sanitize logic
    assert utils.sanitize(None) is None


def test_input():
    '''test if loaded strings/trees are handled properly'''
    assert utils.load_html(123) is None
    assert utils.load_html('<html><body>ÄÖÜ</body></html>') is not None
    assert utils.load_html(b'<html><body>\x2f\x2e\x9f</body></html>') is not None
    #assert utils.load_html(b'0'*int(10e3)) is None
    assert extract(None, 'url', '0000', target_language=None) is None
    # legacy
    assert process_record(None, 'url', '0000', target_language=None) is None


def test_txttocsv():
    mymeta = dict.fromkeys(METADATA_LIST)
    assert utils.txttocsv('', '', mymeta) == 'None\tNone\tNone\tNone\tNone\t\t\n'
    mymeta['title'] = 'Test title'
    mymeta['url'] = 'https://example.org'
    mymeta['hostname'] = 'example.org'
    mymeta['id'] = '1'
    assert utils.txttocsv('Test text', 'Test comment', mymeta) == '1\thttps://example.org\tNone\texample.org\tTest title\tNone\tTest text\tTest comment\n'
    mystring = '<html><body><p>ÄÄÄÄÄÄÄÄÄÄÄÄÄÄ</p></body></html>'
    assert extract(mystring, output_format='csv', config=ZERO_CONFIG) is not None
    assert extract(mystring, output_format='csv', include_comments=False, config=ZERO_CONFIG).endswith('\t\n')
    # test json
    assert extract(mystring, output_format='json', config=ZERO_CONFIG).endswith('}')
    # bare extraction for python
    result = bare_extraction(mystring, config=ZERO_CONFIG)
    assert isinstance(result, dict) and len(result) == 13


def test_exotic_tags(xmloutput=False):
    # cover some edge cases with a specially crafted file
    result = load_mock_page('http://exotic_tags', xml_flag=xmloutput, tei_output=True)
    assert 'Teletype text' in result and 'My new car is silver.' in result
    filepath = os.path.join(TEST_DIR, 'cache', 'exotic_tags_tei.html')
    with open(filepath) as f:
        content = etree.fromstring(f.read())
    res = xml.check_tei(content, 'http://dummy')
    assert etree.tostring(res).startswith(b'<html>\n<text>\n<body>\n<div>\n\n<hi rend="uppercase">Hello</hi>\n<p>Teletype text</p>')
    # misformed HTML declaration
    htmlstring = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 2012"http://www.w3.org/TR/html4/loose.dtd"><html><head></head><body><p>ABC</p></body></html>'
    # outputs '012"http://www.w3.org/TR/html4/loose.dtd">\nABC'
    assert 'ABC' in extract(htmlstring, config=ZERO_CONFIG)
    # quotes
    assert handle_quotes(etree.Element('quote')) is None
    assert handle_table(etree.Element('table')) is None
    # p within p
    element, second = etree.Element('p'), etree.Element('p')
    element.text, second.text = '1st part.', '2nd part.'
    element.append(second)
    converted = handle_paragraphs(element, ['p'], False, ZERO_CONFIG)
    assert etree.tostring(converted) == b'<p>1st part. 2nd part.</p>'
    # delete last <lb>
    third = etree.Element('lb')
    element.append(third)
    assert etree.tostring(converted) == b'<p>1st part. 2nd part.</p>'


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


def test_formatting():
    '''Test HTML formatting conversion and extraction'''
    # simple
    my_document = html.fromstring('<html><body><p><b>This here is in bold font.</b></p></body></html>')
    my_result = extract(my_document, output_format='xml', include_formatting=True, config=ZERO_CONFIG)
    assert '<hi rend="#b">This here is in bold font.</hi>' in my_result
    # nested
    my_document = html.fromstring('<html><body><p><b>This here is in bold and <i>italic</i> font.</b></p></body></html>')
    my_result = extract(my_document, output_format='xml', include_formatting=True, config=ZERO_CONFIG)
    assert '<hi rend="#b">This here is in bold and italic font.</hi>' in my_result
    # empty
    my_document = html.fromstring('<html><body><p><b><i></i></b></p></body></html>')
    my_result = extract(my_document, output_format='xml', include_formatting=True, config=ZERO_CONFIG)
    assert '<main/>' in my_result
    # wild div
    my_document = html.fromstring('<html><body><article><div><strong>Wild text</strong></div></article></body></html>')
    my_result = extract(my_document, output_format='xml', include_formatting=True, config=ZERO_CONFIG)
    assert '<p>' in my_result and '<hi>Wild text</hi>' in my_result  # no rend so far
    my_result = extract(my_document, config=ZERO_CONFIG)
    assert my_result == 'Wild text'
    # links
    doc = html.fromstring('<html><body><p><a href="">Link text</a></p></body></html>')
    my_result = extract(doc, config=ZERO_CONFIG)
    assert my_result == 'Link text'
    # line-breaks
    doc = html.fromstring('<html><body><p><br/></p></body></html>')
    my_result = extract(doc, config=ZERO_CONFIG)
    assert my_result == ''
    doc = html.fromstring('<html><body><p><br/>Here is the text.</p></body></html>')
    my_result = extract(doc, config=ZERO_CONFIG)
    assert my_result == 'Here is the text.'
    # handle formatting tails
    element = etree.Element("hi")
    element.text = 'Here is the text.'
    element.tail = 'And a tail.'
    converted = handle_formatting(element)
    assert etree.tostring(converted) == b'<p><hi>Here is the text.</hi>And a tail.</p>'


def test_baseline():
    _, length, string = baseline('')
    assert (length, string) == (0, '')
    my_document = '<html><body><script type="application/ld+json">{"description":"In letzter Zeit kam man am Begriff \"Hygge\", was so viel wie \"angenehm\" oder \"gemütlich\" bedeutet, ja nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend ...","image":[{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/uncropped-0-0\/7d00b2658fd0a3b19e1b161f4657cc20\/Xw\/ikigai--1-.jpg","width":"2048","height":"1366","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-1280-720\/bf947c7c24167d7c0adae0be10942d57\/Uf\/ikigai--1-.jpg","width":"1280","height":"720","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-938-528\/bf947c7c24167d7c0adae0be10942d57\/JK\/ikigai--1-.jpg","width":"938","height":"528","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/large1x1-622-622\/f5544b7d67e1be04f7729b130e7e0485\/KN\/ikigai--1-.jpg","width":"622","height":"622","@type":"ImageObject"}],"mainEntityOfPage":{"@id":"https:\/\/www.brigitte.de\/liebe\/persoenlichkeit\/ikigai-macht-dich-sofort-gluecklicher--10972896.html","@type":"WebPage"},"headline":"Ikigai macht dich sofort glücklicher!","datePublished":"2019-06-19T14:29:08+0000","dateModified":"2019-06-19T14:29:10+0000","author":{"name":"BRIGITTE.de","@type":"Organization"},"publisher":{"name":"BRIGITTE.de","logo":{"url":"https:\/\/image.brigitte.de\/11476842\/uncropped-0-0\/f19537e97b9189bf0f25ce924168bedb\/kK\/bri-logo-schema-org.png","width":"167","height":"60","@type":"ImageObject"},"@type":"Organization"},"articleBody":"In letzter Zeit kam man am Begriff \"Hygge\" (\"gemütlich\" oder \"angenehm\") nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend Konkurrenz: \"Ikigai\". Bist du glücklich? Schwierige Frage, nicht wahr? Viele von uns müssen da erst mal überlegen.","@type":"NewsArticle"}</script></body></html>'
    _, result, _  = baseline(my_document)
    assert result.startswith('In letzter Zeit kam man') and result.endswith('erst mal überlegen.')
    my_document = '<html><body><article><b>The article consists of this text.</b></article></body></html>'
    _, result, _ = baseline(my_document)
    assert result is not None
    my_document = '<html><body><quote>This is only a quote but it is better than nothing.</quote></body></html>'
    _, result, _ = baseline(my_document)
    assert result is not None


def test_filters():
    '''Test content filtering'''
    if LANGID_FLAG is True:
        # main text
        assert trafilatura.filters.language_filter('Hier ist ein Text auf Deutsch', '', 'de', SAMPLE_META) is False
        assert trafilatura.filters.language_filter('Hier ist ein Text auf Deutsch', '', 'en', SAMPLE_META) is True
        # comments
        assert trafilatura.filters.language_filter('Hier ist ein Text.', 'Die Kommentare sind aber etwas länger.', 'de', SAMPLE_META) is False
    else:
        # no detection
        assert trafilatura.filters.language_filter('Hier ist ein Text.', '', 'en', SAMPLE_META) is False
    # test URL blacklist
    assert trafilatura.extract('<html><head><link rel="canonical" href="https://example.org"/></head><body></body></html>', output_format='xml', url_blacklist={'https://example.org'}) is None
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
    lru_test = LRUCache(maxsize=2)
    trafilatura.filters.LRU_TEST = lru_test
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is None
    # HTML lang filter
    my_p = '<p>In sleep a king, but waking no such matter.</p>'
    assert extract(html.fromstring('<html lang="en-US"><body>' + my_p*50 + '</body></html>'), target_language='en') is not None
    assert extract(html.fromstring('<html lang="en-US"><body>' + my_p*50 + '</body></html>'), target_language='de') is None
    assert check_html_lang(html.fromstring('<html lang="de_DE, en_US"><body></body></html>'), target_language='de') is True
    assert check_html_lang(html.fromstring('<html lang="en"><body></body></html>'), target_language='it') is False
    assert check_html_lang(html.fromstring('<html><head><meta http-equiv="content-language" content="en"></head><body></body></html>'), target_language='en') is True
    assert check_html_lang(html.fromstring('<html><head><meta http-equiv="content-language" content="en"></head><body></body></html>'), target_language='de') is False


def test_external():
    '''Test external components'''
    # remove unwanted elements
    mydoc = html.fromstring('<html><body><footer>Test text</footer></body></html>')
    _, _, mylen = sanitize_tree(mydoc)
    assert mylen == 0
    mydoc = html.fromstring('<html><body><table><th>Test text</th><tr><td>Test</td></tr></table></body></html>')
    _, _, mylen = sanitize_tree(mydoc)
    assert mylen > 0
    # strip fancy tags
    mydoc = html.fromstring('<html><body><p>Text here <fancy>Test text</fancy></p></body></html>')
    mytree, _, _ = sanitize_tree(mydoc)
    assert len(mytree) == 1
    # test langid
    if LANGID_FLAG is True:
        doc = html.fromstring('<html><body>' + '<p>Non è inglese.</p>'*20 + '</body></html>')
        assert extract(doc, no_fallback=False, target_language='en', deduplicate=False) is None


def test_images():
    '''Test image extraction function'''
    mydoc = html.fromstring('<html><body><img src="test.jpg"/></body></html>')
    assert handle_image(html.fromstring('<img src="test.jpg"/>')) is not None
    assert handle_image(html.fromstring('<img data-src="test.jpg" alt="text" title="a title"/>')) is not None
    assert handle_image(html.fromstring('<img other="test.jpg"/>')) is None
    assert utils.is_image_file('test.jpg') is True
    assert utils.is_image_file('test.txt') is False
    assert handle_textelem(etree.Element('graphic'), [], False, DEFAULT_CONFIG) is None
    resources_dir = os.path.join(TEST_DIR, 'resources')
    with open(os.path.join(resources_dir, 'http_sample.html')) as f:
        teststring = f.read()
    assert 'test.jpg Example image' not in extract(teststring)
    assert 'test.jpg Example image' in extract(teststring, include_images=True, no_fallback=True)
    assert '<graphic src="test.jpg" title="Example image"/>' in extract(teststring, include_images=True, no_fallback=True, output_format='xml', config=ZERO_CONFIG)


def test_links():
    '''Test link extraction function'''
    assert handle_textelem(etree.Element('ref'), [], False, DEFAULT_CONFIG) is None
    assert handle_formatting(html.fromstring('<a href="testlink.html">Test link text.</a>')) is not None
    mydoc = html.fromstring('<html><body><p><a href="testlink.html">Test link text.</a></p></body></html>')
    assert 'testlink.html' not in extract(mydoc)
    assert 'testlink.html' in extract(mydoc, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    resources_dir = os.path.join(TEST_DIR, 'resources')
    with open(os.path.join(resources_dir, 'http_sample.html')) as f:
        teststring = f.read()
    assert 'testlink.html' not in extract(teststring, config=ZERO_CONFIG)
    print(extract(teststring, include_links=True, no_fallback=True, config=ZERO_CONFIG))
    assert '[link](testlink.html)' in extract(teststring, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    assert '<ref target="testlink.html">link</ref>' in extract(teststring, include_links=True, no_fallback=True, output_format='xml', config=ZERO_CONFIG)


def test_tei():
    '''test TEI-related functions'''
    # open local resources to avoid redownloading at each run
    resources_dir = os.path.join(TEST_DIR, 'resources')
    with open(os.path.join(resources_dir, 'httpbin_sample.html')) as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result = extract(teststring, "mocked", no_fallback=True, output_format='xmltei', tei_validation=False)
    assert result is not None
    assert xml.validate_tei(etree.fromstring(result)) is True
    assert xml.validate_tei(etree.fromstring(teststring)) is False
    # test with another file
    with open(os.path.join(resources_dir, 'http_sample.html')) as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result = extract(teststring, "mocked", no_fallback=True, output_format='xmltei', tei_validation=False)
    assert result is not None
    assert xml.validate_tei(etree.fromstring(result)) is True
    # include ID in metadata
    result = extract(teststring, "mocked", no_fallback=True, output_format='xmltei', tei_validation=False, record_id='0001')
    assert result is not None
    assert xml.validate_tei(etree.fromstring(result)) is True


def test_htmlprocessing():
    '''test html-related functions'''
    assert trafilatura.htmlprocessing.tree_cleaning(etree.Element('html'), True) is not None
    assert trafilatura.htmlprocessing.prune_html(etree.Element('unwanted')) is not None
    mydoc = html.fromstring('<html><body><table><a href="">Link</a></table><img src="test.jpg"/><u>Underlined</u><tt>True Type</tt><sub>Text</sub><sup>Text</sup></body></html>')
    myconverted = trafilatura.htmlprocessing.convert_tags(mydoc, include_formatting=True, include_tables=True, include_images=True)
    assert myconverted.xpath('.//ref') and myconverted.xpath('.//graphic') and myconverted.xpath('.//hi[@rend="#t"]') and myconverted.xpath('.//table')
    myconverted = trafilatura.htmlprocessing.tree_cleaning(mydoc, include_tables=False, include_images=True)
    assert myconverted.xpath('.//graphic') and not myconverted.xpath('.//table')


def test_fetch():
    '''test URL fetching'''
    assert utils.fetch_url('1234') == ''
    assert utils.fetch_url('https://httpbin.org/status/404') is None
    assert utils.decode_response(b'\x1f\x8babcdef') is not None
    assert utils.fetch_url('https://expired.badssl.com/', no_ssl=True) is not None


if __name__ == '__main__':
    test_trim()
    test_lrucache()
    test_input()
    test_formatting()
    test_exotic_tags()
    test_images()
    test_links()
    test_htmlprocessing()
    test_filters()
    test_baseline()
    test_txttocsv()
    test_external()
    test_fetch()
    test_tei()
