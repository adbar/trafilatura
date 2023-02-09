# pylint:disable-msg=W1401
"""
Unit tests for the trafilatura library.
"""

import logging
import os
import sys

import pytest

from lxml import etree, html

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

# language detection
try:
    import py3langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False


import trafilatura.filters
import trafilatura.htmlprocessing

from trafilatura import bare_extraction, baseline, extract, html2txt, process_record

from trafilatura.core import Extractor, handle_formatting, handle_lists, handle_image, handle_paragraphs, handle_quotes, handle_table, handle_textelem, sanitize_tree, trim
from trafilatura.external import try_justext
from trafilatura.filters import check_html_lang, duplicate_test, textfilter
from trafilatura.lru import LRUCache
from trafilatura.meta import reset_caches
from trafilatura.metadata import Document
from trafilatura.settings import DEFAULT_CONFIG, TAG_CATALOG, use_config

from trafilatura import utils, xml

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')
SAMPLE_META = Document()

ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

NEW_CONFIG = use_config(filename=os.path.join(RESOURCES_DIR, 'newsettings.cfg'))

MOCK_PAGES = {
'http://exotic_tags': 'exotic_tags.html',
}

DEFAULT_OPTIONS = Extractor(*[False]*11)
DEFAULT_OPTIONS.config = DEFAULT_CONFIG


def load_mock_page(url, xml_flag=False, langcheck=None, tei_output=False):
    '''load mock page from samples'''
    try:
        with open(os.path.join(TEST_DIR, 'resources', MOCK_PAGES[url]), 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(os.path.join(TEST_DIR, 'resources', MOCK_PAGES[url]), 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)['encoding']
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
    return extract(htmlstring, url,
                     record_id='0000',
                     no_fallback=False,
                     output_format=output_format,
                     target_language=langcheck)


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
    # non-breaking spaces
    print(utils.sanitize('Test&nbsp;Text'))
    assert utils.sanitize('Test&nbsp;Text') == 'Test Text'
    # clear cache
    # reset caches: examine_date_elements used above
    old_values = trim.cache_info()
    reset_caches()
    assert trim.cache_info() != old_values


def test_input():
    '''test if loaded strings/trees are handled properly'''
    assert utils.is_dubious_html('This is a string.') is True
    htmlstring = "<!DOCTYPE html PUBLIC />\n<html/>"
    beginning = htmlstring[:50].lower()
    assert utils.strip_faulty_doctypes(htmlstring, beginning) == "\n<html/>"
    htmlstring = "<html>\n</html>"
    beginning = htmlstring[:50].lower()
    assert utils.strip_faulty_doctypes(htmlstring, beginning) == htmlstring
    with pytest.raises(TypeError) as err:
        assert utils.load_html(123) is None
    assert 'incompatible' in str(err.value)
    assert utils.load_html('<html><body>ÄÖÜ</body></html>') is not None
    assert utils.load_html(b'<html><body>\x2f\x2e\x9f</body></html>') is not None
    assert utils.load_html('<html><body>\x2f\x2e\x9f</body></html>'.encode('latin-1')) is not None
    #assert utils.load_html(b'0'*int(10e3)) is None
    # old: with pytest.raises(TypeError) as err:
    assert extract(None, 'url', '0000', target_language=None) is None
    # legacy
    assert process_record(None, 'url', '0000', target_language=None) is None
    # GZip
    with open(os.path.join(RESOURCES_DIR, 'webpage.html.gz'), 'rb') as gzfile:
        myinput = gzfile.read()
    assert 'Long story short,' in extract(myinput)

    # unicode normalization
    assert utils.normalize_unicode('A\u0308ffin') != 'A\u0308ffin'
    testresult = extract('<html><body><p>A\u0308ffin</p></body></html>', config=ZERO_CONFIG)
    assert testresult != 'A\u0308ffin' and testresult == 'Äffin'


def test_txttocsv():
    mymeta = Document()
    assert utils.txttocsv('', '', mymeta) == 'None\tNone\tNone\tNone\tNone\tNone\t\t\tNone\n'
    mymeta.title = 'Test title'
    mymeta.url = 'https://example.org'
    mymeta.hostname = 'example.org'
    mymeta.id = '1'
    mymeta.license = 'CC BY-SA'
    mymeta.image = 'https://example.org/image.jpg'
    assert utils.txttocsv('Test text', 'Test comment', mymeta) == '1\thttps://example.org\tNone\texample.org\tTest title\thttps://example.org/image.jpg\tNone\tTest text\tTest comment\tCC BY-SA\n'
    mystring = '<html><body><p>ÄÄÄÄÄÄÄÄÄÄÄÄÄÄ</p></body></html>'
    assert extract(mystring, output_format='csv', config=ZERO_CONFIG) is not None
    assert extract(mystring, output_format='csv', include_comments=False, config=ZERO_CONFIG).endswith('\tNone\n')
    # test json
    result = extract(mystring, output_format='json', config=ZERO_CONFIG)
    assert result.endswith('}') and '"fingerprint":' in result and '"language":' in result
    assert extract(mystring, output_format='json', include_comments=False, config=ZERO_CONFIG).endswith('}')
    # bare extraction for python
    result = bare_extraction(mystring, config=ZERO_CONFIG, as_dict=True)
    assert isinstance(result, dict) and len(result) == 19


def test_exotic_tags(xmloutput=False):
    options = DEFAULT_OPTIONS
    options.config = ZERO_CONFIG
    # cover some edge cases with a specially crafted file
    result = load_mock_page('http://exotic_tags', xml_flag=xmloutput, tei_output=True)
    assert 'Teletype text' in result and 'My new car is silver.' in result
    filepath = os.path.join(TEST_DIR, 'resources', 'exotic_tags_tei.html')
    with open(filepath) as f:
        content = etree.fromstring(f.read())
    res = xml.check_tei(content, 'http://dummy')
    assert etree.tostring(res).startswith(b'<html>\n<text>\n<body>\n<div>\n\n<hi rend="uppercase">Hello</hi>\n<p>Teletype text</p>')
    # misformed HTML declaration
    htmlstring = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 2012"http://www.w3.org/TR/html4/loose.dtd"><html><head></head><body><p>ABC</p></body></html>'
    # outputs '012"http://www.w3.org/TR/html4/loose.dtd">\nABC'
    assert 'ABC' in extract(htmlstring, config=ZERO_CONFIG)
    # quotes
    assert handle_quotes(etree.Element('quote'), options) is None
    assert handle_table(etree.Element('table'), TAG_CATALOG, options) is None
    # p within p
    element, second = etree.Element('p'), etree.Element('p')
    element.text, second.text = '1st part.', '2nd part.'
    element.append(second)
    # delete last <lb>
    element.append(etree.Element('lb'))
    converted = handle_paragraphs(element, ['p'], options)
    assert etree.tostring(converted) == b'<p>1st part. 2nd part.</p>'
    # naked div with <lb>
    assert '1.\n2.\n3.' in extract('<html><body><main><div>1.<br/>2.<br/>3.<br/></div></main></body></html>', no_fallback=True, config=ZERO_CONFIG)
    # HTML5: <details>
    htmlstring = '<html><body><article><details><summary>Epcot Center</summary><p>Epcot is a theme park at Walt Disney World Resort featuring exciting attractions, international pavilions, award-winning fireworks and seasonal special events.</p></details></article></body></html>'
    my_result = extract(htmlstring, no_fallback=True, config=ZERO_CONFIG)
    assert 'Epcot Center' in my_result and 'award-winning fireworks' in my_result
    my_result = extract(htmlstring, no_fallback=False, config=ZERO_CONFIG)
    assert 'Epcot Center' in my_result and 'award-winning fireworks' in my_result
    # edge cases
    htmlstring = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>A weird bug</title>
  </head>
  <body>
      <div>
        <h1>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</h1>
        <h2>Sed et interdum lectus.</h2>
        <p>Quisque molestie nunc eu arcu condimentum fringilla.</p>
        <!-- strong can be changed to b, em, i, u, or kbd -->
        <strong><a></a></strong>
        <h2>Aliquam eget interdum elit, id posuere ipsum.</h2>
        <p>Phasellus lectus erat, hendrerit sed tortor ac, dignissim vehicula metus.</p>
      </div>
  </body>
</html>'''
    assert extract(htmlstring, include_formatting=True, include_links=True, include_images=True) is not None
    htmlstring = '''<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>A weird bug</title>
  </head>
  <body>
    <div id="content">
      <h1>A header</h1>
      <h2>Very specific bug so odd</h2>
      <h3>Nested header</h3>
      <p>Some "hyphenated-word quote" followed by a bit more text line.</p>
      <em><p>em improperly wrapping p here</p></em>
      <p>Text here</p>
    </div>
  </body>
</html>'''
    assert extract(htmlstring, include_formatting=True, include_links=True, include_images=True) is not None
    # comments
    assert extract('<html><body><article><p>text</p><div class="comments"><p>comment</p></div></article></body></html>', include_comments=True, no_fallback=True, config=ZERO_CONFIG).endswith("\ncomment")


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
    options = DEFAULT_OPTIONS

    # trailing <lb>
    my_document = html.fromstring('<html><body><p>This here is the text.<br/></p></body></html>')
    my_result = extract(my_document, output_format='xml', config=ZERO_CONFIG)
    assert 'lb' not in my_result
    # simple formatting
    my_document = html.fromstring('<html><body><p><b>This here is in bold font.</b></p></body></html>')
    my_result = extract(my_document, output_format='xml', include_formatting=True, config=ZERO_CONFIG)
    assert '<hi rend="#b">This here is in bold font.</hi>' in my_result
    # titles as markdown
    my_document = html.fromstring('<html><body><article><h3>Title</h3><p><b>This here is in bold font.</b></p></article></body></html>')
    my_result = extract(my_document, output_format='txt', include_formatting=True, config=ZERO_CONFIG)
    assert my_result == '### Title\n**This here is in bold font.**'
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
    assert '<p>' in my_result and '<hi rend="#b">Wild text</hi>' in my_result  # no rend so far
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
    options.config = ZERO_CONFIG
    converted = handle_formatting(element, options)
    assert etree.tostring(converted) == b'<p><hi>Here is the text.</hi>And a tail.</p>'
    # empty elements
    my_document = html.fromstring('<html><body><div>\t\n</div><div>There is text here.</div></body></html>')
    my_result = extract(my_document, output_format='xml', config=ZERO_CONFIG)
    assert '<main>\n    <p>There is text here.</p>\n  </main>' in my_result
    # lists with links
    my_document = html.fromstring('<html><body><article><ul><li>Number 1</li><li>Number <a href="test.html">2</a></li><li>Number 3</li><p>Test</p></article></body></html>')
    my_result = extract(my_document, output_format='xml', include_links=True, config=ZERO_CONFIG)
    assert '<item>Number <ref target="test.html">2</ref></item>' in my_result

    # XML and Markdown formatting within <p>-tag
    my_document = html.fromstring('<html><body><p><b>bold</b>, <i>italics</i>, <tt>tt</tt>, <strike>deleted</strike>, <u>underlined</u>, <a href="test.html">link</a> and additional text to bypass detection.</p></body></html>')
    my_result = extract(my_document, no_fallback=True, include_formatting=False, config=ZERO_CONFIG)
    # TXT: newline problem here
    assert my_result == 'bold, italics, tt,\ndeleted, underlined, link and additional text to bypass detection.'
    my_result = extract(my_document, output_format='xml', no_fallback=True, include_formatting=True, config=ZERO_CONFIG)
    assert '<p><hi rend="#b">bold</hi>, <hi rend="#i">italics</hi>, <hi rend="#t">tt</hi>, <del>deleted</del>, <hi rend="#u">underlined</hi>, link and additional text to bypass detection.</p>' in my_result
    assert 'rend="#b"' in my_result and 'rend="#i"' in my_result and 'rend="#t"' in my_result and 'rend="#u"' in my_result and '<del>' in my_result
    my_result = extract(my_document, output_format='xml', include_formatting=True, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    assert '<p><hi rend="#b">bold</hi>, <hi rend="#i">italics</hi>, <hi rend="#t">tt</hi>, <del>deleted</del>, <hi rend="#u">underlined</hi>, <ref target="test.html">link</ref> and additional text to bypass detection.</p>' in my_result
    my_result = extract(my_document, output_format='txt', no_fallback=True, include_formatting=True, config=ZERO_CONFIG)
    assert my_result == '**bold**, *italics*, `tt`, ~~deleted~~, __underlined__, link and additional text to bypass detection.'

    # double <p>-elems
    # could be solved by keeping the elements instead of reconstructing them
    my_document = html.fromstring('<html><body><p>AAA, <p>BBB</p>, CCC.</p></body></html>')
    my_result = extract(my_document, output_format='xml', include_formatting=True, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    assert 'AAA' in my_result and 'BBB' in my_result and 'CCC' in my_result

    # line-break following formatting
    my_document = html.fromstring('<html><body><article><p><strong>Staff Review of the Financial Situation</strong><br>Domestic financial conditions remained accommodative over the intermeeting period.</p></article></body></html>')
    my_result = extract(my_document, output_format='txt', no_fallback=True, config=ZERO_CONFIG)
    assert my_result == 'Staff Review of the Financial Situation\nDomestic financial conditions remained accommodative over the intermeeting period.'
    # title with formatting
    my_document = html.fromstring('<html><body><article><h4 id="1theinoperator">1) The <code>in</code> Operator</h4><p>The easiest way to check if a Python string contains a substring is to use the <code>in</code> operator. The <code>in</code> operator is used to check data structures for membership in Python. It returns a Boolean (either <code>True</code> or <code>False</code>) and can be used as follows:</p></article></body></html>')
    my_result = extract(my_document, output_format='xml', no_fallback=True, include_formatting=True, config=ZERO_CONFIG)
    assert '<head rend="h4">1) The <code>in</code> Operator</head>' in my_result and '<p>The easiest way to check if a Python string contains a substring is to use the <code>in</code> operator. The <code>in</code> operator is used to check data structures for membership in Python. It returns a Boolean (either <code>True</code> or <code>False</code>) and can be used as follows:</p>' in my_result


def test_baseline():
    _, string, length = baseline('')
    assert (string, length) == ('', 0)
    my_document = r'<html><body><script type="application/ld+json">{"description":"In letzter Zeit kam man am Begriff \"Hygge\", was so viel wie \"angenehm\" oder \"gemütlich\" bedeutet, ja nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend ...","image":[{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/uncropped-0-0\/7d00b2658fd0a3b19e1b161f4657cc20\/Xw\/ikigai--1-.jpg","width":"2048","height":"1366","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-1280-720\/bf947c7c24167d7c0adae0be10942d57\/Uf\/ikigai--1-.jpg","width":"1280","height":"720","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/16x9-938-528\/bf947c7c24167d7c0adae0be10942d57\/JK\/ikigai--1-.jpg","width":"938","height":"528","@type":"ImageObject"},{"name":"Mit der Ikigai-Methode wirst du glücklicher","url":"https:\/\/image.brigitte.de\/10973004\/large1x1-622-622\/f5544b7d67e1be04f7729b130e7e0485\/KN\/ikigai--1-.jpg","width":"622","height":"622","@type":"ImageObject"}],"mainEntityOfPage":{"@id":"https:\/\/www.brigitte.de\/liebe\/persoenlichkeit\/ikigai-macht-dich-sofort-gluecklicher--10972896.html","@type":"WebPage"},"headline":"Ikigai macht dich sofort glücklicher!","datePublished":"2019-06-19T14:29:08+0000","dateModified":"2019-06-19T14:29:10+0000","author":{"name":"BRIGITTE.de","@type":"Organization"},"publisher":{"name":"BRIGITTE.de","logo":{"url":"https:\/\/image.brigitte.de\/11476842\/uncropped-0-0\/f19537e97b9189bf0f25ce924168bedb\/kK\/bri-logo-schema-org.png","width":"167","height":"60","@type":"ImageObject"},"@type":"Organization"},"articleBody":"In letzter Zeit kam man am Begriff \"Hygge\" (\"gemütlich\" oder \"angenehm\") nicht vorbei. Jetzt macht ihm ein neuer Glücks-Trend Konkurrenz: \"Ikigai\". Bist du glücklich? Schwierige Frage, nicht wahr? Viele von uns müssen da erst mal überlegen.","@type":"NewsArticle"}</script></body></html>'
    _, result, _  = baseline(my_document)
    assert result.startswith('In letzter Zeit kam man') and result.endswith('erst mal überlegen.')
    my_document = '<html><body><article>' + 'The article consists of this text.'*10 + '</article></body></html>'
    _, result, _ = baseline(my_document)
    assert result is not None
    my_document = '<html><body><article><b>The article consists of this text.</b></article></body></html>'
    _, result, _ = baseline(my_document)
    assert result is not None
    my_document = '<html><body><quote>This is only a quote but it is better than nothing.</quote></body></html>'
    _, result, _ = baseline(my_document)
    assert result is not None
    my_document = "<html><body><div>   Document body...   </div><script> console.log('Hello world') </script></body></html>"
    _, result, _ = baseline(my_document)
    assert result == 'Document body...'


def test_html2txt():
    mydoc = "<html><body>Here is the body text</body></html>"
    assert html2txt(mydoc) == "Here is the body text"
    assert html2txt(html.fromstring(mydoc)) == "Here is the body text"


def test_filters():
    '''Test content filtering'''
    if LANGID_FLAG is True:
        # main text
        assert trafilatura.filters.language_filter('Hier ist ein Text auf Deutsch', '', 'de', SAMPLE_META)[0] is False
        assert trafilatura.filters.language_filter('Hier ist ein Text auf Deutsch', '', 'en', SAMPLE_META)[0] is True
        # comments
        assert trafilatura.filters.language_filter('Hier ist ein Text.', 'Die Kommentare sind aber etwas länger.', 'de', SAMPLE_META)[0] is False
        # lang detection on the content
        doc = html.fromstring('<html><body><article><p>How many ages hence/Shall this our lofty scene be acted over,/In states unborn and accents yet unknown!</p></article></body></html>')
        assert extract(doc, config=ZERO_CONFIG, target_language='de') is None
        assert extract(doc, config=ZERO_CONFIG, target_language='en') is not None
    else:
        # no detection
        assert trafilatura.filters.language_filter('Hier ist ein Text.', '', 'en', SAMPLE_META)[0] is False
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
    # paragraph level
    lru_test = LRUCache(maxsize=2)
    trafilatura.filters.LRU_TEST = lru_test
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


def test_external():
    '''Test external components'''
    options = DEFAULT_OPTIONS
    options.tables = True
    # remove unwanted elements
    mydoc = html.fromstring('<html><body><footer>Test text</footer></body></html>')
    _, _, mylen = sanitize_tree(mydoc, options)
    assert mylen == 0
    mydoc = html.fromstring('<html><body><table><th>Test text</th><tr><td>Test</td></tr></table></body></html>')
    _, _, mylen = sanitize_tree(mydoc, options)
    assert mylen > 0
    # strip fancy tags while including links and images
    mydoc = html.fromstring('<html><body><p>Text here <fancy>Test text</fancy><a href="">with a link</a>.</p><img src="test.jpg"/></body></html>')
    mytree, _, _ = sanitize_tree(mydoc, options)
    assert len(mytree) == 1
    mydoc = html.fromstring('<html><body><p>Text here <fancy>Test text</fancy><a href="">with a link</a>.</p><img src="test.jpg"/></body></html>')
    options.links, options.images = True, True
    mytree, _, _ = sanitize_tree(mydoc, options)
    myelems = {element.tag for element in set(mytree.iter())}
    assert 'graphic' in myelems and 'ref' in myelems
    # test langid
    if LANGID_FLAG is True:
        doc = html.fromstring('<html><body>' + '<p>Non è inglese.</p>'*20 + '</body></html>')
        assert extract(doc, no_fallback=False, target_language='en', deduplicate=False) is None
    # no tables
    with open(os.path.join(RESOURCES_DIR, 'apache.html')) as f:
        teststring = f.read()
    assert 'localhost:80' in extract(teststring, no_fallback=False, include_tables=True)
    assert 'localhost:80' not in extract(teststring, no_fallback=False, include_tables=False)
    with open(os.path.join(RESOURCES_DIR, 'scam.html')) as f:
        teststring = f.read()
    assert extract(teststring, no_fallback=True, include_tables=False) == ''
    assert extract(teststring, no_fallback=False, include_tables=False) == ''


def test_images():
    '''Test image extraction function'''
    # file type
    assert utils.is_image_file('test.jpg') is True
    assert utils.is_image_file('test.txt') is False
    # tag with attributes
    assert handle_image(html.fromstring('<img src="test.jpg"/>')) is not None
    assert handle_image(html.fromstring('<img data-src="test.jpg" alt="text" title="a title"/>')) is not None
    assert handle_image(html.fromstring('<img other="test.jpg"/>')) is None
    # HTML conversion
    assert handle_textelem(etree.Element('graphic'), [], DEFAULT_OPTIONS) is None
    with open(os.path.join(RESOURCES_DIR, 'http_sample.html')) as f:
        teststring = f.read()
    assert '![Example image](test.jpg)' not in extract(teststring)
    assert '![Example image](test.jpg)' in extract(teststring, include_images=True, no_fallback=True)
    assert '<graphic src="test.jpg" title="Example image"/>' in extract(teststring, include_images=True, no_fallback=True, output_format='xml', config=ZERO_CONFIG)
    assert extract('<html><body><article><img data-src="test.jpg" alt="text" title="a title"/></article></body></html>', include_images=True, no_fallback=True) == '![a title text](test.jpg)'

    # CNN example
    mydoc = html.fromstring('<img class="media__image media__image--responsive" alt="Harry and Meghan last March, in their final royal engagement." data-src-mini="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-169.jpg" data-src-xsmall="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-medium-plus-169.jpg" data-src-small="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-large-169.jpg" data-src-medium="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg" data-src-large="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-super-169.jpg" data-src-full16x9="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-full-169.jpg" data-src-mini1x1="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-11.jpg" data-demand-load="loaded" data-eq-pts="mini: 0, xsmall: 221, small: 308, medium: 461, large: 781" src="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg" data-eq-state="mini xsmall small medium" data-src="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg">')
    myimage = handle_image(mydoc)
    assert myimage is not None and 'alt' in myimage.attrib and 'src' in myimage.attrib
    # modified CNN example
    mydoc = html.fromstring('<img class="media__image media__image--responsive" alt="Harry and Meghan last March, in their final royal engagement." data-src-mini="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-169.jpg" data-src-xsmall="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-medium-plus-169.jpg" data-src-small="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-large-169.jpg" data-src-medium="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg" data-src-large="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-super-169.jpg" data-src-full16x9="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-full-169.jpg" data-src-mini1x1="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-11.jpg" data-demand-load="loaded" data-eq-pts="mini: 0, xsmall: 221, small: 308, medium: 461, large: 781">')
    myimage = handle_image(mydoc)
    assert myimage is not None and 'alt' in myimage.attrib and 'src' in myimage.attrib and myimage.get('src').startswith('http')


def test_links():
    '''Test link extraction function'''
    options = DEFAULT_OPTIONS
    options.config = ZERO_CONFIG
    assert handle_textelem(etree.Element('ref'), [], options) is None
    assert handle_formatting(html.fromstring('<a href="testlink.html">Test link text.</a>'), options) is not None
    # empty link
    mydoc = html.fromstring('<html><body><p><a></a><b>Some text.</b></p></body></html>')
    assert extract(mydoc) is not None
    # link with target
    mydoc = html.fromstring('<html><body><p><a href="testlink.html">Test link text.</a> This part of the text has to be long enough.</p></body></html>')
    assert 'testlink.html' not in extract(mydoc)
    assert '[Test link text.](testlink.html) This part of the text has to be long enough.' in extract(mydoc, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    # link without target
    mydoc = html.fromstring('<html><body><p><a>Test link text.</a> This part of the text has to be long enough.</p></body></html>')
    assert '[Test link text.] This part of the text has to be long enough.' in extract(mydoc, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    mydoc = html.fromstring('<html><body><article><a>Segment 1</a><h1><a>Segment 2</a></h1><p>Segment 3</p></article></body></html>')
    result = extract(mydoc, output_format='xml', include_links=True, no_fallback=True, config=ZERO_CONFIG)
    assert '1' in result and '2' in result and '3' in result
    with open(os.path.join(RESOURCES_DIR, 'http_sample.html')) as f:
        teststring = f.read()
    assert 'testlink.html' not in extract(teststring, config=ZERO_CONFIG)
    assert '[link](testlink.html)' in extract(teststring, include_links=True, no_fallback=True, config=ZERO_CONFIG)
    assert '<ref target="testlink.html">link</ref>' in extract(teststring, include_links=True, no_fallback=True, output_format='xml', config=ZERO_CONFIG)
    # test license link
    mydoc = html.fromstring('<html><body><p>Test text under <a rel="license" href="">CC BY-SA license</a>.</p></body></html>')
    assert 'license="CC BY-SA license"' in extract(mydoc, include_links=True, no_fallback=True, output_format='xml', config=ZERO_CONFIG)


def test_tei():
    '''test TEI-related functions'''
    # open local resources to avoid redownloading at each run
    with open(os.path.join(RESOURCES_DIR, 'httpbin_sample.html')) as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result1 = extract(teststring, "mocked", no_fallback=True, output_format='xmltei', tei_validation=False)
    result2 = extract(teststring, "mocked", no_fallback=True, output_format='xmltei', tei_validation=True)
    assert result1 is not None and result1 == result2
    assert xml.validate_tei(etree.fromstring(result1)) is True
    assert xml.validate_tei(etree.fromstring(teststring)) is False
    # test with another file
    with open(os.path.join(RESOURCES_DIR, 'http_sample.html')) as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result = extract(teststring, "mocked", no_fallback=True, include_comments=True, output_format='xmltei', tei_validation=False)
    assert result is not None # and '<p>license</p>' in result
    assert xml.validate_tei(etree.fromstring(result)) is True
    result = extract(teststring, "mocked", no_fallback=True, include_comments=False, output_format='xmltei', tei_validation=False)
    assert result is not None # and '<p>license</p>' in result
    assert xml.validate_tei(etree.fromstring(result)) is True
    # include ID in metadata
    result = extract(teststring, "mocked", no_fallback=True, output_format='xmltei', tei_validation=False, record_id='0001')
    assert result is not None
    assert xml.validate_tei(etree.fromstring(result)) is True
    # test header + metadata
    tei = etree.Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
    header = etree.SubElement(tei, 'teiHeader')
    docmeta = Document()
    docmeta.categories, docmeta.tags = [], []
    docmeta.title = 'Title'
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.sitename = 'Site Name'
    docmeta.date = '2021-01-01'
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.date = None
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.hostname = 'hostname'
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.sitename = None
    docmeta.license = 'CC BY-SA'
    docmeta.url = 'https://test.org/'
    docmeta.categories = ['cat1', 'cat2']
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.date = '2021-01-01'
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.title, docmeta.sitename = None, None
    assert xml.write_fullheader(header, docmeta) is not None
    xml_doc = etree.fromstring("<TEI><text><body><div>text</div></body></text></TEI>")
    cleaned = xml.check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text) for elem in cleaned.find(".//div").iter()]
    expected = [("div", None), ("p", "text")]
    assert result == expected
    xml_doc = etree.fromstring("<TEI><text><body><div><div>text1<p>text2</p></div></div></body></text></TEI>")
    cleaned = xml.check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text) for elem in cleaned.find(".//div").iter()]
    expected = [("div", None), ("div", None), ("p", "text1 text2")]
    assert result == expected
    xml_doc = etree.fromstring("<TEI><text><body><div><div>text1<head>text2</head></div></div></body></text></TEI>")
    cleaned = xml.check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text) for elem in cleaned.find(".//div").iter()]
    expected = [("div", None), ("div", None), ("p", "text1"), ("ab", "text2")]
    assert result == expected
    xml_doc = etree.fromstring("<TEI><text><body><div><div>text1<p>text2</p></div>has to be there</div></body></text></TEI>")
    cleaned = xml.check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text, elem.tail) for elem in cleaned.find(".//div/div").iter()]
    expected = [("div", None, None), ("p", "text1 text2 has to be there", None)]
    assert result == expected
    xml_doc = etree.fromstring("<TEI><text><body><div><div>text1<quote>text2</quote></div>has to be there</div></body></text></TEI>")
    cleaned = xml.check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text, elem.tail) for elem in cleaned.find(".//div/div").iter()]
    expected = [("div", None, None), ("p", "text1", None), ("quote", "text2", None), ("p", "has to be there", None)]
    assert result == expected
    xml_doc = etree.fromstring("<TEI><text><body><div><div>text1<p>text2</p>has to be there</div></div></body></text></TEI>")
    cleaned = xml.check_tei(xml_doc, "fake_url")
    result = [(elem.tag, elem.text, elem.tail) for elem in cleaned.find(".//div/div").iter()]
    expected = [("div", None, None), ("p", "text1 text2 has to be there", None)]
    assert result == expected
    htmlstring = html.fromstring("<html><head/><body><div><h2><p>text</p></h2></div></body></html>")
    extracted = extract(htmlstring, url='mocked', no_fallback=True, output_format="xmltei")
    assert xml.validate_tei(etree.fromstring(extracted)) is True
    htmlstring  = html.fromstring("<html><body><article><h1>title</h1><h2>subtitle</h2><p>text</p></article></body></html>")
    extracted = extract(htmlstring, url="mocked", no_fallback=True, output_format="xmltei")
    assert '<ab rend="h1" type="header">title</ab>' in extracted
    assert '<ab rend="h2" type="header">subtitle</ab>' in extracted
    htmlstring = html.fromstring(
    """<html>
        <body><article>
            <h2><div>
              <p>content</p>
              <ul>
                <li>text1</li>
                <li>text2</li>
              </ul>
            </div></h2>
        </article></body>
        </html>"""
    )
    extracted = extract(htmlstring, url="mocked", no_fallback=True, output_format="xmltei")
    assert '<ab rend="h2" type="header">content<list rend="ul"><item>text1' in extracted.replace("\n", "")
    # merge double elements
    tree = html.fromstring(
    """<html>
        <body>
            <p><p>
              <span><p>content</p></span>
            </p></p>
        </body>
        </html>"""
    )
    tree = xml.remove_empty_elements(xml.strip_double_tags(tree))
    result = utils.sanitize(etree.tostring(tree, encoding="unicode")).replace("\n", "")
    assert result == "<html><body><p><span>content</span></p></body></html>"
    tree = html.fromstring(
    """
    <html>
        <body>
            <div>
                <div>
                    <p>
                        <p>text</p>
                    <p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    xml.strip_double_tags(tree)
    assert tree.find(".//div/div") is not None and tree.find(".//p/p") is None
    tree = etree.XML(
    """
    <html><body>
        <div>
            <p>text1<lb/>text2<p>text3</p><lb/>text4</p>
            <p>text5<p>text6</p></p>
        </div>
    </body></html>
    """
    )
    xml.strip_double_tags(tree)
    assert tree.find(".//p/p") is None
    tree = etree.XML(
    """
    <html><body>
        <div>
            <p>text1<lb/>text2<p>text3</p><lb/>text4</p>
            <p>text5<p>text6<p>text7</p></p></p>
        </div>
    </body></html>
    """
    )
    xml.strip_double_tags(tree)
    assert tree.find(".//p/p") is None
    assert "text7" in etree.tostring(tree, encoding="unicode")
    # nested elements with same tag not merged
    tree = html.fromstring(
    """<html>
        <body>
            <div>
                <p>
                  <list>
                    <item>
                        <p>text</p>
                    </item>
                  </list>
                </p>
                <p>
                    <table>
                      <row>
                        <cell>
                          <p>text1</p>
                         </cell>
                      </row>
                    </table>
                </p>
                <p>
                    <note>
                      <p>text2</p>
                    </note>
                </p>
                <p>
                    <quote>
                        <p>text3</p>
                    </quote>
                </p>
                <p>
                    <figure>
                        <p>text4</p>
                    </figure>
                </p>
            </div>
        </body>
    </html>"""
    )
    xml.strip_double_tags(tree)
    for parent_tag in ["item", "cell", "quote", "note", "figure"]:
        assert tree.find(f".//{parent_tag}/p") is not None


def test_htmlprocessing():
    '''test html-related functions'''
    options = DEFAULT_OPTIONS
    options.tables = True
    assert trafilatura.htmlprocessing.tree_cleaning(etree.Element('html'), options) is not None
    assert trafilatura.htmlprocessing.prune_html(etree.Element('unwanted')) is not None
    mydoc = html.fromstring('<html><body><table><a href="">Link</a></table><img src="test.jpg"/><u>Underlined</u><tt>True Type</tt><sub>Text</sub><sup>Text</sup></body></html>')
    options.formatting, options.images, options.links = True, True, True
    myconverted = trafilatura.htmlprocessing.convert_tags(mydoc, options)
    assert myconverted.xpath('.//ref') and myconverted.xpath('.//graphic') and myconverted.xpath('.//hi[@rend="#t"]') and myconverted.xpath('.//table')
    options.images, options.tables = True, False
    myconverted = trafilatura.htmlprocessing.tree_cleaning(mydoc, options)
    assert myconverted.xpath('.//graphic') and not myconverted.xpath('.//table')
    mydoc = html.fromstring('<html><body><article><h1>Test headline</h1><p>Test</p></article></body></html>')
    assert '<head rend="h1">Test headline</head>' in extract(mydoc, output_format='xml', config=ZERO_CONFIG, no_fallback=True)
    assert '<ab rend="h1" type="header">Test headline</ab>' in extract(mydoc, output_format='xmltei', config=ZERO_CONFIG, no_fallback=True)
    # merge with parent function
    element = etree.Element('test')
    xml.merge_with_parent(element)
    mydoc = html.fromstring('<html><body><p><span>A</span><span>B</span><span>C</span></p></body></html>')
    for element in mydoc.iter('span'):
        xml.merge_with_parent(element)
    assert b'<p>A B C</p>' in etree.tostring(mydoc)
    mydoc = html.fromstring('<html><body><p><span>A</span><span>B</span> tail<span>C</span></p></body></html>')
    for element in mydoc.iter('span'):
        xml.merge_with_parent(element)
    assert b'<p>A B tail C</p>' in etree.tostring(mydoc)
    # paywalls
    my_html = '<html><body><main><p>1</p><p id="paywall">2</p><p>3</p></main></body></html>'
    assert extract(my_html, config=ZERO_CONFIG, no_fallback=True) == '1\n3'
    assert extract(my_html, config=ZERO_CONFIG, no_fallback=False) == '1\n3'
    # test tail of node deleted if set as text
    node = etree.fromstring("<div><p></p>tail</div>")[0]
    trafilatura.htmlprocessing.process_node(node, options)
    assert node.text == 'tail'
    assert node.tail is None
    node = etree.fromstring("<list><item></item>text in tail</list>")[0]
    trafilatura.htmlprocessing.process_node(node, options)
    assert node.text == "text in tail"
    assert node.tail is None
    line_break = etree.fromstring("<p><lb/>tail</p>")[0]
    trafilatura.htmlprocessing.process_node(line_break, options)
    assert line_break.text is None
    assert line_break.tail == "tail"
    node = etree.fromstring("<div><p>some text</p>tail</div>")[0]
    trafilatura.htmlprocessing.process_node(node, options)
    assert node.text == "some text"
    assert node.tail == "tail"


def test_extraction_options():
    '''Test the different parameters available in extract() and bare_extraction()'''
    my_html = '<html><head><meta http-equiv="content-language" content="EN"/></head><body><div="article-body"><p>Text.<!-- comment --></p></div></body></html>'
    with pytest.raises(NameError) as err:
        extract(my_html, json_output=True)
    assert extract(my_html, config=NEW_CONFIG) is None
    assert extract(my_html, config=ZERO_CONFIG) is not None
    assert extract(my_html, with_metadata=True, output_format='xml', config=ZERO_CONFIG) is None
    assert extract(my_html, only_with_metadata=True, output_format='xml', config=ZERO_CONFIG) is None
    assert extract(my_html, target_language='de', config=ZERO_CONFIG) is None
    assert etree.tostring(try_justext(html.fromstring(my_html), None, 'de')) == b'<body/>'
    # assert extract(my_html) is None


def test_precision_recall():
    '''test precision- and recall-oriented settings'''
    # the test cases could be better
    my_document = html.fromstring('<html><body><p>This here is the text.</p></body></html>')
    assert extract(my_document, favor_precision=True, config=ZERO_CONFIG, fast=True) is not None
    assert extract(my_document, favor_recall=True, config=ZERO_CONFIG, fast=True) is not None
    my_document = html.fromstring('<html><body><div class="article-body"><div class="teaser-content"><p>This here is a teaser text.</p></div><div><p>This here is the text.</p></div></body></html>')
    assert 'teaser text' in extract(my_document, favor_recall=True, config=ZERO_CONFIG, fast=True)
    assert 'teaser text' not in extract(my_document, config=ZERO_CONFIG, fast=True)
    assert 'teaser text' not in extract(my_document, favor_precision=True, config=ZERO_CONFIG, fast=True)
    my_document = html.fromstring('<html><body><article><div><p><a href="test.html">1.</a><br/><a href="test2.html">2.</a></p></div></article></body></html>')
    result = extract(my_document, favor_recall=True, config=ZERO_CONFIG, fast=True)
    assert '1' not in result
    result = extract(my_document, favor_precision=True, config=ZERO_CONFIG, fast=True)
    assert '1' not in result
    my_document = html.fromstring('<html><body><div class="article-body"><p>content</p><h2>Test</h2></div></body></html>')
    result = extract(my_document, favor_precision=True, config=ZERO_CONFIG, fast=True)
    assert 'content' in result and 'Test' not in result


def test_table_processing():
    options = DEFAULT_OPTIONS
    table_simple_cell = html.fromstring(
        "<table><tr><td>cell1</td><td>cell2</td></tr><tr><td>cell3</td><td>cell4</td></tr></table>"
    )
    processed_table = handle_table(table_simple_cell, TAG_CATALOG, options)
    result = [(child.tag, child.text) for child in processed_table.iter()]
    assert result == [
        ("table", None),
        ("row", None),
        ("cell", "cell1"),
        ("cell", "cell2"),
        ("row", None),
        ("cell", "cell3"),
        ("cell", "cell4"),
    ]
    # if a cell contains 'exotic' tags, they are cleaned during the extraction
    # process and the content is merged with the parent e.g. <td>
    table_cell_with_children = html.fromstring(
        "<table><tr><td><p>text</p><p>more text</p></td></tr></table>"
    )
    processed_table = handle_table(table_cell_with_children, TAG_CATALOG, options)
    assert (
        etree.tostring(processed_table, encoding="unicode")
        == "<table><row><cell><p>text</p><p>more text</p></cell></row></table>"
    )
    # complex table that hasn't been cleaned yet
    htmlstring = html.fromstring(
        """<html>
              <body><article>
                <table>
                  <tbody>
                    <tr>
                      <td>
                        <small>text<br></small>
                        <h4>more_text</h4>
                      </td>
                      <td><a href='link'>linktext</a></td>
                    </tr>
                  </tbody>
                </table>
              </article></body>
            </html>"""
    )
    processed = extract(
        htmlstring, no_fallback=True, output_format='xml', config=DEFAULT_CONFIG, include_links=True
    )
    result = processed.replace('\n', '').replace(' ', '')
    assert """<table><row><cell>text<head>more_text</head></cell></row></table>""" in result
    table_cell_w_text_and_child = html.fromstring(
        "<table><tr><td>text<lb/><p>more text</p></td></tr></table>"
    )
    processed_table = handle_table(
        table_cell_w_text_and_child, TAG_CATALOG, options
    )
    assert (
        etree.tostring(processed_table, encoding="unicode")
        == "<table><row><cell>text<p>more text</p></cell></row></table>"
    )
    table_cell_with_link = html.fromstring(
        "<table><tr><td><ref='test'>link</ref></td></tr></table>"
    )
    processed_table = handle_table(table_cell_with_link, TAG_CATALOG, options)
    result = [child.tag for child in processed_table.find(".//cell").iterdescendants()]
    assert result == ["p"]
    table_with_head = html.fromstring(
        """<table>
      <tr>
        <th>Month</th>
        <th>Days</th>
      </tr>
      <tr>
        <td>January</td>
        <td>31</td>
      </tr>
      <tr>
        <td>February</td>
        <td>28</td>
      </tr>
    </table>"""
    )
    processed_table = handle_table(
        table_with_head, TAG_CATALOG, options
    )
    first_row = processed_table[0]
    assert len(processed_table) == 3
    assert [
        (child.tag, child.attrib, child.text) for child in first_row.iterdescendants()
    ] == [("cell", {"role": "head"}, "Month"), ("cell", {"role": "head"}, "Days")]
    table_with_head_spanning_two_cols = html.fromstring(
        """<table>
      <tr>
        <th>Name</th>
        <th>Adress</th>
        <th colspan="2">Phone</th>
      </tr>
      <tr>
        <td>Jane Doe</td>
        <td>test@example.com</td>
        <td>phone 1</td>
        <td>phone 2</td>
      </tr>
    </table>"""
    )
    processed_table = handle_table(
        table_with_head_spanning_two_cols,
        TAG_CATALOG,
        options,
    )
    first_row = processed_table[0]
    assert len(first_row) == 3
    assert {child.tag for child in first_row.iterdescendants()} == {"cell"}
    table_cell_with_hi = html.fromstring(
        "<table><tr><td><hi>highlighted text</hi></td></tr></table>"
    )
    processed_table = handle_table(table_cell_with_hi, TAG_CATALOG, options)
    result = etree.tostring(processed_table.find(".//cell"), encoding="unicode")
    assert result == "<cell><hi>highlighted text</hi></cell>"
    table_cell_with_span = html.fromstring(
        "<table><tr><td><span style='sth'>span text</span></td></tr></table>"
    )
    processed_table = handle_table(table_cell_with_span, TAG_CATALOG, options)
    result = etree.tostring(processed_table.find(".//cell"), encoding="unicode")
    assert result == "<cell><p/></cell>"
    # tables with nested elements
    htmlstring = '''<html><body><article>
<table>
<tr><td><b>Present Tense</b></td>
<td>I buy</td>
<td>you buy</td>
<td>he/she/it buys</td>
<td>we buy</td>
<td>you buy</td>
<td>they buy</td>
</tr>
    </table></article></body></html>'''
    my_result = extract(htmlstring, no_fallback=True, output_format='xml', include_formatting=True, config=ZERO_CONFIG)
    assert '''<row>
        <cell>
          <hi>Present Tense</hi>
        </cell>
        <cell>I buy</cell>
        <cell>you buy</cell>
        <cell>he/she/it buys</cell>
        <cell>we buy</cell>
        <cell>you buy</cell>
        <cell>they buy</cell>
      </row>''' in my_result
    # table with links
    # todo: further tests and adjustsments
    htmlstring = '<html><body><article><table><tr><td><a href="test.html">' + 'ABCD'*100 + '</a></td></tr></table></article></body></html>'
    result = extract(htmlstring, no_fallback=True, output_format='xml', config=ZERO_CONFIG, include_tables=True, include_links=True)
    assert 'ABCD' not in result
    # nested table
    htmlstring = '<html><body><article><table><th>1</th><table><tr><td>2</td></tr></table></table></article></body></html>'
    result = extract(htmlstring, no_fallback=True, output_format='xml', config=ZERO_CONFIG, include_tables=True)
    # todo: all elements are there, but output not nested
    assert '<cell role="head">1</cell>' in result and '<cell>2</cell>' in result
    nested_table = html.fromstring(
        """
        <table>
        <tr>
        <td>
          <table><tr><td>1</td></tr></table>
        </td>
        </tr>
        </table>"""
    )
    processed_table = handle_table(nested_table, TAG_CATALOG, options)
    result = [
        (el.tag, el.text) if el.text is not None and el.text.strip() else el.tag
        for el in processed_table.iter()
    ]
    #assert result == ["table", "row", "cell", "table", "row", ("cell", "1")]
    assert result == ["table", "row", "cell", ("cell", "1")]
    complex_nested_table = html.fromstring(
    """
    <table>
    <tr>
    <td>
      <table><tr><td>1</td></tr></table>
    </td>
    <td>text1</td>
    </tr>
    <tr><td>text2</td></tr>
    </table>"""
    )
    processed_table = handle_table(complex_nested_table, TAG_CATALOG, options)
    result = [
        (el.tag, el.text) if el.text is not None and el.text.strip() else el.tag
        for el in processed_table.iter()
    ]
    #assert (
    #        result
    #        == ["table", "row", "cell", "table", "row", ("cell", "1"), ("cell", "text1"), "row", ("cell", "text2")]
    #)
    assert result == ['table', 'row', 'cell', ('cell', '1'), ('cell', 'text1'), 'row', ('cell', 'text2')]
    table_with_list = html.fromstring(
    """
    <table><tr><td>
    <p>a list</p>
    <list>
      <item>one</item>
      <item>two</item>
    </list>
    </td>
    </tr></table>
    """)
    processed_table = handle_table(table_with_list, TAG_CATALOG, options)
    result = [
        (el.tag, el.text) if el.text is not None and el.text.strip() else el.tag
        for el in processed_table.iter()
    ]
    # assert result == ["table", "row", "cell", ("p", "a list"), "list", ("item", "one"), ("item", "two"),]
    assert result == ['table', 'row', 'cell', ('p', 'a list'), 'list']
    broken_table = html.fromstring("<table><td>cell1</td><tr><td>cell2</td></tr></table>")
    processed_table = handle_table(broken_table, TAG_CATALOG, options)
    result = [el.tag for el in processed_table.iter()]
    assert result == ['table', 'row', 'cell', 'row', 'cell']
    broken_table = html.fromstring("<table><tr><p>text</p></tr><tr><td>cell</td></tr></table>")
    processed_table = handle_table(broken_table, TAG_CATALOG, options)
    result = [el.tag for el in processed_table.iter()]
    assert result == ["table", "row", "cell", ]


def test_list_processing():
    options = DEFAULT_OPTIONS
    # malformed lists (common error)
    result = etree.tostring(handle_lists(etree.fromstring('<list>Description of the list:<item>List item 1</item><item>List item 2</item><item>List item 3</item></list>'), options))
    assert result.count(b'List item') == 3
    assert b"Description" in result
    # nested list
    htmlstring = '''<html><body><article>
<ul>
  <li>Coffee</li>
  <li>Tea
    <ul>
      <li>Black tea</li>
      <li>Green tea</li>
    </ul>
  </li>
  <li>Milk</li>
</ul>
</article></body></html>'''
    my_result = extract(htmlstring, no_fallback=True, output_format='xml', config=ZERO_CONFIG)
    expected = '''
    <list rend="ul">
      <item>Coffee</item>
      <item>Tea
        <list rend="ul">
          <item>Black tea</item>
          <item>Green tea</item>
        </list>
      </item>
      <item>Milk</item>
    </list>'''.replace("\n", "").replace(" ", "")
    assert expected in my_result.replace("\n", "").replace(" ", "")
    # description list
    htmlstring = '''<html><body><article>
 <dl>
  <dt>Coffee</dt>
  <dd>Black hot drink</dd>
  <dt>Milk</dt>
  <dd>White cold drink</dd>
</dl>
</article></body></html>'''
    my_result = extract(htmlstring, no_fallback=True, output_format='xml', config=ZERO_CONFIG)
    assert '''
    <list rend="dl">
      <item rend="dt-1">Coffee</item>
      <item rend="dd-1">Black hot drink</item>
      <item rend="dt-2">Milk</item>
      <item rend="dd-2">White cold drink</item>
    </list>''' in my_result
    list_item_with_child = html.fromstring("<list><item><p>text</p></item></list>")
    processed_list = handle_lists(list_item_with_child, options)
    result = [(child.tag, child.text) if child.text is not None else child.tag for child in processed_list.iter()]
    assert result == ["list", "item", ("p", "text")]
    list_item_with_text_and_child = html.fromstring("<list><item>text1<p>text2</p></item></list>")
    processed_list = handle_lists(list_item_with_text_and_child, options)
    result = [(child.tag, child.text) if child.text is not None else child.tag for child in processed_list.iter()]
    assert result == ["list", ("item", "text1"), ("p", "text2")]
    list_item_with_lb = html.fromstring("<list><item>text<lb/>more text</item></list>")
    processed_list = handle_lists(list_item_with_lb, options)
    result = [(child.tag, child.text) if child.text is not None else child.tag for child in processed_list.iter()]
    assert result == ["list", ("item", "text"), "lb"]
    list_with_text_outside_item = html.fromstring("<list>header<item>text</item></list>")
    processed_list = handle_lists(list_with_text_outside_item, options)
    result = [(child.tag, child.text) if child.text is not None else child.tag for child in processed_list.iter()]
    assert result == ["list", ("item", "header"), ("item", "text")]
    empty_list = html.fromstring("<list>   <item>text</item></list>")
    processed_list = handle_lists(empty_list, options)
    assert len(processed_list) == 1
    list_item_with_tail = html.fromstring("<list><item>text</item>tail</list>")
    processed_list = handle_lists(list_item_with_tail, options)
    assert processed_list[0].text == "text tail"
    list_item_with_child_and_tail = html.fromstring("<list><item><p>text</p></item>tail</list>")
    processed_list = handle_lists(list_item_with_child_and_tail, options)
    item_element = processed_list[0]
    assert item_element.tail is not True
    assert item_element[0].tail == "tail"
    list_item_with_child_and_tail = html.fromstring("<list><item><p>text</p>tail1</item>tail</list>")
    processed_list = handle_lists(list_item_with_child_and_tail, options)
    item_element = processed_list[0]
    assert item_element.tail is not True
    assert item_element[0].tail == "tail1 tail"
    list_item_with_child_and_tail = html.fromstring("<list><item><p>text</p>\n</item>tail</list>")
    processed_list = handle_lists(list_item_with_child_and_tail, options)
    item_element = processed_list[0]
    assert item_element.tail is not True
    assert item_element[0].tail == "tail"
    list_item_with_tail_and_nested_list = html.fromstring("<list><item><list><item>text</item></list></item>tail</list>")
    processed_list = handle_lists(list_item_with_tail_and_nested_list, options)
    target_element = processed_list.find(".//item/list")
    assert target_element.tail == 'tail'


if __name__ == '__main__':
    test_trim()
    test_lrucache()
    test_input()
    test_formatting()
    test_exotic_tags()
    test_images()
    test_links()
    test_htmlprocessing()
    test_extraction_options()
    test_precision_recall()
    test_filters()
    test_baseline()
    test_txttocsv()
    test_external()
    test_tei()
    test_table_processing()
    test_list_processing()
