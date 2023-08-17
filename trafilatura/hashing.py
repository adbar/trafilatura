"Parts dedicated to content hashing and text similarity."

import re
import string
from base64 import urlsafe_b64encode
from functools import lru_cache
from hashlib import blake2b
from operator import add
from typing import Any, List, Optional

CLEAN_XML = re.compile(r"<[^<]+?>")


def sample_tokens(inputstring: str, length: int = 64) -> List[str]:
    """Split input into list of tokens and adjust length threshold to make sure
    there is enough data."""
    tokens = []
    for token in inputstring.split():
        token = token.strip(string.punctuation)
        if token.isalnum():
            tokens.append(token)
    sample = []
    for i in range(4, -1, -1):
        sample = [t for t in tokens if len(t) > i]
        if len(sample) >= length / 2:
            return sample
    return sample


def generate_bow_hash(inputstring: str, length: int = 24) -> bytes:
    "Create a bag of words and generate a hash for a given string."
    teststring = " ".join(sample_tokens(inputstring)).strip()
    # perform hashing with limited size
    return blake2b(teststring.encode(), digest_size=length).digest()


def generate_hash_filename(content: str) -> str:
    "Create a filename-safe string by hashing the given content."
    # delete potential XML tags first
    content = CLEAN_XML.sub("", content)
    return urlsafe_b64encode(generate_bow_hash(content, 12)).decode()


class Simhash:
    "Implement a basic Charikar hashing approach of string similarity."
    __slots__ = ["hash", "length"]

    def __init__(
        self,
        inputstring: str = "",
        length: int = 64,
        existing_hash: Optional[str] = None,
    ) -> None:
        "Store length and existing or new hash."
        self.length = length
        self.hash = self.validate(existing_hash) or self.create_hash(inputstring)

    def _hash(self, inputstring: str) -> int:
        "Return a numerical hash of the string."
        return int.from_bytes(
            blake2b(inputstring.encode(), digest_size=8).digest(), "big"
        )
        # old: variable-length version of Python's builtin hash by @sean-public
        # see also Siphash13 in https://peps.python.org/pep-0456/
        # if inputstring == "":
        #    return 0
        # mask = 2**self.length - 1
        # x = ord(inputstring[0]) << 7
        # for c in inputstring:
        #    x = ((x * 1000003) ^ ord(c)) & mask
        # x ^= len(inputstring)
        # if x == -1:
        #    return -2
        # return x

    @lru_cache(maxsize=2**14)
    def _vector_to_add(self, token: str) -> List[int]:
        "Create vector to add to the existing string vector"
        the_hash = self._hash(token)
        return [1 if the_hash & (1 << i) else -1 for i in range(self.length)]

    def create_hash(self, inputstring: str) -> int:
        """Calculates a Charikar simhash. References used:
        https://github.com/vilda/shash/
        https://github.com/sean-public/python-hashes/blob/master/hashes/simhash.py
        Optimized for Python by @adbar.
        """
        vector = [0] * self.length

        for token in sample_tokens(inputstring, self.length):
            vector = list(map(add, vector, self._vector_to_add(token)))

        return sum(1 << i for i in range(self.length) if vector[i] >= 0)

    def to_hex(self) -> str:
        "Convert the numerical hash to a hexadecimal string."
        return hex(self.hash)[2:]

    def _hash_to_int(self, inputhash) -> Optional[int]:
        "Convert the hexadecimal hash to a numerical value."
        try:
            return int(inputhash, 16)
        except (TypeError, ValueError):
            return None

    def validate(self, inputhash: Optional[Any]) -> Optional[int]:
        "Validate the input hash and return it, or None otherwise."
        if isinstance(inputhash, int) and 18 <= len(str(inputhash)) <= 22:
            return inputhash
        if isinstance(inputhash, str):
            if inputhash.isdigit() and 18 <= len(inputhash) <= 22:
                return int(inputhash)
            # possibly a hex string
            return self._hash_to_int(inputhash)
        return None

    def hamming_distance(self, other_hash: Any) -> int:
        "Return distance between two hashes of equal length using the XOR operator."
        xor_result = self.hash ^ other_hash.hash
        try:
            # Python >= 3.10
            return xor_result.bit_count()
        except AttributeError:
            return bin(xor_result).count("1")

    def similarity(self, other_hash: Any) -> float:
        """Calculate how similar this hash is from another simhash.
        Returns a float from 0.0 to 1.0.
        """
        return (self.length - self.hamming_distance(other_hash)) / self.length


def content_fingerprint(content: str) -> str:
    "Calculate a simhash hex value for meaningful bits of the content."
    return Simhash(content).to_hex()
