# -*- coding: utf-8 -*-
"""
Module bundling all functions needed to extract the text in a webpage.
"""

## This file is available from https://github.com/adbar/html-extractor
## under GNU GPL v3 license

# compatibility
from __future__ import absolute_import, division, print_function, unicode_literals

# from future import standard_library
# standard_library.install_aliases()

# standard
import logging
import re

from collections import OrderedDict
from io import StringIO # python3


# third-party
import ftfy
import justext # from justext import classify_paragraphs, get_stoplist, revise_paragraph_classification
import langid

# import regex as re # import re

from lxml import etree, html
from lxml.html.clean import Cleaner
from lru import LRU # https://github.com/amitdev/lru-dict # pip3 install lru-dict


# own
# import settings
MIN_EXTRACTED_SIZE = 200
MIN_DUPLCHECK_SIZE = 100
CORPUS_VERSION = 2017.1
LRU_SIZE = 10000000
MIN_EXTRACTED_COMM_SIZE = 100


## TODO:
# add sqlite3 for control of seen URLs?
# line-based heuristics?
# check max depth recursion in output XML?
# https://github.com/lxml/lxml/blob/master/benchmark/bench_etree.py

# alternatives if text too short:
# https://github.com/kingwkb/readability
# https://github.com/grangier/python-goose
# https://github.com/miso-belica/jusText
# https://github.com/buriy/python-readability
# # python-boilerpipe for text?
# # https://github.com/seomoz/dragnet

## DESIDERATA:
# https://github.com/benhoyt/scandir
# title -dash/hyphen- blogname
# date <div class="meta-text"> 10. Jun 2013 ?
# encoding detection? https://code.google.com/p/chared/
# if p empty, take div?
# os.path.getmtime() as last rescue for date?

# <meta name="geo.placename" content="Marl" />
# <meta name="geo.position" content="51.6789;7.11825" />
# <meta name="ICBM" content="51.6789, 7.11825" />
# attributes data-geo-lat data-geo-long

### http://teibyexample.org/xquery/TBEvalidator.xq

# https://github.com/seomoz/simhash-py

# https://github.com/chardet/chardet
# https://github.com/PyYoshi/cChardet

# https://github.com/zachwill/moment

# parser:
# https://html5-parser.readthedocs.io/en/latest/

# metadata:
# https://github.com/peterc/pismo/



## INIT
logger = logging.getLogger(__name__)

comm_length = 2 # was 10

tag_catalog = set(['code', 'del', 'head', 'hi', 'list', 'p', 'span', 'quote']) # item
errors = OrderedDict() # dict() # defaultdict(list)
errors['file'], errors['blogname'], errors['title'], errors['url'], errors['description'], errors['date'], errors['categories'], errors['tags'], errors['body'], errors['comments'], errors['author'], errors['language'] = [[] for _ in range(12)]

cut_empty_elems = ('div')

text_blacklist = ('Gefällt mir', 'Facebook', 'Twitter', 'Google', 'E-Mail', 'Drucken')
comments_blacklist = ('( Abmelden / Ändern )')

## parse
htmlparser = html.HTMLParser() # remove_blank_text=True recover=True

# https://github.com/peterc/pismo/blob/master/lib/pismo/lede_matches.rb
#     {'attr': 'itemprop', 'value': 'articleBody'}, {'attr': 'class', 'value': 'post-content'}, {'tag': 'article'},
bodyexpr = ["//*[(self::div or self::section)][starts-with(@id, 'entry-content')]//*", \
                '//*[(self::div or self::section)][starts-with(@class, "entry-content")]//*', \
                "//*[(self::div or self::section)][starts-with(@class, 'entry')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'post-text')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'post_text')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'post-content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'post_content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'postcontent')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'post-entry')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'postentry')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'post-bodycopy')]//*", \
                "//*[(self::div or self::section)][@class='postarea']//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'main')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'main')]//*", \
                '//*[(self::div or self::section)][@role="main"]//*', \
                "//*[(self::div or self::section)][starts-with(@id, 'main-content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'main-content')]//*", \
                '//*[(self::div or self::section)][@id="content-main"]//*', \
                "//*[(self::div or self::section)][starts-with(@id, 'contents')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'content')]//*", \
                '//*[(self::div or self::section)][@class="hyphenate storycontent"]//*', \
                '//*[(self::div or self::section)][@class="storycontent"]//*', \
                "//*[(self::div or self::section)][starts-with(@id, 'primary')]//*", \
                '//article//*', \
                "//*[(self::div or self::section)][starts-with(@class, 'theme-content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'blog-content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'section-content')]//*", \
                '//*[(self::div or self::section)][@class="art-postcontent"]//*', \
                '//*[(self::div or self::section)][@class="content section"]//*', \
                '//*[(self::div or self::section)][@class="post"]//*', \
                '//*[(self::div or self::section)][@class="single-content"]//*', \
                "//*[(self::div or self::section)][starts-with(@class, 'article')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'wpb_text_column')]//*", \
                '//div[@class="cell"]//*']

commentsexpr = ["//*[(self::div or self::section or self::ol)][starts-with(@id, 'commentlist')]//*", \
                "//*[(self::div or self::section or self::ol)][starts-with(@class, 'commentlist')]//*", \
                "//*[(self::div or self::section or self::ol)][starts-with(@id, 'comments')]//*", \
                "//*[(self::div or self::section or self::ol)][starts-with(@class, 'comments')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'comment-text')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'comment-content')]//*", \
                "//*[(self::div or self::section)][starts-with(@class, 'comment-body')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'comment-section')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'commentspanel')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'comment-form-identity')]//*", \
                "//ul[starts-with(@id, 'commentlist')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'comol')]//*", \
                "//*[(self::div or self::section)][starts-with(@id, 'disqus_thread')]//*", \
                "//ul[starts-with(@id, 'dsq-comments')]//*"]
# <div id="social">


# cleaner config # http://lxml.de/api/lxml.html.clean.Cleaner-class.html
cleaner = Cleaner()
cleaner.annoying_tags = True
cleaner.comments = True
cleaner.embedded = True
cleaner.forms = True
cleaner.frames = True
cleaner.javascript = True
cleaner.links = False
cleaner.meta = False
cleaner.page_structure = False
cleaner.processing_instructions = True
cleaner.remove_unknown_tags = False
cleaner.safe_attrs_only = False
cleaner.scripts = True
cleaner.style = False
cleaner.remove_tags = ['abbr', 'acronym', 'address', 'big', 'cite', 'font', 'ins', 'small', 'sub', 'sup', 'wbr'] #  'center', 'strike', , 'u' 'table', 'tbody', 'td', 'th', 'tr',
cleaner.kill_tags = ['audio', 'canvas', 'embed', 'figure', 'img', 'label', 'map', 'math', 'object', 'picture', 'style', 'svg', 'video'] # 'area', 'table'

# to delete after parsing
delete_tags = set(['link', 'noscript', 'table', 'time'])

# validation
tei_valid = set(['code', 'del', 'head', 'hi', 'item', 'lb', 'list', 'p', 'quote'])
tei_valid_attributes = set(['rendition'])

# counters
tokens_posts = 0
tokens_comments = 0
lrutest = LRU(LRU_SIZE)

# justext
justext_stoplist = justext.get_stoplist('German')


# trim text function
def trim(string):
    """Remove spaces at the beginning and end of a string"""
    # string = re.sub(r'\n+', '\n', string, re.MULTILINE)
    string = re.sub(r'\s+', ' ', string.strip(' \t\n\r'), re.MULTILINE)
    # may be superfluous
    # string = re.sub(r'^\s+|\s+$', '', string.strip(' \t\n\r'))
    return string


## https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
#def recursively_empty(elem):
#    if elem.text:
#        return False
#    return all((recursively_empty(c) for c in elem.iterchildren()))


def load_html(htmlobject):
    """Load object given as input and validate its type (accepted: LXML tree and string)"""
    if isinstance(htmlobject, (etree._ElementTree, html.HtmlElement)):
        # copy tree
        tree = htmlobject
        # derive string
        # htmlstring = html.tostring(htmlobject, encoding='unicode')
    elif isinstance(htmlobject, str):
        # the string is a URL, download it
        #if re.match(r'https?://', htmlobject):
        #    logger.info('URL detected, downloading: %s', htmlobject)
        #    rget = fetch_url(htmlobject)
        #    if rget is not None:
        #        htmlstring = rget.text
        # copy string
        #else:
        # htmlstring = htmlobject
        ## robust parsing
        try:
            # parse
            # parser = html.HTMLParser() # encoding='utf8'
            tree = html.parse(StringIO(htmlobject), parser=htmlparser)
            ## TODO: clean page?
            # cleaner.clean_html(html.parse(StringIO(filecontent), htmlparser))
            # tree = html.fromstring(html.encode('utf8'), parser=htmlparser)
            # <svg>
        except UnicodeDecodeError as err:
            logger.error('unicode %s', err)
            tree = None
        except UnboundLocalError as err:
            logger.error('parsed string %s', err)
            tree = None
        except (etree.XMLSyntaxError, ValueError, AttributeError) as err:
            #errors['file'].append(filename)
            logger.error('parser %s', err)
            tree = None
    else:
        logger.error('this type cannot be processed: %s', type(htmlobject))
        tree = None
        # htmlstring = None
    return tree


def prune_html(tree):
    '''delete empty and unwanted elements'''
    # empty tags
    for element in tree.xpath(".//*[not(node())]"):
        # print(element.tag)
        if element.tag in cut_empty_elems:
            element.getparent().remove(element)
    # remove tags
    for delitem in delete_tags:
        for elem in tree.xpath('//' + delitem):
            elem.getparent().remove(elem)
    # https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
    # Walk over all elements in the tree and remove all nodes that are recursively empty
    # context = etree.iterwalk(tree)
    # for action, element in context:
    #     parent = element.getparent()
    #     if element.tag in cut_empty_elems and recursively_empty(element):
    #        print('#2', elem.tag)
    #        parent.remove(element)
    return tree


def textfilter(elemtext):
    '''Filter out unwanted text'''
    elemtext = re.sub(r'^Gef.llt mir.+|^.hnliche Beitr.+', '', elemtext)
    elemtext = re.sub(r'^Fill in your details below.+|^Trage deine Daten unten.+|^Kommentar verfassen.+|^Bitte logge dich.+|^Hinterlasse einen Kommentar', '', elemtext)
    elemtext = re.sub(r'^Connecting to %s|^Verbinde mit %s', '', elemtext)
    elemtext = re.sub(r'Tags: [A-ZÄÖÜßa-zäöü ,]+', '', elemtext)
    elemtext = trim(elemtext)
    return elemtext


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


def duplicate_test(element):
    '''Check for duplicate text'''
    global lrutest
    # teststring = ' '.join(element.itertext()).encode('utf-8')
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
        elem.attrib.clear()
        elem.tag = 'head'
        elem.set('rendition', '#i')
    # delete p attributes
    for elem in tree.xpath('//p'):
        elem.attrib.clear()
    # br → lb
    for elem in tree.xpath('//br|//hr'): # tree.xpath('//[br or hr]'): ## hr → //lb/line ?
        elem.tag = 'lb'
        elem.attrib.clear()
    # ul/ol → list / li → item
    for elem in tree.xpath('//ul|//ol|//dl'):
        elem.tag = 'list'
        elem.attrib.clear()
        # change children
        #for child in elem.iter():
        #    if child.tag == 'li' or child.tag == 'dt':
        #        child.tag = 'item'
        for child in elem.xpath('//li|//dt'):
            child.tag = 'item'
    # blockquote | q → quote
    for elem in tree.xpath('//blockquote|//q'):
        elem.tag = 'quote'
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
    # change rendition #t (very rare)
    for elem in tree.xpath('//tt'):
        elem.tag = 'hi'
        elem.set('rendition', '#t')
    # del | s | strike → <del rend="overstrike">
    for elem in tree.xpath('//del|//s|//strike'):
        elem.attrib.clear()
        elem.tag = 'del'
        elem.set('rendition', 'overstrike')
    # strip tags
    etree.strip_tags(tree, 'a', 'dd')
    return tree


def try_justext(tree, filecontent, record_id):
    '''safety net: try with justext'''
    tempelem = etree.Element('body')
    justtextstring = html.tostring(tree, pretty_print=False, encoding='unicode')
    logger.info('raw length: %s (file) %s (tostring) ', len(filecontent), len(justtextstring))
    try:
        # paragraphs = custom_justext(tree)
        paragraphs = justext.justext(justtextstring, justext_stoplist)
    except ValueError as err: # ValueError: Input object is not an XML element: HtmlComment
        logger.error('justext %s %s', err, record_id)
        return None
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            # if lrutest.has_key(paragraph.text) is False or lrutest[paragraph.text] <= 2:
            if duplicate_test(paragraph) is not True:
                elem = etree.Element('p')
                elem.text = paragraph.text
                tempelem.append(elem)
            # jt += paragraph.text + '</p><p>'
    # jt += '</p>'
    # temp_jt = u' '.join(jt.itertext())
    # temp_jt = jt
    return tempelem


def extract_content(tree):
    '''Find and extract the main content of a page using a set of expressions'''
    postfound = False
    tempelem = etree.Element('body')
    for expr in bodyexpr:
        if postfound is False:
            # extract content
            for element in tree.xpath(expr):
                if element.tag in tag_catalog: ### potential restriction here
                    elemtext = element.text
                    # print(element.tag, elemtext)
                    # test length and remove
                    ## delete unwanted
                    if elemtext is None or len(elemtext) < 1: # was 10
                        element.getparent().remove(element)
                        continue
                    # replace by temporary tag
                    elem = element
                    if elemtext in text_blacklist:
                        elem.getparent().remove(elem)
                        continue
                    elem.text = textfilter(elemtext) # replace back

                    ## filter potential interesting p elements
                    if not elem.attrib or not 'style' in elem.attrib: # not 'align' in elem.attrib or
                        if elem.text and re.search(r'\w', elem.text):
                            if duplicate_test(elem) is True:
                                continue
                            # filter attributes
                            if elem.tag == 'p': #  or elem.tag == 'item'
                                # for key in elem.attrib:
                                #    elem.attrib.pop(key)
                                elem.attrib.clear()
                            # insert
                            tempelem.append(elem)
                            postfound = True
                        # register non-p elements
                        #if elem.tag != 'p':
                        #    teststring = ' '.join(elem.itertext()).encode('utf-8')
    return tempelem


def extract_comments(tree):
    '''Try and extract comments out of potential sections in the HTML'''
    commentsfound = False
    commentsbody = etree.Element('body')
    for expr in commentsexpr:
        if commentsfound is False:
            # extract content
            for elem in tree.xpath(expr):
                if elem.tag in tag_catalog:
                   # delete unwanted
                   ## TODO: text filter
                    if elem.text:
                        elem.text = re.sub(r'^Fill in your details below.+|^Trage deine Daten unten.+|^Kommentar verfassen.+|^Bitte logge dich.+|^Hinterlasse einen Kommentar', '', elem.text)
                        elem.text = re.sub(r'^Connecting to %s|^Verbinde mit %s', '', elem.text)
                        elem.text = trim(elem.text)
                    # test length and remove
                    if elem.text is None or elem.text in comments_blacklist:
                        elem.getparent().remove(elem)
                        continue
                    # filter potential interesting p elements
                    if not elem.attrib or not 'style' in elem.attrib: # or not 'align' in elem.attrib
                        if elem.text and re.search(r'\w', elem.text):
                            if duplicate_test(elem) is True:
                                continue
                            # delete attributes
                            #for key in elem.attrib:
                            #    elem.attrib.pop(key)
                            # insert if words
                            commentsbody.append(elem)
                            commentsfound = True
    return commentsbody


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


# main process
#@profile
def process_record(filecontent, url, record_id, compare_flag=True, tei_output=True):
    '''Main process for text extraction'''
    global tokens_posts, tokens_comments, lrutest

    # try to read non-unicode as latin1
    #if len(filecontent) < 1:
    #    with open(filename, 'r', encoding='iso-8859-1') as inputfh:
    #        filecontent = inputfh.read()
    #        try:
    #            filecontent = ftfy.fix_text(filecontent, fix_entities=False, fix_encoding=True, fix_surrogates=True)
    #        except UnicodeDecodeError:
    #            print('WARN: unicode repair failed', filename)
    #        if len(filecontent) < 1:
    #            errors['file'].append(filename)
    #            print('ERROR: encoding', filename)
    #            return None

    # init
    tree = load_html(filecontent)
    logger.debug('starting')

    # valid or not?
    # tree = html.parse(StringIO(filecontent), htmlparser) # document_fromstring

    ## clean
    tree = cleaner.clean_html(tree)
    tree = prune_html(tree)

    ## convert tags
    tree = convert_tags(tree)

    ## extract content
    temppost_hand = extract_content(tree)

    ## compare
    temp_text = u' '.join(temppost_hand.itertext())
    if compare_flag is True:
        # try with justext
        temppost_algo = try_justext(tree, filecontent, record_id)
        # compare
        temp_jt = u' '.join(temppost_algo.itertext())
        logger.info('extracted length: %s (jusText) %s (extraction)', len(temp_jt), len(temp_text))
        # condition to use justext
        if len(temp_text) > 10 and len(temp_jt) > 3*len(temp_text):
            postbody = temppost_algo
        else:
            postbody = temppost_hand
    else:
        logger.info('extracted length: %s (extraction)', len(temp_text))
        postbody = temppost_hand

    # comments
    commentsbody = extract_comments(tree)

    # sanity check on length
    temp_text = u' '.join(postbody.itertext())
    temp_comments = u' '.join(commentsbody.itertext())
    if len(temp_text) < MIN_EXTRACTED_SIZE:
        logger.error('not enough text %s %s', record_id, url)
    if len(temp_comments) < comm_length:
        logger.warning('not enough comments %s %s', record_id, url)
    if len(temp_text) < MIN_EXTRACTED_SIZE and len(temp_comments) < comm_length:
        return None

    # sanity check on language
    # comments
    if len(temp_comments) > len(temp_text):
        langtest = temp_comments
    # default
    else:
        langtest = temp_text
    langresult = langid.classify(langtest)
    if langresult[0] != 'de':
    # if langresult[0] != 'en':
        logger.warning('wrong language: %s %s %s', langresult, record_id, url)
        logger.debug('wrong language: %s %s', langresult, temp_text)
        errors['language'].append(url)
        return None

    # cache elements
    cache(postbody)
    cache(commentsbody)

    ## build TEI tree
    # if tei_output is True:
    tei = write_teitree(postbody, commentsbody)

    # filter output (strip unwanted elements), just in case
    # check and repair
    for element in tei.xpath('//text/body//*'):
        # check elements
        if element.tag not in tei_valid:
            # disable warnings for chosen categories
            if element.tag not in ('div', 'span'):
                logger.warning('not a TEI element, removing: %s %s', element.tag, record_id)
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
            if attribute not in tei_valid_attributes:
                logger.warning('not a valid TEI attribute, removing: %s in %s %s', attribute, element.tag, record_id)
                element.attrib.pop(attribute)
        # validate ?
        #if relaxng.validate(tei) is False:
        #    print(relaxng.error_log.last_error)
        # export metadata
        #metadata = (title + '\t' + date + '\t' + uniqueid + '\t' + url + '\t').encode('utf-8')

    # sanity check on markup
    # if re.search(r'\[url', u''.join(postbody.itertext()):

    # check duplicates at body level
    # hashvalue = hashlib.md5(' '.join(postbody.itertext()).encode('utf-8')).digest()
    teststring = ' '.join(postbody.itertext()).encode('utf-8')
    if lrutest.has_key(teststring) is False:
        lrutest[teststring] = 1
        tokens_posts += len(re.findall(r'\w+', u' '.join(postbody.itertext()), re.UNICODE))
        tokens_comments += len(re.findall(r'\w+', u' '.join(commentsbody.itertext()), re.UNICODE))
        returnstring = etree.tostring(tei, pretty_print=True, encoding='unicode')  # , date xml_declaration=True,
        # <hi> space hack
        returnstring = re.sub(r'(\S) ?(<hi>) ?(\S)', r'\1 \2\3', returnstring)
        returnstring = re.sub(r'(\S) ?(</hi>) ?(\S)', r'\1\2 \3', returnstring)
        # &#13; (space) hack
        returnstring = re.sub(r'&#13;', '', returnstring)
        # filter out empty lines
        returnstring = '\n'.join(line for line in returnstring.split('\n') if line.strip())

        ##  garbled unicode
        try:
            returnstring = ftfy.fix_text(returnstring, fix_entities=False, fix_encoding=True, fix_surrogates=True)
        except UnicodeDecodeError as err:
            logger.warning('Unicode error: %s %s', err, record_id)

        # return None

        return returnstring
    # else
    lrutest[teststring] += 1

    logger.info('tokens posts: %s', tokens_posts)
    logger.info('tokens comments: %s', tokens_comments)

    # return values
    return postbody, commentsbody


## TODO: unicode test
#def unicode_test(htmlstring):
#    pass
# https://chardet.readthedocs.io/en/latest/


#def custom_justext(htmldom):
#    paragraphs = ParagraphMaker.make_paragraphs(htmldom)
#    justext.classify_paragraphs(paragraphs, justext.get_stoplist("German"), length_low=LENGTH_LOW_DEFAULT, \
#        length_high=LENGTH_HIGH_DEFAULT, stopwords_low=STOPWORDS_LOW_DEFAULT, \
#        stopwords_high=STOPWORDS_HIGH_DEFAULT, max_link_density=MAX_LINK_DENSITY_DEFAULT, no_headings=NO_HEADINGS_DEFAULT)
#    justext.revise_paragraph_classification(paragraphs, max_heading_distance=MAX_HEADING_DISTANCE_DEFAULT)
#    return paragraphs


#all unicode characters from 0x0000 - 0x0020 (33 total) are bad and will be replaced by "" (empty string)
#for line in fileinput.input(xmlInputFileLocation, inplace=1):
#    for pos in range(0,len(line)):
#        if unichr(line[pos]) < 32:
#            line[pos] = None
#    print u''.join([c for c in line if c])

# invalid_xml = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]')
# newdata, count = invalid_xml.subn('', data)

# reader = codecs.EncodedFile(xmlfile, 'utf8', 'utf8', 'replace')

# &#13;
