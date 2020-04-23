"""
Functions related to content filtering, mostly duplicate detection and language
detection.
"""

import logging
import re

# language detection
try:
    import langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

from .lru import LRUCache
from .settings import (DETECTION_LANGUAGES, LRU_SIZE,
                       MAX_REPETITIONS, MIN_DUPLCHECK_SIZE)
from .utils import trim


LOGGER = logging.getLogger(__name__)

LRU_TEST = LRUCache(maxsize=LRU_SIZE)

if LANGID_FLAG is True:
    langid.set_languages(DETECTION_LANGUAGES)

RE_FILTER = re.compile(r'\W*(Drucken|E-Mail|Facebook|Google|Instagram|Linkedin|PDF|Pinterest|Twitter|Whatsapp|Xing)$', flags=re.IGNORECASE)
# RE_FILTER_2 = re.compile(r'\W*(Tags: [A-ZÄÖÜßa-zäöü ,]+|.hnliche Beitr|Gef.llt mir|[Ss]hare (on|via)|Fill in your details below|Trage deine Daten unten|Kommentar verfassen|Bitte logge dich|Hinterlasse einen Kommentar| to %s| mit %s)')
# COMMENTS_BLACKLIST = ('( Abmelden / Ändern )')


def put_in_cache(body):
    '''Implement LRU cache'''
    global LRU_TEST
    for element in body:
        teststring = trim(' '.join(element.itertext()))
        cacheval = LRU_TEST.get(teststring)
        # if the value is already defined
        if cacheval != -1:
            # print(cacheval, teststring[:10] + '...')
            LRU_TEST.put(teststring, cacheval + 1)
        else:
            # print(0, teststring[:10] + '...')
            LRU_TEST.put(teststring, 1)


def duplicate_test(element):
    '''Check for duplicate text'''
    try:
        teststring = trim(' '.join(element.itertext()))
    except AttributeError:  # justext Paragraph
        teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        # retrieve value from cache
        cacheval = LRU_TEST.get(teststring)
        if cacheval > MAX_REPETITIONS:  # non-existent key will return -1
            # LRU_TEST[teststring] += 1
            return True
    return False


def language_filter(temp_text, temp_comments, target_language, record_id, url):
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
            langresult = langid.classify(langtest)
            if langresult[0] != target_language:
                LOGGER.warning('wrong language: %s %s %s', langresult, record_id, url)
                LOGGER.debug('wrong language: %s %s', langresult, temp_text)
                return True
        else:
            LOGGER.warning('langid not installed, no language detection run')
    return False


def textfilter(element):
    '''Filter out unwanted text'''
    # print('#', element.text)
    if element.text is None and element.tail is not None:
        testtext = element.tail
    else:
        testtext = element.text
    if testtext.isspace():
        return True
    for line in testtext.splitlines():
        #if len(line) <= 5:
        #    continue
        if RE_FILTER.match(line): # or RE_FILTER_2.search(line):
            return True
    return False
