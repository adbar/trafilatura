"""
Module bundling all functions needed to scrape metadata from webpages.
"""


import logging
import re

from collections import namedtuple

from htmldate import find_date
from htmldate.utils import load_html
from lxml import etree, html

from .xpaths import categories_xpaths, tags_xpaths


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


def extract_opengraph(tree):
    '''Search meta tags following the OpenGraph guidelines (https://ogp.me/)'''
    title = author = url = description = site_name = None
    for elem in tree.xpath('//head/meta[@property]'):
        # safeguard
        if elem.get('content') is None or len(elem.get('content')) < 1:
            continue
        # faster: detect OpenGraph schema
        if elem.get('property').startswith('og:'):
            # site name
            if elem.get('property') == 'og:site_name':
                site_name = elem.get('content')
            # blog title
            if elem.get('property') == 'og:title':
                title = elem.get('content')
            # orig URL
            elif elem.get('property') == 'og:url':
                url = elem.get('content')
            # description
            elif elem.get('property') == 'og:description':
                description = elem.get('content')
            # og:author
            elif elem.get('property') in ('og:author', 'og:article:author'):
                author = elem.get('content')
            # og:type
            #elif elem.get('property') == 'og:type':
            #    pagetype = elem.get('content')
            # og:locale
            #elif elem.get('property') == 'og:locale':
            #    pagelocale = elem.get('content')
        else:
            # author
            if elem.get('property') in ('author', 'article:author'):
                author = elem.get('content')
    return trim(title), trim(author), trim(url), trim(description), trim(site_name)


def examine_meta(tree):
    '''Search meta tags for relevant information'''
    title = author = url = description = site_name = None
    # test for potential OpenGraph tags
    if tree.find('//head/meta[@property]') is not None:
        title, author, url, description, site_name = extract_opengraph(tree)
        # test if all return values have been assigned
        if all((title, author, url, description, site_name)):  # if they are all defined
            return (title, author, url, description, site_name, None, None, None)
    for elem in tree.xpath('//head/meta'):
        # safeguard
        if len(elem.attrib) < 1:
            print('# DEBUG:', html.tostring(elem, pretty_print=False, encoding='unicode').strip())
            continue
        # name attribute
        if 'name' in elem.attrib: # elem.get('name') is not None:
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
            # site name
            elif elem.get('name') == 'publisher':
                if site_name is None:
                    site_name = elem.get('content')
            # keywords
            # elif elem.get('name') in ('keywords', page-topic):
        # other types
        else:
            if elem.get('itemprop') == 'author':
                if len(elem.text_content()) > 0:
                    author = elem.text_content()
            elif elem.get('charset') is not None:
                pass  # e.g. charset=UTF-8
            else:
                print('# DEBUG:', html.tostring(elem, pretty_print=False, encoding='unicode').strip())
    return (trim(title), trim(author), trim(url), trim(description), trim(site_name), None, None, None)


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
    author = None
    if tree.find('//a[@rel="author"]') is not None:  # rel="me"
        author = tree.find('//a[@rel="author"]').text
    elif tree.find('//a[@class="author"]') is not None:  # rel="me"
        author = tree.find('//a[@class="author"]').text
    elif tree.find('//span[@class="author"]') is not None:
        author = tree.find('//span[@class="author"]').text
    elif tree.find('//address[@class="author"]') is not None:
        author = tree.find('//address[@class="author"]').text
    elif tree.find('//author') is not None:
        author = tree.find('//author').text
    return trim(author)


def extract_date(tree, url):
    '''Extract the date using external module htmldate'''
    docdate = find_date(tree, extensive_search=False, url=url)
    return docdate


def extract_url(tree):
    '''Extract the URL from the canonical link'''
    element = tree.find('//head/link[@rel="canonical"]')
    if element is not None:
        return element.attrib['href']
    return None


def extract_catstags(metatype, tree):
    '''Find category and tag information'''
    results = list()
    regexpr = '/' + metatype + '/'
    if metatype == 'category':
       xpath_expression = categories_xpaths
    else:
       xpath_expression = tags_xpaths
    #if tree.find(expr) is not None:
    #     # expr = expr + '/a'
    for catexpr in xpath_expression:
        target_elements = tree.xpath(catexpr)
        if len(target_elements) > 0:  # if something has been found
            for elem in target_elements:
                if 'href' in elem.attrib:
                    match = re.search(regexpr, elem.attrib['href'])
                    if match:
                        results.append(elem.text_content())
            return results


def scrape(filecontent, url=None):
    '''Main process for metadata extraction'''
    # create named tuple
    Metadata = namedtuple('Metadata', ['title', 'author', 'url', 'description', 'sitename', 'date', 'categories', 'tags'])
    Metadata.__new__.__defaults__ = (None,) * len(Metadata._fields)
    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return None
    # meta tags
    mymeta = Metadata._make(examine_meta(tree))
    # title
    if getattr(mymeta, 'title') is None:
        mymeta = mymeta._replace(title=extract_title(tree))
    # author
    if getattr(mymeta, 'author') is None:
        mymeta = mymeta._replace(author=extract_author(tree))
    # url
    if getattr(mymeta, 'url') is None:
        mymeta = mymeta._replace(url=extract_url(tree))
    # date
    # if getattr(mymeta, 'date') is None:
    mymeta = mymeta._replace(date=extract_date(tree, url=mymeta.url))
    # categories
    mymeta = mymeta._replace(categories=extract_catstags('category', tree))
    # tags
    mymeta = mymeta._replace(tags=extract_catstags('tags', tree))
    # return
    return mymeta
