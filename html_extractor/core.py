# -*- coding: utf-8 -*-
# pylint:disable-msg=E0611,I1101
"""
Module bundling all functions needed to extract the text in a webpage.
"""

## This file is available from https://github.com/adbar/html-extractor
## under GNU GPL v3 license

# standard
import logging
import re

# from collections import defaultdict

# third-party
import justext # from justext import classify_paragraphs, get_stoplist, revise_paragraph_classification
import langid
langid.set_languages(['de', 'en', 'es', 'fr', 'ja', 'nl', 'ru'])
# import regex as re

from lru import LRU # https://github.com/amitdev/lru-dict # pip3 install lru-dict
## https://docs.python.org/3/library/functools.html#functools.lru_cache
from lxml import etree, html
from lxml.html.clean import Cleaner

# own
from .utils import load_html, sanitize, trim


# import settings
MIN_EXTRACTED_SIZE = 200
MIN_DUPLCHECK_SIZE = 100
LRU_SIZE = 10000000
MIN_EXTRACTED_COMM_SIZE = 100


## TODO:
# add sqlite3 for control of seen URLs?
# line-based heuristics?
# check max depth recursion in output XML?

# alternatives if text too short:
# https://github.com/kingwkb/readability
# https://github.com/grangier/python-goose
# https://github.com/buriy/python-readability
# # python-boilerpipe for text?
# # https://github.com/seomoz/dragnet

### http://teibyexample.org/xquery/TBEvalidator.xq

# https://github.com/seomoz/simhash-py

# parser:
# https://github.com/kovidgoyal/html5-parser
# https://github.com/rushter/selectolax


## INIT
LOGGER = logging.getLogger(__name__)

TAG_CATALOG = frozenset(['code', 'del', 'head', 'hi', 'item', 'lb', 'list', 'p', 'quote']) # 'span'

cut_empty_elems = ('div', 'p', 'section')

comments_blacklist = ('( Abmelden / Ändern )')

# LRU_DICT = defaultdict(int)


BODY_XPATH = ['//*[(self::div or self::section)][contains(@id, "entry-content") or contains(@class, "entry-content") or contains(@id, "article-content") or contains(@class, "article-content")]', \
            "//*[(self::div or self::section)][contains(@class, 'post-text') or contains(@class, 'post_text')]", \
            "//*[(self::div or self::section)][contains(@class, 'post-body')]", \
            "//*[(self::div or self::section)][contains(@class, 'post-content') or contains(@class, 'post_content') or contains(@class, 'postcontent')]", \
            "//*[(self::div or self::section)][contains(@class, 'post-entry') or contains(@class, 'postentry')]", \
            "//*[(self::div or self::section)][starts-with(@class, 'entry')]", \
            '//*[(self::div or self::section)][@id="content-main" or @id="content" or @class="content"]', \
            "//*[(self::div or self::section)][starts-with(@id, 'article')]", \
            '//article', \
            "//*[(self::article or self::div or self::section)][starts-with(@class, 'article')]", \
            "//*[(self::article or self::div or self::section)][starts-with(@id, 'main') or starts-with(@class, 'main') or starts-with(@role, 'main')]", \
            '//*[(self::div or self::section)][@class="text"]', \
            "//*[(self::div or self::section)][starts-with(@class, 'post-bodycopy')]", \
            "//*[(self::div or self::section)][@class='postarea']", \
            '//*[(self::div or self::section)][contains(@class, "storycontent")]', \
            "//*[(self::div or self::section)][starts-with(@id, 'primary')]", \
            "//*[(self::div or self::section)][starts-with(@class, 'theme-content') or starts-with(@class, 'blog-content') or starts-with(@class, 'section-content') or starts-with(@class, 'single-content')]", \
            '//*[(self::div or self::section)][@class="art-postcontent"]', \
            '//*[(self::div or self::section)][@class="post"]', \
            '//div[contains(translate(@class, "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "fulltext")]', \
            "//*[(self::div or self::section)][starts-with(@class, 'wpb_text_column')]", \
            '//div[@class="cell"]', \
            '//*[(self::div or self::section)][@itemprop="articleBody"]', \
           ]

COMMENTS_XPATH = ["//*[(self::div or self::section or self::ol or self::ul)][contains(@id, 'commentlist') or contains(@class, 'commentlist')]", \
                "//*[(self::div or self::section or self::ol or self::ul)][starts-with(@id, 'comments') or starts-with(@class, 'comments') or starts-with(@class, 'Comments')]", \
                "//*[(self::div or self::section or self::ol)][starts-with(@id, 'comment-') or starts-with(@class, 'comment-')]", \
                "//*[(self::div or self::section)][starts-with(@id, 'comol')]", \
                "//*[(self::div or self::section)][starts-with(@id, 'disqus_thread')]", \
                "//ul[starts-with(@id, 'dsq-comments')]" \
                "//*[(self::div or self::section)][starts-with(@id, 'social')]" \
                "//*[(self::div or self::section)][contains(@class, 'comment')]", \
               ]
# '//*[(self::div or self::section)][@id="comments" or @class="comments"]', \

DISCARD_XPATH = ['.//*[(self::div or self::section or self::ul)][contains(@id, "sidebar") or contains(@class, "sidebar")]', \
                 './/*[(self::div or self::section)][contains(@id, "footer") or contains(@class, "footer")]', \
                 './/footer', \
                 './/header', \
                 './/*[(self::div or self::section)][contains(@id, "header") or contains(@class, "header")]', \
                 './/*[(self::div or self::section)][contains(@id, "tags") or contains(@class, "tags")]', \
                 # news outlets
                 './/*[(self::div or self::p or self::section)][contains(@id, "teaser") or contains(@class, "teaser")]',\
                 # navigation
                 './/*[(self::div or self::section)][starts-with(@id, "nav-") or starts-with(@class, "nav-")]', \
                 './/*[starts-with(@id, "breadcrumbs")]',\
                 './/*[contains(@id, "breadcrumb") or contains(@class, "breadcrumb") or contains(@id, "bread-crumb") or contains(@class, "bread-crumb")]',\
                 # related posts
                 './/*[(self::div or self::section)][contains(@id, "related") or contains(@class, "related")]', \
                 # sharing jp-post-flair jp-relatedposts
                 './/*[(self::div or self::section or self::ul)][starts-with(@class, "author-") or starts-with(@id, "shar") or starts-with(@class, "shar") or contains(@class, "share-") or contains(@id, "social") or contains(@class, "social") or starts-with(@id, "jp-") or starts-with(@id, "dpsp-content")]', \
                 './/*[(self::div or self::section)][contains(@id, "author") or contains(@class, "author")]', \
#                './/aside', \ # conflicts with text extraction
                ]

COMMENTS_DISCARD_XPATH = ['.//*[(self::div or self::section)][starts-with(@id, "respond")]', \
                          './/cite', \
                          './/quote', \
                          './/*[starts-with(@id, "reply-") or starts-with(@class, "reply-title")]', \
                          './/*[contains(@id, "akismet") or contains(@class, "akismet")]', \
                         ]


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
lrutest = LRU(LRU_SIZE)

# justext
JUSTEXT_STOPLIST = justext.get_stoplist('German')



def prune_html(tree):
    '''delete empty elements'''
    # empty tags
    for element in tree.xpath(".//*[not(node())]"):
        if element.tag in cut_empty_elems:
            element.getparent().remove(element)
    # https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
    # Walk over all elements in the tree and remove all nodes that are recursively empty
    # context = etree.iterwalk(tree)
    # for action, element in context:
    #     parent = element.getparent()
    #     if element.tag in cut_empty_elems and recursively_empty(element):
    #        parent.remove(element)
    ## https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
    # if elem.text:
    #    return False
    # return all((recursively_empty(c) for c in elem.iterchildren()))
    return tree


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
    if re.match(r'Gef.llt mir.+|.hnliche Beitr.+|Fill in your details below.+|Trage deine Daten unten.+|Kommentar verfassen.+|Bitte logge dich.+|Hinterlasse einen Kommentar|Connecting to %s|Verbinde mit %s|Facebook$|Twitter$|Google$|E-Mail$|Drucken$|LinkedIn$', element.text):
        return True
    if re.search(r'Tags: [A-ZÄÖÜßa-zäöü ,]+', element.text):
        return True
    # elemtext = trim(elemtext)
    #return elemtext
    return False


def cache(body):
    '''Implement LRU cache'''
    global lrutest
    for element in body:
        # teststring = ' '.join(element.itertext()).encode('utf-8')
        teststring = element.text
        if lrutest.has_key(teststring) is True:
            lrutest[teststring] += 1
        else:
            lrutest[teststring] = 1


def duplicate_test(element, justext_switch=False):
    '''Check for duplicate text'''
    global lrutest
    # teststring = ' '.join(element.itertext()).encode('utf-8')
    if justext_switch is False:
        teststring = element.text_content()
    else:
        teststring = element.text
    if len(teststring) > MIN_DUPLCHECK_SIZE:
        if lrutest.has_key(teststring) is True and lrutest[teststring] > 2:
            # lrutest[teststring] += 1
            return True
    return False


def convert_tags(tree):
    '''Convert relevant HTML tags to XML TEI format'''
    # head tags + delete attributes
    for elem in tree.xpath('//h1|//h2|//h3|//h4|//h5|//h6'):
        # elem.attrib.clear()
        elem.tag = 'head'
        # elem.set('rendition', '#i')
    # delete p attributes
    # for elem in tree.xpath('//p'):
        # elem.attrib.clear()
    # br → lb
    for elem in tree.xpath('//br|//hr'): # tree.xpath('//[br or hr]'): ## hr → //lb/line ?
        elem.tag = 'lb'
        elem.attrib.clear()
    # ul/ol → list / li → item
    for elem in tree.xpath('//ul|//ol|//dl'):
        elem.tag = 'list'
        # elem.attrib.clear()
        # change children
        for child in elem.iter(): # for child in elem.xpath('.//li|.//dt'):
            if child.tag == 'li' or child.tag == 'dt':
                child.tag = 'item'
                child.attrib.clear()
            #else:
            #    LOGGER.debug('other child in list: %s', child.tag)
    # blockquote | q → quote
    for elem in tree.xpath('//blockquote|//q'):
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
    for elem in tree.xpath('//pre|//tt'): # //code
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
            # if lrutest.has_key(paragraph.text) is False or lrutest[paragraph.text] <= 2:
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
def extract_content(tree):
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
        if len(subtree.xpath('.//p//text()')) == 0: # no paragraphs containing text
            potential_tags.add('div')
        LOGGER.debug(sorted(potential_tags))
        # extract content
        for element in subtree.xpath('.//*'):
            ## delete unwanted
            if element.tag not in potential_tags:
                continue
            # strip attrs after discard is run
            if element.tag in ('div', 'head', 'list', 'p'):
                element.attrib.clear()
            # TODO: weird and empty elements such as <p><p>...</p></p> ???
            if element.text is None: # or len(element.text) < 10 # text_content()
                # try the tail
                if element.tail is None or len(element.tail) < 2: # was 50
                    element.getparent().remove(element)
                    continue
                # if element.tag == 'lb':
                LOGGER.debug('using tail for element %s', element.tag)
                # TODO: handle differently for br/lb
                element.text = element.tail
                element.tail = ''
                if element.tag == 'lb':
                    element.tag = 'p'
            ## LOGGER.debug(element.tag, element.text)
            if textfilter(element) is True:
                continue

            ## filter potential interesting p elements?
            #not elem.attrib or not 'style' in elem.attrib: # not 'align' in elem.attrib or
            if element.text and re.search(r'\w', element.text): # text_content()
                ## TODO: improve duplicate detection
                if duplicate_test(element) is True:
                    continue
                # small div-correction # could be moved elsewhere
                if element.tag == 'div':
                    element.tag = 'p'
                # handle p-tags and attributes
                #if element.tag == 'p': #  or element.tag == 'item'
                #    element.attrib.clear()
                #    LOGGER.debug(element.text)
                #else:
                #    element.tail = ''
                # insert
                result_body.append(element)
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
            if element.text is not None:
                # if duplicate_test(elem) is True:
                element.attrib.clear()
                element.tail = ''
                result_body.append(element)
    return result_body


# @profile
def extract_comments(tree):
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
                # test length and remove
                if elem.text is None or elem.text in comments_blacklist:
                    # elem.getparent().remove(elem)
                    continue
                ## TODO: text filter
                if textfilter(elem) is True:
                    continue
                # filter potential interesting p elements
                # if not elem.attrib or 'style' not in elem.attrib: # or not 'align' in elem.attrib
                if elem.text and re.search(r'\w', elem.text):
                    if duplicate_test(elem) is True:
                        continue
                    # insert if words
                    comments_body.append(elem)
        # control
        if len(comments_body) > 0: # if it has children
            LOGGER.debug(expr)
            # remove corresponding subtree
            #for subtree in tree.xpath(expr):
            subtree.getparent().remove(subtree)
            break
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
        if element.tag in ('code', 'head', 'item', 'lb', 'p', 'quote'):
            returnstring += '\n' + textelement + '\n'
        else:
            returnstring += textelement + ' '
    #returnstring = sanitize(returnstring)
    #returnstring = trim(returnstring)
    return returnstring


# main process
# @profile
def process_record(filecontent, url=None, record_id='0001', compare_flag=True, tei_output=False, target_language=None, txt_output=False):
    '''Main process for text extraction'''
    # init
    global tokens_posts, tokens_comments, lrutest
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
    commentsbody, cleaned_tree = extract_comments(cleaned_tree)

    ## extract content
    temppost_hand = extract_content(cleaned_tree)

    ## compare
    temp_text = u' '.join(temppost_hand.itertext())
    if compare_flag is True:
        # try with justext
        temppost_algo = try_justext(cleaned_tree, filecontent, record_id)
        # compare
        temp_jt = u' '.join(temppost_algo.itertext())
        LOGGER.info('extracted length: %s (jusText) %s (extraction)', len(temp_jt), len(temp_text))
        # condition to use justext
        if 0 <= len(temp_text) < 300 and len(temp_jt) > 2*len(temp_text): # was len(temp_text) > 10
            postbody = temppost_algo
        else:
            postbody = temppost_hand
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
    if lrutest.has_key(teststring) is False:
        # lrutest[teststring] = 1
        tokens_posts += len(re.findall(r'\w+', ' '.join(postbody.itertext()), re.UNICODE))
        tokens_comments += len(re.findall(r'\w+', ' '.join(commentsbody.itertext()), re.UNICODE))
        if txt_output is True:
            returnstring = xmltotxt(output)
        else:
            returnstring = etree.tostring(output, pretty_print=True, encoding='unicode') # xml_declaration=True,

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
    # lrutest[teststring] += 1

    #LOGGER.info('tokens posts: %s', tokens_posts)
    #LOGGER.info('tokens comments: %s', tokens_comments)

    return None
