var { JSDOM } = require('jsdom');

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

function replaceElementText(element, includeFormatting) {
    let elemText = element.textContent || "";
    
    if (includeFormatting && element.textContent) {
        if (element.tagName === "HEAD") {
            var number = parseInt(element.getAttribute("rend")?.slice(1)) || 2;
            elemText = `${'#'.repeat(number)} ${elemText}`;
        } else if (element.tagName === "DEL") {
            elemText = `~~${elemText}~~`;
        } else if (element.tagName === "HI") {
            var rend = element.getAttribute("rend");
            if (rend in HI_FORMATTING) {
                elemText = `${HI_FORMATTING[rend]}${elemText}${HI_FORMATTING[rend]}`;
            }
        } else if (element.tagName === "CODE") {
            elemText = elemText.includes("\n") ? `\`\`\`\n${elemText}\n\`\`\`` : `\`${elemText}\``;
        }
    }

    if (element.tagName === "REF") {
        if (elemText) {
            var linkText = `[${elemText}]`;
            var target = element.getAttribute("target");
            elemText = target ? `${linkText}(${target})` : linkText;
        } else {
            console.warn("empty link:", elemText, element.attributes);
        }
    } else if (element.tagName === "CELL" && elemText && element.children.length > 0) {
        if (element.children[0].tagName === 'P') {
            elemText += " ";
        }
    } else if (element.tagName === "ITEM" && elemText) {
        elemText = `- ${elemText}\n`;
    }

    return elemText;
}

function processElement(element, returnList, includeFormatting) {
    if (element.textContent) {
        returnList.push(replaceElementText(element, includeFormatting));
    }

    for (var child of element.children) {
        processElement(child, returnList, includeFormatting);
    }

    if (!element.textContent) {
        if (element.tagName === "GRAPHIC") {
            var text = `${element.getAttribute("title") || ""} ${element.getAttribute("alt") || ""}`.trim();
            returnList.push(`![${text}](${element.getAttribute("src") || ""})`);
        } else if (NEWLINE_ELEMS.has(element.tagName.toLowerCase())) {
            if (element.tagName === "ROW") {
                var cellCount = element.querySelectorAll("cell").length;
                var spanInfo = element.getAttribute("colspan") || element.getAttribute("span");
                var maxSpan = spanInfo && !isNaN(spanInfo) ? Math.min(parseInt(spanInfo), MAX_TABLE_WIDTH) : 1;
                
                if (cellCount < maxSpan) {
                    returnList.push("|".repeat(maxSpan - cellCount) + "\n");
                }
                
                if (element.querySelector("cell[role='head']")) {
                    returnList.push(`\n${"---|".repeat(maxSpan)}\n`);
                }
            } else {
                returnList.push("\n");
            }
        } else if (element.tagName !== "CELL") {
            return;
        }
    }

    if (NEWLINE_ELEMS.has(element.tagName.toLowerCase()) && !element.closest("cell")) {
        returnList.push(includeFormatting ? "\n\u2424\n" : "\n");
    } else if (element.tagName === "CELL") {
        returnList.push(" | ");
    } else if (!SPECIAL_FORMATTING.has(element.tagName.toLowerCase())) {
        returnList.push(" ");
    }

    if (element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE) {
        returnList.push(element.nextSibling.textContent);
    }
}

function xmlToTxt(xmlOutput, includeFormatting) {
    var returnList = [];
    processElement(xmlOutput, returnList, includeFormatting);
    return sanitize(returnList.join("")) || "";
}

function writeTeitree(docmeta) {
    var teidoc = document.createElement('TEI');
    teidoc.setAttribute('xmlns', 'http://www.tei-c.org/ns/1.0');
    
    writeFullheader(teidoc, docmeta);
    
    var textelem = document.createElement('text');
    var textbody = document.createElement('body');
    
    // post
    var postbody = cleanAttributes(docmeta.body.cloneNode(true));
    postbody.tagName = 'div';
    postbody.setAttribute('type', 'entry');
    textbody.appendChild(postbody);
    
    // comments
    if (docmeta.commentsbody) {
        var commentsbody = cleanAttributes(docmeta.commentsbody.cloneNode(true));
        commentsbody.tagName = 'div';
        commentsbody.setAttribute('type', 'comments');
        textbody.appendChild(commentsbody);
    }
    
    textelem.appendChild(textbody);
    teidoc.appendChild(textelem);
    
    return teidoc;
}
function writeFullheader(teidoc, docmeta) {
    var header = document.createElement('teiHeader');
    var filedesc = document.createElement('fileDesc');
    
    var bibTitlestmt = document.createElement('titleStmt');
    var title = document.createElement('title');
    title.setAttribute('type', 'main');
    title.textContent = docmeta.title;
    bibTitlestmt.appendChild(title);
    
    if (docmeta.author) {
        var author = document.createElement('author');
        author.textContent = docmeta.author;
        bibTitlestmt.appendChild(author);
    }
    
    filedesc.appendChild(bibTitlestmt);
    
    var publicationstmtA = document.createElement('publicationStmt');
    var publisherString = definePublisherString(docmeta);
    
    if (docmeta.license) {
        var publisher = document.createElement('publisher');
        publisher.textContent = publisherString;
        publicationstmtA.appendChild(publisher);
        
        var availability = document.createElement('availability');
        var p = document.createElement('p');
        p.textContent = docmeta.license;
        availability.appendChild(p);
        publicationstmtA.appendChild(availability);
    } else {
        var p = document.createElement('p');
        publicationstmtA.appendChild(p);
    }
    
    filedesc.appendChild(publicationstmtA);
    
    var notesstmt = document.createElement('notesStmt');
    if (docmeta.id) {
        var note = document.createElement('note');
        note.setAttribute('type', 'id');
        note.textContent = docmeta.id;
        notesstmt.appendChild(note);
    }
    var fingerprintNote = document.createElement('note');
    fingerprintNote.setAttribute('type', 'fingerprint');
    fingerprintNote.textContent = docmeta.fingerprint;
    notesstmt.appendChild(fingerprintNote);
    
    filedesc.appendChild(notesstmt);
    
    var sourcedesc = document.createElement('sourceDesc');
    var sourceBibl = document.createElement('bibl');
    
    var sigle = [docmeta.sitename, docmeta.date].filter(Boolean).join(', ');
    if (!sigle) {
        console.warn('no sigle for URL', docmeta.url);
    }
    sourceBibl.textContent = [docmeta.title, sigle].filter(Boolean).join(', ');
    sourcedesc.appendChild(sourceBibl);
    
    var sigleBibl = document.createElement('bibl');
    sigleBibl.setAttribute('type', 'sigle');
    sigleBibl.textContent = sigle;
    sourcedesc.appendChild(sigleBibl);
    
    var biblfull = document.createElement('biblFull');
    var bibTitlestmt2 = document.createElement('titleStmt');
    var title2 = document.createElement('title');
    title2.setAttribute('type', 'main');
    title2.textContent = docmeta.title;
    bibTitlestmt2.appendChild(title2);
    
    if (docmeta.author) {
        var author2 = document.createElement('author');
        author2.textContent = docmeta.author;
        bibTitlestmt2.appendChild(author2);
    }
    
    biblfull.appendChild(bibTitlestmt2);
    
    var publicationstmt = document.createElement('publicationStmt');
    var publisher = document.createElement('publisher');
    publisher.textContent = publisherString;
    publicationstmt.appendChild(publisher);
    
    if (docmeta.url) {
        var ptr = document.createElement('ptr');
        ptr.setAttribute('type', 'URL');
        ptr.setAttribute('target', docmeta.url);
        publicationstmt.appendChild(ptr);
    }
    
    var date = document.createElement('date');
    date.textContent = docmeta.date;
    publicationstmt.appendChild(date);
    
    biblfull.appendChild(publicationstmt);
    sourcedesc.appendChild(biblfull);
    
    filedesc.appendChild(sourcedesc);
    header.appendChild(filedesc);
    
    var profiledesc = document.createElement('profileDesc');
    var abstract = document.createElement('abstract');
    var abstractP = document.createElement('p');
    abstractP.textContent = docmeta.description;
    abstract.appendChild(abstractP);
    profiledesc.appendChild(abstract);
    
    if (docmeta.categories || docmeta.tags) {
        var textclass = document.createElement('textClass');
        var keywords = document.createElement('keywords');
        if (docmeta.categories) {
            var term = document.createElement('term');
            term.setAttribute('type', 'categories');
            term.textContent = docmeta.categories.join(',');
            keywords.appendChild(term);
        }
        if (docmeta.tags) {
            var term = document.createElement('term');
            term.setAttribute('type', 'tags');
            term.textContent = docmeta.tags.join(',');
            keywords.appendChild(term);
        }
        textclass.appendChild(keywords);
        profiledesc.appendChild(textclass);
    }
    
    var creation = document.createElement('creation');
    var creationDate = document.createElement('date');
    creationDate.setAttribute('type', 'download');
    creationDate.textContent = docmeta.filedate;
    creation.appendChild(creationDate);
    profiledesc.appendChild(creation);
    
    header.appendChild(profiledesc);
    
    var encodingdesc = document.createElement('encodingDesc');
    var appinfo = document.createElement('appInfo');
    var application = document.createElement('application');
    application.setAttribute('ident', 'Trafilatura');
    var label = document.createElement('label');
    label.textContent = 'Trafilatura';
    application.appendChild(label);
    var ptr = document.createElement('ptr');
    ptr.setAttribute('target', 'https://github.com/adbar/trafilatura');
    application.appendChild(ptr);
    appinfo.appendChild(application);
    encodingdesc.appendChild(appinfo);
    
    header.appendChild(encodingdesc);
    
    teidoc.appendChild(header);
    return header;
}

function definePublisherString(docmeta) {
    if (docmeta.hostname && docmeta.sitename) {
        return `${docmeta.sitename.trim()} (${docmeta.hostname})`;
    } else {
        var publisher = docmeta.hostname || docmeta.sitename || 'N/A';
        if (publisher === 'N/A') {
            console.warn('no publisher for URL', docmeta.url);
        }
        return publisher;
    }
}

function handleTextContentOfDivNodes(element) {
    if (element.childNodes[0] && element.childNodes[0].nodeType === Node.TEXT_NODE && element.childNodes[0].textContent.trim()) {
        var newChild = document.createElement("p");
        newChild.textContent = element.childNodes[0].textContent;
        element.insertBefore(newChild, element.firstChild);
        element.childNodes[0].textContent = "";
    }

    if (element.childNodes[element.childNodes.length - 1] && 
        element.childNodes[element.childNodes.length - 1].nodeType === Node.TEXT_NODE && 
        element.childNodes[element.childNodes.length - 1].textContent.trim()) {
        var newChild = document.createElement("p");
        newChild.textContent = element.childNodes[element.childNodes.length - 1].textContent;
        element.appendChild(newChild);
        element.childNodes[element.childNodes.length - 2].textContent = "";
    }
}

function handleUnwantedTails(element) {
    if (element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE) {
        var tailText = element.nextSibling.textContent.trim();
        if (tailText) {
            if (element.tagName === "P") {
                element.textContent += " " + tailText;
            } else {
                var newSibling = document.createElement('p');
                newSibling.textContent = tailText;
                element.parentNode.insertBefore(newSibling, element.nextSibling);
            }
            element.nextSibling.textContent = "";
        }
    }
}

function teiHandleComplexHead(element) {
    var newElement = document.createElement('ab');
    newElement.setAttribute('type', 'header');
    
    if (element.textContent) {
        newElement.textContent = element.textContent.trim();
    }
    
    for (var child of element.children) {
        if (child.tagName === 'P') {
            if (newElement.children.length > 0 || newElement.textContent) {
                if (newElement.children.length === 0 || newElement.lastChild.nodeType !== Node.ELEMENT_NODE) {
                    var lb = document.createElement('lb');
                    newElement.appendChild(lb);
                }
                newElement.appendChild(document.createTextNode(child.textContent));
            } else {
                newElement.textContent = child.textContent;
            }
        } else {
            newElement.appendChild(child.cloneNode(true));
        }
    }
    
    if (element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE) {
        var tailText = element.nextSibling.textContent.trim();
        if (tailText) {
            newElement.appendChild(document.createTextNode(tailText));
        }
    }
    
    return newElement;
}

function wrapUnwantedSiblingsOfDiv(divElement) {
    var newSibling = document.createElement("div");
    let newSiblingIndex = null;
    var parent = divElement.parentNode;
    if (!parent) return;
    
    let sibling = divElement.nextSibling;
    while (sibling) {
        var nextSibling = sibling.nextSibling;
        if (sibling.nodeType === Node.ELEMENT_NODE) {
            if (sibling.tagName === "DIV") {
                break;
            }
            if (TEI_DIV_SIBLINGS.has(sibling.tagName.toLowerCase())) {
                newSiblingIndex = newSiblingIndex || parent.childNodes.indexOf(sibling);
                newSibling.appendChild(sibling);
            } else {
                if (newSiblingIndex && newSibling.childNodes.length > 0) {
                    parent.insertBefore(newSibling, sibling);
                    newSibling = document.createElement("div");
                    newSiblingIndex = null;
                }
            }
        }
        sibling = nextSibling;
    }
    
    if (newSiblingIndex && newSibling.childNodes.length > 0) {
        parent.insertBefore(newSibling, sibling);
    }
}

function moveElementOneLevelUp(element) {
    var parent = element.parentNode;
    var grandParent = parent ? parent.parentNode : null;
    if (!parent || !grandParent) return;

    var newElem = document.createElement("p");
    let sibling = element.nextSibling;
    while (sibling) {
        var nextSibling = sibling.nextSibling;
        newElem.appendChild(sibling);
        sibling = nextSibling;
    }

    grandParent.insertBefore(element, parent.nextSibling);

    if (element.nextSibling && element.nextSibling.nodeType === Node.TEXT_NODE) {
        var tailText = element.nextSibling.textContent.trim();
        if (tailText) {
            newElem.textContent = tailText;
            element.nextSibling.textContent = "";
        }
    }

    if (parent.nextSibling && parent.nextSibling.nodeType === Node.TEXT_NODE) {
        var tailText = parent.nextSibling.textContent.trim();
        if (tailText) {
            newElem.textContent += (newElem.textContent ? " " : "") + tailText;
            parent.nextSibling.textContent = "";
        }
    }

    if (newElem.childNodes.length > 0 || newElem.textContent) {
        grandParent.insertBefore(newElem, element.nextSibling);
    }

    if (parent.childNodes.length === 0 && !parent.textContent) {
        grandParent.removeChild(parent);
    }
}

function trim(str) {
    return str.trim().replace(/\s+/g, ' '); 
};
const RE_FILTER = /^\W*(Drucken|E-?Mail|Facebook|Flipboard|Google|Instagram|Linkedin|Mail|PDF|Pinterest|Pocket|Print|QQ|Reddit|Twitter|WeChat|WeiBo|Whatsapp|Xing|Mehr zum Thema:?|More on this.{0,8})$/i;

function textfilter(element) {
    // Filter out unwanted text
    const testtext = element.text === null ? element.tail : element.text;
    
    // to check: line len → continue if len(line) <= 5
    return !textCharsTest(testtext) || testtext.split('\n').some(line => RE_FILTER.test(line));
}

function textCharsTest(string) {
    // Determine if a string is only composed of spaces and/or control characters
    return Boolean(string) && !/^\s*$/.test(string);
}
function normalizeUnicode(string, unicodeform = 'NFC') {
    // Normalize the given string to the specified unicode format.
    return string.normalize(unicodeform);
}

module.exports = {normalizeUnicode,
    textCharsTest,
    trim,textfilter,
    deleteElement,
    mergeWithParent,
    removeEmptyElements,
    stripDoubleTags,
    buildJsonOutput,
    buildXmlOutput,
    controlXmlOutput,
    buildTeiOutput,
    checkTei,
    xmlToTxt,
    writeTeitree,
    writeFullheader
};