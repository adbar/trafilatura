// Importing required modules
const { JSDOM } = require('jsdom');
const { URL } = require('url');
const { duplicateTest } = require('./deduplication');
const { textfilter, trim } = require('./utils');

// Constants
const CUT_EMPTY_ELEMS = new Set(['p', 'div', 'span']);
const MANUALLY_CLEANED = ['aside', 'footer', 'nav'];
const MANUALLY_STRIPPED = ['img'];

const REND_TAG_MAPPING = {
    'em': '#i',
    'i': '#i',
    'b': '#b',
    'strong': '#b',
    'u': '#u',
    'kbd': '#t',
    'samp': '#t',
    'tt': '#t',
    'var': '#t',
    'sub': '#sub',
    'sup': '#sup'
};

const HTML_TAG_MAPPING = Object.fromEntries(
    Object.entries(REND_TAG_MAPPING).map(([k, v]) => [v, k])
);

const PRESERVE_IMG_CLEANING = new Set(['figure', 'picture', 'source']);

// Helper functions
function deleteElement(element, keepTail = false) {
    if (keepTail && element.nextSibling) {
        element.nextSibling.textContent = (element.nextSibling.textContent || '') + (element.textContent || '');
    }
    element.parentNode.removeChild(element);
}

function stripTags(tree, tagList) {
    tagList.forEach(tag => {
        tree.querySelectorAll(tag).forEach(elem => {
            while (elem.firstChild) {
                elem.parentNode.insertBefore(elem.firstChild, elem);
            }
            elem.parentNode.removeChild(elem);
        });
    });
}

// Main functions
function treeCleaning(tree, options) {
    let cleaningList = [...MANUALLY_CLEANED];
    let strippingList = [...MANUALLY_STRIPPED];

    if (!options.tables) {
        cleaningList.push(...['table', 'td', 'th', 'tr']);
    } else {
        tree.querySelectorAll('figure').forEach(elem => {
            if (elem.querySelector('table')) {
                elem.tagName = 'div';
            }
        });
    }

    if (options.images) {
        cleaningList = cleaningList.filter(e => !PRESERVE_IMG_CLEANING.has(e));
        strippingList = strippingList.filter(e => e !== 'img');
    }

    stripTags(tree, strippingList);

    if (options.focus === "recall" && tree.querySelector('p')) {
        const tcopy = tree.cloneNode(true);
        cleaningList.forEach(expression => {
            tree.querySelectorAll(expression).forEach(element => {
                deleteElement(element);
            });
        });
        if (!tree.querySelector('p')) {
            tree = tcopy;
        }
    } else {
        cleaningList.forEach(expression => {
            tree.querySelectorAll(expression).forEach(element => {
                deleteElement(element);
            });
        });
    }

    return pruneHtml(tree, options.focus);
}

function pruneHtml(tree, focus = "balanced") {
    const tails = focus !== "precision";
    tree.querySelectorAll('*').forEach(element => {
        if (CUT_EMPTY_ELEMS.has(element.tagName.toLowerCase()) && !element.hasChildNodes()) {
            deleteElement(element, tails);
        }
    });
    return tree;
}

function pruneUnwantedNodes(tree, nodelist, withBackup = false) {
    var oldLen = 0;
    if (withBackup) {
        oldLen = tree?.textContent?.length;
        const backup = tree.cloneNode(true);
    }

    nodelist.forEach(selector => {
        tree.querySelectorAll(selector).forEach(subtree => {
            if (subtree.nextSibling) {
                subtree.nextSibling.textContent = (subtree.nextSibling.textContent || '') + ' ' + (subtree.textContent || '');
            }
            subtree.parentNode.removeChild(subtree);
        });
    });

    if (withBackup) {
        const newLen = tree.textContent.length;
        return newLen > oldLen / 7 ? tree : backup;
    }
    return tree;
}


function collectLinkInfo(linksXpath) {
    const mylist = linksXpath.map(elem => trim(elem.textContent)).filter(Boolean);
    const lengths = mylist.map(s => s.length);
    const shortelems = lengths.filter(l => l < 10).length;
    return [lengths.reduce((a, b) => a + b, 0), mylist.length, shortelems, mylist];
}

function linkDensityTest(element, text, favorPrecision = false) {
    const links = element.querySelectorAll('ref');
    if (links.length === 0) return [false, []];

    let mylist = [];
    if (links.length === 1) {
        const lenThreshold = favorPrecision ? 10 : 100;
        const linkText = trim(links[0].textContent);
        if (linkText.length > lenThreshold && linkText.length > text.length * 0.9) {
            return [true, []];
        }
    }

    let limitlen;
    if (element.tagName === 'P') {
        limitlen = element.nextElementSibling ? 30 : 60;
    } else {
        limitlen = element.nextElementSibling ? 100 : 300;
    }

    const elemlen = text.length;
    if (elemlen < limitlen) {
        const [linklen, elemnum, shortelems, templist] = collectLinkInfo(links);
        if (elemnum === 0) return [true, templist];
        console.debug(`list link text/total: ${linklen}/${elemlen} – short elems/total: ${shortelems}/${elemnum}`);
        if (linklen > elemlen * 0.8 || (elemnum > 1 && shortelems / elemnum > 0.8)) {
            return [true, templist];
        }
    }
    return [false, mylist];
}

function linkDensityTestTables(element) {
    const links = element.querySelectorAll('ref');
    if (links.length === 0) return false;

    const elemlen = element.textContent.trim().length;
    if (elemlen < 200) return false;

    const [linklen, elemnum, _] = collectLinkInfo(links);
    if (elemnum === 0) return true;

    console.debug(`table link text: ${linklen} / total: ${elemlen}`);
    return elemlen < 1000 ? linklen > 0.8 * elemlen : linklen > 0.5 * elemlen;
}

function deleteByLinkDensity(subtree, tagname, backtracking = false, favorPrecision = false) {
    const deletions = [];
    const lenThreshold = favorPrecision ? 200 : 100;
    const depthThreshold = favorPrecision ? 1 : 3;

    subtree.querySelectorAll(tagname).forEach(elem => {
        const elemtext = trim(elem.textContent);
        const [result, templist] = linkDensityTest(elem, elemtext, favorPrecision);
        if (result || (
            backtracking && templist.length > 0 &&
            elemtext.length > 0 && elemtext.length < lenThreshold &&
            elem.childElementCount >= depthThreshold
        )) {
            deletions.push(elem);
        }
    });

    deletions.forEach(elem => deleteElement(elem));
    return subtree;
}

function handleTextnode(elem, options, commentsFix = true, preserveSpaces = false) {
    if (elem.tagName === 'DONE' || (elem.childElementCount === 0 && !elem.textContent && !elem.nextSibling)) {
        return null;
    }

    if (!commentsFix && elem.tagName === 'LB') {
        if (!preserveSpaces) {
            elem.nextSibling.textContent = trim(elem.nextSibling.textContent);
        }
        return elem;
    }

    if (!elem.textContent && elem.childElementCount === 0) {
        elem.textContent = elem.nextSibling ? elem.nextSibling.textContent : '';
        elem.nextSibling = null;
        if (commentsFix && elem.tagName === 'LB') {
            elem.tagName = 'P';
        }
    }

    if (!preserveSpaces) {
        elem.textContent = trim(elem.textContent);
        if (elem.nextSibling) {
            elem.nextSibling.textContent = trim(elem.nextSibling.textContent);
        }
    }

    if ((!elem.textContent && textfilter(elem)) || (options.dedup && duplicateTest(elem, options))) {
        return null;
    }
    return elem;
}

function processNode(elem, options) {
    if (elem.tagName === 'DONE' || (elem.childElementCount === 0 && !elem.textContent && !elem.nextSibling)) {
        return null;
    }

    elem.textContent = trim(elem.textContent);
    if (elem.nextSibling) {
        elem.nextSibling.textContent = trim(elem.nextSibling.textContent);
    }

    if (elem.tagName !== 'LB' && !elem.textContent && elem.nextSibling) {
        elem.textContent = elem.nextSibling.textContent;
        elem.nextSibling = null;
    }

    if (elem.textContent || (elem.nextSibling && elem.nextSibling.textContent)) {
        if (textfilter(elem) || (options.dedup && duplicateTest(elem, options))) {
            return null;
        }
    }

    return elem;
}

function convertLists(elem) {
    elem.setAttribute("rend", elem.tagName);
    elem.tagName = "LIST";
    let i = 1;
    elem.querySelectorAll('dd, dt, li').forEach(subelem => {
        if (subelem.tagName === 'DD' || subelem.tagName === 'DT') {
            subelem.setAttribute("rend", `${subelem.tagName.toLowerCase()}-${i}`);
            if (subelem.tagName === 'DD') {
                i++;
            }
        }
        subelem.tagName = "ITEM";
    });
}

function convertQuotes(elem) {
    let codeFlag = false;
    if (elem.tagName === 'PRE') {
        if (elem.childElementCount === 1 && elem.firstElementChild.tagName === 'SPAN') {
            codeFlag = true;
        }
        const codeElems = elem.querySelectorAll('span[class^="hljs"]');
        if (codeElems.length) {
            codeFlag = true;
            codeElems.forEach(subelem => {
                subelem.removeAttribute('class');
            });
        }
    }
    elem.tagName = codeFlag ? "CODE" : "QUOTE";
}

function convertHeadings(elem) {
    elem.removeAttribute('class');
    elem.setAttribute("rend", elem.tagName);
    elem.tagName = "HEAD";
}

function convertLineBreaks(elem) {
    elem.tagName = "LB";
}

function convertDeletions(elem) {
    elem.tagName = "DEL";
    elem.setAttribute("rend", "overstrike");
}

function convertDetails(elem) {
    elem.tagName = "DIV";
    elem.querySelectorAll('summary').forEach(subelem => {
        subelem.tagName = "HEAD";
    });
}

const CONVERSIONS = {
    "DL": convertLists, "OL": convertLists, "UL": convertLists,
    "H1": convertHeadings, "H2": convertHeadings, "H3": convertHeadings,
    "H4": convertHeadings, "H5": convertHeadings, "H6": convertHeadings,
    "BR": convertLineBreaks, "HR": convertLineBreaks,
    "BLOCKQUOTE": convertQuotes, "PRE": convertQuotes, "Q": convertQuotes,
    "DEL": convertDeletions, "S": convertDeletions, "STRIKE": convertDeletions,
    "DETAILS": convertDetails,
};

function convertTags(tree, options, url = null) {
    if (!options.links) {
        const xpathExpr = ".//*[self::div or self::li or self::p]//a" + (options.tables ? '|.//table//a' : '');
        tree.querySelectorAll(xpathExpr).forEach(elem => {
            elem.tagName = 'REF';
        });
        stripTags(tree, ['a']);
    } else {
        const baseUrl = url ? new URL(url).origin : null;
        tree.querySelectorAll('a, ref').forEach(elem => {
            elem.tagName = 'REF';
            const target = elem.getAttribute('href');
            elem.removeAttribute('class');
            if (target) {
                if (baseUrl) {
                    elem.setAttribute('target', new URL(target, baseUrl).href);
                } else {
                    elem.setAttribute('target', target);
                }
            }
        });
    }

    if (options.formatting) {
        Object.keys(REND_TAG_MAPPING).forEach(tag => {
            tree.querySelectorAll(tag).forEach(elem => {
                elem.removeAttribute('class');
                elem.setAttribute('rend', REND_TAG_MAPPING[tag]);
                elem.tagName = 'HI';
            });
        });
    } else {
        stripTags(tree, Object.keys(REND_TAG_MAPPING));
    }

    Object.keys(CONVERSIONS).forEach(tag => {
        tree.querySelectorAll(tag).forEach(elem => {
            CONVERSIONS[tag](elem);
        });
    });

    if (options.images) {
        tree.querySelectorAll('img').forEach(elem => {
            elem.tagName = 'GRAPHIC';
        });
    }

    return tree;
}

const HTML_CONVERSIONS = {
    "LIST": "ul",
    "ITEM": "li",
    "CODE": "pre",
    "QUOTE": "blockquote",
    "HEAD": elem => `h${parseInt(elem.getAttribute('rend').slice(1))}`,
    "LB": "br",
    "GRAPHIC": "img",
    "REF": "a",
    "HI": elem => HTML_TAG_MAPPING[elem.getAttribute('rend')]
};
function convertToHtml(tree) {
    tree.querySelectorAll('*').forEach(elem => {
        if (HTML_CONVERSIONS[elem.tagName]) {
            if (typeof HTML_CONVERSIONS[elem.tagName] === 'function') {
                elem.tagName = HTML_CONVERSIONS[elem.tagName](elem);
            } else {
                elem.tagName = HTML_CONVERSIONS[elem.tagName];
            }
            if (elem.tagName === 'A') {
                elem.setAttribute('href', elem.getAttribute('target'));
                elem.removeAttribute('target');
            } else {
                elem.removeAttribute('class');
                elem.removeAttribute('rend');
            }
        }
    });
    tree.tagName = 'BODY';
    const root = document.createElement('html');
    root.appendChild(tree);
    return root;
}

function buildHtmlOutput(document, withMetadata = false) {
    const htmlTree = convertToHtml(document.body);

    if (withMetadata) {
        const head = document.createElement('head');
        META_ATTRIBUTES.forEach(item => {
            const value = document[item];
            if (value) {
                const meta = document.createElement('meta');
                meta.setAttribute('name', item);
                meta.setAttribute('content', value);
                head.appendChild(meta);
            }
        });
        htmlTree.insertBefore(head, htmlTree.firstChild);
    }

    return htmlTree.outerHTML;
}

// Exports
module.exports = {
    treeCleaning,
    pruneHtml,
    pruneUnwantedNodes,
    collectLinkInfo,
    linkDensityTest,
    linkDensityTestTables,
    deleteByLinkDensity,
    handleTextnode,
    processNode,
    convertLists,
    convertQuotes,
    convertHeadings,
    convertLineBreaks,
    convertDeletions,
    convertDetails,
    convertTags,
    convertToHtml,
    buildHtmlOutput
};