"""
Deriving link info from sitemaps.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re
# import urllib.robotparser # Python >= 3.8
# ROBOT_PARSER = urllib.robotparser.RobotFileParser()

from courlan import clean_url, extract_domain
from courlan.filters import lang_filter # next courlan version: usable directly

from .settings import MAX_SITEMAPS_SEEN
from .utils import fetch_url, fix_relative_urls, HOSTINFO


LOGGER = logging.getLogger(__name__)

LINK_REGEX = re.compile(r'(?<=<loc>)(?<=<!\[CDATA\[)?.+?(?=\]\]>|</loc>)')
XHTML_REGEX = re.compile(r'(?<=<xhtml:link).+?(?=/>)', re.DOTALL)
HREFLANG_REGEX = re.compile(r"(?<=href=[\"']).+?(?=[\"'])")
WHITELISTED_PLATFORMS = re.compile(r'(?:blogger|blogpost|ghost|hubspot|livejournal|medium|typepad|squarespace|tumblr|weebly|wix|wordpress)\.')


def sitemap_search(url, target_lang=None):
    """Look for sitemaps for the given URL and gather links.

    Args:
        url: Homepage or sitemap URL as string.
        target_lang: Define a language to filter URLs based on heuristics
            (two-letter string, ISO 639-1 format).

    Returns:
        The extracted links as list (sorted list of unique links).

    """
    domainname, hostmatch = extract_domain(url), HOSTINFO.match(url)
    if domainname is None or hostmatch is None:
        LOGGER.warning('Invalid URL: %s', url)
        return []
    baseurl = hostmatch.group(0)
    if url.endswith('.xml') or url.endswith('.gz') or url.endswith('sitemap'):
        sitemapurl = url
    else:
        sitemapurl = url.rstrip('/') + '/sitemap.xml'
    sitemapurls, linklist = download_and_process_sitemap(sitemapurl, domainname, baseurl, target_lang)
    if sitemapurls == [] and len(linklist) > 0:
        return linklist
    # try sitemaps in robots.txt file if nothing has been found
    if sitemapurls == [] and linklist == []:
        sitemapurls = find_robots_sitemaps(url, baseurl)
    # iterate through nested sitemaps and results
    i = 1
    while sitemapurls:
        sitemapurls, linklist = download_and_process_sitemap(sitemapurls.pop(), domainname, baseurl, target_lang, sitemapurls, linklist)
        # counter and safeguard
        i += 1
        if i > MAX_SITEMAPS_SEEN:
            break
    linklist = sorted(list(set(linklist)))
    LOGGER.debug('%s sitemap links found for %s', len(linklist), domainname)
    return linklist


def check_sitemap(url, contents):
    '''Check if the sitemap corresponds to an expected format,
       i.e. TXT or XML.'''
    if contents is not None:
        # strip query and fragments
        url = re.sub(r'\?.*$|#.*$', '', url)
        if re.search(r'\.xml\b', url) and \
            (not isinstance(contents, str) or not contents.startswith('<?xml')):
            logging.warning('not a valid XML sitemap: %s', url)
            return None
    return contents


def download_and_process_sitemap(url, domain, baseurl, target_lang, sitemapurls=None, linklist=None):
    'Helper function chaining download and processing of sitemaps.'
    # variables init
    sitemapurls, linklist = sitemapurls or [], linklist or []
    # fetch and pre-process
    LOGGER.info('fetching sitemap: %s', url)
    pagecontent = fetch_url(url)
    add_sitemaps, add_links = process_sitemap(url, domain, baseurl, pagecontent, target_lang)
    return sitemapurls + add_sitemaps, linklist + add_links


def process_sitemap(url, domain, baseurl, pagecontent, target_lang=None):
    'Download a sitemap and extract the links it contains.'
    contents = check_sitemap(url, pagecontent)
    # safeguard
    if contents is None:
        logging.warning('not a sitemap: %s', url) # respheaders
        return [], []
    # try to extract links from TXT file
    if not contents.startswith('<?xml'):
        sitemapurls, linklist = [], []
        for result in re.findall(r'https?://[^\s\r\n]+', contents):
            link, state = handle_link(result, url, domain, baseurl, target_lang)
            if state == 'sitemap':
                sitemapurls.append(link)
            elif state == 'link':
                linklist.append(link)
        return sitemapurls, linklist
    # process XML sitemap
    if target_lang is not None:
        sitemapurls, linklist = extract_sitemap_langlinks(contents, url, domain, baseurl, target_lang)
        if len(sitemapurls) != 0 or len(linklist) != 0:
            return sitemapurls, linklist
    return extract_sitemap_links(contents, url, domain, baseurl, target_lang)


def handle_link(link, sitemapurl, domainname, baseurl, target_lang):
    '''Examine a link and determine if it's valid and if it leads to
       a sitemap or a web page.'''
    state = '0'
    # safety net: recursivity
    if link == sitemapurl:
        return link, state
    # fix and check
    link = fix_relative_urls(baseurl, link)
    # clean and normalize
    link = clean_url(link) # next courlan version: clean_url(link, target_lang)
    if link is not None:
        if lang_filter(link, target_lang) is True:
            newdomain = extract_domain(link)
            # don't take links from another domain and make an exception for main platforms
            if newdomain != domainname and not WHITELISTED_PLATFORMS.search(newdomain):
                LOGGER.warning('Diverging domain names: %s %s', domainname, newdomain)
            else:
                if re.search(r'\.xml$|\.xml[.?#]', link):
                    state = 'sitemap'
                else:
                    state = 'link'
    return link, state


def extract_sitemap_langlinks(pagecontent, sitemapurl, domainname, baseurl, target_lang):
    'Extract links corresponding to a given target language.'
    if not 'hreflang=' in pagecontent:
        return [], []
    sitemapurls, linklist = [], []
    lang_regex = re.compile(r"hreflang=[\"']({}.*?|x-default)[\"']".format(target_lang), re.DOTALL)
    for attributes in XHTML_REGEX.findall(pagecontent):
        if lang_regex.search(attributes):
            match = HREFLANG_REGEX.search(attributes)
            if match:
                link, state = handle_link(match.group(0), sitemapurl, domainname, baseurl, target_lang)
                if state == 'sitemap':
                    sitemapurls.append(link)
                elif state == 'link':
                    linklist.append(link)
    LOGGER.debug('%s sitemaps and %s links with hreflang found for %s', len(sitemapurls), len(linklist), sitemapurl)
    return sitemapurls, linklist


def extract_sitemap_links(pagecontent, sitemapurl, domainname, baseurl, target_lang):
    'Extract sitemap links and web page links from a sitemap file.'
    sitemapurls, linklist = [], []
    # extract
    for link in LINK_REGEX.findall(pagecontent):
        link, state = handle_link(link, sitemapurl, domainname, baseurl, target_lang)
        if state == 'sitemap':
            sitemapurls.append(link)
        elif state == 'link':
            linklist.append(link)
    LOGGER.debug('%s sitemaps and %s links found for %s', len(sitemapurls), len(linklist), sitemapurl)
    return sitemapurls, linklist


def find_robots_sitemaps(url, baseurl):
    '''Guess the location of the robots.txt file and try to extract
       sitemap URLs from it'''
    robotsurl = url.rstrip('/') + '/robots.txt'
    robotstxt = fetch_url(robotsurl)
    if robotstxt is None:
        return []
    return extract_robots_sitemaps(robotstxt, baseurl)


def extract_robots_sitemaps(robotstxt, baseurl):
    'Read a robots.txt file and find sitemap links.'
    # sanity check on length (cause: redirections)
    if len(robotstxt) > 10000:
        return []
    sitemapurls = []
    # source: https://github.com/python/cpython/blob/3.8/Lib/urllib/robotparser.py
    for line in robotstxt.splitlines():
        # remove optional comment and strip line
        i = line.find('#')
        if i >= 0:
            line = line[:i]
        line = line.strip()
        if not line:
            continue
        line = line.split(':', 1)
        if len(line) == 2:
            line[0] = line[0].strip().lower()
            if line[0] == "sitemap":
                # urllib.parse.unquote(line[1].strip())
                candidate = fix_relative_urls(baseurl, line[1].strip())
                sitemapurls.append(candidate)
    LOGGER.debug('%s sitemaps found in robots.txt', len(sitemapurls))
    return sitemapurls
