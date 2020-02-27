# pylint:disable-msg=E0611,I1101
"""
Module bundling all functions needed to extract the text in a webpage.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

# TODO:
# line-based heuristics?
# text blacklist

# standard
import logging
import re
from copy import deepcopy

# third-party
from lxml import etree, html
from readability import Document
from readability.readability import Unparseable

try:
    from htmldate import find_date
    DATE_FLAG = True
except ImportError:
    DATE_FLAG = False

# try this option
try:
    from inscriptis import get_text
except ImportError:
    pass


# own
from .filters import duplicate_test, language_filter, put_in_cache, COMMENTS_BLACKLIST
from .htmlprocessing import (convert_tags, handle_textnode, manual_cleaning,
                             prune_html, recursively_empty, discard_unwanted,
                             discard_unwanted_comments)
from .settings import (HTML_CLEANER, MIN_EXTRACTED_SIZE, MIN_EXTRACTED_COMM_SIZE,
                       MIN_OUTPUT_SIZE, MIN_OUTPUT_COMM_SIZE, TAG_CATALOG)
from .utils import load_html, sanitize, trim, txttocsv, HTML_PARSER
from .xml import check_tei, validate_tei, write_teitree, xmltotxt
from .xpaths import BODY_XPATH, COMMENTS_XPATH


LOGGER = logging.getLogger(__name__)


class LXMLDocument(Document):
    '''Sub-class of readability.Document accepting parsed trees as input'''
    def __init__(self, input_, *args, **kwargs):
        super().__init__(input_)

    def _parse(self, input_):
        return input_


def try_readability(htmlinput, url):
    '''Safety net: try with the generic algorithm readability'''
    # defaults: min_text_length=25, retry_length=250
    try:
        doc = LXMLDocument(htmlinput, url=url, min_text_length=25, retry_length=250)
        resultstring = doc.summary(html_partial=True)  # don't wrap in html and body tags
        newtree = html.fromstring(resultstring, parser=HTML_PARSER)
        return newtree
    except (etree.SerialisationError, Unparseable):
        return etree.Element('div')


def run_inscriptis(htmlstring):
    '''try with the inscriptis module'''
    text = get_text(htmlstring)
    return text


def sanitize_tree(tree):
    '''Sanitize the output from the generic algorithm'''
    # cleaned_tree = manual_cleaning(tree, True)
    # cleaned_tree = HTML_CLEANER.clean_html(cleaned_tree)
    etree.strip_tags(tree, 'div')
    cleaned_tree = convert_tags(tree)
    for elem in cleaned_tree:
        elem.attrib.clear()
        if elem.tag in ('del', 'head', 'hi', 'item', 'p', 'quote'):
            if elem.text is None or elem.text.isspace():
                elem.getparent().remove(elem)
    cleaned_tree = prune_html(cleaned_tree)
    return cleaned_tree


def handle_titles(element):
    '''Process head elements (titles)'''
    element.text = trim(element.text)
    # maybe needs attention
    if element.tail and re.search(r'\w', element.tail):
        LOGGER.debug('tail in title: %s', element.tail)
    if element.text and re.search(r'\w', element.text):
        return element
    return None


def handle_formatting(element):
    '''Process formatting elements (b, i, etc. converted to hi) found
       outside of paragraphs'''
    if element.text is not None or element.tail is not None:
        processed_element = etree.Element('p')
        processed_child = etree.SubElement(processed_element, element.tag)
        if element.text is not None:
            processed_child.text = trim(element.text)
        if element.tail is not None:
            processed_child.tail = trim(element.tail)
    return processed_element


def handle_lists(element):
    '''Process lists elements'''
    processed_element = etree.Element(element.tag)
    for child in element.iter():
        # list-specific check
        if child.tag not in ('dd', 'dt', 'li'):
            continue  # 'item'
        # proceed with iteration, fix for nested elements
        processed_child = handle_textnode(child, comments_fix=True)
        # add child element to processed_element
        if processed_child is not None:
            newsub = etree.SubElement(processed_element, 'item')
            newsub.text = processed_child.text
        child.tag = 'done'
    # avoid double tags??
    if len(processed_element) > 0:  # if it has children
        # test if it has text
        teststring = ''.join(processed_element.itertext())
        if len(teststring) > 0 and re.search(r'[a-z]', teststring):
            return processed_element
    return None


def handle_quotes(element):
    '''Process quotes elements'''
    processed_element = etree.Element(element.tag)
    for child in element.iter():
        processed_child = handle_textnode(child, comments_fix=True)
        if processed_child is not None:
            newsub = etree.SubElement(processed_element, child.tag)
            newsub.text = processed_child.text
            newsub.tail = processed_child.tail
        child.tag = 'done'
    if len(processed_element) > 0:
        # avoid double/nested tags
        etree.strip_tags(processed_element, 'quote')
        # test if it has text
        teststring = ''.join(processed_element.itertext())
        if len(teststring) > 0 and re.search(r'[a-z]', teststring):
            return processed_element
    return None


def handle_other_elements(element, potential_tags):
    '''Handle diverse or unknown elements in the scope of relevant tags'''
    # delete unwanted
    if element.tag not in potential_tags:
        # LOGGER.debug('discarding: %s %s', element.tag, element.text)
        return None
    if element.tag == 'div':
        processed_element = handle_textnode(element, comments_fix=False)
        if processed_element is not None:
            processed_element.attrib.clear()
            # small div-correction # could be moved elsewhere
            if processed_element.tag == 'div':
                processed_element.tag = 'p'
            # insert
            return processed_element
    else:
        LOGGER.debug('processing other element: %s %s', element.tag, element.text)
    return None


def handle_paragraphs(element, potential_tags):
    '''Process paragraphs (p) elements along with their children,
       trim and clean the content'''
    element.attrib.clear()
    # no children
    if len(element) == 0:
        processed_element = handle_textnode(element, comments_fix=False)
        if processed_element is not None:
            return processed_element
        return None
    # children
    processed_element = etree.Element(element.tag)
    processed_element.text = ''
    for child in element.iter():
        if child.tag in potential_tags:
            processed_child = handle_textnode(child, comments_fix=False)
            if processed_child is not None:
                newsub = etree.Element(child.tag)
                # handle formatting
                if child.tag == 'hi':
                    # check depth and clean
                    if len(child) > 0:
                        for item in child:  # children are lists
                            item.text = ' ' + item.text
                            etree.strip_tags(child, item.tag)
                    newsub.set('rend', child.get('rend'))
                # handle line breaks
                elif child.tag == 'lb':
                    processed_child.tail = handle_textnode(child, comments_fix=False).tail
                # needing attention!
                elif child.tag == 'p':
                    LOGGER.debug('extra elem within p: %s %s %s', child.tag, child.text, child.tail)
                    processed_element.text = ' ' + child.text
                    processed_element.text = trim(processed_element.text)
                    continue
                # prepare text
                if processed_child.text is None:
                    processed_child.text = ''
                # if there are already children
                if len(processed_element) > 0:
                    newsub.tail = processed_child.text + processed_child.tail
                else:
                    newsub.text = processed_child.text
                    newsub.tail = processed_child.tail
                processed_element.append(newsub)
                # print(html.tostring(processed_element))
            child.tag = 'done'
    # finish
    if len(processed_element) > 0 or len(processed_element.text) > 0:
        # clean trailing lb-elements
        if len(processed_element) > 0 and processed_element[-1].tag == 'lb' and processed_element[-1].tail is None:
            processed_element[-1].getparent().remove(processed_element[-1])
        return processed_element
    LOGGER.debug('discarding p-child: %s', html.tostring(processed_element))
    return None


def handle_tables(tree, result_body):
    '''Process table elements'''
    LOGGER.debug('Using table extraction')
    search_tree = discard_unwanted(tree)
    for table_elem in search_tree.xpath('//table'):
        # print(html.tostring(table_elem))
        # iterate through elements in table
        for subelement in table_elem.xpath('.//*'):
            # print(subelement.tag, subelement.text)
            subelement.attrib.clear()
            subelement.text = trim(subelement.text)
            if subelement.tag == 'tr':
                subelement.tag = 'row'
                rowtext = ' '.join(subelement.itertext())
                if rowtext is None: # or len(rowtext) < 50
                    subelement.getparent().remove(subelement)
                    continue
                # subelement.text = trim(rowtext)
            elif subelement.tag == 'th':
                subelement.tag = 'head' # 'cell'
            elif subelement.tag == 'td':
                subelement.tag = 'cell'
            # handle spaces?? # elif subelement.tag == 'lb':
            else:
                etree.strip_tags(table_elem, subelement.tag)
        # insert
        if len(' '.join(table_elem.itertext())) > MIN_EXTRACTED_SIZE:
            table_elem.attrib.clear()
            for element in table_elem.iter():
                if not re.search(r'[p{L}]+', ''.join(element.itertext())):
                    element.clear()
                    # element.getparent().remove(element)
            # prune recursively empty elements
            context = etree.iterwalk(table_elem)
            for _, elem in context:
                parent = elem.getparent()
                if recursively_empty(elem):
                    parent.remove(elem)
            result_body.append(table_elem)
    return result_body


def recover_wild_paragraphs(tree, result_body):
    '''Look for all p-elements, including outside of the determined frame
       and throughout the document to recover potentially missing text parts'''
    LOGGER.debug('Taking all p-elements')
    potential_tags = set(TAG_CATALOG)
    # prune
    search_tree = discard_unwanted(tree)
    for element in search_tree.iter('p'):
        # processed_element = handle_textnode(element, comments_fix=False)
        # if processed_element is not None:
        #    processed_element.attrib.clear()
        #    processed_element.tail = ''
        processed_element = handle_paragraphs(element, potential_tags)
        if processed_element is not None:
            result_body.append(processed_element)
    return result_body


def handle_textelem(element, potential_tags):
    '''Process text element and determine how to deal with its content'''
    new_element = None
    # bypass: nested elements
    if element.tag == 'list':
        new_element = handle_lists(element)
    elif element.tag == 'quote':   # + 'code'?
        new_element = handle_quotes(element)
    elif element.tag == 'head':
        new_element = handle_titles(element)
    elif element.tag == 'p':
        new_element = handle_paragraphs(element, potential_tags)
    elif element.tag == 'lb':
        if element.tail is not None and re.search(r'\w+', element.tail):
            processed_element = etree.Element('p')
            processed_element.text = handle_textnode(element, comments_fix=False).tail
            return processed_element
    elif element.tag == 'hi':
        new_element = handle_formatting(element)
    else:
        # other elements (div, ??, ??)
        new_element = handle_other_elements(element, potential_tags)
    return new_element


def extract_content(tree, include_tables=False):
    '''Find the main content of a page using a set of XPath expressions,
       then extract relevant elements, strip them of unwanted subparts and
       convert them'''
    sure_thing = False
    result_body = etree.Element('body')
    # iterate
    for expr in BODY_XPATH:
        # select tree if the expression has been found
        subtree = tree.xpath(expr)
        if len(subtree) == 0:
            continue
        subtree = subtree[0]
        # prune
        subtree = discard_unwanted(subtree)
        # etree.strip_tags(subtree, 'lb') # BoingBoing-Bug
        # print(html.tostring(subtree, pretty_print=True, encoding='unicode'))
        # define iteration strategy
        potential_tags = set(TAG_CATALOG)  # + 'span'?
        # no paragraphs containing text
        if len(subtree.xpath('//p//text()')) == 0:
            potential_tags.add('div')
        LOGGER.debug(sorted(potential_tags))
        # extract content
        for element in subtree.xpath('.//*'):
            processed_elem = handle_textelem(element, potential_tags)
            if processed_elem is not None:
                result_body.append(processed_elem)
        # exit the loop if the result has children
        if len(result_body) > 0:
            sure_thing = True
            LOGGER.debug(expr)
            break
    # try parsing wild <p> elements if nothing found or text too short
    if len(result_body) == 0 or len(' '.join(result_body.itertext())) < MIN_EXTRACTED_SIZE:
        result_body = recover_wild_paragraphs(tree, result_body)
    # parse tables
    if include_tables is True:
        result_body = handle_tables(tree, result_body)
    # filter output
    etree.strip_elements(result_body, 'done')
    etree.strip_tags(result_body, 'div')
    # return
    return result_body, sure_thing


def process_comments_node(elem, potential_tags):
    '''Process comment node and determine how to deal with its content'''
    if elem.tag in potential_tags:
        # print(elem.tag, elem.text_content())
        processed_element = handle_textnode(elem, comments_fix=True)
        # test length and remove
        if processed_element is not None and processed_element.text not in COMMENTS_BLACKLIST:
            processed_element.attrib.clear()
            # if textfilter(elem) is True: # ^Pingback
            #    return None
            return processed_element
    return None


def extract_comments(tree):
    '''Try and extract comments out of potential sections in the HTML'''
    comments_body = etree.Element('body')
    # define iteration strategy
    potential_tags = set(TAG_CATALOG)  # 'span'
    # potential_tags.add('div') trouble with <div class="comment-author meta">
    for expr in COMMENTS_XPATH:
        # select tree if the expression has been found
        subtree = tree.xpath(expr)
        if len(subtree) == 0:
            continue
        subtree = subtree[0]
        # prune
        subtree = discard_unwanted_comments(subtree)
        # extract content
        for elem in subtree.xpath('.//*'):
            processed_elem = process_comments_node(elem, potential_tags)
            if processed_elem is not None:
                comments_body.append(processed_elem)
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            subtree.getparent().remove(subtree)
            break
    return comments_body, tree


def extract_metadata(tree):
    '''Extract title and document date if available/required'''
    try:
        doctitle = trim(tree.find('//title').text)  # h1?
    except (AttributeError, SyntaxError):  # no title found
        doctitle = None
    if DATE_FLAG is True:
        docdate = find_date(tree, extensive_search=False)
    else:
        docdate = None
    return doctitle, docdate


def compare_extraction(tree, url, temppost_hand, sure_thing, no_fallback):
    '''Decide whether to choose own or external extraction
       based on a series of heuristics'''
    temp_text = trim(' '.join(temppost_hand.itertext()))
    len_text = len(temp_text)
    # algo_flag = False
    # readability_flag = False
    if no_fallback is False or sure_thing is False:
        # try with readability
        temppost_algo = try_readability(tree, url)
        len_algo = len(trim(' '.join(temppost_algo.itertext())))
        # compare
        LOGGER.info('extracted length: %s (algorithm) %s (extraction)', len_algo, len_text)
        # conditions to use alternative algorithms
        if len_algo == 0 or len_algo == len_text:
            algo_flag = False
        elif len_text == 0 and len_algo > 0:
            algo_flag = True
        elif len_text > 2*len_algo:
            algo_flag = False
        elif len_algo > 2*len_text:
            algo_flag = True
        #elif len_text >= 500 and 0.9*len_text < len_algo < len_text:
        #    algo_flag = True
        elif len(temppost_hand.xpath('//p')) == 0 and len_algo > 0:
            algo_flag = True  # borderline case
        else:
            # print(sure_thing, len_text, len_algo)
            LOGGER.debug('extraction values: %s %s for %s', len_text, len_algo, url)
            algo_flag = False
        # apply decision
        if algo_flag is True:
            postbody = sanitize_tree(temppost_algo)
            LOGGER.info('using generic algorithm: %s', url)
        else:
            postbody = temppost_hand
            LOGGER.info('using custom extraction: %s', url)
    else:
        LOGGER.info('extracted length: %s (extraction)', len_text)
        postbody = temppost_hand
        len_algo = 0
    return len_text, len_algo, postbody


def extract(filecontent, url=None, record_id='0001', no_fallback=False,
            txt_fallback=False, include_comments=True, csv_output=False, xml_output=False,
            tei_output=False, tei_validation=False, target_language=None,
            include_tables=True, include_formatting=False):
    '''Main process for text extraction'''
    # init
    tree = load_html(filecontent)
    if tree is None:
        return None

    # Metadata here
    if csv_output is True or xml_output is True or tei_output is True:
        doctitle, docdate = extract_metadata(tree)
    else:
        doctitle = docdate = None

    # backup (or not) for further processing
    if no_fallback is True:
        backup_tree = None
    else:
        backup_tree = deepcopy(tree)

    # clean
    cleaned_tree = manual_cleaning(tree, include_tables)
    # save space and processing time
    cleaned_tree = prune_html(cleaned_tree)
    # use LXML cleaner
    cleaned_tree = HTML_CLEANER.clean_html(cleaned_tree)
    # tree_cache[cleaned_tree] = list(cleaned_tree.iter())

    # convert tags, the rest does not work without conversion
    cleaned_tree = convert_tags(cleaned_tree)
    # remove hi-element to avoid tail bug
    if (xml_output is False and tei_output is False) or include_formatting is False:
        etree.strip_tags(cleaned_tree, 'hi')

    # comments first, then remove
    if include_comments is True:
        commentsbody, cleaned_tree = extract_comments(cleaned_tree)
    else:
        commentsbody = etree.Element('body')

    # extract content
    temppost_hand, sure_thing = extract_content(cleaned_tree, include_tables)

    # compare
    len_text, len_algo, postbody = compare_extraction(backup_tree, url, temppost_hand, sure_thing, no_fallback)

    # try to use original/dirty tree
    if len_text == 0 and len_algo == 0:
        tree = convert_tags(tree)
        temppost_hand, sure_thing = extract_content(tree)
        temp_text = ' '.join(temppost_hand.itertext())
        LOGGER.debug('non-clean extracted length: %s (extraction)', len(temp_text))
        postbody = temppost_hand

    # sanity check on length
    temp_text = ' '.join(postbody.itertext())  # trim()?
    temp_comments = ' '.join(commentsbody.itertext())  # trim()?
    if len(temp_text) < MIN_EXTRACTED_SIZE:
        LOGGER.error('not enough text %s %s', record_id, url)
    if len(temp_comments) < MIN_EXTRACTED_COMM_SIZE:
        LOGGER.info('not enough comments %s %s', record_id, url)
    if len(temp_text) < MIN_OUTPUT_SIZE and len(temp_comments) < MIN_OUTPUT_COMM_SIZE:
        LOGGER.info('text and comments not long enough: %s %s', len(temp_text), len(temp_comments))
        if txt_fallback is False or get_text is None:
            return None
        # additional fallback
        rawtext = run_inscriptis(filecontent)
        if len(rawtext) < MIN_OUTPUT_SIZE:
            return None
        postbody = etree.Element('p')
        postbody.text = rawtext
        temp_text = ' '.join(postbody.itertext())  # trim()?

    # sanity check on language
    if language_filter(temp_text, temp_comments, target_language, record_id, url) is True:
        return None

    # cache elements
    put_in_cache(postbody)
    put_in_cache(commentsbody)
    # del tree_cache[cleaned_tree]

    # XML (TEI) steps
    if include_comments is False:
        commentsbody = None
    if tei_output is True:
        # build TEI tree
        output = write_teitree(postbody, commentsbody, url, doctitle, docdate)
        # filter output (strip unwanted elements), just in case
        # check and repair
        output = check_tei(output, url)
        # validate
        # why is it necessary?
        testtree = etree.fromstring(etree.tostring(output))
        if tei_validation is True:
            result = validate_tei(testtree)
            LOGGER.info('TEI validation result: %s %s %s', result, record_id, url)
    else:
        output = etree.Element('doc')
        postbody.tag = 'main'
        output.append(postbody)
        if commentsbody is not None:
            commentsbody.tag = 'comments'
            output.append(commentsbody)
        # url in xml
        if url is not None:
            output.set('source', url)
        if doctitle is not None:
            output.set('title', doctitle)
        if docdate is not None:
            output.set('date', docdate)

    # check duplicates at body level
    if duplicate_test(postbody) is True:
        return None

    if xml_output is False and tei_output is False:
        if csv_output is False:
            returnstring = xmltotxt(output)
        else:
            posttext = xmltotxt(postbody)
            commentstext = xmltotxt(commentsbody)
            returnstring = txttocsv(posttext, commentstext, url, doctitle, docdate)
    else:
        # can be improved
        control_string = etree.tostring(output, encoding='unicode')
        control_string = sanitize(control_string)
        # necessary for cleaning
        control_parser = etree.XMLParser(remove_blank_text=True)
        output_tree = etree.fromstring(control_string, control_parser)
        returnstring = etree.tostring(output_tree, pretty_print=True, encoding='unicode')

    return returnstring


# for legacy and backwards compatibility
process_record = extract
