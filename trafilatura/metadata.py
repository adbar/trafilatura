"""
Module bundling all functions needed to scrape metadata from webpages.
"""

import json
import logging
import re

from courlan.clean import normalize_url
from courlan.core import extract_domain
from courlan.filters import validate_url
from htmldate import find_date
from lxml import html

from .json_metadata import extract_json, extract_json_parse_error
from .metaxpaths import author_xpaths, categories_xpaths, tags_xpaths, title_xpaths
from .utils import line_processing, load_html, normalize_authors, trim


LOGGER = logging.getLogger(__name__)
logging.getLogger('htmldate').setLevel(logging.WARNING)

METADATA_LIST = ['title', 'author', 'url', 'hostname', 'description', 'sitename', 'date', 'categories', 'tags',
                 'fingerprint', 'id', 'license']

HTMLDATE_CONFIG_FAST = {'extensive_search': False, 'original_date': True}
HTMLDATE_CONFIG_EXTENSIVE = {'extensive_search': True, 'original_date': True}

JSON_MINIFY = re.compile(r'("(?:\\"|[^"])*")|\s')

HTMLTITLE_REGEX = re.compile(r'^(.+)?\s+[-|]\s+(.+)$')  # part without dots?
URL_COMP_CHECK = re.compile(r'https?://|/')
HTML_STRIP_TAG = re.compile(r'(<!--.*?-->|<[^>]*>)')

METANAME_AUTHOR = {'author', 'byl', 'dc.creator', 'dcterms.creator', 'sailthru.author', 'citation_author', 'parsely-author'}  # twitter:creator
METANAME_TITLE = {'title', 'dc.title', 'dcterms.title', 'fb_title', 'sailthru.title', 'twitter:title', 'citation_title', 'parsely-title'}
METANAME_DESCRIPTION = {'description', 'dc.description', 'dcterms.description', 'dc:description', 'sailthru.description', 'twitter:description'}
METANAME_PUBLISHER = {'copyright', 'dc.publisher', 'dcterms.publisher', 'publisher', 'citation_journal_title'}
METANAME_TAG = {'keywords', 'parsely-tags'}


def extract_meta_json(tree, metadata):
    '''Parse and extract metadata from JSON-LD data'''
    for elem in tree.xpath('.//script[@type="application/ld+json" or @type="application/settings+json"]'):
        if not elem.text:
            continue
        element_text = JSON_MINIFY.sub(r'\1', elem.text)
        try:
            schema = json.loads(element_text)
            metadata = extract_json(schema, metadata)
        except json.JSONDecodeError:
            metadata = extract_json_parse_error(element_text, metadata)
    return metadata


def extract_opengraph(tree):
    '''Search meta tags following the OpenGraph guidelines (https://ogp.me/)'''
    title, author, url, description, site_name = (None,) * 5
    # detect OpenGraph schema
    for elem in tree.xpath('.//head/meta[starts-with(@property, "og:")]'):
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
        # elif elem.get('property') == 'og:type':
        #    pagetype = elem.get('content')
        # og:locale
        # elif elem.get('property') == 'og:locale':
        #    pagelocale = elem.get('content')
    return trim(title), trim(author), trim(url), trim(description), trim(site_name)


def examine_meta(tree):
    '''Search meta tags for relevant information'''
    metadata = dict.fromkeys(METADATA_LIST)
    # bootstrap from potential OpenGraph tags
    title, author, url, description, site_name = extract_opengraph(tree)
    # test if all return values have been assigned
    if all((title, author, url, description, site_name)):  # if they are all defined
        metadata['title'], metadata['author'], metadata['url'], metadata['description'], metadata[
            'sitename'] = title, author, url, description, site_name
        return metadata
    tags, backup_sitename = [], None
    # skim through meta tags
    for elem in tree.iterfind('.//head/meta[@content]'):
        # content
        if not elem.get('content'):
            continue
        content_attr = HTML_STRIP_TAG.sub('', elem.get('content'))
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
                author = normalize_authors(author, content_attr)
        # name attribute
        elif 'name' in elem.attrib:
            name_attr = elem.get('name').lower()
            # author
            if name_attr in METANAME_AUTHOR:
                author = normalize_authors(author, content_attr)
            # title
            elif name_attr in METANAME_TITLE:
                title = title or content_attr
            # description
            elif name_attr in METANAME_DESCRIPTION:
                description = description or content_attr
            # site name
            elif name_attr in METANAME_PUBLISHER:
                site_name = site_name or content_attr
            elif name_attr in ('twitter:site', 'application-name') or 'twitter:app:name' in elem.get('name'):
                backup_sitename = content_attr
            # url
            elif name_attr == 'twitter:url':
                if url is None and validate_url(content_attr)[0] is True:
                    url = content_attr
            # keywords
            elif name_attr in METANAME_TAG:  # 'page-topic'
                tags.append(content_attr)
        elif 'itemprop' in elem.attrib:
            if elem.get('itemprop') == 'author':
                author = normalize_authors(author, content_attr)
            elif elem.get('itemprop') == 'description':
                description = description or content_attr
            elif elem.get('itemprop') == 'headline':
                title = title or content_attr
            # to verify:
            # elif elem.get('itemprop') == 'name':
            #    if title is None:
            #        title = elem.get('content')
        # other types
        else:
            if not any(key in elem.attrib for key in ('charset', 'http-equiv', 'property')):
                LOGGER.debug('unknown attribute: %s',
                             html.tostring(elem, pretty_print=False, encoding='unicode').strip())
    # backups
    if site_name is None and backup_sitename is not None:
        site_name = backup_sitename
    # copy
    metadata['title'], metadata['author'], metadata['url'], metadata['description'], metadata['sitename'], metadata[
        'tags'] = title, author, url, description, site_name, tags
    return metadata


def extract_metainfo(tree, expressions, len_limit=200):
    '''Extract meta information'''
    # try all XPath expressions
    for expression in expressions:
        # examine all results
        i = 0
        for elem in tree.xpath(expression):
            content = trim(' '.join(elem.itertext()))
            if content and 2 < len(content) < len_limit:
                # LOGGER.debug('metadata found in: %s', expression)
                return content
            i += 1
        if i > 1:
            LOGGER.debug('more than one invalid result: %s %s', expression, i)
    return None


def extract_title(tree):
    '''Extract the document title'''
    # only one h1-element: take it
    h1_results = tree.xpath('//h1')
    if len(h1_results) == 1:
        title = trim(h1_results[0].text_content())
        if len(title) > 0:
            return title
    # extract using x-paths
    title = extract_metainfo(tree, title_xpaths)
    if title is not None:
        return title
    # extract using title tag
    try:
        title = trim(tree.xpath('//head/title')[0].text_content())
        # refine
        mymatch = HTMLTITLE_REGEX.match(title)
        if mymatch:
            if '.' not in mymatch.group(1):
                title = mymatch.group(1)
            elif '.' not in mymatch.group(2):
                title = mymatch.group(2)
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
    author = extract_metainfo(tree, author_xpaths, len_limit=120)
    if author:
        author = normalize_authors(None, author)
    return author


def extract_url(tree, default_url=None):
    '''Extract the URL from the canonical link'''
    # https://www.tutorialrepublic.com/html-reference/html-base-tag.php
    # default url as fallback
    url = default_url
    # try canonical link first
    element = tree.find('.//head//link[@rel="canonical"]')
    if element is not None and 'href' in element.attrib and URL_COMP_CHECK.match(element.attrib['href']):
        url = element.attrib['href']
    # try default language link
    else:
        for element in tree.iterfind('.//head//link[@rel="alternate"]'):
            if 'hreflang' in element.attrib and element.attrib['hreflang'] is not None and element.attrib[
                'hreflang'] == 'x-default':
                if URL_COMP_CHECK.match(element.attrib['href']):
                    LOGGER.debug(html.tostring(element, pretty_print=False, encoding='unicode').strip())
                    url = element.attrib['href']
    # add domain name if it's missing
    if url is not None and url.startswith('/'):
        for element in tree.iterfind('.//head//meta[@content]'):
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
    '''Extract the name of a site from the main title (if it exists)'''
    title_elem = tree.find('.//head/title')
    if title_elem is not None and title_elem.text is not None:
        mymatch = HTMLTITLE_REGEX.match(title_elem.text)
        if mymatch:
            if '.' in mymatch.group(1):
                return mymatch.group(1)
            if '.' in mymatch.group(2):
                return mymatch.group(2)
    return None


def extract_catstags(metatype, tree):
    '''Find category and tag information'''
    results = []
    regexpr = '/' + metatype + '[s|ies]?/'
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
        if element is not None and 'content' in element.attrib:
            results.append(element.attrib['content'])
    results = [line_processing(x) for x in results if x is not None]
    return [x for x in results if x is not None]


def extract_metadata(filecontent, default_url=None, date_config=None, fastmode=False):
    """Main process for metadata extraction.

    Args:
        filecontent: HTML code as string.
        default_url: Previously known URL of the downloaded document.
        date_config: Provide extraction parameters to htmldate as dict().

    Returns:
        A dict() containing the extracted metadata information or None.

    """
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
    metadata = extract_meta_json(tree, metadata)
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
        # decide on fast mode
        if fastmode is False:
            date_config = HTMLDATE_CONFIG_EXTENSIVE
        else:
            date_config = HTMLDATE_CONFIG_FAST
    date_config['url'] = metadata['url']
    try:
        metadata['date'] = find_date(tree, **date_config)
    # temporary fixes for htmldate bugs # todo: remove later
    except (TypeError, UnicodeError):
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
        metadata['tags'] = extract_catstags('tag', tree)
    # license
    for element in tree.xpath('//a[@rel="license"]', ):
        if element.text is not None:
            metadata['license'] = trim(element.text)
            break
    # for safety: length check
    for key, value in metadata.items():
        if value is not None and len(value) > 10000:
            metadata[key] = value[:9999] + '…'
    # remove spaces and control characters
    for item in metadata:
        if metadata[item] is not None and isinstance(metadata[item], str):
            metadata[item] = line_processing(metadata[item])
    # return
    return metadata
