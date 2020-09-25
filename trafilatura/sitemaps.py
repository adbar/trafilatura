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



def sitemap_search(url):
    domain = extract_domain(url)
    sitemapurl = url.rstrip('/') + '/sitemap.xml'
    sitemapurls, linklist = process_sitemap(sitemapurl, domain)
    if sitemapurls == [] and len(linklist) > 0:
        return linklist
    if sitemapurls == [] and linklist == []:
        for sitemapurl in find_robots_sitemaps(url):
            tmp_sitemapurls, tmp_linklist = process_sitemap(url, domain)
            sitemapurls.extend(tmp_sitemapurls)
            linklist.extend(tmp_linklist)
        while sitemapurls:
            tmp_sitemapurls, tmp_linklist = process_sitemap(sitemapurls.pop(), domain)
            sitemapurls.extend(tmp_sitemapurls)
            linklist.extend(tmp_linklist)
    return linklist


def fix_relative_urls(domain, url):
    urlfix = ''
    # process URL
    if url.startswith('/'):
        urlfix = 'http://' + domain.rstrip('/') + url
    else:
        urlfix = url
    return urlfix


def process_sitemap(url, domain):
    pagecontent = fetch_url(url)
    if pagecontent is None:
        return [], []
    return extract_sitemap_links(pagecontent, url, domain)


def extract_sitemap_links(pagecontent, sitemapurl, domainname):

    if not pagecontent.startswith('<?xml'):
        logging.warning('not a sitemap: %s', domainname) # respheaders
        return [], []

    sitemapurls, linklist = list(), list()

    # extract
    for link in re.findall(r'(?<=<loc>).+?(?=</loc>)', pagecontent):
        # check number of nested sitemaps
        #if len(sitemapurls) > settings.MAX_SITEMAPS_PER_NSITEMAP:
        #    break
        # safety net: recursivity
        if link == sitemapurl:
            continue
        ### nested!
        if '.xml' in link and re.search(r'\.xml$|\.xml[.?#]', link): # was \W
            # relative link
            link = fix_relative_urls(domainname, link)
            # no check necessary
            #checked = check_url(link, strict=True, with_redirects=False, with_language=True)
            sitemapurls.append(link)
        else:
            # only add if no hreflang links found
            #if hreflangflag is False:
            link = fix_relative_urls(domainname, link)
            checked = check_url(link) # strict=True, with_redirects=False, with_language=True
            if checked is not None:
                linklist.append(checked[0])
    return sitemapurls, linklist


def find_robots_sitemaps(url):
    robotsurl = url.rstrip('/') + '/robots.txt'
    robotstxt = fetch_url(robotsurl)
    if robotstxt is None:
        return []
    return extract_robots_sitemaps(robotstxt)


def extract_robots_sitemaps(robotstxt):
    sitemaps = list()
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
                sitemaps.append(line[1])
    return sitemaps
