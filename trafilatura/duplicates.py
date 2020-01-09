"""
Module bundling functions related to duplicate detection.
"""

import logging

from .lru import LRUCache
from .settings import LRU_SIZE, MIN_DUPLCHECK_SIZE


LOGGER = logging.getLogger(__name__)
LRU_TEST = LRUCache(maxsize=LRU_SIZE)


def put_in_cache(body):
    '''Implement LRU cache'''
    global LRU_TEST
    for element in body:
        try:
            teststring = ' '.join(element.itertext())
        except AttributeError:  # justext Paragraph
            teststring = element.text
        if teststring in LRU_TEST.cache:
            val = LRU_TEST.get(teststring)
            # print(val, teststring[:10] + '...')
            LRU_TEST.put(teststring, val + 1)
        else:
            # print(0, teststring[:10] + '...')
            LRU_TEST.put(teststring, 1)


def duplicate_test(element):
    '''Check for duplicate text'''
    global LRU_TEST
    try:
        teststring = ' '.join(element.itertext())
    except AttributeError:  # justext Paragraph
        teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        # key in self.cache
        if LRU_TEST.has_key(teststring) is True and LRU_TEST.get(teststring) > 2:
            # LRU_TEST[teststring] += 1
            return True
    return False


def test_body_cache(postbody):
    teststring = ' '.join(postbody.itertext()).encode('utf-8')
    if LRU_TEST.has_key(teststring) is True:
        # LRU_TEST[teststring] = 1
        return True
    return False
