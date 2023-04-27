"""
Examining feeds and extracting links for further processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import json
import re

from courlan import check_url, clean_url, filter_urls, fix_relative_urls, get_hostinfo, validate_url

from .downloads import fetch_url
from .utils import is_similar_domain, load_html


LOGGER = logging.getLogger(__name__)

FEED_TYPES = {'application/atom+xml', 'application/json', 'application/rdf+xml', 'application/rss+xml', 'application/x.atom+xml', 'application/x-atom+xml', 'text/atom+xml', 'text/plain', 'text/rdf+xml', 'text/rss+xml', 'text/xml'}
FEED_OPENING = re.compile(r'<(feed|rss|\?xml)')
LINK_ATTRS = re.compile(r'<link .*?href=".+?"')
LINK_HREF = re.compile(r'href="(.+?)"')
LINK_ELEMENTS = re.compile(r'<link>(?:\s*)(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?(?:\s*)</link>')
BLACKLIST = re.compile(r'\bcomments\b')  # no comment feed


def handle_link_list(linklist, domainname, baseurl, target_lang=None):
    '''Examine links to determine if they are valid and
       lead to a web page'''
    output_links = []
    # sort and uniq
    for item in sorted(set(linklist)):
        # fix and check
        link = fix_relative_urls(baseurl, item)
        # control output for validity
        checked = check_url(link, language=target_lang)
        if checked is not None:
            if not is_similar_domain(domainname, checked[1]) and not "feed" in link:
                LOGGER.error('Rejected, diverging domain names: %s %s', domainname, checked[1])
            else:
                output_links.append(checked[0])
        # Feedburner/Google feeds
        elif 'feedburner' in item or 'feedproxy' in item:
            output_links.append(item)
    return output_links


def extract_links(feed_string, domainname, baseurl, reference, target_lang=None):
    '''Extract links from Atom and RSS feeds'''
    feed_links = []
    # check if it's a feed
    if feed_string is None:
        LOGGER.debug('Empty feed: %s', domainname)
        return feed_links
    feed_string = feed_string.strip()
    # typical first and second lines absent
    if not FEED_OPENING.match(feed_string) and not \
        ('<rss' in feed_string[:100] or '<feed' in feed_string[:100]):
        # could be JSON
        if feed_string.startswith('{'):
            try:
                feed_dict = json.loads(feed_string)
                if 'items' in feed_dict:
                    for item in feed_dict['items']:
                        if 'url' in item:
                            feed_links.append(item['url'])
                        # fallback: https://www.jsonfeed.org/version/1.1/
                        elif 'id' in item:
                            feed_links.append(item['id'])
            except json.decoder.JSONDecodeError:
                LOGGER.debug('JSON decoding error: %s', domainname)
        else:
            LOGGER.debug('Possibly invalid feed: %s', domainname)
        return feed_links
    # could be Atom
    if '<link ' in feed_string:
        for match in LINK_ATTRS.finditer(feed_string):
            link = match[0]
            if 'atom+xml' in link or 'rel="self"' in link:
                continue
            feedlink = LINK_HREF.search(link)[1]
            #if '"' in feedlink:
            #    feedlink = feedlink.split('"')[0]
            feed_links.append(feedlink)
    # could be RSS
    elif '<link>' in feed_string:
        feed_links.extend(
            match[1].strip()
            for match in LINK_ELEMENTS.finditer(feed_string, re.DOTALL)
        )

    # refine
    output_links = handle_link_list(feed_links, domainname, baseurl, target_lang)
    output_links = [l for l in output_links if l != reference and l.count('/') > 2]
    # log result
    if feed_links:
        LOGGER.debug('Links found: %s of which %s valid', len(feed_links), len(output_links))
    else:
        LOGGER.debug('Invalid feed for %s', domainname)
    return output_links


def determine_feed(htmlstring, baseurl, reference):
    '''Try to extract the feed URL from the home page.
       Adapted from http://www.aaronsw.com/2002/feedfinder/'''
    # parse the page to look for feeds
    tree = load_html(htmlstring)
    # safeguard
    if tree is None:
        LOGGER.debug('Invalid HTML/Feed page: %s', baseurl)
        return []
    feed_urls = []
    for linkelem in tree.xpath('//link[@rel="alternate"]'):
        # discard elements without links
        if 'href' not in linkelem.attrib:
            continue
        # most common case
        if 'type' in linkelem.attrib and linkelem.get('type') in FEED_TYPES:
            feed_urls.append(linkelem.get('href'))
        # websites like geo.de
        elif 'atom' in linkelem.get('href') or 'rss' in linkelem.get('href'):
            feed_urls.append(linkelem.get('href'))
    # backup
    if not feed_urls:
        for linkelem in tree.xpath('//a[@href]'):
            if linkelem.get('href')[-4:].lower() in ('.rss', '.rdf', '.xml'):
                feed_urls.append(linkelem.get('href'))
            elif linkelem.get('href')[-5:].lower() == '.atom':
                feed_urls.append(linkelem.get('href'))
            elif 'atom' in linkelem.get('href') or 'rss' in linkelem.get('href'):
                feed_urls.append(linkelem.get('href'))
    # refine
    output_urls = []
    for link in sorted(set(feed_urls)):
        link = fix_relative_urls(baseurl, link)
        link = clean_url(link)
        if link is None or link == reference or validate_url(link)[0] is False:
            continue
        if BLACKLIST.search(link):
            continue
        output_urls.append(link)
    # log result
    LOGGER.debug('Feed URLs found: %s of which %s valid', len(feed_urls), len(output_urls))
    return output_urls


def find_feed_urls(url, target_lang=None):
    """Try to find feed URLs.

    Args:
        url: Webpage or feed URL as string.
             Triggers URL-based filter if the webpage isn't a homepage.
        target_lang: Define a language to filter URLs based on heuristics
             (two-letter string, ISO 639-1 format).

    Returns:
        The extracted links as a list (sorted list of unique links).

    """
    domainname, baseurl = get_hostinfo(url)
    if domainname is None:
        LOGGER.warning('Invalid URL: %s', url)
        return []
    urlfilter = None
    downloaded = fetch_url(url)
    if downloaded is not None:
        # assume it's a feed
        feed_links = extract_links(downloaded, domainname, baseurl, url, target_lang)
        if len(feed_links) == 0:
            # assume it's a web page
            for feed in determine_feed(downloaded, baseurl, url):
                feed_string = fetch_url(feed)
                feed_links.extend(extract_links(feed_string, domainname, baseurl, url, target_lang))
            # filter triggered, prepare it
            if len(url) > len(baseurl) + 2:
                urlfilter = url
        # return links found
        if len(feed_links) > 0:
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug('%s feed links found for %s', len(feed_links), domainname)
            return feed_links
        LOGGER.debug('No usable feed links found: %s', url)
    else:
        LOGGER.warning('Could not download web page: %s', url)
        if url.strip('/') != baseurl:
            return try_homepage(baseurl, target_lang)
    # try alternative: Google News
    if target_lang is not None:
        downloaded = fetch_url(
            f'https://news.google.com/rss/search?q=site:{baseurl}&hl={target_lang}&scoring=n&num=100'
        )
        if downloaded is not None:
            feed_links = extract_links(downloaded, domainname, baseurl, url, target_lang)
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug('%s Google news links found for %s', len(feed_links), domainname)
            return feed_links
    return []


def try_homepage(baseurl, target_lang):
    '''Shift into reverse and try the homepage instead of the particular feed
       page that was given as input.'''
    LOGGER.info('Probing homepage for feeds instead: %s', baseurl)
    return find_feed_urls(baseurl, target_lang)
