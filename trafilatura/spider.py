# pylint:disable-msg=E0611,E1101,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging
import urllib.robotparser
from time import sleep

from courlan import (UrlStore, extract_links, fix_relative_urls, get_hostinfo,
                     is_navigation_page, is_not_crawlable)

from .core import baseline
from .downloads import fetch_url
# from .feeds import find_feed_urls # extract_links ad extract_feed_links
from .settings import DEFAULT_CONFIG
from .utils import decode_response, load_html

# language detection
try:
    import py3langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False

LOGGER = logging.getLogger(__name__)

URL_STORE = UrlStore(compressed=False, strict=False)


def refresh_detection(htmlstring, homepage):
    "Check if there could be a redirection by meta-refresh tag."
    if not '"refresh"' in htmlstring and not '"REFRESH"' in htmlstring:
        return htmlstring, homepage

    html_tree = load_html(htmlstring)
    if html_tree is None:
        return htmlstring, homepage

    # test meta-refresh redirection
    # https://stackoverflow.com/questions/2318446/how-to-follow-meta-refreshes-in-python
    results =  html_tree.xpath('//meta[@http-equiv="refresh"]/@content|//meta[@http-equiv="REFRESH"]/@content')
    if results and ';' in results[0]:
        text = results[0].split(';')[1].strip().lower()
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
        else:
            logging.info('no redirect found: %s', homepage)
    return htmlstring, homepage


def probe_alternative_homepage(homepage):
    "Check if the homepage is redirected and return appropriate values."
    response = fetch_url(homepage, decode=False)
    if response is None or response == '':
        return None, None, None
    # get redirected URL here?
    if response.url not in (homepage, "/"):
        logging.info('followed redirect: %s', response.url)
        homepage = response.url
    # decode response
    htmlstring = decode_response(response.data)
    # is there a meta-refresh on the page?
    htmlstring, homepage = refresh_detection(htmlstring, homepage)
    if homepage is None:  # malformed or malicious content
        return None, None, None
    logging.info('fetching homepage OK: %s', homepage)
    _, base_url = get_hostinfo(homepage)
    return htmlstring, homepage, base_url


def process_links(htmlstring, url="", language=None, rules=None):
    """Examine the HTML code and process the retrieved internal links.
       Extract and filter new internal links after an optional language check.
       Store the links in todo-list while prioritizing the navigation ones."""
    links, links_priority = [], []
    # optional language check: run baseline extraction + language identifier
    if language is not None and LANGID_FLAG is True and htmlstring is not None:
        _, text, _ = baseline(htmlstring)
        result, _ = py3langid.classify(text)
        if result != language:
            return
    # iterate through the links and filter them
    for link in extract_links(pagecontent=htmlstring, url=url, external_bool=False, language=language, with_nav=True):
        # check robots.txt rules
        if rules is not None and not rules.can_fetch("*", link):
            continue
        # sanity check
        if is_not_crawlable(link):
            continue
        # store
        if is_navigation_page(link):
            links_priority.append(link)
        else:
            links.append(link)
    URL_STORE.add_urls(urls=links, appendleft=links_priority)


def process_response(response, base_url, language, rules=None):
    """Convert urllib3 response object and extract links."""
    # add final document URL to known_links
    if response is not None:
        URL_STORE.add_urls([response.url], visited=True)
        if response.data is not None and response.data != '':
            # convert urllib3 response to string
            htmlstring = decode_response(response.data)
            # proceed to link extraction
            process_links(htmlstring, base_url, language=language, rules=rules)


def init_crawl(homepage, todo, known_links, language=None, rules=None):
    """Start crawl by initializing variables and potentially examining the starting page."""
    # config=DEFAULT_CONFIG
    _, base_url = get_hostinfo(homepage)
    if base_url is None or len(base_url) < 1:
        raise ValueError(f'cannot crawl homepage: {homepage}')
    # TODO: just known or also visited?
    if known_links is not None:
        URL_STORE.add_urls(urls=known_links, visited=True)
    i = 0
    # fetch and parse robots.txt file if necessary
    if rules is None:
        rules = urllib.robotparser.RobotFileParser()
        rules.set_url(base_url + '/robots.txt')
        # exceptions happening here
        try:
            rules.read()
        except Exception as exc:
            LOGGER.error('cannot read robots.txt: %s', exc)
            rules = None
    URL_STORE.store_rules(base_url, rules)
    # initialize crawl by visiting homepage if necessary
    if todo is None:
        URL_STORE.add_urls(urls=[homepage], visited=False)
        _, known_num, i = crawl_page(i, base_url, lang=language, rules=rules, initial=True)
    else:
        known_num = len(URL_STORE.find_known_urls(base_url))
    is_on = bool(URL_STORE.find_unvisited_urls(base_url))
    return base_url, i, known_num, rules, is_on


def crawl_page(visited_num, base_url, lang=None, rules=None, initial=False):
    """Examine a webpage, extract navigation links and links."""
    # config=DEFAULT_CONFIG
    if not URL_STORE.is_exhausted_domain(base_url):
        url = URL_STORE.get_url(base_url)
        visited_num += 1
        if initial is True:
            # probe and process homepage
            htmlstring, homepage, base_url = probe_alternative_homepage(url)
            if all((htmlstring, homepage, base_url)):
                # add potentially "new" homepage
                if homepage != url:
                    URL_STORE.add_urls([homepage])
                # extract links on homepage
                process_links(htmlstring, url=url, language=lang, rules=rules)
        else:
            response = fetch_url(url, decode=False)
            process_response(response, base_url, lang, rules=rules)
    # optional backup of gathered pages without nav-pages ? ...
    is_on = bool(URL_STORE.find_unvisited_urls(base_url))
    known_num = len(URL_STORE.find_known_urls(base_url))
    return is_on, known_num, visited_num


def focused_crawler(homepage, max_seen_urls=10, max_known_urls=100000, todo=None, known_links=None, lang=None, config=DEFAULT_CONFIG, rules=None):
    """Basic crawler targeting pages of interest within a website.

    Args:
        homepage: URL of the page to first page to fetch, preferably the homepage of a website.
        max_seen_urls: maximum number of pages to visit, stop iterations at this number or at the exhaustion of pages on the website, whichever comes first.
        max_known_urls: stop if the total number of pages "known" exceeds this number.
        todo: provide a previously generated list of pages to visit / crawl frontier, must be in collections.deque format.
        known_links: provide a previously generated set of links.
        lang: try to target links according to language heuristics.
        config: use a different configuration (configparser format).
        rules: provide politeness rules (urllib.robotparser.RobotFileParser() format).

    Returns:
        List of pages to visit, deque format, possibly empty if there are no further pages to visit.
        Set of known links.

    """
    base_url, i, known_num, rules, is_on = init_crawl(homepage, todo, known_links, language=lang, rules=rules)
    # visit pages until a limit is reached
    while is_on and i < max_seen_urls and known_num <= max_known_urls:
        is_on, known_num, i = crawl_page(i, base_url, lang=lang, rules=rules)
        sleep(URL_STORE.get_crawl_delay(base_url, default=config.getfloat('DEFAULT', 'SLEEP_TIME')))
    todo = set(URL_STORE.find_unvisited_urls(base_url))
    # refocus todo-list on URLs without navigation?
    # [u for u in todo if not is_navigation_page(u)]
    known_links = set(URL_STORE.find_known_urls(base_url))
    return todo, known_links


def is_still_navigation(todo):
    """Probe if there are still navigation URLs in the queue."""
    return any(is_navigation_page(url) for url in todo)
