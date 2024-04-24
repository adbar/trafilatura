# pylint:disable-msg=C0301,E0611,I1101
"""
Functions to process nodes in HTML code.
"""

import logging
from collections import defaultdict
from copy import deepcopy

from courlan.urlutils import fix_relative_urls, get_base_url
from lxml.etree import strip_tags

from .filters import duplicate_test, textfilter
from .settings import CUT_EMPTY_ELEMS, MANUALLY_CLEANED, MANUALLY_STRIPPED
from .utils import trim


LOGGER = logging.getLogger(__name__)

REND_TAG_MAPPING = {
    'em': '#i',
    'i': '#i',
    'b': '#b',
    'strong': '#b',
    'u': '#u',
    'kbd': '#t',
    'samp': '#t',
    'tt': '#t',
    'var': '#t',
    'sub': '#sub',
    'sup': '#sup'
}


def delete_element(element):
    "Remove the element from the LXML tree."
    try:
        element.drop_tree()  # faster when applicable
    except AttributeError:  # pragma: no cover
        element.getparent().remove(element)


def tree_cleaning(tree, options):
    "Prune the tree by discarding unwanted elements."
    # determine cleaning strategy, use lists to keep it deterministic
    favor_recall = options.focus == "recall"
    cleaning_list, stripping_list = \
        MANUALLY_CLEANED.copy(), MANUALLY_STRIPPED.copy()
    if not options.tables:
        cleaning_list.extend(['table', 'td', 'th', 'tr'])
    else:
        # prevent this issue: https://github.com/adbar/trafilatura/issues/301
        for elem in tree.xpath('.//figure[descendant::table]'):
            elem.tag = 'div'
    if options.images:
        # Many websites have <img> inside <figure> or <picture> or <source> tag
        cleaning_list = [e for e in cleaning_list if e
                         not in ('figure', 'picture', 'source')]
        stripping_list.remove('img')

    # strip targeted elements
    strip_tags(tree, stripping_list)

    # prevent removal of paragraphs
    run_p_test = False
    if options.focus == "recall" and tree.find('.//p') is not None:
        tcopy = deepcopy(tree)
        run_p_test = True

    # delete targeted elements
    for expression in cleaning_list:
        for element in tree.getiterator(expression):
            delete_element(element)
    if run_p_test and tree.find('.//p') is None:
        tree = tcopy

    return prune_html(tree)


def prune_html(tree):
    "Delete selected empty elements to save space and processing time."
    # //comment() needed for date extraction
    for element in tree.xpath("//processing-instruction()|//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            delete_element(element)
    return tree


def prune_unwanted_nodes(tree, nodelist, with_backup=False):
    '''Prune the HTML tree by removing unwanted sections.'''
    if with_backup:
        old_len = len(tree.text_content())  # ' '.join(tree.itertext())
        backup = deepcopy(tree)

    for expression in nodelist:
        for subtree in expression(tree):
            # preserve tail text from deletion
            if subtree.tail is not None:
                prev = subtree.getprevious()
                if prev is None:
                    prev = subtree.getparent()
                if prev is not None:
                    # There is a previous node, append text to its tail
                    prev.tail = " ".join([prev.tail, subtree.tail]) if prev.tail else subtree.tail
            # remove the node
            subtree.getparent().remove(subtree)

    if not with_backup:
        return tree

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
    threshold = 50 if favor_precision else 10
    # examine the elements
    for subelem in links_xpath:
        subelemtext = trim(subelem.text_content())
        if subelemtext:
            mylist.append(subelemtext)
            if len(subelemtext) < threshold:
                shortelems += 1
    lengths = sum(len(text) for text in mylist)
    return lengths, len(mylist), shortelems, mylist


def link_density_test(element, text, favor_precision=False):
    '''Remove sections which are rich in links (probably boilerplate)'''
    links_xpath, mylist = element.findall('.//ref'), []
    if links_xpath:
        if element.tag == 'p': #  and not element.getparent().tag == 'item'
            if not favor_precision:
                if element.getnext() is None:
                    limitlen, threshold = 60, 0.8
                else:
                    limitlen, threshold = 30, 0.8
            else:
                limitlen, threshold = 200, 0.8
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
            if linklen > threshold*elemlen or (elemnum > 1 and shortelems/elemnum > 0.8):
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
        if result:
            deletions.append(elem)
        elif backtracking and len(templist) > 0:  # if?
            myelems[elemtext].append(elem)
    # summing up
    if backtracking:
        threshold = 200 if favor_precision else 100
        for text, elem in myelems.items():
            if 0 < len(text) < threshold and len(elem) >= 3:
                deletions.extend(elem)
                # print('backtrack:', text)
            # else: # and not re.search(r'[?!.]', text):
            # print(elem.tag, templist)
    for elem in dict.fromkeys(deletions):
        parent = elem.getparent()
        if parent is not None:
            parent.remove(elem)
    return subtree


def convert_lists(elem):
    # ul/ol → list / li → item
    elem.set("rend", elem.tag)
    elem.tag = "list"
    i = 1
    for subelem in elem.iter("dd", "dt", "li"):
        # keep track of dd/dt items
        if subelem.tag in ("dd", "dt"):
            subelem.set("rend", f"{subelem.tag}-{i}")
            # increment counter after <dd> in description list
            if subelem.tag == "dd":
                i += 1
        # convert elem tag
        subelem.tag = "item"


def convert_quotes(elem):
    code_flag = False
    if elem.tag == "pre":
        # detect if there could be code inside
        children = elem.getchildren()
        # pre with a single span is more likely to be code
        if len(children) == 1 and children[0].tag == "span":
            code_flag = True
        # find hljs elements to detect if it's code
        code_elems = elem.xpath(".//span[starts-with(@class,'hljs')]")
        if code_elems:
            code_flag = True
            for subelem in code_elems:
                subelem.attrib.clear()
    elem.tag = "code" if code_flag else "quote"


def convert_headings(elem):
    "Add head tags and delete attributes."
    elem.attrib.clear()
    elem.set("rend", elem.tag)
    elem.tag = "head"


def convert_line_breaks(elem):
    "br → lb"
    elem.tag = "lb"


def convert_deletions(elem):
    'del | s | strike → <del rend="overstrike">'
    elem.tag = "del"
    elem.set("rend", "overstrike")


def convert_details(elem):
    "Handle details and summary."
    elem.tag = "div"
    for subelem in elem.iter("summary"):
        subelem.tag = "head"


CONVERSIONS = {
    "dl": convert_lists, "ol": convert_lists, "ul": convert_lists,
    "h1": convert_headings, "h2": convert_headings, "h3": convert_headings,
    "h4": convert_headings, "h5": convert_headings, "h6": convert_headings,
    "br": convert_line_breaks, "hr": convert_line_breaks,
    "blockquote": convert_quotes, "pre": convert_quotes, "q": convert_quotes,
    "del": convert_deletions, "s": convert_deletions, "strike": convert_deletions,
    "details": convert_details,
}


def convert_tags(tree, options, url=None):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # delete links for faster processing
    if not options.links:
        xpath_expr = './/div//a|.//ul//a'  # .//p//a ?
        if options.tables:
            xpath_expr += '|.//table//a'
        # necessary for further detection
        for elem in tree.xpath(xpath_expr):
            elem.tag = 'ref'
        # strip the rest
        strip_tags(tree, 'a')
    else:
        # get base URL for converting relative URLs
        base_url = url and get_base_url(url)
        for elem in tree.iter('a', 'ref'):
            elem.tag = 'ref'
            # replace href attribute and delete the rest
            target = elem.get('href') # defaults to None
            elem.attrib.clear()
            if target:
                # convert relative URLs
                if base_url:
                    target = fix_relative_urls(base_url, target)
                elem.set('target', target)

    if options.formatting:
        for elem in tree.iter(REND_TAG_MAPPING.keys()):
            attribute = REND_TAG_MAPPING[elem.tag]
            elem.tag = 'hi'
            elem.set('rend', attribute)
    else:
        strip_tags(tree, *REND_TAG_MAPPING)

    # iterate over all concerned elements
    for elem in tree.iter(CONVERSIONS.keys()):
        CONVERSIONS[elem.tag](elem)
        # wbr
        # pre
        #elif elem.tag == 'pre':
        #    else:
        #        elem.tag = 'quote'
    # images
    if options.images:
        for elem in tree.iter('img'):
            elem.tag = 'graphic'
    return tree


def handle_textnode(elem, options, comments_fix=True, preserve_spaces=False):
    "Convert, format, and probe potential text elements."
    if elem.tag == "done" or (len(elem) == 0 and not elem.text and not elem.tail):
        return None

    # lb bypass
    if not comments_fix and elem.tag == "lb":
        if not preserve_spaces:
            elem.tail = trim(elem.tail)
        # if textfilter(elem) is True:
        #     return None
        # duplicate_test(subelement)?
        return elem

    if not elem.text and len(elem) == 0:
        # try the tail
        # LOGGER.debug('using tail for element %s', elem.tag)
        elem.text, elem.tail = elem.tail, ""
        # handle differently for br/lb
        if comments_fix and elem.tag == "lb":
            elem.tag = "p"

    # trim
    if not preserve_spaces:
        elem.text = trim(elem.text)
        if elem.tail:
            elem.tail = trim(elem.tail)

    # filter content
    # or not re.search(r'\w', element.text):  # text_content()?
    if not elem.text and textfilter(elem) or \
        (options.dedup and duplicate_test(elem, options)):
        return None
    return elem


def process_node(elem, options):
    "Convert, format, and probe potential text elements (light format)."
    if elem.tag == "done" or (len(elem) == 0 and not elem.text and not elem.tail):
        return None

    # trim
    elem.text, elem.tail = trim(elem.text), trim(elem.tail)

    # adapt content string
    if elem.tag != "lb" and not elem.text and elem.tail:
        elem.text, elem.tail = elem.tail, None

    # content checks
    if elem.text or elem.tail:
        if textfilter(elem) or (options.dedup and duplicate_test(elem, options)):
            return None

    return elem
