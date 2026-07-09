"""
Module regrouping baseline and basic extraction functions.
"""
# pylint:disable-msg=E0611

import json
import re
from collections.abc import Iterable
from copy import copy
from html import unescape
from typing import Any

from lxml.etree import Element, SubElement, _Element
from lxml.html import HtmlElement, fragment_fromstring

from .settings import BASIC_CLEAN_XPATH, DEDUPE_SCAN_CAP, MIN_DUPLICATE_LENGTH
from .utils import as_list, load_html, remove_control_characters, trim
from .xml import delete_element

# detection (not removal, unlike HTML_STRIP_TAGS): must not fire on comparison-operator prose
# ("i<b and c>d", b a tag name), only real tags -- closing, bare (<p>), self-closing (<br/>), or
# attribute-bearing (contains '='). The old `[^>]*` swallowed prose up to the next '>'.
_HTML_TAG_NAMES = (
    "a|abbr|address|article|aside|b|blockquote|body|br|caption|cite|code|dd|del|div|dl|dt|"
    "em|figcaption|figure|footer|h[1-6]|head|header|hr|html|i|img|ins|kbd|li|main|mark|nav|"
    "ol|p|pre|q|quote|s|section|small|span|strong|sub|summary|sup|table|tbody|td|tfoot|th|"
    "thead|time|title|tr|u|ul"
)
_HTML_MARKUP = re.compile(rf"</({_HTML_TAG_NAMES})>|<({_HTML_TAG_NAMES})(\s[^<>]*=[^<>]*)?/?>", re.IGNORECASE)


def basic_cleaning(tree: HtmlElement) -> HtmlElement:
    "Remove a few section types from the document."
    for elem in BASIC_CLEAN_XPATH(tree):
        delete_element(elem)
    return tree


# schema.org text properties usable as page content
_JSON_TEXT_KEYS = ("articleBody", "reviewBody")
# types whose description carries the page content (teaser tier: summaries, last resort)
_DESCRIPTION_TYPES = ("Product", "VideoObject")
# cheap script pre-filter, derived from what _walk_json consumes: bare strings match
# property names, quoted ones match @type values. "step" is deliberately not a hook
# (too generic a substring); a schema.org HowTo carrying it is caught via its @type
_JSON_HOOKS = (
    _JSON_TEXT_KEYS + ("recipeInstructions", "acceptedAnswer") + tuple(f'"{t}"' for t in _DESCRIPTION_TYPES + ("HowTo",))
)
_JSON_HOOKS_RE = re.compile("|".join(re.escape(hook) for hook in _JSON_HOOKS))
# a strategy must accumulate more than this much text to be accepted (and a single
# <article> must carry more than this to count as content)
_MIN_CONTENT_LENGTH = 100


def _walk_json(node: Any, bodies: list[str], teasers: list[str]) -> None:
    """Collect schema.org text content from parsed JSON-LD (list-wrapped and @graph-nested
    nodes included). Teasers (Product/VideoObject descriptions) are short summaries,
    only usable when no full-text property exists.

    Note: json_metadata.py's `extract_json` also walks JSON-LD, for metadata rather than
    page content, with different (gated, one-level) traversal — see its docstring for why
    the two aren't unified. `as_list` (utils.py) is the shared building block between them.
    """
    for item in as_list(node):
        if not isinstance(item, dict):
            continue
        bodies.extend(item[key] for key in _JSON_TEXT_KEYS if isinstance(item.get(key), str) and item[key])
        # recipe/how-to instructions: a string, strings, or step objects carrying "text",
        # possibly one itemListElement level down (HowToDirection)
        for key in ("recipeInstructions", "step"):
            for step in as_list(item.get(key)):
                if isinstance(step, str):
                    bodies.append(step)
                elif isinstance(step, dict):
                    subs = [step, *as_list(step.get("itemListElement"))]
                    bodies.extend(sub["text"] for sub in subs if isinstance(sub, dict) and isinstance(sub.get("text"), str))
        # FAQ answers
        answer = item.get("acceptedAnswer")
        if isinstance(answer, dict) and isinstance(answer.get("text"), str):
            bodies.append(answer["text"])
        if any(t in str(item.get("@type", "")) for t in _DESCRIPTION_TYPES) and isinstance(item.get("description"), str):
            teasers.append(item["description"])
        for container in ("@graph", "mainEntity"):
            _walk_json(item.get(container), bodies, teasers)


def _discourse_texts(tree: HtmlElement) -> list[str]:
    "Extract post HTML from the JSON Discourse forums preload into an attribute (page body is empty)."
    node = tree.find('.//div[@id="data-preloaded"]')
    if node is None:
        return []
    try:
        preloaded = json.loads(node.get("data-preloaded") or "")
    except Exception:
        return []
    if not isinstance(preloaded, dict):
        return []
    texts: list[str] = []
    for key, value in preloaded.items():
        if not key.startswith("topic_"):
            continue
        try:
            posts = json.loads(value)["post_stream"]["posts"]
        except Exception:
            continue
        texts.extend(post["cooked"] for post in posts if isinstance(post, dict) and isinstance(post.get("cooked"), str))
    return texts


def _render_text(raw: str) -> str:
    "Derive clean text from an embedded-JSON value which may carry (escaped) HTML markup."
    # some sites HTML-escape the content ("&lt;p&gt;…"); unescape so markup is parsed, not leaked.
    # remove control chars after unescape (&#1; -> one char): strict=False JSON lets them through
    # and lxml rejects them in .text assignments
    raw = remove_control_characters(unescape(raw))
    if _HTML_MARKUP.search(raw):
        # fragment parse: load_html targets full documents and rejects fragments
        try:
            return trim(fragment_fromstring(raw, create_parent="div").text_content())
        except Exception:  # pragma: no cover
            pass
    return trim(raw)


def _build_body(texts: Iterable[str], dedupe: bool = False) -> tuple[_Element, str]:
    "Wrap one paragraph per text in a fresh body element, optionally dropping repeated content."
    postbody = Element("body")
    temp_text = ""
    for text in texts:
        # strip control chars lxml rejects in .text (element inputs skip load_html's cleaning)
        text = remove_control_characters(text)
        # keep short paragraphs (<= MIN_DUPLICATE_LENGTH) even if they recur -- only long substring
        # repeats (e.g. a <p> nested in its <blockquote>) are artifacts. Scan capped at
        # DEDUPE_SCAN_CAP; newline-joined (trimmed text has none) so no match spans two paragraphs
        if text and (
            not dedupe or len(text) <= MIN_DUPLICATE_LENGTH or len(temp_text) > DEDUPE_SCAN_CAP or text not in temp_text
        ):
            SubElement(postbody, "p").text = text
            temp_text += "\n" + text if temp_text else text
    return postbody, temp_text


def _attempt(texts: Iterable[str], dedupe: bool = False) -> tuple[_Element, str, int] | None:
    "Build a body from the texts and accept it if it carries enough content."
    postbody, temp_text = _build_body(texts, dedupe)
    return (postbody, temp_text, len(temp_text)) if len(temp_text) > _MIN_CONTENT_LENGTH else None


def _collect_json_content(tree: HtmlElement) -> tuple[list[str], list[str]]:
    "Gather raw text content embedded as JSON: (full-text bodies, teaser descriptions). Values may carry markup; render with _render_text at use time."
    bodies: list[str] = []
    teasers: list[str] = []
    for elem in tree.iterfind('.//script[@type="application/ld+json"]'):
        if elem.text and _JSON_HOOKS_RE.search(elem.text):
            try:
                # strict=False: real pages carry raw newlines/tabs inside JSON strings
                _walk_json(json.loads(elem.text, strict=False), bodies, teasers)
            except Exception:  # JSONDecodeError
                continue
    # Discourse forums render posts client-side but embed them as JSON in an attribute
    bodies.extend(_discourse_texts(tree))
    return bodies, teasers


def baseline(filecontent: Any) -> tuple[_Element, str, int]:
    """Use baseline extraction function targeting content in embedded JSON or text elements.

    Tries a series of sources and takes the first that yields enough text:
    JSON content embedded in scripts or attributes (schema.org properties,
    Discourse forum posts), article tags, text paragraphs, schema.org teaser
    descriptions, and finally the raw text of the whole page body.

    Args:
        filecontent: HTML code as binary string or string (or LXML element;
            elements are copied, the input is left untouched).

    Returns:
        A LXML <body> element containing the extracted paragraphs,
        the main text as string, and its length as integer.

    """
    tree = load_html(filecontent)
    if tree is None:
        return Element("body"), "", 0
    if isinstance(filecontent, HtmlElement):
        tree = copy(tree)  # basic_cleaning below mutates the tree

    # scrape from embedded JSON: full-text properties first, teaser descriptions kept for
    # later. dedupe: pages often embed the same JSON-LD block twice (theme + SEO plugin)
    json_bodies, json_teasers = _collect_json_content(tree)
    if result := _attempt(map(_render_text, json_bodies), dedupe=True):
        return result

    tree = basic_cleaning(tree)

    # article tags: a dominant one relegates much smaller siblings to noise (related teasers),
    # similar-sized ones are all content (forum posts). Nested articles excluded (counted in ancestor)
    article_texts = [
        text
        for elem in tree.xpath(".//article[not(ancestor::article)]")
        if len(text := trim(elem.text_content())) > _MIN_CONTENT_LENGTH
    ]
    if article_texts:
        # never None: the longest article passes both its own length gate and the cutoff
        cutoff = max(map(len, article_texts)) / 5
        if result := _attempt(text for text in article_texts if len(text) >= cutoff):
            return result

    # scrape from text paragraphs, dropping repeats: a nested element (e.g. <p> in
    # <blockquote>) duplicates part of its container's text, collected first in document order
    paragraphs = (trim(element.text_content()) for element in tree.iter("blockquote", "code", "p", "pre", "q", "quote"))
    if result := _attempt(paragraphs, dedupe=True):
        return result

    # teaser tier: Product/VideoObject descriptions, once every full-text source came up empty.
    # A short summary must not shadow a longer body dump -- it wins only if the dump is shorter
    teaser = _attempt(map(_render_text, json_teasers), dedupe=True)

    # default strategy: clean the tree and take everything
    postbody = Element("body")
    body_elem = tree.find(".//body")
    if body_elem is not None:
        p_elem = SubElement(postbody, "p")
        # strip control chars lxml rejects in .text (element inputs skip load_html's cleaning)
        p_elem.text = remove_control_characters("\n".join(text for e in body_elem.itertext() if (text := trim(e))))
        if not teaser or len(p_elem.text) >= teaser[2]:
            return postbody, p_elem.text, len(p_elem.text)

    return teaser or (postbody, "", 0)


# block-level elements: their boundaries separate text runs (minified pages carry no whitespace there)
_BLOCK_ELEMS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "summary",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}


def html2txt(content: Any, clean: bool = True) -> str:
    """Run basic html2txt on a document.

    Args:
        content: HTML document as string or LXML element (elements are copied, the input is left untouched).
        clean: remove potentially undesirable elements.

    Returns:
        The extracted text in the form of a string or an empty string.

    """
    tree = load_html(content)
    if tree is None:
        return ""
    if isinstance(content, HtmlElement):
        tree = copy(tree)  # the steps below modify the tree
    body = tree.find(".//body")
    if body is None:
        # a caller-supplied element without <body> is itself the content; a parsed
        # document without one (e.g. a feed) is not HTML text
        if not isinstance(content, HtmlElement):
            return ""
        body = tree
    if clean:
        body = basic_cleaning(body)
    # space block boundaries so adjacent runs don't stick (minified pages). remove_control_characters
    # guards the .text write against chars lxml rejects (short-circuits on printable; str input pre-cleaned)
    for elem in body.iter(*_BLOCK_ELEMS):
        elem.text = f" {remove_control_characters(elem.text)}" if elem.text else " "
        elem.tail = f" {remove_control_characters(elem.tail)}" if elem.tail else " "
    return " ".join(body.text_content().split())
