// Meta-functions to be applied module-wide.

var { langcodesScore } = require('./filters.js');

// We'll need to implement our own cache clearing mechanism
var caches = new Set();

/**
 * Add a cache to the set of caches that can be cleared
 * @param {Object} cache - The cache object to add
 */
function addCache(cache) {
    caches.add(cache);
}

/**
 * Reset all known caches used to speed up processing.
 * This may release some memory.
 */
function clearCaches() {
    // Clear all registered caches
    for (var cache of caches) {
        if (typeof cache.clear === 'function') {
            cache.clear();
        }
    }

    // Clear the memoized langcodesScore function
    if (typeof langcodesScore.cache === 'object' && langcodesScore.cache !== null) {
        langcodesScore.cache.clear();
    }
}

module.exports = {
    addCache,
    clearCaches
};