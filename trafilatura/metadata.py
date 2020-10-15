"""
Module bundling all functions needed to scrape metadata from webpages.
"""


import logging
import re

from courlan.clean import normalize_url
from courlan.core import extract_domain
from courlan.filters import validate_url
from htmldate import find_date
from lxml import html

from .metaxpaths import author_xpaths, categories_xpaths, tags_xpaths, title_xpaths
from .utils import load_html, trim


LOGGER = logging.getLogger(__name__)
logging.getLogger('htmldate').setLevel(logging.WARNING)

METADATA_LIST = ['title', 'author', 'url', 'hostname', 'description', 'sitename', 'date', 'categories', 'tags', 'fingerprint', 'id']

HTMLDATE_CONFIG = {'extensive_search': False, 'original_date': True}

TITLE_REGEX = re.compile(r'(.+)?\s+[-|]\s+.*$')
JSON_AUTHOR_1 = re.compile(r'"author":[^}]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_2 = re.compile(r'"[Pp]erson"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_PUBLISHER = re.compile(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', re.DOTALL)
JSON_CATEGORY = re.compile(r'"articleSection": ?"([^"\\]+)', re.DOTALL)
JSON_HEADLINE = re.compile(r'"headline": ?"([^"\\]+)', re.DOTALL)
URL_COMP_CHECK = re.compile(r'https?://|/')


def extract_json(tree, metadata):
    '''Crudely extract metadata from JSON-LD data'''
    for elem in tree.xpath('//script[@type="application/ld+json"]|//script[@type="application/settings+json"]'):
        if not elem.text:
            continue
        if '"author":' in elem.text:
            mymatch = JSON_AUTHOR_1.search(elem.text)
            if mymatch and mymatch.group(1) and ' ' in mymatch.group(1):
                metadata['author'] = trim(mymatch.group(1))
            else:
                mymatch = JSON_AUTHOR_2.search(elem.text)
                if mymatch and mymatch.group(1) and ' ' in mymatch.group(1):
                    metadata['author'] = trim(mymatch.group(1))
        # try to extract publisher
        if '"publisher"' in elem.text:
            mymatch = JSON_PUBLISHER.search(elem.text)
            if mymatch and not ',' in mymatch.group(1):
                metadata['sitename'] = trim(mymatch.group(1))
        # category
        if '"articleSection"' in elem.text:
            mymatch = JSON_CATEGORY.search(elem.text)
            if mymatch:
                metadata['categories'] = [trim(mymatch.group(1))]
        # try to extract title
        if '"headline"' in elem.text and metadata['title'] is None:
            mymatch = JSON_HEADLINE.search(elem.text)
            if mymatch:
                metadata['title'] = trim(mymatch.group(1))
    return metadata


def extract_opengraph(tree):
    '''Search meta tags following the OpenGraph guidelines (https://ogp.me/)'''
    title, author, url, description, site_name = (None,) * 5
    # detect OpenGraph schema
    for elem in tree.xpath('//head/meta[starts-with(@property, "og:")]'):
        # safeguard
        if not elem.get('content'):
            continue
        # site name
        if elem.get('property') == 'og:site_name':
            site_name = elem.get('content')
        # blog title
        elif elem.get('property') == 'og:title':
            title = elem.get('content')
        # orig URL
        elif elem.get('property') == 'og:url':
            if validate_url(elem.get('content'))[0] is True:
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
    metadata = dict.fromkeys(METADATA_LIST)
    # bootstrap from potential OpenGraph tags
    title, author, url, description, site_name = extract_opengraph(tree)
    # test if all return values have been assigned
    if all((title, author, url, description, site_name)):  # if they are all defined
        metadata['title'], metadata['author'], metadata['url'], metadata['description'], metadata['sitename'] = title, author, url, description, site_name
        return metadata
    tags = []
    # skim through meta tags
    for elem in tree.xpath('//head/meta[@content]'):
        # content
        if not elem.get('content'):
            continue
        content_attr = elem.get('content')
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
        elif 'name' in elem.attrib:
            name_attr = elem.get('name').lower()
            # author
            if name_attr in ('author', 'byl', 'dc.creator', 'dcterms.creator', 'sailthru.author'):  # twitter:creator
                if author is None:
                    author = content_attr
            # title
            elif name_attr in ('title', 'dc.title', 'dcterms.title', 'fb_title', 'sailthru.title', 'twitter:title'):
                if title is None:
                    title = content_attr
            # description
            elif name_attr in ('description', 'dc.description', 'dcterms.description', 'dc:description', 'sailthru.description', 'twitter:description'):
                if description is None:
                    description = content_attr
            # site name
            elif name_attr in ('publisher', 'dc.publisher', 'dcterms.publisher', 'twitter:site', 'application-name') or 'twitter:app:name' in elem.get('name'):
                if site_name is None:
                    site_name = content_attr
            # url
            elif name_attr == 'twitter:url':
                if url is None and validate_url(content_attr)[0] is True:
                    url = content_attr
            # keywords
            elif name_attr == 'keywords': # 'page-topic'
                tags.append(content_attr)
        elif 'itemprop' in elem.attrib:
            if elem.get('itemprop') == 'author':
                if author is None:
                    author = content_attr
            elif elem.get('itemprop') == 'description':
                if description is None:
                    description = content_attr
            elif elem.get('itemprop') == 'headline':
                if title is None:
                    title = content_attr
            # to verify:
            #elif elem.get('itemprop') == 'name':
            #    if title is None:
            #        title = elem.get('content')
        # other types
        else:
            if not 'charset' in elem.attrib and not 'http-equiv' in elem.attrib and not 'property' in elem.attrib:
                LOGGER.debug(html.tostring(elem, pretty_print=False, encoding='unicode').strip())
    metadata['title'], metadata['author'], metadata['url'], metadata['description'], metadata['sitename'], metadata['tags'] = title, author, url, description, site_name, tags
    return metadata


def extract_metainfo(tree, expressions, len_limit=200):
    '''Extract meta information'''
    # try all XPath expressions
    for expression in expressions:
        # examine all results
        i = 0
        for elem in tree.xpath(expression):
            content = elem.text_content()
            if content and len(content) < len_limit:
                return trim(content)
            i += 1
        if i > 1:
            LOGGER.debug('more than one invalid result: %s %s', expression, i)
    return None


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
        mymatch = TITLE_REGEX.match(title)
        if mymatch:
            title = mymatch.group(1)
        return title
    except IndexError:
        LOGGER.warning('no main title found')
    # take first h1-title
    if h1_results:
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
    # https://www.tutorialrepublic.com/html-reference/html-base-tag.php
    # default url as fallback
    url = default_url
    # try canonical link first
    element = tree.find('.//head//link[@rel="canonical"]')
    if element is not None and URL_COMP_CHECK.match(element.attrib['href']):
        url = element.attrib['href']
    # try default language link
    else:
        for element in tree.xpath('//head//link[@rel="alternate"]'):
            if 'hreflang' in element.attrib and element.attrib['hreflang'] is not None and element.attrib['hreflang'] == 'x-default':
                if URL_COMP_CHECK.match(element.attrib['href']):
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
    # sanity check: don't return invalid URLs
    if url is not None:
        validation_result, parsed_url = validate_url(url)
        if validation_result is False:
            url = None
        else:
            url = normalize_url(parsed_url)
    return url


def extract_sitename(tree):
    '''Extract the name of a site from the main title'''
    try:
        mymatch = re.search(r'^.*?[-|]\s+(.*)$', tree.find('.//head/title').text)
        if mymatch:
            return mymatch.group(1)
    except AttributeError:
        pass
    return None


def extract_catstags(metatype, tree):
    '''Find category and tag information'''
    results = []
    regexpr = '/' + metatype + '/'
    if metatype == 'category':
        xpath_expression = categories_xpaths
    else:
        xpath_expression = tags_xpaths
    # search using custom expressions
    for catexpr in xpath_expression:
        for elem in tree.xpath(catexpr):
            if 'href' in elem.attrib and re.search(regexpr, elem.attrib['href']):
                results.append(elem.text_content())
        if results:
            break
    # category fallback
    if metatype == 'category' and not results:
        element = tree.find('.//head//meta[@property="article:section"]')
        if element is not None:
            results.append(element.attrib['content'])
    return [trim(x) for x in results if x is not None]


def extract_metadata(filecontent, default_url=None, date_config=None):
    '''Main process for metadata extraction'''
    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return None
    # initialize dict and try to strip meta tags
    metadata = examine_meta(tree)
    # correction: author not a name
    if metadata['author'] is not None:
        if ' ' not in metadata['author'] or metadata['author'].startswith('http'):
            metadata['author'] = None
    # fix: try json-ld metadata and override
    metadata = extract_json(tree, metadata)
    # try with x-paths
    # title
    if metadata['title'] is None:
        metadata['title'] = extract_title(tree)
    # author
    if metadata['author'] is None:
        metadata['author'] = extract_author(tree)
    # url
    if metadata['url'] is None:
        metadata['url'] = extract_url(tree, default_url)
    # hostname
    if metadata['url'] is not None:
        metadata['hostname'] = extract_domain(metadata['url'])
    # extract date with external module htmldate
    if date_config is None:
        date_config = HTMLDATE_CONFIG
    date_config['url'] = metadata['url']
    try:
        metadata['date'] = find_date(tree, **date_config)
    # temporary fix for htmldate bug
    except UnicodeError:
        pass
    # sitename
    if metadata['sitename'] is None:
        metadata['sitename'] = extract_sitename(tree)
    if metadata['sitename'] is not None:
        if metadata['sitename'].startswith('@'):
            # scrap Twitter ID
            metadata['sitename'] = re.sub(r'^@', '', metadata['sitename'])
        # capitalize
        try:
            if not '.' in metadata['sitename'] and not metadata['sitename'][0].isupper():
                metadata['sitename'] = metadata['sitename'].title()
        # fix for empty name
        except IndexError:
            pass
    else:
        # use URL
        if metadata['url']:
            mymatch = re.match(r'https?://(?:www\.|w[0-9]+\.)?([^/]+)', metadata['url'])
            if mymatch:
                metadata['sitename'] = mymatch.group(1)
    # categories
    if not metadata['categories']:
        metadata['categories'] = extract_catstags('category', tree)
    # tags
    if not metadata['tags']:
        metadata['tags'] = extract_catstags('tags', tree)
    # for safety: length check
    for key, value in metadata.items():
        if value is not None and len(value) > 10000:
            metadata[key] = value[:9999] + '…'
    # return
    return metadata
