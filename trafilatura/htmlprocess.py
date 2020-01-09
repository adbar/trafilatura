"""
Functions to process nodes in HTML code.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re

from lxml import etree

from .duplicates import duplicate_test
from .settings import CUT_EMPTY_ELEMS, MANUALLY_CLEANED
from .utils import textfilter, trim
from .xpaths import COMMENTS_DISCARD_XPATH, DISCARD_XPATH


LOGGER = logging.getLogger(__name__)


def manual_cleaning(tree, include_tables):
    '''Prune the tree by discarding unwanted elements'''
    if include_tables is False:
        MANUALLY_CLEANED.append('table')
    for expression in MANUALLY_CLEANED:
        for element in tree.iter(expression):
            element.getparent().remove(element)
    #for expression in ['a', 'abbr', 'acronym', 'address', 'big', 'cite', 'font', 'ins', 'meta', 'small', 'sub', 'sup', 'wbr']:
    #    for element in tree.getiterator(expression):
    #        element.drop_tag()
    return tree


def prune_html(tree):
    '''delete empty elements'''
    # empty tags
    for element in tree.xpath(".//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            element.getparent().remove(element)
    # for expression in CUT_EMPTY_ELEMS:
    #    for element in tree.getiterator(expression):
    #        if recursively_empty(element):
    #            element.getparent().remove(element)
    return tree


def recursively_empty(elem):
    '''return recursively empty elements'''
    # https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
    if elem.text:
        return False
    return all((recursively_empty(c) for c in elem.iterchildren()))


def discard_unwanted(tree):
    '''delete unwanted sections'''
    for expr in DISCARD_XPATH:
        for subtree in tree.xpath(expr):
            subtree.getparent().remove(subtree)
    return tree


def discard_unwanted_comments(tree):
    '''delete unwanted comment sections'''
    for expr in COMMENTS_DISCARD_XPATH:
        for subtree in tree.xpath(expr):
            subtree.getparent().remove(subtree)
    return tree


def convert_tags(tree):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # strip tags
    etree.strip_tags(tree, 'a', 'abbr', 'acronym', 'address', 'big', 'cite', 'font', 'ins', 'meta', 'span', 'small', 'wbr')
    # 'dd', 'sub', 'sup',
    # head tags + delete attributes
    for elem in tree.iter('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        # print(elem.tag, elem.text_content())
        # etree.strip_tags(elem, 'span')
        elem.tag = 'head'
        # elem.set('rendition', '#i')
    # br → lb
    for elem in tree.iter('br', 'hr'): # tree.xpath('//[br or hr]'): ## hr → //lb/line ?
        elem.tag = 'lb'
        elem.attrib.clear()
    # ul/ol → list / li → item
    for elem in tree.iter('ul', 'ol', 'dl'):
        elem.tag = 'list'
        elem.attrib.clear()
    # blockquote | q → quote
    for elem in tree.iter('blockquote', 'pre', 'q'):
        elem.tag = 'quote'
        elem.attrib.clear()
    # change rendition #i
    for elem in tree.iter('em', 'i'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#i')
    # change rendition #b
    for elem in tree.iter('b', 'strong'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#b')
    # change rendition #u (very rare)
    for elem in tree.iter('u'):
        elem.tag = 'hi'
        elem.set('rendition', '#u')
    # change rendition #pre and #t (very rare)
    for elem in tree.iter('tt'):  # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#t')
    # change rendition sub and sup (very rare)
    for elem in tree.iter('sub'):  # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#sub')
    for elem in tree.iter('sup'):  # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#sup')
    # del | s | strike → <del rend="overstrike">
    for elem in tree.iter('del', 's', 'strike'):
        elem.attrib.clear()
        elem.tag = 'del'
        elem.set('rendition', 'overstrike')
    return tree


def handle_textnode(element, comments_fix=True):
    '''Convert, format, and probe potential text elements'''
    if element.text is None and element.tail is None:
        return None
    # lb bypass
    if comments_fix is False and element.tag == 'lb':
        element.tail = trim(element.tail)
        # if textfilter(element) is True:
        #     return None
        # duplicate_test(subelement)?
        return element
    if element.tag in ('dl', 'head', 'ol', 'ul'):
        element.attrib.clear()
    if element.text is None:
        # try the tail
        # LOGGER.debug('using tail for element %s', element.tag)
        element.text = element.tail
        element.tail = ''
        # handle differently for br/lb
        if comments_fix is True and element.tag == 'lb':
            element.tag = 'p'
    # trim
    element.text = trim(element.text)
    if element.tail:
        element.tail = trim(element.tail)
    if element.text and re.search(r'\w', element.text):  # text_content()?
        if textfilter(element) is True:
            return None
        # TODO: improve duplicate detection
        if duplicate_test(element) is True:
            return None
    else:
        return None
    return element
