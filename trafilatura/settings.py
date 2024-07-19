# pylint:disable-msg=E0611
"""
Listing a series of settings that are applied module-wide.
"""

from configparser import ConfigParser
from datetime import datetime
from html import unescape
from typing import Dict, Optional

try:
    from os import sched_getaffinity
    HAS_SCHED = True
except ImportError:
    from os import cpu_count
    HAS_SCHED = False

from pathlib import Path

from lxml.etree import XPath

from .utils import line_processing


SUPPORTED_FMT_CLI = ["csv", "json", "html", "markdown", "txt", "xml", "xmltei"]
SUPPORTED_FORMATS = set(SUPPORTED_FMT_CLI) | {"python"}  # for bare_extraction() only


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

CONFIG_MAPPING = {
    'min_extracted_size': 'MIN_EXTRACTED_SIZE',
    'min_output_size': 'MIN_OUTPUT_SIZE',
    'min_output_comm_size': 'MIN_OUTPUT_COMM_SIZE',
    'min_extracted_comm_size': 'MIN_EXTRACTED_COMM_SIZE',
    'min_duplcheck_size': 'MIN_DUPLCHECK_SIZE',
    'max_repetitions': 'MAX_REPETITIONS',
    'max_file_size': 'MAX_FILE_SIZE',
    'min_file_size': 'MIN_FILE_SIZE'
}


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
    'source', 'url', 'with_metadata', 'only_with_metadata', 'tei_validation',
    'date_params',
    'author_blacklist', 'url_blacklist'
    ]
    # consider dataclasses for Python 3.7+
    def __init__(self, *, config=DEFAULT_CONFIG, output_format="txt",
                 fast=False, precision=False, recall=False,
                 comments=True, formatting=False, links=False, images=False,
                 tables=True, dedup=False, lang=None, max_tree_size=None,
                 url=None, source=None, with_metadata=False, only_with_metadata=False, tei_validation=False,
                 author_blacklist=None, url_blacklist=None, date_params=None):
        self._set_format(output_format)
        self._add_config(config)
        self.fast = fast
        self.focus = "recall" if recall else "precision" if precision else "balanced"
        self.comments = comments
        self.formatting = formatting or self.format == "markdown"
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
        self.with_metadata = (with_metadata or only_with_metadata or
                              url_blacklist or output_format == "xmltei")
        self.date_params = (date_params or
                            set_date_params(self.config.getboolean('DEFAULT', 'EXTENSIVE_DATE_SEARCH')))

    def _set_format(self, chosen_format: str) -> None:
        "Store the format if supported and raise an error otherwise."
        if chosen_format not in SUPPORTED_FORMATS:
            raise AttributeError(f"Cannot set format, must be one of: {', '.join(sorted(SUPPORTED_FORMATS))}")
        self.format = chosen_format

    def _add_config(self, config):
        "Store options loaded from config file."
        for key, value in CONFIG_MAPPING.items():
            setattr(self, key, config.getint('DEFAULT', value))
        self.config = config


def args_to_extractor(args, url=None):
    "Derive extractor configuration from CLI args."
    options = Extractor(
                  config=use_config(filename=args.config_file), output_format=args.output_format,
                  formatting=args.formatting,
                  precision=args.precision, recall=args.recall,
                  comments=args.no_comments, tables=args.no_tables,
                  dedup=args.deduplicate, lang=args.target_language, url=url,
                  with_metadata=args.with_metadata, only_with_metadata=args.only_with_metadata,
                  tei_validation=args.validate_tei
              )
    for attr in ("fast", "images", "links"):
        setattr(options, attr, getattr(args, attr))
    return options


def set_date_params(extensive=True):
    "Provide default parameters for date extraction."
    return {
               "original_date": True,
               "extensive_search": extensive,
               "max_date": datetime.now().strftime("%Y-%m-%d")
           }


class Document:  # consider dataclasses for Python 3.7+
    "Defines a class to store all necessary data and metadata fields for extracted information."
    __slots__ = [
    'title', 'author', 'url', 'hostname', 'description', 'sitename',
    'date', 'categories', 'tags', 'fingerprint', 'id', 'license',
    'body', 'comments', 'commentsbody', 'raw_text', 'text',
    'language', 'image', 'pagetype', 'filedate'  # 'locale'?
    ]
    def __init__(self) -> None:
        for slot in self.__slots__:
            setattr(self, slot, None)

    def __getattr__(self, name: str) -> None:
        raise AttributeError("% attribute not present in Document", name)

    def __setattr__(self, name: str, value) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)

    @classmethod
    def from_dict(cls, data: dict):
        "Set a series of attributes using a dictionary."
        doc = cls()
        for key, value in data.items():
            setattr(doc, key, value)
        return doc

    def set_attributes(self, **kwargs) -> None:
        "Helper function to (re-)set a series of attributes."
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

    def clean_and_trim(self) -> None:
        "Limit text length and trim the attributes."
        for slot in self.__slots__:
            value = getattr(self, slot)
            if isinstance(value, str):
                # length
                if len(value) > 10000:
                    value = value[:9999] + '…'
                # HTML entities, remove spaces and control characters
                value = line_processing(unescape(value))
                setattr(self, slot, value)

    def as_dict(self) -> Dict[str, Optional[str]]:
        "Convert the document to a dictionary."
        return {
            attr: getattr(self, attr, None)
            for attr in self.__slots__
        }


# Safety checks
PARALLEL_CORES = min(len(sched_getaffinity(0)) if HAS_SCHED else cpu_count(), 16)  # 16 processes at most
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

BASIC_CLEAN_XPATH = XPath(".//aside|.//div[contains(@class|@id, 'footer')]|.//footer|.//script|.//style")

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
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    # 'zh': '',
}
