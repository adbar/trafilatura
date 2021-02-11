"""
Examining feeds and extracting links for further processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re

from courlan import check_url, clean_url, extract_domain, validate_url

from .utils import load_html, fetch_url, fix_relative_urls, HOSTINFO

LOGGER = logging.getLogger(__name__)

FEED_TYPES = set(['application/rss+xml', 'application/atom+xml', 'application/x.atom+xml', 'application/x-atom+xml', 'text/xml'])


def handle_link_list(linklist, domainname, baseurl, target_lang=None):
    '''Examine links to determine if they are valid and
       lead to a web page'''
    output_links = []
    # sort and uniq
    for item in sorted(list(set(linklist))):
        # fix and check
        link = fix_relative_urls(baseurl, item)
        # control output for validity
        checked = check_url(link, language=target_lang)
        if checked is not None:
            output_links.append(checked[0])
            if checked[1] != domainname:
                LOGGER.warning('Diverging domain names: %s %s', domainname, checked[1])
    return output_links


def extract_links(feed_string, domainname, baseurl, reference, target_lang=None):
    '''Extract links from Atom and RSS feeds'''
    feed_links = []
    # check if it's a feed
    if feed_string is None:
        return feed_links
    feed_string = feed_string.strip()
    if not re.match(r'<\?xml|<feed|<rss', feed_string):
        return feed_links
    # could be Atom
    if '<link ' in feed_string:
        for link in re.findall(r'<link .*?href=".+?"', feed_string):
            if 'atom+xml' in link or 'rel="self"' in link:
                continue
            mymatch = re.search(r'<link .*?href="(.+?)"', link)
            if mymatch:
                feedlink = mymatch.group(1)
                if '"' in feedlink:
                    feedlink = feedlink.split('"')[0]
                feed_links.append(feedlink)
    # could be RSS
    elif '<link>' in feed_string:
        for item in re.findall(r'<link>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</link>', feed_string):
            feed_links.append(item)
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
        return []
    feed_urls = []
    for linkelem in tree.xpath('//link[@rel="alternate"]'):
        # discard elements without links
        if not 'href' in linkelem.attrib:
            continue
        # most common case
        if 'type' in linkelem.attrib and linkelem.get('type') in FEED_TYPES:
            feed_urls.append(linkelem.get('href'))
        # websites like geo.de
        elif 'atom' in linkelem.get('href') or 'rss' in linkelem.get('href'):
            feed_urls.append(linkelem.get('href'))
    # backup
    if len(feed_urls) == 0:
        for linkelem in tree.xpath('//a[@href]'):
            if linkelem.get('href')[-4:].lower() in ('.rss', '.rdf', '.xml', '.atom'):
                feed_urls.append(linkelem.get('href'))
            elif 'atom' in linkelem.get('href') or 'rss' in linkelem.get('href'):
                feed_urls.append(linkelem.get('href'))
    # refine
    output_urls = []
    for link in sorted(set(feed_urls)):
        link = fix_relative_urls(baseurl, link)
        link = clean_url(link)
        if link == reference or validate_url(link)[0] is False:
            continue
        if re.search(r'\bcomments\b', link): # no comment feed
            continue
        output_urls.append(link)
    # log result
    LOGGER.debug('Feed URLs found: %s of which %s valid', len(feed_urls), len(output_urls))
    return output_urls


def find_feed_urls(url, target_lang=None):
    """Try to find feed URLs.

    Args:
        url: Homepage or feed URL as string.
        target_lang: Define a language to filter URLs based on heuristics
            (two-letter string, ISO 639-1 format).

    Returns:
        The extracted links as list (sorted list of unique links).

    """
    url = url.rstrip('/')
    domainname, hostmatch = extract_domain(url), HOSTINFO.match(url)
    if domainname is None or hostmatch is None:
        LOGGER.warning('Invalid URL: %s', url)
        return []
    baseurl = hostmatch.group(0)
    downloaded = fetch_url(url)
    if downloaded is not None:
        # assume it's a feed
        feed_links = extract_links(downloaded, domainname, baseurl, url, target_lang)
        if len(feed_links) == 0:
            # assume it's a web page
            for feed in determine_feed(downloaded, baseurl, url):
                feed_string = fetch_url(feed)
                feed_links.extend(extract_links(feed_string, domainname, baseurl, url, target_lang))
        # return links found
        if len(feed_links) > 0:
            feed_links = sorted(list(set(feed_links)))
            LOGGER.debug('%s feed links found for %s', len(feed_links), domainname)
            return feed_links
    else:
        LOGGER.warning('Could not download web page: %s', url)
    # try alternative: Google News
    if target_lang is not None:
        url = 'https://news.google.com/rss/search?q=site:' + baseurl + '&hl=' + target_lang + '&scoring=n&num=100'
        downloaded = fetch_url(url)
        if downloaded is not None:
            feed_links = extract_links(downloaded, domainname, baseurl, url, target_lang)
            LOGGER.debug('%s feed links found for %s', len(feed_links), domainname)
            return feed_links
        LOGGER.warning('Could not download web page: %s', url)
    return []
