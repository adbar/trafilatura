"Code parts dedicated to duplicate removal and text similarity."

import re
import string
import unicodedata
from collections import OrderedDict
from difflib import SequenceMatcher
from functools import cache, lru_cache
from hashlib import blake2b
from operator import add
from threading import RLock
from typing import Any

from lxml.etree import _Element

from .dom import HtmlElement
from .settings import LRU_SIZE, Extractor
from .utils import trim

STRIP_EXTENSION = re.compile(r"\.[^/?#]{2,63}$")


@cache
def _punct_tbl() -> dict[int, str]:
    "Punctuation translation table, built lazily: scans all of Unicode (~90ms)."
    return str.maketrans({i: " " for i in range(0x10FFFF) if unicodedata.category(chr(i))[0] == "P"})


@lru_cache(maxsize=1024)
def is_similar_domain(reference: str, new_string: str, threshold: float = 0.5) -> bool:
    "Return the similarity ratio between two short strings, here domain names."
    reference = STRIP_EXTENSION.sub("", reference)
    new_string = STRIP_EXTENSION.sub("", new_string)
    return SequenceMatcher(None, reference, new_string).ratio() >= threshold


def sample_tokens(inputstring: str, length: int = 64) -> list[str]:
    """Split input into list of tokens and adjust length threshold to make sure
    there is enough data."""
    tokens = []
    for token in inputstring.split():
        token = token.strip(string.punctuation)
        if token.isalnum():
            tokens.append(token)

    if not tokens:
        # non-latin punctuation, e.g. mandarin 。
        tokens = [t for t in inputstring.translate(_punct_tbl()).split() if t.isalnum()]

    # tokens are non-empty, so a threshold of 0 would keep them all
    for i in range(4, 0, -1):
        sample = [t for t in tokens if len(t) > i]
        if len(sample) >= length / 2:
            return sample
    return tokens


def generate_bow_hash(inputstring: str, length: int = 24) -> bytes:
    "Create a bag of words and generate a hash for a given string."
    teststring = " ".join(sample_tokens(inputstring))
    return blake2b(teststring.encode(), digest_size=length).digest()


@lru_cache(maxsize=2**14)
def _vector_to_add(token: str, length: int) -> list[int]:
    "Token's contribution to a Simhash vector, cached across all instances."
    token_hash = int.from_bytes(blake2b(token.encode(), digest_size=8).digest(), "big")
    return [1 if token_hash & (1 << i) else -1 for i in range(length)]


class Simhash:
    "Implement a basic Charikar hashing approach of string similarity."

    __slots__ = ("hash", "length")

    def __init__(
        self,
        inputstring: str = "",
        length: int = 64,
        existing_hash: int | str | None = None,
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
        return f"{self.hash:x}"

    def validate(self, inputhash: int | str | None) -> int | None:
        "Validate the input hash and return it, or None otherwise."
        if isinstance(inputhash, str):
            # historical decimal representation, now hex via to_hex()
            if inputhash.isdecimal() and 18 <= len(inputhash) <= 22:
                inputhash = int(inputhash)
            else:
                try:
                    inputhash = int(inputhash, 16)
                except ValueError:
                    return None
        if type(inputhash) is int and 0 <= inputhash < (1 << self.length):
            return inputhash
        return None

    def similarity(self, other_hash: "Simhash") -> float:
        "Similarity to another simhash based on the Hamming distance, from 0.0 to 1.0."
        return (self.length - (self.hash ^ other_hash.hash).bit_count()) / self.length


def content_fingerprint(content: str) -> str:
    "Calculate a simhash hex value for meaningful bits of the content."
    return Simhash(content).to_hex()


class LRUCache:
    "Least Recently Used (LRU) cache backed by an OrderedDict."

    def __init__(self, maxsize: int = 128) -> None:
        if maxsize < 1:
            raise ValueError("maxsize must be at least 1")
        self.lock = RLock()
        self.maxsize = maxsize
        self.cache: OrderedDict[str, int] = OrderedDict()

    def __getstate__(self) -> dict[str, Any]:
        # RLock is not picklable, the cache is copied to avoid sharing it
        with self.lock:
            state = self.__dict__.copy()
            state["cache"] = self.cache.copy()
        del state["lock"]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self.lock = RLock()

    def __bool__(self) -> bool:
        "Always true, even when empty: instances passed as dedup option enable deduplication."
        return True

    def get(self, key: str) -> int:
        "Retrieve a value from the cache, or -1 if the key is absent."
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
        return -1

    def put(self, key: str, value: int) -> None:
        "Store a given key in the cache, evicting the oldest entry if full."
        with self.lock:
            self.cache[key] = value
            self.cache.move_to_end(key)
            if len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)

    def increment(self, key: str) -> int:
        "Increment the stored count, return the previous count or -1."
        with self.lock:
            previous = self.cache.pop(key, -1)
            self.put(key, max(previous, 0) + 1)
            return previous

    def clear(self) -> None:
        "Delete all cache content."
        with self.lock:
            self.cache.clear()


LRU_TEST = LRUCache(maxsize=LRU_SIZE)


def duplicate_test(element: _Element | HtmlElement, options: Extractor) -> bool:
    "Check for duplicate text with LRU cache."
    teststring = trim(" ".join(element.itertext()))
    lru = options.dedup if isinstance(options.dedup, LRUCache) else LRU_TEST
    previous = lru.increment(teststring)
    return len(teststring) > options.min_duplcheck_size and previous > options.max_repetitions
