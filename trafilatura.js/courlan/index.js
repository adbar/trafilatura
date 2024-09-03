// Main entry point for the courlan library

var { cleanUrl, scrubUrl, normalizeUrl } = require('./clean.js');
var { checkUrl, extractLinks, filterLinks } = require('./core.js');
var {
    basicFilter,
    domainFilter,
    extensionFilter,
    langFilter,
    pathFilter,
    typeFilter,
    validateUrl,
    isValidUrl,
    isNavigationPage,
    isNotCrawlable
} = require('./filters.js');
var { sampleUrls } = require('./sampling.js');
var { UrlStore } = require('./urlstore.js');
var {
    getTldinfo,
    extractDomain,
    getBaseUrl,
    getHostAndPath,
    getHostinfo,
    fixRelativeUrls,
    filterUrls,
    isExternal,
    isKnownLink
} = require('./urlutils.js');

module.exports = {
    // clean.js
    cleanUrl,
    scrubUrl,
    normalizeUrl,

    // core.js
    checkUrl,
    extractLinks,
    filterLinks,

    // filters.js
    basicFilter,
    domainFilter,
    extensionFilter,
    langFilter,
    pathFilter,
    typeFilter,
    validateUrl,
    isValidUrl,
    isNavigationPage,
    isNotCrawlable,

    // sampling.js
    sampleUrls,

    // urlstore.js
    UrlStore,

    // urlutils.js
    getTldinfo,
    extractDomain,
    getBaseUrl,
    getHostAndPath,
    getHostinfo,
    fixRelativeUrls,
    filterUrls,
    isExternal,
    isKnownLink
};