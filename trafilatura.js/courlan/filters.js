// Bundles functions needed to target text content and validate the input.

// Simple logging mechanism
var LOGGER = {
    debug: console.debug,
    info: console.info,
    warn: console.warn,
    error: console.error
};

var PROTOCOLS = new Set(['http', 'https']);

// domain/host names
var IP_SET = new Set(['.', ':', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']);

// Regular expressions
var VALID_DOMAIN_PORT = /^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9][A-Za-z0-9-_]{0,61}[A-Za-z](\:(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}))?$/i;

var SITE_STRUCTURE = /\/(?:wp-(?:admin|content|includes|json|themes)|paged?|seite|search|suche|gall?er[a-z]{1,2}|labels|archives|uploads|modules|attachment|oembed)\/|[/_-](?:tags?|schlagwort|[ck]ategor[a-z]{1,2}|[ck]at|auth?or|user)\/[^/]+\/?$|[^0-9]\/[0-9]+\/[0-9]+\/$|[^0-9]\/[0-9]{4}\/$|/i;

var FILE_TYPE = /\.(atom|json|css|xml|js|jpg|jpeg|png|svg|gif|tiff|pdf|ogg|mp3|m4a|aac|avi|mp4|mov|web[mp]|flv|ico|pls|zip|tar|gz|iso|swf|woff|eot|ttf)\b|[/-](img|jpg|png)(\b|_)/i;

var ADULT_AND_VIDEOS = /[/_-](?:bild-?kontakte|fick|gangbang|incest|live-?cams?|live-?chat|porno?|sexcam|sexyeroti[ck]|swinger|x{3})\b/i;

var PATH_LANG_FILTER = /(?:https?:\/\/[^/]+\/)([a-z]{2})([_-][a-z]{2,3})?(?:\/|$)/i;
var ALL_PATH_LANGS = /(?:\/)([a-z]{2})([_-][a-z]{2})?(?:\/)/i;
var ALL_PATH_LANGS_NO_TRAILING = /(?:\/)([a-z]{2})([_-][a-z]{2})?(?:\/|$)/i;
var HOST_LANG_FILTER = /https?:\/\/([a-z]{2})\.(?:[^.]{4,})\.(?:[^.]+)(?:\.[^.]+)?\//i;

var NAVIGATION_FILTER = /[/_-](archives|auth?or|[ck]at|category|kategorie|paged?|schlagwort|seite|tags?|topics?|user)\/|\?p=[0-9]+/i;
const NOTCRAWLABLE = /\/([ck]onta[ck]t|datenschutzerkl.{1,2}rung|login|impressum|imprint)(\.[a-z]{3,4})?\/?$|\/login\?|(?:javascript:|mailto:|tel\.?:|whatsapp:)/i;

var INDEX_PAGE_FILTER = /.{0,5}\/(default|home|index)(\.[a-z]{3,5})?\/?$/i;

var EXTENSION_REGEX = /\.[a-z]{2,5}$/;

var WHITELISTED_EXTENSIONS = new Set([
    '.adp', '.amp', '.asp', '.aspx', '.cfm', '.cgi', '.do', '.htm', '.html',
    '.htx', '.jsp', '.mht', '.mhtml', '.php', '.php3', '.php4', '.php5',
    '.phtml', '.pl', '.shtml', '.stm', '.txt', '.xhtml', '.xml'
]);

/**
 * Filter URLs based on basic formal characteristics.
 * @param {string} url - The URL to filter
 * @returns {boolean} - True if the URL passes the basic filter, false otherwise
 */
function basicFilter(url) {
    return url.startsWith('http') && url.length >= 10 && url.length < 500;
}

/**
 * Find invalid domain/host names.
 * @param {string} domain - The domain to filter
 * @returns {boolean} - True if the domain is valid, false otherwise
 */
function domainFilter(domain) {
    // IPv4 or IPv6
    if ([...domain].every(char => IP_SET.has(char))) {
        try {
            new URL(`http://${domain}`);
            return true;
        } catch (error) {
            return false;
        }
    }

    // malformed domains
    if (!VALID_DOMAIN_PORT.test(domain)) {
        try {
            if (!VALID_DOMAIN_PORT.test(new URL(`http://${domain}`).hostname)) {
                return false;
            }
        } catch (error) {
            return false;
        }
    }

    // unsuitable content
    if (/^\d+$/.test(domain.split('.')[0]) || FILE_TYPE.test(domain)) {
        return false;
    }

    // extensions
    var extensionMatch = EXTENSION_REGEX.exec(domain);
    return !extensionMatch || WHITELISTED_EXTENSIONS.has(extensionMatch[0]);
}

/**
 * Filter based on file extension.
 * @param {string} urlpath - The URL path to filter
 * @returns {boolean} - True if the URL path passes the extension filter, false otherwise
 */
function extensionFilter(urlpath) {
    var extensionMatch = EXTENSION_REGEX.exec(urlpath);
    return !extensionMatch || WHITELISTED_EXTENSIONS.has(extensionMatch[0]);
}

// Simple memoization function
function memoize(fn) {
    var cache = new Map();
    return function(...args) {
        var key = JSON.stringify(args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        var result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

/**
 * Use locale parser to assess the plausibility of the chosen URL segment.
 * @param {string} language - The target language
 * @param {string} segment - The URL segment to assess
 * @param {number} score - The current score
 * @returns {number} - The updated score
 */
var langcodesScore = memoize((language, segment, score) => {
    var delimiter = segment.includes('_') ? '_' : '-';
    try {
        var [lang] = segment.split(delimiter);
        if (lang.toLowerCase() === language.toLowerCase()) {
            score += 1;
        } else {
            score -= 1;
        }
    } catch (error) {
        // Do nothing
    }
    return score;
});

/**
 * Heuristics targeting internationalization and linguistic elements based on a score.
 * @param {string} url - The URL to filter
 * @param {string|null} language - The target language
 * @param {boolean} strict - Whether to use strict filtering
 * @param {boolean} trailingSlash - Whether to consider trailing slashes
 * @returns {boolean} - True if the URL passes the language filter, false otherwise
 */
function langFilter(url, language = null, strict = false, trailingSlash = true) {
    if (language === null) {
        return true;
    }

    let score = 0;
    var match = PATH_LANG_FILTER.exec(url);

    if (match) {
        var occurrences = trailingSlash
            ? url.match(ALL_PATH_LANGS) || []
            : url.match(ALL_PATH_LANGS_NO_TRAILING) || [];

        if (occurrences.length === 1) {
            score = langcodesScore(language, match[1], score);
        } else if (occurrences.length === 2) {
            for (var occurrence of occurrences) {
                score = langcodesScore(language, occurrence[1], score);
            }
        }
    }

    if (strict) {
        var hostMatch = HOST_LANG_FILTER.exec(url);
        if (hostMatch) {
            score += hostMatch[1].toLowerCase() === language.toLowerCase() ? 1 : -1;
        }
    }

    return score >= 0;
}

/**
 * Filters based on URL path: index page, imprint, etc.
 * @param {string} urlpath - The URL path to filter
 * @param {string} query - The URL query string
 * @returns {boolean} - True if the URL path passes the filter, false otherwise
 */
function pathFilter(urlpath, query) {
    if (NOTCRAWLABLE.test(urlpath)) {
        return false;
    }
    return !INDEX_PAGE_FILTER.test(urlpath) || query.length > 0;
}

/**
 * Make sure the target URL is from a suitable type (HTML page with primarily text).
 * @param {string} url - The URL to filter
 * @param {boolean} strict - Whether to use strict filtering
 * @param {boolean} withNav - Whether to include navigation pages
 * @returns {boolean} - True if the URL passes the type filter, false otherwise
 */
function typeFilter(url, strict = false, withNav = false) {
    if (
        url.endsWith('/feed') || url.endsWith('/rss') || url.endsWith('_archive.html') ||
        (SITE_STRUCTURE.test(url) && (!withNav || !isNavigationPage(url))) ||
        (strict && (FILE_TYPE.test(url) || ADULT_AND_VIDEOS.test(url)))
    ) {
        return false;
    }
    return true;
}

/**
 * Parse and validate the input.
 * @param {string|null} url - The URL to validate
 * @returns {[boolean, URL|null]} - A tuple of validation result and parsed URL
 */
function validateUrl(url) {
    try {
        var parsedUrl = new URL(url);
        if (!PROTOCOLS.has(parsedUrl.protocol.slice(0, -1))) {
            return [false, null];
        }
        if (parsedUrl.hostname.length < 5 || (parsedUrl.hostname.startsWith('www.') && parsedUrl.hostname.length < 8)) {
            return [false, null];
        }
        return [true, parsedUrl];
    } catch (error) {
        return [false, null];
    }
}

/**
 * Determine if a given string is a valid URL.
 * @param {string|null} url - The URL to validate
 * @returns {boolean} - True if the URL is valid, false otherwise
 */
function isValidUrl(url) {
    return validateUrl(url)[0];
}

/**
 * Determine if the URL is related to navigation and overview pages rather than content pages.
 * @param {string} url - The URL to check
 * @returns {boolean} - True if the URL is a navigation page, false otherwise
 */
function isNavigationPage(url) {
    return NAVIGATION_FILTER.test(url);
}

/**
 * Run tests to check if the URL may lead to deep web or pages generally not usable in a crawling context.
 * @param {string} url - The URL to check
 * @returns {boolean} - True if the URL is not crawlable, false otherwise
 */
function isNotCrawlable(url) {
    return NOTCRAWLABLE.test(url);
}

module.exports = {
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
};