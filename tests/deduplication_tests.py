# pylint:disable-msg=I1101
"""
Unit tests for the trafilatura's text hashing and cache.
"""

from lxml import etree, html

import trafilatura.deduplication

from trafilatura import extract
from trafilatura.cli_utils import generate_hash_filename
from trafilatura.core import Extractor
from trafilatura.deduplication import (LRUCache, Simhash, content_fingerprint,
                                       duplicate_test)


DEFAULT_OPTIONS = Extractor()


def test_hashes():
    "Test hashing functions."
    content = "abcde ijk l, "*10
    assert content_fingerprint(content) == "528497a1d07b66d6"
    assert generate_hash_filename(content) == "42LNugG3Sc95646i"


def test_content_fingerprint():
    "Test content fingerprint generation for different types of text"
    # Test regular Latin text
    text = "Hello world! This is a test string with some numbers 123."
    fingerprint = trafilatura.deduplication.content_fingerprint(text)
    assert fingerprint == "5efdce9f2b554683"

    # Test Chinese text
    chinese_text = "这是一个测试。我们在测试中文。"
    chinese_fingerprint = trafilatura.deduplication.content_fingerprint(chinese_text)
    print(chinese_fingerprint)
    assert chinese_fingerprint == "ff377edee6edfb78"

    # Test mixed text
    mixed_text = "Hello世界。This is混合文本!"
    mixed_fingerprint = trafilatura.deduplication.content_fingerprint(mixed_text)
    assert mixed_fingerprint == "24979dc6c8a26a5"


def test_simhash():
    "Test similarity calculation based on Simhash class."
    # https://en.wiktionary.org/wiki/put_lipstick_on_a_pig
    factor = 1
    hashes = []
    hashes.append(Simhash("This is like putting lipstick on a pig."*factor))
    # hashes.append(Simhash("This is like putting lipstick on a pig.123"*factor))
    hashes.append(Simhash("This is just like putting lipstick on a pig."*factor))
    hashes.append(Simhash("Putting lipstick on a pig is what this is about."*factor))
    hashes.append(Simhash("The words are completely different but let's see."*factor))

    sims = [hashes[0].similarity(h) for h in hashes]
    assert sims[0] == 1.0 and min(sims) == sims[-1]

    # sanity checks
    assert Simhash(existing_hash=hashes[0].to_hex()).hash == hashes[0].hash
    assert int(hex(hashes[0].hash)[2:], 16) == hashes[0].hash
    assert Simhash(existing_hash=hashes[0].to_hex()).hash == hashes[0].hash

    # re-hashed
    assert Simhash(existing_hash="aghj").hash == 18446744073709551615
    assert Simhash(existing_hash="18446744073709551615").hash == 18446744073709551615
    assert Simhash(existing_hash=123).hash != 123
    assert Simhash(existing_hash=18446744073709551615).hash == 18446744073709551615
    assert Simhash(existing_hash=None).hash == Simhash().hash

    # similarity
    assert Simhash("abcde").similarity(Simhash("abcde")) == 1.0
    assert Simhash("abcde").similarity(Simhash("abcde", length=2)) != 1.0
    assert Simhash("abcde").similarity(Simhash("fghij")) < 0.6
    assert Simhash("abcde "*100).similarity(Simhash("abcde")) == 1.0


def test_lrucache():
    '''test basic duplicate detection'''
    lru_test = LRUCache(maxsize=2)
    trafilatura.deduplication.LRU_TEST = lru_test
    my_body = etree.Element('body')

    ### element too short
    #my_element = html.fromstring('<p>AAAA BBBB</p>')
    #my_body.append(my_element)
    #put_in_cache(my_body)
    #assert duplicate_test(my_element, DEFAULT_CONFIG) is False
    ### cached element
    my_element = html.fromstring('<p>AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB AAAA BBBB</p>')
    my_body.append(my_element)
    assert duplicate_test(my_element, DEFAULT_OPTIONS) is False
    assert duplicate_test(my_element, DEFAULT_OPTIONS) is False
    assert duplicate_test(my_body, DEFAULT_OPTIONS) is False
    assert duplicate_test(my_element, DEFAULT_OPTIONS) is True
    other_body = etree.Element('body')
    other_element = html.fromstring('<p>CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD CCCC DDDD</p>')
    other_body.append(other_element)
    assert duplicate_test(other_body, DEFAULT_OPTIONS) is False
    assert duplicate_test(other_element, DEFAULT_OPTIONS) is False
    assert duplicate_test(other_body, DEFAULT_OPTIONS) is False
    assert duplicate_test(other_element, DEFAULT_OPTIONS) is True
    yet_another_body = etree.Element('body')
    yet_another_element = html.fromstring('<p>EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF EEEE FFFF</p>')
    yet_another_body.append(yet_another_element)
    assert duplicate_test(yet_another_body, DEFAULT_OPTIONS) is False
    assert duplicate_test(yet_another_body, DEFAULT_OPTIONS) is False
    assert duplicate_test(yet_another_body, DEFAULT_OPTIONS) is False
    # 2 elements in cache, original element has been cleared?
    # print(LRU_TEST.maxsize, LRU_TEST.full)
    assert duplicate_test(other_element, DEFAULT_OPTIONS) is True
    assert duplicate_test(yet_another_element, DEFAULT_OPTIONS) is True
    assert duplicate_test(my_element, DEFAULT_OPTIONS) is False
    # clear the cache
    lru_test.clear()
    assert duplicate_test(other_element, DEFAULT_OPTIONS) is False
    # get wrong key
    assert lru_test.get('tralala') == -1


def test_dedup():
    "Test paragraph-level deduplication."
    my_p = '<p>abc</p>'
    doc = html.fromstring('<html><body>' + my_p*50 + '</body></html>')
    trafilatura.deduplication.LRU_TEST = LRUCache(maxsize=2)
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is not None
    assert extract(doc, deduplicate=True) is None

    # paragraph level
    trafilatura.deduplication.LRU_TEST = LRUCache(maxsize=2)
    my_p = etree.fromstring('<p>' + 'abc'*50 + '</p>')
    options = DEFAULT_OPTIONS
    options.dedup = True
    assert trafilatura.htmlprocessing.process_node(my_p, options) is not None
    assert trafilatura.htmlprocessing.process_node(my_p, options) is not None
    assert trafilatura.htmlprocessing.process_node(my_p, options) is not None
    assert trafilatura.htmlprocessing.process_node(my_p, options) is None


def test_sample_tokens(monkeypatch):
    "Test token sampling functions including fallback for non-latin text"

    call_counter = {'fallback': 0, 'main': 0}
    original_fallback = trafilatura.deduplication.sample_tokens_fallback

    def spy_fallback(*args, **kwargs):
        call_counter['fallback'] += 1
        return original_fallback(*args, **kwargs)

    monkeypatch.setattr(trafilatura.deduplication, 'sample_tokens_fallback', spy_fallback)

    # Test regular text
    text = "Hello world! This is a test string with some numbers 123."
    tokens = trafilatura.deduplication.sample_tokens(text)
    assert len(tokens) > 0
    assert "Hello" in tokens
    assert "world" in tokens
    assert "123" in tokens
    assert call_counter['fallback'] == 0, "Fallback shouldn't be called for Latin character text"

    # Test Chinese text with Chinese punctuation
    chinese_text = "这是一个测试。我们在测试中文。"
    tokens = trafilatura.deduplication.sample_tokens(chinese_text)
    assert len(tokens) == 2
    assert "这是一个测试" in tokens
    assert "我们在测试中文" in tokens
    assert call_counter['fallback'] == 1, "Fallback should be called for Chinese text"

    # Test mixed text using the default sample tokens method
    mixed_text = "Hello世界。This is混合文本!"
    tokens = trafilatura.deduplication.sample_tokens(mixed_text)
    assert len(tokens) == 1
    assert 'is混合文本' in tokens
    assert call_counter['fallback'] == 1, "Fallback shouldn't be called due to blank"


if __name__ == "__main__":
    test_hashes()
    test_simhash()
    test_lrucache()
    test_dedup()
    test_sample_tokens()
    test_content_fingerprint()
