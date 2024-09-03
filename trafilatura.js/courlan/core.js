// Core functions needed to make the module work.

var { normalizeUrl, scrubUrl } = require('./clean.js');
var {
    basicFilter,
    domainFilter,
    extensionFilter,
    isNavigationPage,
    isNotCrawlable,
    langFilter,
    pathFilter,
    typeFilter,
    validateUrl
} = require('./filters.js');
var { redirectionTest } = require('./network.js');
var { BLACKLIST } = require('./settings.js');
var {
    extractDomain,
    getBaseUrl,
    fixRelativeUrls,
    isExternal,
    isKnownLink
} = require('./urlutils.js');

// Simple logging mechanism
var LOGGER = {
    debug: console.debug,
    info: console.info,
    warn: console.warn,
    error: console.error
};

// Regular expressions
var FIND_LINKS_REGEX = /<a [^<>]+?>/gi;
var HREFLANG_REGEX = /hreflang=["\']?([a-z-]+)/i;
var LINK_REGEX = /href=["\']?([^ ]+?)(["\' >])/i;

/**
 * Check links for appropriateness and sanity
 * @param {string} url - URL to check
 * @param {Object} options - Configuration options
 * @param {boolean} [options.strict=false] - Set to true for stricter filtering
 * @param {boolean} [options.withRedirects=false] - Set to true for redirection test
 * @param {string} [options.language] - Set target language (ISO 639-1 codes)
 * @param {boolean} [options.withNav=false] - Set to true to include navigation pages
 * @param {boolean} [options.trailingSlash=true] - Set to false to trim trailing slashes
 * @returns {[string, string]|null} - A tuple of canonical URL and extracted domain, or null if invalid
 */
function checkUrl(url, {
    strict = false,
    withRedirects = false,
    language = null,
    withNav = false,
    trailingSlash = true
} = {}) {
    try {
        // Length test
        if (!basicFilter(url)) {
            LOGGER.debug(`rejected, basic filter: ${url}`);
            throw new Error('Failed basic filter');
        }

        // Clean
        url = scrubUrl(url);

        // Get potential redirect
        if (withRedirects) {
            url = redirectionTest(url);
        }

        // Spam & structural elements
        if (!typeFilter(url, { strict, withNav })) {
            LOGGER.debug(`rejected, type filter: ${url}`);
            throw new Error('Failed type filter');
        }

        // Internationalization and language heuristics in URL
        if (language !== null && !langFilter(url, language, strict, trailingSlash)) {
            LOGGER.debug(`rejected, lang filter: ${url}`);
            throw new Error('Failed language filter');
        }

        // Split and validate
        var [validationTest, parsedUrl] = validateUrl(url);
        if (!validationTest) {
            LOGGER.debug(`rejected, validation test: ${url}`);
            throw new Error('Failed validation test');
        }

        // Content filter based on extensions
        if (!extensionFilter(parsedUrl.pathname)) {
            LOGGER.debug(`rejected, extension filter: ${url}`);
            throw new Error('Failed extension filter');
        }

        // Unsuitable domain/host name
        if (!domainFilter(parsedUrl.hostname)) {
            LOGGER.debug(`rejected, domain name: ${url}`);
            throw new Error('Failed domain filter');
        }

        // Strict content filtering
        if (strict && !pathFilter(parsedUrl.pathname, parsedUrl.search)) {
            LOGGER.debug(`rejected, path filter: ${url}`);
            throw new Error('Failed path filter');
        }

        // Normalize
        url = normalizeUrl(parsedUrl, strict, language, trailingSlash);

        // Domain info: use blacklist in strict mode only
        var domain = extractDomain(url, { blacklist: strict ? BLACKLIST : null, fast: true });
        if (domain === null) {
            LOGGER.debug(`rejected, domain name: ${url}`);
            return null;
        }

        return [url, domain];
    } catch (error) {
        LOGGER.debug(`discarded URL: ${url}`);
        return null;
    }
}

/**
 * Filter links in an HTML document using a series of heuristics
 * @param {string} pagecontent - Whole page content
 * @param {Object} options - Configuration options
 * @param {string} [options.url] - Full URL of the original page
 * @param {string} [options.baseUrl] - Base URL for relative links
 * @param {boolean} [options.externalBool=false] - Set to true for external links only, false for internal links only
 * @param {boolean} [options.noFilter=false] - Override settings and bypass checks to return all possible URLs
 * @param {string} [options.language] - Set target language (ISO 639-1 codes)
 * @param {boolean} [options.strict=true] - Set to true for stricter filtering
 * @param {boolean} [options.trailingSlash=true] - Set to false to trim trailing slashes
 * @param {boolean} [options.withNav=false] - Set to true to include navigation pages
 * @param {boolean} [options.redirects=false] - Set to true for redirection test
 * @param {string} [options.reference] - Provide a host reference for external/internal evaluation
 * @returns {Set<string>} - A set containing filtered HTTP links checked for sanity and consistency
 */
function extractLinks(pagecontent, {
    url = null,
    baseUrl = null,
    externalBool = false,
    noFilter = false,
    language = null,
    strict = true,
    trailingSlash = true,
    withNav = false,
    redirects = false,
    reference = null
} = {}) {
    baseUrl = baseUrl || getBaseUrl(url);
    url = url || baseUrl;
    var candidates = new Set();
    var validlinks = new Set();

    if (!pagecontent) {
        return validlinks;
    }

    // Define host reference
    reference = reference || baseUrl;

    // Extract links
    var linkMatches = pagecontent.matchAll(FIND_LINKS_REGEX);
    for (var match of linkMatches) {
        var link = match[0];
        if (link.includes('rel') && link.includes('nofollow')) {
            continue;
        }

        if (!noFilter && language !== null && link.includes('hreflang')) {
            var langMatch = HREFLANG_REGEX.exec(link);
            if (langMatch && (langMatch[1].startsWith(language) || langMatch[1] === 'x-default')) {
                var linkMatch = LINK_REGEX.exec(link);
                if (linkMatch) {
                    candidates.add(linkMatch[1]);
                }
            }
        } else {
            var linkMatch = LINK_REGEX.exec(link);
            if (linkMatch) {
                candidates.add(linkMatch[1]);
            }
        }
    }

    // Filter candidates
    for (var link of candidates) {
        let processedLink = link;
        if (!link.startsWith('http')) {
            processedLink = fixRelativeUrls(url, link);
        }

        if (!noFilter) {
            var checked = checkUrl(processedLink, {
                strict,
                trailingSlash,
                withNav,
                withRedirects: redirects,
                language
            });
            if (checked === null) {
                continue;
            }
            processedLink = checked[0];
            if (externalBool !== isExternal(processedLink, reference, true)) {
                continue;
            }
        }

        if (isKnownLink(processedLink, validlinks)) {
            continue;
        }
        validlinks.add(processedLink);
    }

    LOGGER.info(`${candidates.size} links found – ${validlinks.size} valid links`);
    return validlinks;
}

/**
 * Find links in an HTML document, filter them and add them to the data store
 * @param {string} htmlstring - HTML content
 * @param {string} url - URL of the page
 * @param {Object} options - Configuration options
 * @param {string} [options.baseUrl] - Base URL for relative links
 * @param {string} [options.lang] - Target language
 * @param {Object} [options.rules] - Robot rules parser
 * @param {boolean} [options.external=false] - Whether to include external links
 * @param {boolean} [options.strict=false] - Whether to use strict filtering
 * @param {boolean} [options.withNav=true] - Whether to include navigation pages
 * @returns {[string[], string[]]} - Array of regular links and priority links
 */
function filterLinks(htmlstring, url, {
    baseUrl = null,
    lang = null,
    rules = null,
    external = false,
    strict = false,
    withNav = true
} = {}) {
    var links = [];
    var linksPriority = [];
    url = url || baseUrl;

    var extractedLinks = extractLinks(htmlstring, {
        url,
        externalBool: external,
        language: lang,
        strict,
        withNav
    });

    for (var link of extractedLinks) {
        if (isNotCrawlable(link) || (rules !== null && !rules.canFetch('*', link))) {
            continue;
        }

        if (isNavigationPage(link)) {
            linksPriority.push(link);
        } else {
            links.push(link);
        }
    }

    return [links, linksPriority];
}

module.exports = {
    checkUrl,
    extractLinks,
    filterLinks
};