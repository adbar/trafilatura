"""
Module bundling all functions needed to scrape metadata from webpages.
"""


import logging
import re

from htmldate import find_date
from htmldate.utils import load_html
from lxml import etree, html

LOGGER = logging.getLogger(__name__)


def trim(string):
    '''Remove unnecesary spaces within a text string'''
    if string is not None:
        # delete newlines that are not related to punctuation or markup
        # string = re.sub(r'(?<![p{P}>])\n', ' ', string)
        # proper trimming
        string = ' '.join(re.split(r'\s+', string.strip(' \t\n\r'), flags=re.UNICODE|re.MULTILINE))
        string = string.strip()
    return string


def extract_title(tree):
    '''Extract the document title'''
    try:
        doctitle = tree.find('//title').text  # h1?
    except (AttributeError, SyntaxError):  # no title found
        doctitle = None
    return trim(doctitle)


def extract_date(tree):
    '''Extract the date using external module htmldate'''
    docdate = find_date(tree, extensive_search=False)
    return docdate


def extract(filecontent, url=None):
    '''Main process for metadata extraction'''
    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return None
    # title
    title = extract_title(tree)
    # date
    date = extract_date(tree)
    # author
    # ..
    # return
    return title, date
