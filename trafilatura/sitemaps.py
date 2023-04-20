"""
Deriving link info from sitemaps.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import logging
import re
# import urllib.robotparser # Python >= 3.8
# ROBOT_PARSER = urllib.robotparser.RobotFileParser()

from typing import List, Optional, Tuple

from courlan import clean_url, extract_domain, filter_urls, fix_relative_urls, get_hostinfo, lang_filter

from .downloads import fetch_url, is_live_page
from .settings import MAX_SITEMAPS_SEEN


LOGGER = logging.getLogger(__name__)

LINK_REGEX = re.compile(r'<loc>(?:<!\[CDATA\[)?(http.+?)(?:\]\]>)?</loc>')
XHTML_REGEX = re.compile(r'<xhtml:link.+?>', re.DOTALL)
HREFLANG_REGEX = re.compile(r'href=["\'](.+?)["\']')
WHITELISTED_PLATFORMS = re.compile(r'(?:blogger|blogpost|ghost|hubspot|livejournal|medium|typepad|squarespace|tumblr|weebly|wix|wordpress)\.')

SITEMAP_FORMAT = re.compile(r'^.{0,5}<\?xml|<sitemap|<urlset')
DETECT_SITEMAP_LINK = re.compile(r'\.xml(\..{2,4})?$|\.xml[?#]')
DETECT_LINKS = re.compile(r'https?://[^\s<"]+')
SCRUB_REGEX = re.compile(r'\?.*$|#.*$')
POTENTIAL_SITEMAP = re.compile(r'\.xml\b')  # |\bsitemap\b

GUESSES = ['sitemap.xml.gz', 'sitemap', 'sitemap_index.xml', 'sitemap_news.xml']


class SitemapObject:
    "Store all necessary information on sitemap download and processing."
    __slots__ = ["base_url", "content", "domain", "sitemap_url", "target_lang"]

    def __init__(self, base_url: str, content: str, domain: str, sitemap_url: str, target_lang: Optional[str] = None) -> None:
        self.base_url: str = base_url
        self.content: str = content
        self.domain: str = domain
        self.sitemap_url: str = sitemap_url
        self.target_lang: Optional[str] = target_lang


def sitemap_search(url: str, target_lang: Optional[str] = None) -> List[str]:
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
        LOGGER.warning('invalid URL: %s', url)
        return []
    # check base URL
    if not is_live_page(baseurl):
        LOGGER.warning('base URL unreachable, dropping sitemap: %s', url)
        return []
    # determine sitemap URL
    urlfilter = None
    if url.endswith('.xml') or url.endswith('.gz') or url.endswith('sitemap'):
        sitemapurl = url
    else:
        sitemapurl = baseurl + '/sitemap.xml'
        # filter triggered, prepare it
        if len(url) > len(baseurl) + 2:
            urlfilter = url
    sitemapurls, linklist = download_and_process_sitemap(sitemapurl, domainname, baseurl, target_lang)
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
    sitemaps_seen = {sitemapurl}
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


def is_plausible_sitemap(url: str, contents: Optional[str]) -> bool:
    '''Check if the sitemap corresponds to an expected format,
       i.e. TXT or XML.'''
    if contents is None:
        return False
    # strip query and fragments
    url = SCRUB_REGEX.sub('', url)
    # check content
    if POTENTIAL_SITEMAP.search(url) and \
        (not isinstance(contents, str) or not SITEMAP_FORMAT.match(contents)) \
         or '<html' in contents[:150].lower():
        LOGGER.warning('not a valid XML sitemap: %s', url)
        return False
    return True


def download_and_process_sitemap(url: str, domain: str, baseurl: str, target_lang: Optional[str], sitemapurls: Optional[List[str]] = None, linklist: Optional[List[str]] = None) -> Tuple[List[str], List[str]]:
    'Helper function chaining download and processing of sitemaps.'
    # variables init
    sitemapurls, linklist = sitemapurls or [], linklist or []
    # fetch and pre-process
    LOGGER.info('fetching sitemap: %s', url)
    pagecontent = fetch_url(url)
    sitemap = SitemapObject(baseurl, pagecontent, domain, url, target_lang)
    add_sitemaps, add_links = process_sitemap(sitemap)
    return sitemapurls + add_sitemaps, linklist + add_links


def process_sitemap(sitemap: SitemapObject) -> Tuple[List[str], List[str]]:
    'Download a sitemap and extract the links it contains.'
    plausible = is_plausible_sitemap(sitemap.sitemap_url, sitemap.content)
    # safeguard
    if not plausible:
        return [], []
    # try to extract links from TXT file
    if not SITEMAP_FORMAT.match(sitemap.content):
        sitemapurls, linklist = [], []  # type: List[str], List[str]
        for match in DETECT_LINKS.finditer(sitemap.content):
            link, state = handle_link(match[0], sitemap)
            sitemapurls, linklist = store_sitemap_link(sitemapurls, linklist, link, state)
        return sitemapurls, linklist
    # process XML sitemap
    if sitemap.target_lang is not None:
        sitemapurls, linklist = extract_sitemap_langlinks(sitemap)
        if len(sitemapurls) != 0 or len(linklist) != 0:
            return sitemapurls, linklist
    return extract_sitemap_links(sitemap)


def handle_link(link: str, sitemap: SitemapObject) -> Tuple[str, str]:
    '''Examine a link and determine if it's valid and if it leads to
       a sitemap or a web page.'''
    state = '0'
    # safety net: recursivity
    if link == sitemap.sitemap_url:
        return link, state
    # fix and check
    link = fix_relative_urls(sitemap.base_url, link)
    # clean and normalize
    link = clean_url(link, sitemap.target_lang)
    if link is not None and lang_filter(link, sitemap.target_lang) is True:
        newdomain = extract_domain(link, fast=True)
        if newdomain is None:
            LOGGER.error("couldn't extract domain: %s", link)
        # don't take links from another domain and make an exception for main platforms
        # also bypass: subdomains vs. domains
        elif newdomain != sitemap.domain and not newdomain in sitemap.domain and not WHITELISTED_PLATFORMS.search(newdomain):
            LOGGER.warning('diverging domain names: %s %s', sitemap.domain, newdomain)
        else:
            state = 'sitemap' if DETECT_SITEMAP_LINK.search(link) else 'link'
    return link, state


def store_sitemap_link(sitemapurls: List[str], linklist: List[str], link: str, state: str) -> Tuple[List[str], List[str]]:
    '''Process link according to filtered result: discard it or store it
       in the appropriate list.'''
    if state == 'sitemap' and link is not None:
        sitemapurls.append(link)
    elif state == 'link' and link is not None:
        linklist.append(link)
    return sitemapurls, linklist


def extract_sitemap_langlinks(sitemap: SitemapObject) -> Tuple[List[str], List[str]]:
    'Extract links corresponding to a given target language.'
    if 'hreflang=' not in sitemap.content:
        return [], []
    sitemapurls, linklist = [], []  # type: List[str], List[str]
    # compile regex here for modularity and efficiency
    lang_regex = re.compile(rf"hreflang=[\"']({sitemap.target_lang}.*?|x-default)[\"']", re.DOTALL)
    for attr_match in XHTML_REGEX.finditer(sitemap.content):
        attributes = attr_match[0]
        if lang_regex.search(attributes):
            lang_match = HREFLANG_REGEX.search(attributes)
            if lang_match:
                link, state = handle_link(lang_match[1], sitemap)
                sitemapurls, linklist = store_sitemap_link(sitemapurls, linklist, link, state)
    LOGGER.info('%s sitemaps and %s links with hreflang found for %s', len(sitemapurls), len(linklist), sitemap.sitemap_url)
    LOGGER.debug('sitemaps found: %s', sitemapurls)
    return sitemapurls, linklist


def extract_sitemap_links(sitemap: SitemapObject) -> Tuple[List[str], List[str]]:
    'Extract sitemap links and web page links from a sitemap file.'
    sitemapurls, linklist = [], []  # type: List[str], List[str]
    # extract
    for match in LINK_REGEX.finditer(sitemap.content):
        # process middle part of the match tuple
        link, state = handle_link(match[1], sitemap)
        sitemapurls, linklist = store_sitemap_link(sitemapurls, linklist, link, state)
    LOGGER.info('%s sitemaps and %s links found for %s', len(sitemapurls), len(linklist), sitemap.sitemap_url)
    LOGGER.debug('sitemaps found: %s', sitemapurls)
    return sitemapurls, linklist


def find_robots_sitemaps(baseurl: str) -> List[str]:
    '''Guess the location of the robots.txt file and try to extract
       sitemap URLs from it'''
    robotstxt = fetch_url(baseurl + '/robots.txt')
    return extract_robots_sitemaps(robotstxt, baseurl)


def extract_robots_sitemaps(robotstxt: str, baseurl: str) -> List[str]:
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
    LOGGER.info('%s sitemaps found in robots.txt', len(sitemapurls))
    LOGGER.debug('sitemaps found in robots.txt: %s', sitemapurls)
    return sitemapurls
