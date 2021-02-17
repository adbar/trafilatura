# pylint:disable-msg=E0611,I1101
"""
Module bundling all functions needed to extract the text in a webpage.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


# standard
import logging
import re # import regex as re

from collections import OrderedDict
from copy import deepcopy

from lxml import etree, html

# own
from .external import justext_rescue, sanitize_tree, SANITIZED_XPATH, try_readability
from .filters import (check_html_lang, content_fingerprint, duplicate_test,
                     language_filter, text_chars_test)
from .htmlprocessing import (convert_tags, discard_unwanted,
                             discard_unwanted_comments, handle_textnode,
                             link_density_test, link_density_test_tables,
                             process_node, tree_cleaning)
from .metadata import extract_metadata, METADATA_LIST
from .settings import use_config, DEFAULT_CONFIG, TAG_CATALOG
from .utils import load_html, trim, txttocsv, is_image_file
from .xml import (build_json_output, build_xml_output, build_tei_output,
                  control_xml_output, xmltotxt)
from .xpaths import BODY_XPATH, COMMENTS_XPATH


LOGGER = logging.getLogger(__name__)


def handle_titles(element):
    '''Process head elements (titles)'''
    # maybe needs attention
    if element.tail and re.search(r'\w', element.tail):
        LOGGER.debug('tail in title, stripping: %s', element.tail)
    element.tail = None
    title = process_node(element)
    if title is not None and title.text and re.search(r'\w', title.text):
        return title
    return None


def handle_formatting(element):
    '''Process formatting elements (b, i, etc. converted to hi) found
       outside of paragraphs'''
    processed_element = None
    if element.text is not None or element.tail is not None:
        processed_element = etree.Element('p')
        processed_child = etree.SubElement(processed_element, element.tag)
        if text_chars_test(element.text) is True:
            processed_child.text = trim(element.text)
        if text_chars_test(element.tail) is True:
            processed_child.tail = trim(element.tail)
    return processed_element


def handle_lists(element, dedupbool, config):
    '''Process lists elements'''
    processed_element = etree.Element(element.tag)
    for child in element.iter('item'):
        newchildelem = etree.Element('item')
        if len(child) == 0:
            processed_child = process_node(child)
            if processed_child is not None:
                newchildelem.text, newchildelem.tail = processed_child.text, processed_child.tail
                processed_element.append(newchildelem)
        else:
            # proceed with iteration, fix for nested elements
            for subelem in child.iter():
                processed_subchild = handle_textnode(subelem, comments_fix=False, deduplicate=dedupbool, config=config)
                # add child element to processed_element
                if processed_subchild is not None:
                    subchildelem = etree.SubElement(newchildelem, processed_subchild.tag)
                    subchildelem.text, subchildelem.tail = processed_subchild.text, processed_subchild.tail
                subelem.tag = 'done'
            etree.strip_tags(newchildelem, 'item')
        if newchildelem.text or len(newchildelem) > 0:
            processed_element.append(newchildelem)
        child.tag = 'done'
    # avoid double tags??
    if len(processed_element) > 0:  # if it has children
        # test if it has text
        if text_chars_test(''.join(processed_element.itertext())) is True:
            return processed_element
    return None


def handle_quotes(element):
    '''Process quotes elements'''
    processed_element = etree.Element(element.tag)
    for child in element.iter():
        processed_child = process_node(child) # handle_textnode(child, comments_fix=True)
        if processed_child is not None:
            newsub = etree.SubElement(processed_element, child.tag)
            newsub.text, newsub.tail = processed_child.text, processed_child.tail
        child.tag = 'done'
    if len(processed_element) > 0:
        # avoid double/nested tags
        etree.strip_tags(processed_element, 'quote')
        # test if it has text
        # teststring = ''.join(processed_element.itertext())
        # if len(teststring) > 0 and re.search(r'[p{L}]', teststring):
        return processed_element
    return None


def handle_other_elements(element, potential_tags, dedupbool, config):
    '''Handle diverse or unknown elements in the scope of relevant tags'''
    # delete unwanted
    if element.tag not in potential_tags:
        # LOGGER.debug('discarding: %s %s', element.tag, element.text)
        return None
    if element.tag == 'div':
        processed_element = handle_textnode(element, comments_fix=False, deduplicate=dedupbool, config=config)
        if processed_element is not None:
            processed_element.attrib.clear()
            # small div-correction # could be moved elsewhere
            if processed_element.tag == 'div':
                processed_element.tag = 'p'
            # insert
            return processed_element
    else:
        LOGGER.warning('unexpected element seen: %s %s', element.tag, element.text)
    return None


def handle_paragraphs(element, potential_tags, dedupbool, config):
    '''Process paragraphs (p) elements along with their children,
       trim and clean the content'''
    element.attrib.clear()
    #etree.strip_tags(element, 'p')  # change in precision
    # no children
    if len(element) == 0:
        processed_element = process_node(element)  # handle_textnode(element, comments_fix=False)
        if processed_element is not None:
            return processed_element
        return None
    # children
    processed_element = etree.Element(element.tag)
    for child in element.iter():
        if child.tag not in potential_tags:
            LOGGER.warning('unexpected in p: %s %s %s', child.tag, child.text, child.tail)
            continue
        processed_child = handle_textnode(child, comments_fix=False, deduplicate=dedupbool, config=config)
        if processed_child is not None:
            # needing attention!
            if child.tag == 'p':
                LOGGER.debug('extra p within p: %s %s %s', child.tag, child.text, child.tail)
                if processed_element.text:
                    processed_element.text += ' ' + trim(child.text)
                else:
                    processed_element.text = trim(child.text)
                continue
            newsub = etree.Element(child.tag)
            # handle formatting
            if child.tag in ('hi', 'ref'):
                # check depth and clean
                if len(child) > 0:
                    for item in child:  # children are lists
                        if text_chars_test(item.text) is True:
                            item.text = ' ' + item.text
                        etree.strip_tags(child, item.tag)
                if child.tag == 'hi':
                    newsub.set('rend', child.get('rend'))
                elif child.tag == 'ref':
                    newsub.set('target', child.get('target'))
            # handle line breaks
            elif child.tag == 'lb':
                try:
                    processed_child.tail = process_node(child).tail
                except AttributeError:  # no text
                    pass
            # prepare text
            if text_chars_test(processed_child.text) is False:
                processed_child.text = ''
            # if there are already children
            if len(processed_element) > 0:
                if text_chars_test(processed_child.tail) is True:
                    newsub.tail = processed_child.text + processed_child.tail
                else:
                    newsub.tail = processed_child.text
            else:
                newsub.text, newsub.tail = processed_child.text, processed_child.tail
            processed_element.append(newsub)
            child.tag = 'done'
    # finish
    if len(processed_element) > 0 or processed_element.text:
        # clean trailing lb-elements
        if len(processed_element) > 0 and processed_element[-1].tag == 'lb' and processed_element[-1].tail is None:
            processed_element[-1].getparent().remove(processed_element[-1])
        return processed_element
    LOGGER.debug('discarding p-child: %s', html.tostring(processed_element))
    return None


def handle_table(table_elem):
    '''Process single table element'''
    newtable = etree.Element('table')
    newrow = etree.Element('row')
    i = 0
    # strip these structural elements
    etree.strip_tags(table_elem, 'thead', 'tbody', 'tfoot')
    # explore sub-elements
    for subelement in table_elem.iter():
        i += 1
        if subelement.tag == 'tr':
            # process existing row
            if len(newrow) > 0:
                newtable.append(newrow)
                newrow = etree.Element('row')
            # skip rows empty of text
            #textcontent = ''.join(subelement.itertext())
            #if len(textcontent) == 0 or not re.search(r'[p{L}]+', textcontent):
            #    continue
        elif subelement.tag in ('td', 'th'):
            # process
            processed_cell = process_node(subelement)
            if processed_cell is None or processed_cell.text is None or not processed_cell.text:
                continue
            # define tag
            newsub = etree.SubElement(newrow, 'cell')
            if subelement.tag == 'th':
                newsub.set('role', 'head')
            newsub.text = processed_cell.text
            #newrow.append(newsub)
        # beware of nested tables
        elif subelement.tag == 'table' and i > 1:
            break
    # end of processing
    if len(newrow) > 0:
        newtable.append(newrow)
    if len(newtable) > 0:
        return newtable
    return None


def handle_image(element):
    '''Process image element'''
    if not 'data-src' in element.attrib and not 'src' in element.attrib:
        return None
    # image source
    processed_element = etree.Element(element.tag)
    if element.get('data-src') is not None and is_image_file(element.get('data-src')):
        processed_element.set('src', element.get('data-src'))
    elif element.get('src') is not None and is_image_file(element.get('src')):
        processed_element.set('src', element.get('src'))
    # additional data
    if element.get('alt') is not None:
        processed_element.set('alt', element.get('alt'))
    if element.get('title') is not None:
        processed_element.set('title', element.get('title'))
    return processed_element


def recover_wild_text(tree, result_body, potential_tags=TAG_CATALOG, deduplicate=True, config=None):
    '''Look for all previously unconsidered wild elements, including outside of the determined
       frame and throughout the document to recover potentially missing text parts'''
    LOGGER.debug('Taking all p-elements')
    # prune
    search_tree = discard_unwanted(tree)
    # decide if links are preserved
    if 'ref' in potential_tags:
        etree.strip_tags(search_tree, 'span')
    else:
        etree.strip_tags(search_tree, 'a', 'ref', 'span')
    processed_elems = [handle_textelem(element, potential_tags, deduplicate, config) for element in search_tree.iter('blockquote', 'code', 'div', 'p', 'pre', 'q', 'quote', 'table')]
    result_body.extend(list(filter(None.__ne__, processed_elems)))
    return result_body


def handle_textelem(element, potential_tags, dedupbool, config):
    '''Process text element and determine how to deal with its content'''
    new_element = None
    # bypass: nested elements
    if element.tag == 'list':
        new_element = handle_lists(element, dedupbool, config)
    elif element.tag == 'quote' or element.tag == 'code':
        new_element = handle_quotes(element)
    elif element.tag == 'head':
        new_element = handle_titles(element)
    elif element.tag == 'p':
        new_element = handle_paragraphs(element, potential_tags, dedupbool, config)
    elif element.tag == 'lb':
        if text_chars_test(element.tail) is True:
            element = process_node(element)
            if element is not None:
                new_element = etree.Element('p')
                new_element.text = element.tail
    elif element.tag in ('hi', 'ref'):
        new_element = handle_formatting(element)
    elif element.tag == 'table' and 'table' in potential_tags:
        new_element = handle_table(element)
    elif element.tag == 'graphic' and 'graphic' in potential_tags:
        new_element = handle_image(element)
    else:
        # other elements (div, ??, ??)
        new_element = handle_other_elements(element, potential_tags, dedupbool, config)
    return new_element


def delete_by_link_density(subtree, tagname, backtracking=False):
    '''Determine the link density of elements with respect to their length,
       and remove the elements identified as boilerplate.'''
    myelems, deletions = dict(), list()
    for elem in subtree.iter(tagname):
        result, templist = link_density_test(elem)
        if result is True:
            deletions.append(elem)
        elif backtracking is True and len(templist) > 0:
            text = trim(elem.text_content())
            if text not in myelems:
                myelems[text] = [elem]
            else:
                myelems[text].append(elem)
    # summing up
    if backtracking is True:
        for item in myelems:
            if 0 < len(item) < 100 and len(myelems[item]) >= 3:
                deletions.extend(myelems[item])
                #print('backtrack:', item)
            #elif 20 < len(item) < 100 and len(myelems[item]) >= 3:
            #    deletions.extend(myelems[item])
            #    print('backtrack 2:', item)
            #else: # and not re.search(r'[?!.]', text):
                #print(elem.tag, templist)
    for elem in list(OrderedDict.fromkeys(deletions)):
        elem.getparent().remove(elem)
    return subtree


def extract_content(tree, include_tables=False, include_images=False, include_links=False, deduplicate=False, config=None):
    '''Find the main content of a page using a set of XPath expressions,
       then extract relevant elements, strip them of unwanted subparts and
       convert them'''
    sure_thing = False
    result_body = etree.Element('body')
    potential_tags = set(TAG_CATALOG)  # + 'span'?
    if include_tables is True:
        potential_tags.add('table')
    if include_images is True:
        potential_tags.add('graphic')
    if include_links is True:
        potential_tags.add('ref')
    # iterate
    for expr in BODY_XPATH:
        # select tree if the expression has been found
        subtree = tree.xpath(expr)
        if not subtree:
            continue
        subtree = subtree[0]
        # prune
        subtree = discard_unwanted(subtree)
        # remove elements by link density
        subtree = delete_by_link_density(subtree, 'div', backtracking=True)
        subtree = delete_by_link_density(subtree, 'list', backtracking=False)
        subtree = delete_by_link_density(subtree, 'p', backtracking=False)
        # define iteration strategy
        if 'table' in potential_tags:
            for elem in subtree.iter('table'):
                if link_density_test_tables(elem) is True:
                    elem.getparent().remove(elem)
        # skip if empty tree
        if len(subtree) == 0:
            continue
        # no paragraphs containing text
        if not subtree.xpath('//p//text()'):
            potential_tags.add('div')
        if 'ref' in potential_tags:
            etree.strip_tags(subtree, 'span')
        else:
            etree.strip_tags(subtree, 'ref', 'span') # 'a',
        LOGGER.debug(sorted(potential_tags))
        # etree.strip_tags(subtree, 'lb') # BoingBoing-Bug
        # extract content
        # list(filter(None.__ne__, processed_elems))
        result_body.extend([e for e in
                            [handle_textelem(e, potential_tags, deduplicate, config) for e in subtree.xpath('.//*')]
                            if e is not None])
        # remove trailing titles
        while len(result_body) > 0 and result_body[-1].tag in ('fw', 'head'): # and result_body[-1].tail is None:
            result_body[-1].getparent().remove(result_body[-1])
        # exit the loop if the result has children
        if len(result_body) > 1: # try to change this to 0 or 2
            LOGGER.debug(expr)
            break
    temp_text = trim(' '.join(result_body.itertext()))
    # try parsing wild <p> elements if nothing found or text too short
    if len(result_body) == 0 or len(temp_text) < config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE'):
        result_body = recover_wild_text(tree, result_body, potential_tags=potential_tags, deduplicate=deduplicate, config=config)
        temp_text = trim(' '.join(result_body.itertext()))
    else:
        sure_thing = True
    # filter output
    etree.strip_elements(result_body, 'done')
    etree.strip_tags(result_body, 'div')
    # return
    return result_body, temp_text, len(temp_text), sure_thing


def process_comments_node(elem, potential_tags, dedupbool, config):
    '''Process comment node and determine how to deal with its content'''
    if elem.tag in potential_tags:
        # print(elem.tag, elem.text_content())
        processed_element = handle_textnode(elem, comments_fix=True, deduplicate=dedupbool, config=config)
        # test length and remove
        if processed_element is not None: # and processed_element.text not in COMMENTS_BLACKLIST:
            processed_element.attrib.clear()
            # if textfilter(elem) is True: # ^Pingback
            #    return None
            return processed_element
    return None


def extract_comments(tree, dedupbool, config):
    '''Try and extract comments out of potential sections in the HTML'''
    comments_body = etree.Element('body')
    # define iteration strategy
    potential_tags = set(TAG_CATALOG)  # 'span'
    # potential_tags.add('div') trouble with <div class="comment-author meta">
    for expr in COMMENTS_XPATH:
        # select tree if the expression has been found
        subtree = tree.xpath(expr)
        if not subtree:
            continue
        subtree = subtree[0]
        # prune
        subtree = discard_unwanted_comments(subtree)
        etree.strip_tags(subtree, 'a', 'ref', 'span')
        # extract content
        #for elem in subtree.xpath('.//*'):
        #    processed_elem = process_comments_node(elem, potential_tags)
        #    if processed_elem is not None:
        #        comments_body.append(processed_elem)
        processed_elems = [process_comments_node(elem, potential_tags, dedupbool, config) for elem in subtree.xpath('.//*')]
        comments_body.extend(list(filter(None.__ne__, processed_elems)))
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            subtree.getparent().remove(subtree)
            break
    # lengths
    temp_comments = trim(' '.join(comments_body.itertext()))
    return comments_body, temp_comments, len(temp_comments), tree


def compare_extraction(tree, backup_tree, url, body, text, len_text, target_language, include_formatting, include_links, include_images, config):
    '''Decide whether to choose own or external extraction
       based on a series of heuristics'''
    # bypass
    #if len_text > MIN_EXTRACTED_SIZE*10:
    #    return body, text, len_text
    # try with readability
    temppost_algo = try_readability(backup_tree, url)
    algo_text = trim(' '.join(temppost_algo.itertext()))
    len_algo = len(algo_text)
    # compare
    LOGGER.debug('extracted length: %s (algorithm) %s (extraction)', len_algo, len_text)
    # conditions to use alternative algorithms
    if len_algo in (0, len_text):
        algo_flag = False
    elif len_text == 0 and len_algo > 0:
        algo_flag = True
    elif len_text > 2*len_algo:
        algo_flag = False
    elif len_algo > 2*len_text:
        algo_flag = True
    elif not body.xpath('//p//text()') and len_algo > config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE'):
        algo_flag = True  # borderline case
    else:
        LOGGER.debug('extraction values: %s %s for %s', len_text, len_algo, url)
        algo_flag = False
    # apply decision
    if algo_flag is True:
        body, text, len_text = temppost_algo, algo_text, len_algo
        LOGGER.info('using generic algorithm: %s', url)
    else:
        LOGGER.info('using custom extraction: %s', url)
    # override faulty extraction # len_text < MIN_EXTRACTED_SIZE*10
    if body.xpath(SANITIZED_XPATH):
        body2, text2, len_text2, jt_result = justext_rescue(tree, url, target_language, body, 0, '')
        if jt_result is True: # and not len_text > 2*len_text2:
            LOGGER.debug('using justext, length: %s', len_text2)  #MIN_EXTRACTED_SIZE:
            body, text, len_text = body2, text2, len_text2
        else:
            # post-processing: remove unwanted sections
            body, text, len_text = sanitize_tree(body, include_formatting, include_links, include_images)
    # try with justext
    elif len_text < config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE'):
        LOGGER.error('not enough text %s', url)
        body, text, len_text, jt_result = justext_rescue(tree, url, target_language, body, len_text, text)
        LOGGER.debug('justext length %s', len_text)
        if jt_result is False:
            # post-processing: remove unwanted sections
            body, text, len_text = sanitize_tree(body, include_formatting, include_links, include_images)
    else:
        if algo_flag is True:
            body, text, len_text = sanitize_tree(body, include_formatting, include_links, include_images)
    # second backup
    #if len_text < MIN_EXTRACTED_SIZE:
    #     body2, temp_text2, len_text2 = baseline(backup_tree)
    #     if len_text2 > MIN_EXTRACTED_SIZE:
    #         body, text, len_text = body2, len_text2, temp_text2
    return body, text, len_text


def baseline(filecontent):
    """Use baseline extraction function targeting text paragraphs and/or JSON metadata.

    Args:
        filecontent: HTML code as binary string or string.

    Returns:
        A LXML <body> element containing the extracted paragraphs,
        the main text as string, and its length as integer.

    """

    tree = load_html(filecontent)
    postbody = etree.Element('body')
    if tree is None:
        return postbody, 0, ''
    # scrape from json text
    for elem in tree.iterfind('.//script[@type="application/ld+json"]'):
        if elem.text and '"article' in elem.text:
            mymatch = re.search(r'"articlebody":"(.+?)","', elem.text, re.I)
            if mymatch:
                postbody = etree.Element('body')
                elem = etree.Element('p')
                elem.text = trim(mymatch.group(1).replace('\\"', '"'))
                postbody.append(elem)
                return postbody, elem.text, len(elem.text)
    # scrape from article tag
    article_elem = tree.find('.//article') # |.//main
    if article_elem is not None:  # len(elems) > 0:
        temp_text = trim(article_elem.text_content())
        len_text = len(temp_text)
        if len_text > 0:
            elem = etree.Element('p')
            elem.text = temp_text
            postbody.append(elem)
            return postbody, temp_text, len_text
    # scrape from text paragraphs
    results = set()
    for element in tree.iter('blockquote', 'code', 'p', 'pre', 'q', 'quote'):
        entry = element.text_content()
        if entry not in results:
            elem = etree.Element('p')
            elem.text = entry
            postbody.append(elem)
            results.add(entry)
            # elem.getparent().remove(elem)
    temp_text = trim('\n'.join(postbody.itertext()))
    return postbody, temp_text, len(temp_text)


def determine_returnstring(docmeta, output_format, include_formatting, include_links, tei_validation):
    '''Convert XML tree to chosen format, clean the result and output it as a string'''
    # XML (TEI) steps
    if 'xml' in output_format:
        # last cleaning
        for element in docmeta['body'].iter():
            if element.tag != 'graphic' and len(element) == 0 and not element.text and not element.tail:
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
        # build output trees
        if output_format == 'xml':
            output = build_xml_output(docmeta)
        elif output_format == 'xmltei':
            output = build_tei_output(docmeta)
        # can be improved
        returnstring = control_xml_output(output, output_format, tei_validation, docmeta)
    # CSV, JSON and TXT output
    else:
        if output_format == 'csv':
            posttext = xmltotxt(docmeta['body'], include_formatting, include_links)
            if docmeta['commentsbody'] is not None:
                commentstext = xmltotxt(docmeta['commentsbody'], include_formatting, include_links)
            else:
                commentstext = ''
            returnstring = txttocsv(posttext, commentstext, docmeta)
        elif output_format == 'json':
            returnstring = build_json_output(docmeta)
        else:  # txt
            returnstring = xmltotxt(docmeta['body'], include_formatting, include_links)
            if docmeta['commentsbody'] is not None:
                returnstring += '\n' + xmltotxt(docmeta['commentsbody'], include_formatting, include_links)
                returnstring = returnstring.strip()
    return returnstring


def bare_extraction(filecontent, url=None, no_fallback=False,
                    include_comments=True, output_format='python', target_language=None,
                    include_tables=True, include_images=False, include_formatting=False,
                    include_links=False, deduplicate=False,
                    date_extraction_params=None, with_metadata=False, max_tree_size=None,
                    url_blacklist=None, config=DEFAULT_CONFIG):
    """Internal function for text extraction returning bare Python variables.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        no_fallback: Skip the backup extraction with readability-lxml and justext.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format, Python being the default
            and the interest of this internal function.
            Other values: 'txt', 'csv', 'json', 'xml', or 'xmltei'.
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (present in XML format, converted to markdown otherwise).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        max_tree_size: Discard documents with too many elements.
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        config: Directly provide a configparser configuration.

    Returns:
        A Python dict() containing all the extracted information or None.

    Raises:
        ValueError: Extraction problem.
    """
    # init
    if url_blacklist is None:
        url_blacklist = set()

    # load data
    try:
        tree = load_html(filecontent)
        if tree is None:
            raise ValueError

        # HTML lang check
        if target_language is not None and check_html_lang(tree, target_language) is False:
            raise ValueError

        # backup (or not) for further processing
        if no_fallback is False:
            backup_tree = deepcopy(tree)
        else:
            backup_tree = None

        # extract metadata if necessary
        if output_format != 'txt':
            docmeta = extract_metadata(tree, url, date_extraction_params)
            # cut short if extracted URL in blacklist
            if docmeta['url'] in url_blacklist:
                raise ValueError
            # cut short if core elements are missing
            if with_metadata is True and any(
                    x is None for x in
                    [docmeta['date'], docmeta['title'], docmeta['url']]
                ):
                raise ValueError
        else:
            docmeta = dict.fromkeys(METADATA_LIST)

        # clean + use LXML cleaner
        cleaned_tree = tree_cleaning(tree, include_tables, include_images)

        # convert tags, the rest does not work without conversion
        cleaned_tree = convert_tags(cleaned_tree, include_formatting, include_tables, include_images, include_links)

        # comments first, then remove
        if include_comments is True:
            commentsbody, temp_comments, len_comments, cleaned_tree = extract_comments(cleaned_tree, deduplicate, config)
        else:
            commentsbody, temp_comments, len_comments = None, '', 0

        # extract content
        postbody, temp_text, len_text, sure_thing = extract_content(cleaned_tree, include_tables, include_images, include_links, deduplicate, config)

        # compare if necessary
        if no_fallback is False:
            #if sure_thing is False:
            postbody, temp_text, len_text = compare_extraction(tree, backup_tree, url, postbody, temp_text, len_text, target_language, include_formatting, include_links, include_images, config)
        else:
            # rescue: try to use original/dirty tree
            if sure_thing is False and len_text < config.getint('DEFAULT', 'MIN_EXTRACTED_SIZE'):
                postbody, temp_text, len_text = baseline(filecontent)
                LOGGER.debug('non-clean extracted length: %s (extraction)', len_text)

        # tree size sanity check
        if max_tree_size is not None:
            if len(postbody) > max_tree_size:
                LOGGER.warning('output tree too long: %s', len(postbody))
                etree.strip_tags(postbody, 'hi')
                if len(postbody) > max_tree_size:
                    LOGGER.error('output tree too long: %s, discarding file', len(postbody))
                    raise ValueError
        # size checks
        if len_comments < config.getint('DEFAULT', 'MIN_EXTRACTED_COMM_SIZE'):
            LOGGER.info('not enough comments %s', url)
        if len_text < config.getint('DEFAULT', 'MIN_OUTPUT_SIZE') and \
           len_comments < config.getint('DEFAULT', 'MIN_OUTPUT_COMM_SIZE'):
            LOGGER.info('text and comments not long enough: %s %s', len_text, len_comments)
            raise ValueError

        # check duplicates at body level
        if deduplicate is True and duplicate_test(postbody, config) is True:
            raise ValueError

        # sanity check on language
        if target_language is not None and \
            language_filter(temp_text, temp_comments, target_language, docmeta) is True:
            raise ValueError

    except ValueError:
        LOGGER.info('discarding data for url: %s', url) # docmeta['url'] , record_id
        return None

    # special case: python variables
    if output_format == 'python':
        docmeta['text'] = xmltotxt(postbody, include_formatting, include_links)
        if include_comments is True:
            docmeta['comments'] = xmltotxt(commentsbody, include_formatting, include_links)
    else:
        docmeta['raw-text'], docmeta['body'], docmeta['commentsbody'] = temp_text, postbody, commentsbody
    return docmeta


def extract(filecontent, url=None, record_id=None, no_fallback=False,
            include_comments=True, output_format='txt',
            tei_validation=False, target_language=None,
            include_tables=True, include_images=False, include_formatting=False,
            include_links=False, deduplicate=False,
            date_extraction_params=None, with_metadata=False, max_tree_size=None, url_blacklist=None,
            settingsfile=None, config=DEFAULT_CONFIG):
    """Main function exposed by the package:
       Wrapper for text extraction and conversion to chosen output format.

    Args:
        filecontent: HTML code as string.
        url: URL of the webpage.
        record_id: Add an ID to the metadata.
        no_fallback: Skip the backup extraction with readability-lxml and justext.
        include_comments: Extract comments along with the main text.
        output_format: Define an output format:
            'txt', 'csv', 'json', 'xml', or 'xmltei'.
        tei_validation: Validate the XML-TEI output with respect to the TEI standard.
        target_language: Define a language to discard invalid documents (ISO 639-1 format).
        include_tables: Take into account information within the HTML <table> element.
        include_images: Take images into account (experimental).
        include_formatting: Keep structural elements related to formatting
            (only valuable if output_format is set to XML).
        include_links: Keep links along with their targets (experimental).
        deduplicate: Remove duplicate segments and documents.
        date_extraction_params: Provide extraction parameters to htmldate as dict().
        with_metadata: Only keep documents featuring all essential metadata
            (date, title, url).
        max_tree_size: Discard documents with too many elements.
        url_blacklist: Provide a blacklist of URLs as set() to filter out documents.
        settingsfile: Use a configuration file to override the standard settings.
        config: Directly provide a configparser configuration.

    Returns:
        A string in the desired format or None.

    """
    # configuration init
    config = use_config(settingsfile, config)
    if url_blacklist is None:
        url_blacklist = set()
    # extraction
    docmeta = bare_extraction(
        filecontent, url=url, no_fallback=no_fallback,
        include_comments=include_comments, output_format=output_format,
        target_language=target_language, include_tables=include_tables, include_images=include_images,
        include_formatting=include_formatting, include_links=include_links,
        deduplicate=deduplicate,
        date_extraction_params=date_extraction_params, with_metadata=with_metadata,
        max_tree_size=max_tree_size, url_blacklist=url_blacklist, config=config,
        )
    if docmeta is None:
        return None
    if output_format != 'txt':
        # add record ID to metadata
        docmeta['id'] = record_id
        # calculate fingerprint
        docmeta['fingerprint'] = content_fingerprint(docmeta['raw-text'])
    # return
    return determine_returnstring(docmeta, output_format, include_formatting, include_links, tei_validation)


# for legacy and backwards compatibility
process_record = extract
