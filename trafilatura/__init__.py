# -*- coding: utf-8 -*-
"""
Python & command-line tool to gather text on the Web:
web crawling/scraping, extraction of text, metadata, comments.
"""


__title__ = 'trafilatura'
__author__ = 'Adrien Barbaresi and contributors'
__license__ = "Apache-2.0"
__copyright__ = 'Copyright 2019-2024, Adrien Barbaresi'
__version__ = '1.9.0'


import logging

from .baseline import baseline, html2txt
from .core import bare_extraction, extract, process_record
from .downloads import fetch_response, fetch_url
from .metadata import extract_metadata
from .utils import load_html

logging.getLogger(__name__).addHandler(logging.NullHandler())
