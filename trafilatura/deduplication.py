"Code parts dedicated to duplicate removal and text similarity."

import re
import string
import unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
from hashlib import blake2b
from operator import add
from threading import RLock
from typing import Any

from lxml.etree import _Element

from .settings import LRU_SIZE, Extractor
from .utils import trim

STRIP_EXTENSION = re.compile(r"\.[^/?#]{2,63}$")

BIN_COUNT_FUNC = getattr(int, "bit_count", lambda x: bin(x).count("1"))

PUNCT_TBL = str.maketrans({i: " " for i in range(0x10FFFF) if unicodedata.category(chr(i))[0] == "P"})


@lru_cache(maxsize=1024)
def is_similar_domain(reference: str, new_string: str, threshold: float = 0.5) -> bool:
    "Return the similarity ratio between two short strings, here domain names."
    reference = STRIP_EXTENSION.sub("", reference)
    new_string = STRIP_EXTENSION.sub("", new_string)
    return SequenceMatcher(None, reference, new_string).ratio() >= threshold


def _get_sample_by_length(tokens: list[str], target_length: int) -> list[str]:
    """Helper function to get a sample of tokens based on length criteria."""
    sample = []
    for i in range(4, -1, -1):
        sample = [t for t in tokens if len(t) > i]
        if len(sample) >= target_length / 2:
            return sample
    return sample


def sample_tokens_fallback(inputstring: str, length: int = 64) -> list[str]:
    """
    This fallback implementation is used when the primary sample_tokens function
    generates an empty token list. This is mostly relevant for languages like
    mandarin where none latin-based punctuation is used e.g.: 。
    """
    # Replace all punctuation with spaces using translation table
    clean_text = inputstring.translate(PUNCT_TBL)
    tokens = [t for t in clean_text.split() if t.isalnum()]
    return _get_sample_by_length(tokens, length)


def sample_tokens(inputstring: str, length: int = 64) -> list[str]:
    """Split input into list of tokens and adjust length threshold to make sure
    there is enough data."""
    tokens = []
    for token in inputstring.split():
        token = token.strip(string.punctuation)
        if token.isalnum():
            tokens.append(token)

    sample = _get_sample_by_length(tokens, length)

    if len(sample) == 0:
        return sample_tokens_fallback(inputstring, length)

    return sample


def generate_bow_hash(inputstring: str, length: int = 24) -> bytes:
    "Create a bag of words and generate a hash for a given string."
    teststring = " ".join(sample_tokens(inputstring)).strip()
    # perform hashing with limited size
    return blake2b(teststring.encode(), digest_size=length).digest()


@lru_cache(maxsize=2**14)
def _vector_to_add(token: str, length: int) -> list[int]:
    "Token's contribution to a Simhash vector, cached across all instances."
    token_hash = int.from_bytes(blake2b(token.encode(), digest_size=8).digest(), "big")
    return [1 if token_hash & (1 << i) else -1 for i in range(length)]


class Simhash:
    "Implement a basic Charikar hashing approach of string similarity."

    __slots__ = ["hash", "length"]

    def __init__(
        self,
        inputstring: str = "",
        length: int = 64,
        existing_hash: str | None = None,
    ) -> None:
        "Store length and existing or new hash."
        self.length = length
        self.hash = self.validate(existing_hash) or self.create_hash(inputstring)

    def create_hash(self, inputstring: str) -> int:
        """Calculates a Charikar simhash. References used:
        https://github.com/vilda/shash/
        https://github.com/sean-public/python-hashes/blob/master/hashes/simhash.py
        Optimized for Python by @adbar.
        """
        vector = [0] * self.length

        for token in sample_tokens(inputstring, self.length):
            vector = list(map(add, vector, _vector_to_add(token, self.length)))

        return sum(1 << i for i in range(self.length) if vector[i] >= 0)

    def to_hex(self) -> str:
        "Convert the numerical hash to a hexadecimal string."
        return hex(self.hash)[2:]

    def _hash_to_int(self, inputhash: str) -> int | None:
        "Convert the hexadecimal hash to a numerical value."
        try:
            return int(inputhash, 16)
        except (TypeError, ValueError):
            return None

    def validate(self, inputhash: int | str | None) -> int | None:
        "Validate the input hash and return it, or None otherwise."
        if isinstance(inputhash, int) and 18 <= len(str(inputhash)) <= 22:
            return inputhash
        if isinstance(inputhash, str):
            if inputhash.isdigit() and 18 <= len(inputhash) <= 22:
                return int(inputhash)
            # possibly a hex string
            return self._hash_to_int(inputhash)
        return None

    def hamming_distance(self, other_hash: "Simhash") -> int:
        "Return distance between two hashes of equal length using the XOR operator."
        return BIN_COUNT_FUNC(self.hash ^ other_hash.hash)

    def similarity(self, other_hash: "Simhash") -> float:
        """Calculate how similar this hash is from another simhash.
        Returns a float from 0.0 to 1.0.
        """
        return (self.length - self.hamming_distance(other_hash)) / self.length


def content_fingerprint(content: str) -> str:
    "Calculate a simhash hex value for meaningful bits of the content."
    return Simhash(content).to_hex()


PREV, NEXT, KEY, RESULT = 0, 1, 2, 3  # names for the link fields


class LRUCache:
    """
    Pure-Python Least Recently Used (LRU) cache using a circular doubly linked list
    Adapted from CPython functools.py lru_cache decorator implementation
    https://github.com/python/cpython/blob/3.9/Lib/functools.py#L524
    First adapted by https://github.com/vbarbaresi
    """

    def __init__(self, maxsize: int = 128) -> None:
        # Constants shared by all lru cache instances:
        self.lock = RLock()  # because linkedlist updates aren't threadsafe
        # cache instance variables
        self.maxsize = maxsize
        self.cache: dict[str, list[Any]] = {}
        self.root: list[Any] = []  # root of the circular doubly linked list
        # initialize by pointing to self
        self.root[:] = [self.root, self.root, None, None]
        self.full = False

    def _move_link(self, link: Any) -> Any:
        # Move the link to the front of the circular queue
        link_prev, link_next, _key, result = link
        link_prev[NEXT], link_next[PREV] = link_next, link_prev
        last = self.root[PREV]
        last[NEXT] = self.root[PREV] = link
        link[PREV] = last
        link[NEXT] = self.root
        return result

    def get(self, key: Any) -> Any:
        """Tests if the key that is asked for is in the cache
        and retrieve its value from the linked list."""
        with self.lock:
            link = self.cache.get(key)
            if link:
                return self._move_link(link)
        return -1

    def put(self, key: str, value: Any) -> None:
        "Stores a given key in the cache."
        # Size limited caching that tracks accesses by recency
        with self.lock:
            link = self.cache.get(key)
            if link:
                self._move_link(link)
                self.cache[key][RESULT] = value
            else:
                if self.full:
                    # Use the old root to store the new key and result.
                    oldroot = self.root
                    oldroot[KEY], oldroot[RESULT] = key, value
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
                    self.full = len(self.cache) >= self.maxsize

    def clear(self) -> None:
        "Delete all cache content."
        with self.lock:
            self.cache.clear()
            self.root[:] = [self.root, self.root, None, None]
            self.full = False


LRU_TEST = LRUCache(maxsize=LRU_SIZE)


def put_in_cache(teststring: str) -> None:
    "Implement LRU cache."
    cacheval = LRU_TEST.get(teststring)
    # if the value is already defined
    value = cacheval + 1 if cacheval != -1 else 1
    LRU_TEST.put(teststring, value)


def duplicate_test(element: _Element, options: Extractor) -> bool:
    "Check for duplicate text with LRU cache."
    teststring = trim(" ".join(element.itertext()))
    # teststring = element.text
    if len(teststring) > options.min_duplcheck_size:
        # retrieve value from cache
        cacheval = LRU_TEST.get(teststring)
        if cacheval > options.max_repetitions:  # non-existent key will return -1
            LRU_TEST.put(teststring, cacheval + 1)
            return True
    put_in_cache(teststring)
    return False
