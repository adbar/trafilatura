"""
Module bundling functions related to duplicate detection.
"""

from .lru import LRUCache
from .settings import LRU_SIZE, MAX_REPETITIONS, MIN_DUPLCHECK_SIZE

LRU_TEST = LRUCache(maxsize=LRU_SIZE)


def put_in_cache(body):
    '''Implement LRU cache'''
    global LRU_TEST
    for element in body:
        try:
            teststring = ' '.join(element.itertext())
        except AttributeError:  # justext Paragraph
            teststring = element.text
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
    # global LRU_TEST
    try:
        teststring = ' '.join(element.itertext())
    except AttributeError:  # justext Paragraph
        teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        # retrieve value from cache
        cacheval = LRU_TEST.get(teststring)
        if cacheval > MAX_REPETITIONS:  # non-existent key will return -1
            # LRU_TEST[teststring] += 1
            return True
    return False


#def test_body_cache(postbody):
#    '''Convenience fonction to check document body as a whole'''
#    teststring = ' '.join(postbody.itertext())
#    if LRU_TEST.has_key(teststring) is True:
#        # LRU_TEST[teststring] = 1
#        return True
#    return False
