var { JSDOM } = require('jsdom');
var { deleteByLinkDensity, handleTextnode, linkDensityTestTables, processNode,
        pruneUnwantedNodes } = require('./htmlprocessing');
var { TAG_CATALOG } = require('./settings');
var { FORMATTING_PROTECTED, isImageFile, textCharsTest } = require('./utils');
var { deleteElement } = require('./xml');
var { BODY_XPATH, COMMENTS_DISCARD_XPATH, COMMENTS_XPATH, DISCARD_IMAGE_ELEMENTS,
    OVERALL_DISCARD_XPATH, PRECISION_DISCARD_XPATH, TEASER_DISCARD_XPATH } = require('./xpaths');
var P_FORMATTING = new Set(['hi', 'ref']);
var TABLE_ELEMS = new Set(['td', 'th']);
var TABLE_ALL = new Set(['td', 'th', 'hi']);
var FORMATTING = new Set(['hi', 'ref', 'span']);
var CODES_QUOTES = new Set(['code', 'quote']);
var NOT_AT_THE_END = new Set(['head', 'ref']);

function trim(str) {
    return str.trim().replace(/\s+/g, ' '); 
};


function handleTitles(element, options) {
    if (element.children.length === 0) {
        return processNode(element, options);
    } else {
        var title = element.cloneNode(true);
        Array.from(element.children).forEach(child => {
            var processedChild = handleTextnode(child, options, { commentsFix: false });
            if (processedChild) {
                title.appendChild(processedChild);
            }
            child.tagName = 'DONE';
        });
        if (title && textCharsTest(title.textContent.trim())) {
            return title;
        }
    }
    return null;
}

function handleFormatting(element, options) {
    var formatting = processNode(element, options);
    if (element.children.length === 0 && !formatting) {
        return null;
    }
    var parent = element.parentNode || element.previousElementSibling;
    if (!parent || !FORMATTING_PROTECTED.has(parent.tagName.toLowerCase())) {
        var processedElement = document.createElement('p');
        processedElement.appendChild(formatting);
        return processedElement;
    }
    return formatting;
}

function handleLists(element, options) {
    var processedElement = document.createElement(element.tagName);

    if (element.textContent.trim()) {
        var newChildElem = document.createElement('item');
        newChildElem.textContent = element.textContent;
        processedElement.appendChild(newChildElem);
    }

    Array.from(element.querySelectorAll('item')).forEach(child => {
        var newChildElem = document.createElement('item');
        if (child.children.length === 0) {
            var processedChild = processNode(child, options);
            if (processedChild) {
                newChildElem.textContent = processedChild.textContent;
                if (processedChild.nextSibling && processedChild.nextSibling.textContent.trim()) {
                    newChildElem.textContent += ' ' + processedChild.nextSibling.textContent.trim();
                }
                processedElement.appendChild(newChildElem);
            }
        } else {
            processNestedElements(child, newChildElem, options);
            if (child.nextSibling && child.nextSibling.textContent.trim()) {
                var lastSubchild = Array.from(newChildElem.children).filter(el => el.tagName !== 'DONE').pop();
                if (lastSubchild) {
                    if (!lastSubchild.nextSibling || !lastSubchild.nextSibling.textContent.trim()) {
                        lastSubchild.textContent += child.nextSibling.textContent.trim();
                    } else {
                        lastSubchild.textContent += ' ' + child.nextSibling.textContent.trim();
                    }
                }
            }
        }
        if (newChildElem.textContent || newChildElem.children.length > 0) {
            updateElemRendition(child, newChildElem);
            processedElement.appendChild(newChildElem);
        }
        child.tagName = 'DONE';
    });
    element.tagName = 'DONE';

    if (isTextElement(processedElement)) {
        updateElemRendition(element, processedElement);
        return processedElement;
    }
    return null;
}

function handleQuotes(element, options) {
    // if (isCodeBlockElement(element)) {
    //     return handleCodeBlocks(element);
    // }

    var processedElement = document.createElement(element.tagName);
    Array.from(element.children).forEach(child => {
        var processedChild = processNode(child, options);
        if (processedChild) {
            processedElement.appendChild(processedChild);
        }
        child.tagName = 'DONE';
    });

    // if (isTextElement(processedElement)) {
    //     // Remove nested quote tags
    //     Array.from(processedElement.querySelectorAll('quote')).forEach(quoteElem => {
    //         var parent = quoteElem.parentNode;
    //         while (quoteElem.firstChild) {
    //             parent.insertBefore(quoteElem.firstChild, quoteElem);
    //         }
    //         parent.removeChild(quoteElem);
    //     });
    //     return processedElement;
    // }
    return null;
}

function handleParagraphs(element, potentialTags, options) {
    element.removeAttribute('class');
    element.removeAttribute('id');

    if (element.children.length === 0) {
        return processNode(element, options);
    }

    var processedElement = document.createElement(element.tagName);
    Array.from(element.children).forEach(child => {
        if (!potentialTags.has(child.tagName.toLowerCase()) && child.tagName !== 'DONE') {
            console.debug(`unexpected in p: ${child.tagName} ${child.textContent} ${child.nextSibling ? child.nextSibling.textContent : ''}`);
            return;
        }

        var processedChild = handleTextnode(child, options, { commentsFix: false, preserveSpaces: true });
        if (processedChild) {
            if (processedChild.tagName === 'P') {
                console.debug(`extra p within p: ${processedChild.tagName} ${processedChild.textContent} ${processedChild.nextSibling ? processedChild.nextSibling.textContent : ''}`);
                processedElement.textContent += (processedElement.textContent ? ' ' : '') + processedChild.textContent;
                child.tagName = 'DONE';
                return;
            }

            var newsub = document.createElement(child.tagName);
            if (P_FORMATTING.has(processedChild.tagName.toLowerCase())) {
                if (processedChild.children.length > 0) {
                    Array.from(processedChild.children).forEach(item => {
                        if (textCharsTest(item.textContent)) {
                            item.textContent = ' ' + item.textContent;
                        }
                        while (item.firstChild) {
                            newsub.appendChild(item.firstChild);
                        }
                    });
                }
                if (child.tagName === 'HI') {
                    newsub.setAttribute('rend', child.getAttribute('rend'));
                } else if (child.tagName === 'REF') {
                    if (child.hasAttribute('target')) {
                        newsub.setAttribute('target', child.getAttribute('target'));
                    }
                }
            }

            newsub.textContent = processedChild.textContent;
            if (processedChild.nextSibling) {
                newsub.textContent += processedChild.nextSibling.textContent;
            }
            processedElement.appendChild(newsub);
        }
        child.tagName = 'DONE';
    });

    if (processedElement.children.length > 0) {
        var lastElem = processedElement.lastElementChild;
        if (lastElem.tagName === 'LB' && !lastElem.nextSibling) {
            lastElem.remove();
        }
        return processedElement;
    }
    if (processedElement.textContent) {
        return processedElement;
    }
    console.debug(`discarding p-child: ${processedElement.outerHTML}`);
    return null;
}

function handleOtherElements(element, potentialTags, options) {
    if (element.tagName === 'DIV' && element.classList.contains('w3-code')) {
        return handleCodeBlocks(element);
    }

    if (!potentialTags.has(element.tagName.toLowerCase())) {
        if (element.tagName !== 'DONE') {
            // console.debug(`discarding element: ${element.tagName} ${element.textContent}`);
        }
        return null;
    }

    if (element.tagName === 'DIV') {
        var processedElement = handleTextnode(element, options, { commentsFix: false, preserveSpaces: true });
        if (processedElement && textCharsTest(processedElement.textContent)) {
            processedElement.removeAttribute('class');
            processedElement.removeAttribute('id');
            if (processedElement.tagName === 'DIV') {
                processedElement.tagName = 'P';
            }
            return processedElement;
        }
    } else {
        console.debug(`unexpected element seen: ${element.tagName} ${element.textContent}`);
    }

    return null;
}
function defineCellType(isHeader) {
    // Determine cell element type and mint new element.
    // define tag
    const cellElement = document.createElement("cell");
    if (isHeader) {
      cellElement.setAttribute("role", "head");
    }
    return cellElement;
  }

function handleTable(tableElem, potentialTags, options) {
    var newTable = document.createElement('table');

    // Strip these structural elements
    ['thead', 'tbody', 'tfoot'].forEach(tag => {
        Array.from(tableElem.getElementsByTagName(tag)).forEach(el => {
            while (el.firstChild) {
                el.parentNode.insertBefore(el.firstChild, el);
            }
            el.parentNode.removeChild(el);
        });
    });

    // Calculate maximum number of columns per row, including colspan
    var maxCols = Math.max(...Array.from(tableElem.querySelectorAll('tr')).map(tr => 
        Array.from(tr.querySelectorAll('td, th')).reduce((sum, td) => sum + (parseInt(td.getAttribute('colspan')) || 1), 0)
    ));

    let seenHeaderRow = false;
    let seenHeader = false;
    let newRow = document.createElement('row');
    if (maxCols > 1) {
        newRow.setAttribute('span', maxCols.toString());
    }

    Array.from(tableElem.querySelectorAll('*')).forEach(subelement => {
        if (subelement.tagName === 'TR') {
            if (newRow.children.length > 0) {
                newTable.appendChild(newRow);
                newRow = document.createElement('row');
                if (maxCols > 1) {
                    newRow.setAttribute('span', maxCols.toString());
                }
                seenHeaderRow = seenHeaderRow || seenHeader;
            }
        } else if (TABLE_ELEMS.has(subelement.tagName.toLowerCase())) {
            var isHeader = subelement.tagName === 'TH' && !seenHeaderRow;
            seenHeader = seenHeader || isHeader;
            var newChildElem = defineCellType(isHeader);

            if (subelement.children.length === 0) {
                var processedCell = processNode(subelement, options);
                if (processedCell) {
                    newChildElem.textContent = processedCell.textContent;
                    newChildElem.innerHTML += processedCell.innerHTML;
                }
            } else {
                newChildElem.textContent = subelement.textContent;
                newChildElem.innerHTML += subelement.innerHTML;
                subelement.tagName = 'DONE';
                Array.from(subelement.querySelectorAll('*')).forEach(child => {
                    if (TABLE_ALL.has(child.tagName.toLowerCase())) {
                        if (TABLE_ELEMS.has(child.tagName.toLowerCase())) {
                            child.tagName = 'cell';
                        }
                        var processedSubchild = handleTextnode(child, options, { preserveSpaces: true, commentsFix: true });
                        if (processedSubchild) {
                            defineNewelem(processedSubchild, newChildElem);
                        }
                    } else if (child.tagName === 'LIST' && options.focus === 'recall') {
                        var processedSubchild = handleLists(child, options);
                        if (processedSubchild) {
                            newChildElem.appendChild(processedSubchild);
                        }
                    } else {
                        var processedSubchild = handleTextelem(child, new Set([...potentialTags, 'div']), options);
                        if (processedSubchild) {
                            defineNewelem(processedSubchild, newChildElem);
                        }
                    }
                    child.tagName = 'DONE';
                });
            }

            if (newChildElem.textContent || newChildElem.children.length > 0) {
                newRow.appendChild(newChildElem);
            }
        } else if (subelement.tagName === 'TABLE') {
            return;
        }
        subelement.tagName = 'DONE';
    });

    newRow.removeAttribute('span');

    if (newRow.children.length > 0) {
        newTable.appendChild(newRow);
    }
    if (newTable.children.length > 0) {
        return newTable;
    }
    return null;
}

function defineNewelem(processedElem, origElem) {
    // Create a new sub-element if necessary.
    if (processedElem !== null) {
        const childElem = document.createElement(processedElem.tagName);
        childElem.textContent = processedElem.textContent;
        
        // Handle tail text by appending it as a text node
        if (processedElem.nextSibling && processedElem.nextSibling.nodeType === 3) {
            childElem.appendChild(document.createTextNode(processedElem.nextSibling.textContent));
        }

        origElem.appendChild(childElem);
    }
}


function handleImage(element) {
    var processedElement = document.createElement(element.tagName);

    var src = element.getAttribute('data-src') || element.getAttribute('src');
    if (src && isImageFile(src)) {
        processedElement.setAttribute('src', src);
    } else {
        for (var attr of element.getAttributeNames()) {
            if (attr.startsWith('data-src') && isImageFile(element.getAttribute(attr))) {
                processedElement.setAttribute('src', element.getAttribute(attr));
                break;
            }
        }
    }

    if (element.hasAttribute('alt')) {
        processedElement.setAttribute('alt', element.getAttribute('alt'));
    }
    if (element.hasAttribute('title')) {
        processedElement.setAttribute('title', element.getAttribute('title'));
    }

    if (!processedElement.hasAttributes() || !processedElement.hasAttribute('src')) {
        return null;
    }

    if (!processedElement.getAttribute('src').startsWith('http')) {
        processedElement.setAttribute('src', processedElement.getAttribute('src').replace(/^\/\//, 'http://'));
    }

    return processedElement;
}
function handleTextelem(element, potentialTags, options) {
    let newElement = null;
    switch (element.tagName.toLowerCase()) {
        case 'list':
            newElement = handleLists(element, options);
            break;
        case 'code':
        case 'quote':
            newElement = handleQuotes(element, options);
            break;
        case 'head':
            newElement = handleTitles(element, options);
            break;
        case 'p':
            newElement = handleParagraphs(element, potentialTags, options);
            break;
        case 'lb':
            if (textCharsTest(element.nextSibling && element.nextSibling.textContent)) {
                element = processNode(element, options);
                if (element) {
                    newElement = document.createElement('p');
                    newElement.textContent = element.nextSibling.textContent;
                }
            }
            break;
        case 'hi':
        case 'ref':
        case 'span':
            newElement = handleFormatting(element, options);
            break;
        case 'table':
            if (potentialTags.has('table')) {
                newElement = handleTable(element, potentialTags, options);
            }
            break;
        case 'graphic':
            if (potentialTags.has('graphic')) {
                newElement = handleImage(element);
            }
            break;
        default:
            newElement = handleOtherElements(element, potentialTags, options);
    }
    return newElement;
}

function recoverWildText(tree, resultBody, options, potentialTags = TAG_CATALOG) {
    console.debug('Recovering wild text elements');
    let searchExpr = 'blockquote, code, p, pre, q, quote, table, div.w3-code';
    if (options.focus === "recall") {
        potentialTags.add('div');
        potentialTags.add('lb');
        searchExpr += ', div, lb, list';
    }
    
    var searchTree = pruneUnwantedSections(tree, potentialTags, options);
    
    if (!potentialTags.has('ref')) {
        ['a', 'ref', 'span'].forEach(tag => {
            Array.from(searchTree.getElementsByTagName(tag)).forEach(el => {
                while (el.firstChild) {
                    el.parentNode.insertBefore(el.firstChild, el);
                }
                el.parentNode.removeChild(el);
            });
        });
    } else {
        Array.from(searchTree.getElementsByTagName('span')).forEach(el => {
            while (el.firstChild) {
                el.parentNode.insertBefore(el.firstChild, el);
            }
            el.parentNode.removeChild(el);
        });
    }

    var subelems = searchTree.querySelectorAll(searchExpr);
    subelems.forEach(e => {
        var processed = handleTextelem(e, potentialTags, options);
        if (processed) {
            resultBody.appendChild(processed);
        }
    });

    return resultBody;
}

function pruneUnwantedSections(tree, potentialTags, options) {
    var favorPrecision = options.focus === "precision";
    
    tree = pruneUnwantedNodes(tree, OVERALL_DISCARD_XPATH, { withBackup: true });

    if (!potentialTags.has('graphic')) {
        tree = pruneUnwantedNodes(tree, DISCARD_IMAGE_ELEMENTS);
    }

    if (options.focus !== "recall") {
        tree = pruneUnwantedNodes(tree, TEASER_DISCARD_XPATH);
        if (favorPrecision) {
            tree = pruneUnwantedNodes(tree, PRECISION_DISCARD_XPATH);
        }
    }

    for (let i = 0; i < 2; i++) {
        tree = deleteByLinkDensity(tree, 'div', { backtracking: true, favorPrecision });
        tree = deleteByLinkDensity(tree, 'list', { backtracking: false, favorPrecision });
        tree = deleteByLinkDensity(tree, 'p', { backtracking: false, favorPrecision });
    }

    if (potentialTags.has('table') || favorPrecision) {
        Array.from(tree.getElementsByTagName('table')).forEach(elem => {
            if (linkDensityTestTables(elem)) {
                deleteElement(elem, { keepTail: false });
            }
        });
    }

    if (favorPrecision) {
        while (tree.lastElementChild && tree.lastElementChild.tagName === 'HEAD') {
            deleteElement(tree.lastElementChild, { keepTail: false });
        }
        tree = deleteByLinkDensity(tree, 'head', { backtracking: false, favorPrecision: true });
        tree = deleteByLinkDensity(tree, 'quote', { backtracking: false, favorPrecision: true });
    }

    return tree;
}

function _extract(document, options) {
    var potentialTags = new Set(TAG_CATALOG);
    if (options.tables) {
        ['table', 'td', 'th', 'tr'].forEach(tag => potentialTags.add(tag));
    }
    if (options.images) {
        potentialTags.add('graphic');
    }
    if (options.links) {
        potentialTags.add('ref');
    }

    var resultBody = document.createElement('body');


    
    for (var expr of BODY_XPATH) {
        var subtree;
        //xpath with JSDOM
        try{
        subtree = document.evaluate(
            expr,
            document,
            null,
            9,
            null
          )?.singleNodeValue;
        }catch(e){
            // console.log(e);
        }


        // console.log(subtree.textContent);

        if (!subtree) continue;

        var prunedSubtree = pruneUnwantedSections(subtree, potentialTags, options);
        
        if (prunedSubtree.children.length === 0) continue;

        var ptest = prunedSubtree.querySelectorAll('p');
        var factor = options.focus === "precision" ? 1 : 3;

        if (!ptest.length || Array.from(ptest).reduce((sum, p) => sum + p.textContent.length, 0) < options.minExtractedSize * factor) {
            potentialTags.add('div');
        }

        if (!potentialTags.has('ref')) {
            Array.from(prunedSubtree.getElementsByTagName('ref')).forEach(el => {
                while (el.firstChild) {
                    el.parentNode.insertBefore(el.firstChild, el);
                }
                el.parentNode.removeChild(el);
            });
        }
        if (!potentialTags.has('span')) {
            Array.from(prunedSubtree.getElementsByTagName('span')).forEach(el => {
                while (el.firstChild) {
                    el.parentNode.insertBefore(el.firstChild, el);
                }
                el.parentNode.removeChild(el);
            });
        }

        // console.debug(Array.from(potentialTags).sort());

        var subelems = prunedSubtree.querySelectorAll('*');
        if (Array.from(subelems).every(e => e.tagName === 'LB')) {
            subelems = [prunedSubtree];
        }

        subelems.forEach(e => {
            var el = handleTextelem(e, potentialTags, options);
            if (el) resultBody.appendChild(el);
        });

        while (resultBody.lastElementChild && NOT_AT_THE_END.has(resultBody.lastElementChild.tagName.toLowerCase())) {
            deleteElement(resultBody.lastElementChild, { keepTail: false });
        }

        if (resultBody.children.length > 1) {
            console.debug(expr);
            break;
        }
    }

    var tempText = Array.from(resultBody.querySelectorAll('*'))
        .map(el => el.textContent)
        .join(' ')
        .trim();

        // console.log(resultBody.outerHTML);

    return [resultBody, tempText, potentialTags];
}

function extractContent(dom, options) {


    var backupTree = dom;


    let [resultBody, tempText, potentialTags] = _extract(dom, options);

    // console.debug(tempText);
  

    if (resultBody.children.length === 0 || tempText.length < options.minExtractedSize) {
        resultBody = recoverWildText(dom, resultBody, options, potentialTags);
        tempText = Array.from(resultBody.querySelectorAll('*'))
            .map(el => el.textContent)
            .join(' ')
            .trim();
    }

    // Filter output
    Array.from(resultBody.querySelectorAll('done')).forEach(el => el.remove());
    Array.from(resultBody.querySelectorAll('div')).forEach(el => {
        while (el.firstChild) {
            el.parentNode.insertBefore(el.firstChild, el);
        }
        el.remove();
    });

    return [resultBody, tempText, tempText.length];
}

function processCommentsNode(elem, potentialTags, options) {
    if (potentialTags.has(elem.tagName.toLowerCase())) {
        var processedElement = handleTextnode(elem, options, { commentsFix: true });
        if (processedElement) {
            processedElement.removeAttribute('class');
            processedElement.removeAttribute('id');
            return processedElement;
        }
    }
    return null;
}

function extractComments(tree, options) {
    var commentsBody = document.createElement('body');
    var potentialTags = new Set(TAG_CATALOG);

    for (var expr of COMMENTS_XPATH) {

        var subtree = document.evaluate(
                expr,
                tree,
                null,
                9,
                null
              )?.singleNodeValue;
          

        if (!subtree) continue;

        var prunedSubtree = pruneUnwantedNodes(subtree, COMMENTS_DISCARD_XPATH);

        ['a', 'ref', 'span'].forEach(tag => {
            Array.from(prunedSubtree.getElementsByTagName(tag)).forEach(el => {
                while (el.firstChild) {
                    el.parentNode.insertBefore(el.firstChild, el);
                }
                el.parentNode.removeChild(el);
            });
        });

        Array.from(prunedSubtree.querySelectorAll('*')).forEach(e => {
            var processed = processCommentsNode(e, potentialTags, options);
            if (processed) {
                commentsBody.appendChild(processed);
            }
        });

        if (commentsBody.children.length > 0) {
            console.debug(expr);
            deleteElement(subtree, { keepTail: false });
            break;
        }
    }

    var tempComments = Array.from(commentsBody.querySelectorAll('*'))
        .map(el => el.textContent)
        .join(' ')
        .trim();

    return [commentsBody, tempComments, tempComments.length, tree];
}



function addSubElement(newChildElem, subelem, processedSubchild) {
    const subChildElem = SubElement(newChildElem, processedSubchild.tag);
    subChildElem.text = processedSubchild.text;
    subChildElem.tail = processedSubchild.tail;
    for (const [attr, value] of Object.entries(subelem.attrib)) {
        subChildElem.setAttribute(attr, value);
    }
}

function processNestedElements(child, newChildElem, options) {
    newChildElem.text = child.text;
    for (const subelem of child.getElementsByTagName("*")) {
        let processedSubchild;
        if (subelem.tagName === "list") {
            processedSubchild = handleLists(subelem, options);
            if (processedSubchild !== null) {
                newChildElem.appendChild(processedSubchild);
            }
        } else {
            processedSubchild = handleTextnode(subelem, options, { commentsFix: false });
            if (processedSubchild !== null) {
                addSubElement(newChildElem, subelem, processedSubchild);
            }
        }
        subelem.tagName = "done";
    }
}

function updateElemRendition(elem, newElem) {
    if (elem.getAttribute("rend") !== null) {
        newElem.setAttribute("rend", elem.getAttribute("rend"));
    }
}

function isTextElement(elem) {
    return elem !== null && textCharsTest(elem.textContent.trim());
}

function isCodeBlockElement(element) {
    if (element.getAttribute("lang") || element.tagName === "code") {
        return true;
    }
    const parent = element.parentNode;
    if (parent !== null && parent.getAttribute("class").includes("highlight")) {
        return true;
    }
    const code = element.querySelector("code");
    if (code !== null && element.children.length === 1) {
        return true;
    }
    return false;
}

function handleCodeBlocks(element) {
    const processedElement = element.cloneNode(true);
    for (const child of processedElement.getElementsByTagName("*")) {
        child.tagName = "done";
    }
    processedElement.tagName = "code";
    return processedElement;
}

module.exports = {
    extractContent,
    extractComments
};