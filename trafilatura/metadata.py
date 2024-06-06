"""
Module bundling all functions needed to scrape metadata from webpages.
"""

import json
import logging
import re

from copy import deepcopy

from courlan import extract_domain, get_base_url, is_valid_url, normalize_url, validate_url
from htmldate import find_date
from lxml.html import tostring

from .htmlprocessing import prune_unwanted_nodes
from .json_metadata import (extract_json, extract_json_parse_error,
                            normalize_json)
from .settings import set_date_params
from .utils import (line_processing, load_html, normalize_authors,
                    normalize_tags, trim, unescape)
from .xpaths import (AUTHOR_DISCARD_XPATHS, AUTHOR_XPATHS,
                     CATEGORIES_XPATHS, TAGS_XPATHS, TITLE_XPATHS)

LOGGER = logging.getLogger(__name__)
logging.getLogger('htmldate').setLevel(logging.WARNING)


class Document:
    "Defines a class to store all necessary data and metadata fields for extracted information."
    __slots__ = [
    'title', 'author', 'url', 'hostname', 'description', 'sitename',
    'date', 'categories', 'tags', 'fingerprint', 'id', 'license',
    'body', 'comments', 'commentsbody', 'raw_text', 'text',
    'language', 'image', 'pagetype', 'filedate'  # 'locale'?
    ]
    # consider dataclasses for Python 3.7+
    def __init__(self):
        for slot in self.__slots__:
            setattr(self, slot, None)

    def set_attributes(self, title, author, url, description, site_name, image, pagetype, tags):
        "Helper function to (re-)set a series of attributes."
        if title:
            self.title = title
        if author:
            self.author = author
        if url:
            self.url = url
        if description:
            self.description = description
        if site_name:
            self.sitename = site_name
        if image:
            self.image = image
        if pagetype:
            self.pagetype = pagetype
        if tags:
            self.tags = tags

    def clean_and_trim(self):
        "Limit text length and trim the attributes."
        for slot in self.__slots__:
            value = getattr(self, slot)
            if isinstance(value, str):
                # length
                if len(value) > 10000:
                    new_value = value[:9999] + '…'
                    setattr(self, slot, new_value)
                    value = new_value
                # HTML entities, remove spaces and control characters
                value = line_processing(unescape(value))
                setattr(self, slot, value)

    def as_dict(self):
        "Convert the document to a dictionary."
        return {
            attr: getattr(self, attr, None)
            for attr in self.__slots__
        }


JSON_MINIFY = re.compile(r'("(?:\\"|[^"])*")|\s')

HTMLTITLE_REGEX = re.compile(r'^(.+)?\s+[–•·—|⁄*⋆~‹«<›»>:-]\s+(.+)$')  # part without dots?
HTML_STRIP_TAG = re.compile(r'(<!--.*?-->|<[^>]*>)')

LICENSE_REGEX = re.compile(r'/(by-nc-nd|by-nc-sa|by-nc|by-nd|by-sa|by|zero)/([1-9]\.[0-9])')
TEXT_LICENSE_REGEX = re.compile(r'(cc|creative commons) (by-nc-nd|by-nc-sa|by-nc|by-nd|by-sa|by|zero) ?([1-9]\.[0-9])?', re.I)

METANAME_AUTHOR = {
    'article:author', 'atc-metaauthor', 'author', 'authors', 'byl', 'citation_author',
    'creator', 'dc.creator', 'dc.creator.aut', 'dc:creator',
    'dcterms.creator', 'dcterms.creator.aut', 'dcsext.author', 'parsely-author',
    'rbauthors', 'sailthru.author', 'shareaholic:article_author_name'
}  # questionable: twitter:creator
METANAME_DESCRIPTION = {
    'dc.description', 'dc:description',
    'dcterms.abstract', 'dcterms.description',
    'description', 'sailthru.description', 'twitter:description'
}
METANAME_PUBLISHER = {
    'article:publisher', 'citation_journal_title', 'copyright',
    'dc.publisher', 'dc:publisher', 'dcterms.publisher',
    'publisher', 'sailthru.publisher', 'rbpubname', 'twitter:site'
}  # questionable: citation_publisher
METANAME_TAG = {
    'citation_keywords', 'dcterms.subject', 'keywords', 'parsely-tags',
    'shareaholic:keywords', 'tags'
}
METANAME_TITLE = {
    'citation_title', 'dc.title', 'dcterms.title', 'fb_title',
    'headline', 'parsely-title', 'sailthru.title', 'shareaholic:title',
    'rbtitle', 'title', 'twitter:title'
}
METANAME_URL = {
    'rbmainurl', 'twitter:url'
}
METANAME_IMAGE = {
    'image', 'og:image', 'og:image:url', 'og:image:secure_url',
    'twitter:image', 'twitter:image:src'
}
OG_AUTHOR = {'og:author', 'og:article:author'}
PROPERTY_AUTHOR = {'author', 'article:author'}
TWITTER_ATTRS = {'twitter:site', 'application-name'}

# also interesting: article:section

EXTRA_META = {'charset', 'http-equiv', 'property'}


def check_authors(authors, author_blacklist):
    "Check if the authors string correspond to expected values."
    author_blacklist = {a.lower() for a in author_blacklist}
    new_authors = [
        author.strip()
        for author in authors.split(';')
        if author.strip().lower() not in author_blacklist
    ]
    if new_authors:
        return '; '.join(new_authors).strip('; ')
    return None


def extract_meta_json(tree, metadata):
    '''Parse and extract metadata from JSON-LD data'''
    for elem in tree.xpath('.//script[@type="application/ld+json" or @type="application/settings+json"]'):
        if not elem.text:
            continue
        element_text = normalize_json(JSON_MINIFY.sub(r'\1', elem.text))
        try:
            schema = json.loads(element_text)
            metadata = extract_json(schema, metadata)
        except json.JSONDecodeError:
            metadata = extract_json_parse_error(element_text, metadata)
    return metadata


def extract_opengraph(tree):
    '''Search meta tags following the OpenGraph guidelines (https://ogp.me/)'''
    title, author, url, description, site_name, image, pagetype = (None,) * 7
    # detect OpenGraph schema
    for elem in tree.xpath('.//head/meta[starts-with(@property, "og:")]'):
        # safeguard
        if not elem.get('content') or elem.get('content').isspace():
            continue
        # site name
        if elem.get('property') == 'og:site_name':
            site_name = elem.get('content')
        # blog title
        elif elem.get('property') == 'og:title':
            title = elem.get('content')
        # orig URL
        elif elem.get('property') == 'og:url':
            if is_valid_url(elem.get('content')):
                url = elem.get('content')
        # description
        elif elem.get('property') == 'og:description':
            description = elem.get('content')
        # og:author
        elif elem.get('property') in OG_AUTHOR:
            author = normalize_authors(None, elem.get('content'))
        # image default
        elif elem.get('property') == 'og:image':
            image = elem.get('content')
        # image url
        elif elem.get('property') == 'og:image:url':
            image = elem.get('content')
        # image secure url
        elif elem.get('property') == 'og:image:secure_url':
            image = elem.get('content')
        # og:type
        elif elem.get('property') == 'og:type':
            pagetype = elem.get('content')
        # og:locale
        # elif elem.get('property') == 'og:locale':
        #    pagelocale = elem.get('content')
    return title, author, url, description, site_name, image, pagetype


def examine_meta(tree):
    '''Search meta tags for relevant information'''
    metadata = Document()  # alt: Metadata()
    # bootstrap from potential OpenGraph tags
    title, author, url, description, site_name, image, pagetype = extract_opengraph(tree)
    # test if all values not assigned in the following have already been assigned
    if all((title, author, url, description, site_name, image)):
        metadata.set_attributes(title, author, url, description, site_name, image, pagetype, None)  # tags
        return metadata
    tags, backup_sitename = [], None
    # skim through meta tags
    for elem in tree.iterfind('.//head/meta[@content]'):
        # content
        if not elem.get('content') or elem.get('content').isspace():
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
                tags.append(normalize_tags(content_attr))
            elif elem.get('property') in PROPERTY_AUTHOR:
                author = normalize_authors(author, content_attr)
            elif elem.get('property') == 'article:publisher':
                site_name = site_name or content_attr
            elif elem.get('property') in METANAME_IMAGE:
                image = image or content_attr
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
            # twitter
            elif name_attr in TWITTER_ATTRS or 'twitter:app:name' in elem.get('name'):
                backup_sitename = content_attr
            # url
            elif name_attr == 'twitter:url':
                if url is None and is_valid_url(content_attr):
                    url = content_attr
            # keywords
            elif name_attr in METANAME_TAG:  # 'page-topic'
                tags.append(normalize_tags(content_attr))
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
        elif all(
            key not in elem.attrib
            for key in EXTRA_META
        ):
            LOGGER.debug('unknown attribute: %s',
                         tostring(elem, pretty_print=False, encoding='unicode').strip())
    # backups
    if site_name is None and backup_sitename is not None:
        site_name = backup_sitename
    # copy
    metadata.set_attributes(title, author, url, description, site_name, image, pagetype, tags)
    return metadata


def extract_metainfo(tree, expressions, len_limit=200):
    '''Extract meta information'''
    # try all XPath expressions
    for expression in expressions:
        # examine all results
        i = 0
        for elem in expression(tree):
            content = trim(' '.join(elem.itertext()))
            if content and 2 < len(content) < len_limit:
                return content
            i += 1
        if i > 1:
            LOGGER.debug('more than one invalid result: %s %s', expression, i)
    return None


def examine_title_element(tree):
    '''Extract text segments out of main <title> element.'''
    title, first, second = None, None, None
    try:
        title = trim(tree.xpath('.//head//title')[0].text_content())
        mymatch = HTMLTITLE_REGEX.match(title)
        if mymatch is not None:
            first = mymatch[1] or None
            second = mymatch[2] or None
    except IndexError:
        LOGGER.debug('no main title found')
    return title, first, second


def extract_title(tree):
    '''Extract the document title'''
    # only one h1-element: take it
    h1_results = tree.findall('.//h1')
    if len(h1_results) == 1:
        title = trim(h1_results[0].text_content())
        if len(title) > 0:
            return title
    # extract using x-paths
    title = extract_metainfo(tree, TITLE_XPATHS)
    if title is not None:
        return title
    # extract using title tag
    title, first, second = examine_title_element(tree)
    if first is not None and '.' not in first:
        return first
    if second is not None and '.' not in second:
        return second
    # take first h1-title
    if h1_results:
        return h1_results[0].text_content()
    # take first h2-title
    try:
        title = tree.xpath('.//h2')[0].text_content()
    except IndexError:
        LOGGER.debug('no h2 title found')
    return title


def extract_author(tree):
    '''Extract the document author(s)'''
    subtree = prune_unwanted_nodes(deepcopy(tree), AUTHOR_DISCARD_XPATHS)
    author = extract_metainfo(subtree, AUTHOR_XPATHS, len_limit=120)
    if author:
        author = normalize_authors(None, author)
    # copyright?
    return author


def extract_url(tree, default_url=None):
    '''Extract the URL from the canonical link'''
    url = None
    # https://www.tutorialrepublic.com/html-reference/html-base-tag.php
    # try canonical link first
    element = tree.find('.//head//link[@rel="canonical"][@href]')
    if element is not None:
        url = element.attrib['href']
    # try default language link
    else:
        for element in tree.iterfind('.//head//link[@rel="alternate"][@hreflang]'):
            if element.attrib['hreflang'] == 'x-default':
                LOGGER.debug(tostring(element, pretty_print=False, encoding='unicode').strip())
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
                base_url = get_base_url(element.attrib['content'])
                if base_url:
                    # prepend URL
                    url = base_url + url
                    break
    # sanity check: don't return invalid URLs
    if url is not None:
        validation_result, parsed_url = validate_url(url)
        url = None if validation_result is False else normalize_url(parsed_url)
    return url or default_url


def extract_sitename(tree):
    '''Extract the name of a site from the main title (if it exists)'''
    _, first, second = examine_title_element(tree)
    if first is not None and '.' in first:
        return first
    if second is not None and '.' in second:
        return second
    return None


def extract_catstags(metatype, tree):
    '''Find category and tag information'''
    results = []
    regexpr = '/' + metatype + '[s|ies]?/'
    xpath_expression = CATEGORIES_XPATHS if metatype == 'category' else TAGS_XPATHS
    # search using custom expressions
    for catexpr in xpath_expression:
        results.extend(
            elem.text_content()
            for elem in catexpr(tree)
            if re.search(regexpr, elem.attrib['href'])
        )
        if results:
            break
    # category fallback
    if metatype == 'category' and not results:
        for element in tree.xpath('.//head//meta[@property="article:section" or contains(@name, "subject")][@content]'):
            results.append(element.attrib['content'])
        # optional: search through links
        #if not results:
        #    for elem in tree.xpath('.//a[@href]'):
        #        search for 'category'
    return [r for r in dict.fromkeys(line_processing(x) for x in results if x) if r]


def parse_license_element(element, strict=False):
    '''Probe a link for identifiable free license cues.
       Parse the href attribute first and then the link text.'''
   # look for Creative Commons elements
    match = LICENSE_REGEX.search(element.get('href'))
    if match:
        return 'CC ' + match[1].upper() + ' ' + match[2]
    if element.text is not None:
        # just return the anchor text without further ado
        if strict is False:
            return trim(element.text)
        # else: check if it could be a CC license
        match = TEXT_LICENSE_REGEX.search(element.text)
        if match:
            return match[0]
    return None


def extract_license(tree):
    '''Search the HTML code for license information and parse it.'''
    result = None
    # look for links labeled as license
    for element in tree.findall('.//a[@rel="license"][@href]'):
        result = parse_license_element(element, strict=False)
        if result is not None:
            break
    # probe footer elements for CC links
    if result is None:
        for element in tree.xpath(
            './/footer//a[@href]|.//div[contains(@class, "footer") or contains(@id, "footer")]//a[@href]'
        ):
            result = parse_license_element(element, strict=True)
            if result is not None:
                break
    return result


def extract_image(tree):
    '''Search meta tags following the OpenGraph guidelines (https://ogp.me/)
       and search meta tags with Twitter Image'''

    for elem in tree.xpath('.//head/meta[@property="og:image" or @property="og:image:url"][@content]'):
        return elem.get('content')

    for elem in tree.xpath('.//head/meta[@property="twitter:image" or @property="twitter:image:src"][@content]'):
        return elem.get('content')

    return None


def extract_metadata(filecontent, default_url=None, date_config=None, extensive=True, author_blacklist=None):
    """Main process for metadata extraction.

    Args:
        filecontent: HTML code as string.
        default_url: Previously known URL of the downloaded document.
        date_config: Provide extraction parameters to htmldate as dict().
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.

    Returns:
        A trafilatura.metadata.Document containing the extracted metadata information or None.
        trafilatura.metadata.Document has .as_dict() method that will return a copy as a dict.
    """
    # init
    if author_blacklist is None:
        author_blacklist = set()
    if not date_config:
        date_config = set_date_params(extensive)
    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return None
    # initialize dict and try to strip meta tags
    metadata = examine_meta(tree)
    # to check: remove it and replace with author_blacklist in test case
    if metadata.author is not None and ' ' not in metadata.author:
        metadata.author = None
    # fix: try json-ld metadata and override
    try:
        metadata = extract_meta_json(tree, metadata)
    # todo: fix bugs in json_metadata.py
    except TypeError as err:
        LOGGER.warning('error in JSON metadata extraction: %s', err)
    # title
    if metadata.title is None:
        metadata.title = extract_title(tree)
    # check author in blacklist
    if metadata.author is not None and len(author_blacklist) > 0:
        metadata.author = check_authors(metadata.author, author_blacklist)
    # author
    if metadata.author is None:
        metadata.author = extract_author(tree)
    # recheck author in blacklist
    if metadata.author is not None and len(author_blacklist) > 0:
        metadata.author = check_authors(metadata.author, author_blacklist)
    # url
    if metadata.url is None:
        metadata.url = extract_url(tree, default_url)
    # hostname
    if metadata.url is not None:
        metadata.hostname = extract_domain(metadata.url, fast=True)
    # image
    if metadata.image is None:
        metadata.image = extract_image(tree)
    # extract date with external module htmldate
    date_config['url'] = metadata.url
    metadata.date = find_date(tree, **date_config)
    # sitename
    if metadata.sitename is None:
        metadata.sitename = extract_sitename(tree)
    if metadata.sitename is not None:
        # fix: take 1st element (['Westdeutscher Rundfunk'])
        if isinstance(metadata.sitename, list):
            metadata.sitename = metadata.sitename[0]
        # hotfix: probably an error coming from json_metadata (#195)
        elif isinstance(metadata.sitename, dict):
            metadata.sitename = str(metadata.sitename)
        if metadata.sitename.startswith('@'):
            # scrap Twitter ID
            metadata.sitename = re.sub(r'^@', '', metadata.sitename)
        # capitalize
        try:
            if (
                '.' not in metadata.sitename
                and not metadata.sitename[0].isupper()
            ):
                metadata.sitename = metadata.sitename.title()
        # fix for empty name
        except IndexError as err:
            LOGGER.warning('error in sitename extraction: %s', err)
    # use URL
    elif metadata.url:
        mymatch = re.match(r'https?://(?:www\.|w[0-9]+\.)?([^/]+)', metadata.url)
        if mymatch:
            metadata.sitename = mymatch[1]
    # categories
    if not metadata.categories:
        metadata.categories = extract_catstags('category', tree)
    # tags
    if not metadata.tags:
        metadata.tags = extract_catstags('tag', tree)
    # license
    metadata.license = extract_license(tree)
    # safety checks
    metadata.filedate = date_config["max_date"]
    metadata.clean_and_trim()
    # return result
    return metadata
