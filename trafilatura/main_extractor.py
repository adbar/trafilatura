# pylint:disable-msg=E0611
"""
Functions related to the main Trafilatura extractor.
"""

import logging
import re  # import regex as re

from copy import deepcopy
from typing import Any, Optional, Tuple, Set, Union

from lxml.etree import _Element, Element, SubElement, strip_elements, strip_tags, tostring
from lxml.html import HtmlElement

# own
from .htmlprocessing import (delete_by_link_density, handle_textnode,
                             link_density_test_tables, process_node,
                             prune_unwanted_nodes)
from .settings import TAG_CATALOG, Extractor
from .utils import FORMATTING_PROTECTED, is_image_file, text_chars_test, trim
from .xml import delete_element
from .xpaths import (BODY_XPATH, COMMENTS_DISCARD_XPATH, COMMENTS_XPATH,
                     DISCARD_IMAGE_ELEMENTS, OVERALL_DISCARD_XPATH,
                     PRECISION_DISCARD_XPATH, TEASER_DISCARD_XPATH)


LOGGER = logging.getLogger(__name__)


P_FORMATTING = {'hi', 'ref'}
TABLE_ELEMS = {'td', 'th'}
TABLE_ALL = {'td', 'th', 'hi'}
FORMATTING = {'hi', 'ref', 'span'}
CODES_QUOTES = {'code', 'quote'}
NOT_AT_THE_END = {'head', 'ref'}


def _log_event(msg: str, tag: Any, text: Optional[Union[bytes, str]]) -> None:
    "Format extraction event for debugging purposes."
    LOGGER.debug("%s: %s %s", msg, tag, trim(text or "") or "None")


def handle_titles(element: _Element, options: Extractor) -> Optional[_Element]:
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


def handle_formatting(element: _Element, options: Extractor) -> Optional[_Element]:
    '''Process formatting elements (b, i, etc. converted to hi) found
       outside of paragraphs'''
    formatting = process_node(element, options)
    if formatting is None:  #  and len(element) == 0
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


def add_sub_element(new_child_elem: _Element, subelem: _Element, processed_subchild: _Element) -> None:
    "Add a sub-element to an existing child element."
    sub_child_elem = SubElement(new_child_elem, processed_subchild.tag)
    sub_child_elem.text, sub_child_elem.tail = processed_subchild.text, processed_subchild.tail
    for attr in subelem.attrib:
        sub_child_elem.set(attr, subelem.attrib[attr])


def process_nested_elements(child: _Element, new_child_elem: _Element, options: Extractor) -> None:
    "Iterate through an element child and rewire its descendants."
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


def update_elem_rendition(elem: _Element, new_elem: _Element) -> None:
    "Copy the rend attribute from an existing element to a new one."
    if rend_attr := elem.get("rend"):
        new_elem.set("rend", rend_attr)


def is_text_element(elem: _Element) -> bool:
    "Find if the element contains text."
    return elem is not None and text_chars_test(''.join(elem.itertext())) is True


def define_newelem(processed_elem: _Element, orig_elem: _Element) -> None:
    "Create a new sub-element if necessary."
    if processed_elem is not None:
        childelem = SubElement(orig_elem, processed_elem.tag)
        childelem.text, childelem.tail = processed_elem.text, processed_elem.tail


def handle_lists(element: _Element, options: Extractor) -> Optional[_Element]:
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
                new_child_elem.text = processed_child.text or ""
                if processed_child.tail and processed_child.tail.strip():
                    new_child_elem.text += " " + processed_child.tail
                processed_element.append(new_child_elem)
        else:
            process_nested_elements(child, new_child_elem, options)
            if child.tail is not None and child.tail.strip():
                new_child_elem_children = [el for el in new_child_elem if el.tag != "done"]
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


def is_code_block_element(element: _Element) -> bool:
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


def handle_code_blocks(element: _Element) -> _Element:
    "Turn element into a properly tagged code block."
    processed_element = deepcopy(element)
    for child in element.iter("*"):
        child.tag = "done"
    processed_element.tag = "code"
    return processed_element


def handle_quotes(element: _Element, options: Extractor) -> Optional[_Element]:
    "Process quotes elements."
    if is_code_block_element(element):
        return handle_code_blocks(element)

    processed_element = Element(element.tag)
    for child in element.iter("*"):
        processed_child = process_node(child, options)  # handle_textnode(child, comments_fix=True)
        if processed_child is not None:
            define_newelem(processed_child, processed_element)
        child.tag = "done"
    if is_text_element(processed_element):
        # avoid double/nested tags
        strip_tags(processed_element, "quote")
        return processed_element
    return None


def handle_other_elements(element: _Element, potential_tags: Set[str], options: Extractor) -> Optional[_Element]:
    "Handle diverse or unknown elements in the scope of relevant tags."
    # handle w3schools code
    if element.tag == "div" and "w3-code" in element.get("class", ""):
        return handle_code_blocks(element)

    # delete unwanted
    if element.tag not in potential_tags:
        if element.tag != "done":
            _log_event("discarding element", element.tag, element.text)
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

    return None


def handle_paragraphs(element: _Element, potential_tags: Set[str], options: Extractor) -> Optional[_Element]:
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
            _log_event("unexpected in p", child.tag, child.text)
            continue
        # spacing = child.tag in SPACING_PROTECTED  # todo: outputformat.startswith('xml')?
        # todo: act on spacing here?
        processed_child = handle_textnode(child, options, comments_fix=False, preserve_spaces=True)
        if processed_child is not None:
            # todo: needing attention!
            if processed_child.tag == "p":
                _log_event("extra in p", "p", processed_child.text)
                if processed_element.text:
                    processed_element.text += " " + (processed_child.text or "")
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
                            item.text = " " + item.text  # type: ignore[operator]
                        strip_tags(processed_child, item.tag)
                # correct attributes
                if child.tag == "hi":
                    newsub.set("rend", child.get("rend", ""))
                elif child.tag == "ref":
                    if child.get("target") is not None:
                        newsub.set("target", child.get("target", ""))
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

            if processed_child.tag == 'graphic':
                image_elem = handle_image(processed_child)
                if image_elem is not None:
                    newsub = image_elem
            processed_element.append(newsub)
        child.tag = "done"
    # finish
    if len(processed_element) > 0:
        last_elem = processed_element[-1]
        # clean trailing lb-elements
        if last_elem.tag == "lb" and last_elem.tail is None:
            delete_element(last_elem)
        return processed_element
    if processed_element.text:
        return processed_element
    _log_event("discarding element:", "p", tostring(processed_element))
    return None


def define_cell_type(is_header: bool) -> _Element:
    "Determine cell element type and mint new element."
    # define tag
    cell_element = Element("cell")
    if is_header:
        cell_element.set("role", "head")
    return cell_element


def handle_table(table_elem: _Element, potential_tags: Set[str], options: Extractor) -> Optional[_Element]:
    "Process single table element."
    newtable = Element("table")

    # strip these structural elements
    strip_tags(table_elem, "thead", "tbody", "tfoot")

    # calculate maximum number of columns per row, includin colspan
    max_cols = 0
    for tr in table_elem.iter('tr'):
        max_cols = max(max_cols, sum(int(td.get("colspan", 1)) for td in tr.iter(TABLE_ELEMS)))

    # explore sub-elements
    seen_header_row = False
    seen_header = False
    span_attr = str(max_cols) if max_cols > 1 else ""
    newrow = Element("row")
    if span_attr:
        newrow.set("span", span_attr)

    for subelement in table_elem.iterdescendants():
        if subelement.tag == "tr":
            # process existing row
            if len(newrow) > 0:
                newtable.append(newrow)
                newrow = Element("row")
                if span_attr:
                    newrow.set("span", span_attr)
                seen_header_row = seen_header_row or seen_header
        elif subelement.tag in TABLE_ELEMS:
            is_header = subelement.tag == "th" and not seen_header_row
            seen_header = seen_header or is_header
            new_child_elem = define_cell_type(is_header)
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
                            # subcell_elem = define_cell_type(is_header)
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
                    if processed_subchild is not None:
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

    # clean up row attributes
    newrow.attrib.pop("span", None)

    # end of processing
    if len(newrow) > 0:
        newtable.append(newrow)
    if len(newtable) > 0:
        return newtable
    return None


def handle_image(element: Optional[_Element]) -> Optional[_Element]:
    "Process image elements and their relevant attributes."
    if element is None:
        return None

    processed_element = Element(element.tag)

    for attr in ("data-src", "src"):
        src = element.get(attr, "")
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
    if alt_attr := element.get("alt"):
        processed_element.set("alt", alt_attr)
    if title_attr := element.get("title"):
        processed_element.set("title", title_attr)

    # don't return empty elements or elements without source, just None
    if not processed_element.attrib or not processed_element.get("src"):
        return None

    # post-processing: URLs
    src_attr = processed_element.get("src", "")
    if not src_attr.startswith("http"):
        processed_element.set("src", re.sub(r"^//", "http://", src_attr))

    return processed_element


def handle_textelem(element: _Element, potential_tags: Set[str], options: Extractor) -> Optional[_Element]:
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
            this_element = process_node(element, options)
            if this_element is not None:
                new_element = Element('p')
                new_element.text = this_element.tail
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


def recover_wild_text(tree: HtmlElement, result_body: _Element, options: Extractor, potential_tags: Any = TAG_CATALOG) -> _Element:
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
                       for e in subelems)))  # type: ignore[arg-type]
    return result_body


def prune_unwanted_sections(tree: HtmlElement, potential_tags: Set[str], options: Extractor) -> HtmlElement:
    'Rule-based deletion of targeted document sections'
    favor_precision = options.focus == "precision"
    # prune the rest
    tree = prune_unwanted_nodes(tree, OVERALL_DISCARD_XPATH, with_backup=True)
    # decide if images are preserved
    if 'graphic' not in potential_tags:
        tree = prune_unwanted_nodes(tree, DISCARD_IMAGE_ELEMENTS)
    # balance precision/recall
    if options.focus != "recall":
        tree = prune_unwanted_nodes(tree, TEASER_DISCARD_XPATH)
        if favor_precision:
            tree = prune_unwanted_nodes(tree, PRECISION_DISCARD_XPATH)
    # remove elements by link density, several passes
    for _ in range(2):
        tree = delete_by_link_density(tree, 'div', backtracking=True, favor_precision=favor_precision)
        tree = delete_by_link_density(tree, 'list', backtracking=False, favor_precision=favor_precision)
        tree = delete_by_link_density(tree, 'p', backtracking=False, favor_precision=favor_precision)
    # tables
    if 'table' in potential_tags or favor_precision:
        # tree = delete_by_link_density(tree, 'table', backtracking=False, favor_precision=favor_precision)
        for elem in tree.iter('table'):
            if link_density_test_tables(elem) is True:
                delete_element(elem, keep_tail=False)
    # also filter fw/head, table and quote elements?
    if favor_precision:
        # delete trailing titles
        while len(tree) > 0 and (tree[-1].tag == 'head'):
            delete_element(tree[-1], keep_tail=False)
        tree = delete_by_link_density(tree, 'head', backtracking=False, favor_precision=True)
        tree = delete_by_link_density(tree, 'quote', backtracking=False, favor_precision=True)
    return tree


def _extract(tree: HtmlElement, options: Extractor) -> Tuple[_Element, str, Set[str]]:
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
        # skip if empty tree
        if len(subtree) == 0:
            continue
        # no paragraphs containing text, or not enough
        ptest = subtree.xpath('//p//text()')
        if options.focus == "precision":
            factor = 1
        else:
            factor = 3
        if not ptest or len(''.join(ptest)) < options.min_extracted_size * factor:  # type: ignore[attr-defined]
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
            delete_element(result_body[-1], keep_tail=False)
        # exit the loop if the result has children
        if len(result_body) > 1:
            LOGGER.debug(trim(str(expr)))
            break
    temp_text = ' '.join(result_body.itertext()).strip()
    return result_body, temp_text, potential_tags


def extract_content(cleaned_tree: HtmlElement, options: Extractor) -> Tuple[_Element, str, int]:
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
    if len(result_body) == 0 or len(temp_text) < options.min_extracted_size:  # type: ignore[attr-defined]
        result_body = recover_wild_text(backup_tree, result_body, options, potential_tags)
        temp_text = ' '.join(result_body.itertext()).strip()
    # filter output
    strip_elements(result_body, 'done')
    strip_tags(result_body, 'div')
    # return
    return result_body, temp_text, len(temp_text)


def process_comments_node(elem: _Element, potential_tags: Set[str], options: Extractor) -> Optional[_Element]:
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


def extract_comments(tree: HtmlElement, options: Extractor) -> Tuple[_Element, str, int, HtmlElement]:
    "Try to extract comments out of potential sections in the HTML."
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
        comments_body.extend(filter(lambda x: x is not None, (process_comments_node(e, potential_tags, options) for e in subtree.xpath(".//*"))))  # type: ignore[arg-type]
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            delete_element(subtree, keep_tail=False)
            break
    # lengths
    temp_comments = " ".join(comments_body.itertext()).strip()
    return comments_body, temp_comments, len(temp_comments), tree
