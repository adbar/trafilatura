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
# third-party
import justext

try:
    import langid
    LANGID_FLAG = True
except ImportError:
    LANGID_FLAG = False
try:
    from htmldate import find_date
    DATE_FLAG = True
except ImportError:
    DATE_FLAG = False

from lxml import etree, html

# own
from .duplicates import duplicate_test, put_in_cache, test_body_cache
from .htmlprocess import (convert_tags, handle_textnode, manual_cleaning,
                          prune_html, recursively_empty, discard_unwanted,
                          discard_unwanted_comments)
from .settings import (HTML_CLEANER, LANGUAGES, MIN_EXTRACTED_SIZE,
                       MIN_EXTRACTED_COMM_SIZE, TAG_CATALOG)
from .utils import load_html, sanitize, trim, txttocsv
from .xml import check_tei, validate_tei, write_teitree, xmltotxt
from .xpaths import BODY_XPATH, COMMENTS_XPATH


if LANGID_FLAG is True:
    langid.set_languages(LANGUAGES)

LOGGER = logging.getLogger(__name__)

COMMENTS_BLACKLIST = ('( Abmelden / Ändern )')

# justext
JUSTEXT_STOPLIST = justext.get_stoplist('German')


def try_justext(tree, url):
    '''Safety net: try with the generic algorithm justext'''
    result_body = etree.Element('body')
    justtextstring = html.tostring(tree, pretty_print=False, encoding='utf-8')
    LOGGER.debug('raw length: %s (tostring) ', len(justtextstring))
    try:
        paragraphs = justext.justext(justtextstring, JUSTEXT_STOPLIST)
    except ValueError as err:  # not an XML element: HtmlComment
        LOGGER.error('justext %s %s', err, url)
        result_body = None
    else:
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                if duplicate_test(paragraph) is not True:
                    elem = etree.Element('p')
                    elem.text = paragraph.text
                    result_body.append(elem)
    return result_body


def handle_titles(element, result_body):
    '''Process head elements (titles)'''
    element.text = trim(element.text)
    if element.text and re.search(r'\w', element.text):
        result_body.append(element)
    # maybe needs attention
    if element.tail:
        LOGGER.debug('tail in title: %s', element.tail)
    return result_body


def handle_formatting(element, result_body):
    '''Process formatting elements (b, i, etc. converted to hi) found
       outside of paragraphs'''
    if element.text is not None or element.tail is not None:
        processed_element = etree.Element('p')
        processed_child = etree.SubElement(processed_element, element.tag)
        if element.text is not None:
            processed_child.text = trim(element.text)
        if element.tail is not None:
            processed_child.tail = trim(element.tail)
        result_body.append(processed_element)
    return result_body


def handle_lists(element, result_body):
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
            result_body.append(processed_element)
    return result_body


def handle_quotes(element, result_body):
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
            result_body.append(processed_element)
    return result_body


def handle_other_elements(element, result_body, potential_tags):
    '''Handle diverse or unknown elements in the scope of relevant tags'''
    # delete unwanted
    if element.tag not in potential_tags:
        # LOGGER.debug('discarding: %s %s', element.tag, element.text)
        return result_body
    if element.tag == 'div':
        LOGGER.warning('processing other element: %s', element.tag)
        processed_element = handle_textnode(element, comments_fix=False)
        if processed_element is not None:
            processed_element.attrib.clear()
            # small div-correction # could be moved elsewhere
            if processed_element.tag == 'div':
                processed_element.tag = 'p'
            # insert
            result_body.append(processed_element)
    else:
        LOGGER.debug('processing other element: %s %s', element.tag, element.text)
    return result_body


def handle_paragraphs(element, result_body, potential_tags):
    '''Process paragraphs (p) elements along with their children,
       trim and clean the content'''
    element.attrib.clear()
    # no children
    if len(element) == 0:
        processed_element = handle_textnode(element, comments_fix=False)
        if processed_element is not None:
            result_body.append(processed_element)
        return result_body
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
        result_body.append(processed_element)
    else:
        LOGGER.debug('discarding p-child: %s', html.tostring(processed_element))
    return result_body


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
    # prune
    search_tree = discard_unwanted(tree)
    # print(html.tostring(tree, pretty_print=False, encoding='unicode'))
    for element in search_tree.xpath('//p'):
        # print(element.tag, element.text)
        processed_element = handle_textnode(element, comments_fix=False)
        if processed_element is not None:
            processed_element.attrib.clear()
            processed_element.tail = ''
            result_body.append(processed_element)
    return result_body


def extract_content(tree, include_tables=False):
    '''Find the main content of a page using a set of XPath expressions,
       then extract relevant elements, strip them of unwanted subparts and
       convert them'''
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
        for element in subtree.xpath('.//*'):  # .iter() .getchildren()
            # bypass: nested elements
            if element.tag == 'list':
                result_body = handle_lists(element, result_body)
            elif element.tag == 'quote':   # + 'code'?
                result_body = handle_quotes(element, result_body)
            elif element.tag == 'head':
                result_body = handle_titles(element, result_body)
            elif element.tag == 'p':
                result_body = handle_paragraphs(element, result_body, potential_tags)
            elif element.tag == 'lb':
                if element.tail is not None and re.search(r'\w+', element.tail):
                    processed_element = etree.Element('p')
                    processed_element.text = handle_textnode(element, comments_fix=False).tail
                    result_body.append(processed_element)
            elif element.tag == 'hi':
                result_body = handle_formatting(element, result_body)
            else:
                # other elements (div, ??, ??)
                result_body = handle_other_elements(element, result_body, potential_tags)
        # exit the loop if the result has children
        if len(result_body) > 0:
            LOGGER.debug(expr)
            break
    # try parsing wild <p> elements if nothing found or text too short
    if len(result_body) == 0 or len(' '.join(result_body.itertext())) < 100:
        result_body = recover_wild_paragraphs(tree, result_body)
    # parse tables
    if include_tables is True:
        result_body = handle_tables(tree, result_body)
    # filter output
    etree.strip_elements(result_body, 'done')
    etree.strip_tags(result_body, 'div')
    # return
    return result_body


def extract_comments(tree, include_comments):
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
            if elem.tag in potential_tags:
                # print(elem.tag, elem.text_content())
                processed_element = handle_textnode(elem, comments_fix=True)
                # test length and remove
                if processed_element is None or processed_element.text in COMMENTS_BLACKLIST:
                    # elem.getparent().remove(elem)
                    continue
                # if textfilter(elem) is True: # ^Pingback
                #    continue
                elem.attrib.clear()
                comments_body.append(elem)
        # control
        if len(comments_body) > 0:  # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            subtree.getparent().remove(subtree)
            break
    if include_comments is False:
        comments_body = etree.Element('body')
    return comments_body, tree


def extract_metadata(tree):
    '''Extract title and document date if available/required'''
    try:
        doctitle = trim(tree.find('//title').text)  # h1?
    except AttributeError:  # no title found
        doctitle = None
    if DATE_FLAG is True:
        docdate = find_date(tree, extensive_search=False)
    else:
        docdate = None
    return doctitle, docdate


def compare_extraction(tree, url, temppost_hand, no_fallback):
    '''Decide whether to choose own or external (jusText) extraction
       based on a series of heuristics'''
    temp_text = ' '.join(temppost_hand.itertext())
    if no_fallback is False and 0 <= len(temp_text) < 1500:  # was 300
        # try with justext on cleaned_tree
        temppost_algo = try_justext(tree, url)
        # compare
        temp_jt = ' '.join(temppost_algo.itertext())
        LOGGER.info('extracted length: %s (jusText) %s (extraction)', len(temp_jt), len(temp_text))
        # conditions to use justext # was 300 and 2x
        if 0 <= len(temp_text) < 1500 and len(temp_jt) > 3*len(temp_text):
            justext_flag = True
        elif len(temppost_hand.xpath('//p')) == 0 and len(temp_jt) > 0:
            justext_flag = True  # borderline case
        else:
            justext_flag = False
        if justext_flag is True:  # was len(temp_text) > 10
            postbody = temppost_algo
            LOGGER.info('using justext: %s', url)
        else:
            postbody = temppost_hand
            LOGGER.info('using custom extraction: %s', url)
    else:
        LOGGER.info('extracted length: %s (extraction)', len(temp_text))
        postbody = temppost_hand
        temp_jt = ''
    return temp_text, temp_jt, postbody


def extract(filecontent, url=None, record_id='0001', no_fallback=False,
            include_comments=True, csv_output=False, xml_output=False,
            tei_output=False, tei_validation=False, target_language=None,
            include_tables=True, include_formatting=False):
    '''Main process for text extraction'''
    # init
    tree = load_html(filecontent)
    if tree is None:
        return None
    # print(html.tostring(tree, pretty_print=False, encoding='unicode'))

    # Metadata here
    if csv_output is True or xml_output is True or tei_output is True:
        doctitle, docdate = extract_metadata(tree)
    else:
        doctitle = docdate = None

    # clean
    cleaned_tree = manual_cleaning(tree, include_tables)
    # save space and processing time
    cleaned_tree = prune_html(cleaned_tree)
    # use LXML cleaner
    cleaned_tree = HTML_CLEANER.clean_html(cleaned_tree)
    # tree_cache[cleaned_tree] = list(cleaned_tree.iter())
    # bypass
    # cleaned_tree = tree
    # print(html.tostring(cleaned_tree, pretty_print=False, encoding='unicode'))

    # convert tags, the rest does not work without conversion
    cleaned_tree = convert_tags(cleaned_tree)
    # remove hi-element to avoid tail bug
    if (xml_output is False and tei_output is False) or include_formatting is False:
        etree.strip_tags(cleaned_tree, 'hi')

    # comments first, then remove
    commentsbody, cleaned_tree = extract_comments(cleaned_tree, include_comments)

    # extract content
    temppost_hand = extract_content(cleaned_tree, include_tables)

    # compare
    temp_text, temp_jt, postbody = compare_extraction(tree, url, temppost_hand, no_fallback)

    # try to use original/dirty tree
    if len(temp_text) == 0 and len(temp_jt) == 0:
        tree = convert_tags(tree)
        temppost_hand = extract_content(tree)
        temp_text = ' '.join(temppost_hand.itertext())
        LOGGER.debug('non-clean extracted length: %s (extraction)', len(temp_text))
        postbody = temppost_hand

    # sanity check on length
    temp_text = ' '.join(postbody.itertext())
    temp_comments = ' '.join(commentsbody.itertext())
    if len(temp_text) < MIN_EXTRACTED_SIZE:
        LOGGER.error('not enough text %s %s', record_id, url)
    if len(temp_comments) < MIN_EXTRACTED_COMM_SIZE:
        LOGGER.warning('not enough comments %s %s', record_id, url)
    if len(temp_text) < MIN_EXTRACTED_SIZE and len(temp_comments) < MIN_EXTRACTED_COMM_SIZE:
        LOGGER.info('text and comments not long enough: %s %s', len(temp_text), len(temp_comments))
        return None

    # sanity check on language
    if target_language is not None:
        if LANGID_FLAG is True:
            # comments
            if len(temp_comments) > len(temp_text):
                langtest = temp_comments
            # default
            else:
                langtest = temp_text
            langresult = langid.classify(langtest)
            if langresult[0] != target_language:
                LOGGER.warning('wrong language: %s %s %s', langresult, record_id, url)
                LOGGER.debug('wrong language: %s %s', langresult, temp_text)
                return None
        else:
            LOGGER.warning('langid not installed, no language detection run')

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
    if test_body_cache(postbody) is True:
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
