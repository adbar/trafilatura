# pylint:disable-msg=I1101
"""
Functions to process nodes in HTML code.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re

from lxml import etree
from lxml.html.clean import Cleaner

from .filters import duplicate_test, textfilter
from .settings import CUT_EMPTY_ELEMS, DEFAULT_CONFIG, MANUALLY_CLEANED, MANUALLY_STRIPPED
from .utils import trim
from .xpaths import COMMENTS_DISCARD_XPATH, DISCARD_XPATH

LOGGER = logging.getLogger(__name__)

# HTML_CLEANER config # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
HTML_CLEANER = Cleaner()
HTML_CLEANER.annoying_tags = False  # True
HTML_CLEANER.comments = True
HTML_CLEANER.embedded = False  # True
HTML_CLEANER.forms = False  # True
HTML_CLEANER.frames = False  # True
HTML_CLEANER.javascript = False
HTML_CLEANER.links = False
HTML_CLEANER.meta = False
HTML_CLEANER.page_structure = False
HTML_CLEANER.processing_instructions = True
HTML_CLEANER.remove_unknown_tags = False
HTML_CLEANER.safe_attrs_only = False
HTML_CLEANER.scripts = False
HTML_CLEANER.style = False
#HTML_CLEANER.remove_tags = MANUALLY_STRIPPED
#HTML_CLEANER.kill_tags = MANUALLY_CLEANED


def tree_cleaning(tree, include_tables, include_images=False):
    '''Prune the tree by discarding unwanted elements'''
    # determine cleaning strategy
    cleaning_list, stripping_list = \
        MANUALLY_CLEANED.copy(), MANUALLY_STRIPPED.copy()
    if include_tables is False:
        cleaning_list.append('table')
    if include_images is True:
        # Many websites have <img> inside <figure> or <picture> or <source> tag
        cleaning_list = [e for e in cleaning_list if e
                         not in ('figure', 'picture', 'source')]
        stripping_list.remove('img')
    # delete targeted elements
    for expression in cleaning_list:
        for element in tree.getiterator(expression):
            try:
                element.drop_tree() # faster when applicable
            except AttributeError:
                element.getparent().remove(element)
    HTML_CLEANER.kill_tags, HTML_CLEANER.remove_tags = cleaning_list, stripping_list
    # save space and processing time
    return HTML_CLEANER.clean_html(prune_html(tree))


def prune_html(tree):
    '''Delete selected empty elements'''
    for element in tree.xpath(".//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            try:
                element.drop_tree()
            except AttributeError:
                element.getparent().remove(element)
    return tree


def discard_unwanted(tree):
    '''Delete unwanted sections'''
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


def collect_link_info(links_xpath):
    '''Collect heuristics on link text'''
    linklen, elemnum, shortelems, mylist = 0, 0, 0, []
    for subelem in links_xpath:
        subelemtext = trim(subelem.text_content())
        subelemlen = len(subelemtext)
        if subelemlen == 0:
            continue
        linklen += subelemlen
        elemnum += 1
        if subelemlen < 10:
            shortelems += 1
        mylist.append(subelemtext)
    return linklen, elemnum, shortelems, mylist


def link_density_test(element):
    '''Remove sections which are rich in links (probably boilerplate)'''
    links_xpath, mylist = element.xpath('.//ref'), []
    if links_xpath:
        elemtext = trim(element.text_content())
        elemlen = len(elemtext)
        if element.tag == 'p':
            limitlen, threshold = 25, 0.9
        else:
            if element.getnext() is None:
                limitlen, threshold = 200, 0.66
            #elif re.search(r'[.?!]', elemtext):
            #    limitlen, threshold = 150, 0.66
            else:
                limitlen, threshold = 100, 0.66
        if elemlen < limitlen:
            linklen, elemnum, shortelems, mylist = collect_link_info(links_xpath)
            if elemnum == 0:
                return True, mylist
            #if len(set(mylist))/len(mylist) <= 0.5:
            #    return True, mylist
            LOGGER.debug('list link text/total: %s/%s – short elems/total: %s/%s', linklen, elemlen, shortelems, elemnum)
            if linklen >= threshold*elemlen or shortelems/elemnum >= threshold:
                return True, mylist
            #print(mylist)
    return False, mylist


def link_density_test_tables(element):
    '''Remove tables which are rich in links (probably boilerplate)'''
    # if element.getnext() is not None:
    #    return False
    links_xpath = element.xpath('.//ref')
    if links_xpath:
        elemlen = len(trim(element.text_content()))
        if elemlen > 250:
            linklen, elemnum, shortelems, _ = collect_link_info(links_xpath)
            if elemnum == 0:
                return True
            #if len(set(mylist))/len(mylist) <= 0.5:
            #    return True
            LOGGER.debug('table link text: %s / total: %s', linklen, elemlen)
            if (elemlen < 1000 and linklen > 0.8*elemlen) or (elemlen > 1000 and linklen > 0.5*elemlen):
            #if linklen > 0.5 * elemlen:
                return True
            if shortelems > len(links_xpath) * 0.66:
                return True
    return False


def convert_tags(tree, include_formatting=False, include_tables=False, include_images=False, include_links=False):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # ul/ol → list / li → item
    for elem in tree.iter('ul', 'ol', 'dl'):
        elem.tag = 'list'
        for subelem in elem.iter('dd', 'dt', 'li'):
            subelem.tag = 'item'
        for subelem in elem.iter('a'):
            subelem.tag = 'ref'
    # divs
    for elem in tree.xpath('//div//a'):
        elem.tag = 'ref'
    # tables
    if include_tables is True:
        for elem in tree.xpath('//table//a'):
            elem.tag = 'ref'
    # images
    if include_images is True:
        for elem in tree.iter('img'):
            elem.tag = 'graphic'
    # delete links for faster processing
    if include_links is False:
        etree.strip_tags(tree, 'a')
    else:
        for elem in tree.iter('a', 'ref'):
            elem.tag = 'ref'
            # replace href attribute and delete the rest
            for attribute in elem.attrib:
                if attribute == 'href':
                    elem.set('target', elem.get('href'))
                else:
                    del elem.attrib[attribute]
    # head tags + delete attributes
    for elem in tree.iter('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        elem.tag = 'head'
    # br → lb
    for elem in tree.iter('br', 'hr'):
        elem.tag = 'lb'
    # wbr
    # blockquote, pre, q → quote
    for elem in tree.iter('blockquote', 'pre', 'q'):
        elem.tag = 'quote'
    # include_formatting
    if include_formatting is False:
        etree.strip_tags(tree, 'em', 'i', 'b', 'strong', 'u', 'kbd', 'samp', 'tt', 'var', 'sub', 'sup')
    else:
        # italics
        for elem in tree.iter('em', 'i'):
            elem.tag = 'hi'
            elem.set('rend', '#i')
        # bold font
        for elem in tree.iter('b', 'strong'):
            elem.tag = 'hi'
            elem.set('rend', '#b')
        # u (very rare)
        for elem in tree.iter('u'):
            elem.tag = 'hi'
            elem.set('rend', '#u')
        # tt (very rare)
        for elem in tree.iter('kbd', 'samp', 'tt', 'var'):
            elem.tag = 'hi'
            elem.set('rend', '#t')
        # sub and sup (very rare)
        for elem in tree.iter('sub'):
            elem.tag = 'hi'
            elem.set('rend', '#sub')
        for elem in tree.iter('sup'):
            elem.tag = 'hi'
            elem.set('rend', '#sup')
    # del | s | strike → <del rend="overstrike">
    for elem in tree.iter('del', 's', 'strike'):
        elem.tag = 'del'
        elem.set('rend', 'overstrike')
    return tree


def handle_textnode(element, comments_fix=True, deduplicate=True, config=DEFAULT_CONFIG):
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
        if deduplicate is True and duplicate_test(element, config) is True:
            return None
    else:
        return None
    return element


def process_node(element, deduplicate=True, config=DEFAULT_CONFIG):
    '''Convert, format, and probe potential text elements (light format)'''
    if element.tag == 'done':
        return None
    if len(element) == 0 and not element.text and not element.tail:
        return None
    # trim
    element.text, element.tail = trim(element.text), trim(element.tail)
    # adapt content string
    if element.tag != 'lb' and not element.text and element.tail:
        element.text = element.tail
    # content checks
    if element.text or element.tail:
        if textfilter(element) is True:
            return None
        if deduplicate is True and duplicate_test(element, config) is True:
            return None
    return element
