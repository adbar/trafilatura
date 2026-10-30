# pylint:disable-msg=I1101
"""
Unit tests for the trafilatura's text hashing and cache.
"""

import copy
import pickle

import pytest
from lxml import etree, html

import trafilatura.deduplication
from trafilatura import extract
from trafilatura.cli_utils import generate_hash_filename
from trafilatura.core import Extractor
from trafilatura.deduplication import (
    LRUCache,
    Simhash,
    content_fingerprint,
    duplicate_test,
    generate_bow_hash,
    sample_tokens,
)
from trafilatura.htmlprocessing import process_node
from trafilatura.meta import reset_caches

DEFAULT_OPTIONS = Extractor()


@pytest.fixture(autouse=True)
def _restore_lru_test():
    "Restore the module-global LRU_TEST after tests that reassign it."
    original = trafilatura.deduplication.LRU_TEST
    yield
    trafilatura.deduplication.LRU_TEST = original
    reset_caches()


def test_hashes():
    "Hashing functions and content fingerprints."
    content = "abcde ijk l, " * 10
    assert content_fingerprint(content) == "528497a1d07b66d6"
    assert generate_hash_filename(content) == "42LNugG3Sc95646i"
    assert content_fingerprint("Hello world! This is a test string with some numbers 123.") == "5efdce9f2b554683"
    assert content_fingerprint("这是一个测试。我们在测试中文。") == "ff377edee6edfb78"
    assert content_fingerprint("Hello世界。This is混合文本!") == "24979dc6c8a26a5"


def test_simhash():
    "Test similarity calculation based on Simhash class."
    # https://en.wiktionary.org/wiki/put_lipstick_on_a_pig
    factor = 1
    hashes = []
    hashes.append(Simhash("This is like putting lipstick on a pig." * factor))
    # hashes.append(Simhash("This is like putting lipstick on a pig.123"*factor))
    hashes.append(Simhash("This is just like putting lipstick on a pig." * factor))
    hashes.append(Simhash("Putting lipstick on a pig is what this is about." * factor))
    hashes.append(Simhash("The words are completely different but let's see." * factor))

    sims = [hashes[0].similarity(h) for h in hashes]
    assert sims[0] == 1.0
    assert min(sims) == sims[-1]

    # sanity checks
    assert Simhash(existing_hash=hashes[0].to_hex()).hash == hashes[0].hash
    assert int(hex(hashes[0].hash), 0) == hashes[0].hash
    assert Simhash(existing_hash=hashes[0].to_hex()).hash == hashes[0].hash

    # re-hashed
    assert Simhash(existing_hash="aghj").hash == 18446744073709551615
    assert Simhash(existing_hash="18446744073709551615").hash == 18446744073709551615
    assert Simhash(existing_hash="18446744073709551616").hash != 18446744073709551616
    assert Simhash(existing_hash=123).hash == 123
    assert Simhash(existing_hash=18446744073709551615).hash == 18446744073709551615
    assert Simhash(existing_hash=2**64).hash != 2**64
    assert Simhash(existing_hash=-1).hash != -1
    assert Simhash(existing_hash=None).hash == Simhash().hash

    # similarity
    assert Simhash("abcde").similarity(Simhash("abcde")) == 1.0
    assert Simhash("abcde").similarity(Simhash("abcde", length=2)) != 1.0
    assert Simhash("abcde").similarity(Simhash("fghij")) < 0.6
    assert Simhash("abcde " * 100).similarity(Simhash("abcde")) == 1.0


def _make_pair(text):
    "Body wrapping a paragraph: both share the same text for duplicate_test."
    body = etree.Element("body")
    element = html.fromstring(f"<p>{text}</p>")
    body.append(element)
    return body, element


def test_lrucache():
    "Duplicate detection through the global LRU_TEST cache."
    lru_test = LRUCache(maxsize=2)
    trafilatura.deduplication.LRU_TEST = lru_test

    my_body, my_element = _make_pair("AAAA BBBB " * 13)
    seq = (my_element, my_element, my_body, my_element)
    assert [duplicate_test(e, DEFAULT_OPTIONS) for e in seq] == [False, False, False, True]
    other_body, other_element = _make_pair("CCCC DDDD " * 11)
    seq = (other_body, other_element, other_body, other_element)
    assert [duplicate_test(e, DEFAULT_OPTIONS) for e in seq] == [False, False, False, True]
    yet_another_body, yet_another_element = _make_pair("EEEE FFFF " * 13)
    assert [duplicate_test(yet_another_body, DEFAULT_OPTIONS) for _ in range(3)] == [False] * 3
    # 2 elements in cache, original element has been cleared?
    assert duplicate_test(other_element, DEFAULT_OPTIONS) is True
    assert duplicate_test(yet_another_element, DEFAULT_OPTIONS) is True
    assert duplicate_test(my_element, DEFAULT_OPTIONS) is False
    # clear the cache
    lru_test.clear()
    assert duplicate_test(other_element, DEFAULT_OPTIONS) is False


def test_dedup():
    "Test paragraph-level deduplication."
    my_p = "<p>abc</p>"
    doc = html.fromstring("<html><body>" + my_p * 50 + "</body></html>")
    trafilatura.deduplication.LRU_TEST = LRUCache(maxsize=2)
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is None

    # paragraph level
    trafilatura.deduplication.LRU_TEST = LRUCache(maxsize=2)
    my_p = etree.fromstring("<p>" + "abc" * 50 + "</p>")
    options = Extractor(dedup=True)
    assert process_node(my_p, options) is not None
    assert process_node(my_p, options) is not None
    assert process_node(my_p, options) is not None
    assert process_node(my_p, options) is None


def test_dedup_reset_caches():
    "Repeated identical extractions accumulate in LRU_TEST; reset_caches() clears it (#778)."
    reset_caches()
    try:
        doc = html.fromstring("<html><body>" + "<p>abc</p>" * 50 + "</body></html>")
        results = [extract(doc, deduplicate=True) for _ in range(6)]
        assert results[0] is not None
        assert results[-1] is None
        reset_caches()
        assert extract(doc, deduplicate=True) is not None
    finally:
        reset_caches()


def test_lrucache_api():
    "Direct coverage of the LRUCache public API."
    with pytest.raises(ValueError):
        LRUCache(maxsize=0)
    with pytest.raises(ValueError):
        LRUCache(maxsize=-1)

    original = LRUCache(maxsize=8)
    original.increment("a")
    cache = pickle.loads(pickle.dumps(original))
    assert isinstance(cache, LRUCache)
    assert cache.maxsize == 8
    assert cache.get("a") == 1  # contents survive
    assert cache.increment("a") == 1  # recreated lock works
    assert copy.copy(original).cache is not original.cache  # __getstate__ deep-copies the dict

    lru = LRUCache(maxsize=2)
    assert bool(lru) is True  # an empty cache as dedup option must keep dedup enabled
    assert lru.get("a") == -1
    lru.put("a", 1)
    assert lru.get("a") == 1
    lru.put("b", 2)
    # touching "a" makes "b" the eviction candidate
    assert lru.get("a") == 1
    lru.put("c", 3)
    assert lru.get("b") == -1
    assert lru.get("a") == 1
    assert lru.get("c") == 3
    # put on an existing key updates value and recency
    lru.put("a", 10)
    lru.put("d", 4)
    assert lru.get("c") == -1
    assert lru.get("a") == 10
    lru.clear()
    assert not lru.cache

    # increment matches the get + put composition and returns the previous count
    lru = LRUCache(maxsize=2)
    assert lru.increment("x") == -1
    assert lru.increment("x") == 1
    assert lru.get("x") == 2
    lru.increment("y")
    lru.increment("z")
    assert lru.get("x") == -1  # evicted as oldest


def test_simhash_validate_pins():
    "Pin deliberate validate behaviors so refactoring cannot silently change them."
    reference = Simhash("abcde")
    # negative integers are rejected and trigger re-hashing
    assert Simhash("abcde", existing_hash=-(10**18)).hash == reference.hash
    # booleans are rejected despite being int subclasses
    assert Simhash("abcde", existing_hash=True).hash == reference.hash
    # existing_hash="0" is deliberately re-hashed (kept for backward compatibility)
    assert Simhash(existing_hash="0").hash == 18446744073709551615
    # non-decimal Unicode digits fall through to re-hashing instead of crashing int()
    assert Simhash("abcde", existing_hash="¹" * 18).hash == reference.hash
    # hex strings outside the 64-bit hash range are rejected and re-hashed
    assert Simhash("abcde", existing_hash="-ff").hash == reference.hash
    assert Simhash("abcde", existing_hash="f" * 17).hash == reference.hash
    # small hex values as produced by to_hex() still round-trip
    assert Simhash(existing_hash="ff").hash == 255


def test_duplicate_test_boundaries():
    "min_duplcheck_size is a strict bound and the 4th repetition gets flagged."
    options = Extractor()
    options.dedup = LRUCache(maxsize=1024)  # scoped cache keeps the global one clean
    at_limit = html.fromstring("<p>" + "x" * options.min_duplcheck_size + "</p>")
    assert [duplicate_test(at_limit, options) for _ in range(6)] == [False] * 6
    above_limit = html.fromstring("<p>" + "x" * (options.min_duplcheck_size + 1) + "</p>")
    # max_repetitions=2: flagged once the previous count exceeds it
    assert [duplicate_test(above_limit, options) for _ in range(6)] == [False, False, False, True, True, True]


def test_sample_tokens():
    "Token sampling: regular, fallback and threshold-relaxation inputs."
    tokens = sample_tokens("Hello world! This is a test string with some numbers 123.")
    assert "Hello" in tokens
    assert "world" in tokens
    assert "123" in tokens
    # Chinese punctuation: fallback path
    assert sample_tokens("这是一个测试。我们在测试中文。") == ["这是一个测试", "我们在测试中文"]
    # mixed text: primary path yields one token, no fallback
    assert sample_tokens("Hello世界。This is混合文本!") == ["is混合文本"]
    assert sample_tokens("") == []
    assert sample_tokens("!!! ... ???") == []
    assert sample_tokens("。、！") == []
    # many short tokens force the length threshold down
    assert sample_tokens("ab " * 40) == ["ab"] * 40

    # words with combining marks, see issue #1055
    assert sample_tokens("ประเทศไทย สวยงาม") == ["ประเทศไทย", "สวยงาม"]
    assert sample_tokens("தமிழ் மொழி") == ["தமிழ்", "மொழி"]
    assert sample_tokens("cafe\u0301 nai\u0308ve") == ["cafe\u0301", "nai\u0308ve"]
    assert sample_tokens("\u0301\u0308 ab") == ["ab"]


def test_fingerprint_combining_marks():
    "Different texts with combining marks get different hashes, see issue #1055."
    thai = content_fingerprint("ประเทศไทยเป็นประเทศที่สวยงาม มีวัดและชายหาดมากมาย")
    other = content_fingerprint("วันนี้อากาศดีมาก เราจะไปเดินเล่นที่สวนสาธารณะ")
    assert thai != other
    assert "ffffffffffffffff" not in (thai, other)
    tamil = content_fingerprint("தமிழ் ஒரு பழமையான மொழி")
    assert tamil != content_fingerprint("இன்று வானிலை நன்றாக உள்ளது")
    decomposed = "cafe\u0301 re\u0301sume\u0301 nai\u0308ve"
    assert content_fingerprint(decomposed) != content_fingerprint("cafe\u0301 sold out")
    # enough long tokens keep the strict threshold: short ones are dropped
    tokens = sample_tokens(" ".join(f"token{i}" for i in range(40)) + " ab cd")
    assert "ab" not in tokens
    assert len(tokens) == 40


def test_generate_bow_hash():
    "Digest size parameter and degenerate inputs."
    assert len(generate_bow_hash("Hello world this is a test", 12)) == 12
    assert len(generate_bow_hash("", 24)) == 24
    assert generate_bow_hash("") == generate_bow_hash("   ")


def test_dedup_cache_option():
    "A cache instance passed as dedup option scopes deduplication (#778)."
    doc = html.fromstring("<html><body>" + "<p>abc</p>" * 50 + "</body></html>")

    # fresh cache per call: deterministic, repeated extractions all succeed
    results = [extract(doc, deduplicate=LRUCache(maxsize=1024)) for _ in range(6)]
    assert None not in results
    assert len(set(results)) == 1

    # shared cache across calls: accumulation triggers deduplication
    shared = LRUCache(maxsize=1024)
    results = [extract(doc, deduplicate=shared) for _ in range(6)]
    assert results[0] is not None
    assert results[-1] is None

    # the global cache is untouched by scoped runs
    assert extract(doc, deduplicate=True) is not None
