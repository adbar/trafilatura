"""Regression tests for the paragraph length check in the main extractor."""

import pytest
from lxml import etree, html

from trafilatura import main_extractor as me
from trafilatura.settings import Extractor


def test_extract_does_not_materialize_paragraph_text_xpath():
    """The sufficiency check must not build the quadratic XPath text-node set."""

    class ParagraphElement(html.HtmlElement):
        def xpath(self, expression, *args, **kwargs):
            assert expression != "//p//text()", "paragraph threshold uses an unbounded XPath node set"
            return super().xpath(expression, *args, **kwargs)

    parser = html.HTMLParser()
    parser.set_element_class_lookup(etree.ElementDefaultClassLookup(element=ParagraphElement))
    tree = html.fromstring(
        "<html><body><article>" + "<p>" + "Article text. " * 100 + "</p></article></body></html>", parser=parser
    )
    _, text, _ = me._extract(tree, Extractor())
    assert "Article text." in text


@pytest.mark.parametrize(
    "markup",
    [
        "<root/>",
        "<root><p/></root>",
        "<root><p>abc</p><p>def</p></root>",
        "<root><p>A<hi>B</hi>C<hi>D</hi>E</p>outside</root>",
        "<root><p>α中🙂</p><p>text</p></root>",
        "<root><p>A<p>B<hi>C</hi>D</p>E</p><p>F</p></root>",
        "<root><p>A<!--ignored-->B<?ignored text?>C</p></root>",
        "<p>root paragraph<hi>inline</hi>tail</p>",
    ],
)
@pytest.mark.parametrize("minimum", [-1, 0, 1, 3, 5, 6, 7, 20, 100])
def test_paragraph_threshold_matches_xpath(markup, minimum):
    tree = etree.fromstring(markup)
    texts = tree.xpath("//p//text()")
    expected = bool(texts) and len("".join(texts)) >= minimum
    assert me._has_enough_paragraph_text(tree, minimum) == expected


def test_paragraph_threshold_keeps_absolute_document_scope():
    tree = etree.fromstring("<root><outside><p>long enough paragraph</p></outside><article><p>x</p></article></root>")
    assert me._has_enough_paragraph_text(tree[-1], 20)


def test_paragraph_threshold_empty_text_node():
    tree = etree.fromstring("<root><p/></root>")
    tree[0].text = ""
    assert me._has_enough_paragraph_text(tree, 0)
    assert not me._has_enough_paragraph_text(tree, 1)


@pytest.mark.parametrize("minimum", [0, 1, 3, 4, 5, 20])
def test_paragraph_threshold_unresolved_entity(minimum):
    tree = etree.fromstring(
        '<!DOCTYPE root [<!ENTITY custom "ignored">]><root><p>A&custom;B<hi>C</hi>D</p></root>',
        etree.XMLParser(resolve_entities=False),
    )
    texts = tree.xpath("//p//text()")
    assert me._has_enough_paragraph_text(tree, minimum) == (bool(texts) and len("".join(texts)) >= minimum)


def test_paragraph_threshold_stops_when_satisfied():
    class ParagraphElement(html.HtmlElement):
        @property
        def text(self):
            assert self.get("id") != "unvisited", "text after the threshold must not be read"
            return super().text

    parser = html.HTMLParser()
    parser.set_element_class_lookup(etree.ElementDefaultClassLookup(element=ParagraphElement))
    tree = html.fromstring('<div><p>enough text</p><p id="unvisited">unused text</p></div>', parser=parser)
    assert me._has_enough_paragraph_text(tree, 6)
