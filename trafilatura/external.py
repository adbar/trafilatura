# pylint:disable-msg=I1101
"""
Functions grounding on third-party software.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import logging
import os

try:
    from contextlib import redirect_stderr
    MUFFLE_FLAG = True
except ImportError:
    MUFFLE_FLAG = False


# third-party
from lxml import etree, html
from readability import Document
from readability.readability import Unparseable

# try this option
try:
    import justext
    JT_STOPLIST = set()
    for language in justext.get_stoplists():
        JT_STOPLIST.update(justext.get_stoplist(language))
except ImportError:
    justext = JT_STOPLIST = None

# own
from .htmlprocessing import convert_tags, prune_html
from .settings import JUSTEXT_LANGUAGES
from .utils import sanitize, trim, HTML_PARSER
from .xml import TEI_VALID_TAGS


LOGGER = logging.getLogger(__name__)


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
        if MUFFLE_FLAG is False:
            resultstring = doc.summary(html_partial=True)
        else:
            with open(os.devnull, 'w') as devnull:
                with redirect_stderr(devnull):
                    resultstring = doc.summary(html_partial=True)
        newtree = html.fromstring(resultstring, parser=HTML_PARSER)
        return newtree
    except (etree.SerialisationError, Unparseable):
        return etree.Element('div')


# bypass parsing
#def my_bypass(html_tree, default_encoding, encoding, enc_errors):
#    return html_tree
#if justext:
#    justext.html_to_dom = my_bypass


def try_justext(tree, url, target_language):
    '''Second safety net: try with the generic algorithm justext'''
    result_body = etree.Element('body')
    justtextstring = html.tostring(tree, pretty_print=False, encoding='utf-8')
    # determine language
    if target_language is not None and target_language in JUSTEXT_LANGUAGES:
        langsetting = JUSTEXT_LANGUAGES[target_language]
        justext_stoplist = justext.get_stoplist(langsetting)
    else:
        #justext_stoplist = justext.get_stoplist(JUSTEXT_DEFAULT)
        justext_stoplist = JT_STOPLIST
    # extract
    try:
        paragraphs = justext.justext(justtextstring, justext_stoplist, 50, 200, 0.1, 0.2, 0.2, 200, True)
    except ValueError as err:  # not an XML element: HtmlComment
        LOGGER.error('justext %s %s', err, url)
        result_body = None
    else:
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                #if duplicate_test(paragraph) is not True:
                elem = etree.Element('p')
                elem.text = paragraph.text
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


def convert_tree(tree):
    '''Convert the output from the generic algorithm'''
    tree = prune_html(tree)
    cleaned_tree = convert_tags(tree)
    # cleaned_tree = manual_cleaning(cleaned_tree, True)
    # cleaned_tree = HTML_CLEANER.clean_html(cleaned_tree)
    for elem in cleaned_tree.iter():
        #if elem.tag in ('code', 'del', 'head', 'hi', 'item', 'p', 'quote'):
        #    if elem.text is None or elem.text.isspace():
        #        elem.getparent().remove(elem)
        #        continue
        #if elem.text:
        elem.text = sanitize(elem.text)
        #if elem.tail:
        elem.tail = sanitize(elem.tail)
        # remove attributes
        if elem.tag != 'del' or elem.tag != 'hi':
            elem.attrib.clear()
        # finish table conversion
        if elem.tag == 'tr':
            elem.tag = 'row'
        elif elem.tag == 'td' or elem.tag == 'th':
            elem.tag = 'cell'
            if elem.tag == 'th':
                elem.set('role', 'head')
    return cleaned_tree


def sanitize_tree(tree):
    '''Sanitize the output from the generic algorithm (post-processing)'''
    #for elem in tree.xpath('//aside|//audio|//button|//fieldset|//figure|//footer|//iframe|//img|//input|//label|//link|//nav|//noindex|//noscript|//object|//option|//select|//source|//svg|//time'):
    #    elem.getparent().remove(elem)
    etree.strip_elements(tree, 'aside', 'audio', 'button', 'fieldset', 'figure', 'footer', 'iframe', 'image', 'img', 'input', 'label', 'nav', 'noindex', 'noscript', 'object', 'option', 'select', 'source', 'svg', 'time')
    for tagname in [element.tag for element in set(tree.iter())]:
        if tagname not in TEI_VALID_TAGS:
            etree.strip_tags(tree, tagname)
    text = trim(' '.join(tree.itertext()))
    return tree, text, len(text)
