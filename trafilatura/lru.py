"""
Pure-Python Least Recently Used (LRU) cache using a circular doubly linked list
Adapted from CPython functools.py lru_cache decorator implementation
https://github.com/python/cpython/blob/3.9/Lib/functools.py#L524
First adapted by https://github.com/vbarbaresi
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


from threading import RLock

PREV, NEXT, KEY, RESULT = 0, 1, 2, 3  # names for the link fields


class LRUCache:
    '''Implements a class for the Least Recently Used (LRU) cache'''

    def __init__(self, maxsize=128):
        # Constants shared by all lru cache instances:
        self.lock = RLock()  # because linkedlist updates aren't threadsafe
        # cache instance variables
        self.maxsize = maxsize
        self.cache = {}
        self.root = []  # root of the circular doubly linked list
        # initialize by pointing to self
        self.root[:] = [self.root, self.root, None, None]
        self.full = False

    def _move_link(self, link):
        # Move the link to the front of the circular queue
        link_prev, link_next, _key, result = link
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev
        last = self.root[PREV]
        last[NEXT] = self.root[PREV] = link
        link[PREV] = last
        link[NEXT] = self.root
        return result

    def get(self, key):
        '''Tests if the key that is asked for is in the cache
           and retrieve its value from the linked list'''
        with self.lock:
            link = self.cache.get(key)
            if link is not None:
                result = self._move_link(link)
                return result
        return -1

    def put(self, key, value):
        '''Stores a given key in the cache'''
        # Size limited caching that tracks accesses by recency
        with self.lock:
            link = self.cache.get(key)
            if link is not None:
                self._move_link(link)
                self.cache[key][RESULT] = value
                return
        with self.lock:
            if self.full:
                # Use the old root to store the new key and result.
                oldroot = self.root
                oldroot[KEY] = key
                oldroot[RESULT] = value
                # Empty the oldest link and make it the new root.
                # Keep a reference to the old key and old result to
                # prevent their ref counts from going to zero during the
                # update. That will prevent potentially arbitrary object
                # clean-up code (i.e. __del__) from running while we're
                # still adjusting the links.
                self.root = oldroot[NEXT]
                oldkey = self.root[KEY]
                self.root[KEY] = self.root[RESULT] = None
                # Now update the cache dictionary.
                del self.cache[oldkey]
                # Save the potentially reentrant cache[key] assignment
                # for last, after the root and links have been put in
                # a consistent state.
                self.cache[key] = oldroot
            else:
                # Put result in a new link at the front of the queue.
                last = self.root[PREV]
                link = [last, self.root, key, value]
                last[NEXT] = self.root[PREV] = self.cache[key] = link
                # Use the cache_len bound method instead of the len() function
                # which could potentially be wrapped in an lru_cache itself.
                self.full = (len(self.cache) >= self.maxsize)

    def clear(self):
        '''Delete all cache content'''
        with self.lock:
            self.cache.clear()
            self.root[:] = [self.root, self.root, None, None]
            self.full = False
