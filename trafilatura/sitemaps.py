"""
Deriving link info from sitemaps.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import re
# import urllib.robotparser # Python >= 3.8
# ROBOT_PARSER = urllib.robotparser.RobotFileParser()

from courlan.core import check_url, extract_domain

from .utils import fetch_url


LOGGER = logging.getLogger(__name__)

LINK_REGEX = re.compile(r'(?<=<loc>).+?(?=</loc>)')
XHTML_REGEX = re.compile(r'(?<=<xhtml:link).+?(?=/>)', re.DOTALL)
HREFLANG_REGEX = re.compile(r"(?<=href=[\"']).+?(?=[\"'])")


def sitemap_search(url, target_lang=None):
    'Look for sitemaps for the given URL and gather links.'
    domain = extract_domain(url)
    sitemapurl = url.rstrip('/') + '/sitemap.xml'
    sitemapurls, linklist = process_sitemap(sitemapurl, domain, target_lang)
    if sitemapurls == [] and len(linklist) > 0:
        return linklist
    if sitemapurls == [] and linklist == []:
        for sitemapurl in find_robots_sitemaps(url):
            tmp_sitemapurls, tmp_linklist = process_sitemap(sitemapurl, domain, target_lang)
            sitemapurls.extend(tmp_sitemapurls)
            linklist.extend(tmp_linklist)
    while sitemapurls:
        tmp_sitemapurls, tmp_linklist = process_sitemap(sitemapurls.pop(), domain, target_lang)
        sitemapurls.extend(tmp_sitemapurls)
        linklist.extend(tmp_linklist)
    LOGGER.debug('%s links found for %s', len(linklist), domain)
    return linklist


def fix_relative_urls(domain, url):
    'Prepend protocal and domain information to relative links.'
    urlfix = ''
    # process URL
    if url.startswith('/'):
        urlfix = 'http://' + domain.rstrip('/') + url
    else:
        urlfix = url
    return urlfix


def process_sitemap(url, domain, target_lang=None):
    'Download a sitemap and extract the links it contains.'
    LOGGER.info('fetching sitemap: %s', url)
    pagecontent = fetch_url(url)
    if pagecontent is None or not pagecontent.startswith('<?xml'):
        logging.warning('not a sitemap: %s', domain) # respheaders
        return [], []
    if target_lang is not None:
        sitemapurls, linklist = extract_sitemap_langlinks(pagecontent, url, domain, target_lang)
        if len(sitemapurls) != 0 or len(linklist) != 0:
            return sitemapurls, linklist
    return extract_sitemap_links(pagecontent, url, domain, target_lang)


def handle_link(link, domainname, sitemapurl, target_lang=None):
    '''Examine a link and determine if it's valid and if it leads to
       a sitemap or a web page.'''
    state = '0'
    # safety net: recursivity
    if link == sitemapurl:
        return link, state
    # fix and check
    link = fix_relative_urls(domainname, link)
    if re.search(r'\.xml$|\.xml[.?#]', link):
        state = 'sitemap'
    else:
        checked = check_url(link, language=target_lang)
        if checked is not None:
            link, state = checked[0], 'link'
    return link, state


def extract_sitemap_langlinks(pagecontent, sitemapurl, domainname, target_lang=None):
    'Extract links corresponding to a given target language.'
    if not 'hreflang=' in pagecontent:
        return [], []
    sitemapurls, linklist = [], []
    lang_regex = re.compile(r"hreflang=[\"']({}.*?|x-default)[\"']".format(target_lang), re.DOTALL)
    for attributes in XHTML_REGEX.findall(pagecontent):
        if lang_regex.search(attributes):
            match = HREFLANG_REGEX.search(attributes)
            if match:
                link, state = handle_link(match.group(0), domainname, sitemapurl, target_lang)
                if state == 'sitemap':
                    sitemapurls.append(link)
                elif state == 'link':
                    linklist.append(link)
    LOGGER.debug('%s sitemaps and %s links with hreflang found for %s', len(sitemapurls), len(linklist), sitemapurl)
    return sitemapurls, linklist


def extract_sitemap_links(pagecontent, sitemapurl, domainname, target_lang=None):
    'Extract sitemap links and web page links from a sitemap file.'
    sitemapurls, linklist = [], []
    # extract
    for link in LINK_REGEX.findall(pagecontent):
        link, state = handle_link(link, domainname, sitemapurl, target_lang)
        if state == 'sitemap':
            sitemapurls.append(link)
        elif state == 'link':
            linklist.append(link)
    LOGGER.debug('%s sitemaps and %s links found for %s', len(sitemapurls), len(linklist), sitemapurl)
    return sitemapurls, linklist


def find_robots_sitemaps(url):
    '''Guess the location of the robots.txt file and try to extract 
       sitemap URLs from it'''
    robotsurl = url.rstrip('/') + '/robots.txt'
    robotstxt = fetch_url(robotsurl)
    if robotstxt is None:
        return []
    return extract_robots_sitemaps(robotstxt)


def extract_robots_sitemaps(robotstxt):
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
                line[1] = line[1].strip() # urllib.parse.unquote(line[1].strip())
                sitemapurls.append(line[1])
    LOGGER.debug('%s sitemaps found in robots.txt', len(sitemapurls))
    return sitemapurls
