"""
Functions needed to scrape metadata from JSON-LD format.
For reference, here is the list of all JSON-LD types: https://schema.org/docs/full.html
"""

import json
import logging
import re
from html import unescape
from re import Pattern
from typing import Any

from .settings import Document
from .utils import HTML_STRIP_TAGS, trim

LOGGER = logging.getLogger(__name__)


JSON_ARTICLE_SCHEMA = {
    "article",
    "backgroundnewsarticle",
    "blogposting",
    "medicalscholarlyarticle",
    "newsarticle",
    "opinionnewsarticle",
    "reportagenewsarticle",
    "scholarlyarticle",
    "socialmediaposting",
    "liveblogposting",
}
JSON_OGTYPE_SCHEMA = {
    "aboutpage",
    "checkoutpage",
    "collectionpage",
    "contactpage",
    "faqpage",
    "itempage",
    "medicalwebpage",
    "profilepage",
    "qapage",
    "realestatelisting",
    "searchresultspage",
    "webpage",
    "website",
    "article",
    "advertisercontentarticle",
    "newsarticle",
    "analysisnewsarticle",
    "askpublicnewsarticle",
    "backgroundnewsarticle",
    "opinionnewsarticle",
    "reportagenewsarticle",
    "reviewnewsarticle",
    "report",
    "satiricalarticle",
    "scholarlyarticle",
    "medicalscholarlyarticle",
    "socialmediaposting",
    "blogposting",
    "liveblogposting",
    "discussionforumposting",
    "techarticle",
    "blog",
    "jobposting",
}
JSON_PUBLISHER_SCHEMA = {"newsmediaorganization", "organization", "webpage", "website"}
JSON_AUTHOR_1 = re.compile(r'"author":[^}[]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}[]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_2 = re.compile(r'"[Pp]erson"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_REMOVE = re.compile(
    r',?(?:"\w+":?[:|,\[])?{?"@type":"(?:[Ii]mageObject|[Oo]rganization|[Ww]eb[Pp]age)",[^}[]+}[\]|}]?'
)
JSON_PUBLISHER = re.compile(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', re.DOTALL)
JSON_TYPE = re.compile(r'"@type"\s*:\s*"([^"]*)"', re.DOTALL)
JSON_CATEGORY = re.compile(r'"articleSection": ?"([^"\\]+)', re.DOTALL)
JSON_MATCH = re.compile(r'"author":|"person":', flags=re.IGNORECASE)
JSON_REMOVE_HTML = re.compile(r"<[^>]+>")
JSON_SCHEMA_ORG = re.compile(r"^https?://schema\.org", flags=re.IGNORECASE)
JSON_UNICODE_REPLACE = re.compile(r"\\u([0-9a-fA-F]{4})")

AUTHOR_ATTRS = ("givenName", "additionalName", "familyName")

JSON_NAME = re.compile(r'"@type":"[Aa]rticle", ?"name": ?"([^"\\]+)', re.DOTALL)
JSON_HEADLINE = re.compile(r'"headline": ?"([^"\\]+)', re.DOTALL)
JSON_SEQ = [('"name"', JSON_NAME), ('"headline"', JSON_HEADLINE)]

AUTHOR_PREFIX = re.compile(r"^([a-zäöüß]+(ed|t))? ?(written by|words by|words|by|von|from) ", flags=re.IGNORECASE)
AUTHOR_REMOVE_NUMBERS = re.compile(r"\d.+?$")
AUTHOR_TWITTER = re.compile(r"@[\w]+")
AUTHOR_REPLACE_JOIN = re.compile(r"[._+]")
AUTHOR_REMOVE_NICKNAME = re.compile(r'["‘({\[’\'][^"]+?[‘’"\')\]}]')
AUTHOR_REMOVE_SPECIAL = re.compile(r"[^\w]+$|[:()?*$#!%/<>{}~¿]")
AUTHOR_REMOVE_PREPOSITION = re.compile(r"\b\s+(am|on|for|at|in|to|from|of|via|with|—|-|–)\s+(.*)", flags=re.IGNORECASE)
AUTHOR_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
AUTHOR_SPLIT = re.compile(r"/|;|,|\||&|(?:^|\W)[ua]nd(?:$|\W)", flags=re.IGNORECASE)
AUTHOR_EMOJI_REMOVE = re.compile(
    "["
    "\U00002700-\U000027be"  # Dingbats
    "\U0001f600-\U0001f64f"  # Emoticons
    "\U00002600-\U000026ff"  # Miscellaneous Symbols
    "\U0001f300-\U0001f5ff"  # Miscellaneous Symbols And Pictographs
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\U0001f680-\U0001f6ff"  # Transport and Map Symbols
    "]+",
    flags=re.UNICODE,
)


def is_plausible_sitename(metadata: Document, candidate: Any, content_type: str | None = None) -> bool:
    """Determine if the candidate should be used as sitename."""
    if candidate and isinstance(candidate, str):
        if not metadata.sitename or (len(metadata.sitename) < len(candidate) and content_type != "webpage"):
            return True
        if metadata.sitename and metadata.sitename.startswith("http") and not candidate.startswith("http"):
            return True
    return False


def _get_content_type(content: dict[str, Any]) -> str | None:
    """Return a normalized JSON-LD type name or None."""
    raw_type = content.get("@type")
    if not raw_type:
        return None
    content_type = raw_type[0] if isinstance(raw_type, list) else raw_type
    return content_type.lower()


def _handle_json_publisher_object(content: dict[str, Any], metadata: Document) -> None:
    """Handle a nested publisher object, if one exists."""
    publisher = content.get("publisher")
    if isinstance(publisher, dict) and is_plausible_sitename(metadata, publisher.get("name")):
        metadata.sitename = publisher["name"]


def _extract_json_author_name(author: Any) -> str | None:
    """Extract a string author name from a JSON-LD author object."""
    if isinstance(author, str):
        author = {"name": author}
    if "@type" in author and author["@type"] != "Person":
        return None

    author_name = None
    if "name" in author:
        author_name = author.get("name")
        if isinstance(author_name, list):
            author_name = "; ".join(author_name).strip("; ")
        elif isinstance(author_name, dict) and "name" in author_name:
            author_name = author_name["name"]
    elif "givenName" in author and "familyName" in author:
        author_name = " ".join(author[x] for x in AUTHOR_ATTRS if x in author)

    return author_name if isinstance(author_name, str) else None


def _handle_json_author_field(author_value: Any, metadata: Document) -> None:
    """Parse and normalize a JSON-LD author field."""
    if isinstance(author_value, str):
        try:
            author_value = json.loads(author_value)
        except json.JSONDecodeError:
            metadata.author = normalize_authors(metadata.author, author_value)
            return

    if not isinstance(author_value, list):
        author_value = [author_value]

    for author in author_value:
        author_name = _extract_json_author_name(author)
        if author_name:
            metadata.author = normalize_authors(metadata.author, author_name)


def _handle_json_article_fields(content: dict[str, Any], metadata: Document, content_type: str) -> None:
    """Handle author, category, and title fields for article-like JSON-LD nodes."""
    if "author" in content:
        _handle_json_author_field(content["author"], metadata)

    if not metadata.categories and "articleSection" in content:
        if isinstance(content["articleSection"], str):
            metadata.categories = [content["articleSection"]]
        else:
            metadata.categories = list(filter(None, content["articleSection"]))

    if not metadata.title:
        if "name" in content and content_type == "article":
            metadata.title = content["name"]
        elif "headline" in content:
            metadata.title = content["headline"]


def _handle_json_content(content: dict[str, Any], metadata: Document) -> None:
    """Handle the main JSON-LD payload based on @type."""
    content_type = _get_content_type(content)
    if content_type is None:
        return

    if content_type in JSON_OGTYPE_SCHEMA and not metadata.pagetype:
        metadata.pagetype = normalize_json(content_type)

    if content_type in JSON_PUBLISHER_SCHEMA:
        candidate = content.get("name") or content.get("legalName") or content.get("alternateName")
        if is_plausible_sitename(metadata, candidate, content_type):
            metadata.sitename = candidate
    elif content_type == "person":
        if isinstance(content.get("name"), str) and not content["name"].startswith("http"):
            metadata.author = normalize_authors(metadata.author, content["name"])
    elif content_type in JSON_ARTICLE_SCHEMA:
        _handle_json_article_fields(content, metadata, content_type)


def process_parent(parent: Any, metadata: Document) -> Document:
    "Find and extract selected metadata from JSON parts."
    for content in filter(None, parent):
        _handle_json_publisher_object(content, metadata)
        _handle_json_content(content, metadata)
    return metadata


def extract_json(schema: list[Any] | dict[str, str], metadata: Document) -> Document:
    """Parse and extract metadata from JSON-LD data"""
    if isinstance(schema, dict):
        schema = [schema]

    # collect content from every valid block, then process once (no short-circuit on a flat object)
    parents: list[Any] = []
    for parent in schema:
        context = parent.get("@context")

        if context and isinstance(context, str) and JSON_SCHEMA_ORG.match(context):
            if "@graph" in parent:
                graph = parent["@graph"]
                parents.extend(graph if isinstance(graph, list) else [graph])
            elif (
                "@type" in parent
                and isinstance(parent["@type"], str)
                and "liveblogposting" in parent["@type"].lower()
                and "liveBlogUpdate" in parent
            ):
                updates = parent["liveBlogUpdate"]
                parents.extend(updates if isinstance(updates, list) else [updates])
            else:
                parents.append(parent)

    return process_parent(parents, metadata)


def extract_json_author(elemtext: str, regular_expression: Pattern[str]) -> str | None:
    """Crudely extract author names from JSON-LD data"""
    authors = None
    mymatch = regular_expression.search(elemtext)
    while mymatch:
        # first matching group (JSON_AUTHOR_1 has two)
        name = next(filter(None, mymatch.groups()), None)
        if not name or " " not in name:
            break
        authors = normalize_authors(authors, name)
        elemtext = regular_expression.sub(r"", elemtext, count=1)
        mymatch = regular_expression.search(elemtext)
    return authors or None


def extract_json_parse_error(elem: str, metadata: Document) -> Document:
    """Crudely extract metadata from JSON-LD data"""
    # author info
    element_text_author = JSON_AUTHOR_REMOVE.sub("", elem)
    author = extract_json_author(element_text_author, JSON_AUTHOR_1) or extract_json_author(element_text_author, JSON_AUTHOR_2)
    if author:
        metadata.author = author

    # try to extract page type as an alternative to og:type
    if "@type" in elem:
        mymatch = JSON_TYPE.search(elem)
        if mymatch:
            candidate = normalize_json(mymatch[1].lower())
            if candidate in JSON_OGTYPE_SCHEMA:
                metadata.pagetype = candidate

    # try to extract publisher
    if '"publisher"' in elem:
        mymatch = JSON_PUBLISHER.search(elem)
        if mymatch and "," not in mymatch[1]:
            candidate = normalize_json(mymatch[1])
            if is_plausible_sitename(metadata, candidate):
                metadata.sitename = candidate

    # category
    if '"articleSection"' in elem:
        mymatch = JSON_CATEGORY.search(elem)
        if mymatch:
            metadata.categories = [normalize_json(mymatch[1])]

    # try to extract title
    for key, regex in JSON_SEQ:
        if key in elem and not metadata.title:
            mymatch = regex.search(elem)
            if mymatch:
                metadata.title = normalize_json(mymatch[1])
                break

    return metadata


def normalize_json(string: str) -> str:
    "Normalize unicode strings and trim the output"
    if "\\" in string:
        string = string.replace("\\n", "").replace("\\r", "").replace("\\t", "")
        string = JSON_UNICODE_REPLACE.sub(lambda match: chr(int(match[1], 16)), string)
        string = "".join(c for c in string if ord(c) < 0xD800 or ord(c) > 0xDFFF)
        string = unescape(string)
    return trim(JSON_REMOVE_HTML.sub("", string))


def normalize_authors(current_authors: str | None, author_string: str) -> str | None:
    """Normalize author info to focus on author names only"""
    new_authors = []
    if author_string.lower().startswith("http") or AUTHOR_EMAIL.match(author_string):
        return current_authors
    if current_authors is not None:
        new_authors = current_authors.split("; ")
    # fix to code with unicode
    if "\\u" in author_string:
        try:
            author_string = author_string.encode().decode("unicode_escape")
        except UnicodeDecodeError:
            LOGGER.debug("invalid unicode escape in author: %s", author_string)
    # fix html entities
    if "&#" in author_string or "&amp;" in author_string:
        author_string = unescape(author_string)
    # remove html tags
    author_string = HTML_STRIP_TAGS.sub("", author_string)
    # examine names
    for author in AUTHOR_SPLIT.split(author_string):
        author = trim(author)
        # remove emoji
        author = AUTHOR_EMOJI_REMOVE.sub("", author)
        # remove @username
        author = AUTHOR_TWITTER.sub("", author)
        # replace special characters with space
        author = trim(AUTHOR_REPLACE_JOIN.sub(" ", author))
        author = AUTHOR_REMOVE_NICKNAME.sub("", author)
        # remove special characters
        author = AUTHOR_REMOVE_SPECIAL.sub("", author)
        author = AUTHOR_PREFIX.sub("", author)
        author = AUTHOR_REMOVE_NUMBERS.sub("", author)
        author = AUTHOR_REMOVE_PREPOSITION.sub("", author)
        # skip empty or improbably long strings
        # simple heuristics, regex or vowel tests also possible
        if not author or (len(author) >= 50 and " " not in author and "-" not in author):
            continue
        # title case
        if not author[0].isupper():
            author = author.title()
        if author not in new_authors:
            new_authors.append(author)
    # keep only the fullest form of each name (drop names contained in another)
    new_authors = [n for n in new_authors if not any(n != m and n in m for m in new_authors)]
    if len(new_authors) == 0:
        return current_authors
    return "; ".join(new_authors).strip("; ")
