# pylint:disable-msg=E0611,I1101
"""
All functions related to XML generation, processing and validation.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import lzma

from json import dumps as json_dumps
from html import unescape
from pathlib import Path
from pickle import load as load_pickle

from lxml.etree import Element, RelaxNG, SubElement, XMLParser, fromstring, tostring

from . import __version__
from .filters import text_chars_test
from .utils import sanitize


LOGGER = logging.getLogger(__name__)
# validation
TEI_SCHEMA = str(Path(__file__).parent / 'data/tei-schema-pickle.lzma')
TEI_VALID_TAGS = {'body', 'cell', 'code', 'del', 'div', 'fw', 'graphic', 'head', 'hi', \
                  'item', 'lb', 'list', 'p', 'quote', 'ref', 'row', 'table'}
TEI_VALID_ATTRS = {'rend', 'rendition', 'role', 'target', 'type'}
TEI_RELAXNG = None  # to be downloaded later if necessary

CONTROL_PARSER = XMLParser(remove_blank_text=True)

NEWLINE_ELEMS = {'code', 'fw', 'graphic', 'head', 'lb', 'list', 'p', 'quote', 'row', 'table'}
SPECIAL_FORMATTING = {'del', 'head', 'hi'}
WITH_ATTRIBUTES = {'del', 'fw', 'graphic', 'head', 'hi', 'item', 'list', 'ref'}


def build_json_output(docmeta):
    '''Build JSON output based on extracted information'''
    outputdict = {slot: getattr(docmeta, slot, None) for slot in docmeta.__slots__}
    outputdict['source'] = outputdict.pop('url')
    outputdict['source-hostname'] = outputdict.pop('sitename')
    outputdict['excerpt'] = outputdict.pop('description')
    outputdict['categories'] = ';'.join(outputdict['categories'])
    outputdict['tags'] = ';'.join(outputdict['tags'])
    outputdict['text'] = xmltotxt(outputdict.pop('body'), include_formatting=False)
    if outputdict['commentsbody'] is not None:
        outputdict['comments'] = xmltotxt(outputdict.pop('commentsbody'), include_formatting=False)
    else:
        del outputdict['commentsbody']
    return json_dumps(outputdict, ensure_ascii=False)


def clean_attributes(tree):
    '''Remove unnecessary attributes.'''
    for elem in tree.iter('*'):
        if elem.tag not in WITH_ATTRIBUTES:
            elem.attrib.clear()
    return tree


def remove_empty_elements(tree):
    '''Remove text elements without text.'''
    for element in tree.iter('fw', 'head', 'hi', 'item', 'p'):
        if len(element) == 0 and text_chars_test(element.text) is False and text_chars_test(element.tail) is False:
            element.getparent().remove(element)
    return tree


def build_xml_output(docmeta):
    '''Build XML output tree based on extracted information'''
    output = Element('doc')
    output = add_xml_meta(output, docmeta)
    docmeta.body.tag = 'main'
    # clean XML tree
    docmeta.body = remove_empty_elements(docmeta.body)
    output.append(clean_attributes(docmeta.body))
    if docmeta.commentsbody is not None:
        docmeta.commentsbody.tag = 'comments'
        output.append(clean_attributes(docmeta.commentsbody))
# XML invalid characters
# https://chase-seibert.github.io/blog/2011/05/20/stripping-control-characters-in-python.html
    return output


def control_xml_output(output_tree, output_format, tei_validation, docmeta):
    '''Make sure the XML output is conform and valid if required'''
    control_string = sanitize(tostring(output_tree, encoding='unicode'))
    # necessary for cleaning
    output_tree = fromstring(control_string, CONTROL_PARSER)
    # validate
    if output_format == 'xmltei' and tei_validation is True:
        result = validate_tei(output_tree)
        LOGGER.info('TEI validation result: %s %s %s', result, docmeta.id, docmeta.url)
    return tostring(output_tree, pretty_print=True, encoding='unicode').strip()


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
        if docmeta.hostname is not None:
            output.set('hostname', docmeta.hostname)
        if docmeta.description is not None:
            output.set('excerpt', docmeta.description)
        if docmeta.categories is not None:
            output.set('categories', ';'.join(docmeta.categories))
        if docmeta.tags is not None:
            output.set('tags', ';'.join(docmeta.tags))
        if docmeta.license is not None:
            output.set('license', docmeta.license)
        if docmeta.id is not None:
            output.set('id', docmeta.id)
        if docmeta.fingerprint is not None:
            output.set('fingerprint', docmeta.fingerprint)
        if docmeta.language is not None:
            output.set('language', docmeta.language)
    return output


def build_tei_output(docmeta):
    '''Build TEI-XML output tree based on extracted information'''
    # build TEI tree
    output = write_teitree(docmeta)
    # filter output (strip unwanted elements), just in case
    # check and repair
    output = check_tei(output, docmeta.url)
    return output


def check_tei(xmldoc, url):
    '''Check if the resulting XML file is conform and scrub remaining tags'''
    # convert head tags
    for elem in xmldoc.iter('head'):
        elem.tag = 'fw'
        elem.set('type', 'header')
    # look for elements that are not valid
    for element in xmldoc.findall('.//text/body//*'):
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
    return xmldoc


def validate_tei(xmldoc):  # , filename=""
    '''Check if an XML document is conform to the guidelines of the Text Encoding Initiative'''
    global TEI_RELAXNG
    if TEI_RELAXNG is None:
        # load validator
        with lzma.open(TEI_SCHEMA, 'rb') as schemafile:
            schema_data = load_pickle(schemafile)
        TEI_RELAXNG = RelaxNG(fromstring(schema_data))
    result = TEI_RELAXNG.validate(xmldoc)
    if result is False:
        LOGGER.warning('not a valid TEI document: %s', TEI_RELAXNG.error_log.last_error)
    return result


def replace_element_text(element, include_formatting):
    '''Determine element text based on text and tail'''
    full_text = ''
    # handle formatting: convert to markdown
    if include_formatting is True:
        if element.tag in ('del', 'head') and element.text is not None:
            if element.tag == 'head':
                try:
                    number = int(element.get('rend')[1])
                except (TypeError, ValueError):
                    number = 2
                element.text = ''.join(['='*number, ' ', element.text, ' ', '='*number])
            elif element.tag == 'del':
                element.text = ''.join(['~~', element.text, '~~'])
        elif element.tag == 'hi':
            if element.get('rend') == '#b':
                element.text = ''.join(['**', element.text, '**'])
            elif element.get('rend') == '#i':
                element.text = ''.join(['*', element.text, '*'])
            elif element.get('rend') == '#u':
                element.text = ''.join(['__', element.text, '__'])
            elif element.get('rend') == '#t':
                element.text = ''.join(['`', element.text, '`'])
    # handle links
    if element.tag == 'ref':
        try:
            element.text = ''.join(['[', element.text, ']', '(', element.get('target'), ')'])
        except TypeError:
            LOGGER.warning('missing link attribute: %s %s', element.text, element.attrib)
            try:
                element.text = ''.join(['[', element.text, ']'])
            except TypeError:
                LOGGER.error('empty link: %s %s', element.text, element.attrib)
    # handle text
    if element.text is not None and element.tail is not None:
        full_text = ''.join([element.text, element.tail])
    elif element.text is not None:
        full_text = element.text
    elif element.tail is not None:
        full_text = element.tail
    return full_text


def merge_with_parent(element, include_formatting=False):
    '''Merge element with its parent and convert formatting to markdown.'''
    parent = element.getparent()
    if parent is None:
        return
    full_text = replace_element_text(element, include_formatting)
    previous = element.getprevious()
    if previous is not None:
        # There is a previous node, append text to its tail
        if previous.tail is not None:
            previous.tail = ' '.join([previous.tail, full_text])
        else:
            previous.tail = full_text
    elif parent.text is not None:
        parent.text = ' '.join([parent.text, full_text])
    else:
        parent.text = full_text
    parent.remove(element)


def xmltotxt(xmloutput, include_formatting):
    '''Convert to plain text format and optionally preserve formatting as markdown.'''
    returnlist = []
    # strip_tags(xmloutput, 'div', 'main', 'span')
    # iterate and convert to list of strings
    for element in xmloutput.iter('*'):
        if element.text is None and element.tail is None:
            if element.tag == 'graphic':
                # add source, default to ''
                text = element.get('title', '')
                if element.get('alt') is not None:
                    text += ' ' + element.get('alt')
                returnlist.extend(['![', text, ']', '(', element.get('src', ''), ')'])
            # newlines for textless elements
            if element.tag in ('graphic', 'row', 'table'):
                returnlist.append('\n')
            continue
        # process text
        textelement = replace_element_text(element, include_formatting)
        # common elements
        if element.tag in NEWLINE_ELEMS:
            returnlist.extend(['\n', textelement, '\n'])
        # particular cases
        elif element.tag == 'item':
            returnlist.extend(['\n- ', textelement, '\n'])
        elif element.tag == 'cell':
            returnlist.extend(['|', textelement, '|'])
        elif element.tag == 'comments':
            returnlist.append('\n\n')
        else:
            if element.tag not in SPECIAL_FORMATTING:
                LOGGER.debug('unprocessed element in output: %s', element.tag)
            returnlist.extend([textelement, ' '])
    return unescape(sanitize(''.join(returnlist)))


def write_teitree(docmeta):
    '''Bundle the extracted post and comments into a TEI tree'''
    teidoc = Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
    header = write_fullheader(teidoc, docmeta)
    textelem = SubElement(teidoc, 'text')
    textbody = SubElement(textelem, 'body')
    # post
    postbody = clean_attributes(docmeta.body)
    postbody.tag = 'div'
    postbody.set('type', 'entry') # rendition='#pst'
    textbody.append(postbody)
    # comments
    if docmeta.commentsbody is not None:
        commentsbody = clean_attributes(docmeta.commentsbody)
        commentsbody.tag = 'div'
        commentsbody.set('type', 'comments') # rendition='#cmt'
        textbody.append(commentsbody)
    return teidoc


def _define_publisher_string(docmeta):
    '''Construct a publisher string to include in TEI header'''
    if docmeta.hostname and docmeta.sitename:
        publisherstring = docmeta.sitename.strip() + ' (' + docmeta.hostname + ')'
    elif docmeta.hostname:
        publisherstring = docmeta.hostname
    elif docmeta.sitename:
        publisherstring = docmeta.sitename
    else:
        LOGGER.warning('no publisher for URL %s', docmeta.url)
        publisherstring = 'N/A'
    return publisherstring


def write_fullheader(teidoc, docmeta):
    '''Write TEI header based on gathered metadata'''
    # todo: add language info
    header = SubElement(teidoc, 'teiHeader')
    filedesc = SubElement(header, 'fileDesc')
    bib_titlestmt = SubElement(filedesc, 'titleStmt')
    bib_titlemain = SubElement(bib_titlestmt, 'title', type='main')
    bib_titlemain.text = docmeta.title
    if docmeta.author:
        bib_author = SubElement(bib_titlestmt, 'author')
        bib_author.text = docmeta.author
    publicationstmt_a = SubElement(filedesc, 'publicationStmt')
    publisher_string = _define_publisher_string(docmeta)
    # license, if applicable
    if docmeta.license:
        publicationstmt_publisher = SubElement(publicationstmt_a, 'publisher')
        publicationstmt_publisher.text = publisher_string
        availability = SubElement(publicationstmt_a, 'availability')
        avail_p = SubElement(availability, 'p')
        avail_p.text = docmeta.license
    # insert an empty paragraph for conformity
    else:
        publicationstmt_p = SubElement(publicationstmt_a, 'p')
    notesstmt = SubElement(filedesc, 'notesStmt')
    if docmeta.id:
        idno = SubElement(notesstmt, 'note', type='id')
        idno.text = docmeta.id
    fingerprint = SubElement(notesstmt, 'note', type='fingerprint')
    fingerprint.text = docmeta.fingerprint
    sourcedesc = SubElement(filedesc, 'sourceDesc')
    source_bibl = SubElement(sourcedesc, 'bibl')
    # determination of sigle string
    if docmeta.sitename and docmeta.date:
        sigle = docmeta.sitename + ', ' + docmeta.date
    elif not docmeta.sitename and docmeta.date:
        sigle = docmeta.date
    elif docmeta.sitename:
        sigle = docmeta.sitename
    else:
        LOGGER.warning('no sigle for URL %s', docmeta.url)
        sigle = ''
    if docmeta.title:
        source_bibl.text = docmeta.title + '. ' + sigle
    else:
        source_bibl.text = '. ' + sigle
    source_sigle = SubElement(sourcedesc, 'bibl', type='sigle')
    source_sigle.text = sigle
    biblfull = SubElement(sourcedesc, 'biblFull')
    bib_titlestmt = SubElement(biblfull, 'titleStmt')
    bib_titlemain = SubElement(bib_titlestmt, 'title', type='main')
    bib_titlemain.text = docmeta.title
    if docmeta.author:
        bib_author = SubElement(bib_titlestmt, 'author')
        bib_author.text = docmeta.author
    publicationstmt = SubElement(biblfull, 'publicationStmt')
    publication_publisher = SubElement(publicationstmt, 'publisher')
    publication_publisher.text = publisher_string
    if docmeta.url:
        publication_url = SubElement(publicationstmt, 'ptr', type='URL', target=docmeta.url)
    publication_date = SubElement(publicationstmt, 'date')
    publication_date.text = docmeta.date
    profiledesc = SubElement(header, 'profileDesc')
    abstract = SubElement(profiledesc, 'abstract')
    abstract_p = SubElement(abstract, 'p')
    abstract_p.text = docmeta.description
    if len(docmeta.categories) > 0 or len(docmeta.tags) > 0:
        textclass = SubElement(profiledesc, 'textClass')
        keywords = SubElement(textclass, 'keywords')
        if len(docmeta.categories) > 0:
            cat_list = SubElement(keywords, 'term', type='categories')
            cat_list.text = ','.join(docmeta.categories)
        if len(docmeta.tags) > 0:
            tags_list = SubElement(keywords, 'term', type='tags')
            tags_list.text = ','.join(docmeta.tags)
    encodingdesc = SubElement(header, 'encodingDesc')
    appinfo = SubElement(encodingdesc, 'appInfo')
    application = SubElement(appinfo, 'application', version=__version__, ident='Trafilatura')
    label = SubElement(application, 'label')
    label.text = 'Trafilatura'
    pointer = SubElement(application, 'ptr', target='https://github.com/adbar/trafilatura')
    return header
