# -*- coding: utf-8 -*-
"""
Extract the text content of web pages.
"""

# meta
__title__ = 'trafilatura'
__author__ = 'Adrien Barbaresi and contributors'
__license__ = 'GNU GPL v3+'
__copyright__ = 'Copyright 2019-2022, Adrien Barbaresi'
__version__ = '1.4.0'


import logging

from .core import bare_extraction, baseline, extract, html2txt, process_record
from .downloads import fetch_url
from .metadata import extract_metadata
from .utils import load_html

logging.getLogger(__name__).addHandler(logging.NullHandler())
