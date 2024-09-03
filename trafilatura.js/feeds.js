// Examining feeds and extracting links for further processing.

var { JSDOM } = require('jsdom');
var { URL } = require('url');
var axios = require('axios');

var FEED_TYPES = new Set([
    "application/atom",
    "application/atom+xml",
    "application/feed+json",
    "application/json",
    "application/rdf",
    "application/rdf+xml",
    "application/rss",
    "application/rss+xml",
    "application/x.atom+xml",
    "application/x-atom+xml",
    "application/xml",
    "text/atom",
    "text/atom+xml",
    "text/plain",
    "text/rdf",
    "text/rdf+xml",
    "text/rss",
    "text/rss+xml",
    "text/xml",
]);

var FEED_OPENING = /^<(feed|rss|\?xml)/;
var LINK_ATTRS = /<link .*?href=".+?">/g;
var LINK_HREF = /href="(.+?)"/;
var LINK_ELEMENTS = /<link>(?:\s*)(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?(?:\s*)<\/link>/g;
var BLACKLIST = /\bcomments\b/;
var LINK_VALIDATION_RE = /\.(atom|rdf|rss|xml)$|\b(atom|rss)\b|\?type=100$|feeds\/posts\/default\/?$|\?feed=(atom|rdf|rss|rss2)|feed$/;

var MAX_LINKS = 1000; // Adjust as needed

class FeedParameters {
    constructor(baseurl, domain, reference, external = false, targetLang = null) {
        this.base = baseurl;
        this.domain = domain;
        this.ext = external;
        this.lang = targetLang;
        this.ref = reference;
    }
}

function isPotentialFeed(feedString) {
    if (FEED_OPENING.test(feedString)) {
        return true;
    }
    var beginning = feedString.slice(0, 100);
    return beginning.includes("<rss") || beginning.includes("<feed");
}

function handleLinkList(linklist, params) {
    var outputLinks = [];

    for (var item of new Set(linklist).values()) {
        var link = new URL(item, params.base).href;
        // Implement check_url, is_similar_domain functions as needed
        // var checked = checkUrl(link, params.lang);

        // if (checked) {
        //     if (!params.ext && !link.includes('feed') && !isSimilarDomain(params.domain, checked[1])) {
        //         console.warn(`Rejected, diverging domain names: ${params.domain} ${checked[1]}`);
        //     } else {
        //         outputLinks.push(checked[0]);
        //     }
        // } else 
        if (link.includes("feedburner") || link.includes("feedproxy")) {
            outputLinks.push(link);
        }
    }

    return outputLinks;
}

function findLinks(feedString, params) {
    if (!isPotentialFeed(feedString)) {
        if (feedString.startsWith("{")) {
            try {
                var jsonFeed = JSON.parse(feedString);
                var candidates = (jsonFeed.items || []).map(item => item.url || item.id).filter(Boolean);
                return candidates.slice(0, MAX_LINKS);
            } catch (error) {
                console.debug(`JSON decoding error: ${params.domain}`);
            }
        } else {
            console.debug(`Possibly invalid feed: ${params.domain}`);
        }
        return [];
    }

    if (feedString.includes("<link ")) {
        return Array.from(feedString.matchAll(LINK_ATTRS))
            .map(match => LINK_HREF.exec(match[0])?.[1])
            .filter(link => link && !link.includes("atom+xml") && !link.includes('rel="self"'))
            .slice(0, MAX_LINKS);
    }

    if (feedString.includes("<link>")) {
        return Array.from(feedString.matchAll(LINK_ELEMENTS))
            .map(match => match[1].trim())
            .slice(0, MAX_LINKS);
    }

    return [];
}

function extractLinks(feedString, params) {
    if (!feedString) {
        console.debug(`Empty feed: ${params.domain}`);
        return [];
    }

    var feedLinks = findLinks(feedString.trim(), params);
    var outputLinks = handleLinkList(feedLinks, params)
        .filter(link => link !== params.ref && (link.match(/\//g) || []).length > 2);

    if (feedLinks.length) {
        console.debug(`Links found: ${feedLinks.length} of which ${outputLinks.length} valid`);
    } else {
        console.debug(`Invalid feed for ${params.domain}`);
    }

    return outputLinks;
}

function determineFeed(htmlString, params) {
    var dom = new JSDOM(htmlString);
    var document = dom.window.document;

    if (!document) {
        console.debug(`Invalid HTML/Feed page: ${params.base}`);
        return [];
    }

    let feedUrls = Array.from(document.querySelectorAll('link[rel="alternate"][href]'))
        .filter(link => FEED_TYPES.has(link.getAttribute('type')) || LINK_VALIDATION_RE.test(link.getAttribute('href')))
        .map(link => link.getAttribute('href'));

    if (feedUrls.length === 0) {
        feedUrls = Array.from(document.querySelectorAll('a[href]'))
            .filter(link => LINK_VALIDATION_RE.test(link.getAttribute('href')))
            .map(link => link.getAttribute('href'));
    }

    var outputUrls = [...new Set(feedUrls)]
        .map(link => new URL(link, params.base).href)
        .filter(link => link && link !== params.ref && !BLACKLIST.test(link));

    console.debug(`Feed URLs found: ${feedUrls.length} of which ${outputUrls.length} valid`);
    return outputUrls;
}

async function probeGnews(params, urlfilter) {
    if (params.lang) {
        try {
            var response = await axios.get(`https://news.google.com/rss/search?q=site:${params.domain}&hl=${params.lang}&scoring=n&num=100`);
            if (response.data) {
                var feedLinks = extractLinks(response.data, params);
                // Implement filter_urls function as needed
                // var filteredLinks = filterUrls(feedLinks, urlfilter);
                console.debug(`${feedLinks.length} Google news links found for ${params.domain}`);
                return feedLinks;
            }
        } catch (error) {
            console.error(`Error fetching Google News feed: ${error}`);
        }
    }
    return [];
}

async function findFeedUrls(url, targetLang = null, external = false, sleepTime = 2000) {
    var parsedUrl = new URL(url);
    var domain = parsedUrl.hostname;
    var baseurl = `${parsedUrl.protocol}//${parsedUrl.host}`;

    if (!domain) {
        console.warn(`Invalid URL: ${url}`);
        return [];
    }

    var params = new FeedParameters(baseurl, domain, url, external, targetLang);
    let urlfilter = null;

    try {
        var response = await axios.get(url);
        var downloaded = response.data;

        if (downloaded) {
            let feedLinks = extractLinks(downloaded, params);

            if (feedLinks.length === 0) {
                var feedUrls = determineFeed(downloaded, params);
                for (var feed of feedUrls) {
                    var feedResponse = await axios.get(feed);
                    feedLinks = feedLinks.concat(extractLinks(feedResponse.data, params));
                }

                if (url.length > baseurl.length + 2) {
                    urlfilter = url;
                }
            }

            if (feedLinks.length > 0) {
                // Implement filter_urls function as needed
                // feedLinks = filterUrls(feedLinks, urlfilter);
                console.debug(`${feedLinks.length} feed links found for ${domain}`);
                return feedLinks;
            }

            console.debug(`No usable feed links found: ${url}`);
        } else {
            console.error(`Could not download web page: ${url}`);
            if (url.replace(/\/$/, '') !== baseurl) {
                await new Promise(resolve => setTimeout(resolve, sleepTime));
                return tryHomepage(baseurl, targetLang);
            }
        }
    } catch (error) {
        console.error(`Error fetching URL: ${error}`);
    }

    return probeGnews(params, urlfilter);
}

async function tryHomepage(baseurl, targetLang) {
    console.debug(`Probing homepage for feeds instead: ${baseurl}`);
    return findFeedUrls(baseurl, targetLang);
}

module.exports = {
    findFeedUrls,
    tryHomepage
};