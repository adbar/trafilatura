// Meta-functions to be applied module-wide.

var { resetCachesCourlan } = require('./courlan/meta');
var { resetCachesHtmldate } = require('./htmldate/meta');
// var { defineStoplist } = require('justext/core');
var { LRU_TEST, Simhash, isSimilarDomain } = require('./deduplication');
var { lineProcessing, returnPrintablesAndSpaces, trim } = require('./utils');

function resetCaches() {
    // Reset justext cache
    // defineStoplist.cache.clear();

    // Reset htmldate and charset_normalizer caches
    resetCachesHtmldate();

    // Reset courlan caches
    resetCachesCourlan();

    // Reset own caches
    isSimilarDomain.cache.clear();
    lineProcessing.cache.clear();
    returnPrintablesAndSpaces.cache.clear();
    trim.cache.clear();
    LRU_TEST.clear();
    Simhash.vectorToAdd.cache.clear();

}

module.exports = {
    resetCaches
};