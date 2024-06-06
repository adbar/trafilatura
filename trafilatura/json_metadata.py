"""
Functions needed to scrape metadata from JSON-LD format.
For reference, here is the list of all JSON-LD types: https://schema.org/docs/full.html
"""

import json
import re
from html import unescape

from .utils import normalize_authors, trim

JSON_ARTICLE_SCHEMA = {"article", "backgroundnewsarticle", "blogposting", "medicalscholarlyarticle", "newsarticle", "opinionnewsarticle", "reportagenewsarticle", "scholarlyarticle", "socialmediaposting", "liveblogposting"}
JSON_OGTYPE_SCHEMA = {"aboutpage", "checkoutpage", "collectionpage", "contactpage", "faqpage", "itempage", "medicalwebpage", "profilepage", "qapage", "realestatelisting", "searchresultspage", "webpage", "website", "article", "advertisercontentarticle", "newsarticle", "analysisnewsarticle", "askpublicnewsarticle", "backgroundnewsarticle", "opinionnewsarticle", "reportagenewsarticle", "reviewnewsarticle", "report", "satiricalarticle", "scholarlyarticle", "medicalscholarlyarticle", "socialmediaposting", "blogposting", "liveblogposting", "discussionforumposting", "techarticle", "blog", "jobposting"}
JSON_PUBLISHER_SCHEMA = {"newsmediaorganization", "organization", "webpage", "website"}
JSON_AUTHOR_1 = re.compile(r'"author":[^}[]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}[]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_2 = re.compile(r'"[Pp]erson"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_REMOVE = re.compile(r',?(?:"\w+":?[:|,\[])?{?"@type":"(?:[Ii]mageObject|[Oo]rganization|[Ww]eb[Pp]age)",[^}[]+}[\]|}]?')
JSON_PUBLISHER = re.compile(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', re.DOTALL)
JSON_TYPE = re.compile(r'"@type"\s*:\s*"([^"]*)"', re.DOTALL)
JSON_CATEGORY = re.compile(r'"articleSection": ?"([^"\\]+)', re.DOTALL)
JSON_NAME = re.compile(r'"@type":"[Aa]rticle", ?"name": ?"([^"\\]+)', re.DOTALL)
JSON_HEADLINE = re.compile(r'"headline": ?"([^"\\]+)', re.DOTALL)
JSON_MATCH = re.compile(r'"author":|"person":', flags=re.IGNORECASE)
JSON_REMOVE_HTML = re.compile(r'<[^>]+>')
JSON_SCHEMA_ORG = re.compile(r"^https?://schema\.org", flags=re.IGNORECASE)
JSON_UNICODE_REPLACE = re.compile(r'\\u([0-9a-fA-F]{4})')


def extract_json(schema, metadata):
    '''Parse and extract metadata from JSON-LD data'''
    if isinstance(schema, dict):
        schema = [schema]

    for parent in filter(lambda p: '@context' in p and isinstance(p['@context'], str) and JSON_SCHEMA_ORG.match(p['@context']), schema):
        if '@graph' in parent:
            parent = parent['@graph'] if isinstance(parent['@graph'], list) else [parent['@graph']]
        elif '@type' in parent and isinstance(parent['@type'], str) and 'liveblogposting' in parent['@type'].lower() and 'liveBlogUpdate' in parent:
            parent = parent['liveBlogUpdate'] if isinstance(parent['liveBlogUpdate'], list) else [parent['liveBlogUpdate']]
        else:
            parent = schema

        for content in filter(None, parent):
            # try to extract publisher
            if 'publisher' in content and 'name' in content['publisher']:
                metadata.sitename = content['publisher']['name']

            if '@type' not in content or len(content["@type"]) == 0:
                continue
            if isinstance(content["@type"], list):
                # some websites are using ['Person'] as type
                content_type = content["@type"][0].lower()
            else:
                content_type = content["@type"].lower()

            # The "pagetype" should only be returned if the page is some kind of an article, category, website...
            if content_type in JSON_OGTYPE_SCHEMA and not metadata.pagetype:
                metadata.pagetype = normalize_json(content_type)

            if content_type in JSON_PUBLISHER_SCHEMA:
                candidate = next((content[candidate] for candidate in ("name", "legalName", "alternateName") if content.get(candidate)), None)
                if candidate and isinstance(candidate, str):
                    if metadata.sitename is None or (len(metadata.sitename) < len(candidate) and content_type != "webpage"):
                        metadata.sitename = candidate
                    if metadata.sitename is not None and metadata.sitename.startswith('http') and not candidate.startswith('http'):
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
                            # error thrown: author['name'] can be a list (?)
                            if 'name' in author and author['name'] is not None:
                                author_name = author['name']
                                if isinstance(author_name, list):
                                    author_name = '; '.join(author_name).strip('; ')
                                elif isinstance(author_name, dict) and "name" in author_name:
                                    author_name = author_name["name"]
                                # check for no more bugs on json
                                if isinstance(author_name, str):
                                    metadata.author = normalize_authors(metadata.author, author_name)
                            elif 'givenName' in author and 'familyName' in author:
                                name = [author['givenName'], author.get('additionalName'), author['familyName']]
                                metadata.author = normalize_authors(metadata.author, ' '.join(filter(None, name)))

                # category
                if metadata.categories is None and 'articleSection' in content:
                    if isinstance(content['articleSection'], str):
                        metadata.categories = [content['articleSection']]
                    else:
                        metadata.categories = list(filter(None, content['articleSection']))

                # try to extract title
                if metadata.title is None:
                    if 'name' in content and content_type == 'article':
                        metadata.title = content['name']
                    elif 'headline' in content:
                        metadata.title = content['headline']

    return metadata


def extract_json_author(elemtext, regular_expression):
    '''Crudely extract author names from JSON-LD data'''
    authors = None
    mymatch = regular_expression.search(elemtext)
    while mymatch is not None and mymatch[1] and ' ' in mymatch[1]:
        authors = normalize_authors(authors, mymatch[1])
        elemtext = regular_expression.sub(r'', elemtext, count=1)
        mymatch = regular_expression.search(elemtext)
    return authors or None


def extract_json_parse_error(elem, metadata):
    '''Crudely extract metadata from JSON-LD data'''
    # author info
    element_text_author = JSON_AUTHOR_REMOVE.sub('', elem)
    if any(JSON_MATCH.findall(element_text_author)):
        author = extract_json_author(element_text_author, JSON_AUTHOR_1) or extract_json_author(element_text_author, JSON_AUTHOR_2)
        if author:
            metadata.author = author

    # try to extract page type as an alternative to og:type
    if "@type" in elem:
        mymatch = JSON_TYPE.search(elem)
        candidate = normalize_json(mymatch[1].lower())
        if mymatch and candidate in JSON_OGTYPE_SCHEMA:
            metadata.pagetype = candidate

    # try to extract publisher
    if '"publisher"' in elem:
        mymatch = JSON_PUBLISHER.search(elem)
        if mymatch and ',' not in mymatch[1]:
            candidate = normalize_json(mymatch[1])
            if metadata.sitename is None or len(metadata.sitename) < len(candidate):
                metadata.sitename = candidate
            if metadata.sitename.startswith('http') and not candidate.startswith('http'):
                metadata.sitename = candidate

    # category
    if '"articleSection"' in elem:
        mymatch = JSON_CATEGORY.search(elem)
        if mymatch:
            metadata.categories = [normalize_json(mymatch[1])]

    # try to extract title
    if '"name"' in elem and metadata.title is None:
        mymatch = JSON_NAME.search(elem)
        if mymatch:
            metadata.title = normalize_json(mymatch[1])
    if '"headline"' in elem and metadata.title is None:
        mymatch = JSON_HEADLINE.search(elem)
        if mymatch:
            metadata.title = normalize_json(mymatch[1])

    # exit if found
    return metadata


def normalize_json(inputstring):
    'Normalize unicode strings and trim the output'
    if '\\' in inputstring:
        inputstring = inputstring.replace('\\n', '').replace('\\r', '').replace('\\t', '')
        inputstring = JSON_UNICODE_REPLACE.sub(lambda match: chr(int(match.group(1), 16)), inputstring)
        inputstring = ''.join(c for c in inputstring if ord(c) < 0xD800 or ord(c) > 0xDFFF)
        inputstring = unescape(inputstring)
    return trim(JSON_REMOVE_HTML.sub('', inputstring))
