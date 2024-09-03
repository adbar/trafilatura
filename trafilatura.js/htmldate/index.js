var core = require('./core');
var extractors = require('./extractors');
var meta = require('./meta');
var settings = require('./settings');
var utils = require('./utils');
var validators = require('./validators');

module.exports = {
    ...core,
    ...extractors,
    ...meta,
    ...settings,
    ...utils,
    ...validators
};