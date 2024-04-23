# pylint:disable-msg=E0611
"""
Listing a series of settings that are applied module-wide.
"""

from configparser import ConfigParser
from datetime import datetime

try:
    from os import sched_getaffinity
except ImportError:
    sched_getaffinity = None
    from os import cpu_count

from pathlib import Path

from lxml.etree import XPath


def use_config(filename=None, config=None):
    """
    Use configuration object or read and parse a settings file.
    """
    if config is not None:
        return config

    if filename is None:
        filename = str(Path(__file__).parent / "settings.cfg")
    elif not Path(filename).is_file():
        raise FileNotFoundError("The given config file does not exist")

    config = ConfigParser()
    config.read(filename)
    return config


DEFAULT_CONFIG = use_config()


class Extractor:
    "Defines a class to store all extraction options."
    __slots__ = [
    'config',
    # general
    'format', 'fast', 'focus', 'comments',
    'formatting', 'links', 'images', 'tables', 'dedup', 'lang',
    # extraction size
    'min_extracted_size', 'min_output_size',
    'min_output_comm_size', 'min_extracted_comm_size',
    # deduplication
    'min_duplcheck_size', 'max_repetitions',
    # rest
    'max_file_size', 'min_file_size', 'max_tree_size',
    # meta
    'source', 'url', 'only_with_metadata', 'tei_validation',
    'date_params',
    'author_blacklist', 'url_blacklist'
    ]
    # consider dataclasses for Python 3.7+
    def __init__(self, *, config=DEFAULT_CONFIG, output_format="txt",
                 fast=False, precision=False, recall=False,
                 comments=True, formatting=False, links=False, images=False,
                 tables=True, dedup=False, lang=None, max_tree_size=None,
                 url=None, source=None, only_with_metadata=False, tei_validation=False,
                 author_blacklist=None, url_blacklist=None, date_params=None):
        self._add_config(config)
        self.format = output_format
        self.fast = fast
        if recall:
            self.focus = "recall"
        elif precision:
            self.focus = "precision"
        else:
            self.focus = "balanced"
        self.comments = comments
        self.formatting = formatting or output_format == "markdown"
        self.links = links
        self.images = images
        self.tables = tables
        self.dedup = dedup
        self.lang = lang
        self.max_tree_size = max_tree_size
        self.url = url
        self.source = url or source
        self.only_with_metadata = only_with_metadata
        self.tei_validation = tei_validation
        self.author_blacklist = author_blacklist or set()
        self.url_blacklist = url_blacklist or set()
        self.date_params = date_params or \
                           set_date_params(self.config.getboolean('DEFAULT', 'EXTENSIVE_DATE_SEARCH'))

    def _add_config(self, config):
        "Store options loaded from config file."
        self.min_extracted_size = config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE')
        self.min_output_size = config.getint('DEFAULT', 'MIN_OUTPUT_SIZE')
        self.min_output_comm_size = config.getint('DEFAULT', 'MIN_OUTPUT_COMM_SIZE')
        self.min_extracted_comm_size = config.getint('DEFAULT', 'MIN_EXTRACTED_COMM_SIZE')
        self.min_duplcheck_size = config.getint('DEFAULT', 'MIN_DUPLCHECK_SIZE')
        self.max_repetitions = config.getint('DEFAULT', 'MAX_REPETITIONS')
        self.max_file_size = config.getint('DEFAULT', 'MAX_FILE_SIZE')
        self.min_file_size = config.getint('DEFAULT', 'MIN_FILE_SIZE')
        self.config = config  # todo: remove?


def args_to_extractor(args, url=None):
    "Derive extractor configuration from CLI args."
    options = Extractor(
                  config=use_config(filename=args.config_file), output_format=args.output_format,
                  precision=args.precision, recall=args.recall,
                  comments=args.no_comments, tables=args.no_tables,
                  dedup=args.deduplicate, lang=args.target_language,
                  url=url, only_with_metadata=args.only_with_metadata,
                  tei_validation=args.validate_tei
              )
    for attr in ("fast", "formatting", "images", "links"):
        setattr(options, attr, getattr(args, attr))
    return options


def set_date_params(extensive=True):
    "Provide default parameters for date extraction."
    return {
               "original_date": True,
               "extensive_search": extensive,
               "max_date": datetime.now().strftime("%Y-%m-%d")
           }


# Safety checks
PARALLEL_CORES = min(len(sched_getaffinity(0)) if sched_getaffinity else cpu_count(), 16)  # 16 processes at most
LRU_SIZE = 4096

# Files
MAX_FILES_PER_DIRECTORY = 1000
FILENAME_LEN = 8

# Network
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

BASIC_CLEAN_XPATH = XPath(".//aside|.//footer|.//script|.//style")

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
