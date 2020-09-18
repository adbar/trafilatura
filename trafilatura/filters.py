"""
Functions related to content filtering, mostly duplicate detection and language
detection.
"""

import logging
import re

# language detection
try:
    import cld3
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

from .lru import LRUCache
from .settings import LRU_SIZE, MAX_REPETITIONS, MIN_DUPLCHECK_SIZE
from .utils import remove_control_characters, trim


LOGGER = logging.getLogger(__name__)

LRU_TEST = LRUCache(maxsize=LRU_SIZE)

RE_FILTER = re.compile(r'\W*(Drucken|E-?Mail|Facebook|Flipboard|Google|Instagram|Linkedin|Mail|PDF|Pinterest|Pocket|Print|Reddit|Twitter|Whatsapp|Xing)$', flags=re.IGNORECASE)
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


def duplicate_test(element):
    '''Check for duplicate text with LRU cache'''
    teststring = trim(' '.join(element.itertext()))
    # teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        # retrieve value from cache
        cacheval = LRU_TEST.get(teststring)
        if cacheval > MAX_REPETITIONS:  # non-existent key will return -1
            LRU_TEST.put(teststring, cacheval + 1)
            return True
    put_in_cache(teststring)
    return False


def language_filter(temp_text, temp_comments, target_language, docmeta):
    '''Run external component (if installed) for language identification'''
    # sanity check on language
    if target_language is not None:
        if LANGID_FLAG is True:
            # comments
            if len(temp_comments) > len(temp_text):
                langtest = temp_comments
            # default
            else:
                langtest = temp_text
            result = cld3.get_language(langtest)
            if result.language != target_language:
                LOGGER.warning('wrong language: %s %s %s', result, docmeta['id'], docmeta['url'])
                return True
        else:
            LOGGER.warning('Detector not installed, no language detection run')
    return False


def textfilter(element):
    '''Filter out unwanted text'''
    # print('#', element.text)
    if element.text is None and element.tail is not None:
        testtext = element.tail
    else:
        testtext = element.text
    if text_chars_test(testtext) is False:
        return True
    for line in testtext.splitlines():
        #if len(line) <= 5:
        #    continue
        if RE_FILTER.match(line):
            return True
    return False


def text_chars_test(string):
    '''Determine if a string is only composed of spaces and/or control characters'''
    if string is None or string.isspace():  # or remove_control_characters(string).isspace():
        return False
    return True
