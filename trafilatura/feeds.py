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

from .downloads import fetch_url
from .settings import MAX_LINKS
from .utils import is_similar_domain, load_html

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
        domainname: str,
        reference: str,
        external: bool = False,
        target_lang: Optional[str] = None,
    ) -> None:
        self.base: str = baseurl
        self.domain: str = domainname
        self.ext: bool = external
        self.lang: Optional[str] = target_lang
        self.ref: str = reference


def handle_link_list(linklist: List[str], params: FeedParameters) -> List[str]:
    """Examine links to determine if they are valid and
    lead to a web page"""
    output_links = []
    # sort and uniq
    for item in sorted(set(linklist)):
        # fix and check
        link = fix_relative_urls(params.base, item)
        # control output for validity
        checked = check_url(link, language=params.lang)
        if checked is not None:
            if (
                not params.ext
                and not "feed" in link
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


def extract_links(feed_string: str, params: FeedParameters) -> List[str]:
    """Extract links from Atom and RSS feeds"""
    feed_links = []
    # check if it's a feed
    if feed_string is None:
        LOGGER.debug("Empty feed: %s", params.domain)
        return feed_links
    feed_string = feed_string.strip()
    # typical first and second lines absent
    if not FEED_OPENING.match(feed_string) and not (
        "<rss" in feed_string[:100] or "<feed" in feed_string[:100]
    ):
        # could be JSON
        if feed_string.startswith("{"):
            try:
                feed_dict = json.loads(feed_string)
                if "items" in feed_dict:
                    for item in feed_dict["items"]:
                        # fallback: https://www.jsonfeed.org/version/1.1/
                        if "url" in item or "id" in item:
                            feed_links.append(item.get("url") or item.get("id"))
            except json.decoder.JSONDecodeError:
                LOGGER.debug("JSON decoding error: %s", params.domain)
        else:
            LOGGER.debug("Possibly invalid feed: %s", params.domain)
        return feed_links
    # could be Atom
    if "<link " in feed_string:
        for link in (m[0] for m in islice(LINK_ATTRS.finditer(feed_string), MAX_LINKS)):
            if "atom+xml" in link or 'rel="self"' in link:
                continue
            feedlink = LINK_HREF.search(link)[1]
            # if '"' in feedlink:
            #    feedlink = feedlink.split('"')[0]
            feed_links.append(feedlink)
    # could be RSS
    elif "<link>" in feed_string:
        feed_links.extend(
            [
                m[1].strip()
                for m in islice(
                    LINK_ELEMENTS.finditer(feed_string, re.DOTALL), MAX_LINKS
                )
            ]
        )

    # refine
    output_links = handle_link_list(feed_links, params)
    output_links = [l for l in output_links if l != params.ref and l.count("/") > 2]
    # log result
    if feed_links:
        LOGGER.debug(
            "Links found: %s of which %s valid", len(feed_links), len(output_links)
        )
    else:
        LOGGER.debug("Invalid feed for %s", params.domain)
    return output_links


def determine_feed(htmlstring: str, params: FeedParameters) -> List[str]:
    """Try to extract the feed URL from the home page.
    Adapted from http://www.aaronsw.com/2002/feedfinder/"""
    # parse the page to look for feeds
    tree = load_html(htmlstring)
    # safeguard
    if tree is None:
        LOGGER.debug("Invalid HTML/Feed page: %s", params.base)
        return []
    feed_urls = []
    for linkelem in tree.xpath('//link[@rel="alternate"][@href]'):
        # most common case + websites like geo.de
        if (
            "type" in linkelem.attrib and linkelem.get("type") in FEED_TYPES
        ) or LINK_VALIDATION_RE.search(linkelem.get("href", "")):
            feed_urls.append(linkelem.get("href"))
    # backup
    if not feed_urls:
        for linkelem in tree.xpath("//a[@href]"):
            link = linkelem.get("href", "")
            if LINK_VALIDATION_RE.search(link):
                feed_urls.append(link)
    # refine
    output_urls = []
    for link in dict.fromkeys(feed_urls):
        link = fix_relative_urls(params.base, link)
        link = clean_url(link)
        if link is None or link == params.ref or not is_valid_url(link):
            continue
        if BLACKLIST.search(link):
            continue
        output_urls.append(link)
    # log result
    LOGGER.debug(
        "Feed URLs found: %s of which %s valid", len(feed_urls), len(output_urls)
    )
    return output_urls


def find_feed_urls(
    url: str, target_lang: Optional[str] = None, external: bool = False, sleep_time: int = 2,
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
    domainname, baseurl = get_hostinfo(url)
    if domainname is None:
        LOGGER.warning("Invalid URL: %s", url)
        return []
    params = FeedParameters(baseurl, domainname, url, external, target_lang)
    urlfilter = None
    downloaded = fetch_url(url)
    if downloaded is not None:
        # assume it's a feed
        feed_links = extract_links(downloaded, params)
        if len(feed_links) == 0:
            # assume it's a web page
            for feed in determine_feed(downloaded, params):
                feed_string = fetch_url(feed)
                feed_links.extend(extract_links(feed_string, params))
            # filter triggered, prepare it
            if len(url) > len(baseurl) + 2:
                urlfilter = url
        # return links found
        if len(feed_links) > 0:
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug("%s feed links found for %s", len(feed_links), domainname)
            return feed_links
        LOGGER.debug("No usable feed links found: %s", url)
    else:
        LOGGER.error("Could not download web page: %s", url)
        if url.strip("/") != baseurl:
            sleep(sleep_time)
            return try_homepage(baseurl, target_lang)
    # try alternative: Google News
    if target_lang is not None:
        downloaded = fetch_url(
            f"https://news.google.com/rss/search?q=site:{baseurl}&hl={target_lang}&scoring=n&num=100"
        )
        if downloaded is not None:
            feed_links = extract_links(downloaded, params)
            feed_links = filter_urls(feed_links, urlfilter)
            LOGGER.debug(
                "%s Google news links found for %s", len(feed_links), domainname
            )
            return feed_links
    return []


def try_homepage(baseurl: str, target_lang: Optional[str]) -> List[str]:
    """Shift into reverse and try the homepage instead of the particular feed
    page that was given as input."""
    LOGGER.debug("Probing homepage for feeds instead: %s", baseurl)
    return find_feed_urls(baseurl, target_lang)
