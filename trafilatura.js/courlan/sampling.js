// Utilities dedicated to URL sampling

var { UrlStore } = require('./urlstore.js');

// Simple logging mechanism
var LOGGER = {
    debug: console.debug,
    info: console.info,
    warn: console.warn,
    error: console.error
};

/**
 * Iterate through the hosts in store and draw samples.
 * @param {UrlStore} urlstore - The UrlStore object
 * @param {number} samplesize - The size of the sample to draw
 * @param {number|null} excludeMin - Minimum number of URLs required for a domain
 * @param {number|null} excludeMax - Maximum number of URLs allowed for a domain
 * @returns {string[]} - The sampled URLs
 */
function _makeSample(urlstore, samplesize, excludeMin, excludeMax) {
    var outputUrls = [];
    for (var domain of urlstore.urldict.keys()) {
        var urlpaths = urlstore._loadUrls(domain)
            .filter(p => p.urlpath !== '/' && p.urlpath !== null)
            .map(p => p.path());

        // too few or too many URLs
        if (
            urlpaths.length === 0 ||
            (excludeMin !== null && urlpaths.length < excludeMin) ||
            (excludeMax !== null && urlpaths.length > excludeMax)
        ) {
            LOGGER.warn(`discarded (size): ${domain}\t\turls: ${urlpaths.length}`);
            continue;
        }

        // sample
        let mysample;
        if (urlpaths.length > samplesize) {
            mysample = urlpaths.sort(() => 0.5 - Math.random()).slice(0, samplesize).sort();
        } else {
            mysample = urlpaths;
        }

        outputUrls.push(...mysample.map(p => domain + p));
        LOGGER.debug(`${domain}\t\turls: ${mysample.length}\tprop.: ${mysample.length / urlpaths.length}`);
    }
    return outputUrls;
}

/**
 * Sample a list of URLs by domain name, optionally using constraints on their number
 * @param {string[]} inputUrls - The input URLs to sample from
 * @param {number} samplesize - The size of the sample to draw
 * @param {Object} options - Additional options
 * @param {number|null} [options.excludeMin=null] - Minimum number of URLs required for a domain
 * @param {number|null} [options.excludeMax=null] - Maximum number of URLs allowed for a domain
 * @param {boolean} [options.strict=false] - Whether to use strict mode
 * @param {boolean} [options.verbose=false] - Whether to use verbose logging
 * @returns {string[]} - The sampled URLs
 */
function sampleUrls(inputUrls, samplesize, {
    excludeMin = null,
    excludeMax = null,
    strict = false,
    verbose = false
} = {}) {
    // logging
    if (verbose) {
        LOGGER.level = 'debug';
    } else {
        LOGGER.level = 'error';
    }

    // store
    var urlstore = new UrlStore({
        compressed: true,
        language: null,
        strict: strict,
        verbose: verbose
    });
    urlstore.addUrls(inputUrls);

    // return gathered URLs
    return _makeSample(urlstore, samplesize, excludeMin, excludeMax);
}

module.exports = {
    sampleUrls
};