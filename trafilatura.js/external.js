// Functions grounding on third-party software.

var { JSDOM } = require('jsdom');
var Readability = require('@mozilla/readability').Readability;
var { basicCleaning } = require('./baseline');
var { convertTags, pruneUnwantedNodes, treeCleaning } = require('./htmlprocessing');
var { trim } = require('./utils');

var JUSTEXT_LANGUAGES = {}; // Define your language mappings here
var TEI_VALID_TAGS = new Set([]); // Define your valid TEI tags here

var OVERALL_DISCARD_XPATH = '//aside|//audio|//button|//fieldset|//figure|//footer|//iframe|//input|//label|//link|//nav|//noindex|//noscript|//object|//option|//select|//source|//svg|//time';

var SANITIZED_XPATH = '//aside|//audio|//button|//fieldset|//figure|//footer|//iframe|//input|//label|//link|//nav|//noindex|//noscript|//object|//option|//select|//source|//svg|//time';

function tryReadability(htmlInput) {
    try {
        var doc = new JSDOM(htmlInput);
        var reader = new Readability(doc.window.document);
        var article = reader.parse();
        return new JSDOM(article.content).window.document.body;
    } catch (err) {
        console.warn('readability failed:', err);
        return document.createElement('div');
    }
}

function compareExtraction(tree, backupTree, body, text, lenText, options) {
    if (options.focus === "recall" && lenText > options.minExtractedSize * 10) {
        return [body, text, lenText];
    }

    let useReadability = false;
    let jtResult = false;

    if (options.focus === "precision") {
        backupTree = pruneUnwantedNodes(backupTree, OVERALL_DISCARD_XPATH);
    }

    var temppostAlgo = tryReadability(backupTree.outerHTML);
    var algoText = trim(temppostAlgo.textContent);
    var lenAlgo = algoText.length;

    console.debug(`extracted length: ${lenAlgo} (algorithm) ${lenText} (extraction)`);

    if (lenAlgo === 0 || lenAlgo === lenText) {
        useReadability = false;
    } else if (lenText === 0 && lenAlgo > 0) {
        useReadability = true;
    } else if (lenText > 2 * lenAlgo) {
        useReadability = false;
    } else if (lenAlgo > 2 * lenText && !algoText.startsWith("{")) {
        useReadability = true;
    } else if (body.querySelectorAll('p').length === 0 && lenAlgo > options.minExtractedSize * 2) {
        useReadability = true;
    } else if (body.querySelectorAll('table').length > body.querySelectorAll('p').length && lenAlgo > options.minExtractedSize * 2) {
        useReadability = true;
    } else if (options.focus === "recall" && !body.querySelector('head') && temppostAlgo.querySelectorAll('h2, h3, h4').length > 0 && lenAlgo > lenText) {
        useReadability = true;
    } else {
        console.debug(`extraction values: ${lenText} ${lenAlgo} for ${options.source}`);
        useReadability = false;
    }

    if (useReadability) {
        body = temppostAlgo;
        text = algoText;
        lenText = lenAlgo;
        console.debug(`using generic algorithm: ${options.source}`);
    } else {
        console.debug(`using custom extraction: ${options.source}`);
    }

    if (body.querySelector(SANITIZED_XPATH) || lenText < options.minExtractedSize) {
        console.debug(`unclean document triggering justext examination: ${options.source}`);
        var [body2, text2, lenText2] = justextRescue(tree, options);
        jtResult = !!text2;
        if (text2 && !(lenText > 4 * lenText2)) {
            console.debug(`using justext, length: ${lenText2}`);
            body = body2;
            text = text2;
            lenText = lenText2;
        }
    }

    if (useReadability && !jtResult) {
        [body, text, lenText] = sanitizeTree(body, options);
    }

    return [body, text, lenText];
}

function justextRescue(tree, options) {
    // This is a placeholder for JusText functionality
    // You might want to implement or find a JavaScript equivalent for JusText
    console.warn('JusText functionality not implemented');
    return [tree, '', 0];
}

function sanitizeTree(tree, options) {
    let cleanedTree = treeCleaning(tree, options);
    
    cleanedTree.querySelectorAll(SANITIZED_XPATH).forEach(elem => elem.remove());
    
    if (!options.links) {
        cleanedTree.querySelectorAll('a').forEach(a => {
            var text = document.createTextNode(a.textContent);
            a.parentNode.replaceChild(text, a);
        });
    }

    cleanedTree.querySelectorAll('span').forEach(span => {
        var text = document.createTextNode(span.textContent);
        span.parentNode.replaceChild(text, span);
    });

    cleanedTree = convertTags(cleanedTree, options);

    cleanedTree.querySelectorAll('td, th, tr').forEach(elem => {
        if (elem.tagName === 'TR') {
            elem.tagName = 'ROW';
        } else if (elem.tagName === 'TD' || elem.tagName === 'TH') {
            if (elem.tagName === 'TH') {
                elem.setAttribute('role', 'head');
            }
            elem.tagName = 'CELL';
        }
    });

    var sanitizationList = Array.from(cleanedTree.querySelectorAll('*'))
        .map(element => element.tagName.toLowerCase())
        .filter(tag => !TEI_VALID_TAGS.has(tag));

    sanitizationList.forEach(tag => {
        cleanedTree.querySelectorAll(tag).forEach(elem => {
            var text = document.createTextNode(elem.textContent);
            elem.parentNode.replaceChild(text, elem);
        });
    });

    var text = trim(cleanedTree.textContent);
    return [cleanedTree, text, text.length];
}

module.exports = {
    compareExtraction,
    justextRescue,
    sanitizeTree
};