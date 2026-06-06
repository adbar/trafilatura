# pylint:disable-msg=E0611
"""
Listing a series of settings that are applied module-wide.
"""

import argparse
import os
from configparser import ConfigParser
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

from lxml.etree import Element, XPath, _Element

from .utils import line_processing

# sched_getaffinity (Linux-only) with fallback
_get_affinity = getattr(os, "sched_getaffinity", None)
CPU_COUNT = len(_get_affinity(0)) if _get_affinity is not None else (os.cpu_count() or 1)


SUPPORTED_FMT_CLI = ["csv", "json", "html", "markdown", "txt", "xml", "xmltei"]
SUPPORTED_FORMATS = set(SUPPORTED_FMT_CLI) | {"python"}  # for bare_extraction() only


def use_config(filename: str | None = None, config: ConfigParser | None = None) -> ConfigParser:
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
    "min_extracted_size": "MIN_EXTRACTED_SIZE",
    "min_output_size": "MIN_OUTPUT_SIZE",
    "min_output_comm_size": "MIN_OUTPUT_COMM_SIZE",
    "min_extracted_comm_size": "MIN_EXTRACTED_COMM_SIZE",
    "min_duplcheck_size": "MIN_DUPLCHECK_SIZE",
    "max_repetitions": "MAX_REPETITIONS",
    "max_file_size": "MAX_FILE_SIZE",
    "min_file_size": "MIN_FILE_SIZE",
}


def _get_optional_int(config: ConfigParser, option: str) -> int | None:
    "Read an optional positive integer setting; None when empty or non-numeric."
    value = config.get("DEFAULT", option, fallback="").strip()
    return int(value) if value.isdigit() else None


# todo Python >= 3.10: use dataclass with slots=True
class Extractor:
    "Defines a class to store all extraction options."

    __slots__ = [
        "config",
        # general
        "format",
        "fast",
        "focus",
        "comments",
        "formatting",
        "links",
        "images",
        "tables",
        "dedup",
        "lang",
        # extraction size
        "min_extracted_size",
        "min_output_size",
        "min_output_comm_size",
        "min_extracted_comm_size",
        # deduplication
        "min_duplcheck_size",
        "max_repetitions",
        # rest
        "max_file_size",
        "min_file_size",
        "max_tree_size",
        # meta
        "source",
        "url",
        "with_metadata",
        "only_with_metadata",
        "tei_validation",
        "date_params",
        "author_blacklist",
        "url_blacklist",
    ]

    # config-derived integer sizes, populated by _add_config via CONFIG_MAPPING
    min_extracted_size: int
    min_output_size: int
    min_output_comm_size: int
    min_extracted_comm_size: int
    min_duplcheck_size: int
    max_repetitions: int
    max_file_size: int
    min_file_size: int

    def __init__(
        self,
        *,
        config: ConfigParser = DEFAULT_CONFIG,
        output_format: str = "txt",
        fast: bool = False,
        precision: bool = False,
        recall: bool = False,
        comments: bool = True,
        formatting: bool = False,
        links: bool = False,
        images: bool = False,
        tables: bool = True,
        dedup: bool = False,
        lang: str | None = None,
        url: str | None = None,
        source: str | None = None,
        with_metadata: bool = False,
        only_with_metadata: bool = False,
        tei_validation: bool = False,
        author_blacklist: set[str] | None = None,
        url_blacklist: set[str] | None = None,
        date_params: dict[str, str] | None = None,
    ):
        self._set_source(url, source)
        self._set_format(output_format)
        # single normalization point: an explicit config=None falls back to defaults
        self._add_config(config or DEFAULT_CONFIG)
        self.fast: bool = fast
        self.focus: str = "recall" if recall else "precision" if precision else "balanced"
        self.comments: bool = comments
        self.formatting: bool = formatting or self.format == "markdown"
        self.links: bool = links
        self.images: bool = images
        self.tables: bool = tables
        self.dedup: bool = dedup
        self.lang: str | None = lang
        self.url: str | None = url
        self.only_with_metadata: bool = only_with_metadata
        self.tei_validation: bool = tei_validation
        self.author_blacklist: set[str] = author_blacklist or set()
        self.url_blacklist: set[str] = url_blacklist or set()
        self.with_metadata: bool = with_metadata or only_with_metadata or bool(url_blacklist) or output_format == "xmltei"
        self.date_params: dict[str, Any] = date_params or set_date_params(
            self.config.getboolean("DEFAULT", "EXTENSIVE_DATE_SEARCH")
        )
        self.max_tree_size: int | None = _get_optional_int(self.config, "MAX_TREE_SIZE")

    def _set_source(self, url: str | None, source: str | None) -> None:
        "Set the source attribute in a robust way."
        source = url or source
        self.source = source and source.encode("utf-8", "replace").decode("utf-8")

    def _set_format(self, chosen_format: str) -> None:
        "Store the format if supported and raise an error otherwise."
        if chosen_format not in SUPPORTED_FORMATS:
            raise AttributeError(f"Cannot set format, must be one of: {', '.join(sorted(SUPPORTED_FORMATS))}")
        self.format = chosen_format

    def _add_config(self, config: ConfigParser) -> None:
        "Store options loaded from config file."
        for key, value in CONFIG_MAPPING.items():
            setattr(self, key, config.getint("DEFAULT", value))
        self.config = config


def args_to_extractor(args: argparse.Namespace, url: str | None = None) -> Extractor:
    "Derive extractor configuration from CLI args."
    options = Extractor(
        config=use_config(filename=args.config_file),
        output_format=args.output_format,
        formatting=args.formatting,
        precision=args.precision,
        recall=args.recall,
        comments=args.no_comments,
        tables=args.no_tables,
        dedup=args.deduplicate,
        lang=args.target_language,
        url=url,
        with_metadata=args.with_metadata,
        only_with_metadata=args.only_with_metadata,
        tei_validation=args.validate_tei,
    )
    for attr in ("fast", "images", "links"):
        setattr(options, attr, getattr(args, attr))
    return options


def set_date_params(extensive: bool = True) -> dict[str, Any]:
    "Provide default parameters for date extraction."
    return {
        "original_date": True,
        "extensive_search": extensive,
        "max_date": datetime.now().strftime("%Y-%m-%d"),
    }


# todo Python >= 3.10: use dataclass with slots=True
class Document:
    "Defines a class to store all necessary data and metadata fields for extracted information."

    __slots__ = [
        "title",
        "author",
        "url",
        "hostname",
        "description",
        "sitename",
        "date",
        "categories",
        "tags",
        "fingerprint",
        "id",
        "license",
        "body",
        "comments",
        "commentsbody",
        "raw_text",
        "text",
        "language",
        "image",
        "pagetype",
        "filedate",
        # 'locale'?
    ]

    def __init__(
        self,
        *,
        title: str | None = None,
        author: str | None = None,
        url: str | None = None,
        hostname: str | None = None,
        description: str | None = None,
        sitename: str | None = None,
        date: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        fingerprint: str | None = None,
        idval: str | None = None,
        license_val: str | None = None,
        body: _Element | None = None,
        comments: str | None = None,
        commentsbody: _Element | None = None,
        raw_text: str | None = None,
        text: str | None = None,
        language: str | None = None,
        image: str | None = None,
        pagetype: str | None = None,
        filedate: str | None = None,
    ):
        self.title: str | None = title
        self.author: str | None = author
        self.url: str | None = url
        self.hostname: str | None = hostname
        self.description: str | None = description
        self.sitename: str | None = sitename
        self.date: str | None = date
        self.categories: list[str] | None = categories
        self.tags: list[str] | None = tags
        self.fingerprint: str | None = fingerprint
        self.id: str | None = idval
        self.license: str | None = license_val
        self.body: _Element = body if body is not None else Element("body")
        self.comments: str | None = comments
        self.commentsbody: _Element = commentsbody if commentsbody is not None else Element("body")
        self.raw_text: str | None = raw_text
        self.text: str | None = text
        self.language: str | None = language
        self.image: str | None = image
        self.pagetype: str | None = pagetype
        self.filedate: str | None = filedate

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Document":
        "Set a series of attributes using a dictionary."
        doc = cls()
        for key, value in data.items():
            setattr(doc, key, value)
        return doc

    def clean_and_trim(self) -> None:
        "Limit text length and trim the attributes."
        for slot in self.__slots__:
            value = getattr(self, slot)
            if isinstance(value, str):
                # length
                if len(value) > 10000:
                    value = value[:9999] + "…"
                # HTML entities, remove spaces and control characters
                value = line_processing(unescape(value))
                setattr(self, slot, value)

    def as_dict(self) -> dict[str, str | None]:
        "Convert the document to a dictionary."
        return {attr: getattr(self, attr, None) for attr in self.__slots__}


# Safety checks
PARALLEL_CORES = min(CPU_COUNT, 16)  # 16 processes at most
LRU_SIZE = 4096

# Files
MAX_FILES_PER_DIRECTORY = 1000
FILENAME_LEN = 8

# Network
MAX_LINKS = 10**6
MAX_SITEMAPS_SEEN = 10**4


# filters
CUT_EMPTY_ELEMS = {
    "article",
    "b",
    "blockquote",
    "dd",
    "div",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "i",
    "li",
    "main",
    "p",
    "pre",
    "q",
    "section",
    "span",
    "strong",
}
# 'meta', 'td', 'a', 'caption', 'dl', 'header',
# 'colgroup', 'col',
# CUT_EMPTY_ELEMS = {'div', 'span'}

# order could matter, using lists to keep extraction deterministic
MANUALLY_CLEANED = [
    # important
    "aside",
    "embed",
    "fencedframe",
    "footer",
    "form",
    "head",
    "iframe",
    "menu",
    "object",
    "script",
    # other content
    "applet",
    "audio",
    "canvas",
    "figure",
    "map",
    "picture",
    "svg",
    "video",
    # secondary
    "area",
    "blink",
    "button",
    "datalist",
    "dialog",
    "frame",
    "frameset",
    "fieldset",
    "link",
    "input",
    "ins",
    "label",
    "legend",
    "marquee",
    "math",
    "menuitem",
    "nav",
    "noindex",
    "noscript",
    "optgroup",
    "option",
    "output",
    "param",
    "progress",
    "rp",
    "rt",
    "rtc",
    "select",
    "source",
    "style",
    "track",
    "textarea",
    "time",
    "use",
]
# 'meta', 'hr', 'img', 'data', 'details', 'summary'

MANUALLY_STRIPPED = [
    "abbr",
    "acronym",
    "address",
    "bdi",
    "bdo",
    "big",
    "cite",
    "data",
    "dfn",
    "font",
    "hgroup",
    "img",
    "ins",
    "mark",
    "meta",
    "ruby",
    "small",
    "tbody",
    "template",
    "tfoot",
    "thead",
]
# 'center', 'rb', 'wbr'

BASIC_CLEAN_XPATH = XPath(".//aside|.//div[contains(@class|@id, 'footer')]|.//fencedframe|.//footer|.//script|.//style")

TAG_CATALOG = frozenset(["blockquote", "code", "del", "head", "hi", "lb", "list", "p", "pre", "quote"])
# + list(CUT_EMPTY_ELEMS)

# mapping for languages known to py3langid
JUSTEXT_LANGUAGES = {
    "af": "Afrikaans",
    "an": "Aragonese",
    "ar": "Arabic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "br": "Breton",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "ga": "Irish",
    "gl": "Galician",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "ht": "Haitian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "jv": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "kn": "Kannada",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lb": "Luxembourgish",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ms": "Malay",
    "mt": "Maltese",
    "nb": "Norwegian_Bokmal",
    "ne": "Nepali",
    "nl": "Dutch",
    "nn": "Norwegian_Nynorsk",
    "no": "Norwegian_Bokmal",
    "oc": "Occitan",
    "pl": "Polish",
    "pt": "Portuguese",
    "qu": "Quechua",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sq": "Albanian",
    "sr": "Serbian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "vo": "Volapuk",
    "wa": "Walloon",
    # no justext stoplist available: 'ja' (Japanese), 'zh' (Chinese)
}
