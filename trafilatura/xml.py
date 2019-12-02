# -*- coding: utf-8 -*-
# pylint:disable-msg=E0611,I1101
"""
All functions related to XML generation, processing and validation.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging

from io import StringIO
from lxml import etree

from .utils import fetch_url, sanitize, trim


LOGGER = logging.getLogger(__name__)
# validation
TEI_VALID_TAGS = {'code', 'body', 'del', 'div', 'fw', 'head', 'hi', 'item', \
                  'lb', 'list', 'p', 'quote'}
TEI_VALID_ATTRS = {'rendition', 'type'}
TEI_RELAXNG = None # to be downloaded later if necessary


#@profile
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


#@profile
def validate_tei(tei): # , filename=""
    '''Check if an XML document is conform to the guidelines of the Text Encoding Initiative'''
    global TEI_RELAXNG
    if TEI_RELAXNG is None:
        schema = fetch_url('https://tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng')
        if schema is None:
            LOGGER.error('No reference for validation available, aborting')
            return True
        # remove utf-8 declaration
        schema = schema.replace('<?xml version="1.0" encoding="utf-8"?>', '<?xml version="1.0"?>', 1)
        # load validator
        relaxng_doc = etree.parse(StringIO(schema))
        TEI_RELAXNG = etree.RelaxNG(relaxng_doc)
    result = TEI_RELAXNG.validate(tei)
    if result is False:
        print(TEI_RELAXNG.error_log.last_error)
    #try:
    #    result = relaxng.assert_(tei)
    #except AssertionError as err:
    #    LOGGER.warning('TEI validation error: %s', err)
    return result


#@profile
def xmltotxt(xmloutput):
    '''Convert to plain text format'''
    returnstring = ''
    # returnstring = ' '.join(xmloutput.itertext())
    for element in xmloutput.iter():
        if element.text is None and element.tail is None:
            continue
        if element.text is not None and element.tail is not None:
            textelement = element.text + ' ' + element.tail
        elif element.text is not None and element.tail is None:
            textelement = element.text
        else:
            textelement = element.tail
        textelement = sanitize(textelement)
        textelement = trim(textelement)
        if element.tag in ('code', 'head', 'lb', 'p', 'quote', 'row', 'table'):
            returnstring += '\n' + textelement + '\n'
        elif element.tag == 'item':
            returnstring += '\n- ' + textelement + '\n'
        else:
            returnstring += textelement + ' '
    #returnstring = sanitize(returnstring)
    #returnstring = trim(returnstring)
    return returnstring


#@profile
def write_teitree(postbody, commentsbody, url, doctitle, docdate):
    '''Bundle the extracted post and comments into a TEI tree'''
    tei = etree.Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
    header = etree.SubElement(tei, 'teiHeader')
    filedesc = etree.SubElement(header, 'fileDesc')
    titlestmt = etree.SubElement(filedesc, 'titleStmt')
    title = etree.SubElement(titlestmt, 'title')
    if doctitle is not None:
        title.text = doctitle
    publicationstmt = etree.SubElement(filedesc, 'publicationStmt')
    publication_p = etree.SubElement(publicationstmt, 'publisher')
    publication_date = etree.SubElement(publicationstmt, 'date')
    publication_date.set('type', 'publication')
    if docdate is not None:
        publication_date.text = docdate
    sourcedesc = etree.SubElement(filedesc, 'sourceDesc')
    source_p = etree.SubElement(sourcedesc, 'p')
    source_p.text = url
    textelem = etree.SubElement(tei, 'text')
    textbody = etree.SubElement(textelem, 'body')
    # post
    postbody.tag = 'div'
    postbody.set('type', 'entry') # rendition='#pst'
    # postelem = etree.SubElement(textbody, 'div', type='entry')
    textbody.append(postbody)
    # comments
    if commentsbody is not None:
        commentsbody.tag = 'div'
        commentsbody.set('type', 'comments')# rendition='#cmt'
        # commentselem = etree.SubElement(textbody, 'div', type='comments')
        textbody.append(commentsbody)
    return tei
