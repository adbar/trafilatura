"""
Module regrouping baseline and basic extraction functions.
"""
# pylint:disable-msg=E0611

import json

from typing import Any, Tuple

from lxml.etree import _Element, Element, SubElement
from lxml.html import HtmlElement

from .settings import BASIC_CLEAN_XPATH
from .utils import load_html, trim
from .xml import delete_element


def basic_cleaning(tree: HtmlElement) -> HtmlElement:
    "Remove a few section types from the document."
    for elem in BASIC_CLEAN_XPATH(tree):
        delete_element(elem)
    return tree


def baseline(filecontent: Any) -> Tuple[_Element, str, int]:
    """Use baseline extraction function targeting text paragraphs and/or JSON metadata.

    Args:
        filecontent: HTML code as binary string or string.

    Returns:
        A LXML <body> element containing the extracted paragraphs,
        the main text as string, and its length as integer.

    """
    tree = load_html(filecontent)
    postbody = Element('body')
    if tree is None:
        return postbody, '', 0

    # scrape from json text
    temp_text = ""
    for elem in tree.iterfind('.//script[@type="application/ld+json"]'):
        if elem.text and 'articleBody' in elem.text:
            try:
                json_body = json.loads(elem.text).get("articleBody", "")
            except Exception:  # JSONDecodeError or 'list' object has no attribute 'get'
                json_body = ""
            if json_body:
                if "<p>" in json_body:
                    parsed = load_html(json_body)
                    text = trim(parsed.text_content()) if parsed is not None else ""
                else:
                    text = trim(json_body)
                SubElement(postbody, 'p').text = text
                temp_text += " " + text if temp_text else text
                # return postbody, elem.text, len(elem.text)
    if len(temp_text) > 100:
        return postbody, temp_text, len(temp_text)

    tree = basic_cleaning(tree)

    # scrape from article tag
    temp_text = ""
    for article_elem in tree.iterfind('.//article'):
        text = trim(article_elem.text_content())
        if len(text) > 100:
            SubElement(postbody, 'p').text = text
            temp_text += " " + text if temp_text else text
    if len(postbody) > 0:
        # temp_text = trim('\n'.join(postbody.itertext()))
        return postbody, temp_text, len(temp_text)

    # scrape from text paragraphs
    results = set()
    temp_text = ""
    # postbody = Element('body')
    for element in tree.iter('blockquote', 'code', 'p', 'pre', 'q', 'quote'):
        entry = trim(element.text_content())
        if entry not in results:
            SubElement(postbody, 'p').text = entry
            temp_text += " " + entry if temp_text else entry
            results.add(entry)
    # temp_text = trim('\n'.join(postbody.itertext()))
    if len(temp_text) > 100:
        return postbody, temp_text, len(temp_text)

    # default strategy: clean the tree and take everything
    postbody = Element('body')
    body_elem = tree.find('.//body')
    if body_elem is not None:
        p_elem = SubElement(postbody, 'p')
        # todo: sanitize?
        text_elems = [trim(e) for e in body_elem.itertext()]
        p_elem.text = '\n'.join([e for e in text_elems if e])
        return postbody, p_elem.text, len(p_elem.text)

    # new fallback
    text = html2txt(tree, clean=False)
    SubElement(postbody, 'p').text = text
    return postbody, text, len(text)


def html2txt(content: Any, clean: bool = True) -> str:
    """Run basic html2txt on a document.

    Args:
        content: HTML document as string or LXML element.
        clean: remove potentially undesirable elements.

    Returns:
        The extracted text in the form of a string or an empty string.

    """
    tree = load_html(content)
    if tree is None:
        return ""
    body = tree.find(".//body")
    if body is None:
        return ""
    if clean:
        body = basic_cleaning(body)
    return " ".join(body.text_content().split()).strip()
