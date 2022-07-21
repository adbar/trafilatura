# pylint:disable-msg=C0301,E0611,I1101
"""
Functions to process nodes in HTML code.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging

from collections import defaultdict
from copy import deepcopy

from lxml.etree import strip_tags
from lxml.html.clean import Cleaner

from .filters import duplicate_test, textfilter
from .settings import CUT_EMPTY_ELEMS, DEFAULT_CONFIG, MANUALLY_CLEANED, MANUALLY_STRIPPED
from .utils import trim, uniquify_list


LOGGER = logging.getLogger(__name__)

# HTML_CLEANER config
# https://lxml.de/api/lxml.html.clean.Cleaner-class.html
# https://lxml.de/apidoc/lxml.html.clean.html
HTML_CLEANER = Cleaner(
    annoying_tags = False,  # True
    comments = True,
    embedded = False,  # True
    forms = False,  # True
    frames = False,  # True
    javascript = False,
    links = False,
    meta = False,
    page_structure = False,
    processing_instructions = True,
    remove_unknown_tags = False,
    safe_attrs_only = False,
    scripts = False,
    style = False,
    # remove_tags = MANUALLY_STRIPPED,
    # kill_tags = MANUALLY_CLEANED,
)


def tree_cleaning(tree, include_tables, include_images=False):
    '''Prune the tree by discarding unwanted elements'''
    # determine cleaning strategy, use lists to keep it deterministic
    cleaning_list, stripping_list = \
        MANUALLY_CLEANED.copy(), MANUALLY_STRIPPED.copy()
    if include_tables is False:
        cleaning_list.extend(['table', 'td', 'th', 'tr'])
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


def prune_unwanted_nodes(tree, nodelist, with_backup=False):
    '''Prune the HTML tree by removing unwanted sections.'''
    if with_backup is True:
        old_len = len(tree.text_content())  # ' '.join(tree.itertext())
        backup = deepcopy(tree)
    for expr in nodelist:
        for subtree in tree.xpath(expr):
            # preserve tail text from deletion
            if subtree.tail is not None:
                previous = subtree.getprevious()
                if previous is None:
                    previous = subtree.getparent()
                if previous is not None:
                    # There is a previous node, append text to its tail
                    if previous.tail is not None:
                        previous.tail = ' '.join([previous.tail, subtree.tail])
                    else:
                        previous.tail = subtree.tail
            # remove the node
            subtree.getparent().remove(subtree)
    if with_backup is False:
        return tree
    # else:
    new_len = len(tree.text_content())
    # todo: adjust for recall and precision settings
    if new_len > old_len/7:
        return tree
    return backup


def collect_link_info(links_xpath, favor_precision=False):
    '''Collect heuristics on link text'''
    # init
    shortelems, mylist = 0, []
    # longer strings impact recall in favor of precision
    if favor_precision is False:
        threshold = 10
    else:
        threshold = 50
    # examine the elements
    for subelem in links_xpath:
        subelemtext = trim(subelem.text_content())
        if not subelemtext:
            continue
        mylist.append(subelemtext)
    lengths = [len(text) for text in mylist]
    shortelems = len([l for l in lengths if l < threshold])
    return sum(lengths), len(mylist), shortelems, mylist


def link_density_test(element, text, favor_precision=False):
    '''Remove sections which are rich in links (probably boilerplate)'''
    links_xpath, mylist = element.findall('.//ref'), []
    if links_xpath:
        if element.tag == 'p': #  and not element.getparent().tag == 'item'
            #if element.getnext() is None:
            #    limitlen, threshold = 100, 0.8
            #else:
            if favor_precision is False:
                limitlen, threshold = 25, 0.8
            else:
                limitlen, threshold = 100, 0.8
            #if 'hi' in list(element):
            #    limitlen, threshold = 100, 0.8
        #elif element.tag == 'head':
        #    limitlen, threshold = 50, 0.8
        else:
            if element.getnext() is None:
                limitlen, threshold = 300, 0.8
            #elif re.search(r'[.?!:]', elemtext):
            #    limitlen, threshold = 150, 0.66
            else:
                limitlen, threshold = 100, 0.8
        elemlen = len(text)
        if elemlen < limitlen:
            linklen, elemnum, shortelems, mylist = collect_link_info(links_xpath, favor_precision)
            if elemnum == 0:
                return True, mylist
            LOGGER.debug('list link text/total: %s/%s – short elems/total: %s/%s', linklen, elemlen, shortelems, elemnum)
            # (elemnum > 1 and shortelems/elemnum > 0.8):
            if linklen > threshold*elemlen or shortelems/elemnum > 0.8:
                return True, mylist
    return False, mylist


def link_density_test_tables(element):
    '''Remove tables which are rich in links (probably boilerplate)'''
    # if element.getnext() is not None:
    #     return False
    links_xpath = element.findall('.//ref')
    if links_xpath:
        elemlen = len(trim(element.text_content()))
        if elemlen > 250:
            linklen, elemnum, _, _ = collect_link_info(links_xpath)
            if elemnum == 0:
                return True
            LOGGER.debug('table link text: %s / total: %s', linklen, elemlen)
            if (elemlen < 1000 and linklen > 0.8*elemlen) or (elemlen > 1000 and linklen > 0.5*elemlen):
                return True
            # does more harm than good (issue #76)
            #if shortelems > len(links_xpath) * 0.66:
            #    return True
    return False


def delete_by_link_density(subtree, tagname, backtracking=False, favor_precision=False):
    '''Determine the link density of elements with respect to their length,
       and remove the elements identified as boilerplate.'''
    myelems, deletions = defaultdict(list), []
    for elem in subtree.iter(tagname):
        elemtext = trim(elem.text_content())
        result, templist = link_density_test(elem, elemtext, favor_precision)
        if result is True:
            deletions.append(elem)
        elif backtracking is True and len(templist) > 0:  # if?
            myelems[elemtext].append(elem)
    # summing up
    if backtracking is True:
        if favor_precision is False:
            threshold = 100
        else:
            threshold = 200
        for text, elem in myelems.items():
            if 0 < len(text) < threshold and len(elem) >= 3:
                deletions.extend(elem)
                # print('backtrack:', text)
            # else: # and not re.search(r'[?!.]', text):
            # print(elem.tag, templist)
    for elem in uniquify_list(deletions):
        try:
            elem.getparent().remove(elem)
        except AttributeError:
            pass
    return subtree


def convert_tags(tree, include_formatting=False, include_tables=False, include_images=False, include_links=False):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # ul/ol → list / li → item
    for elem in tree.iter('ul', 'ol', 'dl'):
        elem.tag = 'list'
        for subelem in elem.iter('dd', 'dt', 'li'):
            subelem.tag = 'item'
    # images
    if include_images is True:
        for elem in tree.iter('img'):
            elem.tag = 'graphic'
    # delete links for faster processing
    if include_links is False:
        if include_tables is True:
            xpath_expr = './/div//a|.//list//a|.//table//a'
        else:
            xpath_expr = './/div//a|.//list//a'
        # necessary for further detection
        for elem in tree.xpath(xpath_expr):
            elem.tag = 'ref'
        # strip the rest
        strip_tags(tree, 'a')
    else:
        for elem in tree.iter('a', 'ref'):
            elem.tag = 'ref'
            # replace href attribute and delete the rest
            target = elem.get('href') # defaults to None
            elem.attrib.clear()
            if target is not None:
                elem.set('target', target)
    # head tags + delete attributes
    for elem in tree.iter('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        elem.attrib.clear()
        elem.set('rend', elem.tag)
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
        strip_tags(tree, 'em', 'i', 'b', 'strong', 'u', 'kbd', 'samp', 'tt', 'var', 'sub', 'sup')
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
    # details + summary
    for elem in tree.iter('details'):
        elem.tag = 'div'
        for subelem in elem.iter('summary'):
            subelem.tag = 'head'
    return tree


def handle_textnode(element, comments_fix=True, deduplicate=True, preserve_spaces=False, config=DEFAULT_CONFIG):
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
    if preserve_spaces is False:
        element.text = trim(element.text)
        if element.tail:
            element.tail = trim(element.tail)
    # filter content
    if not element.text:  # or not re.search(r'\w', element.text):  # text_content()?
        return None
    if textfilter(element) is True:
        return None
    if deduplicate is True and duplicate_test(element, config) is True:
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
