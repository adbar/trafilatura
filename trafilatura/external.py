# pylint:disable-msg=E0611,I1101
"""
Functions grounding on third-party software.
"""

import logging
import lzma
from pathlib import Path
from pickle import load as load_pickle

# third-party
from justext.core import (ParagraphMaker, classify_paragraphs,
                          revise_paragraph_classification)
from justext.utils import get_stoplist  # , get_stoplists
from lxml.etree import Element, strip_tags, tostring

# own
from .htmlprocessing import convert_tags, prune_unwanted_nodes, tree_cleaning
from .readability_lxml import Document as ReadabilityDocument  # fork
from .settings import JUSTEXT_LANGUAGES
from .utils import fromstring_bytes, trim
from .xml import TEI_VALID_TAGS
from .xpaths import OVERALL_DISCARD_XPATH, PAYWALL_DISCARD_XPATH, REMOVE_COMMENTS_XPATH

LOGGER = logging.getLogger(__name__)

JT_STOPLIST = None
JT_PICKLE = str(Path(__file__).parent / 'data/jt-stopwords-pickle.lzma')

SANITIZED_XPATH = './/aside|.//audio|.//button|.//fieldset|.//figure|.//footer|.//iframe|.//input|.//label|.//link|.//nav|.//noindex|.//noscript|.//object|.//option|.//select|.//source|.//svg|.//time'


def try_readability(htmlinput):
    '''Safety net: try with the generic algorithm readability'''
    # defaults: min_text_length=25, retry_length=250
    try:
        doc = ReadabilityDocument(htmlinput, min_text_length=25, retry_length=250)
        # force conversion to utf-8 (see #319)
        return fromstring_bytes(doc.summary())
    except Exception as err:
        LOGGER.warning('readability_lxml failed: %s', err)
        return Element('div')


def compare_extraction(tree, backup_tree, body, text, len_text, options):
    '''Decide whether to choose own or external extraction
       based on a series of heuristics'''
    # bypass for recall
    if options.focus == "recall" and len_text > options.min_extracted_size * 10:
        return body, text, len_text
    algo_flag, jt_result = False, False
    # prior cleaning
    backup_tree = prune_unwanted_nodes(backup_tree, PAYWALL_DISCARD_XPATH)
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
        algo_flag = False
    elif len_text == 0 and len_algo > 0:
        algo_flag = True
    elif len_text > 2 * len_algo:
        algo_flag = False
    elif len_algo > 2 * len_text:
        algo_flag = True
    # borderline cases
    elif not body.xpath('.//p//text()') and len_algo > options.min_extracted_size * 2:
        algo_flag = True
    elif len(body.findall('.//table')) > len(body.findall('.//p')) and len_algo > options.min_extracted_size * 2:
        algo_flag = True
    # https://github.com/adbar/trafilatura/issues/354
    elif options.focus == "recall" and not body.xpath('.//head') and temppost_algo.xpath('.//h2|.//h3|.//h4') and len_algo > len_text:
        algo_flag = True
    else:
        LOGGER.debug('extraction values: %s %s for %s', len_text, len_algo, options.source)
        algo_flag = False
    # apply decision
    if algo_flag:
        body, text, len_text = temppost_algo, algo_text, len_algo
        LOGGER.debug('using generic algorithm: %s', options.source)
    else:
        LOGGER.debug('using custom extraction: %s', options.source)
    # override faulty extraction: try with justext
    if body.xpath(SANITIZED_XPATH) or len_text < options.min_extracted_size:  # body.find(...)
        LOGGER.debug('unclean document triggering justext examination: %s', options.source)
        # tree = prune_unwanted_sections(tree, {}, options)
        body2, text2, len_text2, jt_result = justext_rescue(tree, options, body, 0, '')
        # prevent too short documents from replacing the main text
        if jt_result is True and not len_text > 4*len_text2:  # threshold could be adjusted
            LOGGER.debug('using justext, length: %s', len_text2)
            body, text, len_text = body2, text2, len_text2
    # post-processing: remove unwanted sections
    if algo_flag is True and jt_result is False:
        body, text, len_text = sanitize_tree(body, options)
    return body, text, len_text


def jt_stoplist_init():
    'Retrieve and return the content of all JusText stoplists'
    global JT_STOPLIST
    with lzma.open(JT_PICKLE, 'rb') as picklefile:
        JT_STOPLIST = load_pickle(picklefile)
    # stoplist = set()
    # for language in get_stoplists():
    #     stoplist.update(get_stoplist(language))
    # JT_STOPLIST = tuple(stoplist)
    return JT_STOPLIST


def custom_justext(tree, stoplist):
    'Customized version of JusText processing'
    paragraphs = ParagraphMaker.make_paragraphs(tree)
    classify_paragraphs(paragraphs, stoplist, 50, 200, 0.1, 0.2, 0.2, True)
    revise_paragraph_classification(paragraphs, 200)
    return paragraphs


def try_justext(tree, url, target_language):
    '''Second safety net: try with the generic algorithm justext'''
    # init
    result_body = Element('body')
    # determine language
    if target_language is not None and target_language in JUSTEXT_LANGUAGES:
        justext_stoplist = get_stoplist(JUSTEXT_LANGUAGES[target_language])
    else:
        justext_stoplist = JT_STOPLIST or jt_stoplist_init()
    # extract
    try:
        paragraphs = custom_justext(tree, justext_stoplist)
    except ValueError as err:  # not an XML element: HtmlComment
        LOGGER.error('justext %s %s', err, url)
        result_body = None
    else:
        for paragraph in [p for p in paragraphs if not p.is_boilerplate]:
            #if duplicate_test(paragraph) is not True:
            elem, elem.text = Element('p'), paragraph.text
            result_body.append(elem)
    return result_body


def justext_rescue(tree, options, postbody, len_text, text):
    '''Try to use justext algorithm as a second fallback'''
    result_bool = False
    # additional cleaning
    tree = prune_unwanted_nodes(tree, PAYWALL_DISCARD_XPATH)
    tree = prune_unwanted_nodes(tree, REMOVE_COMMENTS_XPATH)
    # proceed
    temppost_algo = try_justext(tree, options.url, options.lang)
    if temppost_algo is not None:
        temp_text = trim(' '.join(temppost_algo.itertext()))
        len_algo = len(temp_text)
        if len_algo > len_text:
            postbody, text, len_text = temppost_algo, temp_text, len_algo
            result_bool = True
    return postbody, text, len_text, result_bool


def sanitize_tree(tree, options):
    '''Convert and sanitize the output from the generic algorithm (post-processing)'''
    # 1. clean
    cleaned_tree = tree_cleaning(tree, options)
    for elem in tree.findall(SANITIZED_XPATH):
        elem.getparent().remove(elem)
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
