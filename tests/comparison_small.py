"""
Compare extraction results with other libraries of the same kind.
"""

import logging
import os
import re
import sys
import time

from lxml import html  # etree

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

# import justext
# from readability import Document

from evaldata import EVAL_PAGES # ADDITIONAL_PAGES as EVAL_PAGES


from trafilatura import extract
try:
    from trafilatura import baseline, html2txt
except ImportError:
    print("Cannot import baseline, using simple version")
    baseline = None
    html2txt = None
#from trafilatura.htmlprocessing import prune_html
#from trafilatura.external import ReadabilityDocument, custom_justext, jt_stoplist_init
#from trafilatura.external import try_readability, sanitize_tree, custom_justext, jt_stoplist_init
#from trafilatura.utils import load_html, sanitize
#from trafilatura.xml import xmltotxt

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)  # logging.WARNING

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

#JT_STOPLIST = jt_stoplist_init()


def trim(string):
    '''Remove unnecessary spaces within a text string'''
    if string is not None:
        # delete newlines that are not related to punctuation or markup
        # string = re.sub(r'(?<![p{P}>])\n', ' ', string)
        # proper trimming
        string = ' '.join(re.split(r'\s+', string.strip(' \t\n\r'), flags=re.UNICODE|re.MULTILINE))
        string = string.strip()
    return string


def load_document_binary(filename):
    '''load mock page from samples'''
    mypath = os.path.join(TEST_DIR, 'cache', filename)
    if not os.path.isfile(mypath):
        mypath = os.path.join(TEST_DIR, 'eval', filename)
    #if not os.path.isfile(mypath):
    #    mypath = os.path.join(TEST_DIR, 'additional', filename)
    with open(mypath, 'rb') as inputf:
        htmlstring = inputf.read()
    return htmlstring


def load_document_string(filename):
    '''load mock page from samples'''
    mypath = os.path.join(TEST_DIR, 'cache', filename)
    if not os.path.isfile(mypath):
        mypath = os.path.join(TEST_DIR, 'eval', filename)
    #if not os.path.isfile(mypath):
    #    mypath = os.path.join(TEST_DIR, 'additional', filename)
    try:
        with open(mypath, 'r', encoding="utf-8") as inputf:
            htmlstring = inputf.read()
    # encoding/windows fix for the tests
    except UnicodeDecodeError:
        # read as binary
        with open(mypath, 'rb') as inputf:
            htmlbinary = inputf.read()
        guessed_encoding = detect(htmlbinary)['encoding']
        if guessed_encoding is not None:
            try:
                htmlstring = htmlbinary.decode(guessed_encoding)
            except UnicodeDecodeError:
                htmlstring = htmlbinary
        else:
            print('Encoding error')
    return htmlstring


def run_html2txt(htmlstring):
    if html2txt is not None:
        return html2txt(htmlstring)
    return ''


def run_baseline_2(htmlstring):
    '''run bare text extraction within lxml'''
    # binary/string as input tweak
    try:
        tree = html.fromstring(htmlstring)
    except ValueError:
        tree = html.fromstring(htmlstring.encode('utf8'))
    result = None
    # try json-ld
    for elem in tree.xpath('//script[@type="application/ld+json"]'):
        if elem.text and '"articleBody":' in elem.text:
            mymatch = re.search(r'"articleBody":"(.+?)","', elem.text)
            if mymatch:
                result = mymatch.group(1)
                result = result.replace('\\"', '"')
                # result = trim(result)
                break
    if result is not None:
        return result
    #results = set()
    resultlist = []
    # iterate potentially relevant elements
    for element in tree.iter('blockquote', 'code', 'p', 'pre', 'q'): # 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        #if element.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        #    if not element.text or len(element.text) < 20:
        #        continue
        #    entry = element.text
        #else:
        entry = element.text_content()
        #if entry not in results and len(entry) > 10:
        resultlist.append(entry)
        #results.add(entry)
    # if nothing has been found
    #if len(resultlist) < 1:
    #    for element in tree.iter('b', 'em', 'i', 'strong'):
    #        entry = element.text_content()
    #        #if entry not in results: # and len(entry) > 15:
    #        resultlist.append(entry)
    #        #results.add(entry)
    #if len(resultlist) == 0:
    #    cleaned_tree = HTML_CLEANER.clean_html(tree)
    #    for element in tree.iter('div'):
    #        entry = element.text_content()
            #if len(entry) > 15:
    #        resultlist.append(entry)
    #        #results.add(entry)
    #print(len(resultlist))
    result = '\n'.join(resultlist)
    # result = sanitize(result)
    # print(result)
    return result


def run_baseline(htmlstring):
    '''run bare text extraction within lxml'''
    if baseline is not None:
        _, result, _ = baseline(htmlstring)
        return result
    return run_baseline_2(htmlstring)


def run_trafilatura(htmlstring):
    '''run trafilatura (without fallback) on content'''
    result = extract(htmlstring, no_fallback=True, include_comments=False, include_tables=True, include_formatting=False) # , deduplicate=False
    return result


#def run_justext(htmlstring):
#    '''try with the generic algorithm justext'''
#    valid = list()
#    # paragraphs = justext.justext(htmlstring, stop_words, 50, 200, 0.1, 0.2, 0.5, 200, True)  # stop_words
#    tree = load_html(htmlstring)
#    try:
#        paragraphs = custom_justext(tree, JT_STOPLIST)
#        for paragraph in [p for p in paragraphs if not p.is_boilerplate]:
#            valid.append(paragraph.text)
#    except UnicodeDecodeError:
#        pass
#    return sanitize(' '.join(valid))


def run_trafilatura_fallback(htmlstring):
    '''run trafilatura (with fallback) on content'''
    result = extract(htmlstring, no_fallback=False, include_comments=False, include_tables=True, include_formatting=False) # , deduplicate=False
    return result


def run_trafilatura_precision(htmlstring):
    '''run trafilatura with preference for precision'''
    result = extract(htmlstring, no_fallback=False, favor_precision=True, include_comments=False, include_tables=True, include_formatting=False) # , deduplicate=False
    return result


def run_trafilatura_recall(htmlstring):
    '''run trafilatura with preference for recall'''
    result = extract(htmlstring, no_fallback=False, favor_recall=True, include_comments=False, include_tables=True, include_formatting=False) # , deduplicate=False
    return result


#def run_readability(htmlstring):
#    '''try with the Python3 port of readability.js'''
#    try:
#        #doc = Document(htmlstring)
#        cleaned_tree, text, _ = sanitize_tree(try_readability(load_html(htmlstring))
#        return text
#        #return xmltotxt(cleaned_tree, False, False)
#    except Exception as err:
#        print('Exception:', err)
#        return ''


def evaluate_result(result, item):
    '''evaluate result contents'''
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    true_negatives = 0
    # report if problematic
    if len(item['with']) == 0 or len(item['with']) > 6:
        print('counter', item)
    if len(item['without']) == 0 or len(item['without']) > 6:
        print('counter', item)
    # internal report
    #if result is None:
    #    print('None', item['file'])
    #elif type(result) is not str:
    #    print('not str', item['file'])
    # examine
    if result is not None and isinstance(result, str):
        # expected output
        for to_include in item['with']:
            if to_include in result:
                true_positives += 1
            else:
                false_negatives += 1
        # unwanted output
        for to_exclude in item['without']:
            if to_exclude in result:
                false_positives += 1
            else:
                true_negatives += 1
    # add up as bulk counts
    else:
        false_negatives += len(item['with'])
        true_negatives += len(item['without'])

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
everything, nothing, html2txt_result, baseline_result, trafilatura_result, justext_result, trafilatura_fallback_result, trafilatura_precision, trafilatura_recall, readability_result = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
nothing.update(template_dict)
everything.update(template_dict)
html2txt_result.update(template_dict)
baseline_result.update(template_dict)
trafilatura_result.update(template_dict)
justext_result.update(template_dict)
trafilatura_fallback_result.update(template_dict)
trafilatura_precision.update(template_dict)
trafilatura_recall.update(template_dict)
readability_result.update(template_dict)


i = 0

for item in EVAL_PAGES:
    if len(EVAL_PAGES[item]['file']) == 0:
        continue
    # print(EVAL_PAGES[item]['file'])
    htmlstring = load_document_binary(EVAL_PAGES[item]['file'])
    if htmlstring is None:
        continue
    # null hypotheses
    tp, fn, fp, tn = evaluate_result('', EVAL_PAGES[item])
    nothing['true positives'] += tp
    nothing['false positives'] += fp
    nothing['true negatives'] += tn
    nothing['false negatives'] += fn
    #tp, fn, fp, tn = evaluate_result(htmlstring, EVAL_PAGES[item])
    #everything['true positives'] += tp
    #everything['false positives'] += fp
    #everything['true negatives'] += tn
    #everything['false negatives'] += fn
    # bare html2txt
    #start = time.time()
    #result = run_html2txt(htmlstring)
    #html2txt_result['time'] += time.time() - start
    #tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    #html2txt_result['true positives'] += tp
    #html2txt_result['false positives'] += fp
    #html2txt_result['true negatives'] += tn
    #html2txt_result['false negatives'] += fn
    # bare lxml
    # if baseline is not None:
    start = time.time()
    result = run_baseline(htmlstring)
    baseline_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    baseline_result['true positives'] += tp
    baseline_result['false positives'] += fp
    baseline_result['true negatives'] += tn
    baseline_result['false negatives'] += fn
    # trafilatura
    start = time.time()
    result = run_trafilatura(htmlstring)
    trafilatura_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    trafilatura_result['true positives'] += tp
    trafilatura_result['false positives'] += fp
    trafilatura_result['true negatives'] += tn
    trafilatura_result['false negatives'] += fn
    # justext / jparser
    #start = time.time()
    #result = run_justext(htmlstring)
    #justext_result['time'] += time.time() - start
    #tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    #justext_result['true positives'] += tp
    #justext_result['false positives'] += fp
    #justext_result['true negatives'] += tn
    #justext_result['false negatives'] += fn
    # trafilatura + fallback
    start = time.time()
    result = run_trafilatura_fallback(htmlstring)
    trafilatura_fallback_result['time'] += time.time() - start
    tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    trafilatura_fallback_result['true positives'] += tp
    trafilatura_fallback_result['false positives'] += fp
    trafilatura_fallback_result['true negatives'] += tn
    trafilatura_fallback_result['false negatives'] += fn
    # trafilatura + precision
    #start = time.time()
    #result = run_trafilatura_precision(htmlstring)
    #trafilatura_precision['time'] += time.time() - start
    #tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    #trafilatura_precision['true positives'] += tp
    #trafilatura_precision['false positives'] += fp
    #trafilatura_precision['true negatives'] += tn
    #trafilatura_precision['false negatives'] += fn
    # trafilatura + recall
    #start = time.time()
    #result = run_trafilatura_recall(htmlstring)
    #trafilatura_recall['time'] += time.time() - start
    #tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    #trafilatura_recall['true positives'] += tp
    #trafilatura_recall['false positives'] += fp
    #trafilatura_recall['true negatives'] += tn
    #trafilatura_recall['false negatives'] += fn
    # readability
    #start = time.time()
    #result = run_readability(htmlstring)
    #readability_result['time'] += time.time() - start
    #tp, fn, fp, tn = evaluate_result(result, EVAL_PAGES[item])
    #readability_result['true positives'] += tp
    #readability_result['false positives'] += fp
    #readability_result['true negatives'] += tn
    #readability_result['false negatives'] += fn
    i += 1


print('number of documents:', i)
print('nothing')
print(nothing)
# print(calculate_f_score(nothing))
#print('everything')
#print(everything)
# print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(everything)))

#print('html2txt')
#print(html2txt_result)
#try:
#    print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(html2txt_result)))
#except ZeroDivisionError:
#    pass

print('baseline')
print(baseline_result)
try:
    print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(baseline_result)))
except ZeroDivisionError:
    pass

print('trafilatura')
print(trafilatura_result)
print("time diff.: %.2f" % (trafilatura_result['time'] / baseline_result['time']))
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_result)))

#print('Justext')
#print(justext_result)
#print("time diff.: %.2f" % (justext_result['time'] / baseline_result['time']))
#print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(justext_result)))

print('trafilatura + fallback')
print(trafilatura_fallback_result)
print("time diff.: %.2f" % (trafilatura_fallback_result['time'] / baseline_result['time']))
print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_fallback_result)))

#print('trafilatura precision')
#print(trafilatura_precision)
#print("time diff.: %.2f" % (trafilatura_precision['time'] / baseline_result['time']))
#print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_precision)))
#print('trafilatura recall')
#print(trafilatura_recall)
#print("time diff.: %.2f" % (trafilatura_recall['time'] / baseline_result['time']))
#print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(trafilatura_recall)))

#print('readability')
#print(readability_result)
#print("time diff.: %.2f" % (readability_result['time'] / baseline_result['time']))
#print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % (calculate_scores(readability_result)))
