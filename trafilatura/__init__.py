# -*- coding: utf-8 -*-
"""
Extract the text content of web pages.
"""

# meta
__title__ = 'trafilatura'
__author__ = 'Adrien Barbaresi and contributors'
__license__ = 'GNU GPL v3+'
__copyright__ = 'Copyright 2019-2021, Adrien Barbaresi'
__version__ = '1.0.0'

# imports
import logging

from .core import bare_extraction, baseline, extract, process_record
from .downloads import fetch_url
from .metadata import extract_metadata
from .utils import load_html

# logging best practices
# http://docs.python-guide.org/en/latest/writing/logging/
# https://github.com/requests/requests/blob/master/requests/__init__.py
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())
