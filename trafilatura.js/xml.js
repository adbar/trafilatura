// All functions related to XML generation, processing and validation.

var { JSDOM } = require('jsdom');
var { sanitize, sanitizeTree, textCharsTest } = require('./utils');

var TEI_VALID_TAGS = new Set(['ab', 'body', 'cell', 'code', 'del', 'div', 'graphic', 'head', 'hi',
                                'item', 'lb', 'list', 'p', 'quote', 'ref', 'row', 'table']);
var TEI_VALID_ATTRS = new Set(['rend', 'rendition', 'role', 'target', 'type']);
var TEI_REMOVE_TAIL = new Set(["ab", "p"]);
var TEI_DIV_SIBLINGS = new Set(["p", "list", "table", "quote", "ab"]);

var NEWLINE_ELEMS = new Set(['code', 'graphic', 'head', 'lb', 'list', 'p', 'quote', 'row', 'table']);
var SPECIAL_FORMATTING = new Set(['del', 'head', 'hi', 'ref']);
var WITH_ATTRIBUTES = new Set(['cell', 'row', 'del', 'graphic', 'head', 'hi', 'item', 'list', 'ref']);
var NESTING_WHITELIST = new Set(["cell", "figure", "item", "note", "quote"]);

var META_ATTRIBUTES = [
    'sitename', 'title', 'author', 'date', 'url', 'hostname',
    'description', 'categories', 'tags', 'license', 'id',
    'fingerprint', 'language'
];

var HI_FORMATTING = {'#b': '**', '#i': '*', '#u': '__', '#t': '`'};

var MAX_TABLE_WIDTH = 1000;

function deleteElement(element, keepTail = true) {
    var parent = element.parentNode;
    if (!parent) return;

    if (keepTail && element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE) {
        var previousSibling = element.previousSibling;
        if (previousSibling && previousSibling.nodeType === Node.TEXT_NODE) {
            previousSibling.textContent += element.nextSibling.textContent;
            parent.removeChild(element.nextSibling);
        } else {
            parent.insertBefore(element.nextSibling, element);
        }
    }

    parent.removeChild(element);
}

function mergeWithParent(element, includeFormatting = false) {
    var parent = element.parentNode;
    if (!parent) return;

    var fullText = replaceElementText(element, includeFormatting);
    var tailText = element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE
        ? element.nextSibling.textContent
        : '';

    var previousSibling = element.previousSibling;
    if (previousSibling && previousSibling.nodeType === Node.TEXT_NODE) {
        previousSibling.textContent += ' ' + fullText + tailText;
    } else if (parent.firstChild === element) {
        parent.insertBefore(document.createTextNode(fullText + tailText), element);
    } else {
        parent.insertBefore(document.createTextNode(' ' + fullText + tailText), element);
    }

    if (element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE) {
        parent.removeChild(element.nextSibling);
    }
    parent.removeChild(element);
}

function removeEmptyElements(tree) {
    var walker = document.createTreeWalker(tree, NodeFilter.SHOW_ELEMENT);
    var elementsToRemove = [];

    let node;
    while (node = walker.nextNode()) {
        if (node.childNodes.length === 0 &&
            !textCharsTest(node.textContent) &&
            !textCharsTest(node.nextSibling && node.nextSibling.textContent)) {
            var parent = node.parentNode;
            if (parent && node.tagName !== "GRAPHIC" && parent.tagName !== 'CODE') {
                elementsToRemove.push(node);
            }
        }
    }

    elementsToRemove.forEach(elem => elem.parentNode.removeChild(elem));
    return tree;
}

function stripDoubleTags(tree) {
    var tagsToCheck = ['HEAD', 'CODE', 'P'];
    tagsToCheck.forEach(tag => {
        var elements = tree.querySelectorAll(tag);
        for (let i = elements.length - 1; i >= 0; i--) {
            var elem = elements[i];
            var nestedElems = elem.querySelectorAll('code, head, p');
            nestedElems.forEach(nestedElem => {
                if (nestedElem.tagName === elem.tagName && 
                    !NESTING_WHITELIST.has(nestedElem.parentNode.tagName.toLowerCase())) {
                    mergeWithParent(nestedElem);
                }
            });
        }
    });
    return tree;
}

function buildJsonOutput(docmeta, withMetadata = true) {
    let outputDict = {};
    if (withMetadata) {
        META_ATTRIBUTES.forEach(attr => {
            if (docmeta[attr] !== undefined) {
                outputDict[attr] = docmeta[attr];
            }
        });
        outputDict.source = outputDict.url;
        delete outputDict.url;
        outputDict['source-hostname'] = outputDict.sitename;
        delete outputDict.sitename;
        outputDict.excerpt = outputDict.description;
        delete outputDict.description;
        outputDict.categories = outputDict.categories ? outputDict.categories.join(';') : '';
        outputDict.tags = outputDict.tags ? outputDict.tags.join(';') : '';
        outputDict.text = xmlToTxt(outputDict.body, false);
        delete outputDict.body;
    } else {
        outputDict.text = xmlToTxt(docmeta.body, false);
    }

    if (docmeta.commentsbody) {
        outputDict.comments = xmlToTxt(docmeta.commentsbody, false);
    }

    return JSON.stringify(outputDict);
}

function cleanAttributes(tree) {
    var walker = document.createTreeWalker(tree, NodeFilter.SHOW_ELEMENT);
    let node;
    while (node = walker.nextNode()) {
        if (!WITH_ATTRIBUTES.has(node.tagName.toLowerCase())) {
            while (node.attributes.length > 0) {
                node.removeAttribute(node.attributes[0].name);
            }
        }
    }
    return tree;
}

function buildXmlOutput(docmeta) {
    var output = document.createElement('doc');
    addXmlMeta(output, docmeta);
    docmeta.body.tagName = 'main';
    output.appendChild(cleanAttributes(docmeta.body));
    if (docmeta.commentsbody) {
        docmeta.commentsbody.tagName = 'comments';
        output.appendChild(cleanAttributes(docmeta.commentsbody));
    }
    return output;
}

function controlXmlOutput(document, options) {
    stripDoubleTags(document.body);
    removeEmptyElements(document.body);

    var func = options.format === "xml" ? buildXmlOutput : buildTeiOutput;
    let outputTree = func(document);

    outputTree = sanitizeTree(outputTree);

    // JSDOM doesn't support XML validation, so we'll skip the TEI validation step here

    return new XMLSerializer().serializeToString(outputTree);
}

function addXmlMeta(output, docmeta) {
    META_ATTRIBUTES.forEach(attribute => {
        var value = docmeta[attribute];
        if (value) {
            output.setAttribute(attribute, Array.isArray(value) ? value.join(';') : value);
        }
    });
}

function buildTeiOutput(docmeta) {
    var output = writeTeitree(docmeta);
    return checkTei(output, docmeta.url);
}

function checkTei(xmldoc, url) {
    // Convert head tags
    xmldoc.querySelectorAll('head').forEach(elem => {
        elem.tagName = 'ab';
        elem.setAttribute('type', 'header');
        var parent = elem.parentNode;
        if (parent) {
            if (elem.children.length > 0) {
                var newElem = teiHandleComplexHead(elem);
                parent.replaceChild(newElem, elem);
                elem = newElem;
            }
            if (parent.tagName === "P") {
                moveElementOneLevelUp(elem);
            }
        }
    });

    // Convert <lb/> when child of <div> to <p>
    xmldoc.querySelectorAll('div > lb').forEach(elem => {
        if (elem.nextSibling && elem.nextSibling.nodeType === Node.TEXT_NODE && elem.nextSibling.textContent.trim()) {
            var newP = document.createElement('p');
            newP.textContent = elem.nextSibling.textContent;
            elem.parentNode.replaceChild(newP, elem);
        }
    });

    // Check and clean elements
    xmldoc.querySelectorAll('body *').forEach(elem => {
        if (!TEI_VALID_TAGS.has(elem.tagName.toLowerCase())) {
            console.warn('not a TEI element, removing:', elem.tagName, url);
            mergeWithParent(elem);
        } else {
            if (TEI_REMOVE_TAIL.has(elem.tagName.toLowerCase())) {
                handleUnwantedTails(elem);
            } else if (elem.tagName === "DIV") {
                handleTextContentOfDivNodes(elem);
                wrapUnwantedSiblingsOfDiv(elem);
            }
            
            // Check attributes
            Array.from(elem.attributes).forEach(attr => {
                if (!TEI_VALID_ATTRS.has(attr.name)) {
                    console.warn('not a valid TEI attribute, removing:', attr.name, 'in', elem.tagName, url);
                    elem.removeAttribute(attr.name);
                }
            });
        }
    });

    return xmldoc;
}

// ... (implement other functions like replaceElementText, xmlToTxt, writeTeitree, etc.)

module.exports = {
    deleteElement,
    mergeWithParent,
    removeEmptyElements,
    stripDoubleTags,
    buildJsonOutput,
    buildXmlOutput,
    controlXmlOutput,
    buildTeiOutput,
    checkTei
};