# pylint:disable-msg=I1101
"""
Functions grounding on third-party software.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import logging

# third-party
from justext.core import classify_paragraphs, ParagraphMaker, preprocessor, revise_paragraph_classification
from justext.utils import get_stoplist, get_stoplists

from lxml.etree import Element, strip_tags
from lxml.html import fromstring


# own
from .htmlprocessing import convert_tags, prune_unwanted_nodes, tree_cleaning
from .readability_lxml import Document as ReadabilityDocument  # fork
from .settings import JUSTEXT_LANGUAGES
from .utils import trim, HTML_PARSER
from .xml import TEI_VALID_TAGS
from .xpaths import PAYWALL_DISCARD_XPATH, REMOVE_COMMENTS_XPATH


LOGGER = logging.getLogger(__name__)

SANITIZED_XPATH = '//aside|//audio|//button|//fieldset|//figure|//footer|//iframe|//input|//label|//link|//nav|//noindex|//noscript|//object|//option|//select|//source|//svg|//time'


def try_readability(htmlinput):
    '''Safety net: try with the generic algorithm readability'''
    # defaults: min_text_length=25, retry_length=250
    try:
        doc = ReadabilityDocument(htmlinput, min_text_length=25, retry_length=250)
        return fromstring(doc.summary(), parser=HTML_PARSER)
    except Exception as err:
        LOGGER.warning('readability_lxml failed: %s', err)
        return Element('div')


def jt_stoplist_init():
    'Retrieve and return the content of all JusText stoplists'
    stoplist = set()
    for language in get_stoplists():
        stoplist.update(get_stoplist(language))
    return tuple(stoplist)

JT_STOPLIST = jt_stoplist_init()


def custom_justext(tree, stoplist):
    'Customized version of JusText processing'
    dom = preprocessor(tree)  # tree_cleaning(tree, True)
    paragraphs = ParagraphMaker.make_paragraphs(dom)
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
        justext_stoplist = JT_STOPLIST
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


def justext_rescue(tree, url, target_language, postbody, len_text, text):
    '''Try to use justext algorithm as a second fallback'''
    result_bool = False
    # additional cleaning
    tree = prune_unwanted_nodes(tree, PAYWALL_DISCARD_XPATH)
    tree = prune_unwanted_nodes(tree, REMOVE_COMMENTS_XPATH)
    # proceed
    temppost_algo = try_justext(tree, url, target_language)
    if temppost_algo is not None:
        temp_text = trim(' '.join(temppost_algo.itertext()))
        len_algo = len(temp_text)
        if len_algo > len_text:
            postbody, text, len_text = temppost_algo, temp_text, len_algo
            result_bool = True
    return postbody, text, len_text, result_bool


def sanitize_tree(tree, include_formatting=False, include_links=False, include_images=False, include_tables=True):
    '''Convert and sanitize the output from the generic algorithm (post-processing)'''
    # 1. clean
    cleaned_tree = tree_cleaning(tree, include_tables, include_images)
    for elem in tree.xpath(SANITIZED_XPATH):
        elem.getparent().remove(elem)
    if include_links is False:
        strip_tags(cleaned_tree, 'a')
    strip_tags(cleaned_tree, 'span')
    # 2. convert
    cleaned_tree = convert_tags(cleaned_tree, include_tables=include_tables, include_formatting=include_formatting, include_links=include_links, include_images=include_images)
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
