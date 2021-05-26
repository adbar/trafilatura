# pylint:disable-msg=E0611,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging

from collections import deque
from time import sleep

from courlan import extract_links, fix_relative_urls, get_hostinfo, is_navigation_page, is_not_crawlable
from lxml import etree

from .core import baseline
# from .feeds import find_feed_urls # extract_links ad extract_feed_links
from .settings import DEFAULT_CONFIG
from .utils import decode_response, fetch_url, load_html

# language detection
try:
    import cld3
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

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
                    _, base_url = get_hostinfo(url2)
                    url2 = fix_relative_urls(base_url, url2)
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
    _, base_url = get_hostinfo(homepage)
    return htmlstring, homepage, base_url


def is_known_link(link, known_links):
    "Compare the link to the existing link base."
    #if link in known_links:
    #    return True
    test1 = link.rstrip('/')
    test2 = test1 + '/'
    if test1 in known_links or test2 in known_links:
        return True
    if link[:5] == 'https':
        testlink = link[:4] + link[:5]
        test1, test2 = testlink.rstrip('/'), testlink.rstrip('/') + '/'
        if testlink in known_links or test1 in known_links or test2 in known_links:
            return True
    else:
        testlink = ''.join([link[:4], 's', link[4:]])
        test1, test2 = testlink.rstrip('/'), testlink.rstrip('/') + '/'
        if testlink in known_links or test1 in known_links or test2 in known_links:
            return True
    return False


def process_links(htmlstring, base_url, known_links, todo, language=None):
    """Examine the HTML code and process the retrieved internal links. Store
       the links in todo-list while prioritizing the navigation ones."""
    navlinks, links, proceed = [], [], True
    # reference=None
    # optional language check: run baseline extraction + language identifier
    if language is not None and LANGID_FLAG is True:
        _, text, _ = baseline(htmlstring)
        result = cld3.get_language(text)
        if result is not None and result.language != language:
            proceed = False
    if proceed is True:
        for link in extract_links(htmlstring, base_url, False, language=language, with_nav=True):
            if is_known_link(link, known_links) is True or is_not_crawlable(link):
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
    # use most short links if there are no navlinks?
    todo.extendleft(navlinks)
    return todo, known_links


def init_crawl(homepage, todo, known_links, language=None):
    """Start crawl by initializing variable and potentially examining the starting page."""
    _, base_url = get_hostinfo(homepage)
    known_links = known_links or set()
    i = 0
    # initialize crawl by visiting homepage if necessary
    if todo is None:
        todo, known_links = crawl_initial_page(homepage, base_url, known_links, language)
        i += 1
    return todo, known_links, base_url, i


def crawl_initial_page(homepage, base_url, known_links, language=None): # config=DEFAULT_CONFIG
    """Examine the homepage, extract navigation links, links,
       and feed links (if any on the homepage)."""
    known_links.add(homepage) # add known homepage
    # probe and process homepage
    htmlstring, homepage, base_url = probe_alternative_homepage(homepage)
    known_links.add(homepage) # add potentially "new" homepage
    # extract links on homepage
    todo, known_links = process_links(htmlstring, base_url, known_links, None, language)
    # UNTESTED!
    # add potential URLs extracted from feeds
    #additional_links = find_feed_urls(homepage, target_lang=language)
    #todo.extend(additional_links)
    #known_links.update(additional_links)
    # TODO: more efficient
    #for feed in determine_feed(htmlstring, base_url, homepage):
    #    feed_string = fetch_url(feed)
    #    if feed_string is not None:
    #        internal_valid.extend(extract_feed_links(feed_string, domainname, baseurl, homepage, LANG))
    #    sleep(config.getfloat('DEFAULT', 'SLEEP_TIME'))
    # optional: add sitemap URLs?
    return todo, known_links


def crawl_page(i, base_url, todo, known_links, lang=None, config=DEFAULT_CONFIG):
    """Examine a webpage, extract navigation links and links."""
    url = todo.popleft()
    known_links.add(url)
    response = fetch_url(url, decode=False)
    htmlstring = ''
    # add final document URL to known_links
    if response is not None:
        known_links.add(response.geturl())
        if response.data is not None and response.data != '':
            # convert urllib3 response to string
            htmlstring = decode_response(response.data)
            # proceed to link extraction
            todo, known_links = process_links(htmlstring, base_url, known_links, todo, language=lang)
            # optional backup of gathered pages without nav-pages
            # ...
    sleep(config.getfloat('DEFAULT', 'SLEEP_TIME'))
    i += 1
    return todo, known_links, i, htmlstring


def focused_crawler(homepage, max_seen_urls=10, max_known_urls=100000, todo=None, known_links=None, lang=None, config=DEFAULT_CONFIG):
    """Basic crawler targeting pages of interest within a website."""
    todo, known_links, base_url, i = init_crawl(homepage, todo, known_links, language)
    # visit pages until a limit is reached
    while todo and i < max_seen_urls and len(known_links) <= max_known_urls:
        todo, known_links, i, _ = crawl_page(i, base_url, todo, known_links, lang=lang, config=config)
    # refocus todo-list on URLs without navigation?
    # [u for u in todo if not is_navigation_page(u)]
    return todo, known_links


def is_still_navigation(todo):
    """Probe if there are still navigation URLs in the queue."""
    return bool([u for u in todo if is_navigation_page(u)])
