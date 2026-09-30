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
from collections import Counter
from dataclasses import dataclass
from math import sqrt
from operator import attrgetter
from typing import Any

from .dom import HtmlElement, fragment_fromstring, tostring
from .utils import load_html, trim

LOGGER = logging.getLogger(__name__)


DOT_SPACE = re.compile(r"\.( |$)")


TAG_SCORES = {
    **dict.fromkeys(("div", "article"), 5),
    **dict.fromkeys(("pre", "td", "blockquote"), 3),
    **dict.fromkeys(("address", "ol", "ul", "dl", "dd", "dt", "li", "form", "aside"), -3),
    **dict.fromkeys(("h1", "h2", "h3", "h4", "h5", "h6", "th", "header", "footer", "nav"), -5),
}

TEXT_CLEAN_ELEMS = {"p", "img", "li", "a", "embed", "input"}

REGEXES = {
    # matched against lowercased attributes
    "unlikelyCandidatesRe": re.compile(
        r"combx|comment|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|pagination|pager|popup|tweet|twitter"
    ),
    "okMaybeItsACandidateRe": re.compile(r"and|article|body|column|content|main|shadow"),
    "positiveRe": re.compile(
        r"article|body|content|entry|hentry|main|page|pagination|post|text|blog|story",
        re.IGNORECASE,
    ),
    "negativeRe": re.compile(
        r"button|combx|comment|com-|contact|figure|foot|footer|footnote|form|input|masthead|media|meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|shopping|tags|tool|widget",
        re.IGNORECASE,
    ),
    "videoRe": re.compile(r"https?:\/\/(?:www\.)?(?:youtube|vimeo)\.com", re.IGNORECASE),
}

# block tag prefixes that keep a div from becoming a <p>, anchors are inline
DIV_TO_P_PREFIXES = ("address", "article", "aside", "audio", "blockquote", "dl", "div", "img", "ol", "p", "table", "ul")

FRAME_TAGS = {"body", "html"}
LIST_TAGS = {"ol", "ul"}


def text_length(elem: HtmlElement) -> int:
    "Return the length of the element with all its contents."
    return len(trim(elem.text_content()))


@dataclass(slots=True, eq=False)
class Candidate:
    "Defines a class to score candidate elements."

    score: float
    elem: HtmlElement


class Document:
    """Class to build a etree document out of html."""

    __slots__ = ["doc", "min_text_length"]

    def __init__(self, doc: HtmlElement, min_text_length: int = 25) -> None:
        """Generate the document

        :param doc: parsed HTML tree.
        :param min_text_length: Set to a higher value for more precise detection of longer texts.

        The Document class is not re-enterable.
        It is designed to create a new Document() for each HTML file to process it.

        API method:
        .summary() -- cleaned up content
        """
        self.doc = doc
        self.min_text_length = min_text_length

    def summary(self) -> str:
        """
        Given a HTML file, extracts the text of the article.

        Warning: It mutates internal DOM representation of the HTML document,
        so it is better to call other API methods before this one.
        """
        for elem in list(self.doc.iter("script", "style", "fencedframe")):
            elem.drop_tree()

        # no retry: it would rerun on the same mutated tree
        self.remove_unlikely_candidates()
        self.transform_misused_divs_into_paragraphs()
        candidates = self.score_paragraphs()
        best_candidate = self.select_best_candidate(candidates)
        if best_candidate:
            article = self.get_article(candidates, best_candidate)
        else:
            LOGGER.debug("No candidate found, returning raw html")
            body = self.doc.find("body")
            article = body if body is not None else self.doc
        return self.sanitize(article, candidates)

    def get_article(self, candidates: dict[HtmlElement, Candidate], best_candidate: Candidate) -> HtmlElement:
        # Now that we have the top candidate, look through its siblings for
        # content that might also be related.
        # Things like preambles, content split by ads that we removed, etc.
        sibling_score_threshold = max(10, best_candidate.score * 0.2)
        # create a new html document with a div
        output = fragment_fromstring("<div/>")
        parent = best_candidate.elem.getparent()
        siblings = list(parent) if parent is not None else [best_candidate.elem]
        for sibling in siblings:
            append = False
            # conditions
            if sibling == best_candidate.elem or (
                sibling in candidates and candidates[sibling].score >= sibling_score_threshold
            ):
                append = True
            elif sibling.tag == "p":
                link_density = self.get_link_density(sibling)
                node_content = sibling.text or ""
                node_length = len(node_content)

                if (node_length > 80 and link_density < 0.25) or (
                    node_length <= 80 and link_density == 0 and DOT_SPACE.search(node_content)
                ):
                    append = True
            # append to the output div
            if append:
                output.append(sibling)
        return output

    def select_best_candidate(self, candidates: dict[HtmlElement, Candidate]) -> Candidate | None:
        return max(candidates.values(), key=attrgetter("score"), default=None)

    def get_link_density(self, elem: HtmlElement) -> float:
        total_length = text_length(elem) or 1
        link_length = sum(text_length(link) for link in elem.findall(".//a"))
        return link_length / total_length

    def score_paragraphs(self) -> dict[HtmlElement, Candidate]:
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
        return Candidate(self.class_weight(elem) + TAG_SCORES.get(str(elem.tag).lower(), 0), elem)

    def remove_unlikely_candidates(self) -> None:
        verdicts: dict[str, bool] = {}
        for elem in self.doc.findall(".//*"):
            attrs = " ".join(filter(None, (elem.get("class"), elem.get("id"))))
            if len(attrs) < 2 or elem.tag in FRAME_TAGS:
                continue
            if attrs not in verdicts:
                low = attrs.lower()
                verdicts[attrs] = bool(REGEXES["unlikelyCandidatesRe"].search(low)) and not REGEXES[
                    "okMaybeItsACandidateRe"
                ].search(low)
            if verdicts[attrs]:
                elem.drop_tree()

    def transform_misused_divs_into_paragraphs(self) -> None:
        for elem in self.doc.findall(".//div"):
            # a div without block descendants becomes a <p>, a link wrapper only if it has loose text
            if not any(str(e.tag).startswith(DIV_TO_P_PREFIXES) for e in elem.iterdescendants("*")) and (
                elem.find(".//a") is None or elem.xpath("text()[normalize-space()]")
            ):
                elem.tag = "p"

        for elem in self.doc.findall(".//div"):
            if elem.text and elem.text.strip():
                p_elem = fragment_fromstring("<p/>")
                p_elem.text, elem.text = elem.text, None
                elem.insert(0, p_elem)

            for pos, child in reversed(list(enumerate(elem))):
                if child.tail and child.tail.strip():
                    p_elem = fragment_fromstring("<p/>")
                    p_elem.text, child.tail = child.tail, None
                    elem.insert(pos + 1, p_elem)
                if child.tag == "br":
                    child.drop_tree()

    def sanitize(self, node: HtmlElement, candidates: dict[HtmlElement, Candidate]) -> str:
        for header in list(node.iter("h1", "h2", "h3", "h4", "h5", "h6")):
            if self.class_weight(header) < 0 or self.get_link_density(header) > 0.33:
                header.drop_tree()

        for elem in list(node.iter("form", "textarea")):
            elem.drop_tree()

        for elem in list(node.iter("iframe")):
            if "src" in elem.attrib and REGEXES["videoRe"].search(elem.attrib["src"]):
                elem.text = "VIDEO"  # ADD content to iframe text node to force <iframe></iframe> proper output
            else:
                elem.drop_tree()

        # Conditionally clean <table>s, <ul>s, and <div>s
        for elem in reversed(list(node.iter("table", "ul", "div", "aside", "header", "footer", "section"))):
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
                counts = Counter(e.tag for e in elem.iterdescendants(*TEXT_CLEAN_ELEMS))
                counts["li"] -= 100
                counts["input"] -= len(elem.findall('.//input[@type="hidden"]'))

                # Count the text length excluding any surrounding whitespace
                content_length = text_length(elem)
                link_density = self.get_link_density(elem)
                if counts["p"] and counts["img"] > 1 + counts["p"] * 1.3:
                    reason = f"too many images ({counts['img']})"
                elif counts["li"] > counts["p"] and elem.tag not in LIST_TAGS:
                    reason = "more <li>s than <p>s"
                elif counts["input"] > (counts["p"] / 3):
                    reason = "less than 3x <p>s than <input>s"
                elif content_length < self.min_text_length and counts["img"] == 0:
                    reason = f"too short content length {content_length} without a single image"
                elif content_length < self.min_text_length and counts["img"] > 2:
                    reason = f"too short content length {content_length} and too many images"
                elif link_density > (0.5 if weight >= 25 else 0.2):
                    reason = f"too many links {link_density:.3f} for its weight {weight}"
                elif (counts["embed"] == 1 and content_length < 75) or counts["embed"] > 1:
                    reason = "<embed>s with too short content length, or too many <embed>s"
                elif not content_length:
                    reason = "no content"
                    # kept between long neighbours: the nearest non-empty sibling on each side
                    nearest = (
                        next((n for sib in sibs if (n := text_length(sib))), 0)
                        for sibs in (elem.itersiblings(), elem.itersiblings(preceding=True))
                    )
                    to_remove = sum(nearest) <= 1000
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

        return tostring(node, encoding=str, method="xml")


# Port of isProbablyReaderable from mozilla/readability.js to Python.
# https://github.com/mozilla/readability
# License of forked code: Apache-2.0.

REGEXPS = {
    "unlikelyCandidates": re.compile(
        r"-ad-|ai2html|banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|footer|gdpr|header|legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote"
    ),
}

DISPLAY_NONE = re.compile(r"display:\s*none", re.IGNORECASE)


def is_node_visible(node: HtmlElement) -> bool:
    """
    Checks if the node is visible by considering style, attributes, and class.
    """

    if "style" in node.attrib and DISPLAY_NONE.search(node.get("style", "")):
        return False
    if "hidden" in node.attrib:
        return False
    if node.get("aria-hidden") == "true" and "fallback-image" not in node.get("class", ""):
        return False
    return True


def is_probably_readerable(html: HtmlElement, options: dict[str, Any] | None = None) -> bool:
    """
    Decides whether or not the document is reader-able without parsing the whole thing.
    """
    options = options or {}
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

        class_and_id = f"{node.get('class', '')} {node.get('id', '')}".lower()
        if REGEXPS["unlikelyCandidates"].search(class_and_id) and not REGEXES["okMaybeItsACandidateRe"].search(class_and_id):
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
