# -*- coding: utf-8 -*-
"""
Extract the date of web pages, or web archeology in practice.
"""

## meta
__title__ = 'textract'
__author__ = 'Adrien Barbaresi'
__license__ = 'GNU GPL v3'
__copyright__ = 'Copyright 2019, Adrien Barbaresi'
__version__ = '0.0.1'

## imports
from .core import *

## logging best practices
# http://docs.python-guide.org/en/latest/writing/logging/
# https://github.com/requests/requests/blob/master/requests/__init__.py

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())
