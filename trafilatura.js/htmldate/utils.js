var axios = require('axios');
var { JSDOM } = require('jsdom');
var { MAX_FILE_SIZE } = require('./settings');

var LOGGER = console;

var UNICODE_ALIASES = new Set(["utf-8", "utf_8"]);

var DOCTYPE_TAG = /^< ?! ?DOCTYPE.+?\/ ?>/i;
var FAULTY_HTML = /(<html.*?)\s*\/>/i;

class Extractor {
    constructor(extensive_search, max_date, min_date, original_date, outputformat) {
        this.extensive = extensive_search;
        this.format = outputformat;
        this.max = max_date;
        this.min = min_date;
        this.original = original_date;
    }
}

function is_wrong_document(data) {
    return !data || data.length > MAX_FILE_SIZE;
}

function isutf8(data) {
    try {
        new TextDecoder('utf-8').decode(data);
        return true;
    } catch (error) {
        return false;
    }
}

function detect_encoding(bytesobject) {
    if (isutf8(bytesobject)) {
        return ["utf-8"];
    }

    // In JavaScript, we don't have direct equivalents for cchardet or charset_normalizer
    // You might want to use a library like jschardet for this functionality
    // For now, we'll just return a default encoding
    return ["utf-8"];
}

function decode_file(filecontent) {
    if (typeof filecontent === 'string') {
        return filecontent;
    }

    let htmltext = null;
    for (var guessed_encoding of detect_encoding(filecontent)) {
        try {
            htmltext = new TextDecoder(guessed_encoding).decode(filecontent);
            break;
        } catch (error) {
            LOGGER.warn(`wrong encoding detected: ${guessed_encoding}`);
            htmltext = null;
        }
    }

    return htmltext || new TextDecoder('utf-8', { fatal: false }).decode(filecontent);
}

function decode_response(response) {
    var resp_content = response.data || response;
    return decode_file(resp_content);
}

async function fetch_url(url) {
    try {
        var response = await axios.get(url, {
            timeout: 30000,
            maxContentLength: MAX_FILE_SIZE,
            responseType: 'arraybuffer'
        });

        if (response.status !== 200) {
            LOGGER.error(`not a 200 response: ${response.status} for URL ${url}`);
            return null;
        }

        if (is_wrong_document(response.data)) {
            LOGGER.error(`incorrect input data for URL ${url}`);
            return null;
        }

        return decode_response(response);
    } catch (error) {
        LOGGER.error(`download error: ${url} ${error}`);
        return null;
    }
}

function is_dubious_html(beginning) {
    return !beginning.includes('html');
}

function repair_faulty_html(htmlstring, beginning) {
    if (beginning.includes('doctype')) {
        var [firstline, ...rest] = htmlstring.split('\n');
        htmlstring = firstline.replace(DOCTYPE_TAG, '') + '\n' + rest.join('\n');
    }

    var lines = htmlstring.split('\n');
    for (let i = 0; i < Math.min(3, lines.length); i++) {
        if (lines[i].includes('<html') && lines[i].endsWith('/>')) {
            lines[i] = lines[i].replace(FAULTY_HTML, '$1>');
            break;
        }
    }
    return lines.join('\n');
}

function load_html(htmlobject) {
    if (htmlobject instanceof JSDOM) {
        return htmlobject;
    }

    if (typeof htmlobject !== 'string' && !(htmlobject instanceof Buffer)) {
        throw new TypeError(`incompatible input type: ${typeof htmlobject}`);
    }

    if (typeof htmlobject === 'string' && htmlobject.startsWith('http') && !htmlobject.includes(' ')) {
        LOGGER.debug(`URL detected, downloading: ${htmlobject}`);
        return fetch_url(htmlobject).then(result => {
            if (result === null) {
                throw new Error(`URL couldn't be processed: ${htmlobject}`);
            }
            return load_html(result);
        });
    }

    htmlobject = decode_file(htmlobject);
    var beginning = htmlobject.slice(0, 50).toLowerCase();
    htmlobject = repair_faulty_html(htmlobject, beginning);

    let dom;
    try {
        dom = new JSDOM(htmlobject);
    } catch (error) {
        LOGGER.error(`JSDOM parsing failed: ${error}`);
        return null;
    }

    if (is_dubious_html(beginning) && dom.window.document.body.children.length < 2) {
        LOGGER.error(`parsed tree length: ${dom.window.document.body.children.length}, wrong data type or not valid HTML`);
        return null;
    }

    return dom;
}

function clean_html(tree, elemlist) {
    elemlist.forEach(tag => {
        var elements = tree.window.document.getElementsByTagName(tag);
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
    });
    return tree;
}

function trim_text(string) {
    return string.split(/\s+/).join(' ').trim();
}

module.exports = {
    Extractor,
    is_wrong_document,
    isutf8,
    detect_encoding,
    decode_file,
    decode_response,
    fetch_url,
    is_dubious_html,
    repair_faulty_html,
    load_html,
    clean_html,
    trim_text
};