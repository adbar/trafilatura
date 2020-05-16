# pylint:disable-msg=E0611
"""
Listing a series of settings that are applied module-wide.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

from lxml.html.clean import Cleaner


MAX_FILE_SIZE = 20000000
MIN_FILE_SIZE = 10
SLEEP_TIME = 2


## extract
MIN_EXTRACTED_SIZE = 200
MIN_EXTRACTED_COMM_SIZE = 10
MIN_DUPLCHECK_SIZE = 100
MIN_OUTPUT_SIZE = 25
MIN_OUTPUT_COMM_SIZE = 10
# PROCESSING_TIMEOUT = 10

LRU_SIZE = 65536
MAX_REPETITIONS = 2

# filters
DETECTION_LANGUAGES = ['af', 'am', 'an', 'ar', 'as', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'dz', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'ga', 'gl', 'gu', 'he', 'hi', 'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'jv', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'la', 'lb', 'lo', 'lt', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'nb', 'ne', 'nl', 'nn', 'no', 'oc', 'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'ro', 'ru', 'rw', 'se', 'si', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'ug', 'uk', 'ur', 'vi', 'vo', 'wa', 'xh', 'zh', 'zu']
# less languages = smaller footprint
# DETECTION_LANGUAGES = ['de', 'en', 'es', 'fr', 'ja', 'nl', 'ru']

#CORPUS_VERSION = 2017.1

CUT_EMPTY_ELEMS = {'article', 'b', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                   'i', 'li', 'main', 'p', 'section', 'span', 'strong', 'td'}
                   # 'meta',

MANUALLY_CLEANED = ['area', 'aside', 'audio', 'del', 'blink', 'button', 'canvas', 'embed', 'figure',
                    'footer', 'form', 'head', 'iframe', 'link', 'input', 'label',
                    'map', 'marquee', 'math', 'nav', 'noscript', 'object', 'option',
                    'picture', 'rp', 'rt', 'script', 'style', 'svg', 'textarea', 'time', 'video']
                    # 'frame' 'frameset' 'source'

MANUALLY_STRIPPED = ['abbr', 'acronym', 'address', 'big', 'cite', 'font', 'img', 'ins', 'meta', 'ruby', 'small', 'wbr']

# HTML_CLEANER config # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
HTML_CLEANER = Cleaner()
HTML_CLEANER.annoying_tags = False # True
HTML_CLEANER.comments = True
HTML_CLEANER.embedded = False # True
HTML_CLEANER.forms = False # True
HTML_CLEANER.frames = False # True
HTML_CLEANER.javascript = False # True
HTML_CLEANER.links = False
HTML_CLEANER.meta = False
HTML_CLEANER.page_structure = False
HTML_CLEANER.processing_instructions = True
HTML_CLEANER.remove_unknown_tags = False
HTML_CLEANER.safe_attrs_only = False
HTML_CLEANER.scripts = False # True
HTML_CLEANER.style = False
HTML_CLEANER.remove_tags = MANUALLY_STRIPPED
# 'a', 'span', 'dd', 'sub', 'sup', 'center',
HTML_CLEANER.kill_tags = MANUALLY_CLEANED


TAG_CATALOG = frozenset(['blockquote', 'code', 'del', 'fw', 'head', 'hi', 'lb', 'list', 'p', 'pre', 'q', 'quote'])
# 'span', 'item'

# JUSTEXT_DEFAULT = 'German'
# JT_STOPLIST = None  # could be a list

JUSTEXT_LANGUAGES = {
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
    # 'ja': '',
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
    'uk': 'Ukranian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    # 'zh': '',
}
