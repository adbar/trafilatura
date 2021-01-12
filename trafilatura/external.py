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

from lxml import etree, html
from readability import Document
from readability.readability import Unparseable

# own
from .htmlprocessing import convert_tags, prune_html  #, tree_cleaning
from .settings import JUSTEXT_LANGUAGES, MANUALLY_STRIPPED
from .utils import trim, HTML_PARSER
from .xml import TEI_VALID_TAGS


LOGGER = logging.getLogger(__name__)

SANITIZED_XPATH = '//aside|//audio|//button|//fieldset|//figure|//footer|//iframe|//img|//image|//input|//label|//link|//nav|//noindex|//noscript|//object|//option|//select|//source|//svg|//time'
SANITIZED_XPATH_WITH_IMAGES = '//aside|//audio|//button|//fieldset|//figure|//footer|//iframe|//input|//label|//link|//nav|//noindex|//noscript|//object|//option|//select|//source|//svg|//time'


def jt_stoplist_init():
    'Retrieve and return the content of all JusText stoplists'
    stoplist = set()
    for language in get_stoplists():
        stoplist.update(get_stoplist(language))
    return stoplist

JT_STOPLIST = jt_stoplist_init()


class LXMLDocument(Document):
    '''Sub-class of readability.Document accepting parsed trees as input'''
    def __init__(self, input_, *args, **kwargs):
        super().__init__(input_)

    def _parse(self, input_):
        return input_


def try_readability(htmlinput, url):
    '''Safety net: try with the generic algorithm readability'''
    # defaults: min_text_length=25, retry_length=250
    try:
        doc = LXMLDocument(htmlinput, url=url, min_text_length=25, retry_length=250)
        return html.fromstring(doc.summary(html_partial=True), parser=HTML_PARSER)
    except (etree.SerialisationError, Unparseable):
        return etree.Element('div')


def custom_justext(tree, stoplist):
    'Customized version of JusText processing'
    dom = preprocessor(tree) # tree_cleaning(tree, True)
    paragraphs = ParagraphMaker.make_paragraphs(dom)
    classify_paragraphs(paragraphs, stoplist, 50, 200, 0.1, 0.2, 0.2, True)
    revise_paragraph_classification(paragraphs, 200)
    return paragraphs


def try_justext(tree, url, target_language):
    '''Second safety net: try with the generic algorithm justext'''
    result_body = etree.Element('body')
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
            elem, elem.text = etree.Element('p'), paragraph.text
            result_body.append(elem)
    return result_body


def justext_rescue(tree, url, target_language, postbody, len_text, text):
    '''Try to use justext algorithm as a second fallback'''
    result_bool = False
    temppost_algo = try_justext(tree, url, target_language)
    if temppost_algo is not None:
        temp_text = trim(' '.join(temppost_algo.itertext()))
        len_algo = len(temp_text)
        if len_algo > len_text:
            postbody, text, len_text = temppost_algo, temp_text, len_algo
            result_bool = True
    return postbody, text, len_text, result_bool


def sanitize_tree(tree, include_formatting=False, include_links=False, include_images=False):
    '''Convert and sanitize the output from the generic algorithm (post-processing)'''
    if include_images is False:
        sanitized_xpath = SANITIZED_XPATH
    else:
        sanitized_xpath = SANITIZED_XPATH_WITH_IMAGES
    # delete unnecessary elements
    for elem in tree.xpath(sanitized_xpath):
        elem.getparent().remove(elem)
    # handle links
    if include_links is True:
       stripped_list = MANUALLY_STRIPPED + ['span']
    else:
       stripped_list = MANUALLY_STRIPPED + ['a', 'span']
    etree.strip_tags(tree, stripped_list)
    tree = prune_html(tree)
    # convert
    cleaned_tree = convert_tags(tree, include_formatting, include_links, include_images)
    for elem in cleaned_tree.iter('td', 'th', 'tr'):
        # elem.text, elem.tail = trim(elem.text), trim(elem.tail)
        # finish table conversion
        if elem.tag == 'tr':
            elem.tag = 'row'
        elif elem.tag in ('td', 'th'):
            if elem.tag == 'th':
                elem.set('role', 'head')
            elem.tag = 'cell'
    # sanitize
    sanitization_list = list()
    for tagname in [element.tag for element in set(cleaned_tree.iter())]:
        if tagname not in TEI_VALID_TAGS:
            sanitization_list.append(tagname)
        #    if tagname in ('article', 'content', 'link', 'main', 'section', 'span'):
        #        for element in cleaned_tree.iter(tagname):
        #            merge_with_parent(element)
        #    else:
        #    print(tagname)
    etree.strip_tags(cleaned_tree, sanitization_list)
    text = trim(' '.join(cleaned_tree.itertext()))
    return cleaned_tree, text, len(text)
