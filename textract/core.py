# -*- coding: utf-8 -*-
"""
Module bundling all functions needed to determine the date of HTML strings or LXML trees.
"""

## This file is available from https://github.com/adbar/textract
## under GNU GPL v3 license

# compatibility
from __future__ import absolute_import, division, print_function, unicode_literals

# from future import standard_library
# standard_library.install_aliases()

# standard
import datetime
import logging
import re
import time

# from codecs import open
from collections import Counter

try:
    from cStringIO import StringIO # Python 2
except ImportError:
    from io import StringIO # Python 3

# third-party
from lxml import etree, html
from lxml.html.clean import Cleaner


## TODO:
# ...



## INIT
logger = logging.getLogger(__name__)

EXPRESSIONS = [
    "//*[contains(@class, 'date') or contains(@class, 'Date') or contains(@class, 'datum') or contains(@class, 'Datum')]",
]
# "//*[contains(@class, 'fa-clock-o')]",


cleaner = Cleaner()
cleaner.comments = True
cleaner.embedded = True
cleaner.forms = False
cleaner.frames = True
cleaner.javascript = False
cleaner.links = False
cleaner.meta = False
cleaner.page_structure = True
cleaner.processing_instructions = True
cleaner.remove_unknown_tags = False
cleaner.safe_attrs_only = False
cleaner.scripts = False
cleaner.style = False
cleaner.kill_tags = ['audio', 'canvas', 'label', 'map', 'math', 'object', 'picture', 'rdf', 'svg', 'table', 'video']
# 'embed', 'figure', 'img',
