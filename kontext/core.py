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


def examine_meta(tree):
    '''Search meta tags for relevant information'''
    title = author = url = description = None
    # "og:" for OpenGraph http://ogp.me/
    for elem in tree.xpath('//head/meta'): # /head/ # for elem in tree.xpath('//meta[@property]'): # /head/
        # safeguard
        if len(elem.attrib) < 1:
            print('# DEBUG:', html.tostring(elem, pretty_print=False, encoding='unicode').strip())
            continue
        # property attribute
        if elem.get('property') is not None:
            # safeguard
            if elem.get('content') is None or len(elem.get('content')) < 1:
                continue
            # faster: detect OpenGraph schema
            if elem.get('property').startswith('og:'):
                # blogname
                #if elem.get('property') == 'og:site_name':
                #    blogname = elem.get('content')
                # blog title
                if elem.get('property') == 'og:title':
                    title = elem.get('content')
                # orig URL
                elif elem.get('property') == 'og:url' and url is None:
                    url = elem.get('content')
                # description
                elif elem.get('property') == 'og:description':
                    description = elem.get('content')
                # og:type
                #elif elem.get('property') == 'og:type':
                #    posttype = elem.get('content')
                # og:author
                elif elem.get('property') in ('og:author', 'og:article:author'):
                    author = elem.get('content')
            else:
                # author
                if elem.get('property') in ('author', 'article:author'): # article:...
                    author = elem.get('content')
        # name attribute
        elif 'name' in elem.attrib: # elem.get('name') is not None:
            # safeguard
            if elem.get('content') is None or len(elem.get('content')) < 1:
                continue
            # author
            if elem.get('name') in ('author', 'byl', 'dc.creator', 'sailthru.author'):
                author = elem.get('content')
            # title
            elif elem.get('name') in ('title', 'dc.title', 'sailthru.title'):
                if title is None:
                    title = elem.get('content')
            # description
            elif elem.get('name') in('description', 'dc.description', 'dc:description', 'sailthru.description'):
                if description is None:
                    description = elem.get('content')
            # blogname
            #elif elem.get('name') == 'publisher':
            #    if blogname is None:
            #        blogname = elem.get('content')
            # TODO: keywords
            # elif elem.get('name') in ('keywords', page-topic):
        # other types
        else:
            if elem.get('itemprop') == 'author':
                if len(elem.text_content()) > 0:
                    author = elem.text_content()
            elif elem.get('charset') is not None:
                pass # e.g. charset=UTF-8
            else:
                print('# DEBUG:', html.tostring(elem, pretty_print=False, encoding='unicode').strip())
    return trim(title), trim(author), trim(url), trim(description)


def extract_title(tree):
    '''Extract the document title'''
    title = None
    # extract from first h1
    if tree.find('//h1') is not None:
        title = tree.xpath('//h1')[0].text  #text_content()
    # try from title element
    elif tree.find('//head/title') is not None:
        title = tree.find('//head/title').text
    # take first h2 tag
    elif tree.find('//h2') is not None:
        title = tree.xpath('//h2')[0].text
    return trim(title)


def extract_author(tree):
    '''Extract the document author(s)'''
    try:
        docauthor = tree.find('//a[@rel="author"]').text  # h1?
    except (AttributeError, SyntaxError):  # no title found
        docauthor = None
    return trim(docauthor)


def extract_date(tree):
    '''Extract the date using external module htmldate'''
    docdate = find_date(tree, extensive_search=False)
    return docdate


def scrape(filecontent, url=None):
    '''Main process for metadata extraction'''
    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return None
    # meta tags
    title, author, url, description = examine_meta(tree)
    # title
    if title is None:
        title = extract_title(tree)
    # author
    if author is None:
        author = extract_author(tree)
    # date
    date = extract_date(tree)
    # return
    return title, author, date, description
