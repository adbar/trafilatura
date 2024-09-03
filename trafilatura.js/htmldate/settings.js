
// Function cache
var CACHE_SIZE = 8192;

// Download
var MAX_FILE_SIZE = 20000000;

// Plausible dates
// earliest possible date to take into account (inclusive)
var MIN_DATE = new Date(1995, 0, 1); // Note: month is 0-indexed in JavaScript

// set an upper limit to the number of candidates
var MAX_POSSIBLE_CANDIDATES = 1000;

var CLEANING_LIST = [
    "applet",
    "audio",
    "canvas",
    "datalist",
    "embed",
    "frame",
    "frameset",
    "iframe",
    "label",
    "map",
    "math",
    "noframes",
    "object",
    "picture",
    "rdf",
    "svg",
    "track",
    "video",
];
// "figure", "input", "layer", "param", "source"

module.exports = {
    CACHE_SIZE,
    MAX_FILE_SIZE,
    MIN_DATE,
    MAX_POSSIBLE_CANDIDATES,
    CLEANING_LIST
};