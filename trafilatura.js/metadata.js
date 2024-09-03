// Module bundling all functions needed to scrape metadata from webpages.

var { JSDOM } = require('jsdom');
var { extractDomain, getBaseUrl, isValidUrl, normalizeUrl, validateUrl } = require('./courlan');
var { findDate } = require('./htmldate');

var { pruneUnwantedNodes } = require('./htmlprocessing');
var { extractJson, extractJsonParseError, normalizeAuthors, normalizeJson } = require('./json_metadata');
var { Document, setDateParams } = require('./settings');
var { HTML_STRIP_TAGS, lineProcessing, loadHtml, trim } = require('./utils');
var { AUTHOR_DISCARD_XPATHS, AUTHOR_XPATHS, CATEGORIES_XPATHS, TAGS_XPATHS, TITLE_XPATHS } = require('./xpaths');

var META_URL = /https?:\/\/(?:www\.|w[0-9]+\.)?([^/]+)/;
var JSON_MINIFY = /("(?:\\"|[^"])*")|\s/g;
var HTMLTITLE_REGEX = /^(.+)?\s+[–•·—|⁄*⋆~‹«<›»>:-]\s+(.+)$/;
var CLEAN_META_TAGS = /["']/g;
var LICENSE_REGEX = /(by-nc-nd|by-nc-sa|by-nc|by-nd|by-sa|by|zero)\/([1-9]\.[0-9])/;
var TEXT_LICENSE_REGEX = /(cc|creative commons) (by-nc-nd|by-nc-sa|by-nc|by-nd|by-sa|by|zero) ?([1-9]\.[0-9])?/i;

var METANAME_AUTHOR = new Set([
    'article:author', 'atc-metaauthor', 'author', 'authors', 'byl', 'citation_author',
    'creator', 'dc.creator', 'dc.creator.aut', 'dc:creator',
    'dcterms.creator', 'dcterms.creator.aut', 'dcsext.author', 'parsely-author',
    'rbauthors', 'sailthru.author', 'shareaholic:article_author_name'
]);

// ... (other constant sets)

function normalizeTags(tags) {
    tags = tags.replace(CLEAN_META_TAGS, '').trim();
    return tags.split(', ').filter(Boolean).join(', ');
}

function checkAuthors(authors, authorBlacklist) {
    var blacklist = new Set(Array.from(authorBlacklist).map(a => a.toLowerCase()));
    var newAuthors = authors.split(';')
        .map(author => author.trim())
        .filter(author => !blacklist.has(author.toLowerCase()));
    return newAuthors.length > 0 ? newAuthors.join('; ') : null;
}

function extractMetaJson(tree, metadata) {
    var scripts = tree.querySelectorAll('script[type="application/ld+json"], script[type="application/settings+json"]');
    for (var elem of scripts) {
        if (!elem.textContent) continue;
        var elementText = normalizeJson(elem.textContent.replace(JSON_MINIFY, '$1'));
        try {
            var schema = JSON.parse(elementText);
            metadata = extractJson(schema, metadata);
        } catch (error) {
            metadata = extractJsonParseError(elementText, metadata);
        }
    }
    return metadata;
}

function extractOpengraph(tree) {
    var ogProperties = {
        'og:title': 'title',
        'og:description': 'description',
        'og:site_name': 'sitename',
        'og:image': 'image',
        'og:image:url': 'image',
        'og:image:secure_url': 'image',
        'og:type': 'pagetype',
    };
    var result = {
        title: null, author: null, url: null, description: null,
        sitename: null, image: null, pagetype: null
    };

    var metaTags = tree.querySelectorAll('head > meta[property^="og:"]');
    for (var elem of metaTags) {
        var propertyName = elem.getAttribute('property');
        var content = elem.getAttribute('content');
        if (content && content.trim()) {
            if (propertyName in ogProperties) {
                result[ogProperties[propertyName]] = content;
            } else if (propertyName === 'og:url' && isValidUrl(content)) {
                result.url = content;
            } else if (OG_AUTHOR.has(propertyName)) {
                result.author = normalizeAuthors(null, content);
            }
        }
    }
    return result;
}

// ... (other functions)

function extractMetadata(filecontent, defaultUrl = null, dateConfig = null, extensive = true, authorBlacklist = null) {
    if (!authorBlacklist) authorBlacklist = new Set();
    if (!dateConfig) dateConfig = setDateParams(extensive);

    var dom = new JSDOM(filecontent);
    var tree = dom.window.document;

    let metadata = examineMeta(tree);
    if (metadata.author && !metadata.author.includes(' ')) {
        metadata.author = null;
    }

    try {
        metadata = extractMetaJson(tree, metadata);
    } catch (error) {
        console.warn('Error in JSON metadata extraction:', error);
    }

    if (!metadata.title) {
        metadata.title = extractTitle(tree);
    }

    if (metadata.author && authorBlacklist.size > 0) {
        metadata.author = checkAuthors(metadata.author, authorBlacklist);
    }

    if (!metadata.author) {
        metadata.author = extractAuthor(tree);
    }

    if (metadata.author && authorBlacklist.size > 0) {
        metadata.author = checkAuthors(metadata.author, authorBlacklist);
    }

    if (!metadata.url) {
        metadata.url = extractUrl(tree, defaultUrl);
    }

    if (metadata.url) {
        metadata.hostname = extractDomain(metadata.url, { fast: true });
    }

    if (!metadata.image) {
        metadata.image = extractImage(tree);
    }

    dateConfig.url = metadata.url;
    metadata.date = findDate(tree, dateConfig);

    if (!metadata.sitename) {
        metadata.sitename = extractSitename(tree);
    }

    // ... (rest of the function)

    metadata.filedate = dateConfig.maxDate;
    metadata.cleanAndTrim();

    return metadata;
}

module.exports = {
    extractMetadata,
    // ... (export other functions as needed)
};