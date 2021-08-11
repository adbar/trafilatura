"""
Functions needed to scrape metadata from JSON-LD format.
"""

import re
import json

from .utils import normalize_authors, trim

JSON_ARTICLE_SCHEMA = {"Article", "BackgroundNewsArticle", "BlogPosting", "MedicalScholarlyArticle", "NewsArticle", "OpinionNewsArticle", "ReportageNewsArticle",  "ScholarlyArticle", "SocialMediaPosting"}
JSON_PUBLISHER_SCHEMA = {"NewsMediaOrganization", "Organization", "WebPage", "Website"}
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

    for parent in filter(None, schema):
        if '@context' not in parent or parent['@context'][-10:].lower() != 'schema.org':
            continue
        if '@graph' in parent:
            parent = parent['@graph']
        elif '@type' in parent and 'LiveBlogPosting' in parent['@type']:
            parent = parent['liveBlogUpdate']
        else:
            parent = schema

        for content in filter(None, parent):
            # try to extract publisher
            if 'publisher' in content:
                if 'name' in content['publisher']:
                    metadata['sitename'] = content['publisher']['name']

            if '@type' not in content:
                continue
            if isinstance(content["@type"], list):
                # some websites are using ['Person'] as type
                content_type = content["@type"][0]
            else:
                content_type = content["@type"]

            if content_type in JSON_PUBLISHER_SCHEMA:
                for candidate in ("name", "alternateName"):
                    if candidate in content:
                        if content[candidate] is not None:
                            if metadata['sitename'] is None or (len(metadata['sitename']) < len(content[candidate]) and content_type != "WebPage"):
                                metadata['sitename'] = content[candidate]
                            if metadata['sitename'] is None and metadata['sitename'].startswith('http') and not content[candidate].startswith('http'):
                                metadata['sitename'] = content[candidate]

            elif content_type == "Person":
                if 'name' in content and not content['name'].startswith('http'):
                    metadata['author'] = normalize_authors(metadata['author'], content['name'])

            elif content_type in JSON_ARTICLE_SCHEMA:
                # author and person
                if 'author' in content:
                    list_authors = content['author']
                    if isinstance(list_authors, str):
                        # try to convert to json object
                        try:
                            list_authors = json.loads(list_authors)
                        except json.JSONDecodeError:
                            pass

                    if not isinstance(list_authors, list):
                        list_authors = [list_authors]
                    for author in list_authors:
                        if ('@type' in author and author['@type'] == 'Person') or ('@type' not in author):
                            # error thrown: author['name'] can be a list (?)
                            if 'name' in author and author['name'] is not None and not isinstance(author['name'], list) and not author['name'].startswith('http'):
                                metadata['author'] = normalize_authors(metadata['author'], author['name'])
                            elif 'givenName' in author is not None and 'familyName' in author:
                                name = [author['givenName'], author['additionalName'], author['familyName']]
                                metadata['author'] = normalize_authors(metadata['author'], ' '.join(
                                    filter(lambda v: v is not None, name)))
                # category
                if metadata['categories'] is None and 'articleSection' in content:
                    if isinstance(content['articleSection'], str):
                        metadata['categories'] = [content['articleSection']]
                    else:
                        metadata['categories'] = content['articleSection']

                # try to extract title
                if metadata['title'] is None:
                    if 'name' in content and content_type == 'Article':
                        metadata['title'] = content['name']
                    elif 'headline' in content:
                        metadata['title'] = content['headline']
    return metadata


def extract_json_author(elemtext, regular_expression):
    '''Crudely extract author names from JSON-LD data'''
    authors = None
    mymatch = regular_expression.search(elemtext)
    while mymatch is not None:
        if mymatch.group(1) and ' ' in mymatch.group(1):
            authors = normalize_authors(authors, mymatch.group(1))
            elemtext = regular_expression.sub(r'', elemtext, count=1)
            mymatch = regular_expression.search(elemtext)
        else:
            break
    if authors is not None:
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
