// Functions performing URL trimming and cleaning

// Note: Logging functionality would need to be implemented or replaced with console.log
// var LOGGER = { debug: console.log };

// Import statements would need to be adjusted based on your JavaScript environment
// import { isValidUrl } from './filters.js';
// import { ALLOWED_PARAMS, LANG_PARAMS, TARGET_LANGS } from './settings.js';
// import { _parse } from './urlutils.js';

// Regular expressions
var PROTOCOLS = /https?:\/\//;
var SELECTION = /(https?:\/\/[^">&? ]+?)(?:https?:\/\/)|(?:https?:\/\/[^/]+?\/[^/]+?[&?]u(?:rl)?=)(https?:\/\/[^"> ]+)/;
var MIDDLE_URL = /https?:\/\/.+?(https?:\/\/.+?)(?:https?:\/\/|$)/;
var NETLOC_RE = /(?<=\w):(?:80|443)/;
var PATH1 = /\/+/g;
var PATH2 = /^(?:\/\.\.(?![^/]))+/;
var REMAINING_MARKUP = /<\/?[a-z]{,4}?>|{.+?}/g;
var TRAILING_AMP = /\/\&$/;
var TRAILING_PARTS = /(.*?)[<>"\s]/;
var TRACKERS_RE = /^(?:dc|fbc|gc|twc|yc|ysc)lid|^(?:click|gbra|msclk|igsh|partner|wbra)id|^(?:ads?|mc|ga|gs|itm|mc|mkt|ml|mtm|oly|pk|utm|vero)_|(?:\b|_)(?:aff|affi|affiliate|campaign|cl?id|eid|ga|gl|kwd|keyword|medium|ref|referr?er|session|source|uid|xtor)/;

/**
 * Helper function: chained scrubbing and normalization
 * @param {string} url - The URL to clean
 * @param {string|null} [language=null] - The language to use for cleaning
 * @returns {string|null} - The cleaned URL or null if invalid
 */
function cleanUrl(url, language = null) {
    try {
        return normalizeUrl(scrubUrl(url), false, language);
    } catch (error) {
        return null;
    }
}

/**
 * Strip unnecessary parts and make sure only one URL is considered
 * @param {string} url - The URL to scrub
 * @returns {string} - The scrubbed URL
 */
function scrubUrl(url) {
    // Remove leading/trailing space and unescaped control chars
    url = url.replace(/\s/g, '').trim();

    // <![CDATA[http://...]]>
    if (url.startsWith('<![CDATA[')) {
        url = url.replace('<![CDATA[', '').replace(']]>', '');
    }

    // Markup rests
    url = url.replace(REMAINING_MARKUP, '');

    // & and &amp;
    url = url.replace(/&amp;/g, '&').replace(TRAILING_AMP, '');

    // Double/faulty URLs
    var protocols = url.match(PROTOCOLS);
    if (protocols && protocols.length > 1 && !url.includes('web.archive.org')) {
        console.log(`double url: ${protocols.length} ${url}`);
        let match = url.match(SELECTION);
        if (match && isValidUrl(match[1])) {
            url = match[1];
            console.log(`taking url: ${url}`);
        } else {
            match = url.match(MIDDLE_URL);
            if (match && isValidUrl(match[1])) {
                url = match[1];
                console.log(`taking url: ${url}`);
            }
        }
    }

    // Too long and garbled URLs e.g. due to quotes URLs
    match = url.match(TRAILING_PARTS);
    if (match) {
        url = match[1];
    }
    if (url.length > 500) {
        console.log(`invalid-looking link ${url.slice(0, 50)}… of length ${url.length}`);
    }

    // Trailing slashes in URLs without path or in embedded URLs
    if ((url.match(/\//g) || []).length === 3 || (url.match(/:\/\//g) || []).length > 1) {
        url = url.replace(/\/$/, '');
    }

    return url;
}

/**
 * Strip unwanted query elements
 * @param {string} querystring - The query string to clean
 * @param {boolean} [strict=false] - Whether to use strict cleaning
 * @param {string|null} [language=null] - The language to use for cleaning
 * @returns {string} - The cleaned query string
 */
function cleanQuery(querystring, strict = false, language = null) {
    if (!querystring) {
        return '';
    }

    var qdict = new URLSearchParams(querystring);
    var newqdict = new URLSearchParams();

    for (var [qelem, value] of qdict.entries()) {
        var teststr = qelem.toLowerCase();
        // Control param
        if (strict) {
            if (!ALLOWED_PARAMS.includes(teststr) && !LANG_PARAMS.includes(teststr)) {
                continue;
            }
        }
        // Get rid of trackers
        else if (TRACKERS_RE.test(teststr)) {
            continue;
        }
        // Control language
        if (language in TARGET_LANGS && LANG_PARAMS.includes(teststr) && !TARGET_LANGS[language].includes(value)) {
            console.log(`bad lang: ${language} ${qelem}`);
            throw new Error('Invalid language');
        }
        // Insert
        newqdict.append(qelem, value);
    }

    return newqdict.toString();
}

/**
 * Probe for punycode in lower-cased hostname and try to decode it
 * @param {string} string - The string to decode
 * @returns {string} - The decoded string
 */
function decodePunycode(string) {
    if (!string.includes('xn--')) {
        return string;
    }

    var parts = string.split('.').map(part => {
        if (part.toLowerCase().startsWith('xn--')) {
            try {
                return punycode.decode(part.slice(4));
            } catch (error) {
                console.log(`invalid utf/idna string: ${part}`);
                return part;
            }
        }
        return part;
    });

    return parts.join('.');
}

/**
 * Normalize URLs parts (specifically path and fragment) while accounting for certain characters
 * @param {string} urlPart - The URL part to normalize
 * @returns {string} - The normalized URL part
 */
function normalizePart(urlPart) {
    return encodeURIComponent(urlPart).replace(/%2F/g, '/').replace(/%21/g, '!').replace(/%3D/g, '=').replace(/%3A/g, ':').replace(/%2C/g, ',').replace(/%2D/g, '-');
}

/**
 * Look for trackers in URL fragments using query analysis, normalize the output
 * @param {string} fragment - The fragment to normalize
 * @param {string|null} [language=null] - The language to use for normalization
 * @returns {string} - The normalized fragment
 */
function normalizeFragment(fragment, language = null) {
    if (fragment.includes('=')) {
        if (fragment.includes('&')) {
            fragment = cleanQuery(fragment, false, language);
        } else if (TRACKERS_RE.test(fragment)) {
            fragment = '';
        }
    }
    return normalizePart(fragment);
}

/**
 * Takes a URL string or a parsed URL and returns a normalized URL string
 * @param {string|URL} parsedUrl - The URL to normalize
 * @param {boolean} [strict=false] - Whether to use strict normalization
 * @param {string|null} [language=null] - The language to use for normalization
 * @param {boolean} [trailingSlash=true] - Whether to keep trailing slashes
 * @returns {string} - The normalized URL
 */
function normalizeUrl(parsedUrl, strict = false, language = null, trailingSlash = true) {
    if (typeof parsedUrl === 'string') {
        parsedUrl = new URL(parsedUrl);
    }

    // Lowercase + remove fragments + normalize punycode
    var scheme = parsedUrl.protocol.slice(0, -1);
    let netloc = decodePunycode(parsedUrl.hostname.toLowerCase());

    // Port
    if (parsedUrl.port === '80' || parsedUrl.port === '443') {
        netloc = netloc.replace(NETLOC_RE, '');
    }

    // Path
    let newpath = normalizePart(parsedUrl.pathname.replace(PATH2, '').replace(PATH1, '/'));

    // Strip unwanted query elements
    var newquery = cleanQuery(parsedUrl.search.slice(1), strict, language);

    if (newquery && !newpath) {
        newpath = '/';
    } else if (!trailingSlash && !newquery && newpath.length > 1 && newpath.endsWith('/')) {
        newpath = newpath.replace(/\/$/, '');
    }

    // Fragment
    var newfragment = strict ? '' : normalizeFragment(parsedUrl.hash.slice(1), language);

    // Rebuild
    return `${scheme}://${netloc}${newpath}${newquery ? '?' + newquery : ''}${newfragment ? '#' + newfragment : ''}`;
}

// Export the functions
export {
    cleanUrl,
    scrubUrl,
    cleanQuery,
    decodePunycode,
    normalizePart,
    normalizeFragment,
    normalizeUrl
};