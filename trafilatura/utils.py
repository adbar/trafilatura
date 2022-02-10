# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML and text processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

# import csv
import gzip
import logging
import re
import sys

from functools import lru_cache
from html import unescape
from unicodedata import normalize

# CChardet is faster and can be more accurate
try:
    import cchardet
except ImportError:
    cchardet = None


from charset_normalizer import detect

from lxml import etree, html
# from lxml.html.soupparser import fromstring as fromsoup

# response types
from urllib3.response import HTTPResponse


LOGGER = logging.getLogger(__name__)

# collect_ids=False, default_doctype=False, huge_tree=True, remove_blank_text=True
HTML_PARSER = html.HTMLParser(remove_comments=True, remove_pis=True, encoding='utf-8')
RECOVERY_PARSER = html.HTMLParser(remove_comments=True, remove_pis=True)

UNICODE_WHITESPACE = re.compile(
    r'''
    \u00A0|\u1680|\u2000|\u2001|\u2002|\u2003|\u2004|\u2005|\u2006|\u2007|
    \u2008|\u2009|\u200a|\u2028|\u2029|\u202F|\u205F|\u3000
    '''
)

NO_TAG_SPACE = re.compile(r'(?<![p{P}>])\n')
SPACE_TRIMMING = re.compile(r'\s+', flags=re.UNICODE|re.MULTILINE)

NOPRINT_TRANS_TABLE = {
    i: None
    for i in range(sys.maxunicode + 1)
    if not chr(i).isprintable() and not chr(i).isspace()
}


# Regex to check image file extensions
IMAGE_EXTENSION = re.compile(r'[^\s]+\.(jpe?g|png|gif|bmp)(\b|$)')

AUTHOR_PREFIX = re.compile(r'^([a-zäöüß]+(ed|t))? ?(written by|words by|words|by|von) ', flags=re.IGNORECASE)
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


def handle_gz_file(filecontent):
    """Tell if a file's magic number corresponds to the GZip format
       and try to decode it"""
    # source: https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
    if isinstance(filecontent, bytes) and filecontent[:2] == b'\x1f\x8b':
        # decode GZipped data
        try:
            filecontent = gzip.decompress(filecontent)
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
    """Read the first chunk of input and return its encoding"""
    # alternatives: https://github.com/scrapy/w3lib/blob/master/w3lib/encoding.py
    # unicode-test
    if isutf8(bytesobject):
        return 'UTF-8'
    # try one of the installed detectors on first part
    if cchardet is not None:
        guess = cchardet.detect(bytesobject[:5000])
    else:
        guess = detect(bytesobject[:5000])
    LOGGER.debug('guessed encoding: %s, confidence: %s', guess['encoding'], guess['confidence'])
    # fallback on full response
    if guess is None or (guess['confidence'] is not None and guess['confidence'] < 0.98):
        guess = detect(bytesobject)
        LOGGER.debug('second-guessed encoding: %s, confidence: %s', guess['encoding'], guess['confidence'])
    return guess['encoding']


def decode_response(response):
    """Read the urllib3 object corresponding to the server response,
       check if it could be GZip and eventually decompress it, then
       try to guess its encoding and decode it to return a unicode string"""
    # urllib3 response object / bytes switch
    if isinstance(response, bytes):
        resp_content = response
    else:
        resp_content = response.data
    # suggested:
    # resp_content = response if isinstance(response, bytes) else response.data
    # decode GZipped data if necessary
    resp_content = handle_gz_file(resp_content)
    # detect encoding
    guessed_encoding = detect_encoding(resp_content)
    LOGGER.debug('response encoding: %s', guessed_encoding)
    # process
    htmltext = None
    if guessed_encoding is not None:
        try:
            htmltext = resp_content.decode(guessed_encoding)
        except (LookupError, UnicodeDecodeError): # VISCII: lookup
            LOGGER.warning('wrong encoding detected: %s', guessed_encoding)
    else:
        LOGGER.error('no encoding detected: %s', guessed_encoding)
    # force decoding # ascii instead?
    if htmltext is None:
        htmltext = str(resp_content, encoding='utf-8', errors='replace')
    return htmltext



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
    (accepted: LXML tree, bytestring and string)
    """
    # use tree directly
    if isinstance(htmlobject, (etree._ElementTree, html.HtmlElement)):
        return htmlobject
    tree = None
    # use trafilatura or urllib3 responses directly
    try:
        if isinstance(htmlobject, HTTPResponse) or htmlobject.data:
            htmlobject = decode_response(htmlobject.data)
    except AttributeError:
        pass
    # GZip test
    htmlobject = handle_gz_file(htmlobject)
    # sanity check
    check_flag = is_dubious_html(htmlobject)
    # try to detect encoding and convert to string
    if isinstance(htmlobject, bytes):
        guessed_encoding = detect_encoding(htmlobject)
        if guessed_encoding is None:
            tree = html.fromstring(htmlobject, parser=RECOVERY_PARSER)
        elif guessed_encoding == 'UTF-8':
            tree = html.fromstring(htmlobject, parser=HTML_PARSER)
        else:
            try:
                htmlobject = htmlobject.decode(guessed_encoding)
                tree = html.fromstring(htmlobject, parser=HTML_PARSER)
            except (LookupError, UnicodeDecodeError):  # VISCII encoding
                LOGGER.warning('encoding issue: %s', guessed_encoding)
                tree = html.fromstring(htmlobject, parser=RECOVERY_PARSER)
    # use string if applicable
    elif isinstance(htmlobject, str):
        try:
            tree = html.fromstring(htmlobject, parser=HTML_PARSER)
        except ValueError:
            # try to parse a bytestring
            try:
                tree = html.fromstring(htmlobject.encode('utf8'), parser=HTML_PARSER)
            except Exception as err:
                LOGGER.error('parser bytestring %s', err)
        except Exception as err:
            LOGGER.error('parsing failed: %s', err)
    # default to None
    else:
        LOGGER.error('this type cannot be processed: %s', type(htmlobject))
    # rejection test: is it (well-formed) HTML at all?
    if tree is not None and check_flag is True and len(tree) < 2:
        LOGGER.error('parsed tree length: %s, wrong data type or not valid HTML', len(tree))
        tree = None
    #if tree is None:
    #    if isinstance(htmlobject, bytes) or isinstance(htmlobject, str):
    #        # more robust parsing
    #        tree = fromsoup(htmlobject)
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
        '{url}\t{fingerprint}\t{hostname}\t{doctitle}\t{docdate}\t{text}\t{comments}\t{textlicense}\n' \
        .format(
        url=docmeta['url'],
        fingerprint=docmeta['fingerprint'],
        hostname=docmeta['hostname'],
        doctitle=docmeta['title'],
        docdate=docmeta['date'],
        text=text,
        comments=comments,
        textlicense=docmeta['license']
        )
    # add id up front if provided
    if docmeta['id'] is not None:
        tsv_output = docmeta['id'] + '\t' + tsv_output
    return tsv_output


@lru_cache(maxsize=128)
def remove_control_characters(string):
    '''Prevent non-printable and XML invalid character errors'''
    # https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python/93029#93029
    return string.translate(NOPRINT_TRANS_TABLE)


def normalize_unicode(string, unicodeform='NFC'):
    'Normalize the given string to the specified unicode format.'
    return normalize(unicodeform, string)


@lru_cache(maxsize=128)
def line_processing(line):
    '''Remove HTML space entities, then discard incompatible unicode
       and invalid XML characters on line level'''
    # spacing HTML entities: https://www.w3.org/MarkUp/html-spec/html-spec_13.html
    line = line.replace('&#13;', '\r').replace('&#10;', '\n').replace('&nbsp;', '\u00A0')
    # remove non-printable chars and normalize space characters
    line = trim(remove_control_characters(UNICODE_WHITESPACE.sub(' ', line)))
    # prune empty lines
    if re.match(r'\s*$', line):
        line = None
    return line


@lru_cache(maxsize=32)
def sanitize(text):
    '''Convert text and discard incompatible and invalid characters'''
    try:
        #returnlines = []
        #for line in text.splitlines():
        #    returnlines.append(line_processing(line))
        # return '\n'.join(list(filter(None.__ne__, returnlines)))
        return '\n'.join([l for l in (line_processing(l) for l in text.splitlines()) if l is not None])
        # return '\n'.join([l for l in map(line_processing, text.splitlines()) if l is not None])
    except AttributeError:
        return None


@lru_cache(maxsize=128)
def trim(string):
    '''Remove unnecessary spaces within a text string'''
    try:
        # remove newlines that are not related to punctuation or markup + proper trimming
        return SPACE_TRIMMING.sub(r' ', NO_TAG_SPACE.sub(r' ', string)).strip(' \t\n\r\v')
    except TypeError:
        return None


def is_image_file(imagesrc):
    '''Check if the observed string corresponds to a valid image extension,
       return False otherwise'''
    return bool(imagesrc is not None and IMAGE_EXTENSION.search(imagesrc))


def filter_urls(linklist, urlfilter):
    'Return a list of links corresponding to the given substring pattern.'
    if urlfilter is None:
        return sorted(set(linklist))
    # filter links
    newlist = [l for l in linklist if urlfilter in l]
    # feedburner option
    if not newlist:
        newlist = [l for l in linklist if urlfilter in l or 'feedburner' in l or 'feedproxy' in l]
    return sorted(set(newlist))


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
        author = AUTHOR_REPLACE_JOIN.sub(' ', author)
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
