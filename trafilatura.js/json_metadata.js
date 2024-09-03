// Functions needed to scrape metadata from JSON-LD format.

var JSON_ARTICLE_SCHEMA = new Set([
    "article", "backgroundnewsarticle", "blogposting", "medicalscholarlyarticle", 
    "newsarticle", "opinionnewsarticle", "reportagenewsarticle", "scholarlyarticle", 
    "socialmediaposting", "liveblogposting"
]);

var JSON_OGTYPE_SCHEMA = new Set([
    "aboutpage", "checkoutpage", "collectionpage", "contactpage", "faqpage", "itempage", 
    "medicalwebpage", "profilepage", "qapage", "realestatelisting", "searchresultspage", 
    "webpage", "website", "article", "advertisercontentarticle", "newsarticle", 
    "analysisnewsarticle", "askpublicnewsarticle", "backgroundnewsarticle", 
    "opinionnewsarticle", "reportagenewsarticle", "reviewnewsarticle", "report", 
    "satiricalarticle", "scholarlyarticle", "medicalscholarlyarticle", "socialmediaposting", 
    "blogposting", "liveblogposting", "discussionforumposting", "techarticle", "blog", "jobposting"
]);

var JSON_PUBLISHER_SCHEMA = new Set([
    "newsmediaorganization", "organization", "webpage", "website"
]);

var JSON_AUTHOR_1 = /"author":[^}[]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}[]+?"names?".+?"([^"]+)/s;
var JSON_AUTHOR_2 = /"[Pp]erson"[^}]+?"names?".+?"([^"]+)/s;
var JSON_AUTHOR_REMOVE = /,?(?:"\w+":?[:|,\[])?{?"@type":"(?:[Ii]mageObject|[Oo]rganization|[Ww]eb[Pp]age)",[^}[]+}[\]|}]?/g;
var JSON_PUBLISHER = /"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)/s;
var JSON_TYPE = /"@type"\s*:\s*"([^"]*)"/s;
var JSON_CATEGORY = /"articleSection": ?"([^"\\]+)/s;
var JSON_MATCH = /"author":|"person":/i;
var JSON_REMOVE_HTML = /<[^>]+>/g;
var JSON_SCHEMA_ORG = /^https?:\/\/schema\.org/i;
var JSON_UNICODE_REPLACE = /\\u([0-9a-fA-F]{4})/g;

var AUTHOR_ATTRS = ['givenName', 'additionalName', 'familyName'];

var JSON_NAME = /"@type":"[Aa]rticle", ?"name": ?"([^"\\]+)/s;
var JSON_HEADLINE = /"headline": ?"([^"\\]+)/s;
var JSON_SEQ = [['"name"', JSON_NAME], ['"headline"', JSON_HEADLINE]];

var AUTHOR_PREFIX = /^([a-zäöüß]+(ed|t))? ?(written by|words by|words|by|von|from) /i;
var AUTHOR_REMOVE_NUMBERS = /\d.+?$/;
var AUTHOR_TWITTER = /@[\w]+/;
var AUTHOR_REPLACE_JOIN = /[._+]/g;
var AUTHOR_REMOVE_NICKNAME = /["'({\['\'][^"]+?[''"\')\]}]/g;
var AUTHOR_REMOVE_SPECIAL = /[^\w]+$|[:()?*$#!%/<>{}~¿]/g;
var AUTHOR_REMOVE_PREPOSITION = /\b\s+(am|on|for|at|in|to|from|of|via|with|—|-|–)\s+(.*)/i;
var AUTHOR_EMAIL = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;
var AUTHOR_SPLIT = /\/|;|,|\||&|(?:^|\W)[u|a]nd(?:$|\W)/i;
var AUTHOR_EMOJI_REMOVE = /[\u2700-\u27BF\uE000-\uF8FF\u2600-\u26FF\u2700-\u27BF\uD83C[\uDC00-\uDFFF]\uD83D[\uDC00-\uDFFF]\uD83E[\uDD10-\uDDFF]]/g;

function isPlausibleSitename(metadata, candidate, contentType = null) {
    if (candidate && typeof candidate === 'string') {
        if (!metadata.sitename || (metadata.sitename.length < candidate.length && contentType !== "webpage")) {
            return true;
        }
        if (metadata.sitename && metadata.sitename.startsWith('http') && !candidate.startsWith('http')) {
            return true;
        }
    }
    return false;
}

function processParent(parent, metadata) {
    for (var content of parent.filter(Boolean)) {
        if ('publisher' in content && 'name' in content.publisher) {
            metadata.sitename = content.publisher.name;
        }

        if (!('@type' in content) || !content["@type"]) {
            continue;
        }

        var contentType = Array.isArray(content["@type"]) ? content["@type"][0].toLowerCase() : content["@type"].toLowerCase();

        if (JSON_OGTYPE_SCHEMA.has(contentType) && !metadata.pagetype) {
            metadata.pagetype = normalizeJson(contentType);
        }

        if (JSON_PUBLISHER_SCHEMA.has(contentType)) {
            var candidate = content.name || content.legalName || content.alternateName;
            if (isPlausibleSitename(metadata, candidate, contentType)) {
                metadata.sitename = candidate;
            }
        } else if (contentType === "person") {
            if (content.name && !content.name.startsWith('http')) {
                metadata.author = normalizeAuthors(metadata.author, content.name);
            }
        } else if (JSON_ARTICLE_SCHEMA.has(contentType)) {
            if ('author' in content) {
                let listAuthors = content.author;
                if (typeof listAuthors === 'string') {
                    try {
                        listAuthors = JSON.parse(listAuthors);
                    } catch (error) {
                        metadata.author = normalizeAuthors(metadata.author, listAuthors);
                    }
                }

                if (!Array.isArray(listAuthors)) {
                    listAuthors = [listAuthors];
                }

                for (var author of listAuthors) {
                    if (!('@type' in author) || author['@type'] === 'Person') {
                        let authorName = null;
                        if ('name' in author) {
                            authorName = author.name;
                            if (Array.isArray(authorName)) {
                                authorName = authorName.join('; ').trim();
                            } else if (typeof authorName === 'object' && "name" in authorName) {
                                authorName = authorName.name;
                            }
                        } else if ('givenName' in author && 'familyName' in author) {
                            authorName = AUTHOR_ATTRS.map(x => author[x]).filter(Boolean).join(' ');
                        }
                        if (typeof authorName === 'string') {
                            metadata.author = normalizeAuthors(metadata.author, authorName);
                        }
                    }
                }
            }

            if (!metadata.categories && 'articleSection' in content) {
                metadata.categories = Array.isArray(content.articleSection) ? 
                    content.articleSection.filter(Boolean) : 
                    [content.articleSection];
            }

            if (!metadata.title) {
                if ('name' in content && contentType === 'article') {
                    metadata.title = content.name;
                } else if ('headline' in content) {
                    metadata.title = content.headline;
                }
            }
        }
    }
    return metadata;
}

function extractJson(schema, metadata) {
    if (!Array.isArray(schema)) {
        schema = [schema];
    }

    for (var parent of schema) {
        var context = parent['@context'];

        if (context && typeof context === 'string' && JSON_SCHEMA_ORG.test(context)) {
            let processedParent;
            if ('@graph' in parent) {
                processedParent = Array.isArray(parent['@graph']) ? parent['@graph'] : [parent['@graph']];
            } else if ('@type' in parent && typeof parent['@type'] === 'string' && 
                       parent['@type'].toLowerCase().includes('liveblogposting') && 
                       'liveBlogUpdate' in parent) {
                processedParent = Array.isArray(parent.liveBlogUpdate) ? parent.liveBlogUpdate : [parent.liveBlogUpdate];
            } else {
                processedParent = schema;
            }

            metadata = processParent(processedParent, metadata);
        }
    }

    return metadata;
}

function extractJsonAuthor(elemtext, regularExpression) {
    let authors = null;
    let match = regularExpression.exec(elemtext);
    while (match && match[1].includes(' ')) {
        authors = normalizeAuthors(authors, match[1]);
        elemtext = elemtext.replace(regularExpression, '');
        match = regularExpression.exec(elemtext);
    }
    return authors;
}

function extractJsonParseError(elem, metadata) {
    var elementTextAuthor = elem.replace(JSON_AUTHOR_REMOVE, '');
    var author = extractJsonAuthor(elementTextAuthor, JSON_AUTHOR_1) || 
                   extractJsonAuthor(elementTextAuthor, JSON_AUTHOR_2);
    if (author) {
        metadata.author = author;
    }

    if (elem.includes("@type")) {
        var typeMatch = JSON_TYPE.exec(elem);
        if (typeMatch) {
            var candidate = normalizeJson(typeMatch[1].toLowerCase());
            if (JSON_OGTYPE_SCHEMA.has(candidate)) {
                metadata.pagetype = candidate;
            }
        }
    }

    if (elem.includes('"publisher"')) {
        var publisherMatch = JSON_PUBLISHER.exec(elem);
        if (publisherMatch && !publisherMatch[1].includes(',')) {
            var candidate = normalizeJson(publisherMatch[1]);
            if (isPlausibleSitename(metadata, candidate)) {
                metadata.sitename = candidate;
            }
        }
    }

    if (elem.includes('"articleSection"')) {
        var categoryMatch = JSON_CATEGORY.exec(elem);
        if (categoryMatch) {
            metadata.categories = [normalizeJson(categoryMatch[1])];
        }
    }

    for (var [key, regex] of JSON_SEQ) {
        if (elem.includes(key) && !metadata.title) {
            var titleMatch = regex.exec(elem);
            if (titleMatch) {
                metadata.title = normalizeJson(titleMatch[1]);
                break;
            }
        }
    }

    return metadata;
}

function normalizeJson(string) {
    if (string.includes('\\')) {
        string = string.replace(/\\n/g, '').replace(/\\r/g, '').replace(/\\t/g, '');
        string = string.replace(JSON_UNICODE_REPLACE, (match, p1) => 
            String.fromCharCode(parseInt(p1, 16))
        );
        string = string.replace(/[\uD800-\uDFFF]/g, '');
        string = string.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#039;/g, "'");
    }
    return string.replace(JSON_REMOVE_HTML, '').trim();
}

function normalizeAuthors(currentAuthors, authorString) {
    let newAuthors = [];
    if (authorString.toLowerCase().startsWith('http') || AUTHOR_EMAIL.test(authorString)) {
        return currentAuthors;
    }
    if (currentAuthors !== null) {
        newAuthors = currentAuthors.split('; ');
    }
    if (authorString.includes('\\u')) {
        authorString = JSON.parse('"' + authorString + '"');
    }
    authorString = authorString.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#039;/g, "'");
    authorString = authorString.replace(/<[^>]*>/g, '');

    for (let author of authorString.split(AUTHOR_SPLIT)) {
        author = author.trim();
        author = author.replace(AUTHOR_EMOJI_REMOVE, '');
        author = author.replace(AUTHOR_TWITTER, '');
        author = author.replace(AUTHOR_REPLACE_JOIN, ' ').trim();
        author = author.replace(AUTHOR_REMOVE_NICKNAME, '');
        author = author.replace(AUTHOR_REMOVE_SPECIAL, '');
        author = author.replace(AUTHOR_PREFIX, '');
        author = author.replace(AUTHOR_REMOVE_NUMBERS, '');
        author = author.replace(AUTHOR_REMOVE_PREPOSITION, '');

        if (!author || (author.length >= 50 && !author.includes(' ') && !author.includes('-'))) {
            continue;
        }

        if (!author[0].toUpperCase() === author[0] || author.split('').filter(c => c === c.toUpperCase()).length < 1) {
            author = author.replace(/\w\S*/g, function(txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
        }

        if (!newAuthors.includes(author) && (newAuthors.length === 0 || newAuthors.every(newAuthor => !author.includes(newAuthor)))) {
            newAuthors.push(author);
        }
    }
    if (newAuthors.length === 0) {
        return currentAuthors;
    }
    return newAuthors.join('; ').trim();
}

module.exports = {
    extractJson,
    extractJsonParseError,
    normalizeJson,
    normalizeAuthors
};