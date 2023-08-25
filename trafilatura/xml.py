# pylint:disable-msg=E0611,I1101
"""
All functions related to XML generation, processing and validation.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import logging
import lzma
from html import unescape
from json import dumps as json_dumps
from pathlib import Path
from pickle import load as load_pickle

from lxml.etree import (Element, RelaxNG, SubElement, XMLParser, fromstring,
                        tostring)

from . import __version__
from .filters import text_chars_test
from .utils import sanitize

LOGGER = logging.getLogger(__name__)
# validation
TEI_SCHEMA = str(Path(__file__).parent / 'data/tei-schema-pickle.lzma')
TEI_VALID_TAGS = {'ab', 'body', 'cell', 'code', 'del', 'div', 'graphic', 'head', 'hi', \
                  'item', 'lb', 'list', 'p', 'quote', 'ref', 'row', 'table'}
TEI_VALID_ATTRS = {'rend', 'rendition', 'role', 'target', 'type'}
TEI_RELAXNG = None  # to be downloaded later if necessary
TEI_REMOVE_TAIL = {"ab", "p"}

CONTROL_PARSER = XMLParser(remove_blank_text=True)

NEWLINE_ELEMS = {
    'cell': '|',
    'item': '\n- ',
    **{tag: '\n' for tag in ['code', 'graphic', 'head', 'lb', 'list', 'p', 'quote', 'row', 'table']}
}
SPECIAL_FORMATTING = {'del', 'head', 'hi'}
WITH_ATTRIBUTES = {'cell', 'del', 'graphic', 'head', 'hi', 'item', 'list', 'ref'}

NESTING_WHITELIST = {"cell", "figure", "item", "note", "quote"}

META_ATTRIBUTES = [
    'sitename', 'title', 'author', 'date', 'url', 'hostname',
    'description', 'categories', 'tags', 'license', 'id',
    'fingerprint', 'language'
]

HI_FORMATTING = {'#b': '**', '#i': '*', '#u': '__', '#t': '`'}


def build_json_output(docmeta):
    '''Build JSON output based on extracted information'''
    outputdict = {slot: getattr(docmeta, slot, None) for slot in docmeta.__slots__}
    outputdict.update({
        'source': outputdict.pop('url'),
        'source-hostname': outputdict.pop('sitename'),
        'excerpt': outputdict.pop('description'),
        'categories': ';'.join(outputdict.pop('categories')),
        'tags': ';'.join(outputdict.pop('tags')),
        'text': xmltotxt(outputdict.pop('body'), include_formatting=False),
    })

    commentsbody = outputdict.pop('commentsbody')
    if commentsbody is not None:
        outputdict['comments'] = xmltotxt(commentsbody, include_formatting=False)

    return json_dumps(outputdict, ensure_ascii=False)


def clean_attributes(tree):
    '''Remove unnecessary attributes.'''
    for elem in tree.iter('*'):
        if elem.tag not in WITH_ATTRIBUTES:
            elem.attrib.clear()
    return tree


def remove_empty_elements(tree):
    '''Remove text elements without text.'''
    for element in tree.iter('*'):  # 'head', 'hi', 'item', 'p'
        if len(element) == 0 and text_chars_test(element.text) is False and text_chars_test(element.tail) is False:
            parent = element.getparent()
            # not root element or element which is naturally empty
            if parent is not None and element.tag != "graphic":
                element.getparent().remove(element)
    return tree


def strip_double_tags(tree):
    "Prevent nested tags among a fixed list of tags."
    for elem in reversed(tree.xpath(".//head | .//code | .//p")):
        for subelem in elem.iterdescendants("code", "head", "p"):
            if subelem.getparent().tag in NESTING_WHITELIST:
                continue
            if subelem.tag == elem.tag:
                merge_with_parent(subelem)
    return tree


def build_xml_output(docmeta):
    '''Build XML output tree based on extracted information'''
    output = Element('doc')
    output = add_xml_meta(output, docmeta)
    docmeta.body.tag = 'main'
    # clean XML tree
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
        LOGGER.debug('TEI validation result: %s %s %s', result, docmeta.id, docmeta.url)
    return tostring(output_tree, pretty_print=True, encoding='unicode').strip()


def add_xml_meta(output, docmeta):
    '''Add extracted metadata to the XML output tree'''
    for attribute in META_ATTRIBUTES:
        value = getattr(docmeta, attribute, None)
        if value is not None:
            output.set(attribute, value if isinstance(value, str) else ';'.join(value))
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
        elem.tag = 'ab'
        elem.set('type', 'header')
        parent = elem.getparent()
        if len(elem) > 0:
            new_elem = _tei_handle_complex_head(elem)
            parent.replace(elem, new_elem)
            elem = new_elem
        if parent.tag == "p":
            _move_element_one_level_up(elem)
    # convert <lb/> when child of <div> to <p>
    for element in xmldoc.findall(".//text/body//div/lb"):
        if element.tail and element.tail.strip():
            element.tag = 'p'
            element.text = element.tail
            element.tail = None
    # look for elements that are not valid
    for element in xmldoc.findall('.//text/body//*'):
        if element.tag in TEI_REMOVE_TAIL and element.tail and element.tail.strip():
            _handle_unwanted_tails(element)
        # check elements
        if element.tag not in TEI_VALID_TAGS:
            # disable warnings for chosen categories
            # if element.tag not in ('div', 'span'):
            LOGGER.warning('not a TEI element, removing: %s %s', element.tag, url)
            merge_with_parent(element)
            continue
        if element.tag == "div":
            _handle_text_content_of_div_nodes(element)
            _wrap_unwanted_siblings_of_div(element)
        # check attributes
        for attribute in element.attrib:
            if attribute not in TEI_VALID_ATTRS:
                LOGGER.warning('not a valid TEI attribute, removing: %s in %s %s', attribute, element.tag, url)
                element.attrib.pop(attribute)
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
    # handle formatting: convert to markdown
    if include_formatting is True and element.text is not None:
        if element.tag in ('del', 'head'):
            if element.tag == 'head':
                try:
                    number = int(element.get('rend')[1])
                except (TypeError, ValueError):
                    number = 2
                element.text = f'{"#" * number} {element.text}'
            elif element.tag == 'del':
                element.text = f'~~{element.text}~~'
        elif element.tag == 'hi':
            rend = element.get('rend')
            if rend in HI_FORMATTING:
                element.text = f'{HI_FORMATTING[rend]}{element.text}{HI_FORMATTING[rend]}'
    # handle links
    if element.tag == 'ref':
        if element.text is not None:
            link_text = f'[{element.text}]'
            if element.get('target') is not None:
                element.text = f"{link_text}({element.get('target')})"
            else:
                LOGGER.warning('missing link attribute: %s %s', element.text, element.attrib)
                element.text = link_text
        else:
            LOGGER.warning('empty link: %s %s', element.text, element.attrib)
    # handle text
    return (element.text or '') + (element.tail or '')


def merge_with_parent(element, include_formatting=False):
    '''Merge element with its parent and convert formatting to markdown.'''
    parent = element.getparent()
    if not parent:
        return

    full_text = replace_element_text(element, include_formatting)

    previous = element.getprevious()
    if previous is not None:
        # There is a previous node, append text to its tail
        if previous.tail is not None:
            previous.tail = f'{previous.tail} {full_text}'
        else:
            previous.tail = full_text
    elif parent.text is not None:
        parent.text = f'{parent.text} {full_text}'
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
                text = f'{element.get("title", "")} {element.get("alt", "")}'
                returnlist.extend(['![', text.strip(), ']', '(', element.get('src', ''), ')'])
            # newlines for textless elements
            if element.tag in ('graphic', 'row', 'table'):
                returnlist.append('\n')
            continue
        # process text
        textelement = replace_element_text(element, include_formatting)
        # common elements
        if element.tag in NEWLINE_ELEMS:
            returnlist.extend([NEWLINE_ELEMS[element.tag], textelement, '\n'])
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
        publisherstring = f'{docmeta.sitename.strip()} ({docmeta.hostname})'
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


def _handle_text_content_of_div_nodes(element):
    if element.text and element.text.strip():
        if element.getchildren() and element[0].tag == 'p':
            p_text = element[0].text or ""
            element[0].text = f'{element.text} {p_text}'.strip()
        else:
            new_child = Element("p")
            new_child.text = element.text
            element.insert(0, new_child)
        element.text = None

    if element.tail and element.tail.strip():
        if element.getchildren() and element[-1].tag == 'p':
            p_text = element[-1].text or ""
            element[-1].text = f'{p_text} {element.tail}'.strip()
        else:
            new_child = Element("p")
            new_child.text = element.tail
            element.append(new_child)
        element.tail = None


def _handle_unwanted_tails(element):
    "Handle tail on p and ab elements"
    if element.tag == 'p':
        if element.text:
            element.text += ' ' + element.tail.strip()
        else:
            element.text = element.tail
    else:
        new_sibling = Element('p')
        new_sibling.text = element.tail.strip()
        parent = element.getparent()
        parent.insert(parent.index(element) + 1 , new_sibling)
    element.tail = None


def _tei_handle_complex_head(element):
    new_element = Element('ab', attrib=element.attrib)
    new_element.text = element.text.strip() if element.text is not None else None
    for child in element.iterchildren():
        if child.tag == 'p':
            if len(new_element) > 0 or new_element.text:
                # add <lb> if <ab> has no children or last tail contains text
                if len(new_element) == 0 or new_element[-1].tail:
                    SubElement(new_element, 'lb')
                new_element[-1].tail = child.text
            else:
                new_element.text = child.text
        else:
            new_element.append(child)
    if element.tail is not None and element.tail.strip():
        new_element.tail = element.tail.strip()
    return new_element


def _wrap_unwanted_siblings_of_div(div_element):
    new_sibling = Element("div")
    new_sibling_index = None
    parent = div_element.getparent()
    # check siblings after target element
    for sibling in div_element.itersiblings():
        if sibling.tag == "div":
            break
        if sibling.tag in {"p", "list", "table", "quote", "ab"}:
            if new_sibling_index is None:
                new_sibling_index = parent.index(sibling)
            new_sibling.append(sibling)
        # some elements (e.g. <lb/>) can appear next to div, but
        # order of elements should be kept, thus add and reset new_sibling
        else:
            if new_sibling_index is not None and len(new_sibling) != 0:
                parent.insert(new_sibling_index, new_sibling)
                new_sibling = Element("div")
                new_sibling_index = None
    if new_sibling_index is not None and len(new_sibling) != 0:
        parent.insert(new_sibling_index, new_sibling)


def _move_element_one_level_up(element):
    parent = element.getparent()
    new_elem = Element("p")
    new_elem.extend(sibling for sibling in element.itersiblings())

    parent.addnext(element)

    if element.tail is not None and element.tail.strip():
        new_elem.text = element.tail.strip()
        element.tail = None
    if len(new_elem) != 0 or new_elem.text:
        element.addnext(new_elem)
    if len(parent) == 0 and parent.text is None:
        parent.getparent().remove(parent)
