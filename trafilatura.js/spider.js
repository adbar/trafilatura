// Functions dedicated to website navigation and crawling/spidering.

var { JSDOM } = require('jsdom');
var { URL } = require('url');
var { UrlStore, extractLinks, fixRelativeUrls, getBaseUrl, isNavigationPage, isNotCrawlable } = require('./courlan');
var { baseline, pruneUnwantedNodes } = require('./core');
var { Response, fetchResponse, fetchUrl } = require('./downloads');
var { DEFAULT_CONFIG } = require('./settings');
var { LANGID_FLAG, decodeFile, loadHtml } = require('./utils');

let langid;
try {
    langid = require('languagedetect');
} catch (error) {
    console.warn('languagedetect module not found. Language detection will be disabled.');
}

var LOGGER = console;

var URL_STORE = new UrlStore({ compressed: false, strict: false });

var ROBOTS_TXT_URL = "/robots.txt";
var MAX_SEEN_URLS = 10;
var MAX_KNOWN_URLS = 100000;

class CrawlParameters {
    constructor(start, lang = null, rules = null, pruneXpath = null) {
        this.start = start;
        this.base = this._getBaseUrl(start);
        this.ref = this._getReference(start);
        this.lang = lang;
        this.rules = rules || getRules(this.base);
        this.i = 0;
        this.knownNum = 0;
        this.isOn = true;
        this.pruneXpath = pruneXpath;
    }

    _getBaseUrl(start) {
        var base = getBaseUrl(start);
        if (!base) {
            throw new Error(`cannot start crawl: ${start}`);
        }
        return base;
    }

    _getReference(start) {
        return start.split('/').slice(0, 3).join('/');
    }

    updateMetadata(urlStore) {
        this.isOn = urlStore.findUnvisitedUrls(this.base).length > 0;
        this.knownNum = urlStore.findKnownUrls(this.base).length;
    }

    filterList(todo) {
        if (!todo) return [];
        return todo.filter(u => u !== this.start && u.startsWith(this.ref));
    }

    isValidLink(link) {
        return (
            (!this.rules || this.rules.canFetch("*", link)) &&
            link.startsWith(this.ref) &&
            !isNotCrawlable(link)
        );
    }
}

function refreshDetection(htmlstring, homepage) {
    if (!htmlstring.includes('"refresh"') && !htmlstring.includes('"REFRESH"')) {
        return [htmlstring, homepage];
    }

    var dom = new JSDOM(htmlstring);
    var doc = dom.window.document;

    var metaRefresh = doc.querySelector('meta[http-equiv="refresh"], meta[http-equiv="REFRESH"]');
    if (!metaRefresh) {
        LOGGER.info(`no redirect found: ${homepage}`);
        return [htmlstring, homepage];
    }

    var content = metaRefresh.getAttribute('content');
    if (!content || !content.includes(';')) {
        LOGGER.info(`no redirect found: ${homepage}`);
        return [htmlstring, homepage];
    }

    let url2 = content.split(';')[1].trim().toLowerCase().replace('url=', '');
    if (!url2.startsWith('http')) {
        var baseUrl = getBaseUrl(homepage);
        url2 = fixRelativeUrls(baseUrl, url2);
    }

    var newHtmlstring = fetchUrl(url2);
    if (!newHtmlstring) {
        LOGGER.warning(`failed redirect: ${url2}`);
        return [null, null];
    }

    LOGGER.info(`successful redirect: ${url2}`);
    return [newHtmlstring, url2];
}

async function probeAlternativeHomepage(homepage) {
    var response = await fetchResponse(homepage, { decode: false });
    if (!response || !response.data) {
        return [null, null, null];
    }

    if (response.url !== homepage && response.url !== '/') {
        LOGGER.info(`followed homepage redirect: ${response.url}`);
        homepage = response.url;
    }

    var htmlstring = decodeFile(response.data);

    var [newHtmlstring, newHomepage] = refreshDetection(htmlstring, homepage);
    if (newHomepage === null) {
        return [null, null, null];
    }

    LOGGER.debug(`fetching homepage OK: ${newHomepage}`);
    return [newHtmlstring, newHomepage, getBaseUrl(newHomepage)];
}

function parseRobots(robotsUrl, data) {
    // This is a simplified version. You might want to use a more robust robots.txt parser library for JavaScript
    var rules = {
        canFetch: (userAgent, url) => {
            // Implement robots.txt parsing logic here
            return true; // Default to allowing all
        }
    };
    return rules;
}

function getRules(baseUrl) {
    var robotsUrl = baseUrl + ROBOTS_TXT_URL;
    var data = fetchUrl(robotsUrl);
    return data ? parseRobots(robotsUrl, data) : null;
}

function isTargetLanguage(htmlstring, language) {
    if (htmlstring && language && LANGID_FLAG && langid) {
        var [, text] = baseline(htmlstring);
        var [result] = langid.classify(text);
        return result === language;
    }
    return true;
}

function isStillNavigation(todo) {
    return todo.some(isNavigationPage);
}

function processLinks(htmlstring, params, url = "") {
    if (!isTargetLanguage(htmlstring, params.lang)) {
        return;
    }

    if (htmlstring && params.pruneXpath) {
        var pruneXpaths = Array.isArray(params.pruneXpath) ? params.pruneXpath : [params.pruneXpath];
        var dom = new JSDOM(htmlstring);
        var doc = dom.window.document;
        pruneXpaths.forEach(xpath => {
            var elements = doc.evaluate(xpath, doc, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
            for (let i = 0; i < elements.snapshotLength; i++) {
                var element = elements.snapshotItem(i);
                element.parentNode.removeChild(element);
            }
        });
        htmlstring = dom.serialize();
    }

    var links = [];
    var linksPriority = [];
    
    extractLinks(htmlstring, url || params.base, false, params.lang, true, false)
        .forEach(link => {
            if (!params.isValidLink(link)) return;
            if (isNavigationPage(link)) {
                linksPriority.push(link);
            } else {
                links.push(link);
            }
        });

    URL_STORE.addUrls(links);
    URL_STORE.addUrls(linksPriority, true);
}

function processResponse(response, params) {
    if (!response || !response.data) return;
    
    URL_STORE.addUrls([response.url], true);
    processLinks(decodeFile(response.data), params, params.base);
}

function initCrawl(start, lang = null, rules = null, todo = null, known = null, pruneXpath = null) {
    var params = new CrawlParameters(start, lang, rules, pruneXpath);

    URL_STORE.addUrls(known || [], true);
    URL_STORE.addUrls(params.filterList(todo));
    URL_STORE.storeRules(params.base, params.rules);

    if (!todo) {
        URL_STORE.addUrls([params.start], false);
        params = crawlPage(params, true);
    } else {
        params.updateMetadata(URL_STORE);
    }

    return params;
}

function crawlPage(params, initial = false) {
    var url = URL_STORE.getUrl(params.base);
    if (!url) {
        params.isOn = false;
        params.knownNum = URL_STORE.findKnownUrls(params.base).length;
        return params;
    }

    params.i++;

    if (initial) {
        var [htmlstring, homepage, newBaseUrl] = probeAlternativeHomepage(url);
        if (htmlstring && homepage && newBaseUrl) {
            URL_STORE.addUrls([homepage]);
            processLinks(htmlstring, params, url);
        }
    } else {
        var response = fetchResponse(url, { decode: false });
        processResponse(response, params);
    }

    params.updateMetadata(URL_STORE);
    return params;
}

function focusedCrawler(homepage, maxSeenUrls = MAX_SEEN_URLS, maxKnownUrls = MAX_KNOWN_URLS, todo = null, knownLinks = null, lang = null, config = DEFAULT_CONFIG, rules = null, pruneXpath = null) {
    let params = initCrawl(homepage, lang, rules, todo, knownLinks, pruneXpath);

    var sleepTime = URL_STORE.getCrawlDelay(params.base, config.SLEEP_TIME);

    while (params.isOn && params.i < maxSeenUrls && params.knownNum < maxKnownUrls) {
        params = crawlPage(params);
        // In JavaScript, we don't have a direct equivalent to Python's time.sleep()
        // You might want to use setTimeout() or a sleep function that returns a Promise
        // For simplicity, we'll just continue the loop immediately
    }

    todo = Array.from(new Set(URL_STORE.findUnvisitedUrls(params.base)));
    knownLinks = Array.from(new Set(URL_STORE.findKnownUrls(params.base)));
    return [todo, knownLinks];
}

module.exports = {
    focusedCrawler,
    CrawlParameters,
    URL_STORE
};