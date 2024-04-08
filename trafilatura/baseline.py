# pylint:disable-msg=E0611
import re

from lxml.etree import Element, SubElement

from .settings import BASIC_CLEAN_XPATH
from .utils import load_html, trim


JSON_SEARCH = re.compile(r'"articlebody": *"(.+?)(?<!\\)"', re.I)



def basic_cleaning(tree):
    "Remove a few section types from the document."
    for elem in BASIC_CLEAN_XPATH(tree):
        elem.getparent().remove(elem)
    return tree


def baseline(filecontent):
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
    for elem in tree.iterfind('.//script[@type="application/ld+json"]'):
        if elem.text and '"article' in elem.text:
            mymatch = JSON_SEARCH.search(elem.text)
            if mymatch:
                elem = SubElement(postbody, 'p')
                elem.text = trim(mymatch[1].replace('\\"', '"'))
                return postbody, elem.text, len(elem.text)

    tree = basic_cleaning(tree)

    # scrape from article tag
    article_elem = tree.find('.//article')
    if article_elem is not None:
        temp_text = trim(article_elem.text_content())
        if len(temp_text) > 100:
            elem = SubElement(postbody, 'p')
            elem.text = temp_text
            return postbody, temp_text, len(temp_text)
    # scrape from text paragraphs
    results = set()
    for element in tree.iter('blockquote', 'code', 'p', 'pre', 'q', 'quote'):
        entry = element.text_content()
        if entry not in results:
            elem = SubElement(postbody, 'p')
            elem.text = entry
            results.add(entry)
    temp_text = trim('\n'.join(postbody.itertext()))
    if len(temp_text) > 100:
        return postbody, temp_text, len(temp_text)
    # default strategy: clean the tree and take everything
    postbody = Element('body')
    body_elem = tree.find('.//body')
    if body_elem is not None:
        # elem.text = trim(body_elem.text_content())
        text = '\n'.join([trim(e) for e in body_elem.itertext()])
        if len(text) > 100:
            elem = SubElement(postbody, 'p')
            elem.text = text
            return postbody, text, len(text)
    # new fallback
    text = html2txt(tree)
    elem = SubElement(postbody, 'p')
    elem.text = text
    return postbody, text, len(text)
    # old: return postbody, '', 0


def html2txt(content):
    """Run basic html2txt on a document.

    Args:
        content: HTML document as string or LXML element.

    Returns:
        The extracted text in the form of a string or an empty string.

    """
    tree = load_html(content)
    if tree is None:
        return ""
    body = tree.find(".//body")
    if body is None:
        return ""
    tree = basic_cleaning(tree)
    return " ".join(body.text_content().split()).strip()
