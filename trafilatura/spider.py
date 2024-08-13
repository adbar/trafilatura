# pylint:disable-msg=E0611,E1101,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging

from time import sleep
from typing import Any, List, Optional, Tuple
from urllib.robotparser import RobotFileParser

from courlan import (
    UrlStore,
    extract_links,
    fix_relative_urls,
    get_hostinfo,
    is_navigation_page,
    is_not_crawlable,
)

try:
    import py3langid
except ImportError:
    pass

from .core import baseline
from .downloads import fetch_response, fetch_url
from .settings import DEFAULT_CONFIG
from .utils import LANGID_FLAG, decode_file, load_html


LOGGER = logging.getLogger(__name__)

URL_STORE = UrlStore(compressed=False, strict=False)

ROBOTS_TXT_URL = "/robots.txt"
MAX_SEEN_URLS = 10
MAX_KNOWN_URLS = 100000


def refresh_detection(
    htmlstring: str, homepage: str
) -> Tuple[Optional[str], Optional[str]]:
    "Check if there could be a redirection by meta-refresh tag."
    if '"refresh"' not in htmlstring and '"REFRESH"' not in htmlstring:
        return htmlstring, homepage

    html_tree = load_html(htmlstring)
    if html_tree is None:
        return htmlstring, homepage

    # test meta-refresh redirection
    # https://stackoverflow.com/questions/2318446/how-to-follow-meta-refreshes-in-python
    results = html_tree.xpath(
        './/meta[@http-equiv="refresh" or @http-equiv="REFRESH"]/@content'
    )
    result = results[0] if results else ""
    if ";" in result:
        url2 = result.split(";")[1].strip().lower().replace("url=", "")
        if not url2.startswith("http"):
            # Relative URL, adapt
            _, base_url = get_hostinfo(url2)
            url2 = fix_relative_urls(base_url, url2)
        # second fetch
        newhtmlstring = fetch_url(url2)
        if newhtmlstring is None:
            logging.warning("failed redirect: %s", url2)
            return None, None
        # else:
        logging.info("successful redirect: %s", url2)
        return newhtmlstring, url2

    logging.info("no redirect found: %s", homepage)
    return htmlstring, homepage


def probe_alternative_homepage(
    homepage: str,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    "Check if the homepage is redirected and return appropriate values."
    response = fetch_response(homepage, decode=False)
    if not response or not response.data:
        return None, None, None

    # get redirected URL here?
    if response.url not in (homepage, "/"):
        logging.info("followed homepage redirect: %s", response.url)
        homepage = response.url

    # decode response
    htmlstring = decode_file(response.data)

    # is there a meta-refresh on the page?
    new_htmlstring, new_homepage = refresh_detection(htmlstring, homepage)
    if new_homepage is None:  # malformed or malicious content
        return None, None, None

    logging.debug("fetching homepage OK: %s", new_homepage)
    _, base_url = get_hostinfo(new_homepage)
    return new_htmlstring, new_homepage, base_url


def process_links(
    htmlstring: str,
    url: Optional[str] = "",
    language: Optional[str] = None,
    rules: Optional[RobotFileParser] = None,
    ref: Optional[str] = None,
) -> None:
    """Examine the HTML code and process the retrieved internal links.
    Extract and filter new internal links after an optional language check.
    Store the links in todo-list while prioritizing the navigation ones."""
    # optional language check: run baseline extraction + language identifier
    if language and LANGID_FLAG and htmlstring:
        _, text, _ = baseline(htmlstring)
        result, _ = py3langid.classify(text)
        if result != language:
            return

    # iterate through the links and filter them
    links, links_priority = [], []
    for link in extract_links(
        pagecontent=htmlstring,
        url=url,
        external_bool=False,
        language=language,
        with_nav=True,
    ):
        # check robots.txt rules + sanity check
        if (rules and not rules.can_fetch("*", link)) or is_not_crawlable(link):
            continue
        # use reference to determine crawl breadth
        if ref and ref not in link:
            continue
        # store
        if is_navigation_page(link):
            links_priority.append(link)
        else:
            links.append(link)

    URL_STORE.add_urls(urls=links, appendleft=links_priority)


def process_response(
    response: Any,
    base_url: str,
    language: Optional[str],
    rules: Optional[RobotFileParser] = None,
    ref: Optional[str] = None,
) -> None:
    """Convert urllib3 response object and extract links."""
    # add final document URL to known_links
    if response is not None:
        URL_STORE.add_urls([response.url], visited=True)
        if response.data:
            # convert urllib3 response to string
            htmlstring = decode_file(response.data)
            # proceed to link extraction
            process_links(htmlstring, base_url, language=language, rules=rules, ref=ref)


def parse_robots(robots_url: str, data: str) -> Optional[RobotFileParser]:
    "Parse a robots.txt file with the standard library urllib.robotparser."
    # https://github.com/python/cpython/blob/main/Lib/urllib/robotparser.py
    rules = RobotFileParser()
    rules.set_url(robots_url)
    # exceptions happening here
    try:
        rules.parse(data.splitlines())
    except Exception as exc:
        LOGGER.error("cannot read robots.txt: %s", exc)
        return None
    return rules


def get_rules(base_url: str) -> Optional[RobotFileParser]:
    "Attempt to fetch and parse robots.txt file for a given website."
    robots_url = base_url + ROBOTS_TXT_URL
    data = fetch_url(robots_url)
    if data is not None:
        return parse_robots(robots_url, data)
    return None


def init_crawl(
    homepage: str,
    todo: Optional[List[str]] = None,
    known_links: Optional[List[str]] = None,
    language: Optional[str] = None,
    rules: Optional[RobotFileParser] = None,
    ref: Optional[str] = None,
) -> Tuple[str, int, int, Optional[RobotFileParser], bool]:
    "Start crawl by initializing variables and potentially examining the starting page."
    # config=DEFAULT_CONFIG
    _, base_url = get_hostinfo(homepage)
    if not base_url:
        raise ValueError(f"cannot crawl homepage: {homepage}")

    # TODO: just known or also visited?
    if known_links:
        URL_STORE.add_urls(urls=known_links, visited=True)
    i = 0

    # fetch and parse robots.txt file if necessary
    rules = rules or get_rules(base_url)
    URL_STORE.store_rules(base_url, rules)

    # initialize crawl by visiting homepage if necessary
    if todo is None:
        URL_STORE.add_urls(urls=[homepage], visited=False)
        _, known_num, i = crawl_page(
            i, base_url, lang=language, rules=rules, initial=True, ref=ref
        )
    else:
        known_num = len(URL_STORE.find_known_urls(base_url))
    is_on = bool(URL_STORE.find_unvisited_urls(base_url))
    return base_url, i, known_num, rules, is_on


def crawl_page(
    visited_num: int,
    base_url: str,
    lang: Optional[str] = None,
    rules: Optional[RobotFileParser] = None,
    initial: bool = False,
    ref: Optional[str] = None,
) -> Tuple[bool, int, int]:
    """Examine a webpage, extract navigation links and links."""
    # config=DEFAULT_CONFIG
    url = URL_STORE.get_url(base_url)
    if not url:
        return False, len(URL_STORE.find_known_urls(base_url)), visited_num

    visited_num += 1

    if initial is True:
        # probe and process homepage
        htmlstring, homepage, new_base_url = probe_alternative_homepage(url)
        if htmlstring and homepage and new_base_url:
            # register potentially new homepage
            URL_STORE.add_urls([homepage])
            # extract links on homepage
            process_links(htmlstring, url=url, language=lang, rules=rules, ref=ref)
    else:
        response = fetch_response(url, decode=False)
        process_response(response, base_url, lang, rules=rules, ref=ref)

    # optional backup of gathered pages without nav-pages ? ...
    is_on = bool(URL_STORE.find_unvisited_urls(base_url))
    known_num = len(URL_STORE.find_known_urls(base_url))
    return is_on, known_num, visited_num


def focused_crawler(
    homepage: str,
    max_seen_urls: int = MAX_SEEN_URLS,
    max_known_urls: int = MAX_KNOWN_URLS,
    todo: Optional[List[str]] = None,
    known_links: Optional[List[str]] = None,
    lang: Optional[str] = None,
    config: Any = DEFAULT_CONFIG,
    rules: Optional[RobotFileParser] = None,
) -> Tuple[List[str], List[str]]:
    """Basic crawler targeting pages of interest within a website.

    Args:
        homepage: URL of the page to first page to fetch, preferably the homepage of a website.
        max_seen_urls: maximum number of pages to visit, stop iterations at this number or at the exhaustion of pages on the website, whichever comes first.
        max_known_urls: stop if the total number of pages "known" exceeds this number.
        todo: provide a previously generated list of pages to visit / crawl frontier.
        known_links: provide a list of previously known pages.
        lang: try to target links according to language heuristics.
        config: use a different configuration (configparser format).
        rules: provide politeness rules (urllib.robotparser.RobotFileParser() format).

    Returns:
        List of pages to visit, deque format, possibly empty if there are no further pages to visit.
        Set of known links.

    """
    reference = homepage.rsplit("/", 1)[0]
    base_url, i, known_num, rules, is_on = init_crawl(
        homepage, todo, known_links, language=lang, rules=rules, ref=reference
    )
    sleep_time = URL_STORE.get_crawl_delay(
        base_url, default=config.getfloat("DEFAULT", "SLEEP_TIME")
    )

    # visit pages until a limit is reached
    while is_on and i < max_seen_urls and known_num <= max_known_urls:
        is_on, known_num, i = crawl_page(i, base_url, lang=lang, rules=rules, ref=reference)
        sleep(sleep_time)

    # refocus todo-list on URLs without navigation?
    todo = list(dict.fromkeys(URL_STORE.find_unvisited_urls(base_url)))
    # [u for u in todo if not is_navigation_page(u)]
    known_links = list(dict.fromkeys(URL_STORE.find_known_urls(base_url)))
    return todo, known_links


def is_still_navigation(todo: List[str]) -> bool:
    """Probe if there are still navigation URLs in the queue."""
    return any(is_navigation_page(url) for url in todo)
