# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML and text processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

# import csv
import logging
import re

from gzip import decompress
from functools import lru_cache
from html import unescape
from unicodedata import normalize

# CChardet is faster and can be more accurate
try:
    from cchardet import detect as cchardet_detect
except ImportError:
    cchardet_detect = None
from charset_normalizer import from_bytes

from lxml.html import HtmlElement, HTMLParser, fromstring
# from lxml.html.soupparser import fromstring as fromsoup

# response types
from urllib3.response import HTTPResponse


LOGGER = logging.getLogger(__name__)

UNICODE_ALIASES = {'utf-8', 'utf_8'}

# note: htmldate could use HTML comments
# huge_tree=True, remove_blank_text=True
HTML_PARSER = HTMLParser(collect_ids=False, default_doctype=False, encoding='utf-8', remove_comments=True, remove_pis=True)

LINES_TRIMMING = re.compile(r'(?<![p{P}>])\n', flags=re.UNICODE|re.MULTILINE)

# Regex to check image file extensions
IMAGE_EXTENSION = re.compile(r'[^\s]+\.(avif|bmp|gif|hei[cf]|jpe?g|png|webp)(\b|$)')

AUTHOR_PREFIX = re.compile(r'^([a-zäöüß]+(ed|t))? ?(written by|words by|words|by|von|from) ', flags=re.IGNORECASE)
AUTHOR_REMOVE_NUMBERS = re.compile(r'\d.+?$')
AUTHOR_TWITTER = re.compile(r'@[\w]+')
AUTHOR_REPLACE_JOIN = re.compile(r'[._+]')
AUTHOR_REMOVE_NICKNAME = re.compile(r'["‘({\[’\'][^"]+?[‘’"\')\]}]')
AUTHOR_REMOVE_SPECIAL = re.compile(r'[^\w]+$|[:()?*$#!%/<>{}~]')
AUTHOR_REMOVE_PREPOSITION = re.compile(r'\b\s+(am|on|for|at|in|to|from|of|via|with|—|-)\s+(.*)', flags=re.IGNORECASE)
AUTHOR_EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
AUTHOR_SPLIT = re.compile(r'/|;|,|\||&|(?:^|\W)[u|a]nd(?:$|\W)', flags=re.IGNORECASE)
AUTHOR_EMOJI_REMOVE = re.compile(
    "["u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF"
    u"\U00002500-\U00002BEF" u"\U00002702-\U000027B0" u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937" u"\U00010000-\U0010ffff" u"\u2640-\u2642" u"\u2600-\u2B55" u"\u200d"
    u"\u23cf" u"\u23e9" u"\u231a" u"\ufe0f" u"\u3030" "]+", flags=re.UNICODE)

CLEAN_META_TAGS = re.compile(r'["\']')


def handle_gz_file(filecontent):
    """Tell if a file's magic number corresponds to the GZip format
       and try to decode it"""
    # source: https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
    if isinstance(filecontent, bytes) and filecontent[:2] == b'\x1f\x8b':
        # decode GZipped data
        try:
            filecontent = decompress(filecontent)
        except (EOFError, OSError):
            logging.warning('invalid GZ file')
    return filecontent


def isutf8(data):
    """Simple heuristic to determine if a bytestring uses standard unicode encoding"""
    try:
        data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    else:
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
    detection_results = from_bytes(bytesobject[:15000]) or from_bytes(bytesobject)
    # return alternatives
    if len(detection_results) > 0:
        guesses.extend([r.encoding for r in detection_results])
    # it cannot be utf-8 (tested above)
    return [g for g in guesses if g not in UNICODE_ALIASES]


def decode_response(response):
    """Read the urllib3 object corresponding to the server response,
       check if it could be GZip and eventually decompress it, then
       try to guess its encoding and decode it to return a unicode string"""
    # urllib3 response object / bytes switch
    resp_content = response if isinstance(response, bytes) else response.data
    return decode_file(resp_content)


def decode_file(filecontent):
    """Guess bytestring encoding and try to decode to Unicode string.
       Resort to destructive conversion otherwise."""
    # init
    if isinstance(filecontent, str):
        return filecontent
    htmltext = None
    # GZip test
    filecontent = handle_gz_file(filecontent)
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


def is_dubious_html(htmlobject):
    "Assess if the object is proper HTML (with a corresponding declaration)."
    if isinstance(htmlobject, bytes):
        if 'html' not in htmlobject[:50].decode(encoding='ascii', errors='ignore').lower():
            return True
    elif isinstance(htmlobject, str):
        if 'html' not in htmlobject[:50].lower():
            return True
    return False


def load_html(htmlobject):
    """Load object given as input and validate its type
    (accepted: lxml.html tree, trafilatura/urllib3 response, bytestring and string)
    """
    # use tree directly
    if isinstance(htmlobject, HtmlElement):
        return htmlobject
    # use trafilatura or urllib3 responses directly
    if isinstance(htmlobject, HTTPResponse) or hasattr(htmlobject, 'data'):
        htmlobject = htmlobject.data
    # do not accept any other type after this point
    if not isinstance(htmlobject, (bytes, str)):
        raise TypeError('incompatible input type', type(htmlobject))
    # start processing
    tree = None
    # try to guess encoding and decode file: if None then keep original
    htmlobject = decode_file(htmlobject)
    # sanity check
    check_flag = is_dubious_html(htmlobject)
    # use Unicode string
    try:
        tree = fromstring(htmlobject, parser=HTML_PARSER)
    except ValueError:
        # "Unicode strings with encoding declaration are not supported."
        try:
            tree = fromstring(htmlobject.encode('utf8'), parser=HTML_PARSER)
        except Exception as err:
            LOGGER.error('lxml parser bytestring %s', err)
    except Exception as err:
        LOGGER.error('lxml parsing failed: %s', err)
    # more robust option: try BeautifulSoup
    #if tree is None or not isinstance(tree, HtmlElement):
    #    if isinstance(htmlobject, (bytes, str)):
    #        try:
    #            tree = fromsoup(htmlobject)
    #        except Exception as err:
    #            LOGGER.error('BS parser error: %s', err)
    # rejection test: is it (well-formed) HTML at all?
    if tree is not None and check_flag is True and len(tree) < 2:
        LOGGER.error('parsed tree length: %s, wrong data type or not valid HTML', len(tree))
        tree = None
    return tree


def txttocsv(text, comments, docmeta):
    '''Output the result in CSV format (tab-separated values)'''
    # outputwriter = csv.writer(sys.stdout, delimiter='\t', quoting=csv.QUOTE_NONE)
    # outputwriter.writerow()
    # with newlines: '\\n'.join()
    text = trim(' '.join(text.splitlines()))
    if comments is not None:
        comments = trim(' '.join(comments.splitlines()))
    tsv_output = \
        f'{docmeta.url}\t{docmeta.fingerprint}\t{docmeta.hostname}\t{docmeta.title}\t{docmeta.date}\t{text}\t{comments}\t{docmeta.license}\n'
    # add id up front if provided
    if docmeta.id is not None:
        tsv_output = docmeta.id + '\t' + tsv_output
    return tsv_output


def remove_control_characters(string):
    '''Prevent non-printable and XML invalid character errors'''
    return ''.join([c for c in string if c.isprintable() or c.isspace()])


def normalize_unicode(string, unicodeform='NFC'):
    'Normalize the given string to the specified unicode format.'
    return normalize(unicodeform, string)


@lru_cache(maxsize=1024)
def line_processing(line):
    '''Remove HTML space entities, then discard incompatible unicode
       and invalid XML characters on line level'''
    # spacing HTML entities: https://www.w3.org/MarkUp/html-spec/html-spec_13.html
    line = line.replace('&#13;', '\r').replace('&#10;', '\n').replace('&nbsp;', '\u00A0')
    # remove newlines that are not related to punctuation or markup
    # remove non-printable chars and normalize space characters (including Unicode spaces)
    line = trim(remove_control_characters(LINES_TRIMMING.sub(r' ', line)))
    # prune empty lines
    if all(map(str.isspace, line)):
        line = None
    return line


def sanitize(text):
    '''Convert text and discard incompatible and invalid characters'''
    try:
        return '\n'.join(filter(None, (line_processing(l) for l in text.splitlines())))
    except AttributeError:
        return None


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
    # examine names
    for author in AUTHOR_SPLIT.split(author_string):
        author = trim(author)
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


# todo: document and check this function
def check_authors(authors, author_blacklist):
    new_authors = [
        author
        for author in authors.split('; ')
        if author.lower() not in [a.lower() for a in author_blacklist]
    ]
    if new_authors:
        return '; '.join(new_authors).strip('; ')
    return None


def uniquify_list(l):
    """
    Remove duplicates from a list while keeping order in an efficient way.
    Dictionaries preserve insertion order since Python 3.6.

    https://www.peterbe.com/plog/fastest-way-to-uniquify-a-list-in-python-3.6
    """
    return list(dict.fromkeys(l))
