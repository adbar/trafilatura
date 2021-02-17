# pylint:disable-msg=E0611,I1101
"""
All functions related to XML generation, processing and validation.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import json
import logging
import pickle

from io import StringIO
from pathlib import Path

from lxml import etree

from . import __version__
from .utils import sanitize


LOGGER = logging.getLogger(__name__)
# validation
TEI_SCHEMA = str(Path(__file__).parent / 'data/tei-schema.pickle')
TEI_VALID_TAGS = {'body', 'cell', 'code', 'del', 'div', 'fw', 'graphic', 'head', 'hi', \
                  'item', 'lb', 'list', 'p', 'quote', 'ref', 'row', 'table'}
TEI_VALID_ATTRS = {'rend', 'rendition', 'role', 'target', 'type'}
TEI_RELAXNG = None # to be downloaded later if necessary

CONTROL_PARSER = etree.XMLParser(remove_blank_text=True)

TEXTELEMS = {'code', 'fw', 'head', 'lb', 'list', 'p', 'quote', 'row', 'table'}


def build_json_output(docmeta):
    '''Build JSON output based on extracted information'''
    outputdict = docmeta
    outputdict['source'] = outputdict.pop('url')
    outputdict['source-hostname'] = outputdict.pop('sitename')
    outputdict['excerpt'] = outputdict.pop('description')
    outputdict['categories'] = ';'.join(outputdict['categories'])
    outputdict['tags'] = ';'.join(outputdict['tags'])
    outputdict['text'] = xmltotxt(outputdict.pop('body'), include_formatting=False, include_links=False)
    if outputdict['commentsbody'] is not None:
        outputdict['comments'] = xmltotxt(outputdict.pop('commentsbody'), include_formatting=False, include_links=False)
    else:
        del outputdict['commentsbody']
    return json.dumps(outputdict)


def clean_attributes(tree):
    '''Remove unnecessary attributes'''
    for elem in tree.iter():
        if elem.tag not in ('del', 'graphic', 'hi', 'ref'):
            elem.attrib.clear()
    return tree


def build_xml_output(docmeta):
    '''Build XML output tree based on extracted information'''
    output = etree.Element('doc')
    output = add_xml_meta(output, docmeta)
    docmeta['body'].tag = 'main'
    output.append(clean_attributes(docmeta['body']))
    if docmeta['commentsbody'] is not None:
        docmeta['commentsbody'].tag = 'comments'
        output.append(clean_attributes(docmeta['commentsbody']))
# XML invalid characters
# https://chase-seibert.github.io/blog/2011/05/20/stripping-control-characters-in-python.html
    return output


def control_xml_output(output_tree, output_format, tei_validation, docmeta):
    '''Make sure the XML output is conform and valid if required'''
    control_string = sanitize(etree.tostring(output_tree, encoding='unicode'))
    # necessary for cleaning
    output_tree = etree.fromstring(control_string, CONTROL_PARSER)
    # validate
    if output_format == 'xmltei' and tei_validation is True:
        result = validate_tei(output_tree)
        LOGGER.info('TEI validation result: %s %s %s', result, docmeta['id'], docmeta['url'])
    return etree.tostring(output_tree, pretty_print=True, encoding='unicode').strip()


def add_xml_meta(output, docmeta):
    '''Add extracted metadata to the XML output tree'''
    # metadata
    if docmeta:
        if docmeta['sitename'] is not None:
            output.set('sitename', docmeta['sitename'])
        if docmeta['title'] is not None:
            output.set('title', docmeta['title'])
        if docmeta['author'] is not None:
            output.set('author', docmeta['author'])
        if docmeta['date'] is not None:
            output.set('date', docmeta['date'])
        if docmeta['url'] is not None:
            output.set('source', docmeta['url'])
        if docmeta['hostname'] is not None:
            output.set('hostname', docmeta['hostname'])
        if docmeta['description'] is not None:
            output.set('excerpt', docmeta['description'])
        if docmeta['categories'] is not None:
            output.set('categories', ';'.join(docmeta['categories']))
        if docmeta['tags'] is not None:
            output.set('tags', ';'.join(docmeta['tags']))
        if docmeta['id'] is not None:
            output.set('id', docmeta['id'])
        if docmeta['fingerprint'] is not None:
            output.set('fingerprint', docmeta['fingerprint'])
    return output


def build_tei_output(docmeta):
    '''Build TEI-XML output tree based on extracted information'''
    # build TEI tree
    output = write_teitree(docmeta)
    # filter output (strip unwanted elements), just in case
    # check and repair
    output = check_tei(output, docmeta['url'])
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
            merge_with_parent(element)
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
        LOGGER.warning('not a valid TEI document: %s', TEI_RELAXNG.error_log.last_error)
    return result


def replace_element_text(element, include_formatting, include_links):
    '''Determine element text based on text and tail'''
    full_text = ''
    # handle formatting
    if include_formatting is True and element.text is not None:
        if element.tag == 'hi':
            if element.get('rend') == '#b':
                element.text = ''.join(['**', element.text, '**'])
            elif element.get('rend') == '#i':
                element.text = ''.join(['*', element.text, '*'])
            elif element.get('rend') == '#u':
                element.text = ''.join(['__', element.text, '__'])
            elif element.get('rend') == '#t':
                element.text = ''.join(['`', element.text, '`'])
        elif element.tag == 'del':
            element.text = ''.join(['~~', element.text, '~~'])
    # handle links
    if include_links is True and element.tag == 'ref':
        element.text = ''.join(['[', element.text, ']', '(', element.get('target'), ')'])
    # handle text
    if element.text is not None and element.tail is not None:
        full_text = ' '.join([element.text, element.tail])
    elif element.text is not None and element.tail is None:
        full_text = element.text
    elif element.text is None and element.tail is not None:
        full_text = element.tail
    return full_text


def merge_with_parent(element, include_formatting=False, include_links=False):
    '''Merge element with its parent and convert formatting to markdown.'''
    parent = element.getparent()
    if parent is None:
        return
    full_text = replace_element_text(element, include_formatting, include_links)
    previous = element.getprevious()
    if previous is not None:
        # There is a previous node, append text to its tail
        if previous.tail is not None:
            previous.tail = ' '.join([previous.tail, full_text])
        else:
            previous.tail = full_text
    else:
        # It's the first node in <parent/>, append to parent's text
        if parent.text is not None:
            parent.text = ' '.join([parent.text, full_text])
        else:
            parent.text = full_text
    parent.remove(element)


def xmltotxt(xmloutput, include_formatting, include_links):
    '''Convert to plain text format and optionally preserve formatting as markdown.'''
    returnlist = []
    # etree.strip_tags(xmloutput, 'div', 'main', 'span')
    # remove and insert into the previous tag
    for element in xmloutput.xpath('//hi|//ref'):
        merge_with_parent(element, include_formatting, include_links)
        continue
    # iterate and convert to list of strings
    for element in xmloutput.iter():
        # process text
        if element.text is None and element.tail is None:
            if element.tag == 'graphic':
                returnlist.extend(['\n', element.get('src')])
                if element.get('alt') is not None:
                    returnlist.extend([' ', element.get('alt')])
                if element.get('title') is not None:
                    returnlist.extend([' ', element.get('title')])
            # newlines for textless elements
            if element.tag in ('graphic', 'row', 'table'):
                returnlist.append('\n')
            continue
        textelement = replace_element_text(element, include_formatting, include_links)
        if element.tag in TEXTELEMS:
            returnlist.extend(['\n', textelement, '\n'])
        elif element.tag == 'item':
            returnlist.extend(['\n- ', textelement, '\n'])
        elif element.tag == 'cell':
            returnlist.extend(['|', textelement, '|'])
        elif element.tag == 'comments':
            returnlist.append('\n\n')
        else:
            LOGGER.debug('unexpected element: %s', element.tag)
            returnlist.extend([textelement, ' '])
    return sanitize(''.join(returnlist))


def write_teitree(docmeta):
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
    postbody = clean_attributes(docmeta['body'])
    postbody.tag = 'div'
    postbody.set('type', 'entry') # rendition='#pst'
    textbody.append(postbody)
    # comments
    if docmeta['commentsbody'] is not None:
        commentsbody = clean_attributes(docmeta['commentsbody'])
        commentsbody.tag = 'div'
        commentsbody.set('type', 'comments') # rendition='#cmt'
        textbody.append(commentsbody)
    return tei


def write_fullheader(header, docmeta):
    '''Write TEI header based on gathered metadata'''
    filedesc = etree.SubElement(header, 'fileDesc')
    bib_titlestmt = etree.SubElement(filedesc, 'titleStmt')
    bib_titlemain = etree.SubElement(bib_titlestmt, 'title', type='main')
    bib_titlemain.text = docmeta['title']
    if docmeta['author']:
        bib_author = etree.SubElement(bib_titlestmt, 'author')
        bib_author.text = docmeta['author']
    publicationstmt_a = etree.SubElement(filedesc, 'publicationStmt')
    # insert an empty paragraph for conformity
    publicationstmt_p = etree.SubElement(publicationstmt_a, 'p')
    notesstmt = etree.SubElement(filedesc, 'notesStmt')
    if docmeta['id'] is not None:
        idno = etree.SubElement(notesstmt, 'note', type='id')
        idno.text = docmeta['id']
    fingerprint = etree.SubElement(notesstmt, 'note', type='fingerprint')
    fingerprint.text = docmeta['fingerprint']
    sourcedesc = etree.SubElement(filedesc, 'sourceDesc')
    source_bibl = etree.SubElement(sourcedesc, 'bibl')
    # determination of sigle string
    if docmeta['sitename'] and docmeta['date']:
        sigle = docmeta['sitename'] + ', ' + docmeta['date']
    elif not docmeta['sitename'] and docmeta['date']:
        sigle = docmeta['date']
    elif docmeta['sitename'] and not docmeta['date']:
        sigle = docmeta['sitename']
    else:
        sigle = ''
    if docmeta['title']:
        source_bibl.text = docmeta['title'] + '. ' + sigle
    else:
        source_bibl.text = '. ' + sigle
    source_sigle = etree.SubElement(sourcedesc, 'bibl', type='sigle')
    source_sigle.text = sigle
    biblfull = etree.SubElement(sourcedesc, 'biblFull')
    bib_titlestmt = etree.SubElement(biblfull, 'titleStmt')
    bib_titlemain = etree.SubElement(bib_titlestmt, 'title', type='main')
    bib_titlemain.text = docmeta['title']
    if docmeta['author']:
        bib_author = etree.SubElement(bib_titlestmt, 'author')
        bib_author.text = docmeta['author']
    publicationstmt = etree.SubElement(biblfull, 'publicationStmt')
    publication_publisher = etree.SubElement(publicationstmt, 'publisher')
    if docmeta['hostname'] is not None:
        publisherstring = docmeta['sitename'].strip() + ' (' + docmeta['hostname'] + ')'
    else:
        publisherstring = docmeta['sitename']
    publication_publisher.text = publisherstring
    if docmeta['url'] is not None:
        publication_url = etree.SubElement(publicationstmt, 'ptr', type='URL', target=docmeta['url'])
    publication_date = etree.SubElement(publicationstmt, 'date')
    publication_date.text = docmeta['date']
    profiledesc = etree.SubElement(header, 'profileDesc')
    abstract = etree.SubElement(profiledesc, 'abstract')
    abstract_p = etree.SubElement(abstract, 'p')
    abstract_p.text = docmeta['description']
    if len(docmeta['categories']) > 0 or len(docmeta['tags']) > 0:
        textclass = etree.SubElement(profiledesc, 'textClass')
        keywords = etree.SubElement(textclass, 'keywords')
        if len(docmeta['categories']) > 0:
            cat_list = etree.SubElement(keywords, 'term', type='categories')
            cat_list.text = ','.join(docmeta['categories'])
        if len(docmeta['tags']) > 0:
            tags_list = etree.SubElement(keywords, 'term', type='tags')
            tags_list.text = ','.join(docmeta['tags'])
    encodingdesc = etree.SubElement(header, 'encodingDesc')
    appinfo = etree.SubElement(encodingdesc, 'appInfo')
    application = etree.SubElement(appinfo, 'application', version=__version__, ident='Trafilatura')
    label = etree.SubElement(application, 'label')
    label.text = 'Trafilatura'
    pointer = etree.SubElement(application, 'ptr', target='https://github.com/adbar/trafilatura')
    return header
