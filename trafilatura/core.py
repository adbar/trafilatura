# -*- coding: utf-8 -*-
# pylint:disable-msg=E0611,I1101
"""
Module bundling all functions needed to extract the text in a webpage.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

# standard
import logging
import re # import regex as re

from io import BytesIO

# third-party
import justext # from justext import classify_paragraphs, get_stoplist, revise_paragraph_classification
import langid

from lru import LRU # https://github.com/amitdev/lru-dict # pip3 install lru-dict
from lxml import etree, html
from lxml.html.clean import Cleaner

# own
from .settings import LANGUAGES, LRU_SIZE, MIN_EXTRACTED_SIZE, MIN_EXTRACTED_COMM_SIZE, MIN_DUPLCHECK_SIZE
from .utils import load_html, sanitize, trim
from .xpaths import BODY_XPATH, COMMENTS_XPATH, DISCARD_XPATH, COMMENTS_DISCARD_XPATH

langid.set_languages(LANGUAGES)

## TODO:
# add sqlite3 for control of seen URLs?
# line-based heuristics?
# check max depth recursion in output XML?


## INIT
LOGGER = logging.getLogger(__name__)

TAG_CATALOG = frozenset(['code', 'del', 'head', 'hi', 'lb', 'list', 'p', 'quote']) # 'span', 'item'

CUT_EMPTY_ELEMS = ('div', 'p', 'section')

comments_blacklist = ('( Abmelden / Ändern )')

# LRU_DICT = defaultdict(int)

# HTML_CLEANER config # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
HTML_CLEANER = Cleaner()
HTML_CLEANER.annoying_tags = True
HTML_CLEANER.comments = True
HTML_CLEANER.embedded = True
HTML_CLEANER.forms = True
HTML_CLEANER.frames = True
HTML_CLEANER.javascript = True
HTML_CLEANER.links = False
HTML_CLEANER.meta = False
HTML_CLEANER.page_structure = False
HTML_CLEANER.processing_instructions = True
HTML_CLEANER.remove_unknown_tags = False
HTML_CLEANER.safe_attrs_only = False
HTML_CLEANER.scripts = True
HTML_CLEANER.style = False
HTML_CLEANER.remove_tags = ['a', 'abbr', 'acronym', 'address', 'big', 'cite', 'font', 'ins', 'meta', 'small', 'sub', 'sup', 'wbr'] #  'center', 'table', 'tbody', 'td', 'th', 'tr', 'span',
HTML_CLEANER.kill_tags = ['aside', 'audio', 'canvas', 'embed', 'figure', 'footer', 'form', 'head', 'iframe', 'img', 'label', 'link', 'map', 'math', 'nav', 'noscript', 'object', 'picture', 'style', 'svg', 'time', 'video'] # 'area', 'table' # 'header'

# validation
TEI_VALID_TAGS = set(['code', 'del', 'div', 'head', 'hi', 'item', 'lb', 'list', 'p', 'quote'])
TEI_VALID_ATTRS = set(['rendition'])

# counters
tokens_posts = 0
tokens_comments = 0
LRU_TEST = LRU(LRU_SIZE)

# justext
JUSTEXT_STOPLIST = justext.get_stoplist('German')



def prune_html(tree):
    '''delete empty elements'''
    # empty tags
    for element in tree.xpath(".//*[not(node())]"):
        if element.tag in CUT_EMPTY_ELEMS:
            element.getparent().remove(element)
    return tree


def recursively_empty(e):
    '''return recursively empty elements'''
    # https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
    if e.text:
        return False
    return all((recursively_empty(c) for c in e.iterchildren()))


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


def textfilter(element):
    '''Filter out unwanted text'''
    ## TODO: text_blacklist
    # print('#', element.text)
    for line in element.text.splitlines():
        if len(line) < 5:
            continue
        # print('###', line)
        if re.match(r'Gef.llt mir|.hnliche Beitr|[Ss]hare (on|via)|Fill in your details below|Trage deine Daten unten|Kommentar verfassen|Bitte logge dich|Hinterlasse einen Kommentar|Connecting to %s|Verbinde mit %s|Facebook$|Twitter$|Google$|E-Mail$|Drucken$|LinkedIn$', line):
            return True
        if re.search(r'Tags: [A-ZÄÖÜßa-zäöü ,]+', line):
            return True
    # elemtext = trim(elemtext)
    #return elemtext
    return False


def cache(body):
    '''Implement LRU cache'''
    global LRU_TEST
    for element in body:
        # teststring = ' '.join(element.itertext()).encode('utf-8')
        teststring = element.text
        if LRU_TEST.has_key(teststring) is True:
            LRU_TEST[teststring] += 1
        else:
            LRU_TEST[teststring] = 1


def duplicate_test(element, justext_switch=False):
    '''Check for duplicate text'''
    global LRU_TEST
    # teststring = ' '.join(element.itertext()).encode('utf-8')
    if justext_switch is False:
        teststring = element.text_content()
    else:
        teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        if LRU_TEST.has_key(teststring) is True and LRU_TEST[teststring] > 2:
            # LRU_TEST[teststring] += 1
            return True
    return False


def convert_tags(tree):
    '''Simplify markup and convert relevant HTML tags to an XML standard'''
    # head tags + delete attributes
    for elem in tree.xpath('//h1|//h2|//h3|//h4|//h5|//h6'):
        elem.tag = 'head'
        elem.attrib.clear()
        # elem.set('rendition', '#i')
    # br → lb
    for elem in tree.xpath('//br|//hr'): # tree.xpath('//[br or hr]'): ## hr → //lb/line ?
        elem.tag = 'lb'
        elem.attrib.clear()
    # ul/ol → list / li → item
    for elem in tree.xpath('//ul|//ol|//dl'):
        elem.tag = 'list'
        elem.attrib.clear()
    # blockquote | q → quote
    for elem in tree.xpath('//blockquote|//pre|//q'):
        elem.tag = 'quote'
        elem.attrib.clear()
    # change rendition #i
    for elem in tree.xpath('//em|//i'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#i')
    # change rendition #b
    for elem in tree.xpath('//b|//strong'):
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#b')
    # change rendition #u (very rare)
    for elem in tree.xpath('//u'):
        elem.tag = 'hi'
        elem.set('rendition', '#u')
    # change rendition #pre and #t (very rare)
    for elem in tree.xpath('//tt'): # //pre| //code
        elem.attrib.clear()
        elem.tag = 'hi'
        elem.set('rendition', '#t')
    # del | s | strike → <del rend="overstrike">
    for elem in tree.xpath('//del|//s|//strike'):
        elem.attrib.clear()
        elem.tag = 'del'
        elem.set('rendition', 'overstrike')
    # add space
    for elem in tree.xpath('//span'): # //a|
        if elem.text is None:
            elem.text = ' '
        else:
            elem.text = elem.text + ' '
    # strip tags
    etree.strip_tags(tree, 'dd', 'span')
    return tree


def try_justext(tree, filecontent, record_id):
    '''safety net: try with justext'''
    result_body = etree.Element('body')
    justtextstring = html.tostring(tree, pretty_print=False, encoding='unicode')
    LOGGER.info('raw length: %s (file) %s (tostring) ', len(filecontent), len(justtextstring))
    try:
        # paragraphs = custom_justext(tree)
        paragraphs = justext.justext(justtextstring, JUSTEXT_STOPLIST)
    except ValueError as err: # ValueError: Input object is not an XML element: HtmlComment
        LOGGER.error('justext %s %s', err, record_id)
        return None
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            # if LRU_TEST.has_key(paragraph.text) is False or LRU_TEST[paragraph.text] <= 2:
            if duplicate_test(paragraph, justext_switch=True) is not True:
                elem = etree.Element('p')
                elem.text = paragraph.text
                result_body.append(elem)
            # jt += paragraph.text + '</p><p>'
    # jt += '</p>'
    # temp_jt = u' '.join(jt.itertext())
    # temp_jt = jt
    return result_body


#def custom_justext(htmldom):
#    paragraphs = ParagraphMaker.make_paragraphs(htmldom)
#    justext.classify_paragraphs(paragraphs, justext.get_stoplist("German"), length_low=LENGTH_LOW_DEFAULT, \
#        length_high=LENGTH_HIGH_DEFAULT, stopwords_low=STOPWORDS_LOW_DEFAULT, \
#        stopwords_high=STOPWORDS_HIGH_DEFAULT, max_link_density=MAX_LINK_DENSITY_DEFAULT, no_headings=NO_HEADINGS_DEFAULT)
#    justext.revise_paragraph_classification(paragraphs, max_heading_distance=MAX_HEADING_DISTANCE_DEFAULT)
#    return paragraphs


# @profile
def handle_textnode(element, comments_fix=True):
    '''Convert, format, and probe potential text elements'''
    if element.text is None: # or len(element.text) < 10 # text_content()
        # try the tail
        if element.tail is None or len(element.tail) < 2: # was 50
            #element.getparent().remove(element)
            #continue
            return None
        # if element.tag == 'lb':
        # LOGGER.debug('using tail for element %s', element.tag)
        # TODO: handle differently for br/lb
        element.text = element.tail
        element.tail = ''
        if comments_fix is True and element.tag == 'lb':
            element.tag = 'p'
    # delete newlines that are not related to punctuation or markup
    element.text = re.sub(r'(?<![p{P}>])\n', ' ', element.text)
    # trim
    element.text = trim(element.text) # + '\n'
    if element.tail:
        element.tail = trim(element.tail) # + '\n'
    ## LOGGER.debug(element.tag, element.text)
    if textfilter(element) is True:
        return None
    if element.text and re.search(r'\w', element.text): # text_content()
        ## TODO: improve duplicate detection
        if duplicate_test(element) is True:
            return None
    else:
        return None
    return element


# @profile
def handle_subelement(subelement):
    '''Convert, format, and probe potential text subelements'''
    if subelement.tail is None:
        return subelement
    # delete newlines that are not related to punctuation or markup
    subelement.tail = re.sub(r'(?<![p{P}>])\n', ' ', subelement.tail)
    # trim
    subelement.tail = trim(subelement.tail) + '\n'
    #if textfilter(subelement) is True:
    #    return None
    #if duplicate_test(subelement) is True:
    #    return None
    return subelement


# @profile
def extract_content(tree, include_tables=False):
    '''Find and extract the main content of a page using a set of expressions'''
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
        # define iteration strategy
        potential_tags = set(TAG_CATALOG) # 'span'
        if len(subtree.xpath('//p//text()')) == 0: # no paragraphs containing text
            LOGGER.debug('adding div')
            potential_tags.add('div')
        LOGGER.debug(sorted(potential_tags))
        # extract content
        for element in subtree.xpath('.//*'):
            ## delete unwanted
            if element.tag not in potential_tags:
                # LOGGER.debug('discarding: %s %s', element.tag, element.text)
                continue
            # bypass: nested elements
            if element.tag in ('list', 'quote'):
                processed_element = etree.Element(element.tag)
                for child in element.iter():
                    # list-specific check
                    if element.tag == 'list' and child.tag not in ('dt', 'li'): # 'item'
                        continue
                    # proceed with iteration
                    processed_child = handle_textnode(child)
                    if processed_child is not None:
                        if element.tag == 'list':
                            newsub = etree.SubElement(processed_element, 'item')
                        else:
                            newsub = etree.SubElement(processed_element, child.tag)
                        newsub.text = processed_child.text
                        if element.tag == 'quote':
                            newsub.tail = processed_child.tail
                    # child.getparent().remove(child)
                    child.tag = 'done' # can cause errors
                # avoid double tags??
                # element.getparent().remove(element)
                # element.tag = 'done' # can cause errors
                if len(processed_element) > 0: # if it has children
                    result_body.append(processed_element)
                continue

            # bypass: head:
            elif element.tag == 'head':
                if element.text is not None:
                    element.text = trim(element.text)
                    if element.text and re.search(r'\w', element.text):
                        result_body.append(element)
                continue

            # strip attrs after discard is run
            elif element.tag == 'p':
                element.attrib.clear()
                # no children
                if len(element) == 0:
                    processed_element = handle_textnode(element)
                    if processed_element is not None:
                        result_body.append(processed_element)
                    continue
                # children
                processed_element = etree.Element(element.tag)
                processed_element.text = ''
                for child in element.iter():
                    if child.tag in potential_tags:
                        processed_child = handle_textnode(child)
                        if child.tag == 'lb':
                            if child.tail is None or not re.search('\w+', child.tail):
                                continue
                            newsub = etree.SubElement(processed_element, 'lb')
                            newsub.tail = handle_subelement(child).tail
                            continue
                        if processed_child is not None:
                            # paragraph, append text
                            if child.tag == 'p':
                                if processed_child.text is not None:
                                    processed_element.text = processed_element.text + processed_child.text
                                if processed_child.tail is not None:
                                    processed_element.text = processed_element.text + ' ' + processed_child.tail
                            else:
                                newsub = etree.SubElement(processed_element, child.tag)
                                if processed_child.text is not None:
                                    newsub.text = trim(processed_child.text)
                                if processed_child.tail is not None:
                                    newsub.tail = trim(processed_child.tail)
                    child.tag = 'done'
                # finish
                #if len(processed_element) > 0:
                if len(processed_element.text) > 0:
                    result_body.append(processed_element)
                continue

            # insert it directly
            elif element.tag == 'lb':
                if element.tail is not None and re.search('\w+', element.tail):
                    element.tail = trim(element.tail)
                    result_body.append(element)

            # other elements (div, ??, ??)
            else:
                LOGGER.debug('processing other element: %s', element.tag)
                processed_element = handle_textnode(element)
                if processed_element is not None:
                    element.attrib.clear()
                    # small div-correction # could be moved elsewhere
                    if element.tag == 'div':
                        element.tag = 'p'
                    # insert
                    result_body.append(processed_element)
        # control
        if len(result_body) > 0: # if it has children
            LOGGER.debug(expr)
            break

    # try parsing wild <p> elements
    if len(result_body) == 0: # no children
        LOGGER.debug('Taking all p-elements')
        # prune
        search_tree = discard_unwanted(tree)
        # print(html.tostring(tree, pretty_print=False, encoding='unicode'))
        for element in search_tree.xpath('//p'):
            # print(element.tag, element.text)
            processed_element = handle_textnode(element)
            if processed_element is not None:
                processed_element.attrib.clear()
                processed_element.tail = ''
                result_body.append(processed_element)

    # TODO:
    # try parsing tables
# for _, element in etree.iterparse(xml_file, tag='a'):
#      print('%s -- %s' % (element.findtext('b'), element[1].text))
#      element.clear()
    if include_tables is True: #len(result_body) == 0: # no children
        LOGGER.debug('Using table extraction')
        search_tree = discard_unwanted(tree)
        for table_elem in search_tree.xpath('//table'):
            # iterate through elements in table
            for subelement in table_elem.xpath('.//*'):
                subelement.attrib.clear()
                if subelement.text is not None:
                    subelement.text = re.sub(r'(?<![p{P}>])\n', ' ', subelement.text)
                subelement.tail = ''
                if subelement.tag == 'th':
                    subelement.tag = 'head'
                elif subelement.tag == 'tr':
                    subelement.tag = 'row'
                    if len(' '.join(subelement.itertext())) < 50:
                        subelement.getparent().remove(subelement)
                        continue
                    if subelement.text is not None:
                        subelement.text = trim(subelement.text)
                elif subelement.tag == 'td':
                    #if len(' '.join(subelement.itertext())) < 30:
                        #subelement.getparent().remove(subelement)
                        #continue
                    if subelement.text is not None:
                        subelement.text = trim(subelement.text)
                    subelement.tag = 'cell'
                else:
                    # subelement.getparent().remove(subelement)
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


# @profile
def extract_comments(tree, include_comments):
    '''Try and extract comments out of potential sections in the HTML'''
    comments_body = etree.Element('body')
    # define iteration strategy
    potential_tags = set(TAG_CATALOG) # 'span'
    ## potential_tags.add('div') trouble with <div class="comment-author meta">
    # LOGGER.debug(sorted(potential_tags))
    ## return comments_body, tree
    for expr in COMMENTS_XPATH:
        # select tree if the expression has been found
        subtree = tree.xpath(expr)
        if len(subtree) == 0:
            continue
        subtree = subtree[0]
        # prune
        subtree = discard_unwanted_comments(subtree)
        # extract content
        for elem in subtree.xpath('.//*'): # was: for elem in tree.xpath(expr):
            if elem.tag in potential_tags: # TAG_CATALOG:
                processed_element = handle_textnode(elem, comments_fix=True)
                # test length and remove
                if processed_element is None or processed_element.text in comments_blacklist:
                    # elem.getparent().remove(elem)
                    continue
                else:
                ## TODO: text filter
                #if textfilter(elem) is True:
                #    continue
                # filter potential interesting p elements
                # if not elem.attrib or 'style' not in elem.attrib: # or not 'align' in elem.attrib
                    # insert if words
                    elem.attrib.clear()
                    comments_body.append(elem)
        # control
        if len(comments_body) > 0: # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            #for subtree in tree.xpath(expr):
            subtree.getparent().remove(subtree)
            break
    if include_comments is False:
        comments_body = etree.Element('body')
    return comments_body, tree


def write_teitree(postbody, commentsbody):
    '''Bundle the extracted post and comments into a TEI tree'''
    tei = etree.Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
    group = etree.SubElement(tei, 'group')
    # post
    postelem = etree.SubElement(group, 'text', type='entry', rendition='#pst')
    postelem.append(postbody)
    # comments
    commentselem = etree.SubElement(group, 'text', type='comments', rendition='#cmt')
    commentselem.append(commentsbody)
    return tei


def check_tei(tei, record_id):
    '''Check if the resulting XML file is conform and scrub remaining tags'''
    for element in tei.xpath('//text/body//*'):
        # check elements
        if element.tag not in TEI_VALID_TAGS:
            # disable warnings for chosen categories
            # if element.tag not in ('div', 'span'):
            LOGGER.warning('not a TEI element, removing: %s %s', element.tag, record_id)
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
                LOGGER.warning('not a valid TEI attribute, removing: %s in %s %s', attribute, element.tag, record_id)
                element.attrib.pop(attribute)
    # validate ?
    #if relaxng.validate(tei) is False:
    #    print(relaxng.error_log.last_error)
    # export metadata
    #metadata = (title + '\t' + date + '\t' + uniqueid + '\t' + url + '\t').encode('utf-8')
    return tei


def xmltotxt(xmloutput):
    '''Convert to plain text format'''
    #TODO: sanitize/valid XML
    returnstring = ''
    # returnstring = ' '.join(xmloutput.itertext())
    for element in xmloutput.iter():
        if element.text is None and element.tail is None:
            continue
        elif element.text is not None and element.tail is not None:
            textelement = element.text + ' ' + element.tail
        elif element.text is not None and element.tail is None:
            textelement = element.text
        else:
            textelement = element.tail
        textelement = sanitize(textelement)
        textelement = trim(textelement)
        if element.tag in ('code', 'head', 'item', 'lb', 'p', 'quote', 'row', 'table'):
            returnstring += '\n' + textelement + '\n'
        else:
            returnstring += textelement + ' '
    #returnstring = sanitize(returnstring)
    #returnstring = trim(returnstring)
    return returnstring


# main process
# @profile
def process_record(filecontent, url=None, record_id='0001', no_fallback=False, include_comments=True, xml_output=False, tei_output=False, target_language=None, include_tables=True):
    '''Main process for text extraction'''
    # init
    # LOGGER.debug('comments status: %s', include_comments)
    global tokens_posts, tokens_comments, LRU_TEST
    tree = load_html(filecontent)
    LOGGER.debug('HTML tree loaded for URL: %s', url)

    # save space and processing time
    cleaned_tree = prune_html(tree)

    ## clean
    cleaned_tree = HTML_CLEANER.clean_html(cleaned_tree)

    ## convert tags
    ## the rest does not work without conversion
    # if tei_output is True:
    cleaned_tree = convert_tags(cleaned_tree)
    # remove hi-element to avoid tail bug
    etree.strip_tags(cleaned_tree, 'hi')

    # comments first, then remove
    commentsbody, cleaned_tree = extract_comments(cleaned_tree, include_comments)

    ## extract content
    temppost_hand = extract_content(cleaned_tree, include_tables)

    ## compare
    temp_text = u' '.join(temppost_hand.itertext())
    if no_fallback is False:
        # try with justext
        temppost_algo = try_justext(tree, filecontent, record_id) # cleaned_tree
        # compare
        temp_jt = u' '.join(temppost_algo.itertext())
        LOGGER.info('extracted length: %s (jusText) %s (extraction)', len(temp_jt), len(temp_text))
        # conditions to use justext
        if 0 <= len(temp_text) < 300 and len(temp_jt) > 2*len(temp_text):
            justext_flag = True
        elif len(temppost_hand.xpath('//p')) == 0 and len(temp_jt) > 0: # borderline case
            justext_flag = True
        else:
            justext_flag = False
        if justext_flag is True: # was len(temp_text) > 10
            postbody = temppost_algo
            LOGGER.info('using justext: %s', url)
        else:
            postbody = temppost_hand
            LOGGER.info('using custom extraction: %s', url)
    else:
        LOGGER.info('extracted length: %s (extraction)', len(temp_text))
        postbody = temppost_hand

    # try to use original/dirty tree
    if len(temp_text) == 0 and len(temp_jt) == 0:
        tree = convert_tags(tree)
        temppost_hand = extract_content(tree)
        temp_text = u' '.join(temppost_hand.itertext())
        LOGGER.debug('non-clean extracted length: %s (extraction)', len(temp_text))
        postbody = temppost_hand

    # sanity check on length
    temp_text = u' '.join(postbody.itertext())
    temp_comments = u' '.join(commentsbody.itertext())
    if len(temp_text) < MIN_EXTRACTED_SIZE:
        LOGGER.error('not enough text %s %s', record_id, url)
    if len(temp_comments) < MIN_EXTRACTED_COMM_SIZE:
        LOGGER.warning('not enough comments %s %s', record_id, url)
    if len(temp_text) < MIN_EXTRACTED_SIZE and len(temp_comments) < MIN_EXTRACTED_COMM_SIZE:
        LOGGER.info('text and comments not long enough: %s %s', len(temp_text), len(temp_comments))
        return None

    # sanity check on language
    if target_language is not None:
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

    # cache elements
    cache(postbody)
    cache(commentsbody)

    # XML TEI steps
    if tei_output is True:
        # build TEI tree
        output = write_teitree(postbody, commentsbody)
        # filter output (strip unwanted elements), just in case
        # check and repair
        output = check_tei(output, record_id)
    else:
        output = etree.Element('root')
        postelem = etree.SubElement(output, 'text')
        postelem.append(postbody)
        commentselem = etree.SubElement(output, 'comments')
        commentselem.append(commentsbody)

    # sanity check on markup
    # if re.search(r'\[url', u''.join(postbody.itertext()):

    # check duplicates at body level
    teststring = ' '.join(postbody.itertext()).encode('utf-8')
    if LRU_TEST.has_key(teststring) is False:
        # LRU_TEST[teststring] = 1
        tokens_posts += len(re.findall(r'\w+', ' '.join(postbody.itertext()), re.UNICODE))
        tokens_comments += len(re.findall(r'\w+', ' '.join(commentsbody.itertext()), re.UNICODE))
        if xml_output is False and tei_output is False:
            returnstring = xmltotxt(output)
        else:
            control_string = etree.tostring(output)
            control_parser = etree.XMLParser(remove_blank_text=True)
            output_tree = etree.parse(BytesIO(control_string), control_parser)
            returnstring = etree.tostring(output_tree, pretty_print=True, encoding='unicode') # xml_declaration=True,

        ##  garbled unicode
        #try:
        #    returnstring = ftfy.fix_text(returnstring, fix_entities=False, fix_encoding=True, fix_surrogates=True)
        #except UnicodeDecodeError as err:
        #    LOGGER.warning('Unicode error: %s %s', err, record_id)
        # <hi> space hack
        #returnstring = re.sub(r'(\S) ?(<hi>) ?(\S)', r'\1 \2\3', returnstring)
        #returnstring = re.sub(r'(\S) ?(</hi>) ?(\S)', r'\1\2 \3', returnstring)

        returnstring = sanitize(returnstring)
        return returnstring

    # else
    # LRU_TEST[teststring] += 1

    #LOGGER.info('tokens posts: %s', tokens_posts)
    #LOGGER.info('tokens comments: %s', tokens_comments)

    return None
