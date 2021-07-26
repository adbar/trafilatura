"""
Module bundling all functions needed to scrape metadata from json.
"""

import re

import trafilatura.metadata
from trafilatura.utils import trim

JSON_ARTICLE_SCHEMA = ["ReportageNewsArticle", "NewsArticle", "BlogPosting", "SocialMediaPosting", "MedicalScholarlyArticle", "BackgroundNewsArticle", "ScholarlyArticle", "Article", "OpinionNewsArticle"]
JSON_PUBLISHER_SCHEMA = ["Organization", "WebPage", "Website"]
JSON_AUTHOR_1 = re.compile(r'"author":[^}[]+?"name?\\?": ?\\?"([^"\\]+)|"author"[^}[]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_2 = re.compile(r'"[Pp]erson"[^}]+?"names?".+?"([^"]+)', re.DOTALL)
JSON_AUTHOR_REMOVE = re.compile(r',?(?:"\w+":?[:|,|\[])?{?"@type":"(?:[Ii]mageObject|[Oo]rganization|[Ww]eb[Pp]age)",[^}[]+}[\]|}]?')
JSON_PUBLISHER = re.compile(r'"publisher":[^}]+?"name?\\?": ?\\?"([^"\\]+)', re.DOTALL)
JSON_CATEGORY = re.compile(r'"articleSection": ?"([^"\\]+)', re.DOTALL)
JSON_NAME = re.compile(r'"@type":"[Aa]rticle", ?"name": ?"([^"\\]+)', re.DOTALL)
JSON_HEADLINE = re.compile(r'"headline": ?"([^"\\]+)', re.DOTALL)
JSON_MATCH = re.compile(r'"author":|"person":', flags=re.IGNORECASE)


def extract_json(schema, metadata):
    '''Parse and extract metadata from JSON-LD data'''
    if isinstance(schema, dict):
        schema = [schema]

    for parent in schema:
        if "@context" not in parent or parent["@context"][-10:].lower() != "schema.org":
            continue
        elif '@graph' in parent:
            parent = parent['@graph']
        elif '@type' in parent and 'LiveBlogPosting' in parent['@type']:
            parent = parent['liveBlogUpdate']
        else:
            parent = schema

        for content in parent:
            # try to extract publisher
            if 'publisher' in content:
                if 'name' in content['publisher']:
                    metadata['sitename'] = content['publisher']['name']

            if metadata['sitename'] is None and content["@type"] in JSON_PUBLISHER_SCHEMA:
                for canditate in ("name", "alternateName"):
                    if canditate in content:
                        if len(metadata['sitename']) < len(content[canditate]) and content["@type"] != "WebPage":
                            metadata['sitename'] = content[canditate]
                        if metadata['sitename'].startswith('http') and not content[canditate].startswith(
                                'http'):
                            metadata['sitename'] = content[canditate]

            if content["@type"] == "Person":
                if 'name' in content and not content['name'].startswith('http'):
                    metadata['author'] = trafilatura.metadata.normalize_authors(metadata['author'], content['name'])

            if content["@type"] in JSON_ARTICLE_SCHEMA:
                # author and person
                if 'author' in content:
                    if not isinstance(content['author'], list):
                        content['author'] = [content['author']]
                    for author in content['author']:
                        if ('@type' in author and author['@type'] == 'Person') or ('@type' not in author):
                            if 'name' in author and not author['name'].startswith('http'):
                                metadata['author'] = trafilatura.metadata.normalize_authors(metadata['author'], author['name'])
                            elif 'givenName' in author is not None and 'familyName' in author:
                                name = [author['givenName'], author['additionalName'], author['familyName']]
                                metadata['author'] = trafilatura.metadata.normalize_authors(metadata['author'], ' '.join(
                                    filter(lambda v: v is not None, name)))
                # category
                if metadata['categories'] is None and 'articleSection' in content:
                    if isinstance(content['articleSection'], str):
                        metadata['categories'] = [content['articleSection']]
                    else:
                        metadata['categories'] = content['articleSection']

                # try to extract title
                if metadata['title'] is None:
                    if 'name' in content and content["@type"] == 'Article':
                        metadata['title'] = content['name']
                    elif 'headline' in content:
                        metadata['title'] = content['headline']
    return metadata


def extract_json_author(elemtext, regular_expression):
    '''Crudely extract author names from JSON-LD data'''
    authors = ''
    mymatch = regular_expression.search(elemtext)
    while mymatch is not None:
        if mymatch.group(1) and ' ' in mymatch.group(1):
            authors = trafilatura.metadata.normalize_authors(authors, mymatch.group(1))
            elemtext = regular_expression.sub(r'', elemtext, count=1)
            mymatch = regular_expression.search(elemtext)
        else:
            break
    if len(authors) > 0:
        return authors
    return None


def extract_json_parse_error(elem, metadata):
    '''Crudely extract metadata from JSON-LD data'''
    # author info
    element_text_author = JSON_AUTHOR_REMOVE.sub('', elem)
    if any(JSON_MATCH.findall(element_text_author)):
        author = extract_json_author(element_text_author, JSON_AUTHOR_1)
        if author is None:
            author = extract_json_author(element_text_author, JSON_AUTHOR_2)
        if author is not None:
            metadata['author'] = author
    # try to extract publisher
    if '"publisher"' in elem:
        mymatch = JSON_PUBLISHER.search(elem)
        if mymatch and not ',' in mymatch.group(1):
            candidate = normalize_json(mymatch.group(1))
            if metadata['sitename'] is None or len(metadata['sitename']) < len(candidate):
                metadata['sitename'] = candidate
            if metadata['sitename'].startswith('http') and not candidate.startswith('http'):
                metadata['sitename'] = candidate
    # category
    if '"articleSection"' in elem:
        mymatch = JSON_CATEGORY.search(elem)
        if mymatch:
            metadata['categories'] = [normalize_json(mymatch.group(1))]
    # try to extract title
    if '"name"' in elem and metadata['title'] is None:
        mymatch = JSON_NAME.search(elem)
        if mymatch:
            metadata['title'] = normalize_json(mymatch.group(1))
    if '"headline"' in elem and metadata['title'] is None:
        mymatch = JSON_HEADLINE.search(elem)
        if mymatch:
            metadata['title'] = normalize_json(mymatch.group(1))
    # exit if found
    return metadata


def normalize_json(inputstring):
    'Normalize unicode strings and trim the output'
    if '\\' in inputstring:
        return trim(inputstring.encode().decode('unicode-escape'))
    return trim(inputstring)
