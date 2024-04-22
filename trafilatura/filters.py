"""
Functions related to content filtering, mostly duplicate detection and language
detection.
"""

import logging
import re

# language detection
try:
    import py3langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

from .lru import LRUCache
from .settings import LRU_SIZE
from .utils import trim

LOGGER = logging.getLogger(__name__)

LRU_TEST = LRUCache(maxsize=LRU_SIZE)

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Language
TARGET_LANG_ATTRS = ('http-equiv="content-language"', 'property="og:locale"')
RE_HTML_LANG = re.compile(r'([a-z]{2})')

# Mostly filters for social media
RE_FILTER = re.compile(r'\W*(Drucken|E-?Mail|Facebook|Flipboard|Google|Instagram|'
                        'Linkedin|Mail|PDF|Pinterest|Pocket|Print|QQ|Reddit|Twitter|'
                        'WeChat|WeiBo|Whatsapp|Xing|Mehr zum Thema:?|More on this.{,8}$)$',
                       flags=re.IGNORECASE)
# COMMENTS_BLACKLIST = ('( Abmelden / Ändern )') # Fill in your details below|Trage deine Daten unten|Kommentar verfassen|Bitte logge dich|Hinterlasse einen Kommentar| to %s| mit %s)


def put_in_cache(teststring):
    '''Implement LRU cache'''
    cacheval = LRU_TEST.get(teststring)
    # if the value is already defined
    value = cacheval + 1 if cacheval != -1 else 1
    LRU_TEST.put(teststring, value)


def duplicate_test(element, options):
    '''Check for duplicate text with LRU cache'''
    teststring = trim(' '.join(element.itertext()))
    # teststring = element.text
    if len(teststring) > options.min_duplcheck_size:
        # retrieve value from cache
        cacheval = LRU_TEST.get(teststring)
        if cacheval > options.max_repetitions:  # non-existent key will return -1
            LRU_TEST.put(teststring, cacheval + 1)
            return True
    put_in_cache(teststring)
    return False


def check_html_lang(tree, target_language, strict=False):
    """Check HTML meta-elements for language information and split
       the result in case there are several languages."""
    for attr in TARGET_LANG_ATTRS:
        elems = tree.findall(f'.//meta[@{attr}][@content]')
        if elems:
            if any(target_language in RE_HTML_LANG.split(elem.get("content", "").lower()) for elem in elems):
                return True
            LOGGER.debug("%s lang attr failed", attr)
            return False

    # HTML lang attribute: sometimes a wrong indication
    if strict:
        elems = tree.xpath("//html[@lang]")
        if elems:
            if any(target_language in RE_HTML_LANG.split(elem.get("lang", "").lower()) for elem in elems):
                return True
            LOGGER.debug("HTML lang failed")
            return False

    LOGGER.debug("No relevant lang elements found")
    return True


def language_classifier(temp_text, temp_comments):
    '''Run external component (if installed) for language identification'''
    if LANGID_FLAG is True:
        result, _ = (
            py3langid.classify(temp_text)
            if len(temp_text) > len(temp_comments)
            else py3langid.classify(temp_comments)
        )
    else:
        LOGGER.warning('Language detector not installed, skipping detection')
        result = None
    return result


def language_filter(temp_text, temp_comments, target_language, docmeta):
    '''Filter text based on language detection and store relevant information'''
    # todo: run and pass info along anyway?
    if target_language is not None:
        # more thorough: detection on actual text content
        docmeta.language = language_classifier(temp_text, temp_comments)
        # HTML lang check? sometimes contradicted by detection above
        #if docmeta.language is None:
        #    if check_html_lang(tree, target_language) is False:
        #        LOGGER.error('wrong HTML meta language for URL %s', url)
        #        raise ValueError
        if docmeta.language is not None and docmeta.language != target_language:
            LOGGER.warning('wrong language: %s %s', docmeta.language, docmeta.url)
            return True, docmeta
    return False, docmeta


def textfilter(element):
    '''Filter out unwanted text'''
    testtext = element.tail if element.text is None else element.text
    # to check: line len → continue if len(line) <= 5
    return not text_chars_test(testtext) or any(map(RE_FILTER.match, testtext.splitlines()))


def text_chars_test(string):
    '''Determine if a string is only composed of spaces and/or control characters'''
    # or not re.search(r'\w', string)
    # return string is not None and len(string) != 0 and not string.isspace()
    return bool(string) and not string.isspace()
