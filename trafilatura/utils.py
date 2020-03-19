# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML and text processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

# import csv
import logging
import re
import socket
import sys
import urllib3

try:
    # this module is faster
    import cchardet
except ImportError:
    cchardet = None
# https://charset-normalizer.readthedocs.io/en/latest/
# https://ftfy.readthedocs.io/en/latest/

import requests
from lxml import etree, html
# from lxml.html.soupparser import fromstring as fromsoup


from .settings import MAX_FILE_SIZE, MIN_FILE_SIZE


LOGGER = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# collect_ids=False, default_doctype=False, huge_tree=True,
HTML_PARSER = html.HTMLParser(remove_comments=True, remove_pis=True, encoding='utf-8')
RECOVERY_PARSER = html.HTMLParser(remove_comments=True, remove_pis=True)

# UNICODE_WHITESPACE = re.compile(r'[\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000]')

NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable() and not chr(i) in (' ', '\t', '\n')
}
# .isspace()
# unicodedata.category(char)[0] != "C" or char in ('\t', '\n')


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
    # unicode-test
    if isutf8(bytesobject):
        return 'UTF-8'
    # try one of the installed detectors
    if cchardet is not None:
        guess = cchardet.detect(bytesobject)
        LOGGER.debug('guessed encoding: %s', guess['encoding'])
        return guess['encoding']
    # fallback on full response
    #if guess is None or guess['encoding'] is None: # or guess['confidence'] < 0.99:
    #    guessed_encoding = chardet.detect(bytesobject)['encoding']
    # return
    return None


def decode_response(response):
    """Read the first chunk of server response and decode it"""
    guessed_encoding = detect_encoding(response.content)
    LOGGER.debug('response/guessed encoding: %s / %s', response.encoding, guessed_encoding)
    # process
    if guessed_encoding is not None:
        try:
            htmltext = response.content.decode(guessed_encoding)
        except UnicodeDecodeError:
            LOGGER.warning('encoding error: %s / %s', response.encoding, guessed_encoding)
            htmltext = response.text
    else:
        htmltext = response.text
    return htmltext


def fetch_url(url):
    """ Fetch page using requests/urllib3
    Args:
        URL: URL of the page to fetch
    Returns:
        request object (headers + body).
    Raises:
        Nothing.
    """
    # customize headers
    headers = {
        'Connection': 'close',  # another way to cover tracks
        # 'User-Agent': '',  # your string here
    }
    # send
    try:
        # read by streaming chunks (stream=True, iter_content=xx)
        # so we can stop downloading as soon as MAX_FILE_SIZE is reached
        response = requests.get(url, timeout=30, verify=False, allow_redirects=True, headers=headers)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        LOGGER.error('malformed URL: %s', url)
    except requests.exceptions.TooManyRedirects:
        LOGGER.error('redirects: %s', url)
    except requests.exceptions.SSLError as err:
        LOGGER.error('SSL: %s %s', url, err)
    except (socket.timeout, requests.exceptions.ConnectionError, requests.exceptions.Timeout, socket.error, socket.gaierror) as err:
        LOGGER.error('connection: %s %s', url, err)
    #except Exception as err:
    #    logging.error('unknown: %s %s', url, err) # sys.exc_info()[0]
    else:
        # safety checks
        if response.status_code != 200:
            LOGGER.error('not a 200 response: %s', response.status_code)
        elif response.text is None or len(response.text) < MIN_FILE_SIZE:
            LOGGER.error('too small/incorrect: %s %s', url, len(response.text))
        elif len(response.text) > MAX_FILE_SIZE:
            LOGGER.error('too large: %s %s', url, len(response.text))
        else:
            return decode_response(response)
    return None


def load_html(htmlobject):
    """Load object given as input and validate its type
    (accepted: LXML tree and string)
    """
    tree = None
    # use tree directly
    if isinstance(htmlobject, (etree._ElementTree, html.HtmlElement)):
        return htmlobject
    # try to detect encoding and convert to string
    if isinstance(htmlobject, bytes):
        guessed_encoding = detect_encoding(htmlobject)
        if guessed_encoding is not None:
            if guessed_encoding == 'UTF-8':
                tree = html.fromstring(htmlobject, parser=HTML_PARSER)
            else:
                try:
                    htmlobject = htmlobject.decode(guessed_encoding)
                except UnicodeDecodeError:
                    LOGGER.warning('encoding issue: %s', guessed_encoding)
                    tree = html.fromstring(htmlobject, parser=RECOVERY_PARSER)
        else:
            tree = html.fromstring(htmlobject, parser=RECOVERY_PARSER)
    # use string if applicable
    if isinstance(htmlobject, str):
        try:
            tree = html.fromstring(htmlobject, parser=HTML_PARSER)
        except ValueError:
            # try to parse a bytestring
            try:
                tree = html.fromstring(htmlobject.encode('utf8'), parser=HTML_PARSER)
            except Exception as err:
                LOGGER.error('parser bytestring %s', err)
        #except UnicodeDecodeError as err:
        #    LOGGER.error('unicode %s', err)
        #except UnboundLocalError as err:
        #    LOGGER.error('parsed string %s', err)
        #except (etree.XMLSyntaxError, AttributeError) as err:
        #    LOGGER.error('parser %s', err)
        except Exception as err:
            LOGGER.error('parsing failed: %s', err)
    # default to None
    #else:
    #    LOGGER.error('this type cannot be processed: %s', type(htmlobject))
    # further test
    #if tree is not None:
    #    try:
    #       ignore = etree.tostring(tree, encoding='unicode')
    #    except UnicodeDecodeError:
    #       tree = None
    #if tree is None:
    #    if isinstance(htmlobject, bytes) or isinstance(htmlobject, str):
    #        # more robust parsing
    #        tree = fromsoup(htmlobject)
    return tree


def txttocsv(text, comments, docmeta):
    '''Output the result in CSV format (tab-separated values)'''
    # outputwriter = csv.writer(sys.stdout, delimiter='\t', quoting=csv.QUOTE_NONE)
    # outputwriter.writerow()
    text = trim(' '.join(text.splitlines()))
    if comments is not None:
        comments = trim(' '.join(comments.splitlines()))
    else:
        comments = ''
    if docmeta.url is None:
        docmeta.url = ''
    if docmeta.title is None:
        docmeta.title = ''
    if docmeta.date is None:
        docmeta.date = ''
    tsv_output = '{url}\t{doctitle}\t{docdate}\t{text}\t{comments}\n'.format(
        url=docmeta.url,
        doctitle=docmeta.title,
        docdate=docmeta.date,
        text=text,
        comments=comments
        )
    return tsv_output


def remove_control_characters(string):
    '''Prevent non-printable and XML invalid character errors'''
    # slow
    # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    # return ''.join(char for char in string if unicodedata.category(char)[0] != "C" or char in ('\t', '\n'))
    # https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python/93029#93029
    return string.translate(NOPRINT_TRANS_TABLE)
    # XML invalid characters
    # https://chase-seibert.github.io/blog/2011/05/20/stripping-control-characters-in-python.html


def sanitize(text):
    '''Convert text and discard incompatible unicode and invalid XML characters'''
    if text is None:
        return None
    # spacing HTML entities: https://www.w3.org/MarkUp/html-spec/html-spec_13.html
    text = text.replace('&#13;', '\r')
    text = text.replace('&#10;', '\n')
    # spaces
    text = re.sub(r'\u00A0|\u2007|\u202F', ' ', text)  # non-breaking spaces
    # text = UNICODE_WHITESPACE.sub('', text)
    # remove non-printable chars
    text = remove_control_characters(text)
    # https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
    # line endings
    # text = text.replace('\r\n', '\n')
    # unwanted characters
    # text = text.replace('\N{SOFT HYPHEN}', '')
    # https://stackoverflow.com/questions/16467479/normalizing-unicode
    # filter out empty lines
    returnlines = list()
    for line in text.splitlines():
        line = trim(line)
        if not re.match(r'[\s\t]*$', line):
            returnlines.append(line)
    return '\n'.join(returnlines)


def trim(string):
    '''Remove unnecessary spaces within a text string'''
    if string is not None:
        # remove newlines that are not related to punctuation or markup
        string = re.sub(r'(?<![p{P}>])\n', ' ', string)
        # proper trimming
        # string = ' '.join(re.split(r'\s+', string.strip(' \t\n\r'), flags=re.UNICODE|re.MULTILINE))
        string = string.strip(' \t\n\r')
        string = re.sub(r'\s+', ' ', string, flags=re.UNICODE|re.MULTILINE)
        # string = string.strip()
    return string
