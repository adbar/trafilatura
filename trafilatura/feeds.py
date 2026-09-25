"""
Examining feeds and extracting links for further processing.
"""

import json
import logging
import re
from configparser import ConfigParser
from itertools import islice
from time import sleep

from courlan import (
    check_url,
    clean_url,
    filter_urls,
    get_hostinfo,
    is_valid_url,
)

from .deduplication import is_similar_domain
from .downloads import fetch_url
from .settings import DEFAULT_CONFIG, MAX_FEEDS_CHECKED, MAX_LINKS
from .utils import load_html, safe_relative_url

LOGGER = logging.getLogger(__name__)

# https://www.iana.org/assignments/media-types/media-types.xhtml
# standard + potential types
FEED_TYPES = {
    "application/atom",  # not IANA-compatible
    "application/atom+xml",
    "application/feed+json",  # not IANA-compatible
    "application/json",
    "application/rdf",  # not IANA-compatible
    "application/rdf+xml",
    "application/rss",  # not IANA-compatible
    "application/rss+xml",
    "application/x.atom+xml",  # not IANA-compatible
    "application/x-atom+xml",  # not IANA-compatible
    "application/xml",
    "text/atom",  # not IANA-compatible
    "text/atom+xml",
    "text/plain",
    "text/rdf",  # not IANA-compatible
    "text/rdf+xml",
    "text/rss",  # not IANA-compatible
    "text/rss+xml",
    "text/xml",
}

FEED_OPENING = re.compile(r"<(feed|rss|\?xml)")

LINK_ATTRS = re.compile(r"""<link\s+(?:[^>"']|"[^"]*"|'[^']*')*["']?/?>""")
LINK_ATTRIBUTES = re.compile(r"""\s([\w:-]+)\s*=\s*(["'])(.*?)\2""", re.DOTALL)
LINK_ELEMENTS = re.compile(r"<link>(?:\s*)(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?(?:\s*)</link>", re.DOTALL)

BLACKLIST = re.compile(r"\bcomments\b")  # no comment feed

LINK_VALIDATION_RE = re.compile(
    r"\.(?:atom|rdf|rss|xml)$|"
    r"\b(?:atom|rss)\b|"
    r"\?type=100$|"  # Typo3
    r"feeds/posts/default/?$|"  # Blogger
    r"\?feed=(?:atom|rdf|rss|rss2)|"
    r"feed$",  # Generic
)


class FeedParameters:
    "Store necessary information to proceed a feed."

    __slots__ = ["base", "domain", "ext", "lang", "ref"]

    def __init__(
        self,
        baseurl: str,
        domain: str,
        reference: str,
        external: bool = False,
        target_lang: str | None = None,
    ) -> None:
        self.base: str = baseurl
        self.domain: str = domain
        self.ext: bool = external
        self.lang: str | None = target_lang
        self.ref: str = reference


def is_potential_feed(feed_string: str) -> bool:
    "Check if the string could be a feed."
    if FEED_OPENING.match(feed_string):
        return True
    beginning = feed_string[:100]
    return "<rss" in beginning or "<feed" in beginning


def handle_link_list(linklist: list[str], params: FeedParameters) -> list[str]:
    """Examine links to determine if they are valid and
    lead to a web page"""
    output_links = []

    for item in sorted(set(linklist)):
        link = safe_relative_url(params.base, item)
        checked = check_url(link, language=params.lang)

        if checked is not None:
            if not params.ext and "feed" not in link and not is_similar_domain(params.domain, checked[1]):
                LOGGER.warning("Rejected, diverging domain names: %s %s", params.domain, checked[1])
            else:
                output_links.append(checked[0])
        # Feedburner/Google feeds
        elif "feedburner" in item or "feedproxy" in item:
            output_links.append(item)

    return output_links


def find_links(feed_string: str, params: FeedParameters) -> list[str]:
    "Try different feed types and return the corresponding links."
    if not is_potential_feed(feed_string):
        # JSON
        if feed_string.startswith("{"):
            try:
                # fallback: https://www.jsonfeed.org/version/1.1/
                items = json.loads(feed_string).get("items", [])
                if not isinstance(items, list):
                    return []
                candidates = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    for key in ("url", "id"):
                        candidate = item.get(key)
                        if isinstance(candidate, str) and candidate:
                            candidates.append(candidate)
                            break
                return candidates
            except (json.decoder.JSONDecodeError, RecursionError):
                LOGGER.debug("JSON decoding error: %s", params.domain)
        else:
            LOGGER.debug("Possibly invalid feed: %s", params.domain)
        return []

    # Atom
    if LINK_ATTRS.search(feed_string):
        links = []
        for match in islice(LINK_ATTRS.finditer(feed_string), MAX_LINKS):
            attributes = {attr[1]: attr[3] for attr in LINK_ATTRIBUTES.finditer(match[0])}
            if attributes.get("href") and attributes.get("rel") != "self" and "atom+xml" not in attributes.get("type", ""):
                links.append(attributes["href"])
        return links

    # RSS
    if "<link>" in feed_string:
        return [m[1].strip() for m in islice(LINK_ELEMENTS.finditer(feed_string), MAX_LINKS)]

    return []


def extract_links(feed_string: str, params: FeedParameters) -> list[str]:
    "Extract and refine links from Atom, RSS and JSON feeds."
    if not feed_string:
        LOGGER.debug("Empty feed: %s", params.domain)
        return []

    feed_links = find_links(feed_string.strip(), params)

    output_links = [link for link in handle_link_list(feed_links, params) if link != params.ref and link.count("/") > 2]

    if feed_links:
        LOGGER.debug("Links found: %s of which %s valid", len(feed_links), len(output_links))
    else:
        LOGGER.debug("Invalid feed for %s", params.domain)

    return output_links


def determine_feed(htmlstring: str, params: FeedParameters) -> list[str]:
    """Parse the HTML and try to extract feed URLs from the home page.
    Adapted from http://www.aaronsw.com/2002/feedfinder/"""
    tree = load_html(htmlstring)
    if tree is None:
        LOGGER.debug("Invalid HTML/Feed page: %s", params.base)
        return []

    # most common case + websites like geo.de
    feed_urls = [
        link.get("href", "")
        for link in tree.xpath('//link[@rel="alternate"][@href]')
        # normalize the type attribute (e.g. "application/rss+xml; charset=UTF-8")
        if link.get("type", "").split(";")[0].strip().lower() in FEED_TYPES or LINK_VALIDATION_RE.search(link.get("href", ""))
    ]

    # backup
    if not feed_urls:
        feed_urls = [
            link.get("href", "") for link in tree.xpath("//a[@href]") if LINK_VALIDATION_RE.search(link.get("href", ""))
        ]

    # refine
    output_urls = []
    for link in dict.fromkeys(feed_urls):
        link = safe_relative_url(params.base, link)
        link = clean_url(link)
        if link and link != params.ref and is_valid_url(link) and not BLACKLIST.search(link):
            output_urls.append(link)

    # log result
    LOGGER.debug("Feed URLs found: %s of which %s valid", len(feed_urls), len(output_urls))
    return output_urls


def probe_gnews(params: FeedParameters, urlfilter: str | None, config: ConfigParser = DEFAULT_CONFIG) -> list[str]:
    "Alternative way to gather feed links: Google News."
    if params.lang:
        downloaded = fetch_url(
            f"https://news.google.com/rss/search?q=site:{params.domain}&hl={params.lang}&scoring=n&num=100",
            config=config,
        )
        if downloaded:
            feed_links = extract_links(downloaded, params)
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug("%s Google news links found for %s", len(feed_links), params.domain)
            return feed_links
    return []


def find_feed_urls(
    url: str,
    target_lang: str | None = None,
    external: bool = False,
    sleep_time: float = 2.0,
    config: ConfigParser = DEFAULT_CONFIG,
) -> list[str]:
    """Try to find feed URLs.

    Args:
        url: Webpage or feed URL as string.
             Triggers URL-based filter if the webpage isn't a homepage.
        target_lang: Define a language to filter URLs based on heuristics
                     (two-letter string, ISO 639-1 format).
        external: Similar hosts only or external URLs
                  (boolean, defaults to False).
        sleep_time: Wait between requests on the same website.
        config: Pass configuration values for download control.

    Returns:
        The extracted links as a list (sorted list of unique links).

    """
    domain, baseurl = get_hostinfo(url)
    if domain is None:
        LOGGER.warning("Invalid URL: %s", url)
        return []

    params = FeedParameters(baseurl, domain, url, external, target_lang)
    urlfilter = None
    downloaded = fetch_url(url, config=config)

    if downloaded is not None:
        # assume it's a feed
        feed_links = extract_links(downloaded, params)
        if not feed_links:
            # assume it's a web page
            for i, feed in enumerate(determine_feed(downloaded, params)[:MAX_FEEDS_CHECKED]):
                if i:
                    sleep(sleep_time)
                feed_string = fetch_url(feed, config=config)
                if feed_string:
                    feed_links.extend(extract_links(feed_string, params))
            # filter triggered, prepare it
            if len(url) > len(baseurl) + 2:
                urlfilter = url
        # return links found
        if feed_links:
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug("%s feed links found for %s", len(feed_links), domain)
            return feed_links
        LOGGER.debug("No usable feed links found: %s", url)
    else:
        LOGGER.error("Could not download web page: %s", url)
        if url.strip("/") != baseurl:
            sleep(sleep_time)
            return try_homepage(baseurl, target_lang, external, sleep_time, config)

    return probe_gnews(params, urlfilter, config)


def try_homepage(
    baseurl: str,
    target_lang: str | None,
    external: bool,
    sleep_time: float,
    config: ConfigParser = DEFAULT_CONFIG,
) -> list[str]:
    """Shift into reverse and try the homepage instead of the particular feed
    page that was given as input."""
    LOGGER.debug("Probing homepage for feeds instead: %s", baseurl)
    return find_feed_urls(baseurl, target_lang, external, sleep_time, config)
