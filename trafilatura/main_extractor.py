# pylint:disable-msg=E0611
"""
Functions related to the main Trafilatura extractor.
"""

import logging
import re  # import regex as re
from copy import deepcopy
from typing import Any
from urllib.parse import urljoin

from lxml.etree import Element, SubElement, _Element, strip_elements, strip_tags, tostring
from lxml.html import HtmlElement

# own
from .htmlprocessing import (
    delete_by_link_density,
    handle_textnode,
    link_density_test_tables,
    process_node,
    prune_unwanted_nodes,
)
from .settings import DEDUPE_SCAN_CAP, INLINE_CARRIED, MIN_DUPLICATE_LENGTH, TAG_CATALOG, Extractor
from .utils import FORMATTING_PROTECTED, is_image_file, text_chars_test, trim
from .xml import delete_element
from .xpaths import (
    BODY_XPATH,
    COMMENTS_DISCARD_XPATH,
    COMMENTS_XPATH,
    DISCARD_IMAGE_ELEMENTS,
    OVERALL_DISCARD_XPATH,
    PRECISION_DISCARD_XPATH,
    TEASER_DISCARD_XPATH,
)

LOGGER = logging.getLogger(__name__)


P_FORMATTING = {"hi", "ref"}
TABLE_ELEMS = {"td", "th"}
_INLINE_WRAP_TAGS = P_FORMATTING | {"del"}
FORMATTING = P_FORMATTING | {"del", "span"}
# meaningful internal attributes to carry onto a rewired sub-element (drop stray class/style/width/etc.)
KEEP_ATTRS = {"rend", "role", "target", "src", "alt", "title"}
CODES_QUOTES = {"code", "quote"}
NOT_AT_THE_END = {"head", "ref"}
# tags allowed inside a blockquote paragraph
_QUOTE_TAGS = set(TAG_CATALOG) | {"ref", "graphic"}


def _elem_text(element: _Element) -> str:
    """Text rendering for the recovery/adjacent dedup checks here: plain concatenation, so
    inline-tag boundaries stay joined ("Hyper<b>link</b>ed" -> "Hyperlinked"). Both sides of
    these checks must use it, or invented spaces defeat the comparison. (deduplication.py's
    duplicate_test uses its own " "-joined rendering for the separate LRU dedup.)
    Not text_content(): callers pass lxml.etree elements, which lack that lxml.html method."""
    return trim("".join(element.itertext()))


def _wraps_inline(element: _Element) -> bool:
    "A formatting element whose children must be carried verbatim: ref, or hi/del wrapping inline content."
    return len(element) > 0 and (element.tag == "ref" or any(c.tag in INLINE_CARRIED for c in element))


def _log_event(msg: str, tag: Any, text: bytes | str | None) -> None:
    "Format extraction event for debugging purposes."
    LOGGER.debug("%s: %s %s", msg, tag, trim(text or "") or "None")


def handle_titles(element: _Element, options: Extractor) -> _Element | None:
    """Process head elements (titles)"""
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
            child.tag = "done"
    if title is not None and text_chars_test("".join(title.itertext())) is True:
        return title
    return None


def handle_formatting(element: _Element, options: Extractor) -> _Element | None:
    """Process formatting elements (b, i, etc. converted to hi) found
    outside of paragraphs"""
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
        processed_element = Element("p")
        processed_element.insert(0, formatting)
    else:
        processed_element = formatting
    return processed_element


def process_nested_elements(child: _Element, new_child_elem: _Element, options: Extractor) -> None:
    "Iterate through an element child and rewire its descendants."
    new_child_elem.text = child.text
    for subelem in child.iterdescendants("*"):
        if subelem.tag == "list":
            processed_subchild = handle_lists(subelem, options)
            if processed_subchild is not None:
                new_child_elem.append(processed_subchild)
        elif subelem.tag in INLINE_CARRIED:
            define_newelem(subelem, new_child_elem, keep_children=True)
        else:
            processed_subchild = handle_textnode(subelem, options, comments_fix=False)
            if processed_subchild is not None:
                define_newelem(processed_subchild, new_child_elem)
        subelem.tag = "done"


def update_elem_rendition(elem: _Element, new_elem: _Element) -> None:
    "Copy the rend attribute from an existing element to a new one."
    if rend_attr := elem.get("rend"):
        new_elem.set("rend", rend_attr)


def is_text_element(elem: _Element) -> bool:
    "Find if the element contains text."
    return elem is not None and text_chars_test("".join(elem.itertext())) is True


def define_newelem(processed_elem: _Element | None, orig_elem: _Element, keep_children: bool = False) -> None:
    "Create a new sub-element, optionally carrying its inline children (INLINE_CARRIED)."
    if processed_elem is not None:
        childelem = SubElement(orig_elem, processed_elem.tag)
        childelem.text, childelem.tail = processed_elem.text, processed_elem.tail
        for key, value in processed_elem.attrib.items():
            if key in KEEP_ATTRS:
                childelem.set(key, value)
        if keep_children:
            for sub in processed_elem:
                if sub.tag in INLINE_CARRIED or sub.tag == "lb":
                    define_newelem(sub, childelem, keep_children=True)
                    # mark only the carried subtree done; non-carried siblings (e.g. nested <p>) stay processable
                    for carried in sub.iter("*"):
                        carried.tag = "done"


def handle_lists(element: _Element, options: Extractor) -> _Element | None:
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


_INLINE_CODE_PARENTS = frozenset(("p", "li", "td", "th", "dd", "dt"))


def is_code_block_element(element: _Element) -> bool:
    "Check if it is a code element according to common structural markers."
    # inline <code> inside paragraph-like parents is not a block element (#849)
    if element.tag == "code":
        parent = element.getparent()
        if parent is not None and parent.tag in _INLINE_CODE_PARENTS:
            return False
    # pip
    if element.get("lang") or element.tag == "code":
        return True
    # GitHub
    parent = element.getparent()
    if parent is not None and "highlight" in parent.get("class", ""):
        return True
    # highlightjs
    code = element.find("code")
    if code is not None and len(element) == 1 and not (element.text or "").strip() and not (code.tail or "").strip():
        return True
    return False


def handle_code_blocks(element: _Element) -> _Element:
    "Turn element into a properly tagged code block."
    processed_element = deepcopy(element)
    for child in element.iter("*"):
        child.tag = "done"
    processed_element.tag = "code"
    return processed_element


def handle_quotes(element: _Element, options: Extractor) -> _Element | None:
    "Process quotes elements."
    if is_code_block_element(element):
        return handle_code_blocks(element)

    processed_element = Element(element.tag)
    processed_element.text = element.text
    for child in element.iterdescendants():
        if child.tag == "graphic":
            processed_child = handle_image(child, options)
            define_newelem(processed_child, processed_element)
        elif child.tag == "p" and len(child) > 0:
            processed_child = handle_paragraphs(child, _QUOTE_TAGS, options)
            if processed_child is not None:
                processed_element.append(processed_child)
        elif child.tag in INLINE_CARRIED:
            define_newelem(child, processed_element, keep_children=True)
        else:
            processed_child = process_node(child, options)
            define_newelem(processed_child, processed_element)
        child.tag = "done"
    if is_text_element(processed_element):
        # avoid double/nested tags
        strip_tags(processed_element, "quote")
        return processed_element
    return None


def handle_other_elements(element: _Element, potential_tags: set[str], options: Extractor) -> _Element | None:
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


def handle_paragraphs(element: _Element, potential_tags: set[str], options: Extractor) -> _Element | None:
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
                # carry inline children verbatim (ref/hi/del wrapping formatting)
                if _wraps_inline(processed_child):
                    define_newelem(processed_child, processed_element, keep_children=True)
                    child.tag = "done"
                    continue
                # check depth and clean
                if len(processed_child) > 0:
                    for item in processed_child:  # children are lists
                        if item.tag == "lb" and item.tail:
                            item.tail = " " + item.tail.lstrip()
                        elif item.text is not None and text_chars_test(item.text):
                            item.text = " " + item.text
                        strip_tags(processed_child, item.tag)  # type: ignore[arg-type]
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

            if processed_child.tag == "graphic":
                image_elem = handle_image(processed_child, options)
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
    cell_element = Element("cell")
    if is_header:
        cell_element.set("role", "head")
    return cell_element


_MAX_SPAN = 100


def _span(cell: _Element, attr: str) -> int:
    "Parse a cell's col/rowspan, defaulting to 1, capped at _MAX_SPAN."
    # isdecimal, not isdigit: int() rejects the superscripts isdigit() admits
    value = cell.get(attr, "1")
    return min(int(value), _MAX_SPAN) if value.isdecimal() else 1


def _row_has_content(row: _Element) -> bool:
    "Whether any cell in a row carries text or children."
    return any(cell.text or len(cell) > 0 for cell in row)


def _flush_rowspan_phantoms(rowspan_map: dict[int, int], newrow: _Element) -> None:
    "Insert empty placeholder cells for rowspan-occupied columns at the current row position."
    while (col := len(newrow)) in rowspan_map:
        newrow.append(define_cell_type(False))
        rowspan_map[col] -= 1
        if rowspan_map[col] == 0:
            del rowspan_map[col]


def _finalize_row(newtable: _Element, newrow: _Element, rowspan_map: dict[int, int], max_cols: int) -> None:
    "Close a row: insert trailing rowspan placeholders, pad to width, append if non-empty."
    _flush_rowspan_phantoms(rowspan_map, newrow)
    while len(newrow) < max_cols:
        newrow.append(define_cell_type(False))
    if _row_has_content(newrow):
        newtable.append(newrow)


def _fill_cell(
    new_child_elem: _Element,
    cell: _Element,
    nested_elems: set[_Element],
    ptags_with_div: set[str],
    options: Extractor,
) -> None:
    "Extract a source td/th cell's content into the new <cell>, rewiring inline and block children."
    if len(cell) == 0:
        processed_cell = process_node(cell, options)
        if processed_cell is not None:
            new_child_elem.text, new_child_elem.tail = processed_cell.text, processed_cell.tail
        return
    new_child_elem.text, new_child_elem.tail = cell.text, cell.tail
    cell.tag = "done"  # rename before inner walk so handle_formatting wraps orphan spans in <p>
    for child in cell.iterdescendants():
        if not isinstance(child.tag, str) or child.tag == "done":
            continue
        if child in nested_elems:
            # preserve tail text of nested tables (text after </table> inside the cell)
            if child.tag == "table" and child.tail:
                if len(new_child_elem) > 0:
                    new_child_elem[-1].tail = (new_child_elem[-1].tail or "") + child.tail
                else:
                    new_child_elem.text = (new_child_elem.text or "") + child.tail
            continue
        if child.tag in TABLE_ELEMS:  # stray cell from malformed HTML
            child.tag = "cell"
            processed_subchild = handle_textnode(child, options, preserve_spaces=True)
        elif child.tag in _INLINE_WRAP_TAGS:
            processed_subchild = handle_textnode(child, options, preserve_spaces=True)
            # handle_textnode drops inline wrappers (ref/hi/del) with children but no direct
            # text (e.g. <ref><hi>link text</hi></ref>); carry the subtree directly instead
            if processed_subchild is None and len(child) > 0:
                define_newelem(child, new_child_elem, keep_children=True)
                for el in child.iter("*"):  # iter() includes child itself
                    el.tag = "done"
                continue
        # lists in cells only in recall mode: keeping them otherwise is noise (measured precision loss)
        elif child.tag == "list" and options.focus == "recall":
            processed_subchild = handle_lists(child, options)
            if processed_subchild is not None:
                new_child_elem.append(processed_subchild)
            child.tag = "done"
            continue
        else:
            processed_subchild = handle_textelem(child, ptags_with_div, options)
        define_newelem(processed_subchild, new_child_elem, keep_children=True)
        child.tag = "done"


def handle_table(table_elem: _Element, potential_tags: set[str], options: Extractor) -> _Element | None:
    "Process single table element."
    newtable = Element("table")
    ptags_with_div = potential_tags | {"div"}

    # strip these structural elements
    strip_tags(table_elem, "thead", "tbody", "tfoot")

    # Collect elements inside nested <table> descendants.  Used only in the inner cell
    # walk: skip without "done"-marking so the main extraction loop can call handle_table()
    # on each nested table separately.  Must hold the elements (not id()) — lxml proxies are
    # weakly referenced; id() values become stale as soon as the proxy is freed.
    nested_elems: set[_Element] = set()
    for nested_table in table_elem.iterdescendants("table"):
        nested_elems.update(nested_table.iter())

    # Count columns using only direct-child rows and direct-child cells (skipping nested tables).
    # table_elem.iter("tr") would traverse nested table rows; findall("tr") stays at this table's level.
    direct_rows = table_elem.findall("tr")
    col_counts = [sum(_span(td, "colspan") for td in tr if td.tag in TABLE_ELEMS) for tr in direct_rows]
    max_cols = min(max(col_counts, default=0), _MAX_SPAN)

    # Handle caption: emit it as a header row before the table body.
    # findall() stays at direct-child level; iter() would also hit nested tables' captions.
    for caption_elem in table_elem.findall("caption"):
        caption_text = " ".join(caption_elem.itertext()).strip()
        if caption_text:
            caption_row = Element("row")
            caption_cell = define_cell_type(True)
            caption_cell.text = caption_text
            caption_row.append(caption_cell)
            while len(caption_row) < max_cols:
                caption_row.append(define_cell_type(False))
            newtable.append(caption_row)
        caption_elem.tag = "done"

    header_row_emitted = False
    row_has_th = False
    newrow = Element("row")
    rowspan_map: dict[int, int] = {}  # col_idx → rows still spanned from a rowspan cell

    for elem in table_elem:
        if not isinstance(elem.tag, str):
            continue
        if elem.tag == "tr":
            # flush the previous row (dropping it if all cells are empty), then start a fresh one
            if len(newrow) > 0:
                _finalize_row(newtable, newrow, rowspan_map, max_cols)
                header_row_emitted = header_row_emitted or row_has_th
            newrow = Element("row")
            row_has_th = False
            _flush_rowspan_phantoms(rowspan_map, newrow)
            cells: _Element | list[_Element] = elem
        elif elem.tag in TABLE_ELEMS:
            cells = [elem]  # orphan cell without <tr> wrapper (malformed HTML)
        else:
            if elem.tag != "table":  # leave nested tables for the main extraction loop
                elem.tag = "done"
            continue

        for cell in cells:
            if not isinstance(cell.tag, str):
                continue
            if cell.tag not in TABLE_ELEMS:
                continue
            is_header = cell.tag == "th" and not header_row_emitted
            row_has_th = row_has_th or is_header
            _flush_rowspan_phantoms(rowspan_map, newrow)
            new_child_elem = define_cell_type(is_header)
            colspan = _span(cell, "colspan")
            # Track rowspan: mark all spanned columns as occupied for subsequent rows
            rows = _span(cell, "rowspan")
            if rows > 1:
                for c in range(len(newrow), len(newrow) + colspan):
                    rowspan_map[c] = rows - 1
            _fill_cell(new_child_elem, cell, nested_elems, ptags_with_div, options)
            # add to tree (keep empty cells so column positions stay aligned)
            newrow.append(new_child_elem)
            # inline colspan: pad with empty cells so subsequent rows align
            for _ in range(colspan - 1):
                newrow.append(define_cell_type(is_header))
            cell.tag = "done"
        elem.tag = "done"

    _finalize_row(newtable, newrow, rowspan_map, max_cols)
    if len(newtable) > 0:
        return newtable
    return None


def handle_image(element: _Element | None, options: Extractor | None = None) -> _Element | None:
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
    link = processed_element.get("src", "")
    if not link.startswith("http"):
        if options is not None and options.url is not None:
            link = urljoin(options.url, link)
        else:
            link = re.sub(r"^//", "http://", link)
        processed_element.set("src", link)

    processed_element.tail = element.tail
    return processed_element


def handle_textelem(element: _Element, potential_tags: set[str], options: Extractor) -> _Element | None:
    """Process text element and determine how to deal with its content"""
    new_element = None
    # bypass: nested elements
    if element.tag == "list":
        new_element = handle_lists(element, options)
    elif element.tag in CODES_QUOTES:
        new_element = handle_quotes(element, options)
    elif element.tag == "head":
        new_element = handle_titles(element, options)
    elif element.tag == "p":
        new_element = handle_paragraphs(element, potential_tags, options)
    elif element.tag == "lb":
        if text_chars_test(element.tail) is True:
            this_element = process_node(element, options)
            if this_element is not None:
                new_element = Element("p")
                new_element.text = this_element.tail
    elif element.tag in FORMATTING:
        new_element = handle_formatting(element, options)  # process_node(element, options)
    elif element.tag == "table" and "table" in potential_tags:
        new_element = handle_table(element, potential_tags, options)
    elif element.tag == "graphic" and "graphic" in potential_tags:
        new_element = handle_image(element, options)
    else:
        # other elements (div, ??, ??)
        new_element = handle_other_elements(element, potential_tags, options)
    return new_element


def recover_wild_text(
    tree: HtmlElement, result_body: _Element, options: Extractor, potential_tags: set[str] | None = None
) -> _Element:
    """Look for all previously unconsidered wild elements, including outside of the determined
    frame and throughout the document to recover potentially missing text parts.

    Do not widen `search_expr` (e.g. headings, more div shapes) without benchmarking the
    full suite: extra recovered text raises len_text, which can suppress the stronger
    rescues that run after this one (compare_extraction, the baseline rescue, the recall
    escalation).
    """
    LOGGER.debug("Recovering wild text elements")
    # copy: the recall branch below mutates potential_tags, must not leak back to the caller
    potential_tags = set(TAG_CATALOG if potential_tags is None else potential_tags)
    # blockquote/pre/q are already renamed to quote/code by convert_tags before this tree is built
    search_expr = ".//code|.//p|.//quote|.//table|.//div[contains(@class, 'w3-code')]"
    if options.focus == "recall":
        potential_tags.update(["div", "lb"])
        search_expr += "|.//div|.//lb|.//list"
    # prune; in fast mode (no external comparator to defer to) keep teaser-class blocks, some of
    # which are real content — this is the last-resort path after the confident extractor failed
    search_tree = prune_unwanted_sections(tree, potential_tags, options, keep_teasers=options.fast)
    # spans are always flattened; links are stripped too unless preserved
    unwanted = ("span",) if "ref" in potential_tags else ("a", "ref", "span")
    strip_tags(search_tree, *unwanted)
    subelems = search_tree.xpath(search_expr)
    # filter out inline <code> to prevent duplication (#849)
    subelems = [
        e for e in subelems
        if not (e.tag == "code" and e.getparent() is not None
                and e.getparent().tag in _INLINE_CODE_PARENTS)
    ]
    # dedup against the pre-main-pass snapshot: skip what the main pass already took -- exact
    # match (not length-gated, #634; accepted cost: identical-text elements collapse) or a
    # length-gated substring (a <p> folded into its <list> container)
    elem_texts = [_elem_text(el) for el in result_body]
    # newline-joined (trimmed element text has no newline) so no substring match spans two elements
    existing = "\n".join(filter(None, elem_texts))
    existing_elems = set(elem_texts)
    for subelem in subelems:
        processed = handle_textelem(subelem, potential_tags, options)
        if processed is None:
            continue
        text = _elem_text(processed)
        # past the cap, the substring scan is skipped and `existing` stops growing
        under_cap = len(existing) <= DEDUPE_SCAN_CAP
        if text and (text in existing_elems or (len(text) > MIN_DUPLICATE_LENGTH and under_cap and text in existing)):
            continue
        result_body.append(processed)
        if under_cap:
            existing += "\n" + text
        existing_elems.add(text)
    return result_body


def prune_unwanted_sections(
    tree: HtmlElement, potential_tags: set[str], options: Extractor, keep_teasers: bool = False
) -> HtmlElement:
    "Rule-based deletion of targeted document sections"
    favor_precision = options.focus == "precision"
    # prune the rest
    tree = prune_unwanted_nodes(tree, OVERALL_DISCARD_XPATH, with_backup=True)
    # decide if images are preserved
    if "graphic" not in potential_tags:
        tree = prune_unwanted_nodes(tree, DISCARD_IMAGE_ELEMENTS)
    # balance precision/recall
    if options.focus != "recall":
        # teaser-class blocks are sometimes real content; keep them on the recovery path,
        # which only runs once the confident extractor has already come up short
        if not keep_teasers:
            tree = prune_unwanted_nodes(tree, TEASER_DISCARD_XPATH)
        if favor_precision:
            tree = prune_unwanted_nodes(tree, PRECISION_DISCARD_XPATH)
    # remove elements by link density, several passes
    for _ in range(2):
        tree = delete_by_link_density(tree, "div", backtracking=True, favor_precision=favor_precision)
        tree = delete_by_link_density(tree, "list", backtracking=False, favor_precision=favor_precision)
        tree = delete_by_link_density(tree, "p", backtracking=False, favor_precision=favor_precision)
    # tables
    if "table" in potential_tags or favor_precision:
        # collect before deleting: removing a table mid-iteration can make tree.iter() skip a table
        # that follows a deleted one containing a nested table (iterator descends into the detached subtree)
        boilerplate_tables = [elem for elem in tree.iter("table") if link_density_test_tables(elem) is True]
        for elem in boilerplate_tables:
            delete_element(elem, keep_tail=False)
    if favor_precision:
        # delete trailing titles
        while len(tree) > 0 and (tree[-1].tag == "head"):
            delete_element(tree[-1], keep_tail=False)
        tree = delete_by_link_density(tree, "head", backtracking=False, favor_precision=True)
        tree = delete_by_link_density(tree, "quote", backtracking=False, favor_precision=True)
    return tree


def _extract(tree: HtmlElement, options: Extractor) -> tuple[_Element, str, set[str]]:
    # init
    potential_tags = set(TAG_CATALOG)
    if options.tables is True:
        potential_tags.update(["table", "td", "th", "tr"])
    if options.images is True:
        potential_tags.add("graphic")
    if options.links is True:
        potential_tags.add("ref")
    result_body = Element("body")
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
        ptest = subtree.xpath("//p//text()")
        factor = 1 if options.focus == "precision" else 3
        if not ptest or len("".join(ptest)) < options.min_extracted_size * factor:
            potential_tags.add("div")
        # polish list of potential tags
        if "ref" not in potential_tags:
            strip_tags(subtree, "ref")
        if "span" not in potential_tags:
            strip_tags(subtree, "span")
        LOGGER.debug(sorted(potential_tags))
        # proper extraction
        subelems = subtree.xpath(".//*")
        # filter out inline <code> — already part of their parent's text
        # flow; processing them separately duplicates their content (#849)
        subelems = [
            e for e in subelems
            if not (e.tag == "code" and e.getparent() is not None
                    and e.getparent().tag in _INLINE_CODE_PARENTS)
        ]
        # e.g. only lb-elems in a div
        if {e.tag for e in subelems} == {"lb"}:
            subelems = [subtree]
        # extract content
        result_body.extend([el for el in (handle_textelem(e, potential_tags, options) for e in subelems) if el is not None])
        # remove trailing titles
        while len(result_body) > 0 and (result_body[-1].tag in NOT_AT_THE_END):
            delete_element(result_body[-1], keep_tail=False)
        # exit once there is real content, not just a lone image
        if sum(e.tag != "graphic" for e in result_body) > 1:
            LOGGER.debug(trim(str(expr)))
            break
    temp_text = " ".join(result_body.itertext()).strip()
    return result_body, temp_text, potential_tags


def extract_content(cleaned_tree: HtmlElement, options: Extractor) -> tuple[_Element, str, int]:
    """Find the main content of a page using a set of XPath expressions,
    then extract relevant elements, strip them of unwanted subparts and
    convert them"""
    # backup
    backup_tree = deepcopy(cleaned_tree)

    result_body, temp_text, potential_tags = _extract(cleaned_tree, options)

    # try parsing wild <p> elements if nothing found or text too short
    # todo: test precision and recall settings here
    if len(result_body) == 0 or len(temp_text) < options.min_extracted_size:
        result_body = recover_wild_text(backup_tree, result_body, options, potential_tags)
        temp_text = " ".join(result_body.itertext()).strip()
    # drop substantial elements repeating the previous one (overlapping-candidate / recovery artifact);
    # length-gated so short genuine repeats stay for the dedup (#778) and tree-size guards
    previous = None
    for el in list(result_body):
        current = _elem_text(el)
        if current and current == previous and len(current) > MIN_DUPLICATE_LENGTH:
            delete_element(el, keep_tail=False)
        else:
            previous = current
    # filter output
    strip_elements(result_body, "done")
    strip_tags(result_body, "div")
    # return
    return result_body, temp_text, len(temp_text)


def process_comments_node(elem: _Element, potential_tags: set[str], options: Extractor) -> _Element | None:
    """Process comment node and determine how to deal with its content"""
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


def extract_comments(tree: HtmlElement, options: Extractor) -> tuple[_Element, str, int, HtmlElement]:
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
        comments_body.extend(
            filter(lambda x: x is not None, (process_comments_node(e, potential_tags, options) for e in subtree.xpath(".//*")))  # type: ignore[arg-type]
        )
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            delete_element(subtree, keep_tail=False)
            break
    # lengths
    temp_comments = " ".join(comments_body.itertext()).strip()
    return comments_body, temp_comments, len(temp_comments), tree
