// Functions related to URL manipulation and extraction of URL parts.

// Regular expressions
var DOMAIN_REGEX = /(?:(?:f|ht)tp)s?:\/\/(?:[^/?#]{,63}\.)?([^/?#.]{4,63}\.[^/?#]{2,63}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[0-9a-f:]{16,})(?:\/|$)/;
var STRIP_PORT_REGEX = /(?<=\D):\d+/;
var CLEAN_FLD_REGEX = /^www[0-9]*\./;
var FEED_WHITELIST_REGEX = /(?:feed(?:burner|proxy))/i;

/**
 * Cached function to extract top-level domain info
 * @param {string} url - The URL to extract domain info from
 * @param {boolean} fast - Whether to use a faster, regex-based method
 * @returns {[string|null, string|null]} - A tuple of domain and full domain
 */
function getTldinfo(url, fast = false) {
    if (!url || typeof url !== 'string') {
        return [null, null];
    }
    if (fast) {
        var domainMatch = url.match(DOMAIN_REGEX);
        if (domainMatch) {
            var fullDomain = domainMatch[1].split('@').pop().replace(STRIP_PORT_REGEX, '');
            var cleanMatch = fullDomain.split('.')[0];
            if (cleanMatch) {
                return [cleanMatch, fullDomain];
            }
        }
    }
    // Fallback: simplified tld extraction
    try {
        var urlObj = new URL(url);
        var parts = urlObj.hostname.split('.');
        if (parts.length >= 2) {
            var domain = parts[parts.length - 2];
            var fld = parts.slice(-2).join('.');
            return [domain, fld.replace(CLEAN_FLD_REGEX, '')];
        }
    } catch (error) {
        // Invalid URL
    }
    return [null, null];
}

/**
 * Extract domain name information using top-level domain info
 * @param {string} url - The URL to extract domain from
 * @param {Set<string>} [blacklist] - A set of blacklisted domains
 * @param {boolean} [fast=false] - Whether to use a faster, regex-based method
 * @returns {string|null} - The extracted domain or null if blacklisted or invalid
 */
function extractDomain(url, blacklist = new Set(), fast = false) {
    var [domain, fullDomain] = getTldinfo(url, fast);
    return (fullDomain && !blacklist.has(domain) && !blacklist.has(fullDomain)) ? fullDomain : null;
}

/**
 * Parse a string or use URL object directly
 * @param {string|URL} url - The URL to parse
 * @returns {URL} - The parsed URL object
 */
function _parse(url) {
    if (typeof url === 'string') {
        return new URL(url);
    } else if (url instanceof URL) {
        return url;
    } else {
        throw new TypeError(`Wrong input type: ${typeof url}`);
    }
}

/**
 * Strip URL of some of its parts to get base URL
 * @param {string|URL} url - The URL to get the base from
 * @returns {string} - The base URL
 */
function getBaseUrl(url) {
    var parsedUrl = _parse(url);
    return `${parsedUrl.protocol}//${parsedUrl.host}`;
}

/**
 * Decompose URL in two parts: protocol + host/domain and path
 * @param {string|URL} url - The URL to decompose
 * @returns {[string, string]} - A tuple of hostname and path
 */
function getHostAndPath(url) {
    var parsedUrl = _parse(url);
    var hostname = getBaseUrl(parsedUrl);
    let pathval = parsedUrl.pathname + parsedUrl.search + parsedUrl.hash;
    if (pathval === '') {
        pathval = '/';
    }
    if (!hostname || !pathval) {
        throw new Error(`Incomplete URL: ${url}`);
    }
    return [hostname, pathval];
}

/**
 * Convenience function returning domain and host info (protocol + host/domain) from a URL
 * @param {string} url - The URL to get info from
 * @returns {[string|null, string]} - A tuple of domain name and base URL
 */
function getHostinfo(url) {
    var domainname = extractDomain(url, undefined, true);
    var baseUrl = getBaseUrl(url);
    return [domainname, baseUrl];
}

/**
 * Prepend protocol and host information to relative links
 * @param {string} baseurl - The base URL
 * @param {string} url - The URL to fix
 * @returns {string} - The fixed URL
 */
function fixRelativeUrls(baseurl, url) {
    if (url.startsWith('{')) {
        return url;
    }

    var baseUrlObj = new URL(baseurl);
    let urlObj;
    try {
        urlObj = new URL(url, baseurl);
    } catch (error) {
        return url; // Return original URL if it's invalid
    }

    if (urlObj.host !== baseUrlObj.host) {
        if (urlObj.protocol) {
            return url;
        }
        return `http://${urlObj.host}${urlObj.pathname}${urlObj.search}${urlObj.hash}`;
    }

    return urlObj.href;
}

/**
 * Return a list of links corresponding to the given substring pattern
 * @param {string[]} linkList - The list of links to filter
 * @param {string|null} urlfilter - The substring pattern to filter by
 * @returns {string[]} - The filtered list of links
 */
function filterUrls(linkList, urlfilter) {
    if (urlfilter === null) {
        return [...new Set(linkList)].sort();
    }
    // filter links
    let filteredList = linkList.filter(l => l.includes(urlfilter));
    // feedburner option: filter and wildcards for feeds
    if (filteredList.length === 0) {
        filteredList = linkList.filter(l => FEED_WHITELIST_REGEX.test(l));
    }
    return [...new Set(filteredList)].sort();
}

/**
 * Determine if a link leads to another host
 * @param {string} url - The URL to check
 * @param {string} reference - The reference URL
 * @param {boolean} [ignoreSuffix=true] - Whether to ignore the suffix in comparison
 * @returns {boolean} - True if the URL is external, false otherwise
 */
function isExternal(url, reference, ignoreSuffix = true) {
    var [strippedRef, ref] = getTldinfo(reference, true);
    var [strippedDomain, domain] = getTldinfo(url, true);
    return ignoreSuffix ? strippedDomain !== strippedRef : domain !== ref;
}

/**
 * Compare the link and its possible variants to the existing URL base
 * @param {string} link - The link to check
 * @param {Set<string>} knownLinks - The set of known links
 * @returns {boolean} - True if the link is known, false otherwise
 */
function isKnownLink(link, knownLinks) {
    // check exact link
    if (knownLinks.has(link)) {
        return true;
    }

    // check link and variants with trailing slashes
    var slashTest = link.endsWith('/') ? link.slice(0, -1) : link + '/';
    if (knownLinks.has(slashTest)) {
        return true;
    }

    // check link and variants with modified protocol
    if (link.startsWith('http')) {
        var protocolTest = link.startsWith('https') ? 'http' + link.slice(5) : 'https' + link.slice(4);
        var slashTestProtocol = protocolTest.endsWith('/') ? protocolTest.slice(0, -1) : protocolTest + '/';
        if (knownLinks.has(protocolTest) || knownLinks.has(slashTestProtocol)) {
            return true;
        }
    }

    return false;
}

module.exports = {
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