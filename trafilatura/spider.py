# pylint:disable-msg=E0611,E1101,I1101
"""
Functions dedicated to website navigation and crawling/spidering.
"""

import logging
from configparser import ConfigParser
from time import sleep
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

from courlan import (
    UrlStore,
    extract_links,
    get_base_url,
    is_navigation_page,
    is_not_crawlable,
)

try:
    import py3langid
except ImportError:
    pass

from lxml.etree import XPath, tostring

from .baseline import baseline
from .downloads import fetch_response, fetch_url
from .htmlprocessing import prune_unwanted_nodes
from .settings import DEFAULT_CONFIG
from .utils import LANGID_FLAG, Response, decode_file, load_html

LOGGER = logging.getLogger(__name__)

URL_STORE = UrlStore(compressed=False, strict=False)

ROBOTS_TXT_URL = "/robots.txt"
MAX_SEEN_URLS = 10
MAX_KNOWN_URLS = 100000


class CrawlParameters:
    "Store necessary information to manage a focused crawl."

    __slots__ = ["base", "config", "i", "is_on", "known_num", "lang", "prune_xpath", "ref", "rules", "start"]

    def __init__(
        self,
        start: str,
        lang: str | None = None,
        rules: RobotFileParser | None = None,
        prune_xpath: str | list[str] | None = None,
        config: ConfigParser = DEFAULT_CONFIG,
    ) -> None:
        self.start: str = start
        self.base: str = self._get_base_url(start)
        self.ref: str = self._get_reference(start)
        self.lang: str | None = lang
        self.config: ConfigParser = config
        self.rules: RobotFileParser | None = rules or get_rules(self.base, config)
        self.i: int = 0
        self.known_num: int = 0
        self.is_on: bool = True
        self.prune_xpath: str | list[str] | None = prune_xpath

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
        self.is_on = self.base in url_store.urldict and not url_store.is_exhausted_domain(self.base)
        self.known_num = len(url_store.find_known_urls(self.base))

    def filter_list(self, todo: list[str] | None) -> list[str]:
        "Prepare the todo list, excluding invalid URLs."
        if not todo:
            return []
        return [u for u in todo if u != self.start and self.ref in u]

    def is_valid_link(self, link: str) -> bool:
        "Run checks: robots.txt rules, URL type and crawl breadth."
        return (not self.rules or self.rules.can_fetch("*", link)) and self.ref in link and not is_not_crawlable(link)


def refresh_detection(htmlstring: str, homepage: str, config: ConfigParser = DEFAULT_CONFIG) -> tuple[str | None, str | None]:
    "Check if there could be a redirection by meta-refresh tag."
    if "refresh" not in htmlstring.lower():
        return htmlstring, homepage

    html_tree = load_html(htmlstring)
    if html_tree is None:
        return htmlstring, homepage

    # test meta-refresh redirection
    # https://stackoverflow.com/questions/2318446/how-to-follow-meta-refreshes-in-python
    result = next(
        (e.get("content", "") for e in html_tree.iter("meta") if e.get("http-equiv", "").lower() == "refresh"),
        "",
    )
    if ";" not in result:
        LOGGER.info("no redirect found: %s", homepage)
        return htmlstring, homepage

    url2 = result.split(";", 1)[1].strip()
    if url2.lower().startswith("url="):
        url2 = url2[4:].strip("'\"")
    if not url2.lower().startswith("http"):
        # relative URL, adapt using the page being processed
        url2 = urljoin(homepage, url2)
    # second fetch
    newhtmlstring = fetch_url(url2, config=config)
    if newhtmlstring is None:
        LOGGER.warning("failed redirect: %s", url2)
        return None, None
    LOGGER.info("successful redirect: %s", url2)
    return newhtmlstring, url2


def probe_alternative_homepage(
    homepage: str,
    config: ConfigParser = DEFAULT_CONFIG,
) -> tuple[str | None, str | None, str | None]:
    "Check if the homepage is redirected and return appropriate values."
    response = fetch_response(homepage, decode=False, config=config)
    if not response or not response.data:
        return None, None, None

    if response.url != homepage:
        LOGGER.info("followed homepage redirect: %s", response.url)
        homepage = response.url

    # decode response
    htmlstring = decode_file(response.data)

    # is there a meta-refresh on the page?
    new_htmlstring, new_homepage = refresh_detection(htmlstring, homepage, config)
    if new_homepage is None:  # malformed or malicious content
        return None, None, None

    LOGGER.debug("fetching homepage OK: %s", new_homepage)
    return new_htmlstring, new_homepage, get_base_url(new_homepage)


def parse_robots(robots_url: str, data: str) -> RobotFileParser | None:
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


def get_rules(base_url: str, config: ConfigParser = DEFAULT_CONFIG) -> RobotFileParser | None:
    "Attempt to fetch and parse robots.txt file for a given website."
    robots_url = base_url + ROBOTS_TXT_URL
    data = fetch_url(robots_url, config=config)
    return parse_robots(robots_url, data) if data else None


def is_target_language(htmlstring: str, language: str | None) -> bool:
    """Run a baseline extraction and use a language detector to
    check if the content matches the target language.
    Return True if language checks are bypassed."""
    if htmlstring and language and LANGID_FLAG:
        _, text, _ = baseline(htmlstring)
        result, _ = py3langid.classify(text)
        return bool(result == language)
    return True


def is_still_navigation(todo: list[str]) -> bool:
    """Probe if there are still navigation URLs in the queue."""
    return any(is_navigation_page(url) for url in todo)


def process_links(
    htmlstring: str,
    params: CrawlParameters,
    url: str | None = "",
) -> None:
    """Examine the HTML code and process the retrieved internal links.
    Extract and filter new internal links after an optional language check.
    Store the links in todo-list while prioritizing the navigation ones."""
    if not is_target_language(htmlstring, params.lang):
        return

    if htmlstring and params.prune_xpath:
        xpaths = [params.prune_xpath] if isinstance(params.prune_xpath, str) else params.prune_xpath
        tree = load_html(htmlstring)
        if tree is not None:
            tree = prune_unwanted_nodes(tree, [XPath(x) for x in xpaths])
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
    response: Response | None,
    params: CrawlParameters,
) -> None:
    """Convert urllib3 response object and extract links."""
    if response is None or not response.data:
        return
    # add final document URL to known_links
    URL_STORE.add_urls([response.url], visited=True)

    # convert urllib3 response to string and proceed to link extraction
    url = response.url if get_base_url(response.url) == params.base else params.base
    process_links(decode_file(response.data), params, url)


def init_crawl(
    start: str,
    lang: str | None = None,
    rules: RobotFileParser | None = None,
    todo: list[str] | None = None,
    known: list[str] | None = None,
    prune_xpath: str | list[str] | None = None,
    config: ConfigParser = DEFAULT_CONFIG,
) -> CrawlParameters:
    """Initialize crawl by setting variables, copying values to the
    URL store and retrieving the initial page if the crawl starts."""
    params = CrawlParameters(start, lang, rules, prune_xpath, config)

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
    url = URL_STORE.get_url(params.base)
    if not url:
        params.update_metadata(URL_STORE)
        return params

    params.i += 1

    if initial:
        # probe and process homepage
        htmlstring, homepage, new_base_url = probe_alternative_homepage(url, params.config)
        if htmlstring and homepage and new_base_url:
            # follow the site's http -> https upgrade (same host only)
            if params.base.startswith("http://") and new_base_url == "https://" + params.base.removeprefix("http://"):
                params.base = new_base_url
                params.ref = "https://" + params.ref.removeprefix("http://")
            # register potentially new homepage
            URL_STORE.add_urls([homepage])
            # resolve links against the final URL unless the redirect left the crawled host
            process_links(htmlstring, params, url=homepage if get_base_url(homepage) == params.base else url)
    else:
        response = fetch_response(url, decode=False, config=params.config)
        process_response(response, params)

    # optional backup of gathered pages without nav-pages ? ...
    params.update_metadata(URL_STORE)
    return params


def focused_crawler(
    homepage: str,
    max_seen_urls: int = MAX_SEEN_URLS,
    max_known_urls: int = MAX_KNOWN_URLS,
    todo: list[str] | None = None,
    known_links: list[str] | None = None,
    lang: str | None = None,
    config: ConfigParser = DEFAULT_CONFIG,
    rules: RobotFileParser | None = None,
    prune_xpath: str | list[str] | None = None,
) -> tuple[list[str], list[str]]:
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
        List of pages to visit, possibly empty if there are no further pages to visit.
        List of known links.

    """
    params = init_crawl(homepage, lang, rules, todo, known_links, prune_xpath, config)

    sleep_time = URL_STORE.get_crawl_delay(params.base, default=params.config.getfloat("DEFAULT", "SLEEP_TIME"))

    # visit pages until a limit is reached
    while params.is_on and params.i < max_seen_urls and params.known_num < max_known_urls:
        params = crawl_page(params)
        if params.is_on:
            sleep(sleep_time)

    # refocus todo-list on URLs without navigation?
    todo = list(dict.fromkeys(URL_STORE.find_unvisited_urls(params.base)))
    # [u for u in todo if not is_navigation_page(u)]
    known_links = list(dict.fromkeys(URL_STORE.find_known_urls(params.base)))
    return todo, known_links
