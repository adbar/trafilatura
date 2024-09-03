// Defines a URL store which holds URLs along with relevant information and entails crawling helpers.

var { normalizeUrl } = require('./clean.js');
var { filterLinks } = require('./core.js');
var { langFilter, validateUrl } = require('./filters.js');
var { clearCaches } = require('./meta.js');
var { getBaseUrl, getHostAndPath, isKnownLink } = require('./urlutils.js');

// Simple logging mechanism
var LOGGER = {
    debug: console.debug,
    info: console.info,
    warn: console.warn,
    error: console.error
};

// Enum for State
var State = {
    OPEN: 1,
    ALL_VISITED: 2,
    BUSTED: 3
};

class DomainEntry {
    constructor(state = State.OPEN) {
        this.count = 0;
        this.rules = null;
        this.state = state;
        this.timestamp = null;
        this.total = 0;
        this.tuples = [];
    }
}

class UrlPathTuple {
    constructor(urlpath, visited) {
        this.urlpath = Buffer.from(urlpath, 'utf-8');
        this.visited = visited;
    }

    path() {
        return this.urlpath.toString('utf-8');
    }
}

class UrlStore {
    constructor({
        compressed = false,
        language = null,
        strict = false,
        trailing = true,
        verbose = false
    } = {}) {
        this.compressed = compressed;
        this.done = false;
        this.language = language;
        this.strict = strict;
        this.trailingSlash = trailing;
        this.urldict = new Map();
    }

    _bufferUrls(data, visited = false) {
        var inputdict = new Map();
        for (var url of new Set(data)) {
            try {
                var [validationResult, parsedUrl] = validateUrl(url);
                if (!validationResult) {
                    LOGGER.debug(`Invalid URL: ${url}`);
                    throw new Error('Invalid URL');
                }
                if (this.language !== null && !langFilter(url, this.language, this.strict, this.trailingSlash)) {
                    LOGGER.debug(`Wrong language: ${url}`);
                    throw new Error('Wrong language');
                }
                var normalizedUrl = normalizeUrl(parsedUrl, {
                    strict: this.strict,
                    language: this.language,
                    trailingSlash: this.trailingSlash
                });
                var [hostinfo, urlpath] = getHostAndPath(normalizedUrl);
                if (!inputdict.has(hostinfo)) {
                    inputdict.set(hostinfo, []);
                }
                inputdict.get(hostinfo).push(new UrlPathTuple(urlpath, visited));
            } catch (error) {
                LOGGER.warn(`Discarding URL: ${url}`);
            }
        }
        return inputdict;
    }

    _loadUrls(domain) {
        if (this.urldict.has(domain)) {
            return this.urldict.get(domain).tuples;
        }
        return [];
    }

    _setDone() {
        if (!this.done && Array.from(this.urldict.values()).every(v => v.state !== State.OPEN)) {
            this.done = true;
        }
    }

    _storeUrls(domain, toRight = null, timestamp = null, toLeft = null) {
        // http/https switch
        if (domain.startsWith('http://')) {
            var candidate = 'https' + domain.slice(4);
            if (this.urldict.has(candidate)) {
                domain = candidate;
            }
        } else if (domain.startsWith('https://')) {
            var candidate = 'http' + domain.slice(5);
            if (this.urldict.has(candidate)) {
                this.urldict.set(domain, this.urldict.get(candidate));
                this.urldict.delete(candidate);
            }
        }

        // load URLs or create entry
        let urls, known;
        if (this.urldict.has(domain)) {
            if (this.urldict.get(domain).state === State.BUSTED) {
                return;
            }
            urls = this._loadUrls(domain);
            known = new Set(urls.map(u => u.path()));
        } else {
            urls = [];
            known = new Set();
        }

        // check if the link or its variants are known
        if (toRight !== null) {
            urls.push(...toRight.filter(t => !isKnownLink(t.path(), known)));
        }
        if (toLeft !== null) {
            urls.unshift(...toLeft.filter(t => !isKnownLink(t.path(), known)));
        }

        if (!this.urldict.has(domain)) {
            this.urldict.set(domain, new DomainEntry());
        }
        this.urldict.get(domain).tuples = urls;
        this.urldict.get(domain).total = urls.length;

        if (timestamp !== null) {
            this.urldict.get(domain).timestamp = timestamp;
        }

        if (urls.every(u => u.visited)) {
            this.urldict.get(domain).state = State.ALL_VISITED;
        } else {
            this.urldict.get(domain).state = State.OPEN;
            if (this.done) {
                this.done = false;
            }
        }
    }

    _searchUrls(urls, switch_ = null) {
        let lastDomain = null;
        let knownPaths = {};
        var remainingUrls = new Set(urls);

        for (var url of Array.from(remainingUrls).sort()) {
            var [hostinfo, urlpath] = getHostAndPath(url);
            if (hostinfo !== lastDomain) {
                lastDomain = hostinfo;
                knownPaths = Object.fromEntries(this._loadUrls(hostinfo).map(u => [u.path(), u.visited]));
            }
            if (urlpath in knownPaths && (switch_ === 1 || (switch_ === 2 && knownPaths[urlpath]))) {
                remainingUrls.delete(url);
            }
        }

        return Array.from(remainingUrls);
    }

    addUrls(urls = null, appendleft = null, visited = false) {
        if (urls) {
            for (var [host, urltuples] of this._bufferUrls(urls, visited)) {
                this._storeUrls(host, urltuples);
            }
        }
        if (appendleft) {
            for (var [host, urltuples] of this._bufferUrls(appendleft, visited)) {
                this._storeUrls(host, null, null, urltuples);
            }
        }
    }

    addFromHtml(htmlstring, url, external = false, lang = null, withNav = true) {
        var baseUrl = getBaseUrl(url);
        var rules = this.getRules(baseUrl);
        var [links, linksPriority] = filterLinks(htmlstring, url, {
            baseUrl,
            external,
            lang: lang || this.language,
            rules,
            strict: this.strict,
            withNav
        });
        this.addUrls(links, linksPriority);
    }

    discard(domains) {
        for (var d of domains) {
            this.urldict.set(d, new DomainEntry(State.BUSTED));
        }
        this._setDone();
    }

    reset() {
        this.urldict = new Map();
        clearCaches();
    }

    getKnownDomains() {
        return Array.from(this.urldict.keys());
    }

    getUnvisitedDomains() {
        return Array.from(this.urldict.entries())
            .filter(([_, v]) => v.state === State.OPEN)
            .map(([d, _]) => d);
    }

    isExhaustedDomain(domain) {
        if (this.urldict.has(domain)) {
            return this.urldict.get(domain).state !== State.OPEN;
        }
        return false;
    }

    unvisitedWebsitesNumber() {
        return this.getUnvisitedDomains().length;
    }

    findKnownUrls(domain) {
        return this._loadUrls(domain).map(u => domain + u.path());
    }

    findUnvisitedUrls(domain) {
        if (!this.isExhaustedDomain(domain)) {
            return this._loadUrls(domain)
                .filter(u => !u.visited)
                .map(u => domain + u.path());
        }
        return [];
    }

    filterUnknownUrls(urls) {
        return this._searchUrls(urls, 1);
    }

    filterUnvisitedUrls(urls) {
        return this._searchUrls(urls, 2);
    }

    hasBeenVisited(url) {
        return this.filterUnvisitedUrls([url]).length === 0;
    }

    isKnown(url) {
        var [hostinfo, urlpath] = getHostAndPath(url);
        return this._loadUrls(hostinfo).some(u => u.path() === urlpath);
    }

    getUrl(domain, asVisited = true) {
        if (!this.isExhaustedDomain(domain)) {
            var urlTuples = this._loadUrls(domain);
            for (var url of urlTuples) {
                if (!url.visited) {
                    if (asVisited) {
                        url.visited = true;
                        this.urldict.get(domain).count += 1;
                        this._storeUrls(domain, urlTuples, new Date());
                    }
                    return domain + url.path();
                }
            }
        }
        this.urldict.get(domain).state = State.ALL_VISITED;
        this._setDone();
        return null;
    }

    getDownloadUrls(timeLimit = 10, maxUrls = 10000) {
        var urls = [];
        for (var [website, entry] of this.urldict.entries()) {
            if (entry.state !== State.OPEN) {
                continue;
            }
            if (!entry.timestamp || (new Date() - entry.timestamp) / 1000 > timeLimit) {
                var url = this.getUrl(website);
                if (url !== null) {
                    urls.push(url);
                    if (urls.length >= maxUrls) {
                        break;
                    }
                }
            }
        }
        this._setDone();
        return urls;
    }

    establishDownloadSchedule(maxUrls = 100, timeLimit = 10) {
        var potential = this.getUnvisitedDomains();
        if (potential.length === 0) {
            return [];
        }

        var perDomain = Math.max(Math.floor(maxUrls / potential.length), 1);
        var targets = [];

        for (var domain of potential) {
            var urlTuples = this._loadUrls(domain);
            var urlpaths = [];

            for (var url of urlTuples) {
                if (urlpaths.length >= perDomain || (targets.length + urlpaths.length) >= maxUrls) {
                    break;
                }
                if (!url.visited) {
                    urlpaths.push(url.path());
                    url.visited = true;
                    this.urldict.get(domain).count += 1;
                }
            }

            var now = new Date();
            var originalTimestamp = this.urldict.get(domain).timestamp;
            let scheduleSecs = 0;

            if (!originalTimestamp || (now - originalTimestamp) / 1000 > timeLimit) {
                scheduleSecs = 0;
            } else {
                scheduleSecs = timeLimit - (now - originalTimestamp) / 1000;
            }

            for (var urlpath of urlpaths) {
                targets.push([scheduleSecs, domain + urlpath]);
                scheduleSecs += timeLimit;
            }

            var totalDiff = new Date(now.getTime() + (scheduleSecs - timeLimit) * 1000);
            this._storeUrls(domain, urlTuples, totalDiff);
        }

        this._setDone();
        return targets.sort((a, b) => a[1].localeCompare(b[1]));
    }

    storeRules(website, rules) {
        if (!this.urldict.has(website)) {
            this.urldict.set(website, new DomainEntry());
        }
        this.urldict.get(website).rules = rules;
    }

    getRules(website) {
        if (this.urldict.has(website)) {
            return this.urldict.get(website).rules;
        }
        return null;
    }

    getCrawlDelay(website, defaultDelay = 5) {
        var rules = this.getRules(website);
        if (rules && typeof rules.getCrawlDelay === 'function') {
            var delay = rules.getCrawlDelay('*');
            if (delay !== null) {
                return delay;
            }
        }
        return defaultDelay;
    }

    getAllCounts() {
        return Array.from(this.urldict.values()).map(v => v.count);
    }

    totalUrlNumber() {
        return Array.from(this.urldict.values()).reduce((sum, v) => sum + v.total, 0);
    }

    downloadThresholdReached(threshold) {
        return Array.from(this.urldict.values()).some(v => v.count >= threshold);
    }

    dumpUrls() {
        return Array.from(this.urldict.keys()).flatMap(domain => this.findKnownUrls(domain));
    }

    printUnvisitedUrls() {
        for (var domain of this.urldict.keys()) {
            console.log(this.findUnvisitedUrls(domain).join('\n'));
        }
    }

    printUrls() {
        for (var domain of this.urldict.keys()) {
            console.log(
                this._loadUrls(domain)
                    .map(u => `${domain}${u.path()}\t${u.visited}`)
                    .join('\n')
            );
        }
    }
}

module.exports = {
    UrlStore
};