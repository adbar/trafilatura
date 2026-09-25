# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML and text processing,
content filtering and language detection.
"""

import logging
import re
import sys
import zlib
from collections.abc import Callable, Iterable, Iterator, Mapping
from functools import lru_cache
from itertools import islice
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, cast
from unicodedata import normalize

# response compression
try:
    import brotli

    # output_buffer_limit (brotli >= 1.2) is the only way to bound the output:
    # process() otherwise returns the whole expansion, which voids the bomb cap
    try:
        brotli.Decompressor().process(b"", output_buffer_limit=1)
        HAS_BROTLI = True
    except Exception:  # pragma: no cover
        HAS_BROTLI = False
except ImportError:
    HAS_BROTLI = False

# zstd: stdlib from 3.14 on, official backport before
try:
    if sys.version_info >= (3, 14):
        from compression import zstd  # pragma: no cover
    else:
        from backports import zstd  # type: ignore[no-redef]

    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

# language detection
try:
    import py3langid

    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

# CChardet is faster and can be more accurate
try:
    from cchardet import detect as cchardet_detect
except ImportError:
    cchardet_detect = None  # type: ignore[assignment]

from charset_normalizer import from_bytes
from courlan import fix_relative_urls, get_base_url
from lxml.etree import _Element
from lxml.html import HtmlElement, HTMLParser, fromstring

# response types
from urllib3.response import HTTPResponse

if TYPE_CHECKING:  # pragma: no cover
    from .settings import Document, Extractor


class Response:
    "Store information gathered in a HTTP response object."

    __slots__ = ["data", "headers", "html", "status", "url"]

    def __init__(self, data: bytes, status: int, url: str) -> None:
        self.data = data
        self.headers: dict[str, str] | None = None
        self.html: str | None = None
        self.status = status
        self.url = url

    def __bool__(self) -> bool:
        return self.data is not None

    def __repr__(self) -> str:
        return self.html or decode_file(self.data)

    def store_headers(self, headerdict: Mapping[str, str]) -> None:
        "Store response headers with lowercase names."
        self.headers = {k.lower(): v for k, v in headerdict.items()}

    def decode_data(self, decode: bool, max_size: int | None = None) -> None:
        "Decode the bytestring in data and store a string in html."
        if decode and self.data:
            self.html = decode_file(self.data, max_size)

    def as_dict(self) -> dict[str, Any]:
        "Convert the response object to a dictionary."
        # heterogeneous value types (bytes, int, dict, str, None)
        return {attr: getattr(self, attr) for attr in self.__slots__}


# accepted input for HTML loading
HtmlInput: TypeAlias = HtmlElement | HTTPResponse | Response | bytes | str

LOGGER = logging.getLogger(__name__)

UNICODE_ALIASES = {"utf-8", "utf_8"}

DOCTYPE_TAG = re.compile("^< ?! ?DOCTYPE[^>]*/[^<>]*>", re.IGNORECASE)
FAULTY_HTML = re.compile(r"(<html.*?)\s*/>", re.IGNORECASE)
HTML_STRIP_TAGS = re.compile(r"(<!--.*?-->|<[^>]*>)")
# control characters
INVALID_XML_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ufffe\uffff]")

# note: htmldate could use HTML comments
# huge_tree=True, remove_blank_text=True
HTML_PARSER = HTMLParser(collect_ids=False, default_doctype=False, encoding="utf-8", remove_comments=True, remove_pis=True)

LINES_TRIMMING = re.compile(r"(?<![p{P}>])\n", flags=re.UNICODE | re.MULTILINE)

URL_BLACKLIST_REGEX = re.compile(r"^https?://|/+$")

# Regex to check image file extensions
IMAGE_EXTENSION = re.compile(r"[^\s]+\.(avif|bmp|gif|hei[cf]|jpe?g|png|webp)(\b|$)", re.IGNORECASE)

FORMATTING_PROTECTED = {"cell", "head", "hi", "item", "p", "quote", "ref", "td"}
SPACING_PROTECTED = {"code", "pre"}

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Language
TARGET_LANG_ATTRS = ('http-equiv="content-language"', 'property="og:locale"')
RE_HTML_LANG = re.compile(r"([a-z]{2})")

# Mostly filters for social media (text-level analog of the xpaths social/share tokens)
RE_FILTER = re.compile(
    r"\W*(Drucken|E-?Mail|Facebook|Flipboard|Google|Instagram|"
    "Linkedin|Mail|PDF|Pinterest|Pocket|Print|QQ|Reddit|Twitter|"
    "WeChat|WeiBo|Whatsapp|Xing|Mehr zum Thema:?|More on this.{,8}$)$",
    flags=re.IGNORECASE,
)
# link text > this fraction of total text = link farm (htmlprocessing.link_density_test)
LINK_FARM_RATIO = 0.9


def _capped(chunks: Iterable[bytes], max_size: int) -> bytes:
    "Accumulate decompressed chunks, rejecting payloads over max_size."
    out = bytearray()
    for chunk in chunks:
        out += chunk
        if len(out) > max_size:
            raise ValueError("decompressed content exceeds MAX_FILE_SIZE")
    return bytes(out)


# bgzip output needs ~320 members for 20MB
MAX_MEMBERS = 1000


def _bounded_members(raw: bytes, make_dec: Callable[[], Any], max_size: int) -> bytes:
    "Decompress a concatenated multi-member stream, rejecting output over max_size."
    out = bytearray()
    for _ in range(MAX_MEMBERS):
        dec = make_dec()
        # single capped call, no flush(): pending input must stay compressed or the cap is void
        out += dec.decompress(raw, max_size + 1 - len(out))
        # covers cap-truncated, oversized, and incomplete streams
        if len(out) > max_size or not dec.eof:
            raise ValueError("oversized or incomplete compressed stream")
        raw = dec.unused_data.lstrip(b"\0")  # NUL padding as gzip.decompress, copied each round
        if not raw:
            return bytes(out)
    raise ValueError("too many compressed members")


def _bounded_inflate(raw: bytes, max_size: int) -> bytes:
    "Decompress a single zlib/deflate stream, ignoring trailing bytes as zlib.decompress does."
    dec = zlib.decompressobj(zlib.MAX_WBITS)
    out = dec.decompress(raw, max_size + 1)
    if len(out) > max_size or not dec.eof:
        raise ValueError("oversized or incomplete compressed stream")
    return out


def _bounded_unbrotli(raw: bytes, max_size: int) -> bytes:
    "Decompress a brotli stream, output-capped at max_size."
    dec = brotli.Decompressor()
    out: bytes = dec.process(raw, output_buffer_limit=max_size + 1)
    # is_finished(): non-brotli input can yield b"" without raising
    if len(out) > max_size or not dec.is_finished():
        raise ValueError("oversized or incomplete compressed stream")
    return out


def handle_compressed_file(filecontent: bytes, max_size: int | None = None) -> bytes:
    """
    Don't trust response headers and try to decompress a binary string
    with a cascade of installed packages, capped at max_size (the configured
    MAX_FILE_SIZE by default) to guard against decompression bombs.
    Use magic numbers when available.
    """
    if not isinstance(filecontent, bytes):
        return filecontent

    if max_size is None:
        # deferred: circular import (settings imports utils)
        from .settings import DEFAULT_CONFIG  # noqa: PLC0415

        max_size = DEFAULT_CONFIG.getint("DEFAULT", "MAX_FILE_SIZE")

    # magic-numbered formats are terminal: failure means a corrupt file, not another format
    # source: https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
    if filecontent[:3] == b"\x1f\x8b\x08":
        try:
            return _bounded_members(filecontent, lambda: zlib.decompressobj(31), max_size)  # 31 = gzip header
        except (zlib.error, ValueError):
            LOGGER.warning("invalid or oversized GZ file")
    elif HAS_ZSTD and filecontent[:4] == b"\x28\xb5\x2f\xfd":
        try:
            return _bounded_members(filecontent, zstd.ZstdDecompressor, max_size)
        except (zstd.ZstdError, ValueError):
            LOGGER.warning("invalid or oversized ZSTD file")
    # no magic numbers: try brotli, then zlib/deflate speculatively
    else:
        if HAS_BROTLI:
            try:
                return _bounded_unbrotli(filecontent, max_size)
            except (brotli.error, ValueError):
                pass
        # single stream: multi-member concatenation is a gzip/zstd property, not a deflate one
        try:
            return _bounded_inflate(filecontent, max_size)
        except (zlib.error, ValueError):
            pass

    # return content unchanged if decompression failed
    return filecontent


def detect_encoding(bytesobject: bytes) -> list[str]:
    """ "Read all input or first chunk and return a list of encodings"""
    # alternatives: https://github.com/scrapy/w3lib/blob/master/w3lib/encoding.py
    # unicode-test
    try:
        bytesobject.decode("UTF-8")
        return ["utf-8"]
    except UnicodeDecodeError:
        pass
    guesses = []
    # additional module
    if cchardet_detect is not None:
        cchardet_guess = cchardet_detect(bytesobject)["encoding"]
        if cchardet_guess is not None:
            guesses.append(cchardet_guess.lower())
    # try charset_normalizer on first part, fallback on full document
    if len(bytesobject) < 10000:
        detection_results = from_bytes(bytesobject)
    else:
        detection_results = from_bytes(bytesobject[:5000] + bytesobject[-5000:]) or from_bytes(bytesobject)
    # return alternatives
    if len(detection_results) > 0:
        guesses.extend([r.encoding for r in detection_results])
    # it cannot be utf-8 (tested above)
    return [g for g in guesses if g not in UNICODE_ALIASES]


def decode_file(filecontent: bytes | str, max_size: int | None = None) -> str:
    """Decompress the bytestring if necessary, guess its encoding and
    decode to a Unicode string, resorting to destructive conversion otherwise."""
    if isinstance(filecontent, str):
        return filecontent

    filecontent = handle_compressed_file(filecontent, max_size)
    # fast path: valid UTF-8 (avoid decoding twice via detect_encoding)
    try:
        return filecontent.decode("utf-8")
    except UnicodeDecodeError:
        pass

    # encoding
    for guessed_encoding in detect_encoding(filecontent):
        try:
            return filecontent.decode(guessed_encoding)
        except (LookupError, UnicodeDecodeError):  # noqa: PERF203 -- VISCII: lookup
            LOGGER.warning("wrong encoding detected: %s", guessed_encoding)

    # destructive fallback if nothing else succeeded
    return str(filecontent, encoding="utf-8", errors="replace")


def is_dubious_html(beginning: str) -> bool:
    "Assess if the object is proper HTML (awith a corresponding tag or declaration)."
    return "html" not in beginning


def repair_faulty_html(htmlstring: str, beginning: str) -> str:
    "Repair faulty HTML strings to make then palatable for libxml2."
    htmlstring = INVALID_XML_CHARS.sub("", htmlstring)
    # libxml2/LXML issue: https://bugs.launchpad.net/lxml/+bug/1955915
    if "doctype" in beginning:
        firstline, _, rest = htmlstring.partition("\n")
        htmlstring = DOCTYPE_TAG.sub("", firstline, count=1) + "\n" + rest
    # other issue with malformed documents: check first three lines
    for i, line in enumerate(iter(htmlstring.splitlines())):
        if "<html" in line and line.endswith("/>"):
            htmlstring = FAULTY_HTML.sub(r"\1>", htmlstring, count=1)
            break
        if i > 2:
            break
    return htmlstring


def fromstring_bytes(htmlobject: str) -> HtmlElement | None:
    "Try to pass bytes to LXML parser."
    tree = None
    try:
        tree = fromstring(htmlobject.encode("utf8", "surrogatepass"), parser=HTML_PARSER)
    except Exception as err:
        LOGGER.error("lxml parser bytestring %s", err)
    return tree


def load_html(htmlobject: HtmlInput, max_size: int | None = None) -> HtmlElement | None:
    """Load object given as input and validate its type
    (accepted: lxml.html tree, trafilatura/urllib3 response, bytestring and string).

    Expects a full document: the dubious-HTML check below rejects a single-block
    fragment (e.g. "<p>x</p>" alone has one child and is treated as not-quite-HTML).
    Wrap bare fragments in an extra element (e.g. f"<div>{fragment}</div>") first.
    """
    # use tree directly
    if isinstance(htmlobject, HtmlElement):
        return htmlobject
    # use trafilatura or urllib3 responses directly
    if isinstance(htmlobject, HTTPResponse) or hasattr(htmlobject, "data"):
        htmlobject = htmlobject.data
    # do not accept any other type after this point
    if not isinstance(htmlobject, (bytes, str)):
        raise TypeError("incompatible input type", type(htmlobject))
    # start processing
    tree = None
    # try to guess encoding and decode file: if None then keep original
    htmlobject = decode_file(htmlobject, max_size)
    # sanity checks
    beginning = htmlobject[:50].lower()
    check_flag = is_dubious_html(beginning)
    # repair first
    htmlobject = repair_faulty_html(htmlobject, beginning)
    # first pass: use Unicode string
    fallback_parse = False
    try:
        tree = fromstring(htmlobject, parser=HTML_PARSER)
    except ValueError:
        # "Unicode strings with encoding declaration are not supported."
        tree = fromstring_bytes(htmlobject)
        fallback_parse = True
    except Exception as err:  # pragma: no cover
        LOGGER.error("lxml parsing failed: %s", err)
    # second pass: try passing bytes to LXML
    if (tree is None or len(tree) < 1) and not fallback_parse:
        tree = fromstring_bytes(htmlobject)
    # rejection test: is it (well-formed) HTML at all?
    # log parsing errors
    if tree is not None and check_flag is True and len(tree) < 2:
        LOGGER.error("parsed tree length: %s, wrong data type or not valid HTML", len(tree))
        tree = None
    return tree


def safe_base_url(url: str) -> str:
    "Get the base URL, empty string if malformed."
    try:
        return get_base_url(url)
    except ValueError:
        return ""


def safe_relative_url(baseurl: str, url: str) -> str:
    "Resolve a link against the base URL, empty string if malformed."
    try:
        return fix_relative_urls(baseurl, url)
    except ValueError:
        return ""


@lru_cache(maxsize=2**14)  # sys.maxunicode = 1114111
def return_printables_and_spaces(char: str) -> str:
    "Return a character if it belongs to certain classes"
    return char if char.isprintable() or char.isspace() else ""


def remove_control_characters(string: str) -> str:
    """Prevent non-printable and XML invalid character errors"""
    # in case most strings are already clean
    if string.isprintable():
        return string
    return "".join(map(return_printables_and_spaces, string))


def normalize_unicode(string: str, unicodeform: Literal["NFC", "NFD", "NFKC", "NFKD"] = "NFC") -> str:
    "Normalize the given string to the specified unicode format."
    return normalize(unicodeform, string)


@lru_cache(maxsize=1024)
def line_processing(line: str, preserve_space: bool = False, trailing_space: bool = False) -> str | None:
    """Remove HTML space entities, then discard incompatible unicode
    and invalid XML characters on line level"""
    # spacing HTML entities: https://www.w3.org/MarkUp/html-spec/html-spec_13.html
    # unique code spaces
    new_line = remove_control_characters(line.replace("&#13;", "\r").replace("&#10;", "\n").replace("&nbsp;", "\u00a0"))
    if not preserve_space:
        # remove newlines that are not related to punctuation or markup
        # remove non-printable chars and normalize space characters (including Unicode spaces)
        new_line = trim(LINES_TRIMMING.sub(r" ", new_line))
        # prune empty lines
        if all(map(str.isspace, new_line)):
            new_line = None  # type: ignore[assignment]
        elif trailing_space:
            space_before = " " if line[0].isspace() else ""
            space_after = " " if line[-1].isspace() else ""
            new_line = f"{space_before}{new_line}{space_after}"
    return new_line


def sanitize(text: str, preserve_space: bool = False, trailing_space: bool = False) -> str | None:
    """Convert text and discard incompatible and invalid characters"""
    # consider all text as a single line
    if trailing_space:
        return line_processing(text, preserve_space, True)
    # process line by line
    try:
        return "\n".join(filter(None, (line_processing(line, preserve_space) for line in text.splitlines()))).replace(
            "\u2424",
            "",
        )
    except AttributeError:
        return None


def sanitize_tree(tree: _Element) -> _Element:
    """Trims spaces, removes control characters and normalizes unicode"""
    for elem in tree.iter():
        parent = elem.getparent()
        parent_tag = parent.tag if parent is not None else ""

        # preserve space if the element or its parent is a specific tag, or if the element has text and children
        # the last part is relevant for item elements with ref inside for example
        preserve_space = elem.tag in SPACING_PROTECTED or parent_tag in SPACING_PROTECTED
        trailing_space = elem.tag in FORMATTING_PROTECTED or parent_tag in FORMATTING_PROTECTED or preserve_space

        # remove invalid attributes (copy: pop() during iteration)
        for attribute in list(elem.attrib):
            if ":" in attribute:  # colon is reserved for namespaces in XML
                if not elem.attrib[attribute] or attribute.split(":", 1)[0] not in tree.nsmap:
                    elem.attrib.pop(attribute)

        if elem.text:
            elem.text = sanitize(elem.text, preserve_space, trailing_space)
        if elem.tail:
            elem.tail = sanitize(elem.tail, preserve_space, trailing_space)
    return tree


@lru_cache(maxsize=1024)
def trim(string: str) -> str:
    "Remove unnecessary spaces within a text string."
    try:
        # remove newlines that are not related to punctuation or markup + proper trimming
        return " ".join(string.split()).strip()
    except (AttributeError, TypeError):
        return ""


def as_list(value: Any) -> list[Any]:
    "Normalize a JSON-like value that may be a single object, a list of them, or None."
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def image_src(element: _Element) -> str | None:
    "Image source of an element: src, data-src, or the first data-src* attribute pointing to an image file."
    for attr in ("data-src", "src"):
        src = element.get(attr, "")
        if is_image_file(src):
            return src
    return next((v for a, v in element.attrib.items() if a.startswith("data-src") and is_image_file(v)), None)


def is_image_file(imagesrc: str | None) -> bool:
    """Check if the observed string corresponds to a valid image extension.
    Use a length threshold and apply a regex on the content."""
    if imagesrc is None or len(imagesrc) > 8192:
        return False
    return bool(IMAGE_EXTENSION.search(imagesrc))


def make_chunks(iterable: Iterable[str], n: int) -> Iterator[tuple[str, ...]]:
    "Chunk data into smaller pieces."
    # 3.12+: https://docs.python.org/3/library/itertools.html#itertools.batched
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def is_acceptable_length(my_len: int, options: "Extractor") -> bool:
    "Check if the document length is within acceptable boundaries."
    if my_len < options.min_file_size:
        LOGGER.error("too small/incorrect for URL %s", options.url)
        return False
    if my_len > options.max_file_size:
        LOGGER.error("too large: length %s for URL %s", my_len, options.url)
        return False
    return True


def check_html_lang(tree: HtmlElement, target_language: str, strict: bool = False) -> bool:
    """Check HTML meta-elements for language information and split
    the result in case there are several languages."""
    for attr in TARGET_LANG_ATTRS:
        elems = tree.findall(f".//meta[@{attr}][@content]")
        if elems:
            if any(target_language in RE_HTML_LANG.split(elem.get("content", "").lower()) for elem in elems):
                return True
            LOGGER.debug("%s lang attr failed", attr)
            return False

    # HTML lang attribute: sometimes a wrong indication
    if strict:
        elems = tree.xpath("//html[@lang]")
        if elems:
            if any(target_language in RE_HTML_LANG.split(elem.get("lang", "").lower()) for elem in elems):
                return True
            LOGGER.debug("HTML lang failed")
            return False

    LOGGER.debug("No relevant lang elements found")
    return True


def language_classifier(temp_text: str, temp_comments: str) -> str | None:
    """Run external component (if installed) for language identification"""
    if LANGID_FLAG is True:
        result, _ = py3langid.classify(temp_text) if len(temp_text) > len(temp_comments) else py3langid.classify(temp_comments)
        return cast("str", result)
    LOGGER.warning("Language detector not installed, skipping detection")  # pragma: no cover
    return None  # pragma: no cover


def language_filter(temp_text: str, temp_comments: str, target_language: str, docmeta: "Document") -> tuple[bool, "Document"]:
    """Filter text based on language detection and store relevant information"""
    # todo: run and pass info along anyway?
    if target_language is not None:
        # more thorough: detection on actual text content
        docmeta.language = language_classifier(temp_text, temp_comments)
        # HTML lang check? sometimes contradicted by detection above
        if docmeta.language is not None and docmeta.language != target_language:
            LOGGER.warning("wrong language: %s %s", docmeta.language, docmeta.url)
            return True, docmeta
    return False, docmeta


def textfilter(element: _Element) -> bool:
    """Filter out unwanted text"""
    testtext = element.tail if element.text is None else element.text
    # to check: line len → continue if len(line) <= 5
    return not testtext or testtext.isspace() or any(map(RE_FILTER.match, testtext.splitlines()))


def text_chars_test(string: str | None) -> bool:
    """Determine if a string is only composed of spaces and/or control characters"""
    return bool(string and not string.isspace())
