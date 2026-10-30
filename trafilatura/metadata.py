"""
Module bundling all functions needed to scrape metadata from webpages.
"""

import json
import logging
import re
from collections.abc import Callable, Sequence
from copy import deepcopy
from html import unescape
from typing import Any
from urllib.parse import urljoin

from courlan import (
    extract_domain,
    is_valid_url,
    normalize_url,
    validate_url,
)
from htmldate import find_date
from lxml.html import HtmlElement, tostring

from .baseline import block_text
from .htmlprocessing import prune_unwanted_nodes
from .json_metadata import (
    extract_json,
    extract_json_parse_error,
    normalize_authors,
    normalize_json,
    normalize_json_values,
)
from .settings import Document, set_date_params
from .utils import HTML_STRIP_TAGS, load_html, safe_base_url, trim
from .xpaths import (
    AUTHOR_DISCARD_XPATHS,
    AUTHOR_XPATHS,
    CATEGORIES_XPATHS,
    TAGS_XPATHS,
    TITLE_XPATHS,
)

__all__ = ["Document"]

LOGGER = logging.getLogger(__name__)
logging.getLogger("htmldate").setLevel(logging.WARNING)

META_URL = re.compile(r"https?://(?:www\.|w[0-9]+\.)?([^/]+)")

JSON_MINIFY = re.compile(r'("(?:\\.|[^"\\])*")|\s')
JSON_WRAPPER = re.compile(r"^\s*(?://|/\*)?\s*(?:<!\[CDATA\[|<!--)(?:\s*\*/)?|(?://|/\*)?\s*(?:\]\]>|-->)(?:\s*\*/)?\s*$")

TITLE_SEPARATORS = "–•·—|⁄*⋆~‹«<›»>:-"
TITLE_SPLIT = re.compile(rf"(?:\s+[{TITLE_SEPARATORS}])+\s+")
NON_WORD = re.compile(r"\W+")

CLEAN_META_TAGS = re.compile(r'["\']')

LICENSE_REGEX = re.compile(r"/(by-nc-nd|by-nc-sa|by-nc|by-nd|by-sa|by|zero)/([1-9]\.[0-9])")
TEXT_LICENSE_REGEX = re.compile(
    r"(cc|creative commons) (by-nc-nd|by-nc-sa|by-nc|by-nd|by-sa|by|zero) ?([1-9]\.[0-9])?",
    re.IGNORECASE,
)

METANAME_AUTHOR = {
    "article:author",
    "atc-metaauthor",
    "author",
    "authors",
    "byl",
    "citation_author",
    "creator",
    "dc.creator",
    "dc.creator.aut",
    "dc:creator",
    "dcterms.creator",
    "dcterms.creator.aut",
    "dcsext.author",
    "parsely-author",
    "rbauthors",
    "sailthru.author",
    "shareaholic:article_author_name",
}  # questionable: twitter:creator
METANAME_DESCRIPTION = {
    "dc.description",
    "dc:description",
    "dcterms.abstract",
    "dcterms.description",
    "description",
    "sailthru.description",
    "twitter:description",
}
METANAME_PUBLISHER = {
    "article:publisher",
    "citation_journal_title",
    "copyright",
    "dc.publisher",
    "dc:publisher",
    "dcterms.publisher",
    "publisher",
    "sailthru.publisher",
    "rbpubname",
}  # questionable: citation_publisher
METANAME_TAG = {
    "citation_keywords",
    "dcterms.subject",
    "keywords",
    "parsely-tags",
    "shareaholic:keywords",
    "tags",
}
METANAME_TITLE = {
    "citation_title",
    "dc.title",
    "dcterms.title",
    "fb_title",
    "headline",
    "parsely-title",
    "sailthru.title",
    "shareaholic:title",
    "rbtitle",
    "title",
    "twitter:title",
}
METANAME_IMAGE = {
    "image",
    "og:image",
    "og:image:url",
    "og:image:secure_url",
    "twitter:image",
    "twitter:image:src",
}
PROPERTY_AUTHOR = {"author", "article:author"}

# also interesting: article:section

EXTRA_META = {"charset", "http-equiv", "property"}

OG_PROPERTIES = {
    "og:title": "title",
    "og:description": "description",
    "og:site_name": "sitename",
    "og:image": "image",
    "og:image:url": "image",
    "og:image:secure_url": "image",
}

OG_AUTHOR = {"og:author", "og:article:author"}

URL_SELECTORS = ['.//head//link[@rel="canonical"]', ".//head//base", './/head//link[@rel="alternate"][@hreflang="x-default"]']


def normalize_tags(tags: str) -> str:
    """Remove special characters of tags"""
    trimmed = trim(unescape(tags))
    if not trimmed:
        return ""
    return CLEAN_META_TAGS.sub(r"", trimmed)


def invert_citation_name(name: str) -> str:
    "citation_author holds one name per tag, often as 'Last, First': turn it into 'First Last'."
    last, sep, first = (part.strip() for part in name.partition(","))
    # leave lists of full names ("Jane Doe, John Roe") to the regular splitting
    if sep and last and first and "," not in first and (" " not in last or " " not in first):
        return f"{first} {last}"
    return name


def check_authors(authors: str, author_blacklist: set[str]) -> str | None:
    "Check if the authors string correspond to expected values."
    author_blacklist = {a.lower() for a in author_blacklist}
    new_authors = [author.strip() for author in authors.split(";") if author.strip().lower() not in author_blacklist]
    if new_authors:
        return "; ".join(new_authors).strip("; ")
    return None


def extract_meta_json(tree: HtmlElement, metadata: Document, backup_sitename: str | None = None) -> Document:
    """Parse and extract metadata from JSON-LD data"""
    for elem in tree.xpath('.//script[@type="application/ld+json" or @type="application/settings+json"]'):
        if not elem.text:
            continue
        # strip CDATA or comment wrappers, then whitespace outside strings
        element_text = JSON_MINIFY.sub(r"\1", JSON_WRAPPER.sub("", elem.text))
        try:
            # strict=False: trim() handles \n\r\t, but strict JSON rejects the full 0x00-0x1F
            # range; rarer control chars (from encoding issues) would otherwise raise here
            # parse before normalizing: decoding the escapes in the raw text would turn an escaped
            # quote into a string delimiter and escaped angle brackets into tags spanning fields
            schema = normalize_json_values(json.loads(element_text, strict=False))
        except json.JSONDecodeError:
            element_text = normalize_json(element_text)
            try:
                schema = json.loads(element_text, strict=False)
            except json.JSONDecodeError:
                metadata = extract_json_parse_error(element_text, metadata)
                continue
        metadata = extract_json(schema, metadata, backup_sitename)
    return metadata


def extract_opengraph(tree: HtmlElement) -> dict[str, str | None]:
    """Search meta tags following the OpenGraph guidelines (https://ogp.me/)"""
    result = dict.fromkeys(("title", "author", "url", "description", "sitename", "image", "pagetype"))

    # detect OpenGraph schema
    for elem in tree.xpath('.//head/meta[starts-with(@property, "og:")]'):
        property_name, content = elem.get("property"), elem.get("content")
        # safeguard
        if content and not content.isspace():
            if property_name == "og:type":
                result["pagetype"] = content.lower()
            elif property_name in OG_PROPERTIES:
                result[OG_PROPERTIES[property_name]] = content
            elif property_name == "og:url" and not result["url"] and is_valid_url(content):
                result["url"] = content
            elif property_name in OG_AUTHOR:
                result["author"] = normalize_authors(None, content)
        # og:locale
        # elif elem.get('property') == 'og:locale':
        #    pagelocale = elem.get('content')
    return result


def split_title(title: str) -> tuple[str, str] | None:
    "Split a title before its last separator run, e.g. 'Article | Site'."
    matches = list(TITLE_SPLIT.finditer(title))
    if not matches or matches[-1].end() == len(title):
        return None
    return title[: matches[-1].start()], title[matches[-1].end() :]


def strip_site_suffix(title: str, sitename: str | None, hostname: str | None) -> str:
    "Remove the last title segment if it names the site, e.g. 'Article | Site'."
    parts = split_title(title)
    if not parts:
        return title
    last = NON_WORD.sub("", parts[1].lower())
    host = (hostname or "").removeprefix("www.")
    # first host label and registered domain, e.g. 'edition' and 'cnn' for edition.cnn.com
    labels = (host.split(".")[0], (extract_domain("http://" + host) or "").split(".")[0])
    for candidate in (NON_WORD.sub("", name.lower()) for name in (sitename or "", *labels)):
        if (
            candidate
            and last
            and (last == candidate or (len(candidate) > 3 and (candidate in last or (len(last) > 3 and last in candidate))))
        ):
            return parts[0]
    return title


META_FIELDS = {
    "property": {
        "article:tag": "tags",
        "article:publisher": "sitename",
        **dict.fromkeys(PROPERTY_AUTHOR, "author"),
        **{name: "image" for name in METANAME_IMAGE if not name.startswith("og:")},
    },
    "name": {
        **dict.fromkeys(METANAME_TAG, "tags"),
        "twitter:url": "url",
        "twitter:site": "backup",
        "application-name": "backup",
        **dict.fromkeys(METANAME_IMAGE, "image"),
        **dict.fromkeys(METANAME_PUBLISHER, "sitename"),
        **dict.fromkeys(METANAME_DESCRIPTION, "description"),
        **dict.fromkeys(METANAME_TITLE, "title"),
        **dict.fromkeys(METANAME_AUTHOR, "author"),
    },
    "itemprop": {"author": "author", "description": "description", "headline": "title"},
}
BACKUP_ORDER = ("application-name", "twitter:site")


def examine_meta(tree: HtmlElement) -> tuple[Document, str | None]:
    """Search meta tags for relevant information, return a backup sitename separately"""
    # bootstrap from potential OpenGraph tags
    metadata = Document().from_dict(extract_opengraph(tree))
    tags: list[str] = []
    backups: dict[str, str] = {}

    for elem in tree.iterfind(".//head/meta[@content]"):
        content = HTML_STRIP_TAGS.sub("", elem.get("content", "")).strip()
        attr = next((a for a in META_FIELDS if a in elem.attrib), None)
        if not content or attr is None:
            if content and all(key not in elem.attrib for key in EXTRA_META):
                LOGGER.debug("unknown attribute: %s", tostring(elem, encoding="unicode").strip())
            continue
        key = elem.get(attr, "").lower()
        field = META_FIELDS[attr].get(key)
        if field is None and attr == "name" and "twitter:app:name" in key:
            field = "backup"
        if field == "author":
            if key == "citation_author":
                content = invert_citation_name(content)
            metadata.author = normalize_authors(metadata.author, content)
        elif field == "tags":
            tags.append(normalize_tags(content))
        elif field == "backup":
            backups.setdefault(key, content)
        elif field and not getattr(metadata, field) and (field != "url" or is_valid_url(content)):
            setattr(metadata, field, content)

    metadata.tags = tags
    # twitter:app:name variants come last, in document order
    return metadata, next((backups[k] for k in (*BACKUP_ORDER, *backups) if k in backups), None)


def extract_metainfo(
    tree: HtmlElement, expressions: Sequence[Callable[[HtmlElement], Any]], len_limit: int = 200
) -> str | None:
    """Extract meta information"""
    # try all XPath expressions
    for expression in expressions:
        # examine all results
        results = expression(tree)
        for elem in results:
            content = trim(" ".join(elem.itertext()))
            if content and 2 < len(content) < len_limit:
                return content
        if len(results) > 1:
            LOGGER.debug("more than one invalid result: %s %s", expression, len(results))
    return None


def examine_title_element(
    tree: HtmlElement,
) -> tuple[str, str | None, str | None]:
    """Extract text segments out of main <title> element."""
    title = ""
    title_element = tree.find(".//head//title")
    if title_element is not None:
        title = trim(title_element.text_content())
        if parts := split_title(title):
            return title, *parts
    LOGGER.debug("no main title found")
    return title, None, None


def extract_title(tree: HtmlElement) -> str | None:
    """Extract the document title"""
    # only one h1-element: take it
    h1_results = tree.findall(".//h1")
    if len(h1_results) == 1 and (title := block_text(h1_results[0])):
        return title
    # extract using x-paths
    title = extract_metainfo(tree, TITLE_XPATHS) or ""
    if title:
        return title
    # extract using title tag
    title, first, second = examine_title_element(tree)
    for t in (first, second, title):
        if t and "." not in t:
            return t
    # take first non-empty h1-title
    for h1_result in h1_results:
        if title := block_text(h1_result):
            return title
    # take first h2-title
    if h2_results := tree.xpath(".//h2"):
        title = block_text(h2_results[0])
    else:
        LOGGER.debug("no h2 title found")
    return title or None


def extract_author(tree: HtmlElement) -> str | None:
    """Extract the document author(s)"""
    subtree = prune_unwanted_nodes(deepcopy(tree), AUTHOR_DISCARD_XPATHS)
    author = extract_metainfo(subtree, AUTHOR_XPATHS, len_limit=120)
    if author:
        author = normalize_authors(None, author)
    # copyright?
    return author


def extract_url(tree: HtmlElement, default_url: str | None = None) -> str | None:
    """Extract the URL from the canonical link"""
    for selector in URL_SELECTORS:
        element = tree.find(selector)
        url = element.attrib.get("href") if element is not None else None
        if url:
            break

    # protocol-relative URL: only the scheme is missing
    if url and url.startswith("//"):
        url = f"https:{url}"
    # fix relative URLs
    elif url and url.startswith("/"):
        for element in tree.iterfind(".//head//meta[@content]"):
            attrtype = element.get("name") or element.get("property") or ""
            if attrtype.startswith(("og:", "twitter:")):
                base_url = safe_base_url(element.attrib["content"])
                if base_url:
                    # prepend URL
                    url = base_url + url
                    break

    # do not return invalid URLs
    if url:
        validation_result, parsed_url = validate_url(url)
        url = normalize_url(parsed_url) if validation_result and parsed_url else None

    return url or default_url


def extract_catstags(metatype: str, tree: HtmlElement) -> list[str]:
    """Find category and tag information"""
    results: list[str] = []
    regexpr = "/" + metatype.rstrip("y") + "(?:y|ies|s)?/"
    xpath_expression = CATEGORIES_XPATHS if metatype == "category" else TAGS_XPATHS
    # search using custom expressions
    for catexpr in xpath_expression:
        results.extend(block_text(elem) for elem in catexpr(tree) if re.search(regexpr, elem.attrib["href"]))
        if results:
            break
    # category fallback
    if metatype == "category" and not results:
        results.extend(
            element.attrib["content"]
            for element in tree.xpath('.//head//meta[@property="article:section" or contains(@name, "subject")][@content]')
        )
        # optional: search through links
        # if not results:
        #    for elem in tree.xpath('.//a[@href]'):
        #        search for 'category'
    return results


def parse_license_element(element: HtmlElement, strict: bool = False) -> str | None:
    """Probe a link for identifiable free license cues.
    Parse the href attribute first and then the link text."""
    # look for Creative Commons elements
    match = LICENSE_REGEX.search(element.get("href", ""))
    if match:
        return f"CC {match[1].upper()} {match[2]}"
    text = block_text(element)
    if text:
        # check if it could be a CC license
        if strict:
            match = TEXT_LICENSE_REGEX.search(text)
            return match[0] if match else None
        return text
    return None


def extract_license(tree: HtmlElement) -> str | None:
    """Search the HTML code for license information and parse it."""
    # look for links labeled as license
    for element in tree.findall(".//a[@rel][@href]"):
        if "license" not in element.get("rel", "").lower().split():
            continue
        result = parse_license_element(element, strict=False)
        if result is not None:
            return result
    # probe footer elements for CC links
    for element in tree.xpath('.//footer//a[@href]|.//div[contains(@class, "footer") or contains(@id, "footer")]//a[@href]'):
        result = parse_license_element(element, strict=True)
        if result is not None:
            return result
    return None


def extract_metadata(
    filecontent: HtmlElement | str,
    default_url: str | None = None,
    date_config: dict[str, Any] | None = None,
    extensive: bool = True,
    author_blacklist: set[str] | None = None,
) -> Document:
    """Main process for metadata extraction.

    Args:
        filecontent: HTML code as string or parsed tree.
        default_url: Previously known URL of the downloaded document.
        date_config: Provide extraction parameters to htmldate as dict().
        extensive: Use extensive search for date extraction.
        author_blacklist: Provide a blacklist of Author Names as set() to filter out authors.

    Returns:
        A trafilatura.settings.Document containing the extracted metadata information.
        The Document class has .as_dict() method that will return a copy as a dict.
    """
    # init
    author_blacklist = author_blacklist or set()
    date_config = {**set_date_params(extensive), **(date_config or {})}

    # load contents
    tree = load_html(filecontent)
    if tree is None:
        return Document()

    # initialize dict and try to strip meta tags
    metadata, backup_sitename = examine_meta(tree)

    # to check: remove it and replace with author_blacklist in test case
    if metadata.author and " " not in metadata.author:
        metadata.author = None

    # fix: try json-ld metadata and override
    try:
        metadata = extract_meta_json(tree, metadata, backup_sitename)
    except Exception as err:  # bugs in json_metadata.py
        LOGGER.warning("error in JSON metadata extraction: %s", err)
    # Twitter and app names rank below meta tags and JSON-LD, above a WebPage name
    metadata.sitename = metadata.sitename or backup_sitename

    # title
    if not metadata.title:
        metadata.title = extract_title(tree)

    # check author in blacklist
    if metadata.author and author_blacklist:
        metadata.author = check_authors(metadata.author, author_blacklist)
    # author
    if not metadata.author:
        metadata.author = extract_author(tree)
    # recheck author in blacklist
    if metadata.author and author_blacklist:
        metadata.author = check_authors(metadata.author, author_blacklist)

    # url
    if not metadata.url:
        metadata.url = extract_url(tree, default_url)

    # hostname
    if metadata.url:
        metadata.hostname = extract_domain(metadata.url, fast=True)

    # extract date with external module htmldate
    date_config["url"] = metadata.url
    metadata.date = find_date(tree, **date_config)

    # sitename, URLs (e.g. Facebook pages) fall back to the hostname
    if metadata.sitename and metadata.sitename.lower().startswith(("http://", "https://", "www.")):
        metadata.sitename = None
    if not metadata.sitename:
        metadata.sitename = next((p for p in examine_title_element(tree)[1:] if p and "." in p), None)
    if metadata.sitename:
        # scrap Twitter ID
        metadata.sitename = metadata.sitename.lstrip("@")
        # capitalize
        if "." not in metadata.sitename and metadata.sitename.islower():
            metadata.sitename = metadata.sitename.title()
    # use URL
    elif metadata.url:
        mymatch = META_URL.match(metadata.url)
        if mymatch:
            metadata.sitename = mymatch[1]

    # categories
    if not metadata.categories:
        metadata.categories = extract_catstags("category", tree)

    # tags
    if not metadata.tags:
        metadata.tags = extract_catstags("tag", tree)
    # one tag per item, keywords often come as a comma-separated string
    metadata.tags = [t for tag in metadata.tags for t in tag.split(",")]

    # license
    metadata.license = extract_license(tree)

    # safety checks
    metadata.filedate = date_config.get("max_date")
    metadata.clean_and_trim()

    if metadata.title:
        metadata.title = strip_site_suffix(metadata.title, metadata.sitename, metadata.hostname)
    # a dot in the first segment means a host or junk, e.g. 'cdn.org/i.jpg'
    image = metadata.image
    if image and metadata.url and not image.startswith(("http://", "https://")):
        if "." not in image.split("/")[0].strip("."):
            metadata.image = urljoin(metadata.url, image)

    return metadata
