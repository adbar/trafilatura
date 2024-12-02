# pylint:disable-msg=E0611,I1101
"""
Functions grounding on third-party software.
"""

import logging

from typing import Any, Tuple

# third-party
from justext.core import ParagraphMaker, classify_paragraphs, revise_paragraph_classification  # type: ignore
from justext.utils import get_stoplist, get_stoplists  # type: ignore
from lxml.etree import _Element, Element, strip_tags, tostring
from lxml.html import HtmlElement

# own
from .baseline import basic_cleaning
from .htmlprocessing import convert_tags, prune_unwanted_nodes, tree_cleaning
from .readability_lxml import Document as ReadabilityDocument  # fork
from .settings import JUSTEXT_LANGUAGES
from .utils import fromstring_bytes, trim
from .xml import TEI_VALID_TAGS
from .xpaths import OVERALL_DISCARD_XPATH

LOGGER = logging.getLogger(__name__)

JT_STOPLIST = None

SANITIZED_XPATH = './/aside|.//audio|.//button|.//fieldset|.//figure|.//footer|.//iframe|.//input|.//label|.//link|.//nav|.//noindex|.//noscript|.//object|.//option|.//select|.//source|.//svg|.//time'


def try_readability(htmlinput: HtmlElement) -> HtmlElement:
    '''Safety net: try with the generic algorithm readability'''
    # defaults: min_text_length=25, retry_length=250
    try:
        doc = ReadabilityDocument(htmlinput, min_text_length=25, retry_length=250)
        # force conversion to utf-8 (see #319)
        summary = fromstring_bytes(doc.summary())
        return summary if summary is not None else HtmlElement()
    except Exception as err:
        LOGGER.warning('readability_lxml failed: %s', err)
        return HtmlElement()


def compare_extraction(tree: HtmlElement, backup_tree: HtmlElement, body: _Element, text: str, len_text: int, options: Any) -> Tuple[_Element, str, int]:
    '''Decide whether to choose own or external extraction
       based on a series of heuristics'''
    # bypass for recall
    if options.focus == "recall" and len_text > options.min_extracted_size * 10:
        return body, text, len_text

    use_readability, jt_result = False, False
    # prior cleaning
    if options.focus == "precision":
        backup_tree = prune_unwanted_nodes(backup_tree, OVERALL_DISCARD_XPATH)

    # try with readability
    temppost_algo = try_readability(backup_tree)
    # unicode fix necessary on certain systems (#331)
    algo_text = trim(tostring(temppost_algo, method='text', encoding='utf-8').decode('utf-8'))
    len_algo = len(algo_text)

    # compare
    LOGGER.debug('extracted length: %s (algorithm) %s (extraction)', len_algo, len_text)
    # conditions to use alternative algorithms
    if len_algo in (0, len_text):
        use_readability = False
    elif len_text == 0 and len_algo > 0:
        use_readability = True
    elif len_text > 2 * len_algo:
        use_readability = False
    # quick fix for https://github.com/adbar/trafilatura/issues/632
    elif len_algo > 2 * len_text and not algo_text.startswith("{"):
        use_readability = True
    # borderline cases
    elif not body.xpath('.//p//text()') and len_algo > options.min_extracted_size * 2:
        use_readability = True
    elif len(body.findall('.//table')) > len(body.findall('.//p')) and len_algo > options.min_extracted_size * 2:
        use_readability = True
    # https://github.com/adbar/trafilatura/issues/354
    elif options.focus == "recall" and not body.xpath('.//head') and temppost_algo.xpath('.//h2|.//h3|.//h4') and len_algo > len_text:
        use_readability = True
    else:
        LOGGER.debug('extraction values: %s %s for %s', len_text, len_algo, options.source)
        use_readability = False

    # apply decision
    if use_readability:
        body, text, len_text = temppost_algo, algo_text, len_algo
        LOGGER.debug('using generic algorithm: %s', options.source)
    else:
        LOGGER.debug('using custom extraction: %s', options.source)

    # override faulty extraction: try with justext
    if body.xpath(SANITIZED_XPATH) or len_text < options.min_extracted_size:  # body.find(...)
        LOGGER.debug('unclean document triggering justext examination: %s', options.source)
        body2, text2, len_text2 = justext_rescue(tree, options)
        jt_result = bool(text2)
        # prevent too short documents from replacing the main text
        if text2 and not len_text > 4*len_text2:  # threshold could be adjusted
            LOGGER.debug('using justext, length: %s', len_text2)
            body, text, len_text = body2, text2, len_text2

    # post-processing: remove unwanted sections
    if use_readability and not jt_result:
        body, text, len_text = sanitize_tree(body, options)  # type: ignore[arg-type]

    return body, text, len_text


def jt_stoplist_init() -> Tuple[str]:
    'Retrieve and return the content of all JusText stoplists'
    global JT_STOPLIST
    stoplist = set()
    for language in get_stoplists():
        stoplist.update(get_stoplist(language))
    JT_STOPLIST = tuple(stoplist)
    return JT_STOPLIST


def custom_justext(tree: HtmlElement, stoplist: Tuple[str]) -> Any:
    'Customized version of JusText processing'
    paragraphs = ParagraphMaker.make_paragraphs(tree)
    classify_paragraphs(paragraphs, stoplist, 50, 150, 0.1, 0.2, 0.25, True)
    revise_paragraph_classification(paragraphs, 150)
    return paragraphs


def try_justext(tree: HtmlElement, url: str, target_language: str) -> _Element:
    '''Second safety net: try with the generic algorithm justext'''
    # init
    result_body = Element('body')
    # determine language
    if target_language in JUSTEXT_LANGUAGES:
        justext_stoplist = get_stoplist(JUSTEXT_LANGUAGES[target_language])
    else:
        justext_stoplist = JT_STOPLIST or jt_stoplist_init()
    # extract
    try:
        paragraphs = custom_justext(tree, justext_stoplist)
    except Exception as err:
        LOGGER.error('justext %s %s', err, url)
    else:
        for paragraph in paragraphs:
            if paragraph.is_boilerplate:
                continue
            #if duplicate_test(paragraph) is not True:
            elem, elem.text = Element('p'), paragraph.text
            result_body.append(elem)
    return result_body


def justext_rescue(tree: HtmlElement, options: Any) -> Tuple[_Element, str, int]:
    '''Try to use justext algorithm as a second fallback'''
    # additional cleaning
    tree = basic_cleaning(tree)
    # proceed
    temppost_algo = try_justext(tree, options.url, options.lang)
    temp_text = trim(' '.join(temppost_algo.itertext()))
    return temppost_algo, temp_text, len(temp_text)


def sanitize_tree(tree: HtmlElement, options: Any) -> Tuple[HtmlElement, str, int]:
    '''Convert and sanitize the output from the generic algorithm (post-processing)'''
    # 1. clean
    cleaned_tree = tree_cleaning(tree, options)
    if options.links is False:
        strip_tags(cleaned_tree, 'a')
    strip_tags(cleaned_tree, 'span')
    # 2. convert
    cleaned_tree = convert_tags(cleaned_tree, options)
    for elem in cleaned_tree.iter('td', 'th', 'tr'):
        # elem.text, elem.tail = trim(elem.text), trim(elem.tail)
        # finish table conversion
        if elem.tag == 'tr':
            elem.tag = 'row'
        elif elem.tag in ('td', 'th'):
            if elem.tag == 'th':
                elem.set('role', 'head')
            elem.tag = 'cell'
    # 3. sanitize
    sanitization_list = [
        tagname
        for tagname in [element.tag for element in set(cleaned_tree.iter('*'))]
        if tagname not in TEI_VALID_TAGS
    ]
    strip_tags(cleaned_tree, *sanitization_list)
    # 4. return
    text = trim(' '.join(cleaned_tree.itertext()))
    return cleaned_tree, text, len(text)
