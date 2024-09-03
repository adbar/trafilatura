// Code parts dedicated to duplicate removal and text similarity.

var crypto = require('crypto');

var STRIP_EXTENSION = /\.[^/?#]{2,63}$/;
var LRU_SIZE = 10000; // Adjust this value as needed

function isSimilarDomain(reference, newString, threshold = 0.5) {
    reference = reference.replace(STRIP_EXTENSION, '');
    newString = newString.replace(STRIP_EXTENSION, '');
    return similarity(reference, newString) >= threshold;
}

function similarity(s1, s2) {
    let longer = s1;
    let shorter = s2;
    if (s1.length < s2.length) {
        longer = s2;
        shorter = s1;
    }
    var longerLength = longer.length;
    if (longerLength === 0) {
        return 1.0;
    }
    return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
}

function editDistance(s1, s2) {
    s1 = s1.toLowerCase();
    s2 = s2.toLowerCase();
    var costs = new Array();
    for (let i = 0; i <= s1.length; i++) {
        let lastValue = i;
        for (let j = 0; j <= s2.length; j++) {
            if (i === 0) {
                costs[j] = j;
            } else {
                if (j > 0) {
                    let newValue = costs[j - 1];
                    if (s1.charAt(i - 1) !== s2.charAt(j - 1)) {
                        newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
    }
                    costs[j - 1] = lastValue;
                    lastValue = newValue;
                }
            }
        }
        if (i > 0) {
            costs[s2.length] = lastValue;
        }
    }
    return costs[s2.length];
}

function sampleTokens(inputString, length = 64) {
    var tokens = inputString.split(/\s+/).filter(token => {
        token = token.replace(/^[^\w]+|[^\w]+$/g, '');
        return token.length > 0 && /^[a-zA-Z0-9]+$/.test(token);
    });

    for (let i = 4; i >= 0; i--) {
        var sample = tokens.filter(t => t.length > i);
        if (sample.length >= length / 2) {
            return sample;
        }
    }
    return tokens;
}

function generateBowHash(inputString, length = 24) {
    var testString = sampleTokens(inputString).join(' ').trim();
    return crypto.createHash('blake2b512').update(testString).digest().slice(0, length);
}

class Simhash {
    constructor(inputString = '', length = 64, existingHash = null) {
        this.length = length;
        this.hash = this.validate(existingHash) || this.createHash(inputString);
    }

    _hash(inputString) {
        return BigInt('0x' + crypto.createHash('blake2b512').update(inputString).digest('hex').slice(0, 16));
    }

    _vectorToAdd(token) {
        var hash = this._hash(token);
        return Array.from({length: this.length}, (_, i) => (hash & (1n << BigInt(i))) ? 1 : -1);
    }

    createHash(inputString) {
        var vector = new Array(this.length).fill(0);
        var tokens = sampleTokens(inputString, this.length);

        for (var token of tokens) {
            var tokenVector = this._vectorToAdd(token);
            for (let i = 0; i < this.length; i++) {
                vector[i] += tokenVector[i];
            }
        }

        return BigInt(vector.reduce((acc, val, i) => acc + (val >= 0 ? 1n << BigInt(i) : 0n), 0n));
    }

    toHex() {
        return this.hash.toString(16);
    }

    validate(inputHash) {
        if (typeof inputHash === 'bigint') {
            return inputHash;
        }
        if (typeof inputHash === 'string') {
            if (/^[0-9]+$/.test(inputHash) && inputHash.length >= 18 && inputHash.length <= 22) {
                return BigInt(inputHash);
            }
            return BigInt('0x' + inputHash);
        }
        return null;
    }

    hammingDistance(otherHash) {
        return (this.hash ^ otherHash.hash).toString(2).split('1').length - 1;
    }

    similarity(otherHash) {
        return (this.length - this.hammingDistance(otherHash)) / this.length;
    }
}

function contentFingerprint(content) {
    return new Simhash(content).toHex();
}

class LRUCache {
    constructor(maxsize = 128) {
        this.maxsize = maxsize;
        this.cache = new Map();
    }

    get(key) {
        if (this.cache.has(key)) {
            var value = this.cache.get(key);
            this.cache.delete(key);
            this.cache.set(key, value);
            return value;
        }
        return -1;
    }

    put(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        } else if (this.cache.size >= this.maxsize) {
            this.cache.delete(this.cache.keys().next().value);
        }
        this.cache.set(key, value);
    }

    clear() {
        this.cache.clear();
    }
}

var LRU_TEST = new LRUCache(LRU_SIZE);

function putInCache(testString) {
    var cacheVal = LRU_TEST.get(testString);
    var value = cacheVal !== -1 ? cacheVal + 1 : 1;
    LRU_TEST.put(testString, value);
}

function duplicateTest(element, options) {
    var testString = element.textContent.trim().replace(/\s+/g, ' ');
    if (testString.length > options.minDuplcheckSize) {
        var cacheVal = LRU_TEST.get(testString);
        if (cacheVal > options.maxRepetitions) {
            LRU_TEST.put(testString, cacheVal + 1);
            return true;
        }
    }
    putInCache(testString);
    return false;
}

module.exports = {
    isSimilarDomain,
    generateBowHash,
    Simhash,
    contentFingerprint,
    LRUCache,
    duplicateTest
};