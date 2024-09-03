// Deriving link info from sitemaps.

var { URL } = require('url');
var { cleanUrl, extractDomain, filterUrls, fixRelativeUrls, getHostinfo, langFilter } = require('./courlan');
var { isSimilarDomain } = require('./deduplication');
var { fetchUrl, isLivePage } = require('./downloads');
var { MAX_LINKS, MAX_SITEMAPS_SEEN } = require('./settings');

var LINK_REGEX = /<loc>(?:<!\[CDATA\[)?(http.+?)(?:\]\]>)?<\/loc>/g;
var XHTML_REGEX = /<xhtml:link.+?>/gs;
var HREFLANG_REGEX = /href=['"](.+?)['"]/;
var WHITELISTED_PLATFORMS = /(?:blogger|blogpost|ghost|hubspot|livejournal|medium|typepad|squarespace|tumblr|weebly|wix|wordpress)\./;

var SITEMAP_FORMAT = /^.{0,5}<\?xml|<sitemap|<urlset/;
var DETECT_SITEMAP_LINK = /\.xml(\..{2,4})?$|\.xml[?#]/;
var DETECT_LINKS = /https?:\/\/[^\s<"]+/g;
var SCRUB_REGEX = /\?.*$|#.*$/;
var POTENTIAL_SITEMAP = /\.xml\b/;

var GUESSES = [
    "sitemap.xml",
    "sitemap.xml.gz",
    "sitemap",
    "sitemap_index.xml",
    "sitemap_news.xml",
];

class SitemapObject {
    constructor(baseUrl, domain, sitemapUrls, targetLang = null, external = false) {
        this.baseUrl = baseUrl;
        this.content = "";
        this.domain = domain;
        this.external = external;
        this.currentUrl = "";
        this.seen = new Set();
        this.sitemapUrls = sitemapUrls;
        this.targetLang = targetLang;
        this.urls = [];
    }

    async fetch() {
        console.debug("fetching sitemap:", this.currentUrl);
        this.content = await fetchUrl(this.currentUrl);
        this.seen.add(this.currentUrl);
    }

    handleLink(link) {
        if (link === this.currentUrl) return;

        link = fixRelativeUrls(this.baseUrl, link);
        link = cleanUrl(link, this.targetLang);

        if (!link || !langFilter(link, this.targetLang)) return;

        var newDomain = extractDomain(link, { fast: true });
        if (!newDomain) {
            console.error("couldn't extract domain:", link);
            return;
        }

        if (!this.external && !WHITELISTED_PLATFORMS.test(newDomain) && !isSimilarDomain(this.domain, newDomain)) {
            console.warn("link discarded, diverging domain names:", this.domain, newDomain);
            return;
        }

        if (DETECT_SITEMAP_LINK.test(link)) {
            this.sitemapUrls.push(link);
        } else {
            this.urls.push(link);
        }
    }

    extractLinks(regex, index, handler) {
        let match;
        let count = 0;
        while ((match = regex.exec(this.content)) !== null && count < MAX_LINKS) {
            handler(match[index]);
            count++;
        }
        console.debug(
            `${this.sitemapUrls.length} sitemaps and ${this.urls.length} links found for ${this.currentUrl}`
        );
    }

    extractSitemapLanglinks() {
        if (!this.content.includes("hreflang=")) return;

        var langRegex = new RegExp(`hreflang=['"](?:${this.targetLang}.*?|x-default)['"]`, 'g');

        var handleLangLink = (attrs) => {
            if (langRegex.test(attrs)) {
                var langMatch = HREFLANG_REGEX.exec(attrs);
                if (langMatch) {
                    this.handleLink(langMatch[1]);
                }
            }
        };

        this.extractLinks(XHTML_REGEX, 0, handleLangLink);
    }

    extractSitemapLinks() {
        this.extractLinks(LINK_REGEX, 1, this.handleLink.bind(this));
    }

    process() {
        var plausible = isPlausibleSitemap(this.currentUrl, this.content);
        if (!plausible) return;

        if (!SITEMAP_FORMAT.test(this.content)) {
            this.extractLinks(DETECT_LINKS, 0, this.handleLink.bind(this));
            return;
        }

        if (this.targetLang !== null) {
            this.extractSitemapLanglinks();
            if (this.sitemapUrls.length > 0 || this.urls.length > 0) return;
        }
        this.extractSitemapLinks();
    }
}

async function sitemapSearch(url, targetLang = null, external = false, sleepTime = 2000) {
    var [domainname, baseurl] = getHostinfo(url);
    if (!domainname) {
        console.warn("invalid URL:", url);
        return [];
    }

    if (!await isLivePage(baseurl)) {
        console.warn("base URL unreachable, dropping sitemap:", url);
        return [];
    }

    let urlfilter = null;

    let sitemapurls = url.endsWith('.gz') || url.endsWith('sitemap') || url.endsWith('.xml') ? [url] : [];

    if (url.length > baseurl.length + 2) {
        urlfilter = url;
    }

    var sitemap = new SitemapObject(baseurl, domainname, sitemapurls, targetLang, external);

    if (sitemap.sitemapUrls.length === 0) {
        sitemap.sitemapUrls = await findRobotsSitemaps(baseurl) || GUESSES.map(g => `${baseurl}/${g}`);
    }

    while (sitemap.sitemapUrls.length > 0 && sitemap.seen.size < MAX_SITEMAPS_SEEN) {
        sitemap.currentUrl = sitemap.sitemapUrls.pop();
        await sitemap.fetch();
        sitemap.process();
        sitemap.sitemapUrls = sitemap.sitemapUrls.filter(s => !sitemap.seen.has(s));

        if (sitemap.seen.size < MAX_SITEMAPS_SEEN) {
            await new Promise(resolve => setTimeout(resolve, sleepTime));
        }
    }

    if (urlfilter) {
        sitemap.urls = filterUrls(sitemap.urls, urlfilter);
    }

    console.debug(`${sitemap.urls.length} sitemap links found for ${domainname}`);
    return sitemap.urls;
}

function isPlausibleSitemap(url, contents) {
    if (!contents) return false;

    url = url.replace(SCRUB_REGEX, '');

    if ((POTENTIAL_SITEMAP.test(url) && !SITEMAP_FORMAT.test(contents)) || contents.toLowerCase().includes('<html')) {
        console.warn("not a valid XML sitemap:", url);
        return false;
    }

    return true;
}

async function findRobotsSitemaps(baseurl) {
    var robotstxt = await fetchUrl(baseurl + "/robots.txt");
    return extractRobotsSitemaps(robotstxt, baseurl);
}

function extractRobotsSitemaps(robotstxt, baseurl) {
    if (!robotstxt || robotstxt.length > 10000) return [];

    var sitemapurls = [];
    var lines = robotstxt.split('\n');

    for (var line of lines) {
        var trimmedLine = line.split('#')[0].trim();
        if (!trimmedLine) continue;

        var [key, value] = trimmedLine.split(':', 2).map(s => s.trim());
        if (key && value && key.toLowerCase() === 'sitemap') {
            var candidate = fixRelativeUrls(baseurl, value);
            sitemapurls.push(candidate);
        }
    }

    console.debug(`${sitemapurls.length} sitemaps found in robots.txt`);
    return sitemapurls;
}

module.exports = {
    sitemapSearch,
    isPlausibleSitemap,
    findRobotsSitemaps,
    extractRobotsSitemaps
};