# -*- coding: utf-8 -*-
"""
Listing a series of settings that are applied module-wide.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

from lxml.html.clean import Cleaner


MAX_FILE_SIZE = 20000000
MIN_FILE_SIZE = 10

## extract
MIN_EXTRACTED_SIZE = 200
MIN_EXTRACTED_COMM_SIZE = 100
MIN_DUPLCHECK_SIZE = 100

LRU_SIZE = 10000000

# filters
LANGUAGES = ['de', 'en', 'es', 'fr', 'ja', 'nl', 'ru']

#CORPUS_VERSION = 2017.1

# HTML_CLEANER config # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
HTML_CLEANER = Cleaner()
HTML_CLEANER.annoying_tags = False # True
HTML_CLEANER.comments = True
HTML_CLEANER.embedded = False # True
HTML_CLEANER.forms = False # True
HTML_CLEANER.frames = False # True
HTML_CLEANER.javascript = False # True
HTML_CLEANER.links = False
HTML_CLEANER.meta = False
HTML_CLEANER.page_structure = False
HTML_CLEANER.processing_instructions = True
HTML_CLEANER.remove_unknown_tags = False
HTML_CLEANER.safe_attrs_only = False
HTML_CLEANER.scripts = False # True
HTML_CLEANER.style = False
# HTML_CLEANER.remove_tags = ['a', 'abbr', 'acronym', 'address', 'big', 'cite', 'dd', 'font', 'ins', 'meta', 'span', 'small', 'sub', 'sup', 'wbr'] #  'center', 'table', 'tbody', 'td', 'th', 'tr',
HTML_CLEANER.remove_tags = ['img']
HTML_CLEANER.kill_tags = ['aside']
# 'audio', 'blink', 'canvas', 'embed', 'figure', 'footer', 'form', 'head', 'iframe', 'img', 'link', 'map', 'math', 'marquee', 'nav', 'noscript', 'object', 'picture', 'script', 'style', 'svg', 'time', 'video' # 'area', 'table' # 'header'

CUT_EMPTY_ELEMS = {'article', 'b', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', \
                   'i', 'li', 'main', 'p', 'section', 'strong', 'td'}
                   # 'meta', 'span',

MANUALLY_CLEANED = ['audio', 'blink', 'button', 'canvas', 'embed', 'figure', \
                    'footer', 'form', 'head', 'iframe', 'input', 'link', \
                    'map', 'marquee', 'math', 'nav', 'noscript', 'object', \
                    'picture', 'script', 'style', 'svg', 'time', 'video']
                    # 'frame' 'frameset' 'source', 'img',

TAG_CATALOG = frozenset(['code', 'del', 'fw', 'head', 'hi', 'lb', 'list', 'p', 'quote'])
# 'span', 'item'
