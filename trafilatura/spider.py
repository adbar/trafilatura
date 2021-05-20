# pylint:disable-msg=E0611,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging
import re

from collections import deque
from time import sleep

from courlan import extract_links
from courlan.filters import is_navigation_page
from lxml import etree

#from .feeds import determine_feed
from .settings import DEFAULT_CONFIG
from .utils import decode_response, fetch_url, fix_relative_urls, get_hostinfo, load_html


LOGGER = logging.getLogger(__name__)


def refresh_detection(htmlstring, homepage):
    "Check if there could be a redirection by meta-refresh tag."
    if '"refresh"' in htmlstring or '"REFRESH"' in htmlstring:
        try:
            html_tree = load_html(htmlstring)
            # test meta-refresh redirection
            # https://stackoverflow.com/questions/2318446/how-to-follow-meta-refreshes-in-python
            attr = html_tree.xpath('//meta[@http-equiv="refresh"]/@content|//meta[@http-equiv="REFRESH"]/@content')[0]
            _, text = attr.split(';')
            text = text.strip().lower()
            if text.startswith('url=') or text.startswith('URL='):
                url2 = text[4:]
                if not url2.startswith('http'):
                    # Relative URL, adapt
                    _, baseurl = get_hostinfo(url2)
                    url2 = fix_relative_urls(baseurl, url2)
                # second fetch
                newhtmlstring = fetch_url(url2)
                if newhtmlstring is None:
                    logging.warning('failed redirect: %s', url2)
                    return None, None
                #else:
                htmlstring, homepage = newhtmlstring, url2
                logging.info('successful redirect: %s', url2)
        except (IndexError, etree.ParserError, etree.XMLSyntaxError, etree.XPathEvalError) as err:
            logging.info('no redirect found: %s %s', homepage, err)
    return htmlstring, homepage


def probe_alternative_homepage(homepage):
    "Check if the homepage is redirected and return appropriate values."
    response = fetch_url(homepage, decode=False)
    if response is None or response == '':
        return None, None, None
    # get redirected URL here?
    if response.geturl() != homepage:
        logging.info('followed redirect: %s', response.geturl())
        homepage = response.geturl()
    # decode response
    htmlstring = decode_response(response.data)
    # is there a meta-refresh on the page?
    htmlstring, homepage = refresh_detection(htmlstring, homepage)
    logging.info('fetching homepage OK: %s', homepage)
    _, baseurl = get_hostinfo(homepage)
    return htmlstring, homepage, baseurl


def process_links(htmlstring, base_url, known_links, todo):
    """Examine the HTML code and process the retrieved internal links. Store
       the links in todo-list while prioritizing the navigation ones."""
    navlinks, links = [], []
    # language=None, reference=None
    for link in extract_links(htmlstring, base_url, False, with_nav=True):
        if link in known_links:
            continue
        if is_navigation_page(link):
            navlinks.append(link)
        else:
            links.append(link)
        known_links.add(link)
    # add links to deque
    if todo is None:
        todo = deque()
    todo.extend(links)
    # prioritize navigation links
    todo.extendleft(navlinks)
    return todo, known_links


def crawl_page(url, base_url, todo, known_links): # language
    """Examine the homepage, extract navigation links, links,
       and feed links (if any on the homepage)."""
    response = fetch_url(url, decode=False)
    # add final document URL to known_links
    known_links.add(response.geturl())
    if response.data is not None and response.data != '':
        # convert urllib3 response to string
        htmlstring = decode_response(response.data)
        # optional language check
        # ...
        todo, known_urls = process_links(htmlstring, base_url, known_links, todo)
        # optional backup of gathered pages without nav-pages
        # ...
    return todo, known_urls, htmlstring


def focused_crawler(homepage, base_url, max_seen_urls=10, max_known_urls=100000, todo=None, known_links=None, config=DEFAULT_CONFIG):
    """Basic crawler targeting pages within a website."""
    # variables init
    known_links = known_links or set()
    if todo is None:
        # probe and process homepage
        htmlstring, homepage, base_url = probe_alternative_homepage(homepage)
        # extract links on homepage
        todo, known_links = process_links(htmlstring, base_url, known_links, todo)
        # optional: find feed URLs
        # feeds.find_feed_urls(url, target_lang=None)
    i = 0
    # visit pages
    while todo and i < max_seen_urls and len(known_links) <= max_known_urls:
        url = todo.popleft()
        todo, known_links, _ = crawl_page(url, base_url, todo, known_links)
        i += 1
        sleep(config.getfloat('DEFAULT', 'SLEEP_TIME'))
    # refocus todo-list on URLs without navigation
    return [u for u in todo if not is_navigation_page(u)], known_links
