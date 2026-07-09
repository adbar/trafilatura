# pylint:disable-msg=E0611,I1101
"""
Functions grounding on third-party software.
"""

import logging
from typing import Any

# third-party
from justext.core import ParagraphMaker, classify_paragraphs, revise_paragraph_classification
from justext.utils import get_stoplist, get_stoplists
from lxml.etree import Element, _Element, strip_tags, tostring
from lxml.html import HtmlElement

# own
from .baseline import basic_cleaning
from .htmlprocessing import convert_tags, prune_unwanted_nodes, tree_cleaning
from .readability_lxml import Document as ReadabilityDocument  # fork
from .settings import JUSTEXT_LANGUAGES, Extractor
from .utils import fromstring_bytes, trim
from .xml import TEI_VALID_TAGS
from .xpaths import OVERALL_DISCARD_XPATH

LOGGER = logging.getLogger(__name__)

JT_STOPLIST = None

SANITIZED_XPATH = ".//aside|.//audio|.//button|.//fencedframe|.//fieldset|.//figure|.//footer|.//iframe|.//input|.//label|.//link|.//nav|.//noindex|.//noscript|.//object|.//option|.//select|.//source|.//svg|.//time"

# adopt justext only when the text it replaces is at most this much longer (swept 2-4: every
# (3, 4]-band page was justext wrongly replacing a longer, closer-to-target extraction)
JUSTEXT_OVERRIDE_RATIO = 3


def try_readability(htmlinput: HtmlElement) -> HtmlElement:
    """Safety net: try with the generic algorithm readability"""
    # defaults: min_text_length=25, retry_length=250
    try:
        doc = ReadabilityDocument(htmlinput, min_text_length=25, retry_length=250)
        # force conversion to utf-8 (see #319)
        summary = fromstring_bytes(doc.summary())
        return summary if summary is not None else HtmlElement()
    except Exception as err:
        LOGGER.warning("readability_lxml failed: %s", err)
        return HtmlElement()


def _prefer_readability(
    body: _Element, algo_body: HtmlElement, algo_text: str, len_text: int, len_algo: int, options: Extractor
) -> bool:
    """Decide whether the readability output should replace the own extraction."""
    # readability empty, or same length as the own extraction (assumed same content)
    if len_algo in (0, len_text):
        return False
    # own extraction much longer
    if len_text > 2 * len_algo:
        return False
    return (
        # own text empty
        len_text == 0
        # readability much longer, unless it grabbed raw JSON (#632)
        or (len_algo > 2 * len_text and not algo_text.startswith("{"))
        # own extraction structurally deficient: no paragraph text or table-dominated
        or (
            len_algo > options.min_extracted_size * 2
            and (not body.xpath(".//p//text()") or len(body.findall(".//table")) > len(body.findall(".//p")))
        )
        # recall mode: readability output substantially longer
        or (options.focus == "recall" and len_algo > 1.5 * len_text and not algo_text.startswith("{"))
        # recall mode: readability recovers a headed article (#354)
        or (
            options.focus == "recall"
            and not body.xpath(".//head")
            and algo_body.xpath(".//h2|.//h3|.//h4")
            and len_algo > len_text
        )
    )


def compare_extraction(
    tree: HtmlElement, backup_tree: HtmlElement, body: _Element, text: str, len_text: int, options: Extractor
) -> tuple[_Element, str, int]:
    """Decide whether to choose own or external extraction
    based on a series of heuristics"""
    # bypass for recall
    if options.focus == "recall" and len_text > options.min_extracted_size * 10:
        return body, text, len_text

    jt_result = False
    # prior cleaning
    if options.focus == "precision":
        backup_tree = prune_unwanted_nodes(backup_tree, OVERALL_DISCARD_XPATH)

    # try with readability
    temppost_algo = try_readability(backup_tree)
    # unicode fix necessary on certain systems (#331)
    algo_text = trim(tostring(temppost_algo, method="text", encoding="utf-8").decode("utf-8"))
    len_algo = len(algo_text)
    LOGGER.debug("extracted length: %s (algorithm) %s (extraction)", len_algo, len_text)

    use_readability = _prefer_readability(body, temppost_algo, algo_text, len_text, len_algo, options)
    if use_readability:
        body, text, len_text = temppost_algo, algo_text, len_algo
    LOGGER.debug("using %s extraction: %s", "generic" if use_readability else "custom", options.source)

    # override faulty extraction: try with justext
    if body.xpath(SANITIZED_XPATH) or len_text < options.min_extracted_size:
        LOGGER.debug("unclean document triggering justext examination: %s", options.source)
        body2, text2, len_text2 = justext_rescue(tree, options)
        # prevent too short documents from replacing the main text
        if text2 and len_text <= JUSTEXT_OVERRIDE_RATIO * len_text2:
            LOGGER.debug("using justext, length: %s", len_text2)
            body, text, len_text = body2, text2, len_text2
            jt_result = True

    # post-processing: remove unwanted sections
    if use_readability and not jt_result:
        body, text, len_text = sanitize_tree(body, options)  # type: ignore[arg-type]

    return body, text, len_text


def jt_stoplist_init() -> tuple[str]:
    "Retrieve and return the content of all JusText stoplists"
    global JT_STOPLIST
    stoplist = set()
    for language in get_stoplists():
        stoplist.update(get_stoplist(language))
    JT_STOPLIST = tuple(stoplist)
    return JT_STOPLIST


def custom_justext(tree: HtmlElement, stoplist: tuple[str]) -> Any:
    "Customized version of JusText processing"
    paragraphs = ParagraphMaker.make_paragraphs(tree)
    classify_paragraphs(paragraphs, stoplist, 50, 150, 0.1, 0.2, 0.25, True)
    revise_paragraph_classification(paragraphs, 150)
    return paragraphs


def try_justext(tree: HtmlElement, url: str | None, target_language: str | None) -> _Element:
    """Second safety net: try with the generic algorithm justext"""
    # init
    result_body = Element("body")
    # determine language
    if target_language in JUSTEXT_LANGUAGES:
        justext_stoplist = get_stoplist(JUSTEXT_LANGUAGES[target_language])
    else:
        justext_stoplist = JT_STOPLIST or jt_stoplist_init()
    # extract
    try:
        paragraphs = custom_justext(tree, justext_stoplist)
    except Exception as err:
        LOGGER.error("justext %s %s", err, url)
    else:
        for paragraph in paragraphs:
            if paragraph.is_boilerplate:
                continue
            # if duplicate_test(paragraph) is not True:
            elem, elem.text = Element("p"), paragraph.text
            result_body.append(elem)
    return result_body


def justext_rescue(tree: HtmlElement, options: Extractor) -> tuple[_Element, str, int]:
    """Try to use justext algorithm as a second fallback"""
    # additional cleaning
    tree = basic_cleaning(tree)
    # proceed
    temppost_algo = try_justext(tree, options.url, options.lang)
    temp_text = trim(" ".join(temppost_algo.itertext()))
    return temppost_algo, temp_text, len(temp_text)


def sanitize_tree(tree: HtmlElement, options: Extractor) -> tuple[HtmlElement, str, int]:
    """Convert and sanitize the output from the generic algorithm (post-processing)"""
    # 1. clean
    cleaned_tree = tree_cleaning(tree, options)
    if options.links is False:
        strip_tags(cleaned_tree, "a")
    strip_tags(cleaned_tree, "span")
    # 2. convert (pass url so relative links are absolutized on the fallback path)
    cleaned_tree = convert_tags(cleaned_tree, options, options.url)
    # Mark first <th>-containing row per parent group as head (mirrors handle_table logic).
    # Groups by direct parent (the enclosing table once tbody/thead/tfoot are stripped upstream);
    # nested tables form their own group.
    seen_group_elems: set[_Element | None] = set()
    for tr in cleaned_tree.iter("tr"):
        parent = tr.getparent()
        if parent not in seen_group_elems and any(c.tag == "th" for c in tr):
            seen_group_elems.add(parent)
            for c in tr:
                if c.tag == "th":
                    c.set("role", "head")
    for elem in cleaned_tree.iter("td", "th", "tr"):
        if elem.tag == "tr":
            elem.tag = "row"
        elif elem.tag in ("td", "th"):
            elem.tag = "cell"
    # 3. sanitize
    sanitization_list = [
        tagname for tagname in [element.tag for element in set(cleaned_tree.iter("*"))] if tagname not in TEI_VALID_TAGS
    ]
    strip_tags(cleaned_tree, *sanitization_list)  # type: ignore[arg-type]
    # 4. return
    text = trim(" ".join(cleaned_tree.itertext()))
    return cleaned_tree, text, len(text)
