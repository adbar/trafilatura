# pylint:disable-msg=E0611,I1101
"""Minimalistic fork of readability-lxml code

This is a python port of a ruby port of arc90's readability project

http://lab.arc90.com/experiments/readability/

Given a html document, it pulls out the main body text and cleans it up.

Ruby port by starrhorne and iterationlabs
Python port by gfxmonk

For list of contributors see
https://github.com/timbertson/python-readability
https://github.com/buriy/python-readability

License of forked code: Apache-2.0.
"""

import logging
import re

from math import sqrt
from operator import attrgetter
from typing import Any, Dict, Optional, Set

from lxml.etree import tostring
from lxml.html import HtmlElement, fragment_fromstring

from .utils import load_html, trim

LOGGER = logging.getLogger(__name__)


DOT_SPACE = re.compile(r"\.( |$)")


def _tostring(string: HtmlElement) -> str:
    return tostring(string, encoding=str, method="xml")


DIV_TO_P_ELEMS = {
    "a",
    "blockquote",
    "dl",
    "div",
    "img",
    "ol",
    "p",
    "pre",
    "table",
    "ul",
}

DIV_SCORES = {"div", "article"}
BLOCK_SCORES = {"pre", "td", "blockquote"}
BAD_ELEM_SCORES = {"address", "ol", "ul", "dl", "dd", "dt", "li", "form", "aside"}
STRUCTURE_SCORES = {"h1", "h2", "h3", "h4", "h5", "h6", "th", "header", "footer", "nav"}

TEXT_CLEAN_ELEMS = {"p", "img", "li", "a", "embed", "input"}

REGEXES = {
    "unlikelyCandidatesRe": re.compile(
        r"combx|comment|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|pagination|pager|popup|tweet|twitter",
        re.I,
    ),
    "okMaybeItsACandidateRe": re.compile(r"and|article|body|column|main|shadow", re.I),
    "positiveRe": re.compile(
        r"article|body|content|entry|hentry|main|page|pagination|post|text|blog|story",
        re.I,
    ),
    "negativeRe": re.compile(
        r"button|combx|comment|com-|contact|figure|foot|footer|footnote|form|input|masthead|media|meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|shopping|tags|tool|widget",
        re.I,
    ),
    "divToPElementsRe": re.compile(
        r"<(?:a|blockquote|dl|div|img|ol|p|pre|table|ul)", re.I
    ),
    "videoRe": re.compile(r"https?:\/\/(?:www\.)?(?:youtube|vimeo)\.com", re.I),
}

FRAME_TAGS = {"body", "html"}
LIST_TAGS = {"ol", "ul"}
# DIV_TO_P_ELEMS = {'a', 'blockquote', 'dl', 'div', 'img', 'ol', 'p', 'pre', 'table', 'ul'}


def text_length(elem: HtmlElement) -> int:
    "Return the length of the element with all its contents."
    return len(trim(elem.text_content()))


class Candidate:
    "Defines a class to score candidate elements."

    __slots__ = ["score", "elem"]

    def __init__(self, score: float, elem: HtmlElement) -> None:
        self.score: float = score
        self.elem: HtmlElement = elem


class Document:
    """Class to build a etree document out of html."""

    __slots__ = ["doc", "min_text_length", "retry_length"]

    def __init__(self, doc: HtmlElement, min_text_length: int = 25, retry_length: int = 250) -> None:
        """Generate the document

        :param doc: string of the html content.
        :param min_text_length: Set to a higher value for more precise detection of longer texts.
        :param retry_length: Set to a lower value for better detection of very small texts.

        The Document class is not re-enterable.
        It is designed to create a new Document() for each HTML file to process it.

        API method:
        .summary() -- cleaned up content
        """
        self.doc = doc
        self.min_text_length = min_text_length
        self.retry_length = retry_length

    def summary(self) -> str:
        """
        Given a HTML file, extracts the text of the article.

        Warning: It mutates internal DOM representation of the HTML document,
        so it is better to call other API methods before this one.
        """
        for elem in self.doc.iter("script", "style"):
            elem.drop_tree()

        ruthless = True
        while True:
            if ruthless:
                self.remove_unlikely_candidates()
            self.transform_misused_divs_into_paragraphs()
            candidates = self.score_paragraphs()

            best_candidate = self.select_best_candidate(candidates)

            if best_candidate:
                article = self.get_article(candidates, best_candidate)
            else:
                if ruthless is True:
                    ruthless = False
                    LOGGER.debug(
                        "Ended up stripping too much - going for a safer parse"
                    )
                    # try again
                    continue
                # go ahead
                LOGGER.debug(
                    "Ruthless and lenient parsing did not work. Returning raw html"
                )
                body = self.doc.find("body")
                article = body if body is not None else self.doc

            cleaned_article = self.sanitize(article, candidates)
            article_length = len(cleaned_article or "")
            if ruthless and article_length < self.retry_length:
                ruthless = False
                # Loop through and try again.
                continue
            return cleaned_article

    def get_article(self, candidates: Dict[HtmlElement, Candidate], best_candidate: Candidate) -> HtmlElement:
        # Now that we have the top candidate, look through its siblings for
        # content that might also be related.
        # Things like preambles, content split by ads that we removed, etc.
        sibling_score_threshold = max(10, best_candidate.score * 0.2)
        # create a new html document with a div
        output = fragment_fromstring("<div/>")
        parent = best_candidate.elem.getparent()
        siblings = list(parent) if parent is not None else [best_candidate.elem]
        for sibling in siblings:
            # in lxml there no concept of simple text
            # if isinstance(sibling, NavigableString): continue
            append = False
            # conditions
            if sibling == best_candidate.elem or (
                sibling in candidates
                and candidates[sibling].score >= sibling_score_threshold
            ):
                append = True
            elif sibling.tag == "p":
                link_density = self.get_link_density(sibling)
                node_content = sibling.text or ""
                node_length = len(node_content)

                if (
                    node_length > 80
                    and link_density < 0.25
                    or (
                        node_length <= 80
                        and link_density == 0
                        and DOT_SPACE.search(node_content)
                    )
                ):
                    append = True
            # append to the output div
            if append:
                output.append(sibling)
        # if output is not None:
        #    output.append(best_candidate.elem)
        return output

    def select_best_candidate(self, candidates: Dict[HtmlElement, Candidate]) -> Optional[Candidate]:
        if not candidates:
            return None
        sorted_candidates = sorted(
            candidates.values(), key=attrgetter("score"), reverse=True
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            for candidate in sorted_candidates[:5]:
                LOGGER.debug("Top 5: %s %s", candidate.elem.tag, candidate.score)
        return next(iter(sorted_candidates))

    def get_link_density(self, elem: HtmlElement) -> float:
        total_length = text_length(elem) or 1
        link_length = sum(text_length(link) for link in elem.findall(".//a"))
        return link_length / total_length

    def score_paragraphs(self) -> Dict[HtmlElement, Candidate]:
        candidates = {}

        for elem in self.doc.iter("p", "pre", "td"):
            parent_node = elem.getparent()
            if parent_node is None:
                continue
            grand_parent_node = parent_node.getparent()

            elem_text = trim(elem.text_content())
            elem_text_len = len(elem_text)

            # discard too short paragraphs
            if elem_text_len < self.min_text_length:
                continue

            for node in (parent_node, grand_parent_node):
                if node is not None and node not in candidates:
                    candidates[node] = self.score_node(node)

            score = 1 + len(elem_text.split(",")) + min((elem_text_len / 100), 3)
            # if elem not in candidates:
            #    candidates[elem] = self.score_node(elem)

            candidates[parent_node].score += score
            if grand_parent_node is not None:
                candidates[grand_parent_node].score += score / 2

        # Scale the final candidates score based on link density. Good content
        # should have a relatively small link density (5% or less) and be
        # mostly unaffected by this operation.
        for elem, candidate in candidates.items():
            candidate.score *= 1 - self.get_link_density(elem)

        return candidates

    def class_weight(self, elem: HtmlElement) -> float:
        weight = 0
        for attribute in filter(None, (elem.get("class"), elem.get("id"))):
            if REGEXES["negativeRe"].search(attribute):
                weight -= 25
            if REGEXES["positiveRe"].search(attribute):
                weight += 25
        return weight

    def score_node(self, elem: HtmlElement) -> Candidate:
        score = self.class_weight(elem)
        tag = str(elem.tag)
        name = tag.lower()
        if name in DIV_SCORES:
            score += 5
        elif name in BLOCK_SCORES:
            score += 3
        elif name in BAD_ELEM_SCORES:
            score -= 3
        elif name in STRUCTURE_SCORES:
            score -= 5
        return Candidate(score, elem)

    def remove_unlikely_candidates(self) -> None:
        for elem in self.doc.findall(".//*"):
            attrs = " ".join(filter(None, (elem.get("class"), elem.get("id"))))
            if len(attrs) < 2:
                continue
            if (
                elem.tag not in FRAME_TAGS
                and REGEXES["unlikelyCandidatesRe"].search(attrs)
                and (not REGEXES["okMaybeItsACandidateRe"].search(attrs))
            ):
                # LOGGER.debug("Removing unlikely candidate: %s", elem.tag)
                elem.drop_tree()

    def transform_misused_divs_into_paragraphs(self) -> None:
        for elem in self.doc.findall(".//div"):
            # transform <div>s that do not contain other block elements into
            # <p>s
            # FIXME: The current implementation ignores all descendants that
            # are not direct children of elem
            # This results in incorrect results in case there is an <img>
            # buried within an <a> for example
            # hurts precision:
            # if not any(e.tag in DIV_TO_P_ELEMS for e in list(elem)):
            if not REGEXES["divToPElementsRe"].search(
                "".join(map(_tostring, list(elem)))
            ):
                elem.tag = "p"

        for elem in self.doc.findall(".//div"):
            if elem.text and elem.text.strip():
                p_elem = fragment_fromstring("<p/>")
                p_elem.text, elem.text = elem.text, None
                elem.insert(0, p_elem)

            for pos, child in sorted(enumerate(elem), reverse=True):
                if child.tail and child.tail.strip():
                    p_elem = fragment_fromstring("<p/>")
                    p_elem.text, child.tail = child.tail, None
                    elem.insert(pos + 1, p_elem)
                if child.tag == "br":
                    child.drop_tree()

    def sanitize(self, node: HtmlElement, candidates: Dict[HtmlElement, Candidate]) -> str:
        for header in node.iter("h1", "h2", "h3", "h4", "h5", "h6"):
            if self.class_weight(header) < 0 or self.get_link_density(header) > 0.33:
                header.drop_tree()

        for elem in node.iter("form", "textarea"):
            elem.drop_tree()

        for elem in node.iter("iframe"):
            if "src" in elem.attrib and REGEXES["videoRe"].search(elem.attrib["src"]):
                elem.text = "VIDEO"  # ADD content to iframe text node to force <iframe></iframe> proper output
            else:
                elem.drop_tree()

        allowed: Set[HtmlElement] = set()
        # Conditionally clean <table>s, <ul>s, and <div>s
        for elem in reversed(
            node.xpath("//table|//ul|//div|//aside|//header|//footer|//section")
        ):
            if elem in allowed:
                continue
            weight = self.class_weight(elem)
            score = candidates[elem].score if elem in candidates else 0
            if weight + score < 0:
                LOGGER.debug(
                    "Removed %s with score %6.3f and weight %-3s",
                    elem.tag,
                    score,
                    weight,
                )
                elem.drop_tree()
            elif elem.text_content().count(",") < 10:
                to_remove = True
                counts = {
                    kind: len(elem.findall(f".//{kind}")) for kind in TEXT_CLEAN_ELEMS
                }
                counts["li"] -= 100
                counts["input"] -= len(elem.findall('.//input[@type="hidden"]'))

                # Count the text length excluding any surrounding whitespace
                content_length = text_length(elem)
                link_density = self.get_link_density(elem)
                parent_node = elem.getparent()
                if parent_node is not None:
                    score = (
                        candidates[parent_node].score
                        if parent_node in candidates
                        else 0
                    )
                # if elem.tag == 'div' and counts["img"] >= 1:
                #    continue
                if counts["p"] and counts["img"] > 1 + counts["p"] * 1.3:
                    reason = f'too many images ({counts["img"]})'
                elif counts["li"] > counts["p"] and elem.tag not in LIST_TAGS:
                    reason = "more <li>s than <p>s"
                elif counts["input"] > (counts["p"] / 3):
                    reason = "less than 3x <p>s than <input>s"
                elif content_length < self.min_text_length and counts["img"] == 0:
                    reason = f"too short content length {content_length} without a single image"
                elif content_length < self.min_text_length and counts["img"] > 2:
                    reason = (
                        f"too short content length {content_length} and too many images"
                    )
                elif weight < 25 and link_density > 0.2:
                    reason = (
                        f"too many links {link_density:.3f} for its weight {weight}"
                    )
                elif weight >= 25 and link_density > 0.5:
                    reason = (
                        f"too many links {link_density:.3f} for its weight {weight}"
                    )
                elif (counts["embed"] == 1 and content_length < 75) or counts[
                    "embed"
                ] > 1:
                    reason = (
                        "<embed>s with too short content length, or too many <embed>s"
                    )
                elif not content_length:
                    reason = "no content"

                    # find x non empty preceding and succeeding siblings
                    siblings = []
                    for sib in elem.itersiblings():
                        sib_content_length = text_length(sib)
                        if sib_content_length:
                            siblings.append(sib_content_length)
                            # if len(siblings) >= 1:
                            break
                    limit = len(siblings) + 1
                    for sib in elem.itersiblings(preceding=True):
                        sib_content_length = text_length(sib)
                        if sib_content_length:
                            siblings.append(sib_content_length)
                            if len(siblings) >= limit:
                                break
                    if siblings and sum(siblings) > 1000:
                        to_remove = False
                        allowed.update(elem.iter("table", "ul", "div", "section"))
                else:
                    to_remove = False

                if to_remove:
                    elem.drop_tree()
                    LOGGER.debug(
                        "Removed %6.3f %s with weight %s cause it has %s.",
                        score,
                        elem.tag,
                        weight,
                        reason or "",
                    )

        self.doc = node
        return _tostring(self.doc)



# Port of isProbablyReaderable from mozilla/readability.js to Python.
# https://github.com/mozilla/readability
# License of forked code: Apache-2.0.

REGEXPS = {
    "unlikelyCandidates": re.compile(
        r"-ad-|ai2html|banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|footer|gdpr|header|legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote",
        re.I,
    ),
    "okMaybeItsACandidate": re.compile(
        r"and|article|body|column|content|main|shadow", re.I
    ),
}

DISPLAY_NONE = re.compile(r"display:\s*none", re.I)


def is_node_visible(node: HtmlElement) -> bool:
    """
    Checks if the node is visible by considering style, attributes, and class.
    """

    if "style" in node.attrib and DISPLAY_NONE.search(node.get("style", "")):
        return False
    if "hidden" in node.attrib:
        return False
    if node.get("aria-hidden") == "true" and "fallback-image" not in node.get(
        "class", ""
    ):
        return False
    return True


def is_probably_readerable(html: HtmlElement, options: Any={}) -> bool:
    """
    Decides whether or not the document is reader-able without parsing the whole thing.
    """
    doc = load_html(html)
    if doc is None:
        return False

    min_content_length = options.get("min_content_length", 140)
    min_score = options.get("min_score", 20)
    visibility_checker = options.get("visibility_checker", is_node_visible)

    nodes = set(doc.xpath(".//p | .//pre | .//article"))
    nodes.update(node.getparent() for node in doc.xpath(".//div/br"))

    score = 0.0
    for node in nodes:
        if not visibility_checker(node):
            continue

        class_and_id = f"{node.get('class', '')} {node.get('id', '')}"
        if REGEXPS["unlikelyCandidates"].search(class_and_id) and not REGEXPS[
            "okMaybeItsACandidate"
        ].search(class_and_id):
            continue

        if node.xpath("./parent::li/p"):
            continue

        text_content_length = len(node.text_content().strip())
        if text_content_length < min_content_length:
            continue

        score += sqrt(text_content_length - min_content_length)
        if score > min_score:
            return True

    return False
