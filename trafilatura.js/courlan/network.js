// Functions devoted to requests over the WWW.

var axios = require('axios');
var https = require('https');

// Simple logging mechanism
var LOGGER = {
    debug: console.debug,
    info: console.info,
    warn: console.warn,
    error: console.error
};

// Disable SSL certificate verification (Note: This is not recommended for production use)
var agent = new https.Agent({
    rejectUnauthorized: false
});

var RETRY_STRATEGY = {
    retries: 2,
    retryDelay: (retryCount) => {
        return retryCount * 1000; // 1s, 2s
    },
    retryCondition: (error) => {
        return [429, 499, 500, 502, 503, 504, 509, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598].includes(error.response?.status);
    }
};

var ACCEPTABLE_CODES = new Set([200, 300, 301, 302, 303, 304, 305, 306, 307, 308]);

var axiosInstance = axios.create({
    httpsAgent: agent,
    maxRedirects: 2,
    timeout: 10000,
    validateStatus: function (status) {
        return ACCEPTABLE_CODES.has(status);
    }
});

/**
 * Test final URL to handle redirects
 * @param {string} url - URL to check
 * @returns {Promise<string>} - The final URL seen
 * @throws {Error} - If the URL cannot be reached
 */
async function redirectionTest(url) {
    try {
        var response = await axiosInstance.head(url, {
            ...RETRY_STRATEGY
        });

        LOGGER.debug(`result found: ${response.request.res.responseUrl} ${response.status}`);
        return response.request.res.responseUrl;
    } catch (error) {
        LOGGER.error(`unknown error: ${url} ${error.message}`);
        throw new Error(`cannot reach URL: ${url}`);
    }
}

module.exports = {
    redirectionTest
};