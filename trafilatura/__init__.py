# -*- coding: utf-8 -*-
"""
Python & command-line tool to gather text on the Web:
web crawling/scraping, extraction of text, metadata, comments.
"""

# meta
__title__ = 'trafilatura'
__author__ = 'Adrien Barbaresi and contributors'
__license__ = 'GNU GPL v3+'
__copyright__ = 'Copyright 2019-2023, Adrien Barbaresi'
__version__ = '1.4.1'


import logging

from .core import bare_extraction, baseline, extract, html2txt, process_record
from .downloads import fetch_url
from .metadata import extract_metadata
from .utils import load_html

logging.getLogger(__name__).addHandler(logging.NullHandler())
