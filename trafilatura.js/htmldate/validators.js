var { CACHE_SIZE, MIN_DATE } = require('./settings');
var { Extractor } = require('./utils');

var LOGGER = console;

function is_valid_date(date_input, outputformat, earliest, latest) {
    // safety check
    if (date_input === null) {
        return false;
    }

    let dateobject;
    if (date_input instanceof Date) {
        dateobject = date_input;
    } else {
        try {
            if (outputformat === 'YYYY-MM-DD') {
                dateobject = new Date(date_input.slice(0, 4), date_input.slice(5, 7) - 1, date_input.slice(8, 10));
            } else {
                dateobject = new Date(date_input);
            }
        } catch (error) {
            return false;
        }
    }

    if (
        earliest.getFullYear() <= dateobject.getFullYear() &&
        dateobject.getFullYear() <= latest.getFullYear() &&
        earliest.getTime() <= dateobject.getTime() &&
        dateobject.getTime() <= latest.getTime()
    ) {
        return true;
    }
    LOGGER.debug(`date not valid: ${date_input}`);
    return false;
}

function is_valid_format(outputformat) {
    // test with date object
    var dateobject = new Date(2017, 8, 1, 0, 0);
    try {
        dateobject.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (err) {
        LOGGER.error(`wrong output format or type: ${outputformat} ${err}`);
        return false;
    }
    // test in abstracto (could be the only test)
    if (typeof outputformat !== 'string' || !outputformat.includes('%')) {
        LOGGER.error(`malformed output format: ${outputformat}`);
        return false;
    }
    return true;
}

function plausible_year_filter(htmlstring, pattern, yearpat, earliest, latest, incomplete = false) {
    var occurrences = new Map();
    var matches = htmlstring.match(new RegExp(pattern, 'g')) || [];
    
    matches.forEach(item => {
        var count = occurrences.get(item) || 0;
        occurrences.set(item, count + 1);
    });

    for (var [item, count] of occurrences) {
        var year_match = item.match(yearpat);
        if (!year_match) {
            LOGGER.debug(`not a year pattern: ${item}`);
            occurrences.delete(item);
            continue;
        }

        var lastdigits = year_match[1];
        let potential_year;
        if (!incomplete) {
            potential_year = parseInt(lastdigits);
        } else {
            var century = lastdigits[0] === '9' ? '19' : '20';
            potential_year = parseInt(century + lastdigits);
        }

        if (!(earliest.getFullYear() <= potential_year && potential_year <= latest.getFullYear())) {
            LOGGER.debug(`no potential year: ${item}`);
            occurrences.delete(item);
        }
    }

    return occurrences;
}

function compare_values(reference, attempt, options) {
    try {
        var timestamp = new Date(attempt).getTime() / 1000;
        if (options.original) {
            reference = reference ? Math.min(reference, timestamp) : timestamp;
        } else {
            reference = Math.max(reference, timestamp);
        }
    } catch (err) {
        LOGGER.debug(`Date parsing exception: ${err} for string ${attempt}`);
    }
    return reference;
}

function filter_ymd_candidate(bestmatch, pattern, original_date, copyear, outputformat, min_date, max_date) {
    if (bestmatch) {
        var pagedate = `${bestmatch[1]}-${bestmatch[2]}-${bestmatch[3]}`;
        if (is_valid_date(pagedate, 'YYYY-MM-DD', min_date, max_date) &&
            (copyear === 0 || parseInt(bestmatch[1]) >= copyear)) {
            LOGGER.debug(`date found for pattern "${pattern}": ${pagedate}`);
            return convert_date(pagedate, 'YYYY-MM-DD', outputformat);
        }
    }
    return null;
}

function convert_date(datestring, inputformat, outputformat) {
    if (inputformat === outputformat) {
        return datestring;
    }
    if (datestring instanceof Date) {
        return datestring.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
    }
    var dateobject = new Date(datestring);
    return dateobject.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
}

function check_extracted_reference(reference, options) {
    if (reference > 0) {
        var dateobject = new Date(reference * 1000);
        var converted = dateobject.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
        if (is_valid_date(converted, options.format, options.min, options.max)) {
            return converted;
        }
    }
    return null;
}

function check_date_input(date_object, default_date) {
    if (date_object instanceof Date) {
        return date_object;
    }
    if (typeof date_object === 'string') {
        try {
            return new Date(date_object);
        } catch (error) {
            LOGGER.warning(`invalid datetime string: ${date_object}`);
        }
    }
    return default_date;
}

function get_min_date(min_date) {
    return check_date_input(min_date, MIN_DATE);
}

function get_max_date(max_date) {
    return check_date_input(max_date, new Date());
}

module.exports = {
    is_valid_date,
    is_valid_format,
    plausible_year_filter,
    compare_values,
    filter_ymd_candidate,
    convert_date,
    check_extracted_reference,
    check_date_input,
    get_min_date,
    get_max_date
};