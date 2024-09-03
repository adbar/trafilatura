// Module regrouping baseline and basic extraction functions.
var { JSDOM } = require('jsdom');

var BASIC_CLEAN_XPATH = [
  '//aside', '//footer', '//figure', '//nav',
  '//header', '//script', '//style', '//link'
]; // Assuming these are the elements to be removed

function deleteElement(elem) {
  if (elem.parentNode) {
    elem.parentNode.removeChild(elem);
  }
}

function basicCleaning(tree) {
  BASIC_CLEAN_XPATH.forEach(xpath => {
    var elements = tree.evaluate(xpath, tree, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
    for (let i = 0; i < elements.snapshotLength; i++) {
      deleteElement(elements.snapshotItem(i));
    }
  });
  return tree;
}

function loadHtml(content) {
  if (typeof content === 'string') {
    var dom = new JSDOM(content);
    return dom.window.document;
  }
  return content;
}

function trim(text) {
  return text.replace(/^\s+|\s+$/g, '').replace(/\s+/g, ' ');
}

function baseline(filecontent) {
  var tree = loadHtml(filecontent);
  var postbody = tree.createElement('body');
  if (!tree) {
    return [postbody, '', 0];
  }

  // Scrape from JSON text
  let tempText = "";
  var jsonScripts = tree.querySelectorAll('script[type="application/ld+json"]');
  for (var elem of jsonScripts) {
    if (elem.textContent && elem.textContent.includes('articleBody')) {
      try {
        var jsonBody = JSON.parse(elem.textContent).articleBody;
        if (jsonBody) {
          var text = jsonBody.includes('<p>') ? 
            new JSDOM(jsonBody).window.document.body.textContent : 
            jsonBody;
          var p = tree.createElement('p');
          p.textContent = trim(text);
          postbody.appendChild(p);
          tempText += tempText ? " " + text : text;
        }
      } catch (error) {
        // Handle JSON parsing error
      }
    }
  }
  if (tempText.length > 100) {
    return [postbody, tempText, tempText.length];
  }

  basicCleaning(tree);

  // Scrape from article tag
  tempText = "";
  var articles = tree.querySelectorAll('article');
  for (var articleElem of articles) {
    var text = trim(articleElem.textContent);
    if (text.length > 100) {
      var p = tree.createElement('p');
      p.textContent = text;
      postbody.appendChild(p);
      tempText += tempText ? " " + text : text;
    }
  }
  if (postbody.childNodes.length > 0) {
    return [postbody, tempText, tempText.length];
  }

  // Scrape from text paragraphs
  var results = new Set();
  tempText = "";
  var elements = tree.querySelectorAll('blockquote, code, p, pre, q, quote');
  for (var element of elements) {
    var entry = trim(element.textContent);
    if (!results.has(entry)) {
      var p = tree.createElement('p');
      p.textContent = entry;
      postbody.appendChild(p);
      tempText += tempText ? " " + entry : entry;
      results.add(entry);
    }
  }
  if (tempText.length > 100) {
    return [postbody, tempText, tempText.length];
  }

  // Default strategy: clean the tree and take everything
  var bodyElem = tree.querySelector('body');
  if (bodyElem) {
    var p = tree.createElement('p');
    p.textContent = Array.from(bodyElem.childNodes)
      .map(node => trim(node.textContent))
      .join('\n');
    postbody.appendChild(p);
    return [postbody, p.textContent, p.textContent.length];
  }

  // New fallback
  var text = html2txt(tree, false);
  var p = tree.createElement('p');
  p.textContent = text;
  postbody.appendChild(p);
  return [postbody, text, text.length];
}

function html2txt(content, clean = true) {
  var tree = loadHtml(content);
  if (!tree) return "";
  
  var body = tree.querySelector('body');
  if (!body) return "";
  
  if (clean) {
    basicCleaning(body);
  }
  
  return body.textContent.split().join(' ').trim();
}

module.exports = {
  baseline,
  html2txt,
  basicCleaning,
  loadHtml,
  trim
};