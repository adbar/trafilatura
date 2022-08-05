"""
Deriving link info from sitemaps.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import logging
import re
# import urllib.robotparser # Python >= 3.8
# ROBOT_PARSER = urllib.robotparser.RobotFileParser()

from courlan import clean_url, extract_domain, filter_urls, fix_relative_urls, get_hostinfo, lang_filter

from .downloads import fetch_url
from .settings import MAX_SITEMAPS_SEEN


LOGGER = logging.getLogger(__name__)

LINK_REGEX = re.compile(r'<loc>(?:<!\[CDATA\[)?(http.+?)(?:\]\]>)?</loc>')
XHTML_REGEX = re.compile(r'<xhtml:link.+?>', re.DOTALL)
HREFLANG_REGEX = re.compile(r'href=["\'](.+?)["\']')
WHITELISTED_PLATFORMS = re.compile(r'(?:blogger|blogpost|ghost|hubspot|livejournal|medium|typepad|squarespace|tumblr|weebly|wix|wordpress)\.')

SITEMAP_FORMAT = re.compile(r'<\?xml|<sitemap|<urlset')
DETECT_SITEMAP_LINK = re.compile(r'\.xml(\..{2,4})?$|\.xml[?#]')
DETECT_LINKS = re.compile(r'https?://[^\s\r\n]+')
SCRUB_REGEX = re.compile(r'\?.*$|#.*$')
POTENTIAL_SITEMAP = re.compile(r'\.xml\b')

GUESSES = ['sitemap.xml.gz', 'sitemap', 'sitemap_index.xml', 'sitemap_news.xml']


def sitemap_search(url, target_lang=None):
    """Look for sitemaps for the given URL and gather links.

    Args:
        url: Webpage or sitemap URL as string.
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
    # determine sitemap URL
    if url.endswith('.xml') or url.endswith('.gz') or url.endswith('sitemap'):
        sitemapurl = url
    else:
        sitemapurl = baseurl + '/sitemap.xml'
        # filter triggered, prepare it
        if len(url) > len(baseurl) + 2:
            urlfilter = url
    sitemapurls, linklist = download_and_process_sitemap(sitemapurl, domainname, baseurl, target_lang)
    sitemaps_seen = {sitemapurl}
    if sitemapurls == [] and len(linklist) > 0:
        linklist = filter_urls(linklist, urlfilter)
        LOGGER.debug('%s sitemap links found for %s', len(linklist), domainname)
        return linklist
    # try sitemaps in robots.txt file if nothing has been found
    if sitemapurls == [] and linklist == []:
        sitemapurls = find_robots_sitemaps(baseurl)
        # try additional URLs just in case
        if not sitemapurls:
            sitemapurls = [''.join([baseurl, '/', g]) for g in GUESSES]
    # iterate through nested sitemaps and results
    i = 1
    while sitemapurls:
        sitemapurl = sitemapurls.pop()
        sitemapurls, linklist = download_and_process_sitemap(sitemapurl, domainname, baseurl, target_lang, sitemapurls, linklist)
        # sanity check: keep track of visited sitemaps and exclude them
        sitemaps_seen.add(sitemapurl)
        sitemapurls = [s for s in sitemapurls if s not in sitemaps_seen]
        # counter and safeguard
        i += 1
        if i > MAX_SITEMAPS_SEEN:
            break
    linklist = filter_urls(linklist, urlfilter)
    LOGGER.debug('%s sitemap links found for %s', len(linklist), domainname)
    return linklist


def check_sitemap(url, contents):
    '''Check if the sitemap corresponds to an expected format,
       i.e. TXT or XML.'''
    if contents is not None:
        # strip query and fragments
        url = SCRUB_REGEX.sub('', url)
        if POTENTIAL_SITEMAP.search(url) and \
            (not isinstance(contents, str) or not SITEMAP_FORMAT.match(contents)) \
             or '<html' in contents[:150].lower():
            LOGGER.info('not a valid XML sitemap: %s', url)
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
        LOGGER.debug('not a sitemap: %s', url) # respheaders
        return [], []
    # try to extract links from TXT file
    if not SITEMAP_FORMAT.match(contents):
        sitemapurls, linklist = [], []
        for match in DETECT_LINKS.finditer(contents):
            result = match[0]
            link, state = handle_link(result, url, domain, baseurl, target_lang)
            sitemapurls, linklist = store_sitemap_link(sitemapurls, linklist, link, state)
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
    link = clean_url(link, target_lang)
    if link is not None and lang_filter(link, target_lang) is True:
        newdomain = extract_domain(link, fast=True)
        if newdomain is None:
            LOGGER.error("Couldn't extract domain: %s", link)
        # don't take links from another domain and make an exception for main platforms
        # also bypass: subdomains vs. domains
        elif newdomain != domainname and not newdomain in domainname and not WHITELISTED_PLATFORMS.search(newdomain):
            LOGGER.warning('Diverging domain names: %s %s', domainname, newdomain)
        else:
            state = 'sitemap' if DETECT_SITEMAP_LINK.search(link) else 'link'
    return link, state


def store_sitemap_link(sitemapurls, linklist, link, state):
    '''Process link according to filtered result: discard it or store it
       in the appropriate list.'''
    if state == 'sitemap' and link is not None:
        sitemapurls.append(link)
    elif state == 'link' and link is not None:
        linklist.append(link)
    return sitemapurls, linklist


def extract_sitemap_langlinks(pagecontent, sitemapurl, domainname, baseurl, target_lang):
    'Extract links corresponding to a given target language.'
    if 'hreflang=' not in pagecontent:
        return [], []
    sitemapurls, linklist = [], []
    # compile regex here for modularity and efficiency
    lang_regex = re.compile(r"hreflang=[\"']({}.*?|x-default)[\"']".format(target_lang), re.DOTALL)
    for attr_match in XHTML_REGEX.finditer(pagecontent):
        attributes = attr_match[0]
        if lang_regex.search(attributes):
            lang_match = HREFLANG_REGEX.search(attributes)
            if lang_match:
                link, state = handle_link(lang_match[1], sitemapurl, domainname, baseurl, target_lang)
                sitemapurls, linklist = store_sitemap_link(sitemapurls, linklist, link, state)
    LOGGER.debug('%s sitemaps and %s links with hreflang found for %s', len(sitemapurls), len(linklist), sitemapurl)
    return sitemapurls, linklist


def extract_sitemap_links(pagecontent, sitemapurl, domainname, baseurl, target_lang):
    'Extract sitemap links and web page links from a sitemap file.'
    sitemapurls, linklist = [], []
    # extract
    for match in LINK_REGEX.finditer(pagecontent):
        # process middle part of the match tuple
        link, state = handle_link(match[1], sitemapurl, domainname, baseurl, target_lang)
        sitemapurls, linklist = store_sitemap_link(sitemapurls, linklist, link, state)
    LOGGER.debug('%s sitemaps and %s links found for %s', len(sitemapurls), len(linklist), sitemapurl)
    return sitemapurls, linklist


def find_robots_sitemaps(baseurl):
    '''Guess the location of the robots.txt file and try to extract
       sitemap URLs from it'''
    robotstxt = fetch_url(baseurl + '/robots.txt')
    return extract_robots_sitemaps(robotstxt, baseurl)


def extract_robots_sitemaps(robotstxt, baseurl):
    'Read a robots.txt file and find sitemap links.'
    # sanity check on length (cause: redirections)
    if robotstxt is None or len(robotstxt) > 10000:
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
