# -*- coding: utf-8 -*-
# pylint:disable-msg=E0611,I1101
"""
Module bundling functions related to HTML processing.
"""

import logging
from io import StringIO # python3

import cchardet as chardet
import requests
from lxml import etree, html


logger = logging.getLogger(__name__)


CUSTOM_HTMLPARSER = html.HTMLParser()


def fetch_url(url):
    """ Fetch page using requests """
    response = requests.get(url)
    if int(response.status_code) != 200:
        return None
    logger.debug('response encoding: %s', response.encoding)
    guessed_encoding = chardet.detect(response.content)['encoding']
    logger.debug('guessed encoding: %s', guessed_encoding)
    if guessed_encoding is not None:
        try:
            htmltext = response.content.decode(guessed_encoding)
        except UnicodeDecodeError:
            htmltext = response.text
    else:
        htmltext = response.text
    return htmltext


def load_html(htmlobject):
    """Load object given as input and validate its type (accepted: LXML tree and string)"""
    if isinstance(htmlobject, (etree._ElementTree, html.HtmlElement)):
        # copy tree
        tree = htmlobject
    elif isinstance(htmlobject, str):
        ## robust parsing
        try:
            #guessed_encoding = chardet.detect(htmlobject.encode())['encoding']
            #logger.info('guessed encoding: %s', guessed_encoding)
            # parse
            # parser = html.HTMLParser() # encoding=guessed_encoding  # document_fromstring
            tree = html.parse(StringIO(htmlobject), parser=CUSTOM_HTMLPARSER)
        except UnicodeDecodeError as err:
            logger.error('unicode %s', err)
            tree = None
        except UnboundLocalError as err:
            logger.error('parsed string %s', err)
            tree = None
        except (etree.XMLSyntaxError, ValueError, AttributeError) as err:
            logger.error('parser %s', err)
            tree = None
    else:
        logger.error('this type cannot be processed: %s', type(htmlobject))
        tree = None
    return tree
