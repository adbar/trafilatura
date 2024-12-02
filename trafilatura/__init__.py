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

from .baseline import baseline, html2txt
from .core import bare_extraction, extract
from .downloads import fetch_response, fetch_url
from .metadata import extract_metadata
from .utils import load_html

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "bare_extraction",
    "baseline",
    "extract",
    "extract_metadata",
    "fetch_response",
    "fetch_url",
    "html2txt",
    "load_html",
]
