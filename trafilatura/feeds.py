"""
Examining feeds and extracting links for further processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re

from courlan import check_url, clean_url, extract_domain, validate_url

from .utils import fetch_url, fix_relative_urls, HOSTINFO

LOGGER = logging.getLogger(__name__)


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
    if not feed_string.startswith('<?xml') or \
        feed_string.startswith('<feed') or feed_string.startswith('<rss'):
        return feed_links
    # could be Atom
    if '<link ' in feed_string:
        for link in re.findall(r'<link .*?href=".+?"', feed_string):
            if 'atom+xml' in link or 'rel="self"' in link:
                continue
            mymatch = re.search(r'<link .*?href="(.+?)"', link)
            if mymatch:
                feed_links.append(mymatch.group(1))
    # could be RSS
    elif '<link>' in feed_string:
        for item in re.findall(r'<link>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</link>', feed_string):
            feed_links.append(item)
    # refine
    output_links = handle_link_list(feed_links, domainname, baseurl, target_lang)
    output_links = [l for l in output_links if l != reference]
    # log result
    if feed_links:
        LOGGER.debug('Links found: %s of which %s valid', len(feed_links), len(output_links))
    else:
        LOGGER.debug('Invalid feed for %s', domainname)
    return output_links


def determine_feed(htmlstring, baseurl, reference):
    '''Try to extract the feed URL from the home page'''
    feed_urls = []
    # try to find RSS URL
    for feed_url in re.findall(r'<link[^<>]+?type="application/rss\+xml"[^<>]+?href="(.+?)"', htmlstring):
        feed_urls.append(feed_url)
    for feed_url in re.findall(r'<link[^<>]+?href="(.+?)"[^<>]+?type="application/rss\+xml"', htmlstring):
        feed_urls.append(feed_url)
    # try to find Atom URL
    if len(feed_urls) == 0:
        for feed_url in re.findall(r'<link[^<>]+?type="application/atom\+xml"[^<>]+?href="(.+?)"', htmlstring):
            feed_urls.append(feed_url)
        for feed_url in re.findall(r'<link[^<>]+?href="(.+?)"[^<>]+?type="application/atom\+xml"', htmlstring):
            feed_urls.append(feed_url)
    # refine
    output_urls = []
    for link in sorted(list(set(feed_urls))):
        link = fix_relative_urls(baseurl, link)
        link = clean_url(link)
        if link == reference or validate_url(link)[0] is False:
            continue
        if 'comments' in link:
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
