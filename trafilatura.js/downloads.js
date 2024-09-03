// All functions needed to steer and execute downloads of web documents.

var axios = require('axios');
var https = require('https');
var { URL } = require('url');
var { UrlStore } = require('./utils');

var DEFAULT_CONFIG = {
    MAX_REDIRECTS: 5,
    DOWNLOAD_TIMEOUT: 30,
    USER_AGENTS: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ],
    COOKIE: null
};

class Response {
    constructor(data, status, url) {
        this.data = data;
        this.headers = null;
        this.html = null;
        this.status = status;
        this.url = url;
    }

    storeHeaders(headerDict) {
        this.headers = Object.fromEntries(
            Object.entries(headerDict).map(([k, v]) => [k.toLowerCase(), v])
        );
    }

    decodeData(decode) {
        if (decode && this.data) {
            this.html = this.data.toString('utf-8');
        }
    }

    asDict() {
        return {
            data: this.data,
            headers: this.headers,
            html: this.html,
            status: this.status,
            url: this.url
        };
    }
}

function determineHeaders(config = DEFAULT_CONFIG) {
    var headers = {
        'User-Agent': config.USER_AGENTS[Math.floor(Math.random() * config.USER_AGENTS.length)]
    };
    if (config.COOKIE) {
        headers['Cookie'] = config.COOKIE;
    }
    return headers;
}

async function fetchUrl(url, decode = true, noSsl = false, config = DEFAULT_CONFIG, options = null) {
    var response = await fetchResponse(url, { decode, noSsl, withHeaders: false, config });
    if (response && response.data) {
        if (!options) {
            options = { config };
        }
        return handleResponse(url, response, decode, options);
    }
    return null;
}

async function fetchResponse(url, { decode = false, noSsl = false, withHeaders = false, config = DEFAULT_CONFIG } = {}) {
    try {
        var axiosConfig = {
            url,
            method: 'GET',
            headers: determineHeaders(config),
            timeout: config.DOWNLOAD_TIMEOUT * 1000,
            maxRedirects: config.MAX_REDIRECTS,
            validateStatus: null,
            httpsAgent: new https.Agent({
                rejectUnauthorized: !noSsl
            })
        };

        var axiosResponse = await axios(axiosConfig);

        var response = new Response(axiosResponse.data, axiosResponse.status, axiosResponse.config.url);
        if (withHeaders) {
            response.storeHeaders(axiosResponse.headers);
        }
        response.decodeData(decode);
        return response;
    } catch (error) {
        console.error(`Error fetching ${url}:`, error.message);
        return null;
    }
}

function handleResponse(url, response, decode, options) {
    var lenTest = (response.html || response.data || '').length;
    if (response.status !== 200) {
        console.error(`Not a 200 response: ${response.status} for URL ${url}`);
    } else if (isAcceptableLength(lenTest, options)) {
        return decode ? response.html : response;
    }
    return null;
}

function isAcceptableLength(length, options) {
    // Implement your length check logic here
    return length > 0 && length < (options.config.MAX_FILE_SIZE || 20000000);
}

function addToCompressedDict(inputList, blacklist = null, urlFilter = null, urlStore = null, compression = false, verbose = false) {
    if (!urlStore) {
        urlStore = new UrlStore({ compressed: compression, strict: false, verbose });
    }

    var uniqueInputList = [...new Set(inputList)];

    let filteredList = uniqueInputList;
    if (blacklist) {
        filteredList = filteredList.filter(u => !blacklist.has(u.replace(/[^/?#]+$/, '')));
    }

    if (urlFilter) {
        filteredList = filteredList.filter(u => urlFilter.some(f => u.includes(f)));
    }

    urlStore.addUrls(filteredList);
    return urlStore;
}

async function loadDownloadBuffer(urlStore, sleepTime = 5000) {
    while (true) {
        var bufferList = urlStore.getDownloadUrls({ timeLimit: sleepTime, maxUrls: 100000 });
        if (bufferList.length > 0 || urlStore.done) {
            break;
        }
        await new Promise(resolve => setTimeout(resolve, sleepTime));
    }
    return [bufferList, urlStore];
}

async function* bufferedDownloads(bufferList, downloadThreads, decode = true, options = null) {
    var worker = decode ? url => fetchUrl(url, true, false, DEFAULT_CONFIG, options) : fetchResponse;

    for (let i = 0; i < bufferList.length; i += 10000) {
        var chunk = bufferList.slice(i, i + 10000);
        var promises = chunk.map(url => worker(url));
        var results = await Promise.all(promises);
        for (let j = 0; j < chunk.length; j++) {
            yield [chunk[j], results[j]];
        }
    }
}

module.exports = {
    Response,
    fetchUrl,
    fetchResponse,
    addToCompressedDict,
    loadDownloadBuffer,
    bufferedDownloads
};