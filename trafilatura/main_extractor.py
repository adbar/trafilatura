# pylint:disable-msg=E0611
"""
Functions related to the main Trafilatura extractor.
"""

import logging
import re  # import regex as re
from copy import deepcopy
from urllib.parse import urljoin

from lxml.etree import Element, SubElement, XPath, _Element, strip_elements, strip_tags, tostring
from lxml.html import HtmlElement

# own
from .htmlprocessing import (
    delete_by_link_density,
    handle_textnode,
    link_density_test_tables,
    process_node,
    prune_unwanted_nodes,
)
from .settings import (
    DEDUPE_SCAN_CAP,
    INLINE_CARRIED,
    INLINE_CONSUMING,
    INLINE_FORMATTABLE,
    MIN_DUPLICATE_LENGTH,
    TAG_CATALOG,
    Extractor,
)
from .utils import FORMATTING_PROTECTED, SPACING_PROTECTED, image_src, text_chars_test, trim
from .xml import delete_element, separates_inline
from .xpaths import (
    BODY_XPATH,
    COMMENTS_DISCARD_XPATH,
    COMMENTS_XPATH,
    DISCARD_IMAGE_ELEMENTS,
    LISTING_BODY_XPATH,
    OVERALL_DISCARD_XPATH,
    PRECISION_DISCARD_XPATH,
    TEASER_DISCARD_XPATH,
)

LOGGER = logging.getLogger(__name__)


TABLE_ELEMS = {"td", "th"}
# meaningful internal attributes to carry onto a rewired sub-element (drop stray class/style/width/etc.)
KEEP_ATTRS = {"rend", "role", "target", "src", "alt", "title"}
CODES_QUOTES = {"code", "quote"}
# blocks rebuilt as new elements by handle_textelem(), which leaves the source tail behind
REBUILT_BLOCKS = CODES_QUOTES | {"list", "table"}
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


def _log_event(msg: str, tag: object, text: bytes | str | None) -> None:
    "Format extraction event for debugging purposes."
    LOGGER.debug("%s: %s %s", msg, tag, trim(text or "") or "None")


def handle_titles(element: _Element, options: Extractor) -> _Element | None:
    """Process head elements (titles)"""
    if len(element) == 0:
        title = process_node(element, options)
    else:
        title = deepcopy(element)
        # children already consumed by an earlier pass over the same tree
        strip_elements(title, "done")
        for child in element.iterdescendants("*"):
            child.tag = "done"
    return title if is_text_element(title) else None


def handle_formatting(element: _Element, options: Extractor) -> _Element | None:
    """Process formatting elements (b, i, etc. converted to hi) found
    outside of paragraphs"""
    formatting = process_node(element, options)
    if formatting is None:
        return None

    parent = element.getparent()
    if parent is not None and parent.tag in FORMATTING_PROTECTED:
        return formatting
    # repair orphan elements
    wrapper = Element("p")
    wrapper.append(formatting)
    return wrapper


def process_nested_elements(child: _Element, new_child_elem: _Element, options: Extractor) -> None:
    "Iterate through an element child and rewire its descendants."
    new_child_elem.text = child.text
    for subelem in child.iterdescendants("*"):
        if subelem.tag == "list":
            _append_block(new_child_elem, handle_lists(subelem, options), subelem)
        elif subelem.tag == "p" and len(subelem) > 0:
            _append_block(new_child_elem, handle_paragraphs(subelem, _QUOTE_TAGS, options), subelem)
        elif subelem.tag == "graphic":
            _append_block(new_child_elem, handle_image(subelem, options), subelem)
        elif subelem.tag in INLINE_CARRIED:
            define_newelem(subelem, new_child_elem, keep_children=True)
        else:
            if len(subelem) > 0 and text_chars_test(subelem.tail):
                # the tail follows the children, which are appended after this element
                subelem[-1].tail, subelem.tail = f"{subelem[-1].tail or ''}{subelem.tail}", None
            define_newelem(handle_textnode(subelem, options, comments_fix=False), new_child_elem)
        subelem.tag = "done"


def _append_block(parent: _Element, processed: _Element | None, source: _Element) -> None:
    "Append a processed block with the source tail, or keep that tail as text after the parent's content."
    if processed is not None:
        processed.tail = source.tail
        parent.append(processed)
    elif source.tail and text_chars_test(source.tail):
        last = parent[-1] if len(parent) > 0 else None
        before, tail = (parent.text if last is None else last.tail) or "", source.tail
        # a dropped block still separates the text around it, a dropped image does not
        if source.tag != "graphic" and (before or last is not None) and not before[-1:].isspace() and not tail[0].isspace():
            tail = f" {tail}"
        if last is None:
            parent.text = before + tail
        else:
            last.tail = before + tail


def update_elem_rendition(elem: _Element, new_elem: _Element) -> None:
    "Copy the rend attribute from an existing element to a new one."
    if rend_attr := elem.get("rend"):
        new_elem.set("rend", rend_attr)


def is_text_element(elem: _Element | None) -> bool:
    "Find if the element contains text."
    return elem is not None and text_chars_test("".join(elem.itertext())) is True


def _copy_attrs(source: _Element, target: _Element) -> None:
    "Carry the meaningful internal attributes over to a rewired element."
    for key, value in source.attrib.items():
        if key in KEEP_ATTRS:
            target.set(key, value)


def define_newelem(processed_elem: _Element | None, orig_elem: _Element, keep_children: bool = False) -> None:
    "Create a new sub-element, optionally carrying its inline children (INLINE_CARRIED)."
    if processed_elem is not None:
        childelem = SubElement(orig_elem, processed_elem.tag)
        childelem.text, childelem.tail = processed_elem.text, processed_elem.tail
        _copy_attrs(processed_elem, childelem)
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

    if text_chars_test(element.text):
        new_child_elem = SubElement(processed_element, "item")
        new_child_elem.text = element.text

    for child in element.iterdescendants("item"):
        # items of a nested list are processed by the recursive call and renamed "done",
        # but lxml fetches the first of them before that happens: skip it here
        if child.tag == "done":
            continue
        new_child_elem = Element("item")
        if len(child) == 0:
            processed_child = process_node(child, options)
            if processed_child is not None:
                new_child_elem.text = " ".join(filter(None, (processed_child.text, processed_child.tail)))
        else:
            process_nested_elements(child, new_child_elem, options)
            if text_chars_test(child.tail) and len(new_child_elem) > 0:
                last = new_child_elem[-1]
                last.tail = f"{last.tail} {child.tail}" if text_chars_test(last.tail) else child.tail
        if is_text_element(new_child_elem) or next(new_child_elem.iter("graphic"), None) is not None:
            update_elem_rendition(child, new_child_elem)
            processed_element.append(new_child_elem)
        child.tag = "done"
    element.tag = "done"
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
    return code is not None and len(element) == 1 and not (element.text or "").strip() and not (code.tail or "").strip()


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
    process_nested_elements(element, processed_element, options)
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

    if element.tag != "div" or "div" not in potential_tags:
        if element.tag != "done":
            _log_event("discarding element", element.tag, element.text)
        return None

    processed_element = handle_textnode(element, options, comments_fix=False, preserve_spaces=True)
    if processed_element is None or not text_chars_test(processed_element.text):
        return None
    processed_element.attrib.clear()
    processed_element.tag = "p"
    return processed_element


def handle_paragraphs(element: _Element, potential_tags: set[str], options: Extractor) -> _Element | None:
    "Process paragraphs along with their children, trim and clean the content."
    # attrib.clear() verified unnecessary here (output_diff 0/1501, 2026-08)

    # no children
    if len(element) == 0:
        return process_node(element, options)

    # children
    processed_element = Element(element.tag)
    # unexpected children: keep their text in place
    strip_tags(element, *{str(c.tag) for c in element.iterdescendants("*") if c.tag not in {*potential_tags, "done"}})
    for child in element.iter("*"):
        # todo: act on spacing here?
        processed_child = handle_textnode(child, options, comments_fix=False, preserve_spaces=True)
        if processed_child is not None:
            # todo: needing attention!
            if processed_child.tag == "p":
                _log_event("extra in p", "p", processed_child.text)
                processed_element.text = " ".join(filter(None, (processed_element.text, processed_child.text)))
                child.tag = "done"
                continue
            # handle formatting
            newsub = Element(child.tag)
            if processed_child.tag in INLINE_CONSUMING:
                # carry inline children verbatim (ref/hi/del wrapping formatting)
                if _wraps_inline(processed_child):
                    define_newelem(processed_child, processed_element, keep_children=True)
                    child.tag = "done"
                    continue
                # check depth and clean
                for item in processed_child:
                    if item.tag == "lb" and item.tail:
                        item.tail = " " + item.tail.lstrip()
                    elif text_chars_test(item.text):
                        item.text = f" {item.text}"
                strip_tags(processed_child, *{str(item.tag) for item in processed_child})
                _copy_attrs(child, newsub)
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
    # text_chars_test, not truthiness: layout wrappers (clearfix/spacer divs, cleared-out
    # ad slots) leave indentation-only text, which used to be emitted as blank paragraphs
    # and, sitting between two copies of a paragraph, also defeated the adjacent dedup
    if text_chars_test(processed_element.text):
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
    if any(cell.text or len(cell) > 0 for cell in newrow):
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
            # nested tables are left to the main loop, their tail moves to the cell holding them
            if child.tag == "table" and next(child.iterancestors("table")) not in nested_elems:
                _append_block(new_child_elem, None, child)
                child.tail = None
            continue
        if separates_inline(child) and not text_chars_test(child.tail):
            new_child_elem.append(Element("lb"))
            child.tag = "done"
            continue
        if child.tag in TABLE_ELEMS:  # stray cell from malformed HTML
            child.tag = "cell"
            processed_subchild = handle_textnode(child, options, preserve_spaces=True)
        elif child.tag in INLINE_CONSUMING:
            processed_subchild = handle_textnode(child, options, preserve_spaces=True)
            # handle_textnode drops inline wrappers (ref/hi/del) with children but no direct
            # text (e.g. <ref><hi>link text</hi></ref>); carry the subtree directly instead
            if processed_subchild is None and len(child) > 0:
                processed_subchild = child
        # lists in cells only in recall mode: keeping them otherwise is noise (measured precision loss)
        elif child.tag == "list":
            processed_list = handle_lists(child, options)
            _append_block(new_child_elem, processed_list if options.focus == "recall" else None, child)
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

    # direct children only, nested tables are left to the main loop.
    # Orphan cells join the current row but do not count for max_cols.
    rows: list[list[_Element]] = [[]]
    captions: list[str] = []
    max_cols = 0
    for elem in table_elem:
        if elem.tag == "tr":
            rows.append([cell for cell in elem if cell.tag in TABLE_ELEMS])
            max_cols = max(max_cols, sum(_span(cell, "colspan") for cell in rows[-1]))
        elif elem.tag in TABLE_ELEMS:
            rows[-1].append(elem)
            continue
        elif elem.tag == "caption":
            captions.append(" ".join(elem.itertext()).strip())
            # text consumed above, not to be emitted again, images are left to the main loop
            for sub in elem.iterdescendants("*"):
                if sub.tag == "graphic":
                    sub.tail = None
                else:
                    sub.tag = "done"
        elif not isinstance(elem.tag, str) or elem.tag == "table":
            continue
        elem.tag = "done"
    max_cols = min(max_cols, _MAX_SPAN)

    for caption_text in filter(None, captions):
        caption_cell = define_cell_type(True)
        caption_cell.text = caption_text
        caption_row = Element("row")
        caption_row.append(caption_cell)
        _finalize_row(newtable, caption_row, {}, max_cols)

    header_row_emitted = False
    rowspan_map: dict[int, int] = {}  # col_idx → rows still spanned from a rowspan cell
    for cells in rows:
        newrow = Element("row")
        row_has_th = False
        for cell in cells:
            is_header = cell.tag == "th" and not header_row_emitted
            row_has_th = row_has_th or is_header
            _flush_rowspan_phantoms(rowspan_map, newrow)
            new_child_elem = define_cell_type(is_header)
            colspan = _span(cell, "colspan")
            # Track rowspan: mark all spanned columns as occupied for subsequent rows
            rowspan = _span(cell, "rowspan")
            if rowspan > 1:
                for c in range(len(newrow), len(newrow) + colspan):
                    rowspan_map[c] = rowspan - 1
            _fill_cell(new_child_elem, cell, nested_elems, ptags_with_div, options)
            # add to tree (keep empty cells so column positions stay aligned)
            newrow.append(new_child_elem)
            # inline colspan: pad with empty cells so subsequent rows align
            for _ in range(colspan - 1):
                newrow.append(define_cell_type(is_header))
            cell.tag = "done"
        _finalize_row(newtable, newrow, rowspan_map, max_cols)
        header_row_emitted = header_row_emitted or row_has_th
    return newtable if len(newtable) > 0 else None


def handle_image(element: _Element, options: Extractor | None = None) -> _Element | None:
    "Process image elements and their relevant attributes."
    link = image_src(element)
    if link is None:
        return None
    if not link.startswith("http"):
        if options is not None and options.url is not None:
            link = urljoin(options.url, link)
        else:
            link = re.sub(r"^//", "http://", link)

    processed_element = Element(element.tag)
    processed_element.set("src", link)
    if alt_attr := element.get("alt"):
        processed_element.set("alt", alt_attr)
    if title_attr := element.get("title"):
        processed_element.set("title", title_attr)
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
    elif element.tag in INLINE_CONSUMING:
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
    tree: HtmlElement,
    result_body: _Element,
    options: Extractor,
    potential_tags: set[str] | None = None,
    consumed: set[_Element] | None = None,
) -> _Element:
    """Look for all previously unconsidered wild elements, including outside of the determined
    frame and throughout the document to recover potentially missing text parts.

    Do not widen `search_expr` (e.g. headings, more div shapes) without benchmarking the
    full suite: extra recovered text increases the extracted length, which can suppress
    the stronger rescues that run after this one (compare_extraction, the baseline rescue,
    the recall escalation).
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
    subelems = search_tree.xpath(search_expr)
    # dedup against the pre-main-pass snapshot: skip what the main pass already took -- exact
    # match (not length-gated, #634; accepted cost: identical-text elements collapse) or a
    # length-gated substring (a <p> folded into its <list> container)
    elem_texts = [_elem_text(el) for el in result_body]
    # newline-joined (trimmed element text has no newline) so no substring match spans two elements
    existing = "\n".join(filter(None, elem_texts))
    existing_elems = set(elem_texts)
    # elements emitted or deduped whole: their descendants are covered
    handled: set[_Element] = set()
    for subelem in subelems:
        if (consumed and subelem in consumed) or any(a in handled for a in subelem.iterancestors()):
            continue
        processed = handle_textelem(subelem, potential_tags, options)
        if processed is None:
            continue
        if processed is subelem:
            handled.add(subelem)
        text = _elem_text(processed)
        # image-only blocks have no text to compare, check their sources against the live body
        images = {img.get("src") for img in processed.iter("graphic")}
        if not text and images and images <= {g.get("src") for g in result_body.iter("graphic")}:
            continue
        # past the cap, the substring scan is skipped and `existing` stops growing
        under_cap = len(existing) <= DEDUPE_SCAN_CAP
        # a copy carrying its source tail is a fragment of a text run: no length gate
        fragment = trim(text + (processed.tail or "")) if text_chars_test(processed.tail) else ""
        if text and (
            text in existing_elems
            or (under_cap and ((len(text) > MIN_DUPLICATE_LENGTH and text in existing) or (fragment and fragment in existing)))
        ):
            continue
        result_body.append(processed)
        if under_cap:
            existing += "\n" + (fragment or text)
        existing_elems.add(text)
    return result_body


def prune_unwanted_sections(
    tree: HtmlElement,
    potential_tags: set[str],
    options: Extractor,
    keep_teasers: bool = False,
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
    # after the link density tests, which need the refs
    strip_tags(tree, "span", *(() if "ref" in potential_tags else ("ref",)))
    return tree


# A sibling-article container is the body of a listing page, but on an article page the same
# shape is a teaser strip ("recommended stories") sitting beside the body. Only the listing
# container carries the bulk of the page, so that share is what tells the two apart.
LISTING_TEXT_SHARE = 0.6


def _holds_most_of_the_text(tree: HtmlElement, expr: XPath) -> bool:
    "Whether the first element matched by expr carries most of the text of the tree."
    match = next((s for s in expr(tree) if s is not None), None)
    if match is None:
        return False
    page_length = len(trim(" ".join(tree.itertext())))
    if not page_length:
        return False
    return len(trim(" ".join(match.itertext()))) / page_length >= LISTING_TEXT_SHARE


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
    expressions = BODY_XPATH
    if options.focus == "recall" and _holds_most_of_the_text(tree, LISTING_BODY_XPATH[0]):
        expressions = LISTING_BODY_XPATH + BODY_XPATH
    # iterate
    for expr in expressions:
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
        LOGGER.debug(sorted(potential_tags))

        subelems = subtree.xpath(".//*")
        # a single text run (only lb or inline elements): process the frame itself
        # lb-only frames go there unconditionally, a failed main pass then hands them to the recovery
        tags = {e.tag for e in subelems}
        if tags == {"lb"} or (subtree.tag == "div" and "div" in potential_tags and tags <= INLINE_FORMATTABLE | {"lb"}):
            subelems = [subtree]
        # the frame's own text before its first child, kept if the frame is accepted
        lead, start = None, len(result_body)
        if subelems != [subtree] and text_chars_test(subtree.text):
            lead = Element("p")
            lead.text = subtree.text
            lead = process_node(lead, options)
        # extract content
        for elem in subelems:
            # handle_other_elements() emits a text-bearing div as-is, children and all, and
            # appending it MOVES it into result_body. Its descendants are still in the list
            # captured above, so revisiting one would emit its text twice -- an <lb> whose tail
            # carries a paragraph turned into a duplicate of that paragraph. handle_paragraphs()
            # marks the children it consumes "done"; this covers the elements it cannot retag.
            if elem.getroottree().getroot() is result_body:
                continue
            # handlers may rename the element to "done", so read these first
            tag, tail = elem.tag, elem.tail
            processed_elem = handle_textelem(elem, potential_tags, options)
            if processed_elem is not None:
                result_body.append(processed_elem)
                # a copy leaves its source behind for a later, wider subtree
                if elem.getroottree().getroot() is not result_body:
                    elem.tag = "done"
            # text right after a rebuilt block is a paragraph of its own, like an <lb> tail,
            # unless the handler already carried it over (a code block copied as a whole)
            if tag in REBUILT_BLOCKS and text_chars_test(tail) and (processed_elem is None or processed_elem.tail is None):
                tail_elem = Element("p")
                tail_elem.text = tail
                if process_node(tail_elem, options) is not None:
                    result_body.append(tail_elem)
        # remove trailing titles
        while len(result_body) > 0 and (result_body[-1].tag in NOT_AT_THE_END):
            delete_element(result_body[-1], keep_tail=False)
        # exit once there is real content, not just a lone image
        if sum(e.tag != "graphic" for e in result_body) > 1:
            LOGGER.debug(trim(str(expr)))
            if lead is not None:
                result_body.insert(start, lead)
            break
    temp_text = " ".join(result_body.itertext()).strip()
    return result_body, temp_text, potential_tags


def extract_content(cleaned_tree: HtmlElement, options: Extractor) -> tuple[_Element, str]:
    """Find the main content of a page using a set of XPath expressions,
    then extract relevant elements, strip them of unwanted subparts and
    convert them"""
    # backup
    backup_tree = deepcopy(cleaned_tree)
    # source order before the main pass moves elements, the backup keeps it
    order = list(cleaned_tree.iter())

    result_body, temp_text, potential_tags = _extract(cleaned_tree, options)

    # try parsing wild <p> elements if nothing found or text too short
    # todo: test precision and recall settings here
    if len(result_body) == 0 or len(temp_text) < options.min_extracted_size:
        # copies of what the main pass consumed are not recovered again
        consumed: set[_Element] = {twin for elem, twin in zip(order, backup_tree.iter(), strict=True) if elem.tag == "done"}
        result_body = recover_wild_text(backup_tree, result_body, options, potential_tags, consumed)
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
    # stripping the divs above merges their indentation into the preceding <lb>'s tail, so an
    # <lb> that only separated pruned blocks (ad slots, clearfix spacers) ends up carrying a
    # run of whitespace -- rendered verbatim as blank, space-filled lines in txt/markdown.
    # Inside code/pre that whitespace is the indentation itself, so leave those alone.
    for linebreak in result_body.iter("lb"):
        if (
            linebreak.tail
            and not text_chars_test(linebreak.tail)
            and not any(anc.tag in SPACING_PROTECTED for anc in linebreak.iterancestors())
        ):
            linebreak.tail = None
    return result_body, temp_text


def extract_comments(tree: HtmlElement, options: Extractor) -> tuple[_Element, str, HtmlElement]:
    "Try to extract comments out of potential sections in the HTML."
    comments_body = Element("body")
    # define iteration strategy
    potential_tags = set(TAG_CATALOG)  # not div: trouble with <div class="comment-author meta">
    for expr in COMMENTS_XPATH:
        # select tree if the expression has been found
        subtree = next((s for s in expr(tree) if s is not None), None)
        if subtree is None:
            continue
        # prune
        subtree = prune_unwanted_nodes(subtree, COMMENTS_DISCARD_XPATH)
        # todo: unified stripping function, taking include_links into account
        strip_tags(subtree, "ref", "span")
        for elem in subtree.xpath(".//*"):
            if elem.tag in potential_tags and (processed := handle_textnode(elem, options, comments_fix=True)) is not None:
                processed.attrib.clear()
                comments_body.append(processed)
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            delete_element(subtree, keep_tail=False)
            break
    return comments_body, " ".join(comments_body.itertext()).strip(), tree
