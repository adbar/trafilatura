"""
Module bundling all functions needed to scrape metadata from webpages.
"""


import logging
import re

from collections import namedtuple
from htmldate import find_date
from lxml import html

from .metaxpaths import author_xpaths, categories_xpaths, tags_xpaths, title_xpaths
from .utils import load_html, trim


LOGGER = logging.getLogger(__name__)
logging.getLogger('htmldate').setLevel(logging.WARNING)

HTMLDATE_CONFIG = {'extensive_search': False, 'original_date': True}


def extract_json(tree, mymeta):
    '''Crudely extract metadata from JSON-LD data'''
    for elem in tree.xpath('//script[@type="application/ld+json"]|//script[@type="application/settings+json"]'):
        if elem.text is None:
            continue
        if '"author":' in elem.text:
            mymatch = re.search(r'"author":[^}]+?"name?\\?": ?\\?"([^"\\]+)', elem.text, re.DOTALL)
            if mymatch and ' ' in mymatch.group(1):
                mymeta = mymeta._replace(author=trim(mymatch.group(1)))
            else:
                mymatch = re.search(r'"author"[^}]+?"names?".+?"([^"]+)', elem.text, re.DOTALL)
                if mymatch and ' ' in mymatch.group(1):
                    mymeta = mymeta._replace(author=trim(mymatch.group(1)))
        # try to extract publisher
        if '"publisher"' in elem.text:
            mymatch = re.search(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', elem.text, re.DOTALL)
            if mymatch and not ',' in mymatch.group(1):
                mymeta = mymeta._replace(sitename=trim(mymatch.group(1)))
        # category
        if '"articleSection"' in elem.text:
            mymatch = re.search(r'"articleSection": ?"([^"\\]+)', elem.text, re.DOTALL)
            if mymatch:
                mymeta = mymeta._replace(categories=[trim(mymatch.group(1))])
        # try to extract title
        if '"headline"' in elem.text and mymeta.title is None:
            mymatch = re.search(r'"headline": ?"([^"\\]+)', elem.text, re.DOTALL)
            if mymatch:
                mymeta = mymeta._replace(title=trim(mymatch.group(1)))
    return mymeta


def extract_opengraph(tree):
    '''Search meta tags following the OpenGraph guidelines (https://ogp.me/)'''
    title, author, url, description, site_name = (None,) * 5
    for elem in tree.xpath('//head/meta[@property]'):
        # detect OpenGraph schema
        if not elem.get('property').startswith('og:'):
            continue
        # safeguard
        if elem.get('content') is None or len(elem.get('content')) < 1:
            continue
        # site name
        if elem.get('property') == 'og:site_name':
            site_name = elem.get('content')
        # blog title
        elif elem.get('property') == 'og:title':
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
    return trim(title), trim(author), trim(url), trim(description), trim(site_name)


def examine_meta(tree):
    '''Search meta tags for relevant information'''
    # bootstrap from potential OpenGraph tags
    title, author, url, description, site_name = extract_opengraph(tree)
    # test if all return values have been assigned
    if all((title, author, url, description, site_name)):  # if they are all defined
        return (title, author, url, description, site_name, None, None, None)
    tags = list()
    # skim through meta tags
    for elem in tree.xpath('//head/meta'):
        # safeguard
        if len(elem.attrib) < 1:
            LOGGER.debug(html.tostring(elem, pretty_print=False, encoding='unicode').strip())
            continue
        # content
        if 'content' not in elem.attrib:
            continue
        content_attr = elem.get('content')
        if len(content_attr) < 1:
            continue
        # image info
        # ...
        # property
        if 'property' in elem.attrib:
            # no opengraph a second time
            if elem.get('property').startswith('og:'):
                continue
            if elem.get('property') == 'article:tag':
                tags.append(content_attr)
            elif elem.get('property') in ('author', 'article:author'):
                if author is None:
                    author = content_attr
        # name attribute
        elif 'name' in elem.attrib: # elem.get('name') is not None:
            # author
            if elem.get('name') in ('author', 'byl', 'dc.creator', 'sailthru.author'):  # twitter:creator
                if author is None:
                    author = content_attr
            # title
            elif elem.get('name') in ('title', 'dc.title', 'sailthru.title', 'twitter:title'):
                if title is None:
                    title = content_attr
            # description
            elif elem.get('name') in ('description', 'dc.description', 'dc:description', 'sailthru.description', 'twitter:description'):
                if description is None:
                    description = content_attr
            # site name
            elif elem.get('name') in ('publisher', 'DC.publisher', 'twitter:site', 'application-name') or 'twitter:app:name' in elem.get('name'):
                if site_name is None:
                    site_name = content_attr
            # url
            elif elem.get('name') == 'twitter:url':
                if url is None:
                    url = content_attr
            # keywords
            elif elem.get('name') == 'keywords': # 'page-topic'
                tags.append(content_attr)
        elif 'itemprop' in elem.attrib:
            if elem.get('itemprop') == 'author':
                if author is None:
                    author = content_attr
            elif elem.get('itemprop') == 'description':
                if description is None:
                    description = content_attr
            # to verify:
            #elif elem.get('itemprop') == 'name':
            #    if title is None:
            #        title = elem.get('content')
        # other types
        else:
            if 'charset' in elem.attrib or 'http-equiv' in elem.attrib or 'property' in elem.attrib:
                pass  # e.g. charset=UTF-8
            else:
                LOGGER.debug(html.tostring(elem, pretty_print=False, encoding='unicode').strip())
    return (trim(title), trim(author), trim(url), trim(description), trim(site_name), None, None, tags)


def extract_metainfo(tree, expressions, len_limit=200):
    '''Extract meta information'''
    result = None
    # try all XPath expressions
    for expression in expressions:
        target_elements = tree.xpath(expression)
        # report potential errors
        if len(target_elements) > 1:
            LOGGER.debug('more than one result: %s %s', expression, len(target_elements))
        # examine all results
        for elem in target_elements:
            if elem.text_content() is not None and len(elem.text_content()) < len_limit:
                result = elem.text_content()
            # exit loop if something usable has been found
            if result is not None:
                break
        # exit loop if something usable has been found
        if result is not None:
            break
    return trim(result)


def extract_title(tree):
    '''Extract the document title'''
    title = None
    # only one h1-element: take it
    h1_results = tree.xpath('//h1')
    if len(h1_results) == 1:
        return h1_results[0].text_content()
    # extract using x-paths
    title = extract_metainfo(tree, title_xpaths)
    if title is not None:
        return title
    # extract using title tag
    try:
        title = tree.xpath('//head/title')[0].text_content()
        # refine
        if '-' in title or '|' in title:
            mymatch = re.search(r'^(.+)?\s+[-|]\s+.*$', title)
            if mymatch:
                title = mymatch.group(1)
        return title
    except IndexError:
        LOGGER.warning('no main title found')
    # take first h1-title
    if len(h1_results) > 0:
        return h1_results[0].text_content()
    # take first h2-title
    try:
        title = tree.xpath('//h2')[0].text_content()
    except IndexError:
        LOGGER.warning('no h2 title found')
    return title


def extract_author(tree):
    '''Extract the document author(s)'''
    author = extract_metainfo(tree, author_xpaths, len_limit=75)
    if author:
        # simple filters for German and English
        author = re.sub(r'^([a-zäöüß]+(ed|t))? ?(by|von) ', '', author, flags=re.IGNORECASE)
        author = re.sub(r'\d.+?$', '', author)
        author = re.sub(r'[^\w]+$|( am| on)', '', trim(author))
        author = author.title()
    return author


def extract_url(tree, default_url=None):
    '''Extract the URL from the canonical link'''
    # default url as fallback
    url = default_url
    # try canonical link first
    element = tree.find('.//head//link[@rel="canonical"]')
    if element is not None:
        url = element.attrib['href']
    # try default language link
    else:
        for element in tree.xpath('//head//link[@rel="alternate"]'):
            if 'hreflang' in element.attrib and element.attrib['hreflang'] is not None and element.attrib['hreflang'] == 'x-default':
                LOGGER.debug(html.tostring(element, pretty_print=False, encoding='unicode').strip())
                url = element.attrib['href']
    # add domain name if it's missing
    if url is not None and url.startswith('/'):
        for element in tree.xpath('//head//meta[@content]'):
            if 'name' in element.attrib:
                attrtype = element.attrib['name']
            elif 'property' in element.attrib:
                attrtype = element.attrib['property']
            else:
                continue
            if attrtype.startswith('og:') or attrtype.startswith('twitter:'):
                domain_match = re.match(r'https?://[^/]+', element.attrib['content'])
                if domain_match:
                    # prepend URL
                    url = domain_match.group(0) + url
                    break
    return url


def extract_sitename(tree):
    '''Extract the name of a site from the main title'''
    try:
        title_elem = tree.find('.//head/title')
        mymatch = re.search(r'^.*?[-|]\s+(.*)$', title_elem.text)
        if mymatch:
            return mymatch.group(1)
    except AttributeError:
        pass
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
                        result = trim(elem.text_content())
                        if result is not None:
                            results.append(result)
    # category fallback
    if metatype == 'category' and len(results) == 0:
        element = tree.find('.//head//meta[@property="article:section"]')
        if element is not None:
            results.append(trim(element.attrib['content']))
    return results


def extract_metadata(filecontent, default_url=None, date_config=None):
    '''Main process for metadata extraction'''
    # create named tuple
    Metadata = namedtuple('Metadata', ['title', 'author', 'url', 'description', 'sitename', 'date', 'categories', 'tags'])
    # Metadata.__new__.__defaults__ = (None,) * len(Metadata._fields)
    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return None
    # meta tags
    mymeta = Metadata._make(examine_meta(tree))
    # correction: author not a name
    if mymeta.author is not None:
        if ' ' not in mymeta.author or mymeta.author.startswith('http'):
            mymeta = mymeta._replace(author=None)
    # fix: try json-ld metadata and override
    mymeta = extract_json(tree, mymeta)
    # extract date with external module htmldate
    if date_config is None:
        date_config = HTMLDATE_CONFIG
    date_config['url'] = mymeta.url
    mymeta = mymeta._replace(date=find_date(tree, **date_config))
    # try with x-paths
    # title
    if mymeta.title is None:
        mymeta = mymeta._replace(title=extract_title(tree))
    # author
    if mymeta.author is None:
        mymeta = mymeta._replace(author=extract_author(tree))
    # url
    if mymeta.url is None:
        mymeta = mymeta._replace(url=extract_url(tree, default_url))
    # sitename
    if mymeta.sitename is None:
        mymeta = mymeta._replace(sitename=extract_sitename(tree))
    if mymeta.sitename is not None:
        if mymeta.sitename.startswith('@'):
            # scrap Twitter ID
            mymeta = mymeta._replace(sitename=re.sub(r'^@', '', mymeta.sitename))
        # capitalize
        if not '.' in mymeta.sitename and not mymeta.sitename[0].isupper():
            mymeta = mymeta._replace(sitename=mymeta.sitename.title())
    else:
        # use URL
        if mymeta.url:
            mymatch = re.match(r'https?://(?:www\.|w[0-9]+\.)?([^/]+)', mymeta.url)
            if mymatch:
                mymeta = mymeta._replace(sitename=mymatch.group(1))
    # categories
    if mymeta.categories is None or len(mymeta.categories) == 0:
        mymeta = mymeta._replace(categories=extract_catstags('category', tree))
    # tags
    if mymeta.tags is None or len(mymeta.tags) == 0:
        mymeta = mymeta._replace(tags=extract_catstags('tags', tree))
    # return
    return mymeta
