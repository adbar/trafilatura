# pylint:disable-msg=E0611,I1101
"""
Module bundling all functions needed to extract the text in a webpage.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


# standard
import logging
import re  # import regex as re
import warnings

from copy import deepcopy

# SIGALRM isn't present on Windows, detect it
try:
    from signal import signal, alarm, SIGALRM
    HAS_SIGNAL = True
except ImportError:
    HAS_SIGNAL = False

from lxml.etree import Element, SubElement, strip_elements, strip_tags
from lxml.html import tostring

# own
from .external import justext_rescue, sanitize_tree, SANITIZED_XPATH, try_readability
from .filters import (LANGID_FLAG, check_html_lang, content_fingerprint, duplicate_test,
                      language_filter, text_chars_test)
from .htmlprocessing import (convert_tags, handle_textnode, process_node,
                             delete_by_link_density, link_density_test_tables,
                             prune_unwanted_nodes, tree_cleaning)
from .metadata import extract_metadata, Document
from .settings import use_config, DEFAULT_CONFIG, TAG_CATALOG
from .utils import is_image_file, load_html, normalize_unicode, trim, txttocsv
from .xml import (build_json_output, build_xml_output, build_tei_output,
                  control_xml_output, xmltotxt)
from .xpaths import (BODY_XPATH, COMMENTS_XPATH, COMMENTS_DISCARD_XPATH, OVERALL_DISCARD_XPATH,
                     TEASER_DISCARD_XPATH, PAYWALL_DISCARD_XPATH, PRECISION_DISCARD_XPATH,
                     DISCARD_IMAGE_ELEMENTS, REMOVE_COMMENTS_XPATH)

LOGGER = logging.getLogger(__name__)

FORMATTING_PROTECTED = {'cell', 'head', 'hi', 'item', 'p', 'quote', 'td'}
SPACING_PROTECTED = {'code', 'hi', 'ref'}
P_FORMATTING = {'hi', 'ref'}
TABLE_ELEMS = {'td', 'th'}
TABLE_ALL = {'td', 'th', 'hi'}
FORMATTING = {'hi', 'ref', 'span'}
CODES_QUOTES = {'code', 'quote'}
NOT_AT_THE_END = {'fw', 'head', 'ref'}

JSON_SEARCH = re.compile(r'"articlebody": *"(.+?)(?<!\\)"', re.I)


class Extractor:
    "Defines a class to store all extraction options."
    __slots__ = [
    'config', 'fast', 'precision', 'recall', 'comments',
    'formatting', 'links', 'images', 'tables', 'dedup',
    ]
    # consider dataclasses for Python 3.7+
    def __init__(self, config, fast, precision, recall, comments,
                 formatting, links, images, tables, deduplicate):
        self.config = config
        self.fast = fast
        self.precision = precision
        self.recall = recall
        self.comments = comments
        self.formatting = formatting
        self.links = links
        self.images = images
        self.tables = tables
        self.dedup = deduplicate


def handle_titles(element, dedupbool, config):
    '''Process head elements (titles)'''
    if len(element) == 0:
        # maybe needs attention?
        # if element.tail and re.search(r'\w', element.tail):
        #    LOGGER.debug('tail in title, stripping: %s', element.tail)
        #    element.tail = None
        title = process_node(element, dedupbool, config)
    # children
    else:
        title = deepcopy(element)
        # list instead of element.iter('*')
        # TODO: write tests for it and check
        for child in list(element):
            # if child.tag not in potential_tags:
            #    LOGGER.debug('unexpected in title: %s %s %s', child.tag, child.text, child.tail)
            #    continue
            processed_child = handle_textnode(child, comments_fix=False, deduplicate=dedupbool, config=config)
            if processed_child is not None:
                title.append(processed_child)
            child.tag = 'done'
    if title is not None and text_chars_test(''.join(title.itertext())) is True:
        return title
    return None


def handle_formatting(element, dedupbool, config):
    '''Process formatting elements (b, i, etc. converted to hi) found
       outside of paragraphs'''
    formatting = process_node(element, dedupbool, config)
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
    #        processed_child = handle_textnode(child, comments_fix=False, deduplicate=dedupbool, config=config)
    #        if processed_child is not None:
    #            formatting.append(processed_child)
    #        child.tag = 'done'
    # if text_chars_test(element.text) is True:
    #    processed_child.text = trim(element.text)
    # if text_chars_test(element.tail) is True:
    #    processed_child.tail = trim(element.tail)
    # if len(element) == 0:
    #    processed_element = process_node(element, dedupbool, config)
    # children
    # else:
    #    processed_element = Element(element.tag)
    #    processed_element.text, processed_element.tail = element.text, element.tail
    #    for child in element.iter('*'):
    #        processed_child = handle_textnode(child, comments_fix=False, deduplicate=dedupbool, config=config)
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


def handle_lists(element, dedupbool, config):
    '''Process lists elements'''
    processed_element = Element(element.tag)
    if element.text is not None:
        processed_element.text = element.text
    # if element.tail is not None:
    #    processed_element.tail = element.text
    for child in element.iter('item'):
        newchildelem = Element('item')
        if len(child) == 0:
            processed_child = process_node(child, dedupbool, config)
            if processed_child is not None:
                newchildelem.text, newchildelem.tail = processed_child.text, processed_child.tail
                processed_element.append(newchildelem)
        else:
            # proceed with iteration, fix for nested elements
            for subelem in child.iter('*'):
                # beware of nested lists
                if subelem.tag == 'list':
                    processed_subchild = handle_lists(subelem, dedupbool, config)
                    if processed_subchild is not None:
                        newchildelem.append(processed_subchild)
                else:
                    processed_subchild = handle_textnode(subelem, comments_fix=False, deduplicate=dedupbool,
                                                         config=config)
                    # add child element to processed_element
                    if processed_subchild is not None:
                        subchildelem = SubElement(newchildelem, processed_subchild.tag)
                        subchildelem.text, subchildelem.tail = processed_subchild.text, processed_subchild.tail
                        if subelem.tag == 'ref' and subelem.get('target') is not None:
                            subchildelem.set('target', subelem.get('target'))
                # strip_tags(newchildelem, 'item')
                subelem.tag = 'done'
        if newchildelem.text or len(newchildelem) > 0:
            # set attribute
            if child.get('rend') is not None:
                newchildelem.set('rend', child.get('rend'))
            processed_element.append(newchildelem)
        child.tag = 'done'
    # test if it has children and text. Avoid double tags??
    if len(processed_element) > 0 and text_chars_test(''.join(processed_element.itertext())) is True:
        # set attribute
        if element.get('rend') is not None:
            processed_element.set('rend', element.get('rend'))
        return processed_element
    return None


def handle_quotes(element, dedupbool, config):
    '''Process quotes elements'''
    processed_element = Element(element.tag)
    for child in element.iter('*'):
        processed_child = process_node(child, dedupbool, config)  # handle_textnode(child, comments_fix=True)
        if processed_child is not None:
            newsub = SubElement(processed_element, child.tag)
            newsub.text, newsub.tail = processed_child.text, processed_child.tail
        child.tag = 'done'
    if len(processed_element) > 0 and text_chars_test(''.join(processed_element.itertext())) is True:
        # avoid double/nested tags
        strip_tags(processed_element, 'quote')
        return processed_element
    return None


def handle_other_elements(element, potential_tags, dedupbool, config):
    '''Handle diverse or unknown elements in the scope of relevant tags'''
    # delete unwanted
    if element.tag not in potential_tags:
        # LOGGER.debug('discarding: %s %s', element.tag, element.text)
        return None
    if element.tag == 'div':
        # make a copy and prune it in case it contains sub-elements handled on their own?
        # divcopy = deepcopy(element)
        processed_element = handle_textnode(element, comments_fix=False, deduplicate=dedupbool, config=config)
        if processed_element is not None and text_chars_test(processed_element.text) is True:
            processed_element.attrib.clear()
            # small div-correction # could be moved elsewhere
            if processed_element.tag == 'div':
                processed_element.tag = 'p'
            # insert
            return processed_element
    else:
        LOGGER.debug('unexpected element seen: %s %s', element.tag, element.text)
    return None


def handle_paragraphs(element, potential_tags, dedupbool, config):
    '''Process paragraphs (p) elements along with their children,
       trim and clean the content'''
    element.attrib.clear()
    # strip_tags(element, 'p') # change in precision due to spaces?
    # no children
    if len(element) == 0:
        processed_element = process_node(element, dedupbool, config)
        if processed_element is not None:
            return processed_element
        return None
    # children
    processed_element = Element(element.tag)
    for child in element.iter('*'):
        if child.tag not in potential_tags and child.tag != 'done':
            LOGGER.debug('unexpected in p: %s %s %s', child.tag, child.text, child.tail)
            continue
        # spacing = child.tag in SPACING_PROTECTED  # todo: outputformat.startswith('xml')?
        # todo: act on spacing here?
        processed_child = handle_textnode(child, comments_fix=False, deduplicate=dedupbool, preserve_spaces=True,
                                          config=config)
        if processed_child is not None:
            # todo: needing attention!
            if processed_child.tag == 'p':
                LOGGER.debug('extra p within p: %s %s %s', processed_child.tag, processed_child.text,
                             processed_child.tail)
                if processed_element.text:
                    processed_element.text += ' ' + processed_child.text
                else:
                    processed_element.text = processed_child.text
                continue
            # handle formatting
            newsub = Element(child.tag)
            if processed_child.tag in P_FORMATTING:
                # check depth and clean
                if len(processed_child) > 0:
                    for item in processed_child:  # children are lists
                        if text_chars_test(item.text) is True:
                            item.text = ' ' + item.text
                        strip_tags(processed_child, item.tag)
                # correct attributes
                if child.tag == 'hi':
                    newsub.set('rend', child.get('rend'))
                elif child.tag == 'ref':
                    if child.get('target') is not None:
                        newsub.set('target', child.get('target'))
            # handle line breaks
            # elif processed_child.tag == 'lb':
            #    try:
            #        processed_child.tail = process_node(child, dedupbool, config).tail
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
            child.tag = 'done'
    # finish
    if len(processed_element) > 0:
        # clean trailing lb-elements
        if (
                processed_element[-1].tag == 'lb'
                and processed_element[-1].tail is None
        ):
            processed_element[-1].getparent().remove(processed_element[-1])
        return processed_element
    if processed_element.text:
        return processed_element
    LOGGER.debug('discarding p-child: %s', tostring(processed_element))
    return None


def define_cell_type(element):
    '''Determine cell element type and mint new element'''
    # define tag
    cell_element = Element('cell')
    if element.tag == 'th':
        cell_element.set('role', 'head')
    return cell_element


def handle_table(table_elem, potential_tags, dedupbool, config):
    '''Process single table element'''
    newtable = Element('table')
    newrow = Element('row')
    i = 0
    # strip these structural elements
    strip_tags(table_elem, 'thead', 'tbody', 'tfoot')
    # explore sub-elements
    for subelement in table_elem.iter('*'):
        i += 1
        if subelement.tag == 'tr':
            # process existing row
            if len(newrow) > 0:
                newtable.append(newrow)
                newrow = Element('row')
        elif subelement.tag in TABLE_ELEMS:
            newchildelem = define_cell_type(subelement)
            # process
            if len(subelement) == 0:
                processed_cell = process_node(subelement, dedupbool, config)
                if processed_cell is not None:
                    newchildelem.text, newchildelem.tail = processed_cell.text, processed_cell.tail
            else:
                # proceed with iteration, fix for nested elements
                for child in subelement.iter('*'):
                    if child.tag in TABLE_ALL:
                        # todo: define attributes properly
                        if child.tag in TABLE_ELEMS:
                            # subcell_elem = define_cell_type(subelement)
                            child.tag = 'cell'
                        processed_subchild = handle_textnode(child, preserve_spaces=True, comments_fix=True,
                                                             deduplicate=dedupbool, config=config)
                    # todo: lists in table cells
                    else:
                        # subcell_elem = Element(child.tag)
                        processed_subchild = handle_textelem(child, potential_tags.union(['div']), dedupbool, config)
                    # add child element to processed_element
                    if processed_subchild is not None:
                        subchildelem = SubElement(newchildelem, processed_subchild.tag)
                        subchildelem.text, subchildelem.tail = processed_subchild.text, processed_subchild.tail
                    child.tag = 'done'
            # add to tree
            if newchildelem.text or len(newchildelem) > 0:
                newrow.append(newchildelem)
        # beware of nested tables
        elif subelement.tag == 'table' and i > 1:
            break
        # cleanup
        subelement.tag = 'done'
    # end of processing
    if len(newrow) > 0:
        newtable.append(newrow)
    if len(newtable) > 0:
        return newtable
    return None


def handle_image(element):
    '''Process image element'''
    # image source
    processed_element = Element(element.tag)
    if is_image_file(element.get('data-src')):
        processed_element.set('src', element.get('data-src'))
    elif is_image_file(element.get('src')):
        processed_element.set('src', element.get('src'))
    else:
        # take the first corresponding attribute
        for attr in element.attrib:
            if attr.startswith('data-src') and is_image_file(element.get(attr)):
                processed_element.set('src', element.get(attr))
                break
    # additional data
    if element.get('alt') is not None:
        processed_element.set('alt', element.get('alt'))
    if element.get('title') is not None:
        processed_element.set('title', element.get('title'))
    # don't return empty elements or elements without source, just None
    if len(processed_element.attrib) == 0 or not processed_element.get('src'):
        return None
    # post-processing: URLs
    url = processed_element.get('src')
    processed_element.set('src', re.sub(r'^//', 'http://', url))
    return processed_element


def recover_wild_text(tree, result_body, options, potential_tags=TAG_CATALOG):
    '''Look for all previously unconsidered wild elements, including outside of the determined
       frame and throughout the document to recover potentially missing text parts'''
    LOGGER.debug('Recovering wild text elements')
    search_list = ['blockquote', 'code', 'p', 'pre', 'q', 'quote', 'table']
    if options.recall is True:
        potential_tags.update(['div', 'lb'])
        search_list.extend(['div', 'lb'])
    # prune
    search_tree = prune_unwanted_sections(tree, potential_tags, options.recall, options.precision)
    # decide if links are preserved
    if 'ref' not in potential_tags:
        strip_tags(search_tree, 'a', 'ref', 'span')
    else:
        strip_tags(search_tree, 'span')
    result_body.extend(filter(None.__ne__, (handle_textelem(e, potential_tags, options.dedup, options.config)
                              for e in search_tree.iter(search_list))))
    return result_body


def handle_textelem(element, potential_tags, dedupbool, config):
    '''Process text element and determine how to deal with its content'''
    new_element = None
    # bypass: nested elements
    if element.tag == 'list':
        new_element = handle_lists(element, dedupbool, config)
    elif element.tag in CODES_QUOTES:
        new_element = handle_quotes(element, dedupbool, config)
    elif element.tag == 'head':
        new_element = handle_titles(element, dedupbool, config)
    elif element.tag == 'p':
        new_element = handle_paragraphs(element, potential_tags, dedupbool, config)
    elif element.tag == 'lb':
        if text_chars_test(element.tail) is True:
            element = process_node(element, dedupbool, config)
            if element is not None:
                new_element = Element('p')
                new_element.text = element.tail
    elif element.tag in FORMATTING:
        new_element = handle_formatting(element, dedupbool, config)  # process_node(element, dedupbool, config)
    elif element.tag == 'table' and 'table' in potential_tags:
        new_element = handle_table(element, potential_tags, dedupbool, config)
    elif element.tag == 'graphic' and 'graphic' in potential_tags:
        new_element = handle_image(element)
    else:
        # other elements (div, ??, ??)
        new_element = handle_other_elements(element, potential_tags, dedupbool, config)
    return new_element


def prune_unwanted_sections(tree, potential_tags, favor_recall, favor_precision):
    'Rule-based deletion of targeted document sections'
    # prune the rest
    tree = prune_unwanted_nodes(tree, OVERALL_DISCARD_XPATH, with_backup=True)
    tree = prune_unwanted_nodes(tree, PAYWALL_DISCARD_XPATH)
    # decide if images are preserved
    if 'graphic' not in potential_tags:
        tree = prune_unwanted_nodes(tree, DISCARD_IMAGE_ELEMENTS)
    # balance precision/recall
    if favor_recall is False:
        tree = prune_unwanted_nodes(tree, TEASER_DISCARD_XPATH)
        if favor_precision is True:
            tree = prune_unwanted_nodes(tree, PRECISION_DISCARD_XPATH)
    # remove elements by link density
    tree = delete_by_link_density(tree, 'div', backtracking=True, favor_precision=favor_precision)
    # tree = delete_by_link_density(tree, 'list', backtracking=False)
    tree = delete_by_link_density(tree, 'p', backtracking=False, favor_precision=favor_precision)
    # tree = delete_by_link_density(tree, 'head', backtracking=False)
    # also filter fw/head, table and quote elements?
    if favor_precision is True:
        tree = delete_by_link_density(tree, 'head', backtracking=False)  # favor_precision=favor_precision
        tree = delete_by_link_density(tree, 'quote', backtracking=False)  # favor_precision=favor_precision
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
        try:
            subtree = tree.xpath(expr)[0]
        except IndexError:
            continue
        # prune the subtree
        subtree = prune_unwanted_sections(subtree, potential_tags, options.recall, options.precision)
        subtree = delete_by_link_density(subtree, 'list', backtracking=False, favor_precision=options.precision)
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
        if not ptest or len(''.join(ptest)) < options.config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE') * factor:
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
        if set(e.tag for e in subelems) == {'lb'}:
            subelems = [subtree]
        # extract content
        result_body.extend(filter(None.__ne__, (handle_textelem(e, potential_tags, options.dedup, options.config) for e in subelems)))
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
    if len(result_body) == 0 or len(temp_text) < options.config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE'):
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
        processed_element = handle_textnode(elem, comments_fix=True, deduplicate=options.dedup, config=options.config)
        # test length and remove
        if processed_element is not None:  # and processed_element.text not in COMMENTS_BLACKLIST:
            processed_element.attrib.clear()
            # if textfilter(elem) is True:  # ^Pingback
            #    return None
            return processed_element
    return None


def extract_comments(tree, options):
    '''Try and extract comments out of potential sections in the HTML'''
    comments_body = Element('body')
    # define iteration strategy
    potential_tags = set(TAG_CATALOG)  # 'span'
    # potential_tags.add('div') trouble with <div class="comment-author meta">
    for expr in COMMENTS_XPATH:
        # select tree if the expression has been found
        subtree = tree.xpath(expr)
        if not subtree:
            continue
        subtree = subtree[0]
        # prune
        subtree = prune_unwanted_nodes(subtree, COMMENTS_DISCARD_XPATH)
        # todo: unified stripping function, taking include_links into account
        strip_tags(subtree, 'a', 'ref', 'span')
        # extract content
        # for elem in subtree.xpath('.//*'):
        #    processed_elem = process_comments_node(elem, potential_tags)
        #    if processed_elem is not None:
        #        comments_body.append(processed_elem)
        # processed_elems = (process_comments_node(elem, potential_tags, dedupbool, config) for elem in
        #                    subtree.xpath('.//*'))
        comments_body.extend(filter(None.__ne__, (process_comments_node(e, potential_tags, options) for e in subtree.xpath('.//*'))))
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            subtree.getparent().remove(subtree)
            break
    # lengths
    temp_comments = ' '.join(comments_body.itertext()).strip()
    return comments_body, temp_comments, len(temp_comments), tree


def compare_extraction(tree, backup_tree, url, body, text, len_text, target_language, options):
    '''Decide whether to choose own or external extraction
       based on a series of heuristics'''
    min_target_length = options.config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE')
    # bypass for recall
    if options.recall is True and len_text > min_target_length * 10:
        return body, text, len_text
    algo_flag, jt_result = False, False
    # prior cleaning
    backup_tree = prune_unwanted_nodes(backup_tree, PAYWALL_DISCARD_XPATH)
    if options.precision is True:
        backup_tree = prune_unwanted_nodes(backup_tree, OVERALL_DISCARD_XPATH)
    # try with readability
    temppost_algo = try_readability(backup_tree)
    algo_text = trim(temppost_algo.text_content())
    len_algo = len(algo_text)
    # compare
    LOGGER.debug('extracted length: %s (algorithm) %s (extraction)', len_algo, len_text)
    # conditions to use alternative algorithms
    if len_algo in (0, len_text):
        algo_flag = False
    elif len_text == 0 and len_algo > 0:
        algo_flag = True
    elif len_text > 2 * len_algo:
        algo_flag = False
    elif len_algo > 2 * len_text:
        algo_flag = True
    # borderline cases
    else:
        if not body.xpath('.//p//text()') and len_algo > min_target_length * 2:
            algo_flag = True
        elif len(body.findall('.//table')) > len(body.findall('.//p')) and len_algo > min_target_length * 2:
            algo_flag = True
        else:
            LOGGER.debug('extraction values: %s %s for %s', len_text, len_algo, url)
            algo_flag = False
    # apply decision
    if algo_flag is True:
        body, text, len_text = temppost_algo, algo_text, len_algo
        LOGGER.info('using generic algorithm: %s', url)
    else:
        LOGGER.info('using custom extraction: %s', url)
    # override faulty extraction: try with justext
    if body.xpath(SANITIZED_XPATH) or len_text < min_target_length:  # body.find(...)
    # or favor_recall is True ?
        # tree = prune_unwanted_sections(tree, {}, options.recall, options.precision)
        body2, text2, len_text2, jt_result = justext_rescue(tree, url, target_language, body, 0, '')
        if jt_result is True:  # and not len_text > 2*len_text2:
            LOGGER.debug('using justext, length: %s', len_text2)
            body, text, len_text = body2, text2, len_text2
    # post-processing: remove unwanted sections
    if algo_flag is True and jt_result is False:
        body, text, len_text = sanitize_tree(body, options)
    return body, text, len_text


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
    # basic tree cleaning
    for elem in tree.xpath('.//aside|.//footer|.//script|.//style'):
        elem.getparent().remove(elem)
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
        The extracted text in the form of a string.

    """
    tree = load_html(content)
    return ' '.join(tree.text_content().split()).strip()


def determine_returnstring(document, output_format, include_formatting, tei_validation):
    '''Convert XML tree to chosen format, clean the result and output it as a string'''
    # XML (TEI) steps
    if 'xml' in output_format:
        # last cleaning
        for element in document.body.iter('*'):
            if element.tag != 'graphic' and len(element) == 0 and not element.text and not element.tail:
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
        # build output trees
        if output_format == 'xml':
            output = build_xml_output(document)
        elif output_format == 'xmltei':
            output = build_tei_output(document)
        # can be improved
        returnstring = control_xml_output(output, output_format, tei_validation, document)
    # CSV
    elif output_format == 'csv':
        posttext = xmltotxt(document.body, include_formatting)
        if document.commentsbody is not None:
            commentstext = xmltotxt(document.commentsbody, include_formatting)
        else:
            commentstext = ''
        returnstring = txttocsv(posttext, commentstext, document)
    # JSON
    elif output_format == 'json':
        returnstring = build_json_output(document)
    # TXT
    else:
        returnstring = xmltotxt(document.body, include_formatting)
        if document.commentsbody is not None:
            returnstring += '\n' + xmltotxt(document.commentsbody, include_formatting)
            returnstring = returnstring.strip()
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
                    as_dict=True, config=DEFAULT_CONFIG):
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
        config: Directly provide a configparser configuration.

    Returns:
        A Python dict() containing all the extracted information or None.

    Raises:
        ValueError: Extraction problem.
    """
    # init
    if url_blacklist is None:
        url_blacklist = set()

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

        # quick and dirty HTML lang check
        if target_language is not None and (no_fallback is True or LANGID_FLAG is False):
            if check_html_lang(tree, target_language) is False:
                LOGGER.error('wrong HTML meta language for URL %s', url)
                raise ValueError

        # extract metadata if necessary
        if output_format != 'txt':
            document = extract_metadata(tree, url, date_extraction_params, no_fallback, author_blacklist)
            # cut short if extracted URL in blacklist
            if document.url in url_blacklist:
                LOGGER.info('blacklisted URL: %s', url)
                raise ValueError
            # cut short if core elements are missing
            if only_with_metadata is True and any(
                    x is None for x in
                    [document.date, document.title, document.url]
            ):
                LOGGER.error('no metadata for URL %s', url)
                raise ValueError
        else:
            document = Document()

        # regroup extraction options
        options = Extractor(config, no_fallback, favor_precision, favor_recall,
                            include_comments, include_formatting, include_links,
                            include_images, include_tables, deduplicate)

        # backup (or not) for further processing
        tree_backup_1 = deepcopy(tree) if no_fallback is False else None
        tree_backup_2 = deepcopy(tree)

        # clean + use LXML cleaner
        cleaned_tree = tree_cleaning(tree, options)
        cleaned_tree_backup = deepcopy(cleaned_tree)

        # convert tags, the rest does not work without conversion
        cleaned_tree = convert_tags(cleaned_tree, options)

        # comments first, then remove
        if include_comments is True:
            commentsbody, temp_comments, len_comments, cleaned_tree = extract_comments(cleaned_tree, options)
        else:
            commentsbody, temp_comments, len_comments = None, '', 0
        if favor_precision is True:
            cleaned_tree = prune_unwanted_nodes(cleaned_tree, REMOVE_COMMENTS_XPATH)

        # extract content
        postbody, temp_text, len_text = extract_content(cleaned_tree, options)

        # compare if necessary
        if no_fallback is False:
            postbody, temp_text, len_text = compare_extraction(cleaned_tree_backup, tree_backup_1, url, postbody, temp_text, len_text, target_language, options)
        # add baseline as additional fallback
        # rescue: try to use original/dirty tree # and favor_precision is False=?
        if len_text < config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE'):
            postbody, temp_text, len_text = baseline(tree_backup_2)
            LOGGER.debug('non-clean extracted length: %s (extraction)', len_text)

        # tree size sanity check
        if max_tree_size is not None:
            # strip tags
            if len(postbody) > max_tree_size:
                LOGGER.warning('output tree too long: %s', len(postbody))
                strip_tags(postbody, 'hi')
            # still too long, raise an error
            if len(postbody) > max_tree_size:
                LOGGER.error('output tree too long: %s, discarding file', len(postbody))
                raise ValueError
        # size checks
        if len_comments < config.getint('DEFAULT', 'MIN_EXTRACTED_COMM_SIZE'):
            LOGGER.info('not enough comments %s', url)
        if len_text < config.getint('DEFAULT', 'MIN_OUTPUT_SIZE') and len_comments < config.getint('DEFAULT',
                                                                                                   'MIN_OUTPUT_COMM_SIZE'):
            LOGGER.info('text and comments not long enough: %s %s', len_text, len_comments)
            raise ValueError

        # check duplicates at body level
        if deduplicate is True and duplicate_test(postbody, config) is True:
            LOGGER.error('duplicate document for URL %s', url)
            raise ValueError

        # sanity check on language
        if target_language is not None:
            is_not_target_lang, document = language_filter(temp_text, temp_comments, target_language, document)
            if is_not_target_lang is True:
                LOGGER.error('wrong language for URL %s', url)
                raise ValueError

    except ValueError:
        LOGGER.info('discarding data for url: %s', url)  # document.url , record_id
        return None

    # special case: python variables
    if output_format == 'python':
        document.text = xmltotxt(postbody, include_formatting)
        if include_comments is True:
            document.comments = xmltotxt(commentsbody, include_formatting)
    else:
        document.raw_text, document.body, document.commentsbody = temp_text, postbody, commentsbody
    if as_dict is True:
        document = {slot: getattr(document, slot, None) for slot in document.__slots__}
    return document


def timeout_handler(signum, frame):
    '''Raise a timeout exception to handle rare malicious files'''
    raise RuntimeError('unusual file processing time, aborting')


def extract(filecontent, url=None, record_id=None, no_fallback=False,
            favor_precision=False, favor_recall=False,
            include_comments=True, output_format='txt',
            tei_validation=False, target_language=None,
            include_tables=True, include_images=False, include_formatting=False,
            include_links=False, deduplicate=False,
            date_extraction_params=None,
            only_with_metadata=False, with_metadata=False,
            max_tree_size=None, url_blacklist=None, author_blacklist=None,
            settingsfile=None, config=DEFAULT_CONFIG,
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
        config: Directly provide a configparser configuration.

    Returns:
        A string in the desired format or None.

    """
    # older, deprecated functions
    if kwargs:
        # output formats
        if any([
            'csv_output' in kwargs, 'json_output' in kwargs,
            'tei_output' in kwargs, 'xml_output' in kwargs
            ]):
            raise NameError(
                'Deprecated argument: use output_format instead, e.g. output_format="xml"'
                )
        # todo: add with_metadata later

    # configuration init
    config = use_config(settingsfile, config)

    # put timeout signal in place
    if HAS_SIGNAL is True:
        timeout = config.getint('DEFAULT', 'EXTRACTION_TIMEOUT')
        if timeout > 0:
            signal(SIGALRM, timeout_handler)
            alarm(timeout)

    # extraction
    try:
        document = bare_extraction(
            filecontent, url=url, no_fallback=no_fallback,
            favor_precision=favor_precision, favor_recall=favor_recall,
            include_comments=include_comments, output_format=output_format,
            target_language=target_language, include_tables=include_tables,
            include_images=include_images,
            include_formatting=include_formatting, include_links=include_links,
            deduplicate=deduplicate,
            date_extraction_params=date_extraction_params,
            only_with_metadata=only_with_metadata, with_metadata=with_metadata,
            max_tree_size=max_tree_size, url_blacklist=url_blacklist,
            author_blacklist=author_blacklist,
            as_dict=False, config=config,
        )
    except RuntimeError:
        LOGGER.error('Processing timeout for %s', url)
        document = None

    # deactivate alarm signal
    if HAS_SIGNAL is True and timeout > 0:
        alarm(0)

    # post-processing
    if document is None:
        return None
    if output_format != 'txt':
        # add record ID to metadata
        document.id = record_id
        # calculate fingerprint
        document.fingerprint = content_fingerprint(document.raw_text)

    # return
    return determine_returnstring(document, output_format, include_formatting, tei_validation)


# for legacy and backwards compatibility
def process_record(filecontent, url=None, record_id=None, no_fallback=False,
                   include_comments=True, target_language=None,
                   include_tables=True):
    "Legacy extraction function, now deprecated."
    # deprecation warning
    warnings.warn(
        "process_record() is deprecated, use extract() instead",
        DeprecationWarning
    )
    return extract(filecontent, url=url, record_id=record_id, no_fallback=no_fallback,
                   include_comments=include_comments, target_language=target_language,
                   include_tables=include_tables)
