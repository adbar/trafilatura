# pylint:disable-msg=E0611
"""
Listing a series of settings that are applied module-wide.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import configparser

from os import cpu_count
from pathlib import Path

from . import __version__


def use_config(filename=None, config=None):
    'Use configuration object or read and parse a settings file'
    # expert option: use config file directly
    if config is not None:
        return config
    # default filename
    if filename is None:
        filename = str(Path(__file__).parent / 'settings.cfg')
    # load
    config = configparser.ConfigParser()
    config.read(filename)
    return config

DEFAULT_CONFIG = use_config()


# Safety checks
DOWNLOAD_THREADS = min(cpu_count(), 16)  # 16 processes at most
TIMEOUT = 30
LRU_SIZE = 4096

# Files
MAX_FILES_PER_DIRECTORY = 1000
FILENAME_LEN = 8
FILE_PROCESSING_CORES = min(cpu_count(), 16)  # 16 processes at most

# Network
USER_AGENT = 'trafilatura/' + __version__ + ' (+https://github.com/adbar/trafilatura)'
USER_AGENTS = [USER_AGENT]
USER_AGENTS_NUM = len(USER_AGENTS)
MAX_SITEMAPS_SEEN = 10000


# filters
CUT_EMPTY_ELEMS = {'article', 'b', 'blockquote', 'dd', 'div', 'dt', 'em',
                   'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'main',
                   'p', 'pre', 'q', 'section', 'span', 'strong'}
                   # 'meta', 'td', 'a', 'caption', 'dl', 'header',
                   # 'colgroup', 'col',
#CUT_EMPTY_ELEMS = {'div', 'span'}

MANUALLY_CLEANED = [
    # important
    'aside', 'embed', 'footer', 'form', 'head', 'iframe', 'menu', 'object', 'script',
    # other content
    'applet', 'audio', 'canvas', 'figure', 'map', 'picture', 'svg', 'video',
    # secondary
    'area', 'blink', 'button', 'datalist', 'details', 'dialog',
    'frame', 'frameset', 'fieldset', 'link', 'input', 'ins', 'label', 'legend',
    'marquee', 'math', 'menuitem', 'nav', 'noscript', 'optgroup', 'option',
    'output', 'param', 'progress', 'rp', 'rt', 'rtc', 'select', 'source',
    'style', 'summary', 'track', 'template', 'textarea', 'time', 'use',
]
# 'meta', 'hr', 'img', 'data'

MANUALLY_STRIPPED = [
    'abbr', 'acronym', 'address', 'bdi', 'bdo', 'big', 'cite', 'data', 'dfn',
    'font', 'hgroup', 'img', 'ins', 'mark', 'meta', 'ruby', 'small', 'tbody',
    'tfoot', 'thead',
]
# 'center', 'rb', 'wbr'

TAG_CATALOG = frozenset(['blockquote', 'code', 'del', 'fw', 'head', 'hi', 'lb', 'list', 'p', 'pre', 'quote'])
# + list(CUT_EMPTY_ELEMS)


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
