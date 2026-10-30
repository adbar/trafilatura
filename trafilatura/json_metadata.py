"""
Functions needed to scrape metadata from JSON-LD format.
For reference, here is the list of all JSON-LD types: https://schema.org/docs/full.html
"""

import json
import logging
import re
from contextlib import suppress
from html import unescape
from re import Pattern
from typing import Any

from .settings import Document
from .utils import HTML_STRIP_TAGS, as_list, trim

LOGGER = logging.getLogger(__name__)


JSON_ARTICLE_SCHEMA = {
    "advertisercontentarticle",
    "analysisnewsarticle",
    "article",
    "askpublicnewsarticle",
    "backgroundnewsarticle",
    "blogposting",
    "discussionforumposting",
    "medicalscholarlyarticle",
    "newsarticle",
    "opinionnewsarticle",
    "report",
    "reportagenewsarticle",
    "reviewnewsarticle",
    "satiricalarticle",
    "scholarlyarticle",
    "socialmediaposting",
    "liveblogposting",
    "techarticle",
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
JSON_PUBLISHER_SCHEMA = {
    "educationalorganization",
    "governmentorganization",
    "newsmediaorganization",
    "ngo",
    "organization",
    "researchorganization",
    "webpage",
    "website",
}
JSON_SCHEMA_TYPES = JSON_OGTYPE_SCHEMA | JSON_PUBLISHER_SCHEMA | {"person"}
JSON_AUTHOR_1 = re.compile(r'"author":[^}[]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}[]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_2 = re.compile(r'"[Pp]erson"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_REMOVE = re.compile(
    r',?(?:"\w+":?[:|,\[])?{?"@type":"(?:[Ii]mageObject|[Oo]rganization|[Ww]eb[Pp]age)",[^}[]+}[\]|}]?'
)
JSON_PUBLISHER = re.compile(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', re.DOTALL)
JSON_TYPE = re.compile(r'"@type"\s*:\s*"([^"]*)"', re.DOTALL)
JSON_CATEGORY = re.compile(r'"articleSection": ?"([^"\\]+)', re.DOTALL)
JSON_SCHEMA_ORG = re.compile(r"^https?://(?:www\.)?schema\.org", flags=re.IGNORECASE)
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
        if metadata.sitename.startswith("http") and not candidate.startswith("http"):
            return True
    return False


def _json_author_name(author: Any) -> str | None:
    "Return the name of a Person author item, a bare string is a name."
    if isinstance(author, str):
        return author
    if not isinstance(author, dict) or (
        "@type" in author and "person" not in {t.lower() for t in as_list(author["@type"]) if isinstance(t, str)}
    ):
        return None
    name = author.get("name")
    if isinstance(name, list):
        name = "; ".join(n for n in name if isinstance(n, str)).strip("; ")
    elif isinstance(name, dict):
        name = name.get("name")
    elif "name" not in author and "givenName" in author and "familyName" in author:
        name = " ".join(author[x] for x in AUTHOR_ATTRS if x in author)
    return name if isinstance(name, str) else None


def process_parent(parent: Any, metadata: Document, backup_sitename: str | None = None) -> Document:
    "Find and extract selected metadata from JSON parts."
    content: dict[str, Any]
    webpage_name = None
    for content in parent:
        # one malformed item must not discard the others
        if not isinstance(content, dict):
            continue
        # publisher may be a bare string, not a dict
        publisher = content.get("publisher")
        if isinstance(publisher, dict) and is_plausible_sitename(metadata, publisher.get("name")):
            metadata.sitename = publisher["name"]

        if "@type" not in content or not content["@type"]:
            continue

        # Prefer the first recognized type, preserving order among recognized types.
        content_types = as_list(content["@type"])
        content_type = next(
            (
                schema_type
                for schema_type in content_types
                if isinstance(schema_type, str) and schema_type.lower() in JSON_SCHEMA_TYPES
            ),
            content_types[0],
        ).lower()

        # The "pagetype" should only be returned if the page is some kind of an article, category, website...
        if content_type in JSON_OGTYPE_SCHEMA and not metadata.pagetype:
            metadata.pagetype = content_type

        if content_type in JSON_PUBLISHER_SCHEMA:
            candidate = content.get("name") or content.get("legalName") or content.get("alternateName")
            # a WebPage name is usually the page title: last resort only
            if content_type == "webpage":
                webpage_name = webpage_name or candidate
            elif is_plausible_sitename(metadata, candidate, content_type):
                metadata.sitename = candidate

        elif content_type == "person":
            if isinstance(content.get("name"), str) and not content["name"].startswith("http"):
                metadata.author = normalize_authors(metadata.author, content["name"])

        elif content_type in JSON_ARTICLE_SCHEMA:
            # author and person
            authors = content.get("author")
            if isinstance(authors, str):
                # may hold a serialized object, else a plain name
                with suppress(json.JSONDecodeError):
                    authors = json.loads(authors)
            for author in as_list(authors):
                if (name := _json_author_name(author)) is not None:
                    metadata.author = normalize_authors(metadata.author, name)

            # category
            if not metadata.categories and "articleSection" in content:
                if isinstance(content["articleSection"], str):
                    metadata.categories = [content["articleSection"]]
                else:
                    metadata.categories = list(filter(None, content["articleSection"]))

            # try to extract title
            if not metadata.title:
                if "name" in content and content_type == "article":
                    metadata.title = content["name"]
                elif "headline" in content:
                    metadata.title = content["headline"]
    if not backup_sitename and is_plausible_sitename(metadata, webpage_name, "webpage"):
        metadata.sitename = webpage_name
    return metadata


def is_schema_org_context(context: Any) -> bool:
    """Tell if a JSON-LD @context refers to schema.org: a string, an object
    with a schema.org @vocab, or a list containing one of these."""
    if isinstance(context, str):
        return bool(JSON_SCHEMA_ORG.match(context))
    if isinstance(context, dict):
        return is_schema_org_context(context.get("@vocab"))
    if isinstance(context, list):
        return any(is_schema_org_context(item) for item in context)
    return False


def extract_json(schema: list[Any] | dict[str, str], metadata: Document, backup_sitename: str | None = None) -> Document:
    """Parse and extract metadata from JSON-LD data.

    Note: baseline.py's `_walk_json` also walks JSON-LD, for page content rather than
    metadata, and is intentionally not shared with this function: this one flattens one
    level, gated per container, since metadata extraction should stay conservative, while
    `_walk_json` recurses unconditionally since content rescue is a last resort.
    """
    schema = as_list(schema)

    # collect content from every valid block, then process once (no short-circuit on a flat object)
    parents: list[Any] = []
    for parent in schema:
        if not isinstance(parent, dict):
            continue
        context = parent.get("@context")

        if is_schema_org_context(context):
            if "@graph" in parent:
                parents.extend(as_list(parent["@graph"]))
            elif (
                "@type" in parent
                and isinstance(parent["@type"], str)
                and "liveblogposting" in parent["@type"].lower()
                and "liveBlogUpdate" in parent
            ):
                parents.extend(as_list(parent["liveBlogUpdate"]))
            else:
                parents.append(parent)

    return process_parent(parents, metadata, backup_sitename)


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


def unescape_json_string(string: str) -> str:
    "Remove lone surrogates and unescape HTML entities"
    string = "".join(c for c in string if ord(c) < 0xD800 or ord(c) > 0xDFFF)
    return unescape(string)


def normalize_json(string: str) -> str:
    "Normalize unicode strings and trim the output"
    if "\\" in string:
        string = string.replace("\\n", "").replace("\\r", "").replace("\\t", "")
        string = JSON_UNICODE_REPLACE.sub(lambda match: chr(int(match[1], 16)), string)
        string = unescape_json_string(string)
    return trim(HTML_STRIP_TAGS.sub("", string))


def normalize_json_values(value: Any) -> Any:
    "Normalize all strings of a parsed JSON object."
    if isinstance(value, str):
        # JSON escapes are already decoded by the parser, entities and surrogates are not
        # markup is stripped first so that escaped angle brackets stay as text
        return trim(unescape_json_string(HTML_STRIP_TAGS.sub("", value)))
    if isinstance(value, list):
        return [normalize_json_values(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_json_values(item) for key, item in value.items()}
    return value


def normalize_authors(current_authors: str | None, author_string: str) -> str | None:
    """Normalize author info to focus on author names only"""
    new_authors = []
    if author_string.lower().startswith("http"):
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
    # remove html tags and email addresses
    author_string = AUTHOR_EMAIL.sub("", HTML_STRIP_TAGS.sub("", author_string))
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
