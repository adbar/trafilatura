# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML and text processing.
"""

import logging
import re
import warnings

# if brotli is installed
try:
    import brotli
except ImportError:
    brotli = None

from difflib import SequenceMatcher
from functools import lru_cache
from gzip import decompress
from html import unescape
from itertools import islice
from unicodedata import normalize

# CChardet is faster and can be more accurate
try:
    from cchardet import detect as cchardet_detect
except ImportError:
    cchardet_detect = None
from charset_normalizer import from_bytes
from lxml.html import HtmlElement, HTMLParser, fromstring
# response types
from urllib3.response import HTTPResponse


LOGGER = logging.getLogger(__name__)

UNICODE_ALIASES = {'utf-8', 'utf_8'}

DOCTYPE_TAG = re.compile("^< ?! ?DOCTYPE.+?/ ?>", re.I)
FAULTY_HTML = re.compile(r"(<html.*?)\s*/>", re.I)

# note: htmldate could use HTML comments
# huge_tree=True, remove_blank_text=True
HTML_PARSER = HTMLParser(collect_ids=False, default_doctype=False, encoding='utf-8', remove_comments=True, remove_pis=True)

LINES_TRIMMING = re.compile(r'(?<![p{P}>])\n', flags=re.UNICODE|re.MULTILINE)

URL_BLACKLIST_REGEX = re.compile(r'^https?://|/+$')

# Regex to check image file extensions
IMAGE_EXTENSION = re.compile(r'[^\s]+\.(avif|bmp|gif|hei[cf]|jpe?g|png|webp)(\b|$)')

AUTHOR_PREFIX = re.compile(r'^([a-zäöüß]+(ed|t))? ?(written by|words by|words|by|von|from) ', flags=re.IGNORECASE)
AUTHOR_REMOVE_NUMBERS = re.compile(r'\d.+?$')
AUTHOR_TWITTER = re.compile(r'@[\w]+')
AUTHOR_REPLACE_JOIN = re.compile(r'[._+]')
AUTHOR_REMOVE_NICKNAME = re.compile(r'["‘({\[’\'][^"]+?[‘’"\')\]}]')
AUTHOR_REMOVE_SPECIAL = re.compile(r'[^\w]+$|[:()?*$#!%/<>{}~¿]')
AUTHOR_REMOVE_PREPOSITION = re.compile(r'\b\s+(am|on|for|at|in|to|from|of|via|with|—|-|–)\s+(.*)', flags=re.IGNORECASE)
AUTHOR_EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
AUTHOR_SPLIT = re.compile(r'/|;|,|\||&|(?:^|\W)[u|a]nd(?:$|\W)', flags=re.IGNORECASE)
AUTHOR_EMOJI_REMOVE = re.compile(
    "["
    u"\U00002700-\U000027BF"  # Dingbats
    u"\U0001F600-\U0001F64F"  # Emoticons
    u"\U00002600-\U000026FF"  # Miscellaneous Symbols
    u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
    u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
    "]+", flags=re.UNICODE)
AUTHOR_REMOVE_HTML = re.compile(r'<[^>]+>')
CLEAN_META_TAGS = re.compile(r'["\']')

STRIP_EXTENSION = re.compile(r"\.[^/?#]{2,63}$")

FORMATTING_PROTECTED = {'cell', 'head', 'hi', 'item', 'p', 'quote', 'ref', 'td'}
SPACING_PROTECTED = {'code', 'pre'}


def handle_compressed_file(filecontent):
    """Tell if a file's magic number corresponds to the GZip format
       and try to decode it. Alternatively, try Brotli if the package
       is installed."""
    if isinstance(filecontent, bytes):
        # source: https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
        if filecontent[:2] == b'\x1f\x8b':
            # decode GZipped data
            try:
                filecontent = decompress(filecontent)
            except (EOFError, OSError):
                logging.warning('invalid GZ file')
        # try brotli
        elif brotli is not None:
            try:
                filecontent = brotli.decompress(filecontent)
            except brotli.error:
                pass  # logging.debug('invalid Brotli file')
    return filecontent


def isutf8(data):
    """Simple heuristic to determine if a bytestring uses standard unicode encoding"""
    try:
        data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    return True


def detect_encoding(bytesobject):
    """"Read all input or first chunk and return a list of encodings"""
    # alternatives: https://github.com/scrapy/w3lib/blob/master/w3lib/encoding.py
    # unicode-test
    if isutf8(bytesobject):
        return ['utf-8']
    guesses = []
    # additional module
    if cchardet_detect is not None:
        cchardet_guess = cchardet_detect(bytesobject)['encoding']
        if cchardet_guess is not None:
            guesses.append(cchardet_guess.lower())
    # try charset_normalizer on first part, fallback on full document
    if len(bytesobject) < 10000:
        detection_results = from_bytes(bytesobject)
    else:
        detection_results = from_bytes(bytesobject[:5000] + bytesobject[-5000:]) or \
                            from_bytes(bytesobject)
    # return alternatives
    if len(detection_results) > 0:
        guesses.extend([r.encoding for r in detection_results])
    # it cannot be utf-8 (tested above)
    return [g for g in guesses if g not in UNICODE_ALIASES]


def decode_response(content):
    """Read the urllib3 object corresponding to the server response,
       try to guess its encoding and decode it to return a unicode string"""
    warnings.warn(
        "decode_response() will be deprecated, use decode_file() on the content.",
         PendingDeprecationWarning
    )
    return decode_file(content)


def decode_file(filecontent):
    """Check if the bytestring could be GZip and eventually decompress it,
       guess bytestring encoding and try to decode to Unicode string.
       Resort to destructive conversion otherwise."""
    # init
    if isinstance(filecontent, str):
        return filecontent
    htmltext = None
    # GZip and Brotli test
    filecontent = handle_compressed_file(filecontent)
    # encoding
    for guessed_encoding in detect_encoding(filecontent):
        try:
            htmltext = filecontent.decode(guessed_encoding)
        except (LookupError, UnicodeDecodeError): # VISCII: lookup
            LOGGER.warning('wrong encoding detected: %s', guessed_encoding)
            htmltext = None
        else:
            break
    # return original content if nothing else succeeded
    return htmltext or str(filecontent, encoding='utf-8', errors='replace')


def is_dubious_html(beginning: str) -> bool:
    "Assess if the object is proper HTML (awith a corresponding tag or declaration)."
    return "html" not in beginning


def repair_faulty_html(htmlstring: str, beginning: str) -> str:
    "Repair faulty HTML strings to make then palatable for libxml2."
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


def fromstring_bytes(htmlobject):
    "Try to pass bytes to LXML parser."
    tree = None
    try:
        tree = fromstring(htmlobject.encode("utf8", "surrogatepass"), parser=HTML_PARSER)
    except Exception as err:
        LOGGER.error("lxml parser bytestring %s", err)
    return tree


def load_html(htmlobject):
    """Load object given as input and validate its type
    (accepted: lxml.html tree, trafilatura/urllib3 response, bytestring and string)
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
    htmlobject = decode_file(htmlobject)
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
        LOGGER.error(
            "parsed tree length: %s, wrong data type or not valid HTML", len(tree)
        )
        tree = None
    return tree


@lru_cache(maxsize=2**14)  # sys.maxunicode = 1114111
def return_printables_and_spaces(char):
    'Return a character if it belongs to certain classes'
    return char if char.isprintable() or char.isspace() else ''


def remove_control_characters(string):
    '''Prevent non-printable and XML invalid character errors'''
    return ''.join(map(return_printables_and_spaces, string))


def normalize_unicode(string, unicodeform='NFC'):
    'Normalize the given string to the specified unicode format.'
    return normalize(unicodeform, string)


@lru_cache(maxsize=1024)
def line_processing(line, preserve_space=False, trailing_space=False):
    '''Remove HTML space entities, then discard incompatible unicode
       and invalid XML characters on line level'''
    # spacing HTML entities: https://www.w3.org/MarkUp/html-spec/html-spec_13.html
    # unique code spaces
    new_line = remove_control_characters(line.replace('&#13;', '\r').replace('&#10;', '\n').replace('&nbsp;', '\u00A0'))
    if not preserve_space:
        # remove newlines that are not related to punctuation or markup
        # remove non-printable chars and normalize space characters (including Unicode spaces)
        new_line = trim(LINES_TRIMMING.sub(r" ", new_line))
        # prune empty lines
        if all(map(str.isspace, new_line)):
            new_line = None
        elif trailing_space:
            space_before = " " if line[0].isspace() else ""
            space_after = " " if line[-1].isspace() else ""
            new_line = "".join([space_before, new_line, space_after])
    return new_line


def sanitize(text, preserve_space=False, trailing_space=False):
    '''Convert text and discard incompatible and invalid characters'''
    # consider all text as a single line
    if trailing_space:
        return line_processing(text, preserve_space, True)
    # process line by line
    try:
        return '\n'.join(filter(None, (line_processing(l, preserve_space) for l in text.splitlines()))).replace('\u2424', '')
    except AttributeError:
        return None


def sanitize_tree(tree):
    '''Trims spaces, removes control characters and normalizes unicode'''
    for elem in tree.iter():
        parent = elem.getparent()
        parent_tag = parent.tag if parent is not None else ""

        # preserve space if the element or its parent is a specific tag, or if the element has text and children
        # the last part is relevant for item elements with ref inside for example
        preserve_space = elem.tag in SPACING_PROTECTED or parent_tag in SPACING_PROTECTED
        trailing_space = elem.tag in FORMATTING_PROTECTED or parent_tag in FORMATTING_PROTECTED or preserve_space

        # remove invalid attributes
        for attribute in elem.attrib:
            if ':' in attribute:  # colon is reserved for namespaces in XML
                if not elem.attrib[attribute] or attribute.split(':', 1)[0] not in tree.nsmap:
                    elem.attrib.pop(attribute)

        if elem.text:
            elem.text = sanitize(elem.text, preserve_space, trailing_space)
        if elem.tail:
            elem.tail = sanitize(elem.tail, preserve_space, trailing_space)
    return tree


@lru_cache(maxsize=1024)
def trim(string):
    '''Remove unnecessary spaces within a text string'''
    try:
        # remove newlines that are not related to punctuation or markup + proper trimming
        # return LINES_TRIMMING.sub(r' ', string).strip(' \t\n\r\v')
        # faster:
        return ' '.join(string.split()).strip()
    except (AttributeError, TypeError):
        return None


def normalize_tags(tags):
    '''Remove special characters of tags'''
    tags = CLEAN_META_TAGS.sub(r'', trim(unescape(tags)))
    return ", ".join(filter(None, tags.split(", ")))


def is_image_file(imagesrc):
    '''Check if the observed string corresponds to a valid image extension,
       return False otherwise'''
    return bool(imagesrc is not None and IMAGE_EXTENSION.search(imagesrc))


def normalize_authors(current_authors, author_string):
    '''Normalize author info to focus on author names only'''
    new_authors = []
    if author_string.lower().startswith('http') or AUTHOR_EMAIL.match(author_string):
        return current_authors
    if current_authors is not None:
        new_authors = current_authors.split('; ')
    # fix to code with unicode
    if '\\u' in author_string:
        author_string = author_string.encode().decode('unicode_escape')
    # fix html entities
    if '&#' in author_string or '&amp;' in author_string:
        author_string = unescape(author_string)
    # remove html tags
    author_string = AUTHOR_REMOVE_HTML.sub('', author_string)
    # examine names
    for author in AUTHOR_SPLIT.split(author_string):
        author = trim(author)
        # remove emoji
        author = AUTHOR_EMOJI_REMOVE.sub('', author)
        # remove @username
        author = AUTHOR_TWITTER.sub('', author)
        # replace special characters with space
        author = trim(AUTHOR_REPLACE_JOIN.sub(' ', author))
        author = AUTHOR_REMOVE_NICKNAME.sub('', author)
        # remove special characters
        author = AUTHOR_REMOVE_SPECIAL.sub('', author)
        author = AUTHOR_PREFIX.sub('', author)
        author = AUTHOR_REMOVE_NUMBERS.sub('', author)
        author = AUTHOR_REMOVE_PREPOSITION.sub('', author)
        # skip empty or improbably long strings
        if len(author) == 0 or (
            # simple heuristics, regex or vowel tests also possible
            ' ' not in author and '-' not in author and len(author) >= 50
            ):
            continue
        # title case
        if not author[0].isupper() or sum(1 for c in author if c.isupper()) < 1:
            author = author.title()
        # safety checks
        if author not in new_authors and (len(new_authors) == 0 or all(new_author not in author for new_author in new_authors)):
            new_authors.append(author)
    if len(new_authors) == 0:
        return current_authors
    return '; '.join(new_authors).strip('; ')


@lru_cache(maxsize=1024)
def is_similar_domain(reference, new_string, threshold=0.5):
    "Return the similarity ratio between two short strings, here domain names."
    if new_string != reference:
        new_string = STRIP_EXTENSION.sub("", new_string)
        reference = STRIP_EXTENSION.sub("", reference)
        if SequenceMatcher(None, reference, new_string).ratio() < threshold:
            return False
    return True


def make_chunks(iterable, n):
    """
    Chunk data into smaller pieces.
    https://docs.python.org/3/library/itertools.html
    """
    it = iter(iterable)
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        yield chunk
    # Python 3.8+ with walrus operator
    # while batch := tuple(islice(it, n)):
    #    yield batch
