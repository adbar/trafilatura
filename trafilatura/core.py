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
from .lru import LRUCache
from .settings import (CUT_EMPTY_ELEMS, HTML_CLEANER, LANGUAGES, LRU_SIZE,
                       MANUALLY_CLEANED, MIN_DUPLCHECK_SIZE, MIN_EXTRACTED_SIZE,
                       MIN_EXTRACTED_COMM_SIZE, TAG_CATALOG)
from .utils import load_html, sanitize, textfilter, trim, txttocsv
from .xml import check_tei, validate_tei, write_teitree, xmltotxt
from .xpaths import BODY_XPATH, COMMENTS_XPATH, COMMENTS_DISCARD_XPATH, DISCARD_XPATH


if LANGID_FLAG is True:
    langid.set_languages(LANGUAGES)

LRU_TEST = LRUCache(maxsize=LRU_SIZE)

LOGGER = logging.getLogger(__name__)

COMMENTS_BLACKLIST = ('( Abmelden / Ändern )')

# justext
JUSTEXT_STOPLIST = justext.get_stoplist('German')


def manual_cleaning(tree, include_tables):
    '''Prune the tree by discarding unwanted elements'''
    if include_tables is False:
        MANUALLY_CLEANED.append('table')
    for expression in MANUALLY_CLEANED:
        for element in tree.iter(expression):
            element.getparent().remove(element)
    #for expression in ['a', 'abbr', 'acronym', 'address', 'big', 'cite', 'font', 'ins', 'meta', 'small', 'sub', 'sup', 'wbr']:
    #    for element in tree.getiterator(expression):
    #        element.drop_tag()
    return tree


def prune_html(tree):
    '''delete empty elements'''
    # empty tags
    for element in tree.xpath(".//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            element.getparent().remove(element)
    # for expression in CUT_EMPTY_ELEMS:
    #    for element in tree.getiterator(expression):
    #        if recursively_empty(element):
    #            element.getparent().remove(element)
    return tree


def recursively_empty(elem):
    '''return recursively empty elements'''
    # https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
    if elem.text:
        return False
    return all((recursively_empty(c) for c in elem.iterchildren()))


def discard_unwanted(tree):
    '''delete unwanted sections'''
    for expr in DISCARD_XPATH:
        for subtree in tree.xpath(expr):
            subtree.getparent().remove(subtree)
    return tree


def discard_unwanted_comments(tree):
    '''delete unwanted comment sections'''
    for expr in COMMENTS_DISCARD_XPATH:
        for subtree in tree.xpath(expr):
            subtree.getparent().remove(subtree)
    return tree


def cache(body):
    '''Implement LRU cache'''
    global LRU_TEST
    for element in body:
        try:
            teststring = ' '.join(element.itertext())
        except AttributeError:  # justext Paragraph
            teststring = element.text
        if teststring in LRU_TEST.cache:
            val = LRU_TEST.get(teststring)
            # print(val, teststring[:10] + '...')
            LRU_TEST.put(teststring, val + 1)
        else:
            # print(0, teststring[:10] + '...')
            LRU_TEST.put(teststring, 1)


def duplicate_test(element):
    '''Check for duplicate text'''
    global LRU_TEST
    try:
        teststring = ' '.join(element.itertext())
    except AttributeError:  # justext Paragraph
        teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        # key in self.cache
        if LRU_TEST.has_key(teststring) is True and LRU_TEST.get(teststring) > 2:
            # LRU_TEST[teststring] += 1
            return True
    return False


def convert_tags(tree):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # strip tags
    etree.strip_tags(tree, 'a', 'abbr', 'acronym', 'address', 'big', 'cite', 'font', 'ins', 'meta', 'span', 'small', 'wbr')
    # 'dd', 'sub', 'sup',
    # head tags + delete attributes
    for elem in tree.iter('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        # print(elem.tag, elem.text_content())
        # etree.strip_tags(elem, 'span')
        elem.tag = 'head'
        # elem.set('rendition', '#i')
    # br → lb
    for elem in tree.iter('br', 'hr'): # tree.xpath('//[br or hr]'): ## hr → //lb/line ?
        elem.tag = 'lb'
        elem.attrib.clear()
    # ul/ol → list / li → item
    for elem in tree.iter('ul', 'ol', 'dl'):
        elem.tag = 'list'
        elem.attrib.clear()
    # blockquote | q → quote
    for elem in tree.iter('blockquote', 'pre', 'q'):
        elem.tag = 'quote'
        elem.attrib.clear()
    # change rendition #i
    for elem in tree.iter('em', 'i'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#i')
    # change rendition #b
    for elem in tree.iter('b', 'strong'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#b')
    # change rendition #u (very rare)
    for elem in tree.iter('u'):
        elem.tag = 'hi'
        elem.set('rendition', '#u')
    # change rendition #pre and #t (very rare)
    for elem in tree.iter('tt'):  # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#t')
    # change rendition sub and sup (very rare)
    for elem in tree.iter('sub'):  # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#sub')
    for elem in tree.iter('sup'):  # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#sup')
    # del | s | strike → <del rend="overstrike">
    for elem in tree.iter('del', 's', 'strike'):
        elem.attrib.clear()
        elem.tag = 'del'
        elem.set('rendition', 'overstrike')
    return tree


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


def handle_textnode(element, comments_fix=True):
    '''Convert, format, and probe potential text elements'''
    if element.text is None and element.tail is None:
        return None
    # lb bypass
    if comments_fix is False and element.tag == 'lb':
        element.tail = trim(element.tail)
        # if textfilter(element) is True:
        #     return None
        # duplicate_test(subelement)?
        return element
    if element.tag in ('dl', 'head', 'ol', 'ul'):
        element.attrib.clear()
    if element.text is None:
        # try the tail
        # LOGGER.debug('using tail for element %s', element.tag)
        element.text = element.tail
        element.tail = ''
        # handle differently for br/lb
        if comments_fix is True and element.tag == 'lb':
            element.tag = 'p'
    # trim
    element.text = trim(element.text)
    if element.tail:
        element.tail = trim(element.tail)
    if element.text and re.search(r'\w', element.text):  # text_content()?
        if textfilter(element) is True:
            return None
        # TODO: improve duplicate detection
        if duplicate_test(element) is True:
            return None
    else:
        return None
    return element


def extract_content(tree, include_tables=False):
    '''Find and extract the main content of a page using a set of expressions'''
    #tree_cache = dict()
    #tree_cache[tree] = list(tree.iter())
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
            if element.tag in ('list', 'quote'):  # + 'code'?
                processed_element = etree.Element(element.tag)
                for child in element.iter():
                    # list-specific check
                    if element.tag == 'list' and child.tag not in ('dd', 'dt', 'li'):
                        continue  # 'item'
                    # proceed with iteration, fix for nested elements
                    processed_child = handle_textnode(child, comments_fix=True)
                    # add child element to processed_element
                    if processed_child is not None:
                        if element.tag == 'list':
                            newsub = etree.SubElement(processed_element, 'item')
                        else:
                            newsub = etree.SubElement(processed_element, child.tag)
                        newsub.text = processed_child.text
                        if element.tag == 'quote':
                            newsub.tail = processed_child.tail
                    child.tag = 'done'
                # avoid double tags??
                if len(processed_element) > 0: # if it has children
                    #teststring = ''.join(processed_element.itertext())
                    #if len(teststring) > 0 and re.search(r'[a-z]', teststring): # if it has text
                    # correct nested elements
                    if processed_element.tag == 'quote':
                        etree.strip_tags(processed_element, 'quote')
                        # processed_element.tag == 'quote' #superfluous?
                    result_body.append(processed_element)
            # bypass: head:
            elif element.tag == 'head':
                element.text = trim(element.text)
                if element.text and re.search(r'\w', element.text):
                    element.attrib.clear()
                    result_body.append(element)
            # strip attrs after discard is run
            elif element.tag == 'p':
                element.attrib.clear()
                # no children
                if len(element) == 0:
                    processed_element = handle_textnode(element, comments_fix=False)
                    if processed_element is not None:
                        result_body.append(processed_element)
                    continue
                # children
                processed_element = etree.Element(element.tag)
                processed_element.text = ''
                for child in element.iter():
                    if child.tag in potential_tags:
                        processed_child = handle_textnode(child, comments_fix=False)
                        if processed_child is not None:
                            newsub = etree.Element(child.tag)
                            # paragraph, append text
                            #if child.tag == 'p':
                                # if there are already children
                            #    if len(processed_element) > 0:
                            #        newsub.tail = processed_child.text + processed_child.tail
                            #    else:
                            #        newsub.text = processed_child.text
                            #        newsub.tail = processed_child.tail
                            # handle hi
                            if child.tag == 'hi':
                                # check depth and clean
                                if len(child) > 0:
                                    for item in child: # children are lists
                                        item.text = ' ' + item.text
                                        etree.strip_tags(child, item.tag)
                                newsub.set('rendition', child.get('rendition'))
                            # handle spaces
                            elif child.tag == 'lb':
                                # delete if empty paragraph so far
                                #if len(processed_element.text) < 1:
                                #    if child.tail is not None and re.search(r'\w+', child.tail):
                                #        processed_child.text = child.tail
                                    # child.tag = 'done'
                                #else:
                                #    if child.tail is not None and re.search(r'\w+', child.tail):
                                #        processed_child.tail = handle_subelement(child).tail
                                processed_child.tail = handle_textnode(child, comments_fix=False).tail
                            else:
                                if child.tag == 'p':
                                    LOGGER.debug('extra elem within p: %s %s %s', child.tag, child.text, child.tail)
                            # prepare text
                            if processed_child.text is None:
                                processed_child.text = ''
                            if processed_child.tail is None:
                                processed_child.tail = ''
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
            # insert it directly
            elif element.tag == 'lb':
                if element.tail is not None and re.search(r'\w+', element.tail):
                    processed_element = etree.Element('p')
                    processed_element.text = handle_textnode(element, comments_fix=False).tail
                    result_body.append(processed_element)
            # insert it directly
            elif element.tag == 'hi':
                if element.text is not None or element.tail is not None:
                    processed_element = etree.Element('p')
                    processed_child = etree.SubElement(processed_element, element.tag)
                    if element.text is not None:
                        processed_child.text = trim(element.text)
                    if element.tail is not None:
                        processed_child.tail = trim(element.tail)
                    result_body.append(processed_element)
            # other elements (div, ??, ??)
            else:
                ## delete unwanted
                if element.tag not in potential_tags:
                    # LOGGER.debug('discarding: %s %s', element.tag, element.text)
                    continue
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
                elif element.tag != 'div' and element.tag in potential_tags:
                    LOGGER.debug('processing other element: %s %s', element.tag, element.text)
        # control
        if len(result_body) > 0: # if it has children
            LOGGER.debug(expr)
            break

    # try parsing wild <p> elements
    # no children if text too short
    if len(result_body) == 0 or len(' '.join(result_body.itertext())) < 100: # MIN_EXTRACTED_SIZE:
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

    # try parsing tables
    # if len(result_body) == 0: # no children
    # for _, element in etree.iterparse(xml_file, tag='a'):
    if include_tables is True:
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
        doctitle = trim(tree.find('//title').text) # h1?
    except AttributeError: # no title found
        doctitle = None
    if DATE_FLAG is True:
        docdate = find_date(tree, extensive_search=False)
    else:
        docdate = None
    return doctitle, docdate


def compare_extraction(tree, url, temppost_hand, no_fallback):
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
    global LRU_TEST
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
    cache(postbody)
    cache(commentsbody)
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
    teststring = ' '.join(postbody.itertext()).encode('utf-8')
    if LRU_TEST.has_key(teststring) is True:  # key in self.cache
        # LRU_TEST[teststring] = 1
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
