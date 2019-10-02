# -*- coding: utf-8 -*-
# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML and text processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re
import socket
import unicodedata

from io import StringIO # python3

try:
    # this module is faster
    import cchardet as chardet
except ImportError:
    import chardet

import requests
import urllib3
from lxml import etree, html

from .settings import MAX_FILE_SIZE # MIN_FILE_SIZE ?


LOGGER = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CUSTOM_HTMLPARSER = html.HTMLParser() # etree.HTMLParser() # remove_pis=True, collect_ids=False

UNICODE_WHITESPACE = re.compile(u'[\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000]')


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
    headers = requests.utils.default_headers()
    headers.update({
        'Connection': 'close',  # another way to cover tracks
        # 'User-Agent': '', # your string here
    })
    # send
    try:
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
    # if no error
    else:
        # safety checks
        if int(response.status_code) != 200:
            LOGGER.error('not a 200 response: %s', response.status_code)
        #elif response.text is None or len(response.text) < 100:
        #    LOGGER.error('file too small/incorrect response: %s %s', url, len(response.text))
        elif len(response.text) > MAX_FILE_SIZE:
            LOGGER.error('file too large: %s %s', url, len(response.text))
        else:
            guessed_encoding = chardet.detect(response.content)['encoding']
            LOGGER.debug('response/guessed encoding: %s / %s', response.encoding, guessed_encoding)
            if guessed_encoding is not None:
                try:
                    htmltext = response.content.decode(guessed_encoding)
                except UnicodeDecodeError:
                    htmltext = response.text
            else:
                htmltext = response.text
            # return here
            return htmltext
    # catchall
    return None


def load_html(htmlobject):
    '''Load object given as input and validate its type (accepted: LXML tree and string)'''
    tree = None
    if isinstance(htmlobject, (etree._ElementTree, html.HtmlElement)):
        # copy tree
        tree = htmlobject
    elif isinstance(htmlobject, str):
        ## robust parsing
        try:
            #guessed_encoding = chardet.detect(htmlobject.encode())['encoding']
            #LOGGER.info('guessed encoding: %s', guessed_encoding)
            # parse # encoding=guessed_encoding
            tree = html.parse(StringIO(htmlobject)) # , parser=CUSTOM_HTMLPARSER
        except UnicodeDecodeError as err:
            LOGGER.error('unicode %s', err)
        except ValueError:
            # try to parse a bytestring
            try:
                tree = html.fromstring(htmlobject.encode('utf8'))
            except Exception as err:
                LOGGER.error('parser bytestring %s', err)
        except UnboundLocalError as err:
            LOGGER.error('parsed string %s', err)
        except (etree.XMLSyntaxError, AttributeError) as err:
            LOGGER.error('parser %s', err)
    else:
        LOGGER.error('this type cannot be processed: %s', type(htmlobject))
    return tree


def remove_control_characters(string):
    '''Prevent XML invalid character errors'''
    # TODO: slow
    # https://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
    return ''.join(char for char in string if unicodedata.category(char)[0] != "C" or char in ('\t', '\n'))
    # return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', string)
    # invalid_xml = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]')
    # text = invalid_xml.sub('', text)
    #\x0b\x0c\r\x1c\x1d\x1e\x1f \x85\xa0


def sanitize(text):
    '''Convert text and discard incompatible unicode and invalid XML characters'''
    text = remove_control_characters(text)
    text = text.replace('\r\n', '\n')
    text = text.replace('&#13;', '')
    text = UNICODE_WHITESPACE.sub('', text)
    #text = re.sub(r'&#13;|', '', text)
    # filter out empty lines
    returntext = ''
    for line in text.splitlines():
        if not re.match(r'[\s\t]*$', line):
            # line = line.replace('\s\s\s', '\s')
            returntext += line + '\n'
    return returntext


def trim(string):
    '''Remove unnecesary spaces within a text string'''
    # delete newlines that are not related to punctuation or markup
    # string = re.sub(r'(?<![p{P}>])\n', ' ', string)
    # proper trimming
    string = re.sub(r'\s+', ' ', string.strip(' \t\n\r'), re.MULTILINE)
    string = string.strip()
    return string
