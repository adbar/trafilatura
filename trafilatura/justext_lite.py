"""Minimal paragraph classifier derived from jusText, without stopwords.

Original code: https://github.com/miso-belica/jusText
"""

# Copyright (c) 2011, Jan Pomikalek <jan.pomikalek@gmail.com>
# Copyright (c) 2013, Michal Belica
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re

from lxml.etree import _Element, iterwalk

from .settings import BASIC_CLEAN_XPATH

PARAGRAPH_TAGS = frozenset(
    {
        "body", "blockquote", "caption", "center", "col", "colgroup", "dd", "div", "dl", "dt",
        "fieldset", "form", "legend", "optgroup", "option", "p", "pre", "table", "td",
        "tfoot", "th", "thead", "tr", "ol", "ul", "li", "h1", "h2", "h3", "h4", "h5", "h6",
    }
)  # fmt: skip

# hidden data blobs, scrolling link farms, raw-text fallbacks holding markup as text
SKIP = frozenset({"marquee", "textarea", "iframe", "noembed", "noframes"})
# hidden blocks (menus, modals, lightboxes), click-to-open panels are kept
HIDDEN = re.compile(r"display\s*:\s*none", re.IGNORECASE)
KEEP_HIDDEN = re.compile("faq|accordion|collaps", re.IGNORECASE)

HEADINGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})

LENGTH_LOW = 50
LENGTH_HIGH = 150
MAX_LINK_DENSITY = 0.25

NEWLINES = re.compile(r"\s*[\n\r]\s*")
SPACES = re.compile(r"[^\S\n]+")


def _normalize(text: str) -> str:
    return SPACES.sub(" ", NEWLINES.sub("\n", text))


def _classify(text: str, link_chars: int, in_select: bool) -> str:
    "Context-free classification by length and link density."
    length = len(text)
    if link_chars / length > MAX_LINK_DENSITY or in_select or "\xa9" in text:
        return "bad"
    if length < LENGTH_LOW:
        return "bad" if link_chars else "short"
    return "good" if length > LENGTH_HIGH else "neargood"


def _nearest(classes: list[str], skip: set[str]) -> tuple[list[str], list[str]]:
    "Nearest class not in skip, on each side."
    left, right = [], []
    last = "bad"
    for cls in classes:
        left.append(last)
        if cls not in skip:
            last = cls
    last = "bad"
    for cls in reversed(classes):
        right.append(last)
        if cls not in skip:
            last = cls
    return left, right[::-1]


def _revise(classes: list[str]) -> None:
    "Context-sensitive classification: short and near-good paragraphs follow their neighbours."
    prev_gb, next_gb = _nearest(classes, {"short", "neargood"})
    prev_any, next_any = _nearest(classes, {"short"})
    for i, cls in enumerate(classes):
        if cls != "short":
            continue
        prev, nxt = prev_gb[i], next_gb[i]
        if prev == nxt:
            classes[i] = prev
        else:
            # exactly one side is bad, look past it for a near-good block
            near = prev_any[i] if prev == "bad" else next_any[i]
            classes[i] = "good" if near == "neargood" else "bad"
    # no short left, the left neighbour is already resolved
    _, next_gb = _nearest(classes, {"neargood"})
    prev = "bad"
    for i, cls in enumerate(classes):
        if cls == "neargood":
            classes[i] = "bad" if prev == "bad" and next_gb[i] == "bad" else "good"
        prev = classes[i]


def _skip(tag: str, elem: _Element) -> bool:
    "Subtrees left out of the text, their tail is kept."
    if tag in SKIP:
        return True
    if tag == "noscript":
        # childless, holding markup parsed as text
        return not len(elem) and (elem.text or "").lstrip().startswith("<")
    if tag in ("html", "body"):
        # hidden until a script reveals the page
        return False
    style = elem.get("style")
    return bool(style and HIDDEN.search(style) and not KEEP_HIDDEN.search(f"{elem.get('class', '')} {elem.get('id', '')}"))


def _kind(stack: list[str]) -> str:
    "Output tag for a block: heading level, code, list item (ol or ul), quote or paragraph."
    # direct parent only, an unclosed heading can hold the rest of the page
    if stack and stack[-1] in HEADINGS:
        return stack[-1]
    ancestors = set(stack)
    if "pre" in ancestors:
        return "code"
    if ancestors & {"li", "dd", "dt"}:
        return next((t for t in stack if t in ("ol", "ul")), "ul")
    if "blockquote" in ancestors:
        return "quote"
    return "p"


def extract_paragraphs(root: _Element) -> list[tuple[str, str, int]]:
    "Split a tree into text blocks at block-level tags and return those classified as content, with their kind and list number."
    blocks: list[tuple[str, str, int]] = []
    classes: list[str] = []
    nodes: list[str] = []
    stack: list[str] = []
    # open ol/ul/dl, numbered in document order so that adjacent lists stay apart
    lists: list[int] = []
    link_chars = selects = links = list_count = 0
    in_select = False
    skipped: _Element | None = None
    # basic_cleaning targets, skipped instead of deleted so the input stays untouched
    dropped = set(BASIC_CLEAN_XPATH(root))

    def close() -> None:
        nonlocal link_chars, in_select
        if nodes:
            text = "".join(nodes)
            kind = _kind(stack)
            # code keeps its indentation
            text = text.strip("\r\n").rstrip() if kind == "code" else _normalize(text.strip())
            if text.strip():
                blocks.append((text, kind, lists[0] if lists else 0))
                classes.append(_classify(text, link_chars, in_select))
            nodes.clear()
            link_chars = 0
        in_select = selects > 0

    walker = iterwalk(root, events=("start", "end", "comment", "pi"))
    for event, elem in walker:
        if event == "start":
            tag: str = elem.tag  # type: ignore[assignment]
            tag = tag.rpartition("}")[2]
            if elem is not root and (elem in dropped or _skip(tag, elem)):
                skipped = elem
                nodes.append(" ")
                walker.skip_subtree()
                continue
            if tag == "select":
                selects += 1
            if tag in PARAGRAPH_TAGS:
                close()
                stack.append(tag)
                if tag in ("ol", "ul", "dl"):
                    list_count += 1
                    lists.append(list_count)
            elif tag == "br":
                nodes.append("\n" if "pre" in stack else " ")
            elif tag == "a":
                links = 1
            text = elem.text
        else:
            # a skipped element still gets its end event
            if event == "end" and elem is not skipped:
                tag = elem.tag  # type: ignore[assignment]
                tag = tag.rpartition("}")[2]
                if tag == "select":
                    selects -= 1
                if tag in PARAGRAPH_TAGS:
                    close()
                    stack.pop()
                    if tag in ("ol", "ul", "dl"):
                        lists.pop()
                if tag == "a":
                    links = 0
            text = elem.tail
        if text and text.isspace() and "pre" not in stack:
            nodes.append(" ")
        elif text:
            nodes.append(text)
            if links:
                link_chars += len(_normalize(text))
    close()
    _revise(classes)
    return [block for block, cls in zip(blocks, classes, strict=True) if cls == "good"]
