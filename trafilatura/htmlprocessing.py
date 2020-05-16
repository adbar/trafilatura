# pylint:disable-msg=I1101
"""
Functions to process nodes in HTML code.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re

from lxml import etree

from .filters import duplicate_test, textfilter
from .settings import CUT_EMPTY_ELEMS, MANUALLY_CLEANED
from .utils import sanitize, trim
from .xpaths import COMMENTS_DISCARD_XPATH, DISCARD_XPATH


LOGGER = logging.getLogger(__name__)


def manual_cleaning(tree, include_tables):
    '''Prune the tree by discarding unwanted elements'''
    if include_tables is False:
        MANUALLY_CLEANED.append('table')
    for expression in MANUALLY_CLEANED:
        #for element in tree.iter(expression):
        for element in tree.getiterator(expression):
            element.drop_tree()
    return tree


def prune_html(tree):
    '''delete selected empty elements'''
    for element in tree.xpath("//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            element.getparent().remove(element)
            #element.drop_tree()
    return tree


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


def link_density_test(element):
    links_xpath = element.xpath('//link')
    if len(links_xpath) > 0:
        elemlen = len(sanitize(element.text_content()))
        if elemlen < 100:
            linklen = 0
            for subelem in links_xpath:
                linklen += len(sanitize(subelem.text_content()))
            if linklen > 0.95*elemlen:
                #print(trim(element.text_content()))
                #print(trim(subelem.text_content()))
                return True
    return False


def convert_tags(tree):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # strip tags 'a', 'span', 'dd', 'sub', 'sup', 'center', 
    etree.strip_tags(tree, 'abbr', 'acronym', 'address', 'big', 'cite',
                     'font', 'ins', 'meta', 'ruby', 'small', 'wbr')
    # head tags + delete attributes
    for elem in tree.iter('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        # etree.strip_tags(elem, 'span')
        elem.tag = 'head'
        elem.attrib.clear()
        # elem.set('rendition', '#i')
    # br → lb
    for elem in tree.iter('br', 'hr'):
        elem.tag = 'lb'
        elem.attrib.clear()
    # ul/ol → list / li → item
    for elem in tree.iter('ul', 'ol', 'dl'):
        elem.tag = 'list'
        elem.attrib.clear()
        for subelem in elem.iter('dd', 'dt', 'li'):
            subelem.tag = 'item'
            subelem.attrib.clear()
        for subelem in elem.iter('a'):
            subelem.tag = 'link'
    # blockquote, pre, q → quote
    for elem in tree.iter('blockquote', 'pre', 'q'):
        elem.tag = 'quote'
        elem.attrib.clear()
    # italics
    for elem in tree.iter('em', 'i'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rend', '#i')
    # bold font
    for elem in tree.iter('b', 'strong'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rend', '#b')
    # u (very rare)
    for elem in tree.iter('u'):
        elem.tag = 'hi'
        elem.set('rend', '#u')
    # tt (very rare)
    for elem in tree.iter('tt'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rend', '#t')
    # sub and sup (very rare)
    for elem in tree.iter('sub'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rend', '#sub')
    for elem in tree.iter('sup'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rend', '#sup')
    # del | s | strike → <del rend="overstrike">
    for elem in tree.iter('del', 's', 'strike'):
        elem.attrib.clear()
        elem.tag = 'del'
        elem.set('rend', 'overstrike')
    #for elem in tree.iter():
    #    print(elem.tag)
    etree.strip_tags(tree, 'a')
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


def process_node(element):
    '''Convert, format, and probe potential text elements (light format)'''
    if element.tag == 'done':
        return None
    if len(element) == 0 and not element.text and not element.tail:
        return None
    # trim
    if element.text:
        element.text = trim(element.text)
    if element.tail:
        element.tail = trim(element.tail)
    # content checks
    if element.tag != 'lb' and not element.text and element.tail:
        element.text = element.tail
    if element.text or element.tail:
        if textfilter(element) is True or duplicate_test(element) is True:
            return None
    return element
