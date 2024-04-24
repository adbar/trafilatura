# pylint:disable-msg=E0611
"""
Functions related to the main Trafilatura extractor.
"""

import logging
import re  # import regex as re

from copy import deepcopy

from lxml.etree import Element, SubElement, strip_elements, strip_tags, tostring

# own
from .filters import text_chars_test
from .htmlprocessing import (delete_by_link_density, handle_textnode,
                             link_density_test_tables, process_node,
                             prune_unwanted_nodes)
from .settings import TAG_CATALOG
from .utils import FORMATTING_PROTECTED, is_image_file
from .xpaths import (BODY_XPATH, COMMENTS_DISCARD_XPATH, COMMENTS_XPATH,
                     DISCARD_IMAGE_ELEMENTS, OVERALL_DISCARD_XPATH,
                     PAYWALL_DISCARD_XPATH, PRECISION_DISCARD_XPATH,
                     TEASER_DISCARD_XPATH)


LOGGER = logging.getLogger(__name__)


P_FORMATTING = {'hi', 'ref'}
TABLE_ELEMS = {'td', 'th'}
TABLE_ALL = {'td', 'th', 'hi'}
FORMATTING = {'hi', 'ref', 'span'}
CODES_QUOTES = {'code', 'quote'}
NOT_AT_THE_END = {'head', 'ref'}


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
                    elif child.tag == "list" and options.focus == "recall":
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
    if options.focus == "recall":
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
    favor_precision = options.focus == "precision"
    # prune the rest
    tree = prune_unwanted_nodes(tree, OVERALL_DISCARD_XPATH, with_backup=True)
    tree = prune_unwanted_nodes(tree, PAYWALL_DISCARD_XPATH)
    # decide if images are preserved
    if 'graphic' not in potential_tags:
        tree = prune_unwanted_nodes(tree, DISCARD_IMAGE_ELEMENTS)
    # balance precision/recall
    if options.focus != "recall":
        tree = prune_unwanted_nodes(tree, TEASER_DISCARD_XPATH)
        if favor_precision:
            tree = prune_unwanted_nodes(tree, PRECISION_DISCARD_XPATH)
    # remove elements by link density
    tree = delete_by_link_density(tree, 'div', backtracking=True, favor_precision=favor_precision)
    tree = delete_by_link_density(tree, 'list', backtracking=False, favor_precision=favor_precision)
    tree = delete_by_link_density(tree, 'p', backtracking=False, favor_precision=favor_precision)
    # also filter fw/head, table and quote elements?
    if favor_precision:
        # delete trailing titles
        while len(tree) > 0 and (tree[-1].tag == 'head'):
            tree[-1].getparent().remove(tree[-1])
        tree = delete_by_link_density(tree, 'head', backtracking=False)  # favor_precision=favor_precision
        tree = delete_by_link_density(tree, 'quote', backtracking=False)  # favor_precision=favor_precision
    return tree


def _extract(tree, options):
    # init
    potential_tags = set(TAG_CATALOG)
    if options.tables is True:
        potential_tags.update(['table', 'td', 'th', 'tr'])
    if options.images is True:
        potential_tags.add('graphic')
    if options.links is True:
        potential_tags.add('ref')
    result_body = Element('body')
    # iterate
    for expr in BODY_XPATH:
        # select tree if the expression has been found
        subtree = next((s for s in expr(tree) if s is not None), None)
        if subtree is None:
            continue
        # prune the subtree
        subtree = prune_unwanted_sections(subtree, potential_tags, options)
        # second pass?
        # subtree = delete_by_link_density(subtree, 'list', backtracking=False, favor_precision=options.focus == "precision")
        if 'table' in potential_tags or options.focus == "precision":
            for elem in subtree.iter('table'):
                if link_density_test_tables(elem) is True:
                    elem.getparent().remove(elem)
        # skip if empty tree
        if len(subtree) == 0:
            continue
        # no paragraphs containing text, or not enough
        ptest = subtree.xpath('//p//text()')
        if options.focus == "precision":
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
    return result_body, temp_text, potential_tags


def extract_content(cleaned_tree, options):
    '''Find the main content of a page using a set of XPath expressions,
       then extract relevant elements, strip them of unwanted subparts and
       convert them'''
    # backup
    backup_tree = deepcopy(cleaned_tree)

    result_body, temp_text, potential_tags = _extract(cleaned_tree, options)
    #if len(result_body) == 0:
    #    result_body, temp_text, potential_tags = _extract(tree_backup, options)

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
