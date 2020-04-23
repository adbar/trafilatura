# pylint:disable-msg=E0611,I1101
"""
All functions related to XML generation, processing and validation.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import pickle

from io import StringIO
from lxml import etree

import pkg_resources

from .utils import sanitize


LOGGER = logging.getLogger(__name__)
# validation
TEI_SCHEMA = pkg_resources.resource_filename('trafilatura', 'data/tei-schema.pickle')
TEI_VALID_TAGS = {'cell', 'code', 'body', 'del', 'div', 'fw', 'head', 'hi', 'item', \
                  'lb', 'list', 'p', 'quote', 'row', 'table'}
TEI_VALID_ATTRS = {'rendition', 'role', 'type'}
TEI_RELAXNG = None # to be downloaded later if necessary

# XML invalid characters
# https://chase-seibert.github.io/blog/2011/05/20/stripping-control-characters-in-python.html


def build_xml_output(postbody, commentsbody):
    '''Build XML output tree based on extracted information'''
    output = etree.Element('doc')
    postbody.tag = 'main'
    output.append(postbody)
    if commentsbody is not None:
        commentsbody.tag = 'comments'
        output.append(commentsbody)
    return output


def add_xml_meta(output, docmeta):
    '''Add extracted metadata to the XML output tree'''
    # metadata
    if docmeta:
        if docmeta.sitename is not None:
            output.set('sitename', docmeta.sitename)
        if docmeta.title is not None:
            output.set('title', docmeta.title)
        if docmeta.author is not None:
            output.set('author', docmeta.author)
        if docmeta.date is not None:
            output.set('date', docmeta.date)
        if docmeta.url is not None:
            output.set('source', docmeta.url)
        if docmeta.description is not None:
            output.set('excerpt', docmeta.description)
        if docmeta.categories is not None and len(docmeta.categories) > 0:
            cats = ';'.join(docmeta.categories)
            output.set('categories', cats)
        if docmeta.tags is not None and len(docmeta.tags) > 0:
            tags = ';'.join(docmeta.tags)
            output.set('tags', tags)
    return output


def build_tei_output(postbody, commentsbody, docmeta):
    '''Build TEI-XML output tree based on extracted information'''
    # build TEI tree
    output = write_teitree(postbody, commentsbody, docmeta)
    # filter output (strip unwanted elements), just in case
    # check and repair
    output = check_tei(output, docmeta.url)
    return output


def check_tei(tei, url):
    '''Check if the resulting XML file is conform and scrub remaining tags'''
    # convert head tags
    for elem in tei.iter('head'):
        elem.tag = 'fw'
        elem.set('type', 'header')
    # look for elements that are not valid
    for element in tei.xpath('//text/body//*'):
        # check elements
        if element.tag not in TEI_VALID_TAGS:
            # disable warnings for chosen categories
            # if element.tag not in ('div', 'span'):
            LOGGER.warning('not a TEI element, removing: %s %s', element.tag, url)
            # append text AND tail to parent
            full_text = ''
            if element.text is not None and element.tail is not None:
                full_text = element.text + ' ' + element.tail
            elif element.text is not None and element.tail is None:
                full_text = element.text
            elif element.text is None and element.tail is not None:
                full_text = element.tail
            parent = element.getparent()
            previous = element.getprevious()
            if previous is not None:
                # There is a previous node, append text to its tail
                if previous.tail is not None:
                    previous.tail += ' ' + full_text
                else:
                    previous.tail = full_text
            else:
                # It's the first node in <parent/>, append to parent's text
                if parent.text is not None:
                    parent.text += ' ' + full_text
                else:
                    parent.text = full_text
            parent.remove(element)
            continue
        # check attributes
        for attribute in element.attrib:
            if attribute not in TEI_VALID_ATTRS:
                LOGGER.warning('not a valid TEI attribute, removing: %s in %s %s', attribute, element.tag, url)
                element.attrib.pop(attribute)
    # export metadata
    #metadata = (title + '\t' + date + '\t' + uniqueid + '\t' + url + '\t').encode('utf-8')
    return tei


def validate_tei(tei):  # , filename=""
    '''Check if an XML document is conform to the guidelines of the Text Encoding Initiative'''
    global TEI_RELAXNG
    if TEI_RELAXNG is None:
        # load validator
        with open(TEI_SCHEMA, 'rb') as schemafile:
            schema_data = pickle.load(schemafile)
        relaxng_doc = etree.parse(StringIO(schema_data))
        TEI_RELAXNG = etree.RelaxNG(relaxng_doc)
    result = TEI_RELAXNG.validate(tei)
    if result is False:
        print(TEI_RELAXNG.error_log.last_error)
    return result


def xmltotxt(xmloutput):
    '''Convert to plain text format'''
    returnlist = []
    etree.strip_tags(xmloutput, 'hi')
    for element in xmloutput.iter():
        # process text
        if element.text is None and element.tail is None:
            # newlines for textless elements
            if element.tag in ('row', 'table'):
                returnlist.append('\n')
            continue
        if element.text is not None and element.tail is not None:
            textelement = element.text + ' ' + element.tail
        elif element.text is not None and element.tail is None:
            textelement = element.text
        else:
            textelement = element.tail
        if element.tag in ('code', 'fw', 'head', 'lb', 'p', 'quote', 'row', 'table'):
            returnlist.append('\n' + textelement + '\n')
        elif element.tag == 'item':
            returnlist.append('\n- ' + textelement + '\n')
        elif element.tag == 'cell':
            returnlist.append('|' + textelement + '|')
        elif element.tag == 'comments':
            returnlist.append('\n\n')
        else:
            returnlist.append(textelement + ' ')
    returnstring = sanitize(''.join(returnlist))
    return returnstring


def write_teitree(postbody, commentsbody, docmeta):
    '''Bundle the extracted post and comments into a TEI tree'''
    tei = etree.Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
    header = etree.SubElement(tei, 'teiHeader')
    #if simplified is True:
    #    header = write_simpleheader(header, docmeta)
    #else:
    header = write_fullheader(header, docmeta)
    textelem = etree.SubElement(tei, 'text')
    textbody = etree.SubElement(textelem, 'body')
    # post
    postbody.tag = 'div'
    postbody.set('type', 'entry') # rendition='#pst'
    textbody.append(postbody)
    # comments
    if commentsbody is not None and len(commentsbody) > 0:
        commentsbody.tag = 'div'
        commentsbody.set('type', 'entry') # rendition='#cmt'
        textbody.append(commentsbody)
    return tei


def write_fullheader(header, docmeta):
    '''Write TEI header based on gathered metadata'''
    filedesc = etree.SubElement(header, 'fileDesc')
    bib_titlestmt = etree.SubElement(filedesc, 'titleStmt')
    bib_titlemain = etree.SubElement(bib_titlestmt, 'title', type='main')
    bib_titlemain.text = docmeta.title
    if docmeta.author:
        bib_author = etree.SubElement(bib_titlestmt, 'author')
        bib_author.text = docmeta.author
    publicationstmt_a = etree.SubElement(filedesc, 'publicationStmt')
    publicationstmt_p = etree.SubElement(publicationstmt_a, 'p')
    sourcedesc = etree.SubElement(filedesc, 'sourceDesc')
    source_bibl = etree.SubElement(sourcedesc, 'bibl')
    if docmeta.sitename and docmeta.date:
        sigle = docmeta.sitename + ', ' + docmeta.date
    elif not docmeta.sitename and docmeta.date:
        sigle = docmeta.date
    elif docmeta.sitename and not docmeta.date:
        sigle = docmeta.sitename
    else:
        sigle = ''
    source_bibl.text = docmeta.title + '. ' + sigle
    source_sigle = etree.SubElement(sourcedesc, 'bibl', type='sigle')
    source_sigle.text = sigle
    biblfull = etree.SubElement(sourcedesc, 'biblFull')
    bib_titlestmt = etree.SubElement(biblfull, 'titleStmt')
    bib_titlemain = etree.SubElement(bib_titlestmt, 'title', type='main')
    bib_titlemain.text = docmeta.title
    if docmeta.author:
        bib_author = etree.SubElement(bib_titlestmt, 'author')
        bib_author.text = docmeta.author
    publicationstmt = etree.SubElement(biblfull, 'publicationStmt')
    publication_publisher = etree.SubElement(publicationstmt, 'publisher')
    publication_publisher.text = docmeta.sitename
    publication_url = etree.SubElement(publicationstmt, 'ptr', type='URL', target=docmeta.url)
    publication_date = etree.SubElement(publicationstmt, 'date')
    publication_date.text = docmeta.date
    profiledesc = etree.SubElement(header, 'profileDesc')
    abstract = etree.SubElement(profiledesc, 'abstract')
    abstract_p = etree.SubElement(abstract, 'p')
    abstract_p.text = docmeta.description
    if len(docmeta.categories) > 0 or len(docmeta.tags) > 0:
        textclass = etree.SubElement(profiledesc, 'textClass')
        keywords = etree.SubElement(textclass, 'keywords')
        if len(docmeta.categories) > 0:
            cat_list = etree.SubElement(keywords, 'term', type='categories')
            cat_list.text = ','.join(docmeta.categories)
        if len(docmeta.tags) > 0:
            tags_list = etree.SubElement(keywords, 'term', type='tags')
            tags_list.text = ','.join(docmeta.tags)
    return header


#def write_simpleheader(header, docmeta):
#    filedesc = etree.SubElement(header, 'fileDesc')
#    #biblfull = etree.SubElement(sourcedesc, 'biblFull')
#    bib_titlestmt = etree.SubElement(filedesc, 'titleStmt')
#    bib_titlemain = etree.SubElement(bib_titlestmt, 'title', type='main')
#    bib_titlemain.text = docmeta.title
#    bib_titlesub = etree.SubElement(bib_titlestmt, 'title', type='excerpt')
#    bib_titlesub.text = docmeta.description
#    bib_author = etree.SubElement(bib_titlestmt, 'author')
#    bib_author.text = docmeta.author
#    publicationstmt = etree.SubElement(filedesc, 'publicationStmt')
#    publication_publisher = etree.SubElement(publicationstmt, 'publisher')
#    publication_publisher.text = docmeta.sitename
#    publication_url = etree.SubElement(publicationstmt, 'idno', type='URL')
#    publication_url.text = docmeta.url
#    publication_date = etree.SubElement(publicationstmt, 'date')
#    publication_date.set('type', 'publication')
#    publication_date.text = docmeta.date
#    sourcedesc = etree.SubElement(filedesc, 'sourceDesc')
#    source_p = etree.SubElement(sourcedesc, 'p')
#    if len(docmeta.categories) > 0 or len(docmeta.tags) > 0:
#        if len(docmeta.categories) > 0:
#            cat_list = etree.SubElement(source_p, 'list', type='categories')
#            for cat in docmeta.categories:
#                item = etree.SubElement(cat_list, 'item')
#                item.text = cat
#        if len(docmeta.tags) > 0:
#            tags_list = etree.SubElement(source_p, 'list', type='tags')
#            for tag in docmeta.tags:
#                item = etree.SubElement(tags_list, 'item')
#                item.text = tag
#    return header
