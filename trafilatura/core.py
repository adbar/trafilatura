# pylint:disable-msg=E0611,I1101
"""
Module bundling all functions needed to extract the text in a webpage.
"""

import logging
import re  # import regex as re
import sys
import warnings

from copy import deepcopy

from lxml.etree import Element, SubElement, XPath, strip_elements, strip_tags, tostring

# own
from .baseline import baseline
from .external import compare_extraction
from .filters import (LANGID_FLAG, check_html_lang, duplicate_test,
                      language_filter, text_chars_test)
from .hashing import content_fingerprint
from .htmlprocessing import (convert_tags, delete_by_link_density,
                             handle_textnode, link_density_test_tables,
                             process_node, prune_unwanted_nodes, tree_cleaning)
from .metadata import Document, extract_metadata, set_date_params
from .settings import DEFAULT_CONFIG, TAG_CATALOG, use_config
from .utils import FORMATTING_PROTECTED, is_image_file, load_html, normalize_unicode
from .xml import build_json_output, control_xml_output, xmltotxt, xmltocsv
from .xpaths import (BODY_XPATH, COMMENTS_DISCARD_XPATH, COMMENTS_XPATH,
                     DISCARD_IMAGE_ELEMENTS, OVERALL_DISCARD_XPATH,
                     PAYWALL_DISCARD_XPATH, PRECISION_DISCARD_XPATH,
                     REMOVE_COMMENTS_XPATH, TEASER_DISCARD_XPATH)

LOGGER = logging.getLogger(__name__)

P_FORMATTING = {'hi', 'ref'}
TABLE_ELEMS = {'td', 'th'}
TABLE_ALL = {'td', 'th', 'hi'}
FORMATTING = {'hi', 'ref', 'span'}
CODES_QUOTES = {'code', 'quote'}
NOT_AT_THE_END = {'head', 'ref'}


class Extractor:
    "Defines a class to store all extraction options."
    __slots__ = [
    'config',
    # general
    'format', 'fast', 'precision', 'recall', 'comments',
    'formatting', 'links', 'images', 'tables', 'dedup', 'lang',
    # extraction size
    'min_extracted_size', 'min_output_size',
    'min_output_comm_size', 'min_extracted_comm_size',
    # deduplication
    'min_duplcheck_size', 'max_repetitions',
    # rest
    'max_file_size', 'min_file_size', 'max_tree_size',
    # meta
    'url', 'only_with_metadata', 'tei_validation', 'date_params',
    'author_blacklist', 'url_blacklist'
    ]
    # consider dataclasses for Python 3.7+
    def __init__(self, *, config=DEFAULT_CONFIG, output_format="txt",
                 fast=False, precision=False, recall=False,
                 comments=True, formatting=False, links=False, images=False,
                 tables=True, dedup=False, lang=None, max_tree_size=None,
                 url=None, only_with_metadata=False, tei_validation=False,
                 author_blacklist=None, url_blacklist=None, date_params=None):
        self._add_config(config)
        self.format = output_format
        self.fast = fast
        self.precision = precision
        self.recall = recall
        self.comments = comments
        self.formatting = formatting
        self.links = links
        self.images = images
        self.tables = tables
        self.dedup = dedup
        self.lang = lang
        self.max_tree_size = max_tree_size
        self.url = url
        self.only_with_metadata = only_with_metadata
        self.tei_validation = tei_validation
        self.author_blacklist = author_blacklist or set()
        self.url_blacklist = url_blacklist or set()
        self.date_params = set_date_params(date_params, not self.config.getboolean('DEFAULT', 'EXTENSIVE_DATE_SEARCH'))

    def _add_config(self, config):
        "Store options loaded from config file."
        self.min_extracted_size = config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE')
        self.min_output_size = config.getint('DEFAULT', 'MIN_OUTPUT_SIZE')
        self.min_output_comm_size = config.getint('DEFAULT', 'MIN_OUTPUT_COMM_SIZE')
        self.min_extracted_comm_size = config.getint('DEFAULT', 'MIN_EXTRACTED_COMM_SIZE')
        self.min_duplcheck_size = config.getint('DEFAULT', 'MIN_DUPLCHECK_SIZE')
        self.max_repetitions = config.getint('DEFAULT', 'MAX_REPETITIONS')
        self.max_file_size = config.getint('DEFAULT', 'MAX_FILE_SIZE')
        self.min_file_size = config.getint('DEFAULT', 'MIN_FILE_SIZE')
        self.config = config  # todo: remove?


def handle_titles(element, options):
    '''Process head elements (titles)'''
    if len(element) == 0:
        # maybe needs attention?
        # if element.tail and re.search(r'\w', element.tail):
        #    LOGGER.debug('tail in title, stripping: %s', element.tail)
        #    element.tail = None
        title = process_node(element, options)
    # children
    else:
        title = deepcopy(element)
        # list instead of element.iter('*')
        # TODO: write tests for it and check
        for child in list(element):
            # if child.tag not in potential_tags:
            #    LOGGER.debug('unexpected in title: %s %s %s', child.tag, child.text, child.tail)
            #    continue
            processed_child = handle_textnode(child, options, comments_fix=False)
            if processed_child is not None:
                title.append(processed_child)
            child.tag = 'done'
    if title is not None and text_chars_test(''.join(title.itertext())) is True:
        return title
    return None


def handle_formatting(element, options):
    '''Process formatting elements (b, i, etc. converted to hi) found
       outside of paragraphs'''
    formatting = process_node(element, options)
    if len(element) == 0 and formatting is None:
        return None
    # repair orphan elements
    # if formatting is None:
    #    formatting = Element(element.tag)
    #     return None
    # if len(element) > 0:
    #    for child in element.iter('*'):
    #        if child.tag not in potential_tags:
    #            LOGGER.debug('unexpected in title: %s %s %s', child.tag, child.text, child.tail)
    #            continue
    #        processed_child = handle_textnode(child, options, comments_fix=False)
    #        if processed_child is not None:
    #            formatting.append(processed_child)
    #        child.tag = 'done'
    # if text_chars_test(element.text) is True:
    #    processed_child.text = trim(element.text)
    # if text_chars_test(element.tail) is True:
    #    processed_child.tail = trim(element.tail)
    # if len(element) == 0:
    #    processed_element = process_node(element, options)
    # children
    # else:
    #    processed_element = Element(element.tag)
    #    processed_element.text, processed_element.tail = element.text, element.tail
    #    for child in element.iter('*'):
    #        processed_child = handle_textnode(child, options, comments_fix=False)
    #        if processed_child is not None:
    #            processed_element.append(processed_child)
    #        child.tag = 'done'
    # repair orphan elements
    # shorter code but triggers warning:
    # parent = element.getparent() or element.getprevious()
    parent = element.getparent()
    if parent is None:
        parent = element.getprevious()
    if parent is None or parent.tag not in FORMATTING_PROTECTED:
        processed_element = Element('p')
        processed_element.insert(0, formatting)
    else:
        processed_element = formatting
    return processed_element


def add_sub_element(new_child_elem, subelem, processed_subchild):
    sub_child_elem = SubElement(new_child_elem, processed_subchild.tag)
    sub_child_elem.text, sub_child_elem.tail = processed_subchild.text, processed_subchild.tail
    for attr in subelem.attrib:
        sub_child_elem.set(attr, subelem.get(attr))


def process_nested_elements(child, new_child_elem, options):
    new_child_elem.text = child.text
    for subelem in child.iterdescendants("*"):
        if subelem.tag == "list":
            processed_subchild = handle_lists(subelem, options)
            if processed_subchild is not None:
                new_child_elem.append(processed_subchild)
        else:
            processed_subchild = handle_textnode(subelem, options, comments_fix=False)
            if processed_subchild is not None:
                add_sub_element(new_child_elem, subelem, processed_subchild)
        subelem.tag = "done"
        #subelem.getparent().remove(subelem)


def update_elem_rendition(elem, new_elem):
    # set attribute
    if elem.get("rend") is not None:
        new_elem.set("rend", elem.get("rend"))


def is_text_element(elem):
    return elem is not None and text_chars_test(''.join(elem.itertext())) is True


def define_newelem(processed_elem, orig_elem):
    if processed_elem is not None:
        childelem = SubElement(orig_elem, processed_elem.tag)
        childelem.text, childelem.tail = processed_elem.text, processed_elem.tail


def handle_lists(element, options):
    "Process lists elements including their descendants."
    processed_element = Element(element.tag)

    if element.text is not None and element.text.strip():
        new_child_elem = SubElement(processed_element, "item")
        new_child_elem.text = element.text
    # if element.tail is not None:
    #    processed_element.tail = element.text

    for child in element.iterdescendants("item"):
        new_child_elem = Element("item")
        if len(child) == 0:
            processed_child = process_node(child, options)
            if processed_child is not None:
                new_child_elem.text = processed_child.text
                if processed_child.tail is not None and processed_child.tail.strip():
                    new_child_elem.text += " " + processed_child.tail
                processed_element.append(new_child_elem)
        else:
            process_nested_elements(child, new_child_elem, options)
            if child.tail is not None and child.tail.strip():
                new_child_elem_children = [el for el in new_child_elem.getchildren() if el.tag != "done"]
                if new_child_elem_children:
                    last_subchild = new_child_elem_children[-1]
                    if last_subchild.tail is None or not last_subchild.tail.strip():
                        last_subchild.tail = child.tail
                    else:
                        last_subchild.tail += " " + child.tail
        if new_child_elem.text or len(new_child_elem) > 0:
            update_elem_rendition(child, new_child_elem)
            processed_element.append(new_child_elem)
        child.tag = "done"
    element.tag = "done"
    # test if it has children and text. Avoid double tags??
    if is_text_element(processed_element):
        update_elem_rendition(element, processed_element)
        return processed_element
    return None


def is_code_block_element(element):
    "Check if it is a code element according to common structural markers."
    # pip
    if element.get("lang") or element.tag == "code":
        return True
    # GitHub
    parent = element.getparent()
    if parent is not None and "highlight" in parent.get("class", ""):
        return True
    # highlightjs
    code = element.find("code")
    if code is not None and len(element) == 1:
        return True
    return False


def handle_code_blocks(element):
    "Turn element into a properly tagged code block."
    processed_element = deepcopy(element)
    for child in element.iter("*"):
        child.tag = "done"
    processed_element.tag = "code"
    return processed_element


def handle_quotes(element, options):
    "Process quotes elements."
    if is_code_block_element(element):
        return handle_code_blocks(element)

    processed_element = Element(element.tag)
    for child in element.iter("*"):
        processed_child = process_node(child, options)  # handle_textnode(child, comments_fix=True)
        define_newelem(processed_child, processed_element)
        child.tag = "done"
    if is_text_element(processed_element):
        # avoid double/nested tags
        strip_tags(processed_element, "quote")
        return processed_element
    return None


def handle_other_elements(element, potential_tags, options):
    "Handle diverse or unknown elements in the scope of relevant tags."
    # handle w3schools code
    if element.tag == "div" and "w3-code" in element.get("class", ""):
        return handle_code_blocks(element)

    # delete unwanted
    if element.tag not in potential_tags:
        if element.tag != "done":
            LOGGER.debug("discarding element: %s %s", element.tag, element.text)
        return None

    if element.tag == "div":
        # make a copy and prune it in case it contains sub-elements handled on their own?
        # divcopy = deepcopy(element)
        processed_element = handle_textnode(element, options, comments_fix=False, preserve_spaces=True)
        if processed_element is not None and text_chars_test(processed_element.text) is True:
            processed_element.attrib.clear()
            # small div-correction # could be moved elsewhere
            if processed_element.tag == "div":
                processed_element.tag = "p"
            # insert
            return processed_element
    else:
        LOGGER.debug("unexpected element seen: %s %s", element.tag, element.text)

    return None


def handle_paragraphs(element, potential_tags, options):
    "Process paragraphs along with their children, trim and clean the content."
    element.attrib.clear()  # todo: test if necessary
    # strip_tags(element, 'p') # change in precision due to spaces?

    # no children
    if len(element) == 0:
        return process_node(element, options)

    # children
    processed_element = Element(element.tag)
    for child in element.iter("*"):
        if child.tag not in potential_tags and child.tag != "done":
            LOGGER.debug("unexpected in p: %s %s %s", child.tag, child.text, child.tail)
            continue
        # spacing = child.tag in SPACING_PROTECTED  # todo: outputformat.startswith('xml')?
        # todo: act on spacing here?
        processed_child = handle_textnode(child, options, comments_fix=False, preserve_spaces=True)
        if processed_child is not None:
            # todo: needing attention!
            if processed_child.tag == "p":
                LOGGER.debug("extra p within p: %s %s %s", processed_child.tag, processed_child.text,
                             processed_child.tail)
                if processed_element.text:
                    processed_element.text += " " + processed_child.text
                else:
                    processed_element.text = processed_child.text
                child.tag = "done"
                continue
            # handle formatting
            newsub = Element(child.tag)
            if processed_child.tag in P_FORMATTING:
                # check depth and clean
                if len(processed_child) > 0:
                    for item in processed_child:  # children are lists
                        if text_chars_test(item.text) is True:
                            item.text = " " + item.text
                        strip_tags(processed_child, item.tag)
                # correct attributes
                if child.tag == "hi":
                    newsub.set("rend", child.get("rend"))
                elif child.tag == "ref":
                    if child.get("target") is not None:
                        newsub.set("target", child.get("target"))
            # handle line breaks
            # elif processed_child.tag == 'lb':
            #    try:
            #        processed_child.tail = process_node(child, options).tail
            #    except AttributeError:  # no text
            #        pass
            # prepare text
            # todo: to be moved to handle_textnode()
            # if text_chars_test(processed_child.text) is False:
            #    processed_child.text = ''
            # if text_chars_test(processed_child.tail) is False:
            #    processed_child.tail = ''
            # if there are already children
            # if len(processed_element) > 0:
            #    if text_chars_test(processed_child.tail) is True:
            #        newsub.tail = processed_child.text + processed_child.tail
            #    else:
            #        newsub.tail = processed_child.text
            newsub.text, newsub.tail = processed_child.text, processed_child.tail
            processed_element.append(newsub)
        child.tag = "done"
    # finish
    if len(processed_element) > 0:
        last_elem = processed_element[-1]
        # clean trailing lb-elements
        if last_elem.tag == "lb" and last_elem.tail is None:
            last_elem.getparent().remove(last_elem)
        return processed_element
    if processed_element.text:
        return processed_element
    LOGGER.debug("discarding p-child: %s", tostring(processed_element))
    return None


def define_cell_type(element):
    "Determine cell element type and mint new element."
    # define tag
    cell_element = Element("cell")
    if element.tag == "th":
        cell_element.set("role", "head")
    return cell_element


def handle_table(table_elem, potential_tags, options):
    "Process single table element."
    newtable = Element("table")
    newrow = Element("row")

    # strip these structural elements
    strip_tags(table_elem, "thead", "tbody", "tfoot")

    # explore sub-elements
    for subelement in table_elem.iterdescendants():
        if subelement.tag == "tr":
            # process existing row
            if len(newrow) > 0:
                newtable.append(newrow)
                newrow = Element("row")
        elif subelement.tag in TABLE_ELEMS:
            new_child_elem = define_cell_type(subelement)
            # process
            if len(subelement) == 0:
                processed_cell = process_node(subelement, options)
                if processed_cell is not None:
                    new_child_elem.text, new_child_elem.tail = processed_cell.text, processed_cell.tail
            else:
                # proceed with iteration, fix for nested elements
                new_child_elem.text, new_child_elem.tail = subelement.text, subelement.tail
                subelement.tag = "done"
                for child in subelement.iterdescendants():
                    if child.tag in TABLE_ALL:
                        # todo: define attributes properly
                        if child.tag in TABLE_ELEMS:
                            # subcell_elem = define_cell_type(subelement)
                            child.tag = "cell"
                        processed_subchild = handle_textnode(child, options, preserve_spaces=True, comments_fix=True)
                    # todo: lists in table cells
                    elif child.tag == "list" and options.recall:
                        processed_subchild = handle_lists(child, options)
                        if processed_subchild is not None:
                            new_child_elem.append(processed_subchild)
                            processed_subchild = None  # don't handle it anymore
                    else:
                        # subcell_elem = Element(child.tag)
                        processed_subchild = handle_textelem(child, potential_tags.union(["div"]), options)
                    # add child element to processed_element
                    define_newelem(processed_subchild, new_child_elem)
                    child.tag = "done"
            # add to tree
            if new_child_elem.text or len(new_child_elem) > 0:
                newrow.append(new_child_elem)
        # beware of nested tables
        elif subelement.tag == "table":
            break
        # cleanup
        subelement.tag = "done"

    # end of processing
    if len(newrow) > 0:
        newtable.append(newrow)
    if len(newtable) > 0:
        return newtable
    return None


def handle_image(element):
    "Process image elements and their relevant attributes."
    processed_element = Element(element.tag)

    for attr in ("data-src", "src"):
        src = element.get(attr)
        if is_image_file(src):
            processed_element.set("src", src)
            break
    else:
        # take the first corresponding attribute
        for attr, value in element.attrib.items():
            if attr.startswith("data-src") and is_image_file(value):
                processed_element.set("src", value)
                break

    # additional data
    if element.get("alt") is not None:
        processed_element.set("alt", element.get("alt"))
    if element.get("title") is not None:
        processed_element.set("title", element.get("title"))

    # don't return empty elements or elements without source, just None
    if not processed_element.attrib or not processed_element.get("src"):
        return None

    # post-processing: URLs
    if not processed_element.get("src").startswith("http"):
        processed_element.set("src", re.sub(r"^//", "http://", processed_element.get("src")))

    return processed_element


def handle_textelem(element, potential_tags, options):
    '''Process text element and determine how to deal with its content'''
    new_element = None
    # bypass: nested elements
    if element.tag == 'list':
        new_element = handle_lists(element, options)
    elif element.tag in CODES_QUOTES:
        new_element = handle_quotes(element, options)
    elif element.tag == 'head':
        new_element = handle_titles(element, options)
    elif element.tag == 'p':
        new_element = handle_paragraphs(element, potential_tags, options)
    elif element.tag == 'lb':
        if text_chars_test(element.tail) is True:
            element = process_node(element, options)
            if element is not None:
                new_element = Element('p')
                new_element.text = element.tail
    elif element.tag in FORMATTING:
        new_element = handle_formatting(element, options)  # process_node(element, options)
    elif element.tag == 'table' and 'table' in potential_tags:
        new_element = handle_table(element, potential_tags, options)
    elif element.tag == 'graphic' and 'graphic' in potential_tags:
        new_element = handle_image(element)
    else:
        # other elements (div, ??, ??)
        new_element = handle_other_elements(element, potential_tags, options)
    return new_element


def recover_wild_text(tree, result_body, options, potential_tags=TAG_CATALOG):
    '''Look for all previously unconsidered wild elements, including outside of the determined
       frame and throughout the document to recover potentially missing text parts'''
    LOGGER.debug('Recovering wild text elements')
    search_expr = './/blockquote|.//code|.//p|.//pre|.//q|.//quote|.//table|.//div[contains(@class, \'w3-code\')]'
    if options.recall is True:
        potential_tags.update(['div', 'lb'])
        search_expr += '|.//div|.//lb|.//list'
    # prune
    search_tree = prune_unwanted_sections(tree, potential_tags, options)
    # decide if links are preserved
    if 'ref' not in potential_tags:
        strip_tags(search_tree, 'a', 'ref', 'span')
    else:
        strip_tags(search_tree, 'span')
    subelems = search_tree.xpath(search_expr)
    result_body.extend(filter(lambda x: x is not None, (handle_textelem(e, potential_tags, options)
                       for e in subelems)))
    return result_body


def prune_unwanted_sections(tree, potential_tags, options):
    'Rule-based deletion of targeted document sections'
    # prune the rest
    tree = prune_unwanted_nodes(tree, OVERALL_DISCARD_XPATH, with_backup=True)
    tree = prune_unwanted_nodes(tree, PAYWALL_DISCARD_XPATH)
    # decide if images are preserved
    if 'graphic' not in potential_tags:
        tree = prune_unwanted_nodes(tree, DISCARD_IMAGE_ELEMENTS)
    # balance precision/recall
    if options.recall is False:
        tree = prune_unwanted_nodes(tree, TEASER_DISCARD_XPATH)
        if options.precision is True:
            tree = prune_unwanted_nodes(tree, PRECISION_DISCARD_XPATH)
    # remove elements by link density
    tree = delete_by_link_density(tree, 'div', backtracking=True, favor_precision=options.precision)
    tree = delete_by_link_density(tree, 'list', backtracking=False, favor_precision=options.precision)
    tree = delete_by_link_density(tree, 'p', backtracking=False, favor_precision=options.precision)
    # also filter fw/head, table and quote elements?
    if options.precision is True:
        # delete trailing titles
        while len(tree) > 0 and (tree[-1].tag == 'head'):
            tree[-1].getparent().remove(tree[-1])
        tree = delete_by_link_density(tree, 'head', backtracking=False)  # favor_precision=options.precision
        tree = delete_by_link_density(tree, 'quote', backtracking=False)  # favor_precision=options.precision
    return tree


def extract_content(tree, options):
    '''Find the main content of a page using a set of XPath expressions,
       then extract relevant elements, strip them of unwanted subparts and
       convert them'''
    # backup
    backup_tree = deepcopy(tree)
    # init
    result_body = Element('body')
    potential_tags = set(TAG_CATALOG)
    if options.tables is True:
        potential_tags.update(['table', 'td', 'th', 'tr'])
    if options.images is True:
        potential_tags.add('graphic')
    if options.links is True:
        potential_tags.add('ref')
    # iterate
    for expr in BODY_XPATH:
        # select tree if the expression has been found
        subtree = next((s for s in expr(tree) if s is not None), None)
        if subtree is None:
            continue
        # prune the subtree
        subtree = prune_unwanted_sections(subtree, potential_tags, options)
        # second pass?
        # subtree = delete_by_link_density(subtree, 'list', backtracking=False, favor_precision=options.precision)
        if 'table' in potential_tags or options.precision is True:
            for elem in subtree.iter('table'):
                if link_density_test_tables(elem) is True:
                    elem.getparent().remove(elem)
        # skip if empty tree
        if len(subtree) == 0:
            continue
        # no paragraphs containing text, or not enough
        ptest = subtree.xpath('//p//text()')
        if options.recall is True:
            factor = 5
        elif options.precision is True:
            factor = 1
        else:
            factor = 3
        if not ptest or len(''.join(ptest)) < options.min_extracted_size * factor:
            potential_tags.add('div')
        # polish list of potential tags
        if 'ref' not in potential_tags:
            strip_tags(subtree, 'ref')
        if 'span' not in potential_tags:
            strip_tags(subtree, 'span')
        LOGGER.debug(sorted(potential_tags))
        # proper extraction
        subelems = subtree.xpath('.//*')
        # e.g. only lb-elems in a div
        if {e.tag for e in subelems} == {'lb'}:
            subelems = [subtree]
        # extract content
        result_body.extend([el for el in (handle_textelem(e, potential_tags, options) for e in subelems) if el is not None])
        # remove trailing titles
        while len(result_body) > 0 and (result_body[-1].tag in NOT_AT_THE_END):
            result_body[-1].getparent().remove(result_body[-1])
        # exit the loop if the result has children
        if len(result_body) > 1:
            LOGGER.debug(expr)
            break
    temp_text = ' '.join(result_body.itertext()).strip()
    # try parsing wild <p> elements if nothing found or text too short
    # todo: test precision and recall settings here
    if len(result_body) == 0 or len(temp_text) < options.min_extracted_size:
        result_body = recover_wild_text(backup_tree, result_body, options, potential_tags)
        temp_text = ' '.join(result_body.itertext()).strip()
    # filter output
    strip_elements(result_body, 'done')
    strip_tags(result_body, 'div')
    # return
    return result_body, temp_text, len(temp_text)


def process_comments_node(elem, potential_tags, options):
    '''Process comment node and determine how to deal with its content'''
    if elem.tag in potential_tags:
        # print(elem.tag, elem.text_content())
        processed_element = handle_textnode(elem, options, comments_fix=True)
        # test length and remove
        if processed_element is not None:  # and processed_element.text not in COMMENTS_BLACKLIST:
            processed_element.attrib.clear()
            # if textfilter(elem) is True:  # ^Pingback
            #    return None
            return processed_element
    return None


def extract_comments(tree, options):
    "Try and extract comments out of potential sections in the HTML."
    comments_body = Element("body")
    # define iteration strategy
    potential_tags = set(TAG_CATALOG)  # 'span'
    # potential_tags.add('div') trouble with <div class="comment-author meta">
    for expr in COMMENTS_XPATH:
        # select tree if the expression has been found
        subtree = next((s for s in expr(tree) if s is not None), None)
        if subtree is None:
            continue
        # prune
        subtree = prune_unwanted_nodes(subtree, COMMENTS_DISCARD_XPATH)
        # todo: unified stripping function, taking include_links into account
        strip_tags(subtree, "a", "ref", "span")
        # extract content
        # for elem in subtree.xpath('.//*'):
        #    processed_elem = process_comments_node(elem, potential_tags)
        #    if processed_elem is not None:
        #        comments_body.append(processed_elem)
        # processed_elems = (process_comments_node(elem, potential_tags, options) for elem in
        #                    subtree.xpath('.//*'))
        comments_body.extend(filter(lambda x: x is not None, (process_comments_node(e, potential_tags, options) for e in subtree.xpath(".//*"))))
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            subtree.getparent().remove(subtree)
            break
    # lengths
    temp_comments = " ".join(comments_body.itertext()).strip()
    return comments_body, temp_comments, len(temp_comments), tree


def determine_returnstring(document, options):
    '''Convert XML tree to chosen format, clean the result and output it as a string'''
    # XML (TEI) steps
    if 'xml' in options.format:
        # last cleaning
        for element in document.body.iter('*'):
            if element.tag != 'graphic' and len(element) == 0 and not element.text and not element.tail:
                parent = element.getparent()
                # do not remove elements inside <code> to preserve formatting
                if parent is not None and parent.tag != 'code':
                    parent.remove(element)
        # build output tree
        returnstring = control_xml_output(document, options)
    # CSV
    elif options.format == 'csv':
        returnstring = xmltocsv(document, options.formatting)
    # JSON
    elif options.format == 'json':
        returnstring = build_json_output(document)
    # TXT
    else:
        returnstring = xmltotxt(document.body, options.formatting)
        if document.commentsbody is not None:
            returnstring = f"{returnstring}\n{xmltotxt(document.commentsbody, options.formatting)}".strip()
    # normalize Unicode format (defaults to NFC)
    return normalize_unicode(returnstring)


def bare_extraction(filecontent, url=None, no_fallback=False,  # fast=False,
                    favor_precision=False, favor_recall=False,
                    include_comments=True, output_format='python', target_language=None,
                    include_tables=True, include_images=False, include_formatting=False,
                    include_links=False, deduplicate=False,
                    date_extraction_params=None,
                    only_with_metadata=False, with_metadata=False,
                    max_tree_size=None, url_blacklist=None, author_blacklist=None,
                    as_dict=True, prune_xpath=None,
                    config=DEFAULT_CONFIG, options=None):
    """Internal function for text extraction returning bare Python variables.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        no_fallback: Use faster heuristics and skip backup extraction.
        favor_precision: prefer less text but correct extraction.
        favor_recall: prefer more text even when unsure.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format, Python being the default
            and the interest of this internal function.
            Other values: "txt", "csv", "json", "xml", or "xmltei".
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (present in XML format, converted to markdown otherwise).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        only_with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        max_tree_size: Discard documents with too many elements.
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.
        as_dict: Legacy option, return a dictionary instead of a class with attributes.
        prune_xpath: Provide an XPath expression to prune the tree before extraction.
            can be str or list of str.
        config: Directly provide a configparser configuration.
        options: Directly provide a whole extractor configuration.

    Returns:
        A Python dict() containing all the extracted information or None.

    Raises:
        ValueError: Extraction problem.
    """

    # deprecation warnings
    if with_metadata is True:
        only_with_metadata = with_metadata
        warnings.warn(
            '"with_metadata" will be deprecated in a future version, use "only_with_metadata instead"',
            PendingDeprecationWarning
        )
    #if no_fallback is True:
    #    fast = no_fallback
        #warnings.warn(
        #    '"no_fallback" will be deprecated in a future version, use "fast" instead',
        #    PendingDeprecationWarning
        #)

    # load data
    try:
        tree = load_html(filecontent)
        if tree is None:
            LOGGER.error('empty HTML tree for URL %s', url)
            raise ValueError

        # regroup extraction options
        if not options or not isinstance(options, Extractor):
            options = Extractor(
                          config=config, output_format=output_format,
                          fast=no_fallback, precision=favor_precision, recall=favor_recall,
                          comments=include_comments, formatting=include_formatting, links=include_links,
                          images=include_images, tables=include_tables,
                          dedup=deduplicate, lang=target_language, max_tree_size=max_tree_size,
                          url=url, only_with_metadata=only_with_metadata,
                          author_blacklist=author_blacklist, url_blacklist=url_blacklist,
                          date_params=date_extraction_params
                      )

        # quick and dirty HTML lang check
        if options.lang and (options.fast or LANGID_FLAG is False):
            if check_html_lang(tree, options.lang) is False:
                LOGGER.error('wrong HTML meta language for URL %s', options.url)
                raise ValueError

        # extract metadata if necessary
        if options.format != 'txt':

            document = extract_metadata(tree, options.url, options.date_params, options.fast, options.author_blacklist)

            # cut short if extracted URL in blacklist
            if document.url in options.url_blacklist:
                LOGGER.warning('blacklisted URL: %s', document.url)
                raise ValueError

            # cut short if core elements are missing
            if options.only_with_metadata and any(
                    x is None for x in
                    [document.date, document.title, document.url]
            ):
                LOGGER.error('no metadata for URL %s', document.url)
                raise ValueError

        else:
            document = Document()

        # prune all xpath expressions that user specified
        # no backup as this is unetre full control of the user
        if prune_xpath is not None:
            if isinstance(prune_xpath, str):
                prune_xpath = [prune_xpath]
            tree = prune_unwanted_nodes(tree, [XPath(x) for x in prune_xpath])

        # backup (or not) for further processing
        tree_backup_1 = deepcopy(tree) if not options.fast else None
        tree_backup_2 = deepcopy(tree)

        # clean + use LXML cleaner
        cleaned_tree = tree_cleaning(tree, options)
        cleaned_tree_backup = deepcopy(cleaned_tree)

        # convert tags, the rest does not work without conversion
        cleaned_tree = convert_tags(cleaned_tree, options, options.url or document.url)

        # comments first, then remove
        if options.comments:
            commentsbody, temp_comments, len_comments, cleaned_tree = extract_comments(cleaned_tree, options)
        else:
            commentsbody, temp_comments, len_comments = None, '', 0
        if options.precision:
            cleaned_tree = prune_unwanted_nodes(cleaned_tree, REMOVE_COMMENTS_XPATH)

        # extract content
        postbody, temp_text, len_text = extract_content(cleaned_tree, options)

        # compare if necessary
        if not options.fast:
            postbody, temp_text, len_text = compare_extraction(cleaned_tree_backup, tree_backup_1, postbody, temp_text, len_text, options)
        # add baseline as additional fallback
        # rescue: try to use original/dirty tree # and favor_precision is False=?
        if len_text < options.min_extracted_size:
            postbody, temp_text, len_text = baseline(tree_backup_2)
            LOGGER.debug('non-clean extracted length: %s (extraction)', len_text)

        # tree size sanity check
        if options.max_tree_size:
            # strip tags
            if len(postbody) > options.max_tree_size:
                LOGGER.debug('output tree too long: %s', len(postbody))
                strip_tags(postbody, 'hi')
            # still too long, raise an error
            if len(postbody) > options.max_tree_size:
                LOGGER.debug('output tree too long: %s, discarding file', len(postbody))
                raise ValueError
        # size checks
        if len_comments < options.min_extracted_comm_size:
            LOGGER.debug('not enough comments %s', url)
        if len_text < options.min_output_size and \
           len_comments < options.min_output_comm_size:
            LOGGER.debug('text and comments not long enough: %s %s', len_text, len_comments)
            raise ValueError

        # check duplicates at body level
        if options.dedup and duplicate_test(postbody, options) is True:
            LOGGER.debug('discarding duplicate document for URL %s', url)
            raise ValueError

        # sanity check on language
        if options.lang:
            is_not_target_lang, document = language_filter(temp_text, temp_comments, options.lang, document)
            if is_not_target_lang is True:
                LOGGER.debug('wrong language for URL %s', url)
                raise ValueError

    except (TypeError, ValueError):
        LOGGER.warning('discarding data for url: %s', url)  # document.url , record_id
        return None

    # special case: python variables
    if options.format == 'python':
        document.text = xmltotxt(postbody, options.formatting)
        if options.comments:
            document.comments = xmltotxt(commentsbody, options.formatting)
            document.commentsbody = commentsbody
        document.raw_text = document.text
    else:
        document.raw_text, document.commentsbody = temp_text, commentsbody
    document.body = postbody

    return document if not as_dict else document.as_dict()


def extract(filecontent, url=None, record_id=None, no_fallback=False,
            favor_precision=False, favor_recall=False,
            include_comments=True, output_format='txt',
            tei_validation=False, target_language=None,
            include_tables=True, include_images=False, include_formatting=False,
            include_links=False, deduplicate=False,
            date_extraction_params=None,
            only_with_metadata=False, with_metadata=False,
            max_tree_size=None, url_blacklist=None, author_blacklist=None,
            settingsfile=None, prune_xpath=None,
            config=DEFAULT_CONFIG, options=None,
            **kwargs):
    """Main function exposed by the package:
       Wrapper for text extraction and conversion to chosen output format.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        record_id: Add an ID to the metadata.
        no_fallback: Skip the backup extraction with readability-lxml and justext.
        favor_precision: prefer less text but correct extraction.
        favor_recall: when unsure, prefer more text.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format:
            'txt', 'csv', 'json', 'xml', or 'xmltei'.
        tei_validation: Validate the XML-TEI output with respect to the TEI standard.
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (only valuable if output_format is set to XML).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        only_with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        max_tree_size: Discard documents with too many elements.
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.
        settingsfile: Use a configuration file to override the standard settings.
        prune_xpath: Provide an XPath expression to prune the tree before extraction.
            can be str or list of str.
        config: Directly provide a configparser configuration.
        options: Directly provide a whole extractor configuration.

    Returns:
        A string in the desired format or None.

    """
    # older, deprecated functions
    if kwargs and any([
        # output formats
            'csv_output' in kwargs,
            'json_output' in kwargs,
            'tei_output' in kwargs,
            'xml_output' in kwargs
        ]):
        raise NameError(
            'Deprecated argument: use output_format instead, e.g. output_format="xml"'
            )
        # todo: add with_metadata later

    # regroup extraction options
    if not options or not isinstance(options, Extractor):
        options = Extractor(
                      config=use_config(settingsfile, config), output_format=output_format,
                      fast=no_fallback, precision=favor_precision, recall=favor_recall,
                      comments=include_comments, formatting=include_formatting, links=include_links,
                      images=include_images, tables=include_tables,
                      dedup=deduplicate, lang=target_language, max_tree_size=max_tree_size,
                      url=url, only_with_metadata=only_with_metadata,
                      tei_validation=tei_validation,
                      author_blacklist=author_blacklist, url_blacklist=url_blacklist,
                      date_params=date_extraction_params
                  )

    # extraction
    try:
        document = bare_extraction(
            filecontent, options=options,
            with_metadata=with_metadata,
            as_dict=False, prune_xpath=prune_xpath,
        )
    except RuntimeError:
        LOGGER.error('Processing timeout for %s', url)
        document = None

    # post-processing
    if document is None:
        return None
    if options.format != 'txt':
        # add record ID to metadata
        document.id = record_id
        # calculate fingerprint
        if document.raw_text is not None:
            document.fingerprint = content_fingerprint(str(document.title) + " " + str(document.raw_text))

    # return
    return determine_returnstring(document, options)


def process_record(content, *args, **kwargs):
    "Deprecated extraction function."
    sys.exit("process_record() is deprecated, use extract() instead")
