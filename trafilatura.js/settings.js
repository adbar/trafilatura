// Listing a series of settings that are applied module-wide.

var os = require('os');
var { lineProcessing } = require('./utils');

var { convertHTMLSpecialChars } = require( "./html-special-chars.js");

var SUPPORTED_FMT_CLI = ["csv", "json", "html", "markdown", "txt", "xml", "xmltei"];
var SUPPORTED_FORMATS = new Set([...SUPPORTED_FMT_CLI, "python"]);

var DEFAULT_CONFIG = {
    DOWNLOAD_TIMEOUT: '30',
    MAX_FILE_SIZE: '20000000',
    MIN_FILE_SIZE: '10',
    SLEEP_TIME: '5',
    USER_AGENTS: '',
    COOKIE: '',
    MAX_REDIRECTS: '2',
    MIN_EXTRACTED_SIZE: '250',
    MIN_EXTRACTED_COMM_SIZE: '1',
    MIN_OUTPUT_SIZE: '1',
    MIN_OUTPUT_COMM_SIZE: '1',
    EXTRACTION_TIMEOUT: '30',
    MIN_DUPLCHECK_SIZE: '100',
    MAX_REPETITIONS: '2',
    EXTENSIVE_DATE_SEARCH: 'on',
    EXTERNAL_URLS: 'off'
  };

var CONFIG_MAPPING = {
    'min_extracted_size': 'MIN_EXTRACTED_SIZE',
    'min_output_size': 'MIN_OUTPUT_SIZE',
    'min_output_comm_size': 'MIN_OUTPUT_COMM_SIZE',
    'min_extracted_comm_size': 'MIN_EXTRACTED_COMM_SIZE',
    'min_duplcheck_size': 'MIN_DUPLCHECK_SIZE',
    'max_repetitions': 'MAX_REPETITIONS',
    'max_file_size': 'MAX_FILE_SIZE',
    'min_file_size': 'MIN_FILE_SIZE'
};

class Extractor {
    constructor({
        config = DEFAULT_CONFIG,
        outputFormat = "txt",
        fast = false,
        precision = false,
        recall = false,
        comments = true,
        formatting = false,
        links = false,
        images = false,
        tables = true,
        dedup = false,
        lang = null,
        maxTreeSize = null,
        url = null,
        source = null,
        withMetadata = false,
        onlyWithMetadata = false,
        teiValidation = false,
        authorBlacklist = null,
        urlBlacklist = null,
        dateParams = null
    } = {}) {
        this.setFormat(outputFormat);
        this.addConfig(config);
        this.fast = fast;
        this.focus = recall ? "recall" : precision ? "precision" : "balanced";
        this.comments = comments;
        this.formatting = formatting || this.format === "markdown";
        this.links = links;
        this.images = images;
        this.tables = tables;
        this.dedup = dedup;
        this.lang = lang;
        this.maxTreeSize = maxTreeSize;
        this.url = url;
        this.source = url || source;
        this.onlyWithMetadata = onlyWithMetadata;
        this.teiValidation = teiValidation;
        this.authorBlacklist = authorBlacklist || new Set();
        this.urlBlacklist = urlBlacklist || new Set();
        this.withMetadata = withMetadata || onlyWithMetadata || urlBlacklist || outputFormat === "xmltei";
        this.dateParams = dateParams || setDateParams(config.EXTENSIVE_DATE_SEARCH === 'True');
    }

    setFormat(chosenFormat) {
        if (!SUPPORTED_FORMATS.has(chosenFormat)) {
            throw new Error(`Cannot set format, must be one of: ${Array.from(SUPPORTED_FORMATS).sort().join(', ')}`);
        }
        this.format = chosenFormat;
    }

    addConfig(config) {
        for (var [key, value] of Object.entries(CONFIG_MAPPING)) {
            this[key] = parseInt(config[value], 10);
        }
        this.config = config;
    }
}

function argsToExtractor(args, url = null) {
    return new Extractor({
        config: useConfig(args.configFile),
        outputFormat: args.outputFormat,
        formatting: args.formatting,
        precision: args.precision,
        recall: args.recall,
        comments: args.noComments,
        tables: args.noTables,
        dedup: args.deduplicate,
        lang: args.targetLanguage,
        url: url,
        withMetadata: args.withMetadata,
        onlyWithMetadata: args.onlyWithMetadata,
        teiValidation: args.validateTei,
        fast: args.fast,
        images: args.images,
        links: args.links
    });
}

function setDateParams(extensive = true) {
    return {
        originalDate: true,
        extensiveSearch: extensive,
        maxDate: new Date().toISOString().split('T')[0]
    };
}

class Document {
    constructor() {
        this.title = null;
        this.author = null;
        this.url = null;
        this.hostname = null;
        this.description = null;
        this.sitename = null;
        this.date = null;
        this.categories = null;
        this.tags = null;
        this.fingerprint = null;
        this.id = null;
        this.license = null;
        this.body = null;
        this.comments = null;
        this.commentsbody = null;
        this.rawText = null;
        this.text = null;
        this.language = null;
        this.image = null;
        this.pagetype = null;
        this.filedate = null;
    }

    static fromDict(data) {
        var doc = new Document();
        Object.assign(doc, data);
        return doc;
    }

    setAttributes(attributes) {
        Object.assign(this, attributes);
    }

    cleanAndTrim() {
        for (var [key, value] of Object.entries(this)) {
            if (typeof value === 'string') {
                let newValue = value;
                if (newValue.length > 10000) {
                    newValue = newValue.slice(0, 9999) + '…';
                }
                newValue = lineProcessing(convertHTMLSpecialChars(newValue));
                this[key] = newValue;
            }
        }
    }

    asDict() {
        return { ...this };
    }
}

// Safety checks
var PARALLEL_CORES = Math.min(os.cpus().length, 16);  // 16 processes at most
var LRU_SIZE = 4096;

// Files
var MAX_FILES_PER_DIRECTORY = 1000;
var FILENAME_LEN = 8;

// Network
var MAX_LINKS = 10**6;
var MAX_SITEMAPS_SEEN = 10**4;

// Filters
var CUT_EMPTY_ELEMS = new Set(['article', 'b', 'blockquote', 'dd', 'div', 'dt', 'em',
                                 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'main',
                                 'p', 'pre', 'q', 'section', 'span', 'strong']);

var MANUALLY_CLEANED = [
    'aside', 'embed', 'footer', 'form', 'head', 'iframe', 'menu', 'object', 'script',
    'applet', 'audio', 'canvas', 'figure', 'map', 'picture', 'svg', 'video',
    'area', 'blink', 'button', 'datalist', 'dialog',
    'frame', 'frameset', 'fieldset', 'link', 'input', 'ins', 'label', 'legend',
    'marquee', 'math', 'menuitem', 'nav', 'noscript', 'optgroup', 'option',
    'output', 'param', 'progress', 'rp', 'rt', 'rtc', 'select', 'source',
    'style', 'track', 'textarea', 'time', 'use',
];

var MANUALLY_STRIPPED = [
    'abbr', 'acronym', 'address', 'bdi', 'bdo', 'big', 'cite', 'data', 'dfn',
    'font', 'hgroup', 'img', 'ins', 'mark', 'meta', 'ruby', 'small', 'tbody',
    'template', 'tfoot', 'thead',
];

var BASIC_CLEAN_XPATH = "//aside|//div[contains(@class|@id, 'footer')]|//footer|//script|//style";

var TAG_CATALOG = new Set(['blockquote', 'code', 'del', 'head', 'hi', 'lb', 'list', 'p', 'pre', 'quote']);

var JUSTEXT_LANGUAGES = {
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'cz': 'Czech',
    'da': 'Danish',
    'de': 'German',
    'en': 'English',
    'el': 'Greek',
    'es': 'Spanish',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'ko': 'Korean',
    'id': 'Indonesian',
    'it': 'Italian',
    'no': 'Norwegian_Nynorsk',
    'nl': 'Dutch',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sr': 'Serbian',
    'sv': 'Swedish',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
};

module.exports = {
    Extractor,
    Document,
    argsToExtractor,
    setDateParams,
    SUPPORTED_FMT_CLI,
    SUPPORTED_FORMATS,
    DEFAULT_CONFIG,
    PARALLEL_CORES,
    LRU_SIZE,
    MAX_FILES_PER_DIRECTORY,
    FILENAME_LEN,
    MAX_LINKS,
    MAX_SITEMAPS_SEEN,
    CUT_EMPTY_ELEMS,
    MANUALLY_CLEANED,
    MANUALLY_STRIPPED,
    BASIC_CLEAN_XPATH,
    TAG_CATALOG,
    JUSTEXT_LANGUAGES
};