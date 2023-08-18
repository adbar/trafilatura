

from trafilatura.hashing import (Simhash, content_fingerprint,
                                 generate_hash_filename)


def test_hashes():
    "Test hashing functions."
    content = "abcde ijk l, "*10
    assert content_fingerprint(content) == "528497a1d07b66d6"
    assert generate_hash_filename(content) == "42LNugG3Sc95646i"



def test_simhash():
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



if __name__ == "__main__":
    test_hashes()
    test_simhash()
