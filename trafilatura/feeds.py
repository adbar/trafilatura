"""
Examining feeds and extracting links for further processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re

from .utils import fetch_url

LOGGER = logging.getLogger(__name__)


def validate_url(url):
    '''Superficially check if a given URL could be valid'''
    if re.match(r'https?://[^/]+/.+$', url):
        return True
    return False


def extract_links(feed):
    '''Extract links from Atom and RSS feeds'''
    links = list()
    # could be Atom
    if '<link ' in feed:
        for item in re.findall(r'<link .*?href="(.+?)"', feed):
            links.append(item)
    # could be RSS
    elif '<link>' in feed:
        for item in re.findall(r'<link>(.+?)</link>', feed):
            links.append(item)
    else:
        return links
    # control output for validity
    for item in links:
        if validate_url(item) is False:
            links.remove(item)
    return links


def fetch_feed(feed_url):
    '''Download and superficially parse a feed URL'''
    feed_download = fetch_url(feed_url)
    if feed_download is not None:
        feed_links = extract_links(feed_download)
        if len(feed_links) > 0:
            return feed_links
    LOGGER.debug('Does not seem to be a valid feed')
    return None
