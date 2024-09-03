/**
 * @summary JavaScript port of Trafilatura, a web scraping library for text extraction
 * @author Adrien Barbaresi, et al (2019), Apache-2.0
 */

var { JSDOM } = require("jsdom");
var { baseline } = require("./baseline");
var { extractMetadata } = require("./metadata");
var { extractContent } = require("./main_extractor");
var { treeCleaning } = require("./htmlprocessing");
var { normalizeUnicode, loadHtml } = require("./utils");

var DEFAULT_CONFIG = {}; // Define your default configuration here
var TXT_FORMATS = new Set(["markdown", "txt"]);

class Document {
  constructor() {
    this.title = "";
    this.author = "";
    this.url = "";
    this.hostname = "";
    this.description = "";
    this.sitename = "";
    this.date = "";
    this.categories = [];
    this.tags = [];
    this.fingerprint = "";
    this.id = "";
    this.license = "";
    this.body = null;
    this.commentsbody = null;
    this.raw_text = "";
    this.text = "";
    this.comments = "";
  }

  asDict() {
    return { ...this };
  }
}

class Extractor {
  constructor(options = {}) {
    this.config = options.config || DEFAULT_CONFIG;
    this.outputFormat = options.outputFormat || "txt";
    this.fast = options.fast || false;
    this.precision = options.precision || false;
    this.recall = options.recall || false;
    this.comments = options.comments !== undefined ? options.comments : true;
    this.formatting = options.formatting || false;
    this.links = options.links || false;
    this.images = options.images || false;
    this.tables = options.tables !== undefined ? options.tables : true;
    this.dedup = options.dedup || false;
    this.lang = options.lang || null;
    this.maxTreeSize = options.maxTreeSize || null;
    this.url = options.url || null;
    this.withMetadata = options.withMetadata || false;
    this.onlyWithMetadata = options.onlyWithMetadata || false;
    this.teiValidation = options.teiValidation || false;
    this.authorBlacklist = options.authorBlacklist || new Set();
    this.urlBlacklist = options.urlBlacklist || new Set();
    this.dateParams = options.dateParams || null;
  }
}

function determineReturnString(document, options) {
  let returnString = "";

  if (options.outputFormat.includes("xml")) {
    // Implement XML output
  } else if (options.outputFormat === "csv") {
    // Implement CSV output
  } else if (options.outputFormat === "json") {
    // Implement JSON output
  } else if (options.outputFormat === "html") {
    // Implement HTML output
  } else {
    // Markdown and TXT
    let header = "";
    if (options.withMetadata) {
      header = "---\n";
      [
        "title",
        "author",
        "url",
        "hostname",
        "description",
        "sitename",
        "date",
        "categories",
        "tags",
        "fingerprint",
        "id",
        "license",
      ].forEach((attr) => {
        if (document[attr]) {
          header += `${attr}: ${document[attr]}\n`;
        }
      });
      header += "---\n";
    }
    returnString = `${header}${document.text}`;
    if (document.commentsbody) {
      returnString = `${returnString}\n${document.comments}`.trim();
    }
  }

  return normalizeUnicode(returnString);
}

function trafilaturaSequence(
  cleanedTree,
  cleanedTreeBackup,
  treeBackup,
  options
) {
  let [postbody, tempText, lenText] = extractContent(cleanedTree, options);

  if (!options.fast) {
    // Implement comparison with external extractors
  }

  if (lenText < options.minExtractedSize && options.focus !== "precision") {
    [postbody, tempText, lenText] = baseline(treeBackup.cloneNode(true));
  }

  return [postbody, tempText, lenText];
}

function bareExtraction(filecontent, options) {
  // try {
  var tree = filecontent;
  if (!tree) {
    console.error("empty HTML tree:", options.url);
    throw new Error("Empty HTML tree");
  }

  let document = new Document();

  if (options.withMetadata) {
    document = extractMetadata(
      tree,
      options.url,
      options.dateParams,
      options.fast,
      options.authorBlacklist
    );

    if (options.urlBlacklist.has(document.url)) {
      console.warn("blacklisted URL:", document.url);
      throw new Error("Blacklisted URL");
    }

    if (
      options.onlyWithMetadata &&
      !(document.date && document.title && document.url)
    ) {
      console.error("no metadata:", options.url);
      throw new Error("Missing metadata");
    }
  }

  let cleanedTree = treeCleaning(tree, options);
  var cleanedTreeBackup = cleanedTree.cloneNode(true);

  // Implement comment extraction if needed

  let [postbody, tempText, lenText] = trafilaturaSequence(
    cleanedTree,
    cleanedTreeBackup,
    tree,
    options
  );

  // Implement additional checks (tree size, language, etc.)

  if (options.outputFormat === "python") {
    document.text = postbody.textContent;
    if (options.comments) {
      document.comments = document.commentsbody
        ? document.commentsbody.textContent
        : "";
    }
    document.raw_text = document.text;
  } else {
    document.raw_text = tempText;
    document.commentsbody = document.commentsbody;
  }
  document.body = postbody;

  return document;
  // } catch (error) {
  //     console.warn('discarding data:', options.url);
  //     return null;
  // }
}

function extract(htmlOrDom, options = {}) {
  //convert html to dom if needed
  var document =
    typeof htmlOrDom == "string"
      ? new JSDOM(htmlOrDom).window.document
      : htmlOrDom;

  global.document = document;

  var extractorOptions = new Extractor(options);

  try {
    var doc = bareExtraction(document, extractorOptions);

    if (!doc) {
      return null;
    }

    if (!TXT_FORMATS.has(extractorOptions.outputFormat)) {
      if (extractorOptions.outputFormat === "python") {
        throw new Error(
          "'python' format only usable in bareExtraction() function"
        );
      }
      doc.id = options.recordId;
      // Implement fingerprint calculation if needed
    }

    return determineReturnString(doc, extractorOptions);
  } catch (error) {
    console.error("Processing error for", options.url, error);
    return null;
  }
}

module.exports = {
  extract,
  bareExtraction,
  Extractor,
  Document,
};
