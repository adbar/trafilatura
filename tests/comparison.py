"""
Compare extraction results with other libraries of the same kind.
"""

# import logging
import os
import re
import time

from lxml import etree, html

try:
    import cchardet as chardet
except ImportError:
    import chardet

import html2text
import justext
from boilerpy3 import extractors
from dragnet import extract_content #, extract_content_and_comments
from goose3 import Goose
from inscriptis import get_text
from jparser import PageModel
# from libextract.api import extract as lib_extract
from newspaper import fulltext
from newsplease import NewsPlease
from readability import Document
from trafilatura import extract
## add to tests?
# https://github.com/nikitautiu/learnhtml
## TODO: time, best of 3

from evaldata import EVAL_PAGES
from trafilatura.utils import sanitize

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

boilerpipe_extractor = extractors.DefaultExtractor()  # ArticleExtractor DefaultExtractor LargestContentExtractor

g = Goose()


def load_document(filename):
    '''load mock page from samples'''
    mypath = os.path.join(TEST_DIR, 'cache', filename)
    if not os.path.isfile(mypath):
        mypath = os.path.join(TEST_DIR, 'eval', filename)
    try:
        with open(mypath, 'r') as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(mypath, 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = chardet.detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    return htmlstring


def run_trafilatura(htmlstring):
    '''run trafilatura (without fallback) on content'''
    result = extract(htmlstring, no_fallback=True, include_comments=False, include_tables=True)
    return result # sanitize(result)


def run_justext(htmlstring):
    '''try with the generic algorithm justext'''
    valid = list()
    paragraphs = justext.justext(htmlstring, justext.get_stoplist("German"))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            valid.append(paragraph.text)
    result = ' '.join(valid)
    return result # sanitize(result)


def run_trafilatura_fallback(htmlstring):
    '''run trafilatura (with fallback) on content'''
    result = extract(htmlstring, no_fallback=False, include_comments=False, include_tables=True)
    return result # sanitize(result)


def run_goose(htmlstring):
    '''try with the goose algorithm'''
    article = g.extract(raw_html=htmlstring)
    return article.cleaned_text # sanitize(article.cleaned_text)


def run_readability(htmlstring):
    '''try with the Python3 port of readability.js'''
    try:
        doc = Document(htmlstring)
        return doc.summary() # sanitize(doc.summary())
    except Exception as err:
        print('Exception:', err)
        return ''

def run_inscriptis(htmlstring):
    '''try with the inscriptis module'''
    text = get_text(htmlstring)
    return text # sanitize(text)


def run_html2text(htmlstring):
    '''try with the html2text module'''
    text = html2text.html2text(htmlstring)
    return text # sanitize(text)


def run_newspaper(htmlstring):
    '''try with the newspaper module'''
    try:
        text = fulltext(htmlstring) # sanitize(fulltext(htmlstring))
    except AttributeError:
        return ''
    return text


def run_dragnet(htmlstring):
    '''try with the dragnet module'''
    content = extract_content(htmlstring)
    return content # sanitize(content)


def run_boilerpipe(htmlstring):
    '''try with the boilerpipe algorithm'''
    try:
        content = boilerpipe_extractor.get_content(htmlstring)
        # sanitize(boilerpipe_extractor.get_content(htmlstring))
    except:
        content = ''
    return content


def run_newsplease(htmlstring):
    '''try with newsplease'''
    try:
        article = NewsPlease.from_html(htmlstring, url=None)
        return article.maintext # sanitize(article.maintext)
    except Exception as err:
        print('Exception:', err)
        return ''

def run_jparser(htmlstring):
    '''try with jparser'''
    try:
        pm = PageModel(htmlstring)
    except ValueError:
        return ''
    result = pm.extract()
    mylist = list()
    for x in result['content']:
        if x['type'] in ('text', 'html'):
            mylist.append(str(x['data']))
    returnstring = ' '.join(mylist)
    # returnstring = re.sub(r'\s+', ' ', returnstring)
    returnstring = re.sub(r'\s+(p{P}+)', '\1', returnstring)
    return sanitize(returnstring)


#def run_libextract(htmlstring):
#    '''try with the libextract module'''
#    textlist = list()
#    for textnode in list(lib_extract(htmlstring)):
#        textlist.append(textnode.text_content())
#    textcontent = '\n'.join(textlist)
#    return contextcontenttent


def evaluate_result(result, item):
    '''evaluate result contents'''
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    true_negatives = 0
    for to_include in item['with']:
        if len(to_include) == 0:
            print(item)
        if result is not None:
            if to_include in result:
                true_positives += 1
            else:
                false_negatives += 1
        else:
            false_negatives += 1
    for to_exclude in item['without']:
        if result is not None:
            if to_exclude in result:
                false_positives += 1
            else:
                true_negatives += 1
        else:
            true_negatives += 1
    return true_positives, false_negatives, false_positives, true_negatives


def calculate_scores(mydict):
    '''output weighted result score'''
    tp, fn, fp, tn = mydict['true positives'], mydict['false negatives'], mydict['false positives'], mydict['true negatives']
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    fscore = (2*tp)/(2*tp + fp + fn)  # 2*((precision*recall)/(precision+recall))
    return precision, recall, accuracy, fscore


template_dict = {'true positives': 0, 'false positives': 0, 'true negatives': 0, 'false negatives': 0, 'time': 0}
everything, nothing, trafilatura_result, justext_result, trafilatura_X_result, goose_result, readability_result, inscriptis_result, newspaper_result, html2text_result, dragnet_result, boilerpipe_result, newsplease_result, jparser_result = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
everything.update(template_dict)
nothing.update(template_dict)
trafilatura_result.update(template_dict)
justext_result.update(template_dict)
trafilatura_X_result.update(template_dict)
goose_result.update(template_dict)
readability_result.update(template_dict)
inscriptis_result.update(template_dict)
newspaper_result.update(template_dict)
html2text_result.update(template_dict)
dragnet_result.update(template_dict)
boilerpipe_result.update(template_dict)
newsplease_result.update(template_dict)
jparser_result.update(template_dict)


i = 0

for item in EVAL_PAGES:
    if len(EVAL_PAGES[item]['file']) == 0:
        continue
    htmlstring = load_document(EVAL_PAGES[item]['file'])
    # null hypotheses
    tp, fn, fp, tn = evaluate_result('', EVAL_PAGES[item])
    nothing['true positives'] += tp
    nothing['false positives'] += fp
    nothing['true negatives'] += tn
    nothing['false negatives'] += fn
    tp, fn, fp, tn = evaluate_result(htmlstring, EVAL_PAGES[item])
    everything['true positives'] += tp
    everything['false positives'] += fp
    everything['true negatives'] += tn
    everything['false negatives'] += fn
    # html2text
    start = time.time()
    result = run_html2text(htmlstring)
    html2text_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    html2text_result['true positives'] += tp
    html2text_result['false positives'] += fp
    html2text_result['true negatives'] += tn
    html2text_result['false negatives'] += fn
    # inscriptis
    start = time.time()
    result = run_inscriptis(htmlstring)
    inscriptis_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    inscriptis_result['true positives'] += tp
    inscriptis_result['false positives'] += fp
    inscriptis_result['true negatives'] += tn
    inscriptis_result['false negatives'] += fn
    # trafilatura
    start = time.time()
    result = run_trafilatura(htmlstring)
    trafilatura_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    trafilatura_result['true positives'] += tp
    trafilatura_result['false positives'] += fp
    trafilatura_result['true negatives'] += tn
    trafilatura_result['false negatives'] += fn
    # justext
    start = time.time()
    result = run_justext(htmlstring)
    justext_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    justext_result['true positives'] += tp
    justext_result['false positives'] += fp
    justext_result['true negatives'] += tn
    justext_result['false negatives'] += fn
    # trafilatura + X
    start = time.time()
    result = run_trafilatura_fallback(htmlstring)
    trafilatura_X_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    trafilatura_X_result['true positives'] += tp
    trafilatura_X_result['false positives'] += fp
    trafilatura_X_result['true negatives'] += tn
    trafilatura_X_result['false negatives'] += fn
    # readability
    start = time.time()
    result = run_readability(htmlstring)
    readability_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    readability_result['true positives'] += tp
    readability_result['false positives'] += fp
    readability_result['true negatives'] += tn
    readability_result['false negatives'] += fn
    # goose
    start = time.time()
    result = run_goose(htmlstring)
    goose_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    goose_result['true positives'] += tp
    goose_result['false positives'] += fp
    goose_result['true negatives'] += tn
    goose_result['false negatives'] += fn
    # newspaper
    start = time.time()
    result = run_newspaper(htmlstring)
    newspaper_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    newspaper_result['true positives'] += tp
    newspaper_result['false positives'] += fp
    newspaper_result['true negatives'] += tn
    newspaper_result['false negatives'] += fn
    # dragnet
    start = time.time()
    result = run_dragnet(htmlstring)
    dragnet_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    dragnet_result['true positives'] += tp
    dragnet_result['false positives'] += fp
    dragnet_result['true negatives'] += tn
    dragnet_result['false negatives'] += fn
    # boilerpipe
    start = time.time()
    result = run_boilerpipe(htmlstring)
    boilerpipe_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    boilerpipe_result['true positives'] += tp
    boilerpipe_result['false positives'] += fp
    boilerpipe_result['true negatives'] += tn
    boilerpipe_result['false negatives'] += fn
    # newsplease
    start = time.time()
    result = run_newsplease(htmlstring)
    newsplease_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    newsplease_result['true positives'] += tp
    newsplease_result['false positives'] += fp
    newsplease_result['true negatives'] += tn
    newsplease_result['false negatives'] += fn
    # jparser
    start = time.time()
    result = run_jparser(htmlstring)
    jparser_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    jparser_result['true positives'] += tp
    jparser_result['false positives'] += fp
    jparser_result['true negatives'] += tn
    jparser_result['false negatives'] += fn
    i += 1

print('number of documents:', i)
print('nothing')
print(nothing)
# print(calculate_f_score(nothing))
print('everything')
print(everything)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(everything)))

print('html2text')
print(html2text_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(html2text_result)))
print('inscriptis')
print(inscriptis_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(inscriptis_result)))

print('justext')
print(justext_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(justext_result)))

print('goose')
print(goose_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(goose_result)))

print('newspaper')
print(newspaper_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(newspaper_result)))

print('dragnet')
print(dragnet_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(dragnet_result)))

print('boilerpipe')
print(boilerpipe_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(boilerpipe_result)))

print('newsplease')
print(newsplease_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(newsplease_result)))

print('readability')
print(readability_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(readability_result)))

print('jparser')
print(jparser_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(jparser_result)))

print('trafilatura')
print(trafilatura_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_result)))

print('trafilatura + X')
print(trafilatura_X_result)
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_X_result)))
