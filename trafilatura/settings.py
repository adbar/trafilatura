# pylint:disable-msg=E0611
"""
Listing a series of settings that are applied module-wide.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import os

from configparser import ConfigParser
from os import cpu_count
from pathlib import Path

import psutil


def calculate_thread_count():
    """
    Calculate optimal number of download threads based on CPU and network conditions.
    """
    cpu_cores = psutil.cpu_count(logical=True)
    network_speed = 50  # Placeholder for network speed
    network_factor = max(1, network_speed // 10)
    return min(max(1, cpu_cores * network_factor), 20)

DOWNLOAD_THREADS = calculate_thread_count()


def calculate_memory_usage():
    """
    Calculate memory usage limit for caching based on system memory.
    """
    total_memory = psutil.virtual_memory().total
    return max(512, int(total_memory * 0.1 / (1024 ** 2)))

MAX_MEMORY_USAGE_MB = calculate_memory_usage()


def setup_logging():
    """
    Set up logging with adjustable verbosity.
    """
    log_level = os.getenv('TRAFILATURA_LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

setup_logging()


def use_config(filename=None, config=None):
    """
    Use configuration object or read and parse a settings file.
    """
    if config is not None:
        return config
    if filename is None:
        filename = str(Path(__file__).parent / 'settings.cfg')
    config = ConfigParser()
    config.read(filename)
    return config


DEFAULT_CONFIG = use_config()

# Retaining original settings
LRU_SIZE = 4096
MAX_FILES_PER_DIRECTORY = 1000
FILENAME_LEN = 8
FILE_PROCESSING_CORES = min(cpu_count(), 16)
MAX_LINKS = 10**6
MAX_SITEMAPS_SEEN = 10**4


# filters
CUT_EMPTY_ELEMS = {'article', 'b', 'blockquote', 'dd', 'div', 'dt', 'em',
                   'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'main',
                   'p', 'pre', 'q', 'section', 'span', 'strong'}
                   # 'meta', 'td', 'a', 'caption', 'dl', 'header',
                   # 'colgroup', 'col',
#CUT_EMPTY_ELEMS = {'div', 'span'}

# order could matter, using lists to keep extraction deterministic
MANUALLY_CLEANED = [
    # important
    'aside', 'embed', 'footer', 'form', 'head', 'iframe', 'menu', 'object', 'script',
    # other content
    'applet', 'audio', 'canvas', 'figure', 'map', 'picture', 'svg', 'video',
    # secondary
    'area', 'blink', 'button', 'datalist', 'dialog',
    'frame', 'frameset', 'fieldset', 'link', 'input', 'ins', 'label', 'legend',
    'marquee', 'math', 'menuitem', 'nav', 'noscript', 'optgroup', 'option',
    'output', 'param', 'progress', 'rp', 'rt', 'rtc', 'select', 'source',
    'style', 'track', 'textarea', 'time', 'use',
]
# 'meta', 'hr', 'img', 'data', 'details', 'summary'

MANUALLY_STRIPPED = [
    'abbr', 'acronym', 'address', 'bdi', 'bdo', 'big', 'cite', 'data', 'dfn',
    'font', 'hgroup', 'img', 'ins', 'mark', 'meta', 'ruby', 'small', 'tbody',
    'template', 'tfoot', 'thead',
]
# 'center', 'rb', 'wbr'

TAG_CATALOG = frozenset(['blockquote', 'code', 'del', 'head', 'hi', 'lb', 'list', 'p', 'pre', 'quote'])
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
