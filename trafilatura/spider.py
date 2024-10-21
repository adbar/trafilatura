# pylint:disable-msg=E0611,E1101,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging

from configparser import ConfigParser
from time import sleep
from typing import List, Optional, Tuple
from urllib.robotparser import RobotFileParser

from courlan import (
    UrlStore,
    extract_links,
    fix_relative_urls,
    get_base_url,
    is_navigation_page,
    is_not_crawlable,
)

try:
    import py3langid  # type: ignore
except ImportError:
    pass

from lxml.etree import XPath, tostring

from .core import baseline, prune_unwanted_nodes
from .downloads import Response, fetch_response, fetch_url
from .settings import DEFAULT_CONFIG
from .utils import LANGID_FLAG, decode_file, load_html


LOGGER = logging.getLogger(__name__)

URL_STORE = UrlStore(compressed=False, strict=False)

ROBOTS_TXT_URL = "/robots.txt"
MAX_SEEN_URLS = 10
MAX_KNOWN_URLS = 100000


class CrawlParameters:
    "Store necessary information to manage a focused crawl."
    __slots__ = ["start", "base", "lang", "rules", "ref", "i", "known_num", "is_on", "prune_xpath"]

    def __init__(
        self,
        start: str,
        lang: Optional[str] = None,
        rules: Optional[RobotFileParser] = None,
        prune_xpath: Optional[str] = None,
    ) -> None:
        self.start: str = start
        self.base: str = self._get_base_url(start)
        self.ref: str = self._get_reference(start)
        self.lang: Optional[str] = lang
        self.rules: Optional[RobotFileParser] = rules or get_rules(self.base)
        self.i: int = 0
        self.known_num: int = 0
        self.is_on: bool = True
        self.prune_xpath: Optional[str] = prune_xpath

    def _get_base_url(self, start: str) -> str:
        "Set reference domain for the crawl."
        base: str = get_base_url(start)
        if not base:
            raise ValueError(f"cannot start crawl: {start}")
        return base

    def _get_reference(self, start: str) -> str:
        "Determine the reference URL."
        return start.rsplit("/", 1)[0] if start.count("/") >= 3 else start

    def update_metadata(self, url_store: UrlStore) -> None:
        "Adjust crawl data based on URL store info."
        self.is_on = bool(url_store.find_unvisited_urls(self.base))
        self.known_num = len(url_store.find_known_urls(self.base))

    def filter_list(self, todo: Optional[List[str]]) -> List[str]:
        "Prepare the todo list, excluding invalid URLs."
        if not todo:
            return []
        return [u for u in todo if u != self.start and self.ref in u]

    def is_valid_link(self, link: str) -> bool:
        "Run checks: robots.txt rules, URL type and crawl breadth."
        return (
            (not self.rules or self.rules.can_fetch("*", link))
            and self.ref in link
            and not is_not_crawlable(link)
        )


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

    if not result or ";" not in result:
        logging.info("no redirect found: %s", homepage)
        return htmlstring, homepage

    url2 = result.split(";")[1].strip().lower().replace("url=", "")
    if not url2.startswith("http"):
        # Relative URL, adapt
        base_url = get_base_url(url2)
        url2 = fix_relative_urls(base_url, url2)
    # second fetch
    newhtmlstring = fetch_url(url2)
    if newhtmlstring is None:
        logging.warning("failed redirect: %s", url2)
        return None, None
    # else:
    logging.info("successful redirect: %s", url2)
    return newhtmlstring, url2


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
    return new_htmlstring, new_homepage, get_base_url(new_homepage)


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
    return parse_robots(robots_url, data) if data else None


def is_target_language(htmlstring: str, language: Optional[str]) -> bool:
    """Run a baseline extraction and use a language detector to
    check if the content matches the target language.
    Return True if language checks are bypassed."""
    if htmlstring and language and LANGID_FLAG:
        _, text, _ = baseline(htmlstring)
        result, _ = py3langid.classify(text)
        return bool(result == language)
    return True


def is_still_navigation(todo: List[str]) -> bool:
    """Probe if there are still navigation URLs in the queue."""
    return any(is_navigation_page(url) for url in todo)


def process_links(
    htmlstring: str,
    params: CrawlParameters,
    url: Optional[str] = "",
) -> None:
    """Examine the HTML code and process the retrieved internal links.
    Extract and filter new internal links after an optional language check.
    Store the links in todo-list while prioritizing the navigation ones."""
    if not is_target_language(htmlstring, params.lang):
        return

    if htmlstring and params.prune_xpath is not None:
        if isinstance(params.prune_xpath, str):
            params.prune_xpath = [params.prune_xpath]  # type: ignore[assignment]
        tree = load_html(htmlstring)
        if tree is not None:
            tree = prune_unwanted_nodes(tree, [XPath(x) for x in params.prune_xpath])
            htmlstring = tostring(tree).decode()

    links, links_priority = [], []
    for link in extract_links(
        pagecontent=htmlstring,
        url=url or params.base,
        external_bool=False,
        language=params.lang,
        with_nav=True,
        strict=False,
    ):
        if not params.is_valid_link(link):
            continue
        if is_navigation_page(link):
            links_priority.append(link)
        else:
            links.append(link)

    URL_STORE.add_urls(urls=links, appendleft=links_priority)


def process_response(
    response: Optional[Response],
    params: CrawlParameters,
) -> None:
    """Convert urllib3 response object and extract links."""
    if response is None or not response.data:
        return
    # add final document URL to known_links
    URL_STORE.add_urls([response.url], visited=True)

    # convert urllib3 response to string and proceed to link extraction
    process_links(decode_file(response.data), params, params.base)


def init_crawl(
    start: str,
    lang: Optional[str] = None,
    rules: Optional[RobotFileParser] = None,
    todo: Optional[List[str]] = None,
    known: Optional[List[str]] = None,
    prune_xpath: Optional[str] = None,
) -> CrawlParameters:
    """Initialize crawl by setting variables, copying values to the
    URL store and retrieving the initial page if the crawl starts."""
    params = CrawlParameters(start, lang, rules, prune_xpath)

    # todo: just known or also visited?
    URL_STORE.add_urls(urls=known or [], visited=True)
    URL_STORE.add_urls(urls=params.filter_list(todo))
    URL_STORE.store_rules(params.base, params.rules)

    # visiting the start page if necessary
    if not todo:
        URL_STORE.add_urls(urls=[params.start], visited=False)
        params = crawl_page(params, initial=True)
    else:
        params.update_metadata(URL_STORE)

    return params


def crawl_page(
    params: CrawlParameters,
    initial: bool = False,
) -> CrawlParameters:
    """Examine a webpage, extract navigation links and links."""
    # config=DEFAULT_CONFIG
    url = URL_STORE.get_url(params.base)
    if not url:
        params.is_on = False
        params.known_num = len(URL_STORE.find_known_urls(params.base))
        return params

    params.i += 1

    if initial:
        # probe and process homepage
        htmlstring, homepage, new_base_url = probe_alternative_homepage(url)
        if htmlstring and homepage and new_base_url:
            # register potentially new homepage
            URL_STORE.add_urls([homepage])
            # extract links on homepage
            process_links(htmlstring, params, url=url)
    else:
        response = fetch_response(url, decode=False)
        process_response(response, params)

    # optional backup of gathered pages without nav-pages ? ...
    params.update_metadata(URL_STORE)
    return params


def focused_crawler(
    homepage: str,
    max_seen_urls: int = MAX_SEEN_URLS,
    max_known_urls: int = MAX_KNOWN_URLS,
    todo: Optional[List[str]] = None,
    known_links: Optional[List[str]] = None,
    lang: Optional[str] = None,
    config: ConfigParser = DEFAULT_CONFIG,
    rules: Optional[RobotFileParser] = None,
    prune_xpath: Optional[str] = None,
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
        prune_xpath: remove unwanted elements from the HTML pages using XPath.

    Returns:
        List of pages to visit, deque format, possibly empty if there are no further pages to visit.
        Set of known links.

    """
    params = init_crawl(homepage, lang, rules, todo, known_links, prune_xpath)

    sleep_time = URL_STORE.get_crawl_delay(
        params.base, default=config.getfloat("DEFAULT", "SLEEP_TIME")
    )

    # visit pages until a limit is reached
    while (
        params.is_on and params.i < max_seen_urls and params.known_num < max_known_urls
    ):
        params = crawl_page(params)
        sleep(sleep_time)

    # refocus todo-list on URLs without navigation?
    todo = list(dict.fromkeys(URL_STORE.find_unvisited_urls(params.base)))
    # [u for u in todo if not is_navigation_page(u)]
    known_links = list(dict.fromkeys(URL_STORE.find_known_urls(params.base)))
    return todo, known_links
