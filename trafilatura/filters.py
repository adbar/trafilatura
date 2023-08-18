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
    if cacheval != -1:
        # print(cacheval, teststring[:10] + '...')
        LRU_TEST.put(teststring, cacheval + 1)
    else:
        # print(0, teststring[:10] + '...')
        LRU_TEST.put(teststring, 1)


def duplicate_test(element, config):
    '''Check for duplicate text with LRU cache'''
    teststring = trim(' '.join(element.itertext()))
    # teststring = element.text
    if len(teststring) > config.getint('DEFAULT', 'MIN_DUPLCHECK_SIZE'):
        # retrieve value from cache
        cacheval = LRU_TEST.get(teststring)
        if cacheval > config.getint('DEFAULT', 'MAX_REPETITIONS'):  # non-existent key will return -1
            LRU_TEST.put(teststring, cacheval + 1)
            return True
    put_in_cache(teststring)
    return False


def check_html_lang(tree, target_language, strict=False):
    '''Check HTML meta-elements for language information and split
       the result in case there are several languages'''
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Language
    target_elements = tree.findall('.//meta[@http-equiv="content-language"][@content]')
    if target_elements:
        for elem in target_elements:
            if target_language in RE_HTML_LANG.split(elem.get('content').lower()):
                return True
        LOGGER.debug('HTML content-language failed')
        return False
    # locale
    target_elements = tree.findall('.//meta[@property="og:locale"][@content]')
    if target_elements:
        for elem in target_elements:
            if target_language in RE_HTML_LANG.split(elem.get('content').lower()):
                return True
        LOGGER.debug('HTML og:locale failed')
        return False
    # HTML lang attribute: sometimes a wrong indication
    if strict is True:
        target_elements = tree.xpath('//html[@lang]')
        if target_elements:
            for elem in target_elements:
                if target_language in RE_HTML_LANG.split(elem.get('lang').lower()):
                    return True
            LOGGER.debug('HTML lang failed')
            return False
    LOGGER.debug('No relevant lang elements found')
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
    # print('#', element.text)
    if element.text is None and element.tail is not None:
        testtext = element.tail
    else:
        testtext = element.text
    if text_chars_test(testtext) is False:
        return True
    # to check: line len → continue if len(line) <= 5
    return any(RE_FILTER.match(line) for line in testtext.splitlines())


def text_chars_test(string):
    '''Determine if a string is only composed of spaces and/or control characters'''
    # or not re.search(r'\w', string)
    # return string is not None and len(string) != 0 and not string.isspace()
    return string not in (None, '') and not string.isspace()
