# pylint:disable-msg=I1101,W1401
"""
Unit tests for the trafilatura library.
"""

import logging
import sys
import time

from copy import copy
from os import path
from unittest.mock import patch

import pytest

from lxml import etree, html


try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

import trafilatura.htmlprocessing
from trafilatura import bare_extraction, baseline, extract, extract_with_metadata, xml
from trafilatura import core
from trafilatura.external import sanitize_tree, try_justext, try_readability
from trafilatura.main_extractor import (
    _span,
    handle_formatting,
    handle_image,
    handle_lists,
    handle_paragraphs,
    handle_quotes,
    handle_table,
    handle_textelem,
)
from trafilatura.meta import reset_caches
from trafilatura.metadata import Document
from trafilatura.readability_lxml import is_probably_readerable
from trafilatura.settings import TAG_CATALOG, use_config
from trafilatura.deduplication import LRU_TEST
from trafilatura.utils import (
    LANGID_FLAG,
    detect_encoding,
    is_dubious_html,
    is_image_file,
    is_in_table_cell,
    language_classifier,
    line_processing,
    load_html,
    normalize_unicode,
    repair_faulty_html,
    return_printables_and_spaces,
    sanitize,
    textfilter,
    trim,
)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


TEST_DIR = path.abspath(path.dirname(__file__))
RESOURCES_DIR = path.join(TEST_DIR, "resources")
SAMPLE_META = Document()

ZERO_CONFIG = use_config()  # fresh copy: must not mutate the package-global DEFAULT_CONFIG
ZERO_CONFIG["DEFAULT"]["MIN_OUTPUT_SIZE"] = "0"
ZERO_CONFIG["DEFAULT"]["MIN_EXTRACTED_SIZE"] = "0"

NEW_CONFIG = use_config(filename=path.join(RESOURCES_DIR, "newsettings.cfg"))


_INTRO = "enough intro text here for extraction"


def _extract_doc(body, *, intro=True, **kwargs):
    "Wrap body in an article doc and extract; config defaults to ZERO_CONFIG (min-sizes 0)."
    kwargs.setdefault("config", ZERO_CONFIG)
    inner = f"<p>{_INTRO}</p>{body}" if intro else body
    return extract(f"<html><body><article>{inner}</article></body></html>", **kwargs)


def _table_md(table, **kwargs):
    return _extract_doc(table, output_format="markdown", include_tables=True, **kwargs)


def _table_txt(table):
    return _extract_doc(table, intro=False, output_format="txt", fast=True, include_tables=True)


def _md_inline(body, **kwargs):
    return _extract_doc(body, output_format="markdown", include_formatting=True, **kwargs) or ""


MOCK_PAGES = {
    "http://exotic_tags": "exotic_tags.html",
}


@pytest.fixture
def options():
    "A fresh Extractor per test (never a shared, mutable module global)."
    return core.Extractor()


def load_mock_page(url, xml_flag=False, langcheck=None, tei_output=False):
    """load mock page from samples"""
    try:
        with open(path.join(TEST_DIR, "resources", MOCK_PAGES[url]), "r", encoding="utf-8") as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(path.join(TEST_DIR, "resources", MOCK_PAGES[url]), "rb") as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)["encoding"]
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print("Encoding error")
    if xml_flag:
        output_format = "xml"
    elif tei_output:
        output_format = "xmltei"
    else:
        output_format = "txt"
    return extract(htmlstring, url, record_id="0000", output_format=output_format, target_language=langcheck)


def test_trim():
    """test string trimming"""
    assert trim("	Test  ") == "Test"
    assert trim("\t\tTest  Test\r\n") == "Test Test"
    my_elem = etree.Element("body")
    my_elem.text = "Test Text"
    assert textfilter(my_elem) is False
    # my_elem.text = 'Tags: Arbeit, Urlaub'
    my_elem.text = "Instagram"
    assert textfilter(my_elem) is True
    my_elem.text = "\t\t"
    assert textfilter(my_elem) is True
    # sanitize logic
    assert sanitize(None) is None
    # non-breaking spaces
    assert sanitize("Test&nbsp;Text") == "Test Text"
    # clear cache
    # reset caches: examine_date_elements used above
    old_values = trim.cache_info()
    reset_caches()
    assert trim.cache_info() != old_values


def test_reset_caches():
    "reset_caches() must empty every trafilatura-owned cache, not just trim."
    caches = (trim, line_processing, return_printables_and_spaces)
    for fn in caches:
        fn("x")
    LRU_TEST.put("k", 1)
    assert all(fn.cache_info().currsize for fn in caches) and LRU_TEST.cache
    reset_caches()
    assert not any(fn.cache_info().currsize for fn in caches) and not LRU_TEST.cache


def test_input(options):
    """test if loaded strings/trees are handled properly"""
    teststring = "高山云雾出好茶".encode("utf-8")
    assert detect_encoding(teststring) == ["utf-8"]
    teststring = "高山云雾出好茶".encode("gb18030")
    assert "gb18030" in detect_encoding(teststring)
    assert "gb18030" in detect_encoding(teststring * 1000)

    assert is_dubious_html("This is a string.") is True

    htmlstring = "<!DOCTYPE html PUBLIC />\n<html></html>"
    beginning = htmlstring[:50].lower()
    assert repair_faulty_html(htmlstring, beginning) == "\n<html></html>"

    htmlstring = "<html>\n</html>"
    beginning = htmlstring[:50].lower()
    assert repair_faulty_html(htmlstring, beginning) == htmlstring

    htmlstring = "<html/>\n</html>"
    beginning = htmlstring[:50].lower()
    assert repair_faulty_html(htmlstring, beginning) == "<html>\n</html>"

    htmlstring = '<!DOCTYPE html>\n<html lang="en-US"/>\n<head/>\n<body/>\n</html>'
    beginning = htmlstring[:50].lower()
    assert repair_faulty_html(htmlstring, beginning) == '<!DOCTYPE html>\n<html lang="en-US">\n<head/>\n<body/>\n</html>'

    htmlstring = "<!DOCTYPE html><html><head></head><body>Foo <br/> Bar</body></html>"
    beginning = htmlstring[:50].lower()
    assert repair_faulty_html(htmlstring, beginning) == "<!DOCTYPE html><html><head></head><body>Foo <br/> Bar</body></html>\n"

    # XML-illegal chars are stripped pre-parse (see utils.INVALID_XML_CHARS)
    htmlstring = "<html><body><p>a\x00b\x1dc￾￿d</p>\t<p>keep\tme</p></body></html>"
    assert repair_faulty_html(htmlstring, htmlstring[:50].lower()) == "<html><body><p>abcd</p>\t<p>keep\tme</p></body></html>"
    page = (
        "<html><body><article>"
        + "<p>Long enough article paragraph\x1d for baseline￿ to trigger.</p>" * 3
        + "</article></body></html>"
    )
    assert baseline(page)[2] > 0  # no ValueError, control chars stripped
    assert extract(page, fast=True) is not None

    with pytest.raises(TypeError) as err:
        assert load_html(123) is None
    assert "incompatible" in str(err.value)

    assert load_html("<html><body>ÄÖÜ</body></html>") is not None
    assert load_html(b"<html><body>\x2f\x2e\x9f</body></html>") is not None
    assert load_html("<html><body>\x2f\x2e\x9f</body></html>".encode("latin-1")) is not None
    # assert load_html(b'0'*int(10e3)) is None
    # old: with pytest.raises(TypeError) as err:
    assert extract(None, "url", "0000", target_language=None) is None
    # GZip
    with open(path.join(RESOURCES_DIR, "webpage.html.gz"), "rb") as gzfile:
        myinput = gzfile.read()
    assert "Long story short," in extract(myinput)

    # responses exposing a .data attribute are unwrapped
    class _RespLike:
        data = b"<html><body><p>response data</p></body></html>"

    assert load_html(_RespLike()) is not None

    # unicode normalization
    assert normalize_unicode("A\u0308ffin") != "A\u0308ffin"
    testresult = extract("<html><body><p>A\u0308ffin</p></body></html>", config=ZERO_CONFIG)
    assert testresult != "A\u0308ffin" and testresult == "Äffin"
    options = core.Extractor(source="test\udcc3this")
    assert options.source == "test?this"

    # output format
    assert "ABC" in extract("<html><body><p>ABC</p></body></html>", output_format="xml")
    with pytest.raises(AttributeError):
        assert extract("<html><body><p>ABC</p></body></html>", output_format="xyz") is not None
    assert bare_extraction("<html><body><p>ABC</p></body></html>", output_format="python").text == "ABC"
    with pytest.raises(AttributeError):
        assert bare_extraction("<html><body><p>ABC</p></body></html>", output_format="xyz") is not None

    # text elements
    elem = etree.Element("p")
    elem.text = "text"
    assert handle_textelem(elem, [], options).text == "text"
    elem = etree.Element("unexpected")
    elem.text = "text"
    assert handle_textelem(elem, [], options) is None


def test_document_isolation():
    "Documents must not share a mutable Element default (thread-safety / correctness)."
    d1, d2 = Document(), Document()
    assert d1.body is not d2.body
    assert d1.commentsbody is not d2.commentsbody
    assert d1.body.tag == "body" and len(d1.body) == 0


def test_xmltocsv():
    doc = Document()
    doc.body = etree.fromstring("<xml/>")
    doc.commentsbody = etree.fromstring("<xml/>")
    assert xml.xmltocsv(doc, False) == "null\tnull\tnull\tnull\tnull\tnull\tnull\tnull\tnull\tnull\tnull\r\n"

    doc.title = "Test title"
    doc.url = "https://example.org"
    doc.hostname = "example.org"
    doc.id = "1"
    doc.license = "CC BY-SA"
    doc.image = "https://example.org/image.jpg"
    doc.pagetype = "article"
    text = "Test text"
    comments = "Test comment"
    doc.body = etree.fromstring(f"<p>{text}</p>")
    doc.commentsbody = etree.fromstring(f"<p>{comments}</p>")

    target = "https://example.org\t1\tnull\texample.org\tTest title\thttps://example.org/image.jpg\tnull\tTest text\tTest comment\tCC BY-SA\tarticle\r\n"

    assert xml.xmltocsv(doc, False) == target

    mystring = "<html><body><p>ÄÄÄÄÄÄÄÄÄÄÄÄÄÄ</p></body></html>"
    assert extract(mystring, output_format="csv", config=ZERO_CONFIG) is not None
    assert extract(mystring, output_format="csv", include_comments=False, config=ZERO_CONFIG).endswith("\tnull\r\n")


def test_tojson():
    # test json
    mystring = "<html><body><p>ÄÄÄÄÄÄÄÄÄÄÄÄÄÄ</p></body></html>"
    result = extract(mystring, output_format="json", config=ZERO_CONFIG)
    assert "Ä" in result and result.endswith("}")
    result = extract(mystring, output_format="json", config=ZERO_CONFIG, with_metadata=True)
    assert result.endswith("}") and '"fingerprint":' in result and '"language":' in result
    assert extract(mystring, output_format="json", include_comments=False, config=ZERO_CONFIG).endswith("}")


def test_python_output():
    # bare extraction for python
    mystring = "<html><body><p>ÄÄÄÄÄÄÄÄÄÄÄÄÄÄ</p></body></html>"
    result = bare_extraction(mystring, config=ZERO_CONFIG)
    dict_result = result.as_dict()
    assert isinstance(dict_result, dict) and len(dict_result) == 21


def test_exotic_tags(options, xmloutput=False):
    options._add_config(ZERO_CONFIG)
    # cover some edge cases with a specially crafted file
    result = load_mock_page("http://exotic_tags", xml_flag=xmloutput, tei_output=True)
    assert "Teletype text" in result and "My new car is silver." in result
    filepath = path.join(TEST_DIR, "resources", "exotic_tags_tei.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = etree.fromstring(f.read())
    res = xml.check_tei(content, "http://dummy")
    assert etree.tostring(res).startswith(
        b'<html>\n<text>\n<body>\n<div>\n\n<hi rend="uppercase">Hello</hi>\n<p>Teletype text</p>'
    )
    # misformed HTML declaration
    htmlstring = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 2012"http://www.w3.org/TR/html4/loose.dtd"><html><head></head><body><p>ABC</p></body></html>'
    # outputs '012"http://www.w3.org/TR/html4/loose.dtd">\nABC'
    assert "ABC" in extract(htmlstring, config=ZERO_CONFIG)
    # quotes
    assert handle_quotes(etree.Element("quote"), options) is None
    assert handle_table(etree.Element("table"), TAG_CATALOG, options) is None
    # p within p
    element, second = etree.Element("p"), etree.Element("p")
    element.text, second.text = "1st part.", "2nd part."
    element.append(second)
    # delete last <lb>
    element.append(etree.Element("lb"))
    converted = handle_paragraphs(element, ["p"], options)
    assert etree.tostring(converted) == b"<p>1st part. 2nd part.</p>"
    # naked div with <lb>
    assert "1.\n2.\n3." in extract(
        "<html><body><main><div>1.<br/>2.<br/>3.<br/></div></main></body></html>", fast=True, config=ZERO_CONFIG
    )
    # HTML5: <details>
    htmlstring = "<html><body><article><details><summary>Epcot Center</summary><p>Epcot is a theme park at Walt Disney World Resort featuring exciting attractions, international pavilions, award-winning fireworks and seasonal special events.</p></details></article></body></html>"
    my_result = extract(htmlstring, fast=True, config=ZERO_CONFIG)
    assert "Epcot Center" in my_result and "award-winning fireworks" in my_result
    my_result = extract(htmlstring, fast=False, config=ZERO_CONFIG)
    assert "Epcot Center" in my_result and "award-winning fireworks" in my_result

    # edge cases
    htmlstring = """<!DOCTYPE html>
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
        <p>Phasellus lectus erat, hendrerit sed tortor ac, dignissim vehicula metus.<br/></p>
      </div>
  </body>
</html>"""
    assert extract(htmlstring, include_formatting=True, include_links=True, include_images=True) is not None

    htmlstring = """<!DOCTYPE html>
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
      <p>Text here<br/></p>
      <h3>More articles</h3>
    </div>
  </body>
</html>"""
    common = {"include_formatting": True, "include_links": True, "include_images": True}
    params = [common, {**common, "favor_precision": True}, {**common, "favor_recall": True}]
    for p in params:
        result = extract(htmlstring, **p)
        assert "em improperly wrapping p here" in result and result.endswith("Text here")

    # comments
    assert extract(
        '<html><body><article><p>text</p><div class="comments"><p>comment</p></div></article></body></html>',
        include_comments=True,
        fast=True,
        config=ZERO_CONFIG,
    ).endswith("\ncomment")


def test_formatting(options):
    """Test HTML formatting conversion and extraction"""

    # trailing <lb>
    my_document = html.fromstring("<html><body><p>This here is the text.<br/></p></body></html>")
    my_result = extract(my_document, output_format="xml", config=ZERO_CONFIG)
    assert "lb" not in my_result
    # simple formatting
    my_document = html.fromstring("<html><body><p><b>This here is in bold font.</b></p></body></html>")
    my_result = extract(my_document, output_format="xml", include_formatting=True, config=ZERO_CONFIG)
    assert '<hi rend="#b">This here is in bold font.</hi>' in my_result
    # titles as markdown
    my_string = (
        "<html><body><article><h3>Title</h3><p><b>This here is in bold font.</b>Non-bold here</p></article></body></html>"
    )
    my_document = html.fromstring(my_string)
    my_result = extract(my_document, output_format="txt", include_formatting=True, config=ZERO_CONFIG)
    assert my_result == "### Title\n\n**This here is in bold font.**Non-bold here"
    assert extract(my_string, output_format="markdown", config=ZERO_CONFIG) == my_result
    assert '<hi rend="#b">' in etree.tostring(
        bare_extraction(my_string, output_format="markdown", config=ZERO_CONFIG).body, encoding="unicode"
    )

    meta_string = "<html><head><title>Test</title></head><body><p>ABC.</p></body></html>"
    meta_result = extract(meta_string, output_format="markdown", config=ZERO_CONFIG, with_metadata=True)
    assert " ".join(meta_result.split()) == "--- title: Test --- ABC."

    # space between paragraphs
    my_document = html.fromstring(
        "<html><body><article><h3>Title</h3><p>Paragraph 1</p><p>Paragraph 2</p></article></body></html>"
    )
    my_result = extract(my_document, output_format="txt", include_formatting=True, config=ZERO_CONFIG)
    assert my_result.endswith("Paragraph 1\n\nParagraph 2")

    # code sections
    my_document = html.fromstring(
        "<html><body><article><h3>Title</h3><p>Here is a code sample:</p><code>import trafilatura</code></p></article></body></html>"
    )
    my_result = extract(my_document, output_format="txt", include_formatting=True, config=ZERO_CONFIG)
    assert (
        my_result
        == """### Title

Here is a code sample:

`import trafilatura`"""
    )
    my_document = html.fromstring(
        '<html><body><article><h3>Title</h3><p>Here is a code sample:</p><code><span>import</span> <span>something</span><br/>something.run("somewhere")</code><p>Sometimes code is wrapped using <code>pre</code> and <code>code</code>:</p><pre><code>import trafilatura\ntrafilatura.extract("")</code></pre><p>Less often code is wrapped using just <code>pre</code>:</p><pre>\ntrafilatura.extract("")</pre></article></body></html>'
    )
    my_result = extract(my_document, output_format="txt", include_formatting=True, config=ZERO_CONFIG)
    assert (
        my_result
        == """### Title

Here is a code sample:

```
import something
something.run("somewhere")
```
Sometimes code is wrapped using `pre` and `code`:

```
import trafilatura
trafilatura.extract("")
```
Less often code is wrapped using just `pre`:

```
trafilatura.extract("")
```"""
    )

    # nested
    my_document = html.fromstring("<html><body><p><b>This here is in bold and <i>italic</i> font.</b></p></body></html>")
    my_result = extract(my_document, output_format="xml", include_formatting=True, config=ZERO_CONFIG)
    assert '<hi rend="#b">This here is in bold and <hi rend="#i">italic</hi> font.</hi>' in my_result
    # empty
    my_document = html.fromstring("<html><body><p><b><i></i></b></p></body></html>")
    my_result = extract(my_document, output_format="xml", include_formatting=True, config=ZERO_CONFIG)
    assert "<main/>" in my_result
    # wild div
    my_document = html.fromstring("<html><body><article><div><strong>Wild text</strong></div></article></body></html>")
    my_result = extract(my_document, output_format="xml", include_formatting=True, config=ZERO_CONFIG)
    assert "<p>" in my_result and '<hi rend="#b">Wild text</hi>' in my_result  # no rend so far
    my_document = html.fromstring("<html><body><article><div><strong>Wild text</strong></div></article></body></html>")
    my_result = extract(my_document, config=ZERO_CONFIG)
    assert my_result == "Wild text"
    # links
    doc = html.fromstring('<html><body><p><a href="">Link text</a></p></body></html>')
    my_result = extract(doc, config=ZERO_CONFIG)
    assert my_result == "Link text"
    # line-breaks
    doc = html.fromstring("<html><body><p><br/></p></body></html>")
    my_result = extract(doc, config=ZERO_CONFIG)
    assert my_result == ""
    doc = html.fromstring("<html><body><p><br/>Here is the text.</p></body></html>")
    my_result = extract(doc, config=ZERO_CONFIG)
    assert my_result == "Here is the text."
    # handle formatting tails
    element = etree.Element("hi")
    element.text = "Here is the text."
    element.tail = "And a tail."
    options._add_config(ZERO_CONFIG)
    converted = handle_formatting(element, options)
    assert etree.tostring(converted) == b"<p><hi>Here is the text.</hi>And a tail.</p>"
    # empty elements
    my_document = html.fromstring("<html><body><div>\t\n</div><div>There is text here.</div></body></html>")
    my_result = extract(my_document, output_format="xml", config=ZERO_CONFIG)
    assert "<main>\n    <p>There is text here.</p>\n  </main>" in my_result
    # lists with links
    my_document = html.fromstring(
        '<html><body><article><ul><li>Number 1</li><li>Number <a href="test.html">2</a></li><li>Number 3</li><p>Test</p></article></body></html>'
    )
    my_result = extract(my_document, output_format="xml", include_links=True, config=ZERO_CONFIG)
    assert '<item>Number <ref target="test.html">2</ref></item>' in my_result

    my_document = html.fromstring("""<html><body><article>
        <ul>
            <li>Number 0</li>
            <li>Number <a href="test.html">1</a></li>
            <li><a href="test.html">Number 2</a> n2</li>
            <li>Number 3</li>
            <li><p>Number 4</p> n4</li>
        </ul>
        Test</article></body></html>
    """)
    my_result = extract(my_document, output_format="markdown", include_links=True, config=ZERO_CONFIG)
    assert my_result == "- Number 0\n- Number [1](test.html)\n- [Number 2](test.html) n2\n- Number 3\n- Number 4 n4\n\nTest"
    # XML and Markdown formatting within <p>-tag
    my_document = html.fromstring(
        '<html><body><p><b>bold</b>, <i>italics</i>, <tt>tt</tt>, <strike>deleted</strike>, <u>underlined</u>, <a href="test.html">link</a> and additional text to bypass detection.</p></body></html>'
    )
    my_result = extract(copy(my_document), fast=True, include_formatting=False, config=ZERO_CONFIG)
    assert my_result == "bold, italics, tt, deleted, underlined, link and additional text to bypass detection."

    my_result = extract(copy(my_document), fast=True, include_formatting=True, config=ZERO_CONFIG)
    assert my_result == "**bold**, *italics*, `tt`, ~~deleted~~, __underlined__, link and additional text to bypass detection."

    my_result = extract(copy(my_document), fast=True, include_links=True, include_formatting=True, config=ZERO_CONFIG)
    assert (
        my_result
        == "**bold**, *italics*, `tt`, ~~deleted~~, __underlined__, [link](test.html) and additional text to bypass detection."
    )

    my_result = extract(copy(my_document), output_format="xml", fast=True, include_formatting=True, config=ZERO_CONFIG)
    assert (
        '<p><hi rend="#b">bold</hi>, <hi rend="#i">italics</hi>, <hi rend="#t">tt</hi>, <del>deleted</del>, <hi rend="#u">underlined</hi>, link and additional text to bypass detection.</p>'
        in my_result
    )
    assert (
        'rend="#b"' in my_result
        and 'rend="#i"' in my_result
        and 'rend="#t"' in my_result
        and 'rend="#u"' in my_result
        and "<del>" in my_result
    )

    my_result = extract(
        copy(my_document), output_format="xml", include_formatting=True, include_links=True, fast=True, config=ZERO_CONFIG
    )
    assert (
        '<p><hi rend="#b">bold</hi>, <hi rend="#i">italics</hi>, <hi rend="#t">tt</hi>, <del>deleted</del>, <hi rend="#u">underlined</hi>, <ref target="test.html">link</ref> and additional text to bypass detection.</p>'
        in my_result
    )
    my_result = extract(my_document, output_format="txt", fast=True, include_formatting=True, config=ZERO_CONFIG)
    assert my_result == "**bold**, *italics*, `tt`, ~~deleted~~, __underlined__, link and additional text to bypass detection."

    # double <p>-elems
    # could be solved by keeping the elements instead of reconstructing them
    my_document = html.fromstring("<html><body><p>AAA, <p>BBB</p>, CCC.</p></body></html>")
    my_result = extract(
        my_document, output_format="xml", include_formatting=True, include_links=True, fast=True, config=ZERO_CONFIG
    )
    assert "AAA" in my_result and "BBB" in my_result and "CCC" in my_result

    # line-break following formatting
    my_document = html.fromstring(
        "<html><body><article><p><strong>Staff Review of the Financial Situation</strong><br>Domestic financial conditions remained accommodative over the intermeeting period.</p></article></body></html>"
    )
    my_result = extract(my_document, output_format="txt", fast=True, config=ZERO_CONFIG)
    assert (
        my_result
        == "Staff Review of the Financial Situation\nDomestic financial conditions remained accommodative over the intermeeting period."
    )
    # title with formatting
    my_document = html.fromstring(
        '<html><body><article><h4 id="1theinoperator">1) The <code>in</code> Operator</h4><p>The easiest way to check if a Python string contains a substring is to use the <code>in</code> operator. The <code>in</code> operator is used to check data structures for membership in Python. It returns a Boolean (either <code>True</code> or <code>False</code>) and can be used as follows:</p></article></body></html>'
    )
    my_result = extract(my_document, output_format="xml", fast=True, include_formatting=True, config=ZERO_CONFIG)
    assert (
        '<head rend="h4">1) The <code>in</code> Operator</head>' in my_result
        and "<p>The easiest way to check if a Python string contains a substring is to use the <code>in</code> operator. The <code>in</code> operator is used to check data structures for membership in Python. It returns a Boolean (either <code>True</code> or <code>False</code>) and can be used as follows:</p>"
        in my_result
    )

    my_document = html.fromstring("""
    <html><head><body><article>python code below:
<pre><code>
def test:
    print('hello')
    print('world')
    </code></pre>
    </article></body></html>
    """)
    my_result = extract(my_document, output_format="markdown", include_formatting=True, config=ZERO_CONFIG)
    assert "python code below:\n```\ndef test:\n    print('hello')\n    print('world')\n    \n```" == my_result

    my_result = extract(my_document, output_format="markdown", include_formatting=True, config=ZERO_CONFIG)
    assert (
        """python code below:
```
def test:
    print('hello')
    print('world')
    
```"""
        == my_result
    )

    my_document = html.fromstring("<html><body><table><td><p>Sjätte <nobr>AP-fonden</nobr></p></td></table></body></html>")
    my_result = extract(my_document, output_format="xml", include_tables=True, config=ZERO_CONFIG)
    assert "AP-fonden" in my_result


def test_blockquote_inline_content():
    "Inline formatting, links, and images inside blockquotes must be preserved."
    assert _md_inline("<blockquote><p>A <b>bold</b> word</p></blockquote>") == f"{_INTRO}\n\nA **bold** word"
    assert (
        _md_inline("<blockquote><p>see <a href='http://x.com'>link</a></p></blockquote>", include_links=True)
        == f"{_INTRO}\n\nsee [link](http://x.com)"
    )
    assert (
        _md_inline("<blockquote><p>text</p><img src='x.jpg' alt='img'/></blockquote>", include_images=True)
        == f"{_INTRO}\n\ntext\n\n![img](x.jpg)"
    )


def test_yoast_faq_block():
    "Yoast FAQ block questions are bold but act as headers and must be kept (issue #471)."
    # a long lead paragraph keeps <div> out of the potential tags, as on the reported page
    lead = (
        "The wrap dress is a dress with a front closure formed by wrapping one side across the other "
        "and knotting the attached ties that wrap around the back at the waist or fastening buttons. "
        "It was popularised in the seventies and has remained a wardrobe staple ever since, flattering "
        "many different body shapes thanks to its adjustable and forgiving cut. " * 2
    )
    htmlstring = (
        "<html><body><article><h1>Wrap dress</h1><p>" + lead + "</p>"
        '<div class="schema-faq wp-block-yoast-faq-block">'
        '<div class="schema-faq-section" id="faq-question-1">'
        '<strong class="schema-faq-question">Who invented the wrap dress?</strong> '
        '<p class="schema-faq-answer">It was popularised by Diane von Furstenberg in 1974.</p>'
        "</div></div></article></body></html>"
    )
    # default (no formatting): the question must not be dropped
    assert "Who invented the wrap dress?" in extract(htmlstring, config=ZERO_CONFIG)
    # with formatting: it is rendered as a header
    assert "### Who invented the wrap dress?" in extract(
        htmlstring, output_format="txt", include_formatting=True, config=ZERO_CONFIG
    )
    assert '<head rend="h3">Who invented the wrap dress?</head>' in extract(
        htmlstring, output_format="xml", config=ZERO_CONFIG
    )


def test_include_formatting_markdown():
    "markdown defaults to formatted, but an explicit include_formatting=False is honored (was ignored for markdown)."
    doc = "<html><body><article><p>plain and <b>bold</b> text here.</p></article></body></html>"
    assert extract(doc, output_format="markdown", config=ZERO_CONFIG) == "plain and **bold** text here."
    assert extract(doc, output_format="markdown", include_formatting=False, config=ZERO_CONFIG) == "plain and bold text here."
    assert extract(doc, output_format="txt", include_formatting=True, config=ZERO_CONFIG) == "plain and **bold** text here."


def test_markdown_list_item_inline_spacing():
    """Inline formatting tails inside list items must keep their leading space (issue #845)"""
    htmlstring = "<html><body><article><ol><li>Foo <em>bar</em> baz.</li></ol></article></body></html>"
    assert extract(htmlstring, output_format="markdown", config=ZERO_CONFIG) == "1. Foo *bar* baz."


def test_extract_with_metadata():
    """Test extract_with_metadata method"""
    url = "http://aa.bb/cc.html"
    my_document = html.fromstring("""<html>
        <head></head>
        <body>
        <article>
        <p>AAA, <p>BBB</p>, CCC.</p>
        </article>
        </body>
        </html>
    """)
    parsed_doc = extract_with_metadata(my_document, output_format="txt", include_formatting=True, fast=True, url=url)
    content = parsed_doc.text
    assert "AAA" in content and "BBB" in content and "CCC" in content
    assert url == parsed_doc.url and parsed_doc.date is None and parsed_doc.title is None

    my_document = html.fromstring("""<html>
        <head><title>title</title></head>
        <body>
        <article>
        <div>May 24, 2021</div>
        <p>AAA, <p>BBB</p>, CCC.</p>
        </article>
        </body>
        </html>
    """)
    parsed_doc = extract_with_metadata(my_document, output_format="txt", include_formatting=True, fast=True, url=url)
    content = parsed_doc.text
    assert "AAA" in content and "BBB" in content and "CCC" in content
    assert url == parsed_doc.url and "2021-05-24" == parsed_doc.date and "title" == parsed_doc.title

    parsed_doc = extract_with_metadata(my_document, output_format="xml", config=ZERO_CONFIG)
    assert "AAA, BBB , CCC." == parsed_doc.raw_text and "ee7d2fb6fcf2837d" == parsed_doc.fingerprint
    content = parsed_doc.text
    assert "AAA" in content and "BBB" in content and "CCC" in content

    my_document = html.fromstring("""<html>
        <head><meta http-equiv="content-language" content="es"></head>
        <body>
        <article>
        <p>AAA, <p>BBB</p>, CCC.</p>
        </article>
        </body>
        </html>
    """)
    parsed_doc = extract_with_metadata(my_document, target_language="en", fast=True)
    assert parsed_doc is None

    with pytest.raises(ValueError):
        extract_with_metadata(my_document, output_format="python")


def test_external(options):
    """Test external components"""
    options.tables = True
    # remove unwanted elements
    mydoc = html.fromstring("<html><body><footer>Test text</footer></body></html>")
    _, _, mylen = sanitize_tree(mydoc, options)
    assert mylen == 0
    mydoc = html.fromstring("<html><body><table><th>Test text</th><tr><td>Test</td></tr></table></body></html>")
    _, _, mylen = sanitize_tree(mydoc, options)
    assert mylen > 0
    # strip fancy tags while including links and images
    mydoc = html.fromstring(
        '<html><body><p>Text here <fancy>Test text</fancy><a href="">with a link</a>.</p><img src="test.jpg"/></body></html>'
    )
    mytree, _, _ = sanitize_tree(mydoc, options)
    assert len(mytree) == 1
    mydoc = html.fromstring(
        '<html><body><p>Text here <fancy>Test text</fancy><a href="">with a link</a>.</p><img src="test.jpg"/></body></html>'
    )
    options.links, options.images = True, True
    mytree, _, _ = sanitize_tree(mydoc, options)
    myelems = {element.tag for element in set(mytree.iter())}
    assert "graphic" in myelems and "ref" in myelems
    # test langid
    if LANGID_FLAG is True:
        doc = html.fromstring("<html><body>" + "<p>Non è inglese.</p>" * 20 + "</body></html>")
        assert extract(doc, fast=False, target_language="en", deduplicate=False) is None
    # no tables
    with open(path.join(RESOURCES_DIR, "apache.html"), "r", encoding="utf-8") as f:
        teststring = f.read()
    assert "localhost:80" in extract(teststring, fast=False, include_tables=True)
    assert "localhost:80" not in extract(teststring, fast=False, include_tables=False)
    with open(path.join(RESOURCES_DIR, "scam.html"), "r", encoding="utf-8") as f:
        teststring = f.read()
    assert extract(teststring, fast=True, include_tables=False, config=ZERO_CONFIG) == ""
    assert extract(teststring, fast=False, include_tables=False, config=ZERO_CONFIG) == ""
    # invalid XML attributes: namespace colon in attribute key (issue #375). Those attributes should be stripped
    bad_xml = '<p>Testing</p><ul style="" padding:1px; margin:15px""><b>Features:</b> <li>Saves the cost of two dedicated phone lines.</li> al station using Internet or cellular technology.</li> <li>Requires no change to the existing Fire Alarm Control Panel configuration. The IPGSM-4G connects directly to the primary and secondary telephone ports.</li>'
    res = extract(bad_xml, output_format="xml")
    assert "Features" in res


def test_images(options):
    """Test image extraction function"""
    # file type
    assert is_image_file(None) is False
    assert is_image_file("") is False
    assert is_image_file("test.jpg") is True
    assert is_image_file("test.txt") is False
    assert is_image_file("test.jpg" * 2000) is False  # length threshold
    # tag with attributes
    assert handle_image(None) is None
    assert handle_image(html.fromstring('<img src="test.jpg"/>')) is not None
    assert handle_image(html.fromstring('<img data-src="test.jpg" alt="text" title="a title"/>')) is not None
    assert handle_image(html.fromstring('<img other="test.jpg"/>')) is None
    # HTML conversion
    assert handle_textelem(etree.Element("graphic"), [], options) is None
    with open(path.join(RESOURCES_DIR, "http_sample.html"), "r", encoding="utf-8") as f:
        teststring = f.read()
    assert "![Example image](test.jpg)" not in extract(teststring)
    assert "![Example image](test.jpg)" in extract(teststring, include_images=True, fast=True)
    assert '<graphic src="test.jpg" title="Example image"/>' in extract(
        teststring, include_images=True, fast=True, output_format="xml", config=ZERO_CONFIG
    )

    def img(body, **kw):
        return _extract_doc(body, intro=False, include_images=True, fast=True, **kw)

    assert img('<img data-src="test.jpg" alt="text" title="a title"/>') == "![a title text](test.jpg)"
    assert img('<p><img data-src="test.jpg" alt="text" title="a title"/></p>') == "![a title text](test.jpg)"
    assert img('<p><img other="test.jpg" alt="text" title="a title"/></p>') == ""
    assert img('<div><p><img data-src="test.jpg" alt="text" title="a title"/></p></div>') == "![a title text](test.jpg)"
    assert img('<div><p><img data-src-small="test.jpg" alt="text" title="a title"/></p></div>') == "![a title text](test.jpg)"
    assert (
        img('<div><p><img src="https://a.b/test.jpg" alt="text" title="a title"/></p></div>')
        == "![a title text](https://a.b/test.jpg)"
    )

    url = "http://a.b/c/d.html"
    assert (
        img('<div><p><img src="//a.b/test.jpg" alt="text" title="a title"/></p></div>', url=url)
        == "![a title text](http://a.b/test.jpg)"
    )
    assert (
        img('<div><p><img src="/a.b/test.jpg" alt="text" title="a title"/></p></div>', url=url)
        == "![a title text](http://a.b/a.b/test.jpg)"
    )
    assert (
        img('<div><p><img src="./a.b/test.jpg" alt="text" title="a title"/></p></div>', url=url)
        == "![a title text](http://a.b/c/a.b/test.jpg)"
    )
    assert (
        img('<div><p><img src="../a.b/test.jpg" alt="text" title="a title"/></p></div>', url=url)
        == "![a title text](http://a.b/a.b/test.jpg)"
    )

    assert (
        handle_image(
            html.fromstring(
                '<img src="data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="text"></img>'
            )
        )
        is None
    )

    # CNN example
    mydoc = html.fromstring(
        '<img class="media__image media__image--responsive" alt="Harry and Meghan last March, in their final royal engagement." data-src-mini="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-169.jpg" data-src-xsmall="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-medium-plus-169.jpg" data-src-small="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-large-169.jpg" data-src-medium="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg" data-src-large="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-super-169.jpg" data-src-full16x9="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-full-169.jpg" data-src-mini1x1="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-11.jpg" data-demand-load="loaded" data-eq-pts="mini: 0, xsmall: 221, small: 308, medium: 461, large: 781" src="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg" data-eq-state="mini xsmall small medium" data-src="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg">'
    )
    myimage = handle_image(mydoc)
    assert myimage is not None and "alt" in myimage.attrib and "src" in myimage.attrib
    # modified CNN example
    mydoc = html.fromstring(
        '<img class="media__image media__image--responsive" alt="Harry and Meghan last March, in their final royal engagement." data-src-mini="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-169.jpg" data-src-xsmall="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-medium-plus-169.jpg" data-src-small="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-large-169.jpg" data-src-medium="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-exlarge-169.jpg" data-src-large="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-super-169.jpg" data-src-full16x9="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-full-169.jpg" data-src-mini1x1="//cdn.cnn.com/cnnnext/dam/assets/210307091919-harry-meghan-commonwealth-day-small-11.jpg" data-demand-load="loaded" data-eq-pts="mini: 0, xsmall: 221, small: 308, medium: 461, large: 781">'
    )
    myimage = handle_image(mydoc)
    assert (
        myimage is not None and "alt" in myimage.attrib and "src" in myimage.attrib and myimage.get("src").startswith("http")
    )


def test_links(options):
    """Test link extraction function"""
    options._add_config(ZERO_CONFIG)
    assert handle_textelem(etree.Element("ref"), [], options) is None
    assert handle_formatting(html.fromstring('<a href="testlink.html">Test link text.</a>'), options) is not None
    # empty link
    mydoc = html.fromstring("<html><body><p><a></a><b>Some text.</b></p></body></html>")
    assert extract(mydoc) is not None
    # link with target
    mydoc = html.fromstring(
        '<html><body><p><a href="testlink.html">Test link text.</a> This part of the text has to be long enough.</p></body></html>'
    )
    assert "testlink.html" not in extract(copy(mydoc))
    assert "[Test link text.](testlink.html) This part of the text has to be long enough." in extract(
        copy(mydoc), include_links=True, fast=True, config=ZERO_CONFIG
    )
    # relative link conversion
    assert "[Test link text.](https://www.example.com/testlink.html) This part of the text has to be long enough." in extract(
        copy(mydoc), url="https://www.example.com/", include_links=True, fast=True, config=ZERO_CONFIG
    )
    # link without target
    mydoc = html.fromstring(
        "<html><body><p><a>Test link text.</a> This part of the text has to be long enough.</p></body></html>"
    )
    assert "[Test link text.] This part of the text has to be long enough." in extract(
        copy(mydoc), include_links=True, fast=True, config=ZERO_CONFIG
    )
    mydoc = html.fromstring(
        "<html><body><article><a>Segment 1</a><h1><a>Segment 2</a></h1><p>Segment 3</p></article></body></html>"
    )
    result = extract(copy(mydoc), output_format="xml", include_links=True, fast=True, config=ZERO_CONFIG)
    assert "1" in result and "2" in result and "3" in result
    with open(path.join(RESOURCES_DIR, "http_sample.html"), "r", encoding="utf-8") as f:
        teststring = f.read()
    assert "testlink.html" not in extract(teststring, config=ZERO_CONFIG)
    assert "[link](testlink.html)" in extract(teststring, include_links=True, fast=True, config=ZERO_CONFIG)
    assert '<ref target="testlink.html">link</ref>' in extract(
        teststring, include_links=True, fast=True, output_format="xml", config=ZERO_CONFIG
    )
    # test license link
    mydoc = html.fromstring('<html><body><p>Test text under <a rel="license" href="">CC BY-SA license</a>.</p></body></html>')
    assert 'license="CC BY-SA license"' in extract(
        mydoc, include_links=True, fast=True, output_format="xml", config=ZERO_CONFIG, with_metadata=True
    )

    # link in p, length threshold
    mydoc = html.fromstring(f"<html><body><article><p><a>f{'abcd' * 20}</a></p></article></body></html>")
    assert "abc" in extract(copy(mydoc), fast=True, config=ZERO_CONFIG, favor_precision=False)
    assert extract(mydoc, fast=True, config=ZERO_CONFIG, favor_precision=True) == ""


def test_tei():
    """test TEI-related functions"""
    # open local resources to avoid redownloading at each run
    with open(path.join(RESOURCES_DIR, "httpbin_sample.html"), "r", encoding="utf-8") as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result1 = extract(teststring, "mocked", fast=True, output_format="xmltei", tei_validation=False)
    result2 = extract(teststring, "mocked", fast=True, output_format="xmltei", tei_validation=True)
    assert result1 is not None and result1 == result2
    assert xml.validate_tei(etree.fromstring(result1)) is True
    assert xml.validate_tei(etree.fromstring(teststring)) is False
    # test with another file
    with open(path.join(RESOURCES_DIR, "http_sample.html"), "r", encoding="utf-8") as f:
        teststring = f.read()
    # download, parse and validate simple html file
    result = extract(teststring, "mocked", fast=True, include_comments=True, output_format="xmltei", tei_validation=False)
    assert result is not None  # and '<p>license</p>' in result
    assert xml.validate_tei(etree.fromstring(result)) is True
    result = extract(teststring, "mocked", fast=True, include_comments=False, output_format="xmltei", tei_validation=False)
    assert result is not None  # and '<p>license</p>' in result
    assert xml.validate_tei(etree.fromstring(result)) is True
    # include ID in metadata
    result = extract(teststring, "mocked", fast=True, output_format="xmltei", tei_validation=False, record_id="0001")
    assert result is not None
    assert xml.validate_tei(etree.fromstring(result)) is True
    # test header + metadata
    tei = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    header = etree.SubElement(tei, "teiHeader")
    docmeta = Document()
    docmeta.categories, docmeta.tags = [], []
    docmeta.title = "Title"
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.sitename = "Site Name"
    docmeta.date = "2021-01-01"
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.date = None
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.hostname = "hostname"
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.sitename = None
    docmeta.license = "CC BY-SA"
    docmeta.url = "https://test.org/"
    docmeta.categories = ["cat1", "cat2"]
    assert xml.write_fullheader(header, docmeta) is not None
    docmeta.date = "2021-01-01"
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
    xml_doc = etree.fromstring(
        "<TEI><text><body><div><div>text1<quote>text2</quote></div>has to be there</div></body></text></TEI>"
    )
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
    extracted = extract(htmlstring, url="mocked", fast=True, output_format="xmltei", config=ZERO_CONFIG)
    assert xml.validate_tei(etree.fromstring(extracted)) is True
    htmlstring = html.fromstring("<html><body><article><h1>title</h1><h2>subtitle</h2><p>text</p></article></body></html>")
    extracted = extract(htmlstring, url="mocked", fast=True, output_format="xmltei", config=ZERO_CONFIG)
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
    extracted = extract(htmlstring, url="mocked", fast=True, output_format="xmltei", config=ZERO_CONFIG)
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
    result = sanitize(etree.tostring(tree, encoding="unicode")).replace("\n", "")
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


def test_htmlprocessing(options):
    """test html-related functions"""
    assert xml.xmltotxt(None, include_formatting=False) == ""

    options.tables = True
    assert trafilatura.htmlprocessing.tree_cleaning(etree.Element("html"), options) is not None
    assert trafilatura.htmlprocessing.prune_html(etree.Element("unwanted")) is not None
    mydoc = html.fromstring(
        '<html><body><table><a href="">Link</a></table><img src="test.jpg"/><u>Underlined</u><tt>True Type</tt><sub>Text</sub><sup>Text</sup></body></html>'
    )
    options.formatting, options.images, options.links = True, True, True
    myconverted = trafilatura.htmlprocessing.convert_tags(mydoc, options)
    assert (
        myconverted.xpath(".//ref")
        and myconverted.xpath(".//graphic")
        and myconverted.xpath('.//hi[@rend="#t"]')
        and myconverted.xpath(".//table")
    )

    # multiple images inside a link must keep their original order after being
    # lifted out of the <ref> (addnext reverses order if iterated forward)
    multi_img = html.fromstring(
        '<html><body><a href="/x"><img src="a.jpg"/><img src="b.jpg"/><img src="c.jpg"/></a></body></html>'
    )
    options.images, options.links = True, True
    multi_converted = trafilatura.htmlprocessing.convert_tags(multi_img, options)
    srcs = [g.get("src") for g in multi_converted.iter("graphic")]
    assert srcs == ["a.jpg", "b.jpg", "c.jpg"]

    options.images, options.tables = True, False
    myconverted = trafilatura.htmlprocessing.tree_cleaning(mydoc, options)
    assert myconverted.xpath(".//graphic") and not myconverted.xpath(".//table")
    mydoc = html.fromstring("<html><body><article><h1>Test headline</h1><p>Test</p></article></body></html>")
    assert '<head rend="h1">Test headline</head>' in extract(copy(mydoc), output_format="xml", config=ZERO_CONFIG, fast=True)
    assert '<ab rend="h1" type="header">Test headline</ab>' in extract(
        copy(mydoc), output_format="xmltei", config=ZERO_CONFIG, fast=True
    )

    # merge with parent function
    element = etree.Element("test")
    xml.delete_element(element)
    assert etree.tostring(element) == b"<test/>"
    element = etree.Element("test")
    xml.merge_with_parent(element)
    assert etree.tostring(element) == b"<test/>"

    mydoc = html.fromstring("<html><body><p><span>A</span><span>B</span><span>C</span></p></body></html>")
    for element in mydoc.iter("span"):
        xml.merge_with_parent(element)
    assert b"<p>A B C</p>" in etree.tostring(mydoc)
    mydoc = html.fromstring("<html><body><p><span>A</span><span>B</span> tail<span>C</span></p></body></html>")
    for element in mydoc.iter("span"):
        xml.merge_with_parent(element)
    assert b"<p>A B tail C</p>" in etree.tostring(mydoc)

    # paywalls
    my_html = '<html><body><main><p>1</p><p id="premium">2</p><p>3</p></main></body></html>'
    assert extract(my_html, config=ZERO_CONFIG, fast=True) == "1\n3"
    assert extract(my_html, config=ZERO_CONFIG, fast=False) == "1\n3"
    # fencedframe
    fenced_html = "<html><body><article><p>real</p><fencedframe><p>ad</p></fencedframe><p>more</p></article></body></html>"
    assert "ad" not in extract(fenced_html, config=ZERO_CONFIG, fast=True)
    assert "ad" not in extract(fenced_html, config=ZERO_CONFIG, fast=False)
    fenced_outer = "<html><body><fencedframe><article><h1>ad</h1><p>buy now buy now buy now buy now</p></article></fencedframe></body></html>"
    assert "ad" not in extract(fenced_outer, config=ZERO_CONFIG, fast=False)
    assert extract(fenced_outer, config=use_config()) is None
    # test tail of node deleted if set as text
    node = etree.fromstring("<div><p></p>tail</div>")[0]
    trafilatura.htmlprocessing.process_node(node, options)
    assert node.text == "tail"
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
    node = etree.fromstring("<p><ref target='url'><hi rend='#b'>bold</hi>inner</ref>outer</p>")[0]
    processed = trafilatura.htmlprocessing.handle_textnode(node, options)
    assert processed.tail == "outer"
    node = etree.fromstring("<p><ref target='url'>text</ref>tail</p>")[0]
    processed = trafilatura.htmlprocessing.handle_textnode(node, options)
    assert processed.tail == "tail" and processed.text == "text"
    node = etree.fromstring("<p><ref target='url'></ref>tail</p>")[0]
    processed = trafilatura.htmlprocessing.handle_textnode(node, options)
    assert processed.tail == "" and processed.text == "tail"
    node = etree.fromstring("<p><ref target='url'>text<hi rend='#b'>bold</hi></ref>tail</p>")[0]
    processed = trafilatura.htmlprocessing.handle_textnode(node, options)
    assert processed.tail == "tail" and processed.text == "text"

    # fix for bug 807
    node = html.fragment_fromstring("<div><p><span>span</span> span tail</p> p tail </div>")
    assert node.text_content() == "span span tail p tail "
    prune = etree.XPath(".//span")
    processed = trafilatura.htmlprocessing.prune_unwanted_nodes(node, [prune])
    assert node.text_content() == " span tail p tail "

    # link_density_test_tables: a text-rich table whose only <ref> links carry no text
    # (e.g. icon/flag links wrapping images) has zero link text -> not boilerplate, kept
    linkless_table = html.fromstring("<table><cell>" + "word " * 50 + '<ref target="/x"></ref></cell></table>')
    assert trafilatura.htmlprocessing.link_density_test_tables(linkless_table) is False
    # short table (elemlen < 200) is never removed regardless of link ratio
    assert (
        trafilatura.htmlprocessing.link_density_test_tables(
            html.fromstring("<table><cell>short " + '<ref target="/x">link</ref> ' * 5 + "</cell></table>")
        )
        is False
    )
    # replace_element_text: an empty <ref> (no text) yields an empty string
    assert xml.replace_element_text(etree.Element("ref"), include_formatting=False) == ""

    # regression #797: a code block with a tailless <lb> must not emit a literal "None"
    code = etree.fromstring("<code>print(1)<lb/></code>")
    code_md = xml.replace_element_text(code, include_formatting=True)
    assert "None" not in code_md and "print(1)" in code_md

    # handle_paragraphs: a trailing <lb> with no tail is stripped from the output
    para = etree.fromstring("<p>text<lb>x</lb></p>")
    processed = handle_paragraphs(para, {"p", "lb"}, options)
    assert processed is not None and not processed.findall(".//lb")

    # handle_paragraphs: non-INLINE_CARRIED children of <hi> are stripped with a leading space
    fmt_opts = core.Extractor(formatting=True)
    para = etree.fromstring('<p><hi rend="#b">pre<quote>mid</quote>end</hi></p>')
    hi = handle_paragraphs(para, set(TAG_CATALOG), fmt_opts).find("hi")
    assert hi is not None and "pre" in hi.text and " mid" in hi.text

    para = etree.fromstring('<p><hi rend="#b">start<lb/>tail</hi></p>')
    hi = handle_paragraphs(para, set(TAG_CATALOG) | {"lb"}, fmt_opts).find("hi")
    assert hi is not None and " tail" in hi.text


def test_extraction_options():
    """Test the different parameters available in extract() and bare_extraction()"""
    my_html = '<html><head><meta http-equiv="content-language" content="EN"/></head><body><div="article-body"><p>Text.<!-- comment --><?php echo "This is a PHP processing instruction"; ?></p></div></body></html>'

    with pytest.raises(ValueError):
        extract(my_html, output_format="python")
    assert extract(my_html, config=NEW_CONFIG) is None
    assert extract(my_html, config=ZERO_CONFIG) is not None
    assert extract(my_html, only_with_metadata=False, output_format="xml", config=ZERO_CONFIG) is not None
    assert extract(my_html, only_with_metadata=True, output_format="xml", config=ZERO_CONFIG) is None
    assert extract(my_html, target_language="de", config=ZERO_CONFIG) is None
    assert extract(my_html, target_language="de", fast=True, config=ZERO_CONFIG) is None

    # justext hardening
    assert etree.tostring(try_justext(html.fromstring(my_html), None, "de")) == b"<body/>"
    assert etree.tostring(try_justext(None, None, "de")) == b"<body/>"
    # assert extract(my_html) is None

    # readability
    my_html = "<html><body><p>" + "Text. " * 10 + "</p></body></html>"
    result = etree.tostring(try_readability(html.fromstring(my_html)))
    assert len(result) > 10 and b"Text" in result
    my_html = "<html><body><p>" + "Text. " * 10 + "<embed>Test</embed></p></body></html>"
    result = etree.tostring(try_readability(html.fromstring(my_html)))
    assert b"Test" not in result

    my_html = "<html><head/><body>" + "<p>ABC def ghi jkl.</p>" * 1000 + "<p>Posted on 1st Dec 2019<.</p></body></html>"
    assert bare_extraction(my_html, config=ZERO_CONFIG, with_metadata=True).date is not None
    assert bare_extraction(my_html, config=NEW_CONFIG, with_metadata=True).date is None
    assert bare_extraction(my_html, config=NEW_CONFIG, with_metadata=False).date is None


def test_precision_recall():
    """test precision- and recall-oriented settings"""
    # the test cases could be better
    my_document = html.fromstring("<html><body><p>This here is the text.</p></body></html>")
    assert extract(copy(my_document), favor_precision=True, config=ZERO_CONFIG, fast=True) is not None
    assert extract(copy(my_document), favor_recall=True, config=ZERO_CONFIG, fast=True) is not None

    my_document = html.fromstring(
        '<html><body><div class="article-body"><div class="teaser-content"><p>This here is a teaser text.</p></div><div><p>This here is the text.</p></div></body></html>'
    )
    assert "teaser text" in extract(copy(my_document), favor_recall=True, config=ZERO_CONFIG, fast=True)
    assert "teaser text" not in extract(copy(my_document), config=ZERO_CONFIG, fast=True)
    assert "teaser text" not in extract(copy(my_document), favor_precision=True, config=ZERO_CONFIG, fast=True)

    my_document = html.fromstring(
        '<html><body><article><div><p><a href="test.html">1.</a><br/><a href="test2.html">2.</a></p></div></article></body></html>'
    )
    result = extract(copy(my_document), favor_recall=True, config=ZERO_CONFIG, fast=True)
    assert "1" not in result
    result = extract(copy(my_document), favor_precision=True, config=ZERO_CONFIG, fast=True)
    assert "1" not in result

    my_document = html.fromstring(
        '<html><body><div class="article-body"><p>content</p><p class="link">Test</p></div></body></html>'
    )
    result = extract(copy(my_document), favor_precision=False, config=ZERO_CONFIG, fast=True)
    assert "content" in result and "Test" in result
    result = extract(copy(my_document), favor_precision=True, config=ZERO_CONFIG, fast=True)
    assert "content" in result and "Test" not in result

    my_document = html.fromstring("<html><body><article><aside><p>Here is the text.</p></aside></article></body></html>")
    result = extract(copy(my_document), favor_recall=False, config=ZERO_CONFIG, fast=True)
    assert result != "Here is the text."
    result = extract(copy(my_document), favor_recall=True, config=ZERO_CONFIG, fast=True)
    assert result == "Here is the text."

    my_document = html.fromstring("<html><body><div><h2>Title</h2><small>Text.</small></div></body></html>")
    result = extract(copy(my_document), favor_recall=True, config=ZERO_CONFIG, fast=False)
    assert len(result) > 0

    my_document = html.fromstring("<html><body><div><span>Text.</span></div></body></html>")
    assert extract(copy(my_document), favor_precision=True, fast=True, config=ZERO_CONFIG) == ""
    assert extract(copy(my_document), favor_recall=True, fast=True, config=ZERO_CONFIG) == "Text."


def test_url_blacklist():
    "A document whose canonical URL is blacklisted is rejected."
    doc = '<html><head><link rel="canonical" href="https://example.org/page"/></head><body><article><p>Some real article body text here.</p></article></body></html>'
    assert extract(doc, config=ZERO_CONFIG) is not None
    assert extract(doc, url_blacklist={"https://example.org/page"}, config=ZERO_CONFIG) is None


def test_recover_wild_text_default_tags():
    "recover_wild_text with default tags in recall mode must not crash (frozenset .update())"
    from trafilatura.main_extractor import recover_wild_text

    options = core.Extractor(recall=True)
    tree = html.fromstring("<body><div>some wild text outside the main frame, long enough to be recovered</div></body>")
    result = recover_wild_text(tree, etree.Element("body"), options)
    assert result is not None


_MED_REF = '<ref target="/x">' + "x" * 250 + "</ref>"
_BIG_REF = '<ref target="/x">' + "x" * 600 + "</ref>"
# 60% link density at ~600 chars: kept by the 0.8 (medium) threshold, removed by the 0.5 (large) threshold
_STRADDLE_REF = '<ref target="/x">' + "x" * 360 + "</ref>"


@pytest.mark.parametrize(
    "html_str,expected",
    [
        # medium table (<1000 chars): 80% link threshold
        (f"<table><cell>{'y' * 50}{_MED_REF}</cell></table>", True),  # 83% links → removed
        (f"<table><cell>{'y' * 200}{_MED_REF}</cell></table>", False),  # 56% links → kept
        # straddle table (500-999 chars): 60% links — kept by 0.8 threshold, removed by 0.5 (guards the 1000-char boundary)
        (f"<table><cell>{'y' * 240}{_STRADDLE_REF}</cell></table>", False),  # 60% links, ~600 chars → kept
        # large table (>=1000 chars): 50% link threshold
        (f"<table><cell>{'y' * 400}{_BIG_REF}</cell></table>", True),  # 60% links → removed
        (f"<table><cell>{'y' * 600}{_BIG_REF}</cell></table>", False),  # 40% links → kept
    ],
)
def test_link_density_tables_threshold(html_str: str, expected: bool) -> None:
    assert trafilatura.htmlprocessing.link_density_test_tables(html.fromstring(html_str)) is expected


def test_link_density_tables_textless_links_kept() -> None:
    "A text-rich table whose only own-depth ref is a textless icon link is not boilerplate (#lineups)."
    # 250 chars of real text + one image-wrapping link with no text -> elemnum 0, must be kept
    icon_table = html.fromstring(
        "<table><cell>" + "data " * 50 + '<ref target="/x"><graphic src="/i.png"/></ref></cell></table>'
    )
    assert trafilatura.htmlprocessing.link_density_test_tables(icon_table) is False


def test_is_in_table_cell():
    "is_in_table_cell must check real ancestry, not 'a cell exists somewhere' (#767)."
    tree = etree.fromstring("<body><table><row><cell><p>inside</p></cell></row></table><p>outside</p></body>")
    inside = tree.xpath(".//cell/p")[0]
    outside = tree.xpath("./p")[0]
    assert is_in_table_cell(inside) is True
    assert is_in_table_cell(outside) is False  # buggy '//ancestor::cell' would return True


_COLSPAN_CONTENT_BASE = "<tr><td>a</td><td>b</td><td>c</td></tr>"
_COLSPAN_CONTENT_ROW = "<tr><td>a</td><td colspan='2'><p>b</p><p>c</p></td></tr>"


@pytest.mark.parametrize(
    "rows,expected",
    [
        (1, "| a | b | c | \n| a | b c |  |"),
        (2, "| a | b | c | \n| a | b c |  | \n| a | b c |  |"),
    ],
    ids=["one-colspan-row", "two-colspan-rows"],
)
def test_table_colspan_content(rows, expected):
    "A colspan=2 cell with block children is flattened; the placeholder fills to max_cols."
    html_str = (
        f"<html><body><article><table>{_COLSPAN_CONTENT_BASE}{_COLSPAN_CONTENT_ROW * rows}</table></article></body></html>"
    )
    assert extract(html_str, fast=True, output_format="txt", config=ZERO_CONFIG, include_tables=True) == expected


def test_table_processing(options):
    # regression: comments/PIs in a <table> have a read-only .tag and must not crash handle_table
    table_with_comment = html.fromstring("<table><!-- c1 --><tr><td>cell text<!-- c2 --></td></tr></table>")
    processed = handle_table(table_with_comment, TAG_CATALOG, options)
    assert processed is not None and "cell text" in "".join(processed.itertext())

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
    table_cell_with_children = html.fromstring("<table><tr><td><p>text</p><p>more text</p></td></tr></table>")
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
    processed = extract(htmlstring, fast=True, output_format="xml", config=ZERO_CONFIG, include_links=True)
    result = processed.replace("\n", "").replace(" ", "")
    assert (
        """<table><row><cell>text<headrend="h4">more_text</head></cell><cell><reftarget="link">linktext</ref></cell></row></table>"""
        in result
    )

    # multi-row table with <a> in every cell must keep all rows and link text
    # (regression: handle_formatting detached the ref mid-iteration, collapsing
    # subsequent rows into wild text, see issue #794)
    multi_row_links = """<html><body><article>
        <p>Enough intro text to satisfy trafilatura's minimum extraction length requirements for this test.</p>
        <table>
            <tr><th>Key</th><th>Value</th></tr>
            <tr><td><a href="/k1">Coord</a>:</td><td><a href="/v1">48 N</a></td></tr>
            <tr><td><a href="/k2">State</a>:</td><td><a href="/v2">BW</a></td></tr>
            <tr><td><a href="/k3">Region</a>:</td><td><a href="/v3">Stuttgart</a></td></tr>
        </table>
    </article></body></html>"""
    md = extract(multi_row_links, output_format="markdown", include_tables=True, include_links=True, config=ZERO_CONFIG)
    for key, href, value in [("Coord", "/k1", "48 N"), ("State", "/k2", "BW"), ("Region", "/k3", "Stuttgart")]:
        assert f"[{key}]({href})" in md
        assert value in md

    table_cell_w_text_and_child = html.fromstring("<table><tr><td>text<lb/><p>more text</p></td></tr></table>")
    processed_table = handle_table(table_cell_w_text_and_child, TAG_CATALOG, options)
    assert etree.tostring(processed_table, encoding="unicode") == "<table><row><cell>text<p>more text</p></cell></row></table>"
    table_cell_with_link = html.fromstring("<table><tr><td><ref target='test'>link</ref></td></tr></table>")
    processed_table = handle_table(table_cell_with_link, TAG_CATALOG, options)
    result = [child.tag for child in processed_table.find(".//cell").iterdescendants()]
    # the ref is kept inside the cell instead of being wrapped in a <p>,
    # which previously detached it and broke the table (see issue #794)
    assert result == ["ref"]
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
    processed_table = handle_table(table_with_head, TAG_CATALOG, options)
    first_row = processed_table[0]
    assert len(processed_table) == 3
    assert [(child.tag, child.attrib, child.text) for child in first_row.iterdescendants()] == [
        ("cell", {"role": "head"}, "Month"),
        ("cell", {"role": "head"}, "Days"),
    ]

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
    assert len(first_row) == 4  # Name, Adress, Phone, Phone-colspan-placeholder
    assert {child.tag for child in first_row.iterdescendants()} == {"cell"}
    table_cell_with_hi = html.fromstring("<table><tr><td><hi>highlighted text</hi></td></tr></table>")
    processed_table = handle_table(table_cell_with_hi, TAG_CATALOG, options)
    result = etree.tostring(processed_table.find(".//cell"), encoding="unicode")
    assert result == "<cell><hi>highlighted text</hi></cell>"
    table_cell_with_span = html.fromstring("<table><tr><td><span style='sth'>span text</span></td></tr></table>")
    processed_table = handle_table(table_cell_with_span, TAG_CATALOG, options)
    result = etree.tostring(processed_table.find(".//cell"), encoding="unicode")
    assert result == "<cell><p/></cell>"
    # tables with nested elements
    htmlstring = """<html><body><article>
<table>
<tr><td><b>Present Tense</b></td>
<td>I buy</td>
<td>you buy</td>
<td>he/she/it buys</td>
<td>we buy</td>
<td>you buy</td>
<td>they buy</td>
</tr>
    </table></article></body></html>"""
    my_result = extract(htmlstring, fast=True, output_format="xml", include_formatting=True, config=ZERO_CONFIG)
    assert (
        """<row>
        <cell>
          <hi rend="#b">Present Tense</hi>
        </cell>
        <cell>I buy</cell>
        <cell>you buy</cell>
        <cell>he/she/it buys</cell>
        <cell>we buy</cell>
        <cell>you buy</cell>
        <cell>they buy</cell>
      </row>"""
        in my_result
    )
    assert extract(htmlstring, fast=True, output_format="txt", config=ZERO_CONFIG).startswith(
        "| Present Tense | I buy | you buy |"
    )
    # table with links
    table = '<table><tr><td><a href="test.html">' + "ABCD" * 100 + "</a></td></tr></table>"
    result = _extract_doc(table, intro=False, fast=True, output_format="xml", include_tables=True, include_links=True)
    assert "ABCD" not in result
    # malformed source: <th> and inner <table> are siblings, not parent/child;
    # pipeline extracts them as two separate flat tables, not one nested structure
    table = "<table><th>1</th><table><tr><td>2</td></tr></table></table>"
    result = _extract_doc(table, intro=False, fast=True, output_format="xml", include_tables=True)
    assert '<cell role="head">1</cell>' in result and "<cell>2</cell>" in result
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
    # handle_table processes only the outer table and drops the inner one; the extraction
    # walk re-extracts it as a sibling (embedding caused duplication — see T7)
    processed_table = handle_table(nested_table, TAG_CATALOG, options)
    result = [(el.tag, el.text) if el.text is not None and el.text.strip() else el.tag for el in processed_table.iter()]
    assert result == ["table", "row", "cell"]
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
    result = [(el.tag, el.text) if el.text is not None and el.text.strip() else el.tag for el in processed_table.iter()]
    assert result == ["table", "row", "cell", ("cell", "text1"), "row", ("cell", "text2"), "cell"]
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
    """
    )
    processed_table = handle_table(copy(table_with_list), TAG_CATALOG, options)
    result = [(el.tag, el.text) if el.text is not None and el.text.strip() else el.tag for el in processed_table.iter()]
    assert result == ["table", "row", "cell", ("p", "a list"), "list"]

    options.focus = "recall"
    processed_table = handle_table(copy(table_with_list), TAG_CATALOG, options)
    result = [(el.tag, el.text) if el.text is not None and el.text.strip() else el.tag for el in processed_table.iter()]
    assert result == [
        "table",
        "row",
        "cell",
        ("p", "a list"),
        "list",
        ("item", "one"),
        ("item", "two"),
    ]

    broken_table = html.fromstring("<table><td>cell1</td><tr><td>cell2</td></tr></table>")
    processed_table = handle_table(broken_table, TAG_CATALOG, options)
    result = [el.tag for el in processed_table.iter()]
    assert result == ["table", "row", "cell", "row", "cell"]
    broken_table = html.fromstring("<table><tr><p>text</p></tr><tr><td>cell</td></tr></table>")
    processed_table = handle_table(broken_table, TAG_CATALOG, options)
    result = [el.tag for el in processed_table.iter()]
    assert result == [
        "table",
        "row",
        "cell",
    ]
    # colgroup/col tests live in test_table_colgroup_no_crash (parametrized)
    # table nested in figure https://github.com/adbar/trafilatura/issues/301
    table = "<figure><table><th>1</th><tr><td>2</td></tr></table></figure>"
    result = _extract_doc(table, intro=False, fast=True, output_format="xml", include_tables=True)
    assert "1" in result and "2" in result
    # table headers in non-XML formats
    table = "<table><tr><th>head 1</th><th>head 2</th></tr><tr><td>1</td><td>2</td></tr></table>"
    assert "|---|---|" in _table_txt(table)
    # regression: a header row's separator must match the column count even with no body row (was "|---|")
    single_header = "<table><tr><th>a</th><th>b</th><th>c</th></tr></table>"
    assert "|---|---|---|" in _table_txt(single_header)

    # remove new lines in table cells in text format
    table = "<table><tr><td>cell<br>1</td><td>cell<p>2</p></td></tr></table>"
    assert "| cell 1 | cell 2 |" in _table_txt(table)

    # only one header row is allowed in text format
    table = "<table><tr><th>a</th><th>b</th></tr><tr><th>c</th><th>d</th></tr></table>"
    assert _table_txt(table).count("---|") == 2

    # colspan/span handling lives in test_table_colspan_* (parametrized)

    # links: this gets through (for now)
    table = '<table><tr><td><a href="link.html">a</a></td></tr></table>'
    assert _table_txt(table) == "| a |"

    # link: this is filtered out
    assert _table_txt(f'<table><tr><td><a href="link.html">{"abc" * 100}</a></td></tr></table>') == ""
    assert _table_txt(f'<table><tr><td><a href="link.html">{" " * 100}</a></td></tr></table>') == ""

    # image markdown tests live in test_table_image_in_cell (parametrized)


_IMG_URL = "http://aa.bb/c.jpg"
_IMG_TABLE_HEADER = "<tr><td>a</td><td>b</td><td>c</td></tr>"
_IMG_TABLE_TAIL = "<td><p>b</p><p>c</p></td><td>d</td>"


@pytest.mark.parametrize(
    "cell1,expected_cell1",
    [
        (
            f'<td>a<img src="{_IMG_URL}" alt="img"/><span>a</span></td>',
            f"a ![img]({_IMG_URL}) a",
        ),
        (
            f'<td><a href="{_IMG_URL}"><img src="{_IMG_URL}" alt="img"/><span>a</span></a></td>',
            f"![img]({_IMG_URL}) a",
        ),
        (
            f'<td><img src="{_IMG_URL}" alt="img"/><span>a</span></td>',
            f"![img]({_IMG_URL}) a",
        ),
        (
            f'<td><img src="{_IMG_URL}" alt="img1"/><span>a</span><img src="{_IMG_URL}" alt="img2"/></td>',
            f"![img1]({_IMG_URL}) a ![img2]({_IMG_URL})",
        ),
    ],
    ids=["text-img-span", "linked-img-span", "img-span", "two-imgs"],
)
def test_table_image_in_cell(cell1, expected_cell1):
    "Images in table cells render as GFM inline images; link wrapping is preserved."
    html_str = (
        f"<html><body><article><table>{_IMG_TABLE_HEADER}<tr>{cell1}{_IMG_TABLE_TAIL}</tr></table></article></body></html>"
    )
    result = extract(
        html_str, fast=True, output_format="markdown", config=ZERO_CONFIG, include_images=True, include_tables=True
    )
    assert result == f"| a | b | c | \n| {expected_cell1} | b c | d |"


# link + bold paragraph, plus a table cell with a link/bold and an image cell — shared by the combo tests
_COMBO_DOC = (
    "<html><body><article>"
    '<p>Intro with a <a href="http://x.io/p">link</a> and <b>bold</b> word.</p>'
    "<table><tr><td>h1</td><td>h2</td></tr>"
    '<tr><td><a href="http://x.io/c"><b>bold link</b></a></td>'
    '<td><img src="http://x.io/i.jpg" alt="pic"/></td></tr></table>'
    "</article></body></html>"
)
_COMBO_ALL_ON = dict(include_links=True, include_formatting=True, include_images=True, include_tables=True)


def test_combined_links_formatting_images_tables():
    "All four flags on: cells keep formatting + images, and a link wrapping formatting keeps its target."
    result = extract(_COMBO_DOC, output_format="markdown", config=ZERO_CONFIG, **_COMBO_ALL_ON)
    assert result == (
        "Intro with a [link](http://x.io/p) and **bold** word.\n\n"
        "| h1 | h2 | \n| [**bold link**](http://x.io/c) | ![pic](http://x.io/i.jpg) |"
    )


@pytest.mark.parametrize(
    "off,expected",
    [
        (
            "include_links",
            "Intro with a link and **bold** word.\n\n| h1 | h2 | \n| **bold link** | ![pic](http://x.io/i.jpg) |",
        ),
        (
            "include_formatting",
            "Intro with a [link](http://x.io/p) and bold word.\n| h1 | h2 | \n| [bold link](http://x.io/c) | ![pic](http://x.io/i.jpg) |",
        ),
        (
            "include_images",
            "Intro with a [link](http://x.io/p) and **bold** word.\n\n| h1 | h2 | \n| [**bold link**](http://x.io/c) |  |",
        ),
        ("include_tables", "Intro with a [link](http://x.io/p) and **bold** word."),
    ],
)
def test_combined_flags_toggle_off(off, expected):
    "Pin current behavior: disabling one flag changes only its feature (combined doc)."
    result = extract(_COMBO_DOC, output_format="markdown", config=ZERO_CONFIG, **{**_COMBO_ALL_ON, off: False})
    assert result == expected


# first-row tail cell + a 3-cell second row that sets the table to 3 columns;
# the first row fills to 3 via a colspan placeholder or a trailing pad depending on the span
_COLSPAN_ROWS = "<td>b</td></tr><tr><td>c</td><td>d</td><td>e</td></tr></table>"


def test_table_colspan_padding():
    "A colspan=2 cell materializes an inline placeholder; the row fills to the table's column count."
    assert "| a |  | b |" in _table_txt(f"<table><tr><td colspan='2'>a</td>{_COLSPAN_ROWS}")


@pytest.mark.parametrize("bad_span", ['span="2"', 'span="2.1"', 'span="-1"', 'span="abc"'])
def test_table_bad_span_attr_treated_as_colspan1(bad_span):
    "Non-colspan span attributes are ignored (colspan=1); trailing pad fills to max_cols."
    assert "| a | b |  |" in _table_txt(f"<table><tr><td {bad_span}>a</td>{_COLSPAN_ROWS}")


@pytest.mark.parametrize(
    "first_cell", ['<td colspan="9007199254740991">a</td>', '<th colspan="9007199254740991">a</th>', '<td colspan="2x">a</td>']
)
def test_table_huge_or_bad_colspan_no_crash(first_cell):
    "Huge or non-numeric colspan must not crash or discard the document (#657)."
    assert _table_txt(f"<table><tr>{first_cell}{_COLSPAN_ROWS}") is not None


@pytest.mark.parametrize(
    "colspan,expected",
    [("1", 1), ("3", 3), ("12", 12), ("²", 1), ("1²", 1), ("2x", 1), ("", 1), ("-2", 1)],
)
def test_colspan_zero_trust(colspan, expected):
    "_span must default to 1 for non-decimal values (isdigit() admits superscripts that int() rejects)."
    assert _span(html.fromstring(f'<td colspan="{colspan}">x</td>'), "colspan") == expected


def test_table_rowspan_aligned():
    "A rowspan=2 cell leaves a placeholder in the continuation row so columns stay aligned."
    assert _table_md("<table><tr><td rowspan='2'>x</td><td>a</td></tr><tr><td>b</td></tr></table>").endswith(
        "| x | a | \n|  | b |"
    )


def test_table_rowspan_colspan_combined():
    "A cell with both rowspan and colspan registers all spanned columns in the rowspan map."
    # Col 0-1 spanned by rowspan=2 colspan=2 cell; row 2 must have 2 phantoms then 1 real cell.
    result = _table_md("<table><tr><td rowspan='2' colspan='2'>big</td><td>c</td></tr><tr><td>x</td></tr></table>")
    # Row 2: 2 phantoms (cols 0-1 rowspan-occupied) + real cell x at col 2
    assert "|  |  | x |" in result


def test_table_rowspan_decrement_on_padding():
    "Rowspan entry is decremented when a short row is padded, so it does not bleed into subsequent rows."
    # Col 1 has rowspan=2; row 2 is short (only col 0 filled). Row 3 must not receive a stale phantom.
    result = _table_md(
        "<table>"
        "<tr><td>a</td><td rowspan='2'>b</td><td>c</td></tr>"
        "<tr><td>x</td></tr>"
        "<tr><td>d</td><td>e</td><td>f</td></tr>"
        "</table>"
    )
    assert "| d | e | f |" in result


@pytest.mark.parametrize(
    "html,suffix",
    [
        ("<table><tr><td></td><td>b</td></tr></table>", "|  | b |"),
        ("<table><tr><td>a</td><td></td></tr></table>", "| a |  |"),
        ("<table><tr><td>a</td><td>b</td></tr><tr><td></td><td></td></tr></table>", "| a | b |"),
        (
            "<table><tr><td>a</td><td>c</td></tr><tr><td></td><td></td></tr><tr><td>d</td><td>e</td></tr></table>",
            "| a | c | \n| d | e |",
        ),
        (
            "<table><tr><td>a</td><td>c</td></tr><tr></tr><tr><td>d</td><td>e</td></tr></table>",
            "| a | c | \n| d | e |",
        ),
    ],
    ids=["leading-empty", "trailing-empty", "all-empty-row-dropped", "empty-row-middle", "empty-tr"],
)
def test_table_empty_cells_and_rows(html, suffix):
    "Empty cells are kept blank to keep columns aligned; rows that are entirely empty are dropped."
    assert _table_md(html).endswith(suffix)


def test_table_cell_list_no_row_break():
    "A <ul> in a cell (no recall mode) must not inject a row-breaking newline."
    row = _table_md("<table><tr><td><ul><li>i1</li><li>i2</li></ul></td><td>b</td></tr></table>").split("\n\n")[-1]
    assert "\n" not in row and row.endswith("| b |")


@pytest.mark.parametrize(
    "html,suffix,kwargs",
    [
        ("<table><tr><td><h2>Title</h2></td><td>b</td></tr></table>", "| Title | b |", {}),
        ("<table><tr><td><p>para</p></td><td>b</td></tr></table>", "| para | b |", {}),
        ("<table><tr><td><h2>Title</h2>txt</td><td>b</td></tr></table>", "| Title txt | b |", {}),
        (
            "<table><tr><td><ul><li>i1</li><li>i2</li></ul></td><td>b</td></tr></table>",
            "| i1 i2 | b |",
            {"favor_recall": True},
        ),
    ],
    ids=["heading", "paragraph", "heading-plus-tail", "list-recall"],
)
def test_table_cell_block_elements_flattened(html, suffix, kwargs):
    "Block elements in a cell are flattened to inline: no ## marker, space-separated, no mashing."
    assert _table_md(html, **kwargs).endswith(suffix)


@pytest.mark.parametrize(
    "expected,cell,kwargs",
    [
        ("**bold**", "<p><b>bold</b></p>", {"include_formatting": True}),
        ("![a](/i.jpg)", "<p><img src='/i.jpg' alt='a'></p>", {"include_images": True}),
        ("pre **mid** post", "<p>pre <b>mid</b> post</p>", {"include_formatting": True}),
        ("x ~~gone~~ y", "<p>x <del>gone</del> y</p>", {"include_formatting": True}),
        ("x `c` y", "<p>x <code>c</code> y</p>", {"include_formatting": True}),
    ],
)
def test_table_cell_keeps_nested_formatting(expected, cell, kwargs):
    "regression #829/#396: formatting/images wrapped in a block inside a cell must survive."
    assert expected in _table_md(f"<table><tr><td>{cell}</td><td>x</td></tr></table>", **kwargs)


def test_include_images_does_not_truncate():
    "regression #194/#842: a lead image plus one paragraph must not let _extract break early and drop later content."
    # real config + a >250-char lead so wild-text recovery does not fire and mask the early break
    real_config = use_config()
    lead = "This single lead paragraph is deliberately long enough to exceed the minimum extracted size. " * 4
    doc = (
        "<html><body>"
        f"<article><img src='/lead.jpg' alt='lead'><p>{lead}</p></article>"
        "<div id='content'>"
        + "".join(f"<p>Continuation paragraph {i} that must also survive extraction in full here.</p>" for i in range(1, 5))
        + "</div></body></html>"
    )
    result = extract(doc, output_format="txt", include_images=True, config=real_config) or ""
    assert "/lead.jpg" in result
    assert all(f"Continuation paragraph {i}" in result for i in range(1, 5))


def test_no_duplicate_content():
    "regression #768/#817: content must not be emitted twice (overlapping candidates / wild-text recovery)."
    # real config: ZERO_CONFIG's min_extracted_size=0 hides #817
    real_config = use_config()
    dup768 = "<!doctype html><body><main><article><div><br>Line that has to have at least 125 characters for the bug to appear so here is some filler text text text text text text text</div></article></main></body></html>"
    assert (extract(dup768, output_format="txt", config=real_config) or "").count("Line that has to have") == 1
    dup817 = "<html><body><div id='content'><p>Authoritative taxonomy of but let us leave it as it is 1 2 3</p></div><p>some text long enough not to skip and printed twice on this line some text long enough not to skip and printed twice on this line</p></body></html>"
    assert (extract(dup817, output_format="txt", config=real_config) or "").count("Authoritative taxonomy") == 1


def test_list_item_block_child_single_bullet():
    "regression: a list item wrapping content in a block gets one bullet, not one per child."
    assert _md_inline("<ul><li><p>x <b>bold</b> y</p></li></ul>") == f"{_INTRO}\n\n- x **bold** y"


def test_list_item_image_gets_bullet():
    "regression: an image alone in a list item gets a bullet like text items."
    result = _extract_doc("<ul><li><img src='/i.jpg' alt='a'></li><li>plain</li></ul>", include_images=True)
    assert "- ![a](/i.jpg)\n" in result  # bulleted, no trailing space


@pytest.mark.parametrize(
    "snippet,expected",
    [
        ("<b> x </b>", "**x**"),
        ("<i> x </i>", "*x*"),
        ("<del> x </del>", "~~x~~"),
        ("<code> x </code>", "`x`"),
    ],
)
def test_inline_marker_flanking_whitespace(snippet, expected):
    "regression #843: flanking whitespace stays outside markdown markers (valid CommonMark)."
    assert _md_inline(f"<p>a {snippet} b</p>") == f"{_INTRO}\n\na  {expected}  b"


def test_inline_marker_edge_cases():
    "regression #843: whitespace-only inline drops the marker; a link keeps flanking space outside [..](..)."
    assert _md_inline("<p>a <b>   </b> b</p>") == f"{_INTRO}\n\na     b"
    assert (
        _md_inline("<p>see <a href='/x'> bold link </a> ok</p>", include_links=True) == f"{_INTRO}\n\nsee  [bold link](/x)  ok"
    )


def test_ordered_list_numbering():
    "regression #843 family: ordered lists render as 1. 2. 3., unordered lists keep '- '."
    assert _md_inline("<ol><li>one</li><li>two</li><li>three</li></ol>") == f"{_INTRO}\n\n1. one\n2. two\n3. three"
    assert _md_inline("<ol><li>only</li></ol>") == f"{_INTRO}\n\n1. only"
    assert _md_inline("<ul><li>a</li><li>b</li></ul>") == f"{_INTRO}\n\n- a\n- b"


def test_nested_list_indentation():
    "regression A5: a nested list is indented and starts on its own line, not mashed onto the parent item."
    assert _md_inline("<ul><li>a<ul><li>b</li><li>c</li></ul></li><li>d</li></ul>") == f"{_INTRO}\n\n- a\n  - b\n  - c\n- d"
    assert _md_inline("<ul><li>a<ol><li>b</li></ol></li></ul>") == f"{_INTRO}\n\n- a\n  1. b"


def test_loose_text_tail_not_squished():
    "regression #661: a block's loose-text tail must not mash onto the next sibling block."
    html_string = """<!DOCTYPE html><html lang="en-us"><body><main><section>
        <p>First</p>
        This gets Squished
        <div>
            <h4>There should be a space</h4>
            <p>Another sentence</p>
            This also gets Squished
        </div>
        <div>
            <h4>Where is the space</h4>
            <p>This sentence has to be long enough. If it's long enough the duplication stops, but if it's not long enough then you'll get an extra first. This sentence has to be long enough.</p>
        </div>
    </section></main></body></html>"""
    result = extract(html_string) or ""
    assert "SquishedThere" not in result and "SquishedWhere" not in result


@pytest.mark.parametrize(
    "rend,expected",
    [
        ("h1", "# T"),
        ("h2", "## T"),
        ("h6", "###### T"),
        (None, "## T"),  # absent -> default level 2
        ("", "## T"),
        ("h", "## T"),  # no digit
        ("hx", "## T"),  # non-digit
        ("h²", "## T"),  # superscript: isdigit() True but int() raises -> must not crash
        ("h٤", "## T"),  # non-ASCII decimal digit -> not an accepted level
        ("h0", "## T"),  # out of range
        ("h9", "## T"),  # out of range
    ],
)
def test_heading_level_zero_trust(rend, expected):
    "replace_element_text must never crash on a malformed head rend and defaults to level 2."
    el = etree.Element("head")
    el.text = "T"
    if rend is not None:
        el.set("rend", rend)
    assert xml.replace_element_text(el, True) == expected


def test_table_nested_in_cell():
    "Single-row nested table in a row with no other content is left for the outer walk, not inlined."
    doc = "<table><tr><td>A</td></tr><tr><td><table><tr><td>inner</td></tr></table></td></tr><tr><td>AFTER</td></tr></table>"
    texts = list(handle_table(html.fromstring(doc), TAG_CATALOG, core.Extractor()).itertext())
    assert "A" in texts and "AFTER" in texts and "inner" not in texts


def test_table_nested_in_cell_pipeline():
    "End-to-end: nested table is extracted as a separate table by the main walk, not inlined — no duplication."
    outer_text = "This is the outer row with plenty of text to survive readability. " * 2
    inner_text = "Inner nested table cell with sufficient content for extraction. " * 2
    doc = f"<table><tr><td>{outer_text}</td></tr><tr><td><table><tr><td>{inner_text}</td></tr></table></td></tr></table>"
    # intro=True ensures readability selects the full <article> (not just one <tr>)
    result = _extract_doc(doc, intro=True, output_format="xml", include_tables=True)
    assert outer_text.strip()[:20] in result
    assert inner_text.strip()[:20] in result
    # no duplication: inner text appears in exactly one cell
    assert result.count(inner_text.strip()) == 1


def test_table_nested_tail_preserved():
    "Tail text between </table> and next element in the same cell must not be dropped."
    doc = "<table><tr><td>before<table><tr><td>inner</td></tr></table>after-tail</td></tr></table>"
    result = handle_table(html.fromstring(doc), TAG_CATALOG, core.Extractor())
    texts = "".join(result.itertext())
    assert "before" in texts and "after-tail" in texts and "inner" not in texts


def test_table_nested_tail_with_prior_child():
    "Nested-table tail text is appended to the last child when new_child_elem already has children."
    doc = "<table><tr><td><del>struck</del><table><tr><td>inner</td></tr></table>after-tail</td></tr></table>"
    texts = "".join(handle_table(html.fromstring(doc), TAG_CATALOG, core.Extractor()).itertext())
    assert "after-tail" in texts and "inner" not in texts


def test_table_comment_in_row():
    "Comment nodes inside <tr> are skipped without crashing."
    doc = "<table><tr><!-- ignored --><td>visible</td></tr></table>"
    assert handle_table(html.fromstring(doc), TAG_CATALOG, core.Extractor()).find(".//cell").text == "visible"


def test_table_caption():
    "Table caption is emitted as a header row above the table body."
    result = _table_md("<table><caption>My Caption</caption><tr><td>a</td><td>b</td></tr></table>")
    assert "My Caption" in result
    # caption row appears before the body row
    assert result.index("My Caption") < result.index("| a |")
    # separator must span all columns (2), not just the caption cell (1)
    assert "|---|---|" in result
    # whitespace-only caption is silently skipped; body row still extracted
    opts = core.Extractor()
    result2 = handle_table(html.fromstring("<table><caption>  </caption><tr><td>x</td></tr></table>"), TAG_CATALOG, opts)
    assert result2 is not None and result2.find(".//cell").text == "x"
    assert all(c.get("role") != "head" for c in result2.iter("cell"))


def test_table_orphan_cells_no_tr():
    "A table with no <tr> at all (only orphan td/th children) still extracts."
    result = handle_table(html.fromstring("<table><td>a</td><td>b</td></table>"), TAG_CATALOG, core.Extractor())
    assert [c.text for c in result.iter("cell")] == ["a", "b"]


def test_table_stray_cell_descendant():
    "A td/th nested inside a non-table element within a cell is renamed to <cell> and extracted."
    result = handle_table(
        html.fromstring("<table><tr><td><div><td>inner</td></div></td></tr></table>"),
        TAG_CATALOG,
        core.Extractor(),
    )
    assert any(c.text == "inner" for c in result.iter("cell"))


@pytest.mark.parametrize(
    "colgroup_html",
    [
        "<table><colgroup><col style='width:50%'><col style='width:50%'></colgroup><tr><td>a</td><td>b</td></tr></table>",
        "<table><col span='2'><tr><td>x</td><td>y</td></tr></table>",
        "<table><col><td>orphan</td><tr><td>normal</td></tr></table>",
    ],
    ids=["colgroup", "col-span", "col-orphan-td"],
)
def test_table_colgroup_no_crash(colgroup_html):
    "colgroup/col as direct table children are layout hints; must not crash and all cells must have text."
    result = handle_table(html.fromstring(colgroup_html), TAG_CATALOG, core.Extractor())
    assert all(c.text for c in result.iter("cell"))


@pytest.mark.parametrize("role", ["presentation", "none"])
def test_aria_layout_table_reclassified(role):
    "Any table with role=presentation/none is reclassified as div (explicit WAI-ARIA layout declaration)."
    from trafilatura.htmlprocessing import tree_cleaning

    opts = core.Extractor()
    opts.tables = True
    # with nested table: outer reclassified, inner kept
    doc = html.fromstring(
        f'<html><body><table role="{role}"><tr><td><table><tr><td>data</td></tr></table></td></tr></table></body></html>'
    )
    tree_cleaning(doc, opts)
    assert doc.find(".//table[@role]") is None
    assert doc.find(".//table") is not None
    # without nested table: also reclassified
    doc = html.fromstring(f'<html><body><table role="{role}"><tr><td>text</td></tr></table></body></html>')
    tree_cleaning(doc, opts)
    assert doc.find(".//table") is None


def test_sanitize_tree_th_dedup():
    "sanitize_tree marks only the first <th>-containing row per parent as role=head; subsequent th-rows are plain cells."
    from trafilatura.external import sanitize_tree

    opts = core.Extractor()
    opts.tables = True
    # two <th> rows: only the first should get role="head"
    doc = html.fromstring(
        "<html><body><table>"
        "<tr><th>A</th><th>B</th></tr>"
        "<tr><th>C</th><th>D</th></tr>"
        "<tr><td>1</td><td>2</td></tr>"
        "</table></body></html>"
    )
    tree, _, _ = sanitize_tree(doc, opts)
    head_cells = tree.xpath('.//cell[@role="head"]')
    plain_cells = [c for c in tree.xpath(".//cell") if c.get("role") != "head"]
    assert len(head_cells) == 2  # only A and B
    assert all(c.text in ("A", "B") for c in head_cells)
    assert all(c.text in ("C", "D", "1", "2") for c in plain_cells)
    # regression: a table with no <th> at all must not crash and produces no head cells
    doc2 = html.fromstring("<html><body><table><tr><td>x</td></tr></table></body></html>")
    tree2, _, _ = sanitize_tree(doc2, opts)
    assert tree2.xpath('.//cell[@role="head"]') == []


def test_list_item_attr_whitelist():
    "Nested elements in a list item keep meaningful attrs only (no stray class/width leak)."
    body = '<ul><li>x <img src="p.jpg" class="c" width="9" alt="a"/> <a href="http://x.io" class="q">lnk</a> y</li></ul>'
    out = _extract_doc(body, output_format="xml", include_links=True, include_images=True, favor_recall=True)
    assert '<graphic src="p.jpg" alt="a"/>' in out  # class/width dropped
    assert "class=" not in out and "width=" not in out
    assert '<ref target="http://x.io">' in out  # target kept


def test_image_tail_not_duplicated():
    "regression: an image's tail text must not be emitted twice outside a table cell."
    result = _extract_doc("<ul><li>a <img src='i.jpg' alt='A'/> b</li></ul>", include_images=True)
    assert result.endswith("a ![A](i.jpg) b")


def test_list_item_link_with_inline_formatting():
    "regression: a link whose only content is a bold/del/code span must not drop the href in list items."
    # bold-only link: <a href="url"><b>text</b></a>  -> [**text**](url) not just **text**
    assert (
        _md_inline(
            "<ul><li>see <a href='http://x.com'><b>bold link</b></a> here</li></ul>",
            include_links=True,
        )
        == f"{_INTRO}\n\n- see [**bold link**](http://x.com) here"
    )
    # link with mixed text+bold: <a href="url">text <b>bold</b></a>
    assert (
        _md_inline(
            "<ul><li>see <a href='http://x.com'>link <b>bold</b></a> here</li></ul>",
            include_links=True,
        )
        == f"{_INTRO}\n\n- see [link **bold**](http://x.com) here"
    )


def test_paragraph_link_with_inline_formatting():
    "regression: <p><a href><b>bold</b></a></p> must preserve both the link and the formatting."
    assert (
        _md_inline(
            "<p>see <a href='http://x.com'><b>bold</b></a> more</p>",
            include_links=True,
        )
        == f"{_INTRO}\n\nsee [**bold**](http://x.com) more"
    )


def test_nested_inline_formatting():
    "regression: nested inline elements must compose markers correctly."
    # <b><i>x</i></b> → ***x***
    assert _md_inline("<p>text <b><i>nested</i></b> end</p>") == f"{_INTRO}\n\ntext ***nested*** end"
    # <b>prefix <i>italic</i></b> → **prefix *italic***
    assert _md_inline("<p><b>prefix <i>italic</i></b></p>") == f"{_INTRO}\n\n**prefix *italic***"
    # list item context
    assert _md_inline("<ul><li>text <b><i>nested</i></b> end</li></ul>") == f"{_INTRO}\n\n- text ***nested*** end"


def test_blockquote_bare_inline():
    "regression: bare inline element directly in blockquote must preserve its tail text."
    assert _md_inline("<blockquote><b>bold</b> text here</blockquote>") == f"{_INTRO}\n\n**bold** text here"


def test_del_and_code_in_non_paragraph_contexts():
    "del and code inline elements work inside list items, blockquotes, and at the top level."
    # del at top level (bare, no p/blockquote wrapper — exercises FORMATTING routing)
    assert _md_inline("<del>gone</del>") == f"{_INTRO}\n\n~~gone~~"
    # del in list item
    assert _md_inline("<ul><li>text <del>struck</del> more</li></ul>") == f"{_INTRO}\n\n- text ~~struck~~ more"
    # del in blockquote
    assert _md_inline("<blockquote>text <del>struck</del> more</blockquote>") == f"{_INTRO}\n\ntext ~~struck~~ more"
    # code in list item
    assert _md_inline("<ul><li>use <code>func()</code> here</li></ul>") == f"{_INTRO}\n\n- use `func()` here"


def test_hi_del_nesting_with_direct_text():
    "bold wrapping strikethrough preserves both markers when the outer hi element has direct text."
    # <b>text<del>struck</del></b> — outer has text 'text', del child is preserved
    assert _md_inline("<p>before <b>bold <del>struck</del></b></p>") == f"{_INTRO}\n\nbefore **bold ~~struck~~**"


def test_list_processing(options):
    # basic lists
    my_doc = "<html><body><article><p>P 1</p><ul><li>Item 1</li><li>Item 2</li></ul><p>P 2</p></article></body></html>"
    my_result = extract(my_doc, fast=True, output_format="txt", config=ZERO_CONFIG)
    assert my_result == "P 1\n- Item 1\n- Item 2\nP 2"
    # malformed lists (common error)
    result = etree.tostring(
        handle_lists(
            etree.fromstring(
                "<list>Description of the list:<item>List item 1</item><item>List item 2</item><item>List item 3</item></list>"
            ),
            options,
        )
    )
    assert result.count(b"List item") == 3
    assert b"Description" in result
    # nested list
    htmlstring = """<html><body><article>
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
</article></body></html>"""
    my_result = extract(htmlstring, fast=True, output_format="xml", config=ZERO_CONFIG)
    expected = """
    <list rend="ul">
      <item>Coffee</item>
      <item>Tea
        <list rend="ul">
          <item>Black tea</item>
          <item>Green tea</item>
        </list>
      </item>
      <item>Milk</item>
    </list>""".replace("\n", "").replace(" ", "")
    assert expected in my_result.replace("\n", "").replace(" ", "")
    # description list
    htmlstring = """<html><body><article>
 <dl>
  <dt>Coffee</dt>
  <dd>Black hot drink</dd>
  <dt>Milk</dt>
  <dd>White cold drink</dd>
</dl>
</article></body></html>"""
    my_result = extract(htmlstring, fast=True, output_format="xml", config=ZERO_CONFIG)
    assert (
        """
    <list rend="dl">
      <item rend="dt-1">Coffee</item>
      <item rend="dd-1">Black hot drink</item>
      <item rend="dt-2">Milk</item>
      <item rend="dd-2">White cold drink</item>
    </list>"""
        in my_result
    )
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
    # list items whose only content is a link must be kept (GH #788)
    htmlstring = """<html><body><article>
<p>If your eye is twitching and you do not have other symptoms, here are some common everyday causes worth knowing about.</p>
<ul>
<li><p><a href="https://example.org/stress">Stress</a></p></li>
<li><p>Fatigue</p></li>
<li><p><a href="https://example.org/strain">Eye strain</a></p></li>
</ul>
</article></body></html>"""
    my_result = extract(htmlstring, fast=True, output_format="markdown", include_links=True, config=ZERO_CONFIG)
    assert "[Stress](https://example.org/stress)" in my_result
    assert "Fatigue" in my_result
    assert "[Eye strain](https://example.org/strain)" in my_result
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
    assert target_element.tail == "tail"


def test_code_blocks():
    highlightjs = """<div class="s-prose js-post-body" itemprop="text">
<p>Code:</p>
<pre class="lang-sql s-code-block"><code class="hljs language-sql">code\n
<span class="hljs-keyword">highlighted</span> more <span class="hljs-keyword">code</span>
</code></pre>
</div>"""
    testresult = extract(highlightjs, config=ZERO_CONFIG, output_format="xml")
    assert "<code>code\n\nhighlighted more code\n</code>" in testresult and "quote" not in testresult
    github = """<div class="highlight highlight-source-shell notranslate position-relative overflow-auto" dir="auto"><pre>$ pip install PyGithub</pre><div class="zeroclipboard-container position-absolute right-0 top-0">
    <clipboard-copy aria-label="Copy" class="ClipboardButton btn js-clipboard-copy m-2 p-0 tooltipped-no-delay" data-copy-feedback="Copied!" data-tooltip-direction="w" value="$ pip install PyGithub" tabindex="0" role="button" style="display: inherit;">
      <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon m-2">
    <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>
      <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-check js-clipboard-check-icon color-fg-success d-none m-2">
    <path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path>
</svg>
    </clipboard-copy>
  </div></div>
    """
    testresult = extract(github, config=ZERO_CONFIG, output_format="xml")
    assert "<code>$ pip install PyGithub</code>" in testresult and "quote" not in testresult
    inline_code = "<div><p>paragraph</p><p>here is <code>some</code> code</p></div>"
    testresult = extract(inline_code, config=ZERO_CONFIG, output_format="xml")
    assert "<code>some</code>" in testresult and "quote" not in testresult
    w3schools = """<div class="w3-example"><h3>Example</h3>
<p>Create a class named Person, use the __init__() function to assign values
for name and age:</p>
<div class="w3-code notranslate pythonHigh"><span class="pythoncolor" style="color:black"><span class="pythonnumbercolor" style="color:red">
</span>  <span class="pythonkeywordcolor" style="color:mediumblue">class</span> Person:<br>&nbsp; <span class="pythonkeywordcolor" style="color:mediumblue">def</span> __init__(self, name, age):<br>&nbsp;&nbsp;&nbsp; <span class="pythonnumbercolor" style="color:red">
</span>  self.name = name<br>&nbsp;&nbsp;&nbsp; self.age = age<br><br>p1 = Person(<span class="pythonstringcolor" style="color:brown">"John"</span>, <span class="pythonnumbercolor" style="color:red">
</span>  <span class="pythonnumbercolor" style="color:red">36</span>)<br><span class="pythonnumbercolor" style="color:red">
</span>  <br><span class="pythonkeywordcolor" style="color:mediumblue">print</span>(p1.name)<br><span class="pythonkeywordcolor" style="color:mediumblue">print</span>(p1.age) </span></div>
</div>"""
    testresult = extract(w3schools, config=ZERO_CONFIG, output_format="xml")
    expected = """<code>
  class Person:<lb/>\xa0 def __init__(self, name, age):<lb/>\xa0\xa0\xa0 
  self.name = name<lb/>\xa0\xa0\xa0 self.age = age<lb/><lb/>p1 = Person("John", 
  36)<lb/>
  <lb/>print(p1.name)<lb/>print(p1.age) </code>"""
    assert expected in testresult and "quote" not in testresult
    pip = """<div><p>Code:</p>
<pre lang="python3"><span class="kn">import</span> <span class="nn">openai</span>
<span class="kn">from</span> <span class="nn">openai_function_call</span> <span class="kn">import</span> <span class="n">openai_function</span></pre></div>"""
    expected = """<code>import openai
from openai_function_call import openai_function</code>"""
    testresult = extract(pip, config=ZERO_CONFIG, output_format="xml")
    assert expected in testresult and "quote" not in testresult
    medium_js = """<div><p>Code:</p>
    <pre class="lw lx ly lz ma nq nr ns bo nt ba bj"><span id="fe48" class="nu mo ev nr b bf nv nw l nx ny" data-selectable-paragraph=""><span class="hljs-keyword">import</span> openai_function<br><br><span class="hljs-meta">@openai_function</span></span></pre>"""
    expected = """<code>import openai_function<lb/><lb/>@openai_function</code>"""
    testresult = extract(medium_js, config=ZERO_CONFIG, output_format="xml")
    assert expected in testresult and "quote" not in testresult
    medium_ssr = """<div><p>Code:</p>
    <pre class="lw lx ly lz ma nq nr ns bo nt ba bj"><span id="fe48" class="nu mo ev nr b bf nv nw l nx ny">import openai_function<br><br>@openai_function<br>def sum(a:int, b:int):<br>  &quot;&quot;&quot;Sum description adds a + b&quot;&quot;&quot;</span></pre>"""
    expected = '''<code>import openai_function<lb/><lb/>@openai_function<lb/>def sum(a:int, b:int):<lb/>  """Sum description adds a + b"""</code>'''
    testresult = extract(medium_ssr, config=ZERO_CONFIG, output_format="xml")
    assert expected in testresult and "quote" not in testresult
    code_el = """<div><p>Code:</p>
    <pre><code><span>my code</span></code></pre>"""
    expected = """<code>my code</code>"""
    testresult = extract(code_el, config=ZERO_CONFIG, output_format="xml")
    assert expected in testresult and "quote" not in testresult
    # blockquote with surrounding text/tail must not be misdetected as a highlightjs code block
    bq_text = "<html><body><article><blockquote>see <code>x</code> above</blockquote></article></body></html>"
    assert "<quote>" in extract(bq_text, output_format="xml", config=ZERO_CONFIG)
    bq_tail = "<html><body><article><blockquote><code>x</code> tail</blockquote></article></body></html>"
    assert "<quote>" in extract(bq_tail, output_format="xml", config=ZERO_CONFIG)


def test_markdown_escaping():
    "Markdown-mode output escapes metacharacters that would corrupt GFM structure."
    # pipe in table cell text must be escaped so it doesn't split the column
    tree = etree.fromstring(b"<body><table><row><cell>a|b</cell><cell>c</cell></row></table></body>")
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "a\\|b" in result

    # pipe inside formatted text (hi) inside a cell must also be escaped
    tree = etree.fromstring(b'<body><table><row><cell><hi rend="#b">x|y</hi></cell></row></table></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "x\\|y" in result

    # URL with a space must be wrapped in angle brackets
    tree = etree.fromstring(b'<body><p><ref target="http://a b/c">link</ref></p></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "[link](<http://a b/c>)" in result

    # square brackets in link text must be escaped
    tree = etree.fromstring(b'<body><p><ref target="http://x">a[b]c</ref></p></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "[a\\[b\\]c](http://x)" in result

    # square brackets in image alt must be escaped
    tree = etree.fromstring(b'<body><graphic src="img.png" alt="a[b]c"/></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "![a\\[b\\]c](img.png)" in result

    # a ref with no/empty target renders as bare [text]; a graphic with no src keeps empty parens
    assert xml.xmltotxt(etree.fromstring(b"<body><p><ref>txt</ref></p></body>"), True).strip() == "[txt]"
    assert xml.xmltotxt(etree.fromstring(b'<body><p><ref target="">txt</ref></p></body>'), True).strip() == "[txt]"
    assert xml.xmltotxt(etree.fromstring(b'<body><graphic alt="a"/></body>'), True).strip() == "![a]()"

    # backtick in inline code needs a longer fence
    tree = etree.fromstring(b'<body><p><hi rend="#t">a\x60b</hi></p></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "``a`b``" in result

    # inline code whose content abuts a backtick gets a space pad so the fence does not merge
    assert xml.xmltotxt(etree.fromstring(b'<body><p><hi rend="#t">\x60x</hi></p></body>'), True).strip() == "`` `x ``"
    assert xml.xmltotxt(etree.fromstring(b'<body><p><hi rend="#t">x\x60</hi></p></body>'), True).strip() == "`` x` ``"
    assert xml.xmltotxt(etree.fromstring(b'<body><p><hi rend="#t">\x60</hi></p></body>'), True).strip() == "`` ` ``"

    # triple backtick in block code needs a 4-backtick fence
    tree = etree.fromstring(b"<body><code>a\x60\x60\x60b</code></body>")
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "````" in result and "a```b" in result

    # ~~ inside del content must not close the strikethrough early
    tree = etree.fromstring(b"<body><p><del>a~~b</del></p></body>")
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "~~a~\\~b~~" in result

    # del as a direct child of a table cell (no enclosing p)
    result = extract(
        "<html><body><table><tr><td><del>gone</del></td></tr></table></body>",
        output_format="markdown",
        include_formatting=True,
        config=ZERO_CONFIG,
    )
    assert result and "~~gone~~" in result

    # del wrapping an inline child must preserve the strikethrough marker
    tree = etree.fromstring(b'<body><p><del><hi rend="#b">bold</hi></del></p></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "~~**bold**~~" in result

    # pipe in graphic tail inside a table cell must be escaped
    tree = etree.fromstring(b'<body><table><row><cell><graphic src="img.png" alt="img"/>tail|text</cell></row></table></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "tail\\|text" in result
    # pipe in non-graphic element tail inside a cell must also be escaped (separate code path)
    tree = etree.fromstring(b'<body><table><row><cell><hi rend="#b">bold</hi>tail|pipe</cell></row></table></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "tail\\|pipe" in result

    # block math in a cell must not inject newlines that split the table row
    tree = etree.fromstring(b"<body><table><row><cell>x \\[E=mc^2\\] y</cell></row></table></body>")
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "\n" not in result.strip() and "$$ E=mc^2 $$" in result

    # bold wrapping a link must preserve both the bold marker and the link
    tree = etree.fromstring(b'<body><p><hi rend="#b"><ref target="http://x.com">link</ref></hi></p></body>')
    result = xml.xmltotxt(tree, include_formatting=True)
    assert "**[link](http://x.com)**" in result

    # a graphic wrapped in inline formatting must keep the image, not be dropped
    bold_img = b'<body><p><hi rend="#b">x <graphic src="i.jpg" alt="A"/> y</hi></p></body>'
    assert xml.xmltotxt(etree.fromstring(bold_img), True).strip() == "**x ![A](i.jpg) y**"
    struck_img = b'<body><p><del>x <graphic src="i.jpg" alt="A"/> y</del></p></body>'
    assert xml.xmltotxt(etree.fromstring(struck_img), True).strip() == "~~x ![A](i.jpg) y~~"


def test_xmltotxt_no_mutation():
    "xmltotxt must not mutate its input tree (math/emphasis passes run on a deepcopy)."
    tree = etree.fromstring(b'<body><p>formula \\(x\\) <hi rend="#b"><hi rend="#i">y</hi></hi></p></body>')
    before = etree.tostring(tree, encoding="unicode")
    out = xml.xmltotxt(tree, True)
    assert "$x$" in out and "***y***" in out  # output is converted
    assert etree.tostring(tree, encoding="unicode") == before  # source tree untouched


def test_math_conversion():
    "LaTeX math delimiters are converted to $ notation; unmatched delimiters and code are left alone."
    # inline math \(...\) → $...$
    assert xml.xmltotxt(etree.fromstring(b"<body><p>\\(x^2\\)</p></body>"), True).strip() == "$x^2$"
    # unmatched \( must not become a lone $
    assert xml.xmltotxt(etree.fromstring(b"<body><p>regex \\( open</p></body>"), True).strip() == "regex \\( open"
    # math delimiters inside a fenced code block must not be converted
    tree = etree.fromstring(b"<body><code>prefix\n\\[E=mc^2\\]\nsuffix</code></body>")
    assert "\\[E=mc^2\\]" in xml.xmltotxt(tree, include_formatting=True)
    # math delimiters inside inline code must not be converted either
    tree = etree.fromstring(b'<body><p>use <hi rend="#t">a\\(x\\)b</hi> here</p></body>')
    assert "`a\\(x\\)b`" in xml.xmltotxt(tree, include_formatting=True)
    # but math in a code element's prose tail is still converted
    tree = etree.fromstring(b"<body><p><code>k</code> then \\(t\\) end</p></body>")
    assert "`k` then $t$ end" in xml.xmltotxt(tree, include_formatting=True)


def test_inline_edge_cases():
    "Cover lb in inline context, structural-tag fallback, and redundant emphasis collapse."
    # <lb/> inside an inline element (hi) renders as a newline
    assert "**A\nB**" in xml.xmltotxt(etree.fromstring(b'<body><p><hi rend="#b">A<lb/>B</hi></p></body>'), True)
    # structural tag (e.g. <span>) nested inside inline: its text is carried through
    assert "**carried**" in xml.xmltotxt(
        etree.fromstring(b'<body><p><hi rend="#b"><span>carried</span></hi></p></body>'),
        True,
    )
    # redundant nested emphasis is collapsed: **x** not ****x****
    assert (
        xml.xmltotxt(
            etree.fromstring(b'<body><p><hi rend="#b"><hi rend="#b">x</hi></hi></p></body>'),
            True,
        ).strip()
        == "**x**"
    )


def test_heading_inline_formatting():
    "A heading keeps its # prefix even when it starts with an inline child (e.g. <h2><strong>...)."

    def md(b):
        return xml.xmltotxt(etree.fromstring(b), include_formatting=True).strip()

    # child-first headings must NOT lose the # prefix
    assert md(b'<body><head rend="h2"><hi rend="#b">B</hi> text</head></body>') == "## **B** text"
    assert md(b'<body><head rend="h2"><hi rend="#b">B</hi></head></body>') == "## **B**"
    assert md(b'<body><head rend="h3"><hi rend="#i">I</hi> rest</head></body>') == "### *I* rest"
    assert md(b'<body><head><hi rend="#b">B</hi> t</head></body>') == "## **B** t"  # no rend -> level 2
    # text-first and plain headings are unchanged
    assert md(b'<body><head rend="h2">x <hi rend="#b">B</hi></head></body>') == "## x **B**"
    assert md(b'<body><head rend="h2">plain</head></body>') == "## plain"
    # a heading inside a table cell stays prefix-less
    assert (
        md(b'<body><table><row><cell><head rend="h3"><hi rend="#b">H</hi></head></cell></row></table></body>') == "| **H** |"
    )


def test_mixed_content_extraction():
    """
    Test extraction from HTML with mixed content.
    """
    html_content = '<html><body><p>Text here</p><img src="img.jpg"/><video src="video.mp4"/></body></html>'
    expected = "Text here"
    result = extract(html_content, fast=False, config=ZERO_CONFIG)
    assert result.strip() == expected, "Mixed content extraction failed"


def test_nonstd_html_entities():
    """
    Test handling non-standard HTML entities.
    """
    html_content = "<html><body><p>Text &customentity; more text</p></body></html>"
    expected = "Text &customentity; more text"
    result = extract(html_content, fast=False, config=ZERO_CONFIG)
    assert result.strip() == expected, "Non-standard HTML entity handling failed"


def test_large_doc_performance():
    """
    Performance test on large HTML documents.
    """
    large_html = "<html><body>" + "<p>Sample text</p>" * 10000 + "</body></html>"
    start = time.time()
    extract(large_html, fast=False, config=ZERO_CONFIG)
    end = time.time()
    assert end - start < 5, "Large document performance issue"


@pytest.mark.skipif(not LANGID_FLAG, reason="py3langid not installed")
def test_lang_detection():
    """
    Accuracy of language detection.
    """
    samples = [
        {"html": "<html><body><p>Texto en español</p></body></html>", "expected": "es"},
        {"html": "<html><body><p>Texte en français</p></body></html>", "expected": "fr"},
    ]
    for sample in samples:
        result = extract(sample["html"], fast=False, config=ZERO_CONFIG)
        detected = language_classifier(result, "")
        assert detected == sample["expected"]


def test_config_loading():
    "Check if the config file is read correctly."
    with pytest.raises(FileNotFoundError):
        config = use_config(filename="/bogus-dir/bogus-file.txt")

    config = use_config(filename=path.join(RESOURCES_DIR, "newsettings.cfg"))
    assert config is not None

    # an explicit config object short-circuits and is returned unchanged
    assert use_config(config=config) is config

    # the settingsfile= argument must actually be applied, not silently ignored:
    # newsettings.cfg sets MIN_OUTPUT_SIZE/MIN_EXTRACTED_SIZE far above this doc's length
    settingsfile = path.join(RESOURCES_DIR, "newsettings.cfg")
    html = "<html><body><article><p>Short paragraph of content here.</p></article></body></html>"
    assert extract(html) is not None
    assert extract(html, settingsfile=settingsfile) is None
    assert extract_with_metadata(html, settingsfile=settingsfile) is None
    # an explicit config object is still honored when no settingsfile is given
    assert extract(html, config=NEW_CONFIG) is None
    # a missing settingsfile is reported, not silently ignored
    with pytest.raises(FileNotFoundError):
        extract(html, settingsfile="/bogus-dir/bogus-file.txt")

    # a partial settings file must not raise NoOptionError: defaults are seeded, user keys override
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".cfg", delete=False) as tmp:
        tmp.write("[DEFAULT]\nMIN_EXTRACTED_SIZE = 9999\n")
        partial_path = tmp.name
    partial = use_config(filename=partial_path)
    options = core.Extractor(config=partial)
    assert options.min_extracted_size == 9999  # from the partial file
    # unset key falls back to default; read fresh as DEFAULT_CONFIG may be mutated in-place elsewhere
    assert options.min_output_size == use_config().getint("DEFAULT", "MIN_OUTPUT_SIZE")


def test_is_probably_readerable():
    """
    Test is_probably_readerable function.
    """
    assert not is_probably_readerable("ABC")

    very_small_str = "hello there"
    small_str = "hello there " * 11
    large_str = "hello there " * 12
    very_large_str = "hello there " * 50
    linebreaks_str = f"{large_str} <br>" * 10

    very_small_doc = load_html(f"<html><p id='main'>{very_small_str}</p></html>")
    small_doc = load_html(f"<html><p id='main'>{small_str}</p></html>")
    large_doc = load_html(f"<html><p id='main'>{large_str}</p></html>")
    very_large_doc = load_html(f"<html><p id='main'>{very_large_str}</p></html>")
    likely_doc = load_html(
        f"<html><p id='main' class='header'>{very_large_str}</p><p id='header' class='article'>{very_large_str}</p><p id='footer' class='body'>{very_large_str}</p></html>"
    )
    unlikely_doc = load_html(f"<html><p id='header'>{very_large_str}</p><p class='footer'>{very_large_str}</p></html>")
    visible_doc = load_html(
        f"<html><p id='main' style='display: block'>{very_large_str}</p><p id='main'>{very_large_str}</p><p id='main' aria-hidden='false'>{very_large_str}</p></html>"
    )
    invisible_doc = load_html(
        f"<html><p id='main' style='display: none'>{very_large_str}</p><p id='main' hidden>{very_large_str}</p><p id='main' aria-hidden='true'>{very_large_str}</p></html>"
    )
    linebreaks_doc = load_html(f"<html><div>{linebreaks_str * 10}</div></html>")
    no_linebreaks_doc = load_html(f"<html><div>{large_str * 10}</div></html>")

    # should only declare large documents as readerable when default options
    assert not is_probably_readerable(very_small_doc)
    assert not is_probably_readerable(small_doc)
    assert not is_probably_readerable(large_doc)
    assert is_probably_readerable(very_large_doc)

    # should declare small and large documents as readerable when lower min_content_length
    options = {"min_content_length": 120, "min_score": 0}
    assert not is_probably_readerable(very_small_doc, options)
    assert is_probably_readerable(small_doc, options)
    assert is_probably_readerable(large_doc, options)
    assert is_probably_readerable(very_large_doc, options)

    # should only declare largest document as readerable when higher min_content_length
    options = {"min_content_length": 200, "min_score": 0}
    assert not is_probably_readerable(very_small_doc, options)
    assert not is_probably_readerable(small_doc, options)
    assert not is_probably_readerable(large_doc, options)
    assert is_probably_readerable(very_large_doc, options)

    # should declare large documents as readerable when lower min_score
    options = {"min_content_length": 0, "min_score": 4}
    assert not is_probably_readerable(very_small_doc, options)
    assert is_probably_readerable(small_doc, options)
    assert is_probably_readerable(large_doc, options)
    assert is_probably_readerable(very_large_doc, options)

    # should declare large documents as readerable when higher min_score
    options = {"min_content_length": 0, "min_score": 11.5}
    assert not is_probably_readerable(very_small_doc, options)
    assert not is_probably_readerable(small_doc, options)
    assert is_probably_readerable(large_doc, options)
    assert is_probably_readerable(very_large_doc, options)

    # should check id and class attributes
    assert is_probably_readerable(likely_doc)
    assert not is_probably_readerable(unlikely_doc)

    # should check linebreaks in div elements
    assert is_probably_readerable(linebreaks_doc)
    assert not is_probably_readerable(no_linebreaks_doc)

    called = False

    def visibility_checker_invisible(node):
        nonlocal called
        called = True
        return False

    # should use node visibility checker provided as option - not visible
    options = {"visibility_checker": visibility_checker_invisible}
    assert not is_probably_readerable(very_large_doc, options)
    assert called

    called = False

    def visibility_checker_visible(node):
        nonlocal called
        called = True
        return True

    # should use node visibility checker provided as option - visible
    options = {"visibility_checker": visibility_checker_visible}
    assert is_probably_readerable(very_large_doc, options)
    assert called

    # should use default node visibility checker
    assert is_probably_readerable(visible_doc)
    assert not is_probably_readerable(invisible_doc)

    # https://github.com/mozilla/readability/blob/main/test/test-pages/mozilla-2/source.html#L22
    with open(
        path.join(RESOURCES_DIR, "mozilla.org.firefox.developer.html"),
        "r",
        encoding="utf-8",
    ) as f:
        teststring = f.read()

    doc = load_html(teststring)
    assert not is_probably_readerable(doc)


def test_html_conversion():
    "Test conversion from internal XML to HTML output."
    xml = """<xml>
    <list>
        <item>Item 1</item>
        <item>Item 2</item>
    </list>
    <p>Text</p>
    <head rend="h1">Heading 1</head>
    <head rend="h2">Heading 2</head>
    <head>No attribute</head>
    <hi rend="#i">Italic</hi>
    <hi rend="#b">Bold</hi>
    <hi>No rend</hi>
    <ref target="https://example.com">Link</ref>
    <ref>No href</ref>
</xml>"""
    tree = etree.fromstring(xml)
    html_tree = trafilatura.htmlprocessing.convert_to_html(copy(tree))
    expected_html = """<html><body>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    <p>Text</p>
    <h1>Heading 1</h1>
    <h2>Heading 2</h2>
    <h3>No attribute</h3>
    <i>Italic</i>
    <strong>Bold</strong>
    <i>No rend</i>
    <a href="https://example.com">Link</a>
    <a href="">No href</a>
</body></html>"""
    assert etree.tostring(html_tree, method="html").decode() == expected_html

    html = "<html><body><article><h1>Title</h1><p>Text.</p></article></body></html>"
    excepted_html = """<html>
  <body>
    <h1>Title</h1>
    <p>Text.</p>
  </body>
</html>"""
    result = extract(html, output_format="html", config=ZERO_CONFIG)
    assert result == excepted_html

    html = "<html><body><article><h1>Title 1</h1><p>Text.</p></article></body></html>"
    excepted_html = """<html>
  <head>
    <meta name="title" content="Title 1"/>
    <meta name="fingerprint" content="f6fd180b8fbe3670"/>
  </head>
  <body>
    <h1>Title 1</h1>
    <p>Text.</p>
  </body>
</html>"""
    result = extract(html, output_format="html", config=ZERO_CONFIG, with_metadata=True)
    assert result == excepted_html

    # regression #819/#777: row->tr, head cell->th, plain cell->td, span/role dropped
    table_xml = (
        "<body><table>"
        '<row span="3"><cell role="head">Name</cell><cell role="head">Phone</cell></row>'
        '<row span="3"><cell>Jane</cell><cell>p1</cell><cell>p2</cell></row>'
        "</table></body>"
    )
    table_html = etree.tostring(trafilatura.htmlprocessing.convert_to_html(etree.fromstring(table_xml)), encoding="unicode")
    assert table_html == (
        "<html><body><table>"
        "<tr><th>Name</th><th>Phone</th></tr>"
        "<tr><td>Jane</td><td>p1</td><td>p2</td></tr>"
        "</table></body></html>"
    )

    # regression: internal <graphic> must become <img> in HTML output, keeping src/alt/title
    img_xml = '<body><graphic src="a.jpg" alt="cap" title="t"/></body>'
    img_html = etree.tostring(trafilatura.htmlprocessing.convert_to_html(etree.fromstring(img_xml)), encoding="unicode")
    assert img_html == '<html><body><img src="a.jpg" alt="cap" title="t"/></body></html>'

    # end-to-end: an image reaches HTML output as <img> (not <graphic>)
    doc = '<html><body><article><p>Body text here.</p><img src="pic.jpg" alt="a"/></article></body></html>'
    out = extract(doc, output_format="html", include_images=True, config=ZERO_CONFIG)
    assert '<img src="pic.jpg" alt="a"/>' in out and "<graphic" not in out


def test_deprecations():
    "Test deprecated function parameters."
    htmlstring = "<html><body><article>ABC</article></body></html>"
    assert extract(htmlstring, no_fallback=True, config=ZERO_CONFIG) is not None
    assert bare_extraction(htmlstring, no_fallback=True, config=ZERO_CONFIG) is not None
    assert bare_extraction(htmlstring, as_dict=True, config=ZERO_CONFIG) is not None
    with pytest.raises(ValueError):
        extract(htmlstring, max_tree_size=100)
    with pytest.raises(ValueError):
        bare_extraction(htmlstring, max_tree_size=100)

    # single source of truth for the effective "fast" flag
    assert core._check_deprecation(no_fallback=True) is True
    assert core._check_deprecation(fast=True) is True
    assert core._check_deprecation() is False

    # regression: no_fallback=True must reach Extractor.fast via both entry points
    captured = []

    class _SpyExtractor(core.Extractor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            captured.append(self.fast)

    with patch.object(core, "Extractor", _SpyExtractor):
        extract(htmlstring, no_fallback=True, config=ZERO_CONFIG)
        bare_extraction(htmlstring, no_fallback=True, config=ZERO_CONFIG)
    assert captured and all(captured)
