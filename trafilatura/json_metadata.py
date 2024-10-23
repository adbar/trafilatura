"""
Functions needed to scrape metadata from JSON-LD format.
For reference, here is the list of all JSON-LD types: https://schema.org/docs/full.html
"""

import json
import re

from html import unescape
from typing import Any, Dict, List, Optional, Pattern, Union

from .settings import Document
from .utils import HTML_STRIP_TAGS, trim


JSON_ARTICLE_SCHEMA = {"article", "backgroundnewsarticle", "blogposting", "medicalscholarlyarticle", "newsarticle", "opinionnewsarticle", "reportagenewsarticle", "scholarlyarticle", "socialmediaposting", "liveblogposting"}
JSON_OGTYPE_SCHEMA = {"aboutpage", "checkoutpage", "collectionpage", "contactpage", "faqpage", "itempage", "medicalwebpage", "profilepage", "qapage", "realestatelisting", "searchresultspage", "webpage", "website", "article", "advertisercontentarticle", "newsarticle", "analysisnewsarticle", "askpublicnewsarticle", "backgroundnewsarticle", "opinionnewsarticle", "reportagenewsarticle", "reviewnewsarticle", "report", "satiricalarticle", "scholarlyarticle", "medicalscholarlyarticle", "socialmediaposting", "blogposting", "liveblogposting", "discussionforumposting", "techarticle", "blog", "jobposting"}
JSON_PUBLISHER_SCHEMA = {"newsmediaorganization", "organization", "webpage", "website"}
JSON_AUTHOR_1 = re.compile(r'"author":[^}[]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}[]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_2 = re.compile(r'"[Pp]erson"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_REMOVE = re.compile(r',?(?:"\w+":?[:|,\[])?{?"@type":"(?:[Ii]mageObject|[Oo]rganization|[Ww]eb[Pp]age)",[^}[]+}[\]|}]?')
JSON_PUBLISHER = re.compile(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', re.DOTALL)
JSON_TYPE = re.compile(r'"@type"\s*:\s*"([^"]*)"', re.DOTALL)
JSON_CATEGORY = re.compile(r'"articleSection": ?"([^"\\]+)', re.DOTALL)
JSON_MATCH = re.compile(r'"author":|"person":', flags=re.IGNORECASE)
JSON_REMOVE_HTML = re.compile(r'<[^>]+>')
JSON_SCHEMA_ORG = re.compile(r"^https?://schema\.org", flags=re.IGNORECASE)
JSON_UNICODE_REPLACE = re.compile(r'\\u([0-9a-fA-F]{4})')

AUTHOR_ATTRS = ('givenName', 'additionalName', 'familyName')

JSON_NAME = re.compile(r'"@type":"[Aa]rticle", ?"name": ?"([^"\\]+)', re.DOTALL)
JSON_HEADLINE = re.compile(r'"headline": ?"([^"\\]+)', re.DOTALL)
JSON_SEQ = [('"name"', JSON_NAME), ('"headline"', JSON_HEADLINE)]

AUTHOR_PREFIX = re.compile(r'^([a-zäöüß]+(ed|t))? ?(written by|words by|words|by|von|from) ', flags=re.IGNORECASE)
AUTHOR_REMOVE_NUMBERS = re.compile(r'\d.+?$')
AUTHOR_TWITTER = re.compile(r'@[\w]+')
AUTHOR_REPLACE_JOIN = re.compile(r'[._+]')
AUTHOR_REMOVE_NICKNAME = re.compile(r'["‘({\[’\'][^"]+?[‘’"\')\]}]')
AUTHOR_REMOVE_SPECIAL = re.compile(r'[^\w]+$|[:()?*$#!%/<>{}~¿]')
AUTHOR_REMOVE_PREPOSITION = re.compile(r'\b\s+(am|on|for|at|in|to|from|of|via|with|—|-|–)\s+(.*)', flags=re.IGNORECASE)
AUTHOR_EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
AUTHOR_SPLIT = re.compile(r'/|;|,|\||&|(?:^|\W)[u|a]nd(?:$|\W)', flags=re.IGNORECASE)
AUTHOR_EMOJI_REMOVE = re.compile(
    "["
    "\U00002700-\U000027BE"  # Dingbats
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U00002600-\U000026FF"  # Miscellaneous Symbols
    "\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U0001F680-\U0001F6FF"  # Transport and Map Symbols
    "]+", flags=re.UNICODE)


def is_plausible_sitename(metadata: Document, candidate: Any, content_type: Optional[str] = None) -> bool:
    '''Determine if the candidate should be used as sitename.'''
    if candidate and isinstance(candidate, str):
        if not metadata.sitename or (len(metadata.sitename) < len(candidate) and content_type != "webpage"):
            return True
        if metadata.sitename and metadata.sitename.startswith('http') and not candidate.startswith('http'):
            return True
    return False


def process_parent(parent: Any, metadata: Document) -> Document:
    "Find and extract selected metadata from JSON parts."
    for content in filter(None, parent):  # type: Dict[str, Any]
        # try to extract publisher
        if 'publisher' in content and 'name' in content['publisher']:
            metadata.sitename = content['publisher']['name']

        if '@type' not in content or not content["@type"]:
            continue

        # some websites are using ['Person'] as type
        content_type = content["@type"][0] if isinstance(content["@type"], list) else content["@type"]
        content_type = content_type.lower()

        # The "pagetype" should only be returned if the page is some kind of an article, category, website...
        if content_type in JSON_OGTYPE_SCHEMA and not metadata.pagetype:
            metadata.pagetype = normalize_json(content_type)

        if content_type in JSON_PUBLISHER_SCHEMA:
            candidate = content.get("name") or content.get("legalName") or content.get("alternateName")
            if is_plausible_sitename(metadata, candidate, content_type):
                metadata.sitename = candidate

        elif content_type == "person":
            if content.get('name') and not content['name'].startswith('http'):
                metadata.author = normalize_authors(metadata.author, content['name'])

        elif content_type in JSON_ARTICLE_SCHEMA:
            # author and person
            if 'author' in content:
                list_authors = content['author']
                if isinstance(list_authors, str):
                    # try to convert to json object
                    try:
                        list_authors = json.loads(list_authors)
                    except json.JSONDecodeError:
                        # it is a normal string
                        metadata.author = normalize_authors(metadata.author, list_authors)

                if not isinstance(list_authors, list):
                    list_authors = [list_authors]

                for author in list_authors:
                    if '@type' not in author or author['@type'] == 'Person':
                        author_name = None
                        # error thrown: author['name'] can be a list (?)
                        if 'name' in author:
                            author_name = author.get('name')
                            if isinstance(author_name, list):
                                author_name = '; '.join(author_name).strip('; ')
                            elif isinstance(author_name, dict) and "name" in author_name:
                                author_name = author_name["name"]
                        elif 'givenName' in author and 'familyName' in author:
                            author_name = ' '.join(author[x] for x in AUTHOR_ATTRS if x in author)
                        # additional check to prevent bugs
                        if isinstance(author_name, str):
                            metadata.author = normalize_authors(metadata.author, author_name)

            # category
            if not metadata.categories and 'articleSection' in content:
                if isinstance(content['articleSection'], str):
                    metadata.categories = [content['articleSection']]
                else:
                    metadata.categories = list(filter(None, content['articleSection']))

            # try to extract title
            if not metadata.title:
                if 'name' in content and content_type == 'article':
                    metadata.title = content['name']
                elif 'headline' in content:
                    metadata.title = content['headline']
    return metadata


def extract_json(schema: Union[List[Any], Dict[str, str]], metadata: Document) -> Document:
    '''Parse and extract metadata from JSON-LD data'''
    if isinstance(schema, dict):
        schema = [schema]

    for parent in schema:

        context = parent.get('@context')

        if context and isinstance(context, str) and JSON_SCHEMA_ORG.match(context):
            if '@graph' in parent:
                parent = parent['@graph'] if isinstance(parent['@graph'], list) else [parent['@graph']]
            elif '@type' in parent and isinstance(parent['@type'], str) and 'liveblogposting' in parent['@type'].lower() and 'liveBlogUpdate' in parent:
                parent = parent['liveBlogUpdate'] if isinstance(parent['liveBlogUpdate'], list) else [parent['liveBlogUpdate']]
            else:
                parent = schema

            metadata = process_parent(parent, metadata)

    return metadata


def extract_json_author(elemtext: str, regular_expression: Pattern[str]) -> Optional[str]:
    '''Crudely extract author names from JSON-LD data'''
    authors = None
    mymatch = regular_expression.search(elemtext)
    while mymatch and ' ' in mymatch[1]:
        authors = normalize_authors(authors, mymatch[1])
        elemtext = regular_expression.sub(r'', elemtext, count=1)
        mymatch = regular_expression.search(elemtext)
    return authors or None


def extract_json_parse_error(elem: str, metadata: Document) -> Document:
    '''Crudely extract metadata from JSON-LD data'''
    # author info
    element_text_author = JSON_AUTHOR_REMOVE.sub('', elem)
    author = extract_json_author(element_text_author, JSON_AUTHOR_1) or \
             extract_json_author(element_text_author, JSON_AUTHOR_2)
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
        if mymatch and ',' not in mymatch[1]:
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
    'Normalize unicode strings and trim the output'
    if '\\' in string:
        string = string.replace('\\n', '').replace('\\r', '').replace('\\t', '')
        string = JSON_UNICODE_REPLACE.sub(lambda match: chr(int(match[1], 16)), string)
        string = ''.join(c for c in string if ord(c) < 0xD800 or ord(c) > 0xDFFF)
        string = unescape(string)
    return trim(JSON_REMOVE_HTML.sub('', string))


def normalize_authors(current_authors: Optional[str], author_string: str) -> Optional[str]:
    '''Normalize author info to focus on author names only'''
    new_authors = []
    if author_string.lower().startswith('http') or AUTHOR_EMAIL.match(author_string):
        return current_authors
    if current_authors is not None:
        new_authors = current_authors.split('; ')
    # fix to code with unicode
    if '\\u' in author_string:
        author_string = author_string.encode().decode('unicode_escape')
    # fix html entities
    if '&#' in author_string or '&amp;' in author_string:
        author_string = unescape(author_string)
    # remove html tags
    author_string = HTML_STRIP_TAGS.sub('', author_string)
    # examine names
    for author in AUTHOR_SPLIT.split(author_string):
        author = trim(author)
        # remove emoji
        author = AUTHOR_EMOJI_REMOVE.sub('', author)
        # remove @username
        author = AUTHOR_TWITTER.sub('', author)
        # replace special characters with space
        author = trim(AUTHOR_REPLACE_JOIN.sub(' ', author))
        author = AUTHOR_REMOVE_NICKNAME.sub('', author)
        # remove special characters
        author = AUTHOR_REMOVE_SPECIAL.sub('', author)
        author = AUTHOR_PREFIX.sub('', author)
        author = AUTHOR_REMOVE_NUMBERS.sub('', author)
        author = AUTHOR_REMOVE_PREPOSITION.sub('', author)
        # skip empty or improbably long strings
        # simple heuristics, regex or vowel tests also possible
        if not author or (len(author) >= 50 and ' ' not in author and '-' not in author):
            continue
        # title case
        if not author[0].isupper() or sum(1 for c in author if c.isupper()) < 1:
            author = author.title()
        # safety checks
        if author not in new_authors and (len(new_authors) == 0 or all(new_author not in author for new_author in new_authors)):
            new_authors.append(author)
    if len(new_authors) == 0:
        return current_authors
    return '; '.join(new_authors).strip('; ')
