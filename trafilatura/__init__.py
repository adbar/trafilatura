"""
Python & command-line tool to gather text on the Web:
web crawling/scraping, extraction of text, metadata, comments.
"""

__title__ = "Trafilatura"
__author__ = "Adrien Barbaresi and contributors"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2019-present, Adrien Barbaresi"
__version__ = "2.0.0"


import logging

from .core import _internal_extraction


from .utils import load_html

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "bare_extraction",
    "_internal_extraction",
    "baseline",
    "fetch_response",
    "fetch_url",
    "load_html",
]
