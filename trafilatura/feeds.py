"""
Examining feeds and extracting links for further processing.
"""

import json
import logging
import re

from itertools import islice
from time import sleep
from typing import List, Optional

from courlan import (
    check_url,
    clean_url,
    filter_urls,
    fix_relative_urls,
    get_hostinfo,
    is_valid_url,
)

from .deduplication import is_similar_domain
from .downloads import fetch_url
from .settings import MAX_LINKS
from .utils import load_html

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

LINK_ATTRS = re.compile(r'<link .*?href=".+?"')
LINK_HREF = re.compile(r'href="(.+?)"')
LINK_ELEMENTS = re.compile(
    r"<link>(?:\s*)(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?(?:\s*)</link>"
)

BLACKLIST = re.compile(r"\bcomments\b")  # no comment feed

LINK_VALIDATION_RE = re.compile(
    r"\.(?:atom|rdf|rss|xml)$|"
    r"\b(?:atom|rss)\b|"
    r"\?type=100$|"  # Typo3
    r"feeds/posts/default/?$|"  # Blogger
    r"\?feed=(?:atom|rdf|rss|rss2)|"
    r"feed$"  # Generic
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
        target_lang: Optional[str] = None,
    ) -> None:
        self.base: str = baseurl
        self.domain: str = domain
        self.ext: bool = external
        self.lang: Optional[str] = target_lang
        self.ref: str = reference


def is_potential_feed(feed_string: str) -> bool:
    "Check if the string could be a feed."
    if FEED_OPENING.match(feed_string):
        return True
    beginning = feed_string[:100]
    return "<rss" in beginning or "<feed" in beginning


def handle_link_list(linklist: List[str], params: FeedParameters) -> List[str]:
    """Examine links to determine if they are valid and
    lead to a web page"""
    output_links = []

    for item in sorted(set(linklist)):
        link = fix_relative_urls(params.base, item)
        checked = check_url(link, language=params.lang)

        if checked is not None:
            if (
                not params.ext
                and "feed" not in link
                and not is_similar_domain(params.domain, checked[1])
            ):
                LOGGER.warning(
                    "Rejected, diverging domain names: %s %s", params.domain, checked[1]
                )
            else:
                output_links.append(checked[0])
        # Feedburner/Google feeds
        elif "feedburner" in item or "feedproxy" in item:
            output_links.append(item)

    return output_links


def find_links(feed_string: str, params: FeedParameters) -> List[str]:
    "Try different feed types and return the corresponding links."
    if not is_potential_feed(feed_string):
        # JSON
        if feed_string.startswith("{"):
            try:
                # fallback: https://www.jsonfeed.org/version/1.1/
                candidates = [
                    item.get("url") or item.get("id")
                    for item in json.loads(feed_string).get("items", [])
                ]
                return [c for c in candidates if c is not None]
            except json.decoder.JSONDecodeError:
                LOGGER.debug("JSON decoding error: %s", params.domain)
        else:
            LOGGER.debug("Possibly invalid feed: %s", params.domain)
        return []

    # Atom
    if "<link " in feed_string:
        return [
            LINK_HREF.search(link)[1]  # type: ignore[index]
            for link in (
                m[0] for m in islice(LINK_ATTRS.finditer(feed_string), MAX_LINKS)
            )
            if "atom+xml" not in link and 'rel="self"' not in link
        ]
        # if '"' in feedlink:
        #    feedlink = feedlink.split('"')[0]

    # RSS
    if "<link>" in feed_string:
        return [
            m[1].strip()
            for m in islice(LINK_ELEMENTS.finditer(feed_string, re.DOTALL), MAX_LINKS)
        ]

    return []


def extract_links(feed_string: str, params: FeedParameters) -> List[str]:
    "Extract and refine links from Atom, RSS and JSON feeds."
    if not feed_string:
        LOGGER.debug("Empty feed: %s", params.domain)
        return []

    feed_links = find_links(feed_string.strip(), params)

    output_links = [
        link
        for link in handle_link_list(feed_links, params)
        if link != params.ref and link.count("/") > 2
    ]

    if feed_links:
        LOGGER.debug(
            "Links found: %s of which %s valid", len(feed_links), len(output_links)
        )
    else:
        LOGGER.debug("Invalid feed for %s", params.domain)

    return output_links


def determine_feed(htmlstring: str, params: FeedParameters) -> List[str]:
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
        if link.get("type") in FEED_TYPES
        or LINK_VALIDATION_RE.search(link.get("href", ""))
    ]

    # backup
    if not feed_urls:
        feed_urls = [
            link.get("href", "")
            for link in tree.xpath("//a[@href]")
            if LINK_VALIDATION_RE.search(link.get("href", ""))
        ]

    # refine
    output_urls = []
    for link in dict.fromkeys(feed_urls):
        link = fix_relative_urls(params.base, link)
        link = clean_url(link)
        if (
            link
            and link != params.ref
            and is_valid_url(link)
            and not BLACKLIST.search(link)
        ):
            output_urls.append(link)

    # log result
    LOGGER.debug(
        "Feed URLs found: %s of which %s valid", len(feed_urls), len(output_urls)
    )
    return output_urls


def probe_gnews(params: FeedParameters, urlfilter: Optional[str]) -> List[str]:
    "Alternative way to gather feed links: Google News."
    if params.lang:
        downloaded = fetch_url(
            f"https://news.google.com/rss/search?q=site:{params.domain}&hl={params.lang}&scoring=n&num=100"
        )
        if downloaded:
            feed_links = extract_links(downloaded, params)
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug(
                "%s Google news links found for %s", len(feed_links), params.domain
            )
            return feed_links
    return []


def find_feed_urls(
    url: str,
    target_lang: Optional[str] = None,
    external: bool = False,
    sleep_time: float = 2.0,
) -> List[str]:
    """Try to find feed URLs.

    Args:
        url: Webpage or feed URL as string.
             Triggers URL-based filter if the webpage isn't a homepage.
        target_lang: Define a language to filter URLs based on heuristics
                     (two-letter string, ISO 639-1 format).
        external: Similar hosts only or external URLs
                  (boolean, defaults to False).
        sleep_time: Wait between requests on the same website.

    Returns:
        The extracted links as a list (sorted list of unique links).

    """
    domain, baseurl = get_hostinfo(url)
    if domain is None:
        LOGGER.warning("Invalid URL: %s", url)
        return []

    params = FeedParameters(baseurl, domain, url, external, target_lang)
    urlfilter = None
    downloaded = fetch_url(url)

    if downloaded is not None:
        # assume it's a feed
        feed_links = extract_links(downloaded, params)
        if not feed_links:
            # assume it's a web page
            for feed in determine_feed(downloaded, params):
                feed_string = fetch_url(feed)
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
            return try_homepage(baseurl, target_lang)

    return probe_gnews(params, urlfilter)


def try_homepage(baseurl: str, target_lang: Optional[str]) -> List[str]:
    """Shift into reverse and try the homepage instead of the particular feed
    page that was given as input."""
    LOGGER.debug("Probing homepage for feeds instead: %s", baseurl)
    return find_feed_urls(baseurl, target_lang)
