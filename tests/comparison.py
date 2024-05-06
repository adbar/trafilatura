"""
Compare extraction results with other libraries of the same kind.
"""

# import logging
import csv
import os
import re
import time

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

import html2text
import html_text
import justext
from boilerpy3 import extractors
from bs4 import BeautifulSoup
from goose3 import Goose
from inscriptis import get_text
from newspaper import fulltext
from newsplease import NewsPlease
from readabilipy import simple_json_from_html_string
from readability import Document
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import bytes_to_str, detect_encoding
from resiliparse.parse.html import HTMLTree

from trafilatura import extract

try:
    from trafilatura import baseline
except ImportError:
    print("Cannot import baseline, using simple version")
    baseline = None
from evaldata import EVAL_PAGES

# from trafilatura.utils import sanitize

## TODO: time, best of 3

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

boilerpipe_extractor = extractors.ArticleExtractor()  # ArticleExtractor DefaultExtractor LargestContentExtractor

g = Goose()


def trim(string):
    '''Remove unnecessary spaces within a text string'''
    if string is not None:
        string = ' '.join(re.split(r'\s+', string.strip(' \t\n\r'), flags=re.UNICODE|re.MULTILINE))
        string = string.strip()
    return string


def load_document_binary(filename):
    '''load mock page from samples'''
    mypath = os.path.join(TEST_DIR, 'cache', filename)
    if not os.path.isfile(mypath):
        mypath = os.path.join(TEST_DIR, 'eval', filename)
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


def run_baseline(htmlstring):
    '''run bare text extraction within lxml'''
    _, result, _ = baseline(htmlstring)
    return result


def run_trafilatura(htmlstring):
    '''run trafilatura (without fallback) on content'''
    return extract(
        htmlstring,
        no_fallback=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_justext(htmlstring):
    '''try with the generic algorithm justext'''
    paragraphs = justext.justext(htmlstring, justext.get_stoplist("German"),
                                 50, 200, 0.1, 0.2, 0.2, 200, True)  # stop_words
    valid = [
        paragraph.text
        for paragraph in paragraphs
        if not paragraph.is_boilerplate
    ]

    return ' '.join(valid)   # sanitize(result)


def run_trafilatura_fallback(htmlstring):
    '''run trafilatura (with fallback) on content'''
    return extract(
        htmlstring,
        no_fallback=False,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_trafilatura_precision(htmlstring):
    '''run trafilatura with preference for precision'''
    return extract(
        htmlstring,
        no_fallback=False,
        favor_precision=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_trafilatura_recall(htmlstring):
    '''run trafilatura with preference for recall'''
    return extract(
        htmlstring,
        no_fallback=False,
        favor_recall=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_goose(htmlstring):
    '''try with the goose algorithm'''
    try:
        article = g.extract(raw_html=htmlstring)
        return article.cleaned_text  # sanitize(article.cleaned_text)
    except ValueError:
        return ''


def run_readability(htmlstring):
    '''try with the Python3 port of readability.js'''
    try:
        doc = Document(htmlstring)
        return doc.summary()  # sanitize(doc.summary())
    except Exception as err:
        print('Exception:', err)
        return ''

def run_inscriptis(htmlstring):
    '''try with the inscriptis module'''
    try:
        text = get_text(htmlstring)
    except TypeError:
        text = ''
    return text # sanitize(text)


def run_html2text(htmlstring):
    '''try with the html2text module'''
    try:
        text = html2text.html2text(htmlstring)
        # sanitize(text)
    except TypeError:
        text = ''
    return text


def run_html_text(htmlstring):
    '''try with the html2text module'''
    try:
        text = html_text.extract_text(htmlstring, guess_layout=False)
    except TypeError:
        text = ''
    return text


def run_newspaper(htmlstring):
    '''try with the newspaper module'''
    try:
        text = fulltext(htmlstring)  # sanitize(fulltext(htmlstring))
    except AttributeError:
        return ''
    return text


def run_boilerpipe(htmlstring):
    '''try with the boilerpipe algorithm'''
    try:
        content = boilerpipe_extractor.get_content(htmlstring)
        # sanitize(boilerpipe_extractor.get_content(htmlstring))
    except Exception:
        content = ''
    return content


def run_newsplease(htmlstring):
    '''try with newsplease'''
    try:
        article = NewsPlease.from_html(htmlstring, url=None)
        return article.maintext # sanitize(article.maintext)
    except Exception as err:
        #print('Newsplease exception:', err)
        return ''


def run_readabilipy(htmlstring):
    '''try with the readability.py module'''
    try:
        article = simple_json_from_html_string(htmlstring, use_readability=True)
        returnlist = [textelem['text'] for textelem in article['plain_text']]
        return '\n'.join(returnlist) # sanitize(content)
    except Exception as err:
        #print('Readabilipy exception:', err)
        return ''


def run_resiliparse(htmlstring):
    '''try with the resiliparse package'''
    try:
        decoded = bytes_to_str(htmlstring, detect_encoding(htmlstring))
    except TypeError:  # already a string
        decoded = htmlstring
    tree = HTMLTree.parse(decoded)
    return extract_plain_text(tree, main_content=True)


def run_bs4(htmlstring):
    '''try with the BeautifulSoup module'''
    return BeautifulSoup(htmlstring, features='lxml').get_text(strip=True)


def run_nothing(htmlstring):
    return ''


def run_everything(htmlstring):
    return htmlstring


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
    tp, fn, fp, tn = mydict['true positives'], mydict['false negatives'], \
        mydict['false positives'], mydict['true negatives']
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    fscore = (2*tp)/(2*tp + fp + fn)  # 2*((precision*recall)/(precision+recall))
    return precision, recall, accuracy, fscore


def compute_confusion_matrix(run_function, dict_result, htmlstring, item):
    # TODO correlations between algorithms for instances?
    start = time.time()
    result = run_function(htmlstring)
    dict_result['time'] += time.time() - start
    if result:  # empty string returned
        tp, fn, fp, tn = evaluate_result(result, item)
        dict_result['true positives'] += tp
        dict_result['false positives'] += fp
        dict_result['true negatives'] += tn
        dict_result['false negatives'] += fn
    else:
        dict_result['skipped_instances'] += 1
    return dict_result


def run_comparison(small: bool = False, output_csv: bool = True,
                   output_md: bool = True):
    algorithms = {'nothing': [],
                  'everything': [],
                  'baseline': [run_baseline]}
    # save all results to a dictionary
    results_all = dict()
    template_dict = {'true positives': 0,
                    'false positives': 0,
                    'true negatives': 0,
                    'false negatives': 0,
                    'time': 0,
                    'skipped_instances': 0}
    # initialize result dictionaries
    nothing, everything, baseline_result, trafilatura_result, justext_result, \
        trafilatura_fallback_result, trafilatura_precision, trafilatura_recall, \
            goose_result, readability_result, inscriptis_result, \
                newspaper_result, html2text_result, html_text_result, \
                    boilerpipe_result, newsplease_result, readabilipy_result, \
                        resiliparse_result, bs4_result = (template_dict.copy()
                                                          for i in range(19)) 

    i = 0

    for item in EVAL_PAGES:
        if len(EVAL_PAGES[item]['file']) == 0:
            continue
        htmlstring = load_document_string(EVAL_PAGES[item]['file'])
        if htmlstring is None:
            continue
        # counter
        i += 1
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
        # baseline, bare lxml
        baseline_result = compute_confusion_matrix(run_baseline, baseline_result, htmlstring, EVAL_PAGES[item])
        # trafilatura
        trafilatura_result = compute_confusion_matrix(run_trafilatura, trafilatura_result, htmlstring, EVAL_PAGES[item])
        # trafilatura + X
        trafilatura_fallback_result = compute_confusion_matrix(run_trafilatura_fallback, trafilatura_fallback_result, htmlstring, EVAL_PAGES[item])
        if small == True:  # only include null hypotheses, trafilatura
            continue

        # html2text
        html2text_result = compute_confusion_matrix(run_html2text, html2text_result, htmlstring, EVAL_PAGES[item])
        # html_text
        html_text_result = compute_confusion_matrix(run_html_text, html_text_result, htmlstring, EVAL_PAGES[item])
        # inscriptis
        inscriptis_result = compute_confusion_matrix(run_inscriptis, inscriptis_result, htmlstring, EVAL_PAGES[item])
        # justext
        justext_result = compute_confusion_matrix(run_justext, justext_result, htmlstring, EVAL_PAGES[item])
        # trafilatura + precision
        trafilatura_precision = compute_confusion_matrix(run_trafilatura_precision, trafilatura_precision, htmlstring, EVAL_PAGES[item])
        # trafilatura + recall
        trafilatura_recall = compute_confusion_matrix(run_trafilatura_recall, trafilatura_recall, htmlstring, EVAL_PAGES[item])
        # readability
        readability_result = compute_confusion_matrix(run_readability, readability_result, htmlstring, EVAL_PAGES[item])
        # goose
        goose_result = compute_confusion_matrix(run_goose, goose_result, htmlstring, EVAL_PAGES[item])
        # newspaper
        newspaper_result = compute_confusion_matrix(run_newspaper, newspaper_result, htmlstring, EVAL_PAGES[item])
        # boilerpipe
        boilerpipe_result = compute_confusion_matrix(run_boilerpipe, boilerpipe_result, htmlstring, EVAL_PAGES[item])
        # newsplease
        newsplease_result = compute_confusion_matrix(run_newsplease, newsplease_result, htmlstring, EVAL_PAGES[item])
        # readabilipy
        readabilipy_result = compute_confusion_matrix(run_readabilipy, readabilipy_result, htmlstring, EVAL_PAGES[item])
        # resiliparse
        resiliparse_result = compute_confusion_matrix(run_resiliparse, resiliparse_result, htmlstring, EVAL_PAGES[item])
        # bs4
        bs4_result = compute_confusion_matrix(run_bs4, bs4_result, htmlstring, EVAL_PAGES[item])


    print('number of documents:', i)
    print('nothing')
    print(nothing)
    print('everything')
    print(everything)
    everything_scores = (calculate_scores(everything))
    print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % everything_scores)
    results_all['everything'] = everything_scores

    print('baseline')
    print(baseline_result)
    try:
        baseline_scores = (calculate_scores(baseline_result))
        print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % baseline_scores)
        results_all['baseline'] = baseline_scores
    except ZeroDivisionError:
        pass

    def print_scores(result_str, result_dict):
        print(result_str)
        print(result_dict)
        print(f"time diff.: {result_dict['time'] / baseline_result['time']:.2f}")
        scores = (calculate_scores(result_dict))
        print("precision: %.3f recall: %.3f accuracy: %.3f f-score: %.3f" % scores)
        results_all[result_str] = scores

    print_scores('trafilatura', trafilatura_result)
    print_scores('trafilatura + X', trafilatura_fallback_result)
    if not small:
        print_scores('html2text', html2text_result)
        print_scores('html_text', html_text_result)
        print_scores('inscriptis', inscriptis_result)
        print_scores('justext', justext_result)
        print_scores('goose', goose_result)
        print_scores('newspaper', newspaper_result)
        print_scores('boilerpipe', boilerpipe_result)
        print_scores('newsplease', newsplease_result)
        print_scores('readability', readability_result)
        print_scores('readabilipy', readabilipy_result)
        print_scores('resiliparse', resiliparse_result)
        print_scores('bs4', bs4_result)
        print_scores('trafilatura precision', trafilatura_precision)
        print_scores('trafilatura recall', trafilatura_recall)

    print(results_all)
    column_names = ['algorithm', 'precision', 'recall', 'accuracy', 'f-score']
    if output_csv:
        with open('results.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(column_names)
            for algorithm, results in results_all.items():
                writer.writerow([algorithm, results[0], results[1], results[2], results[3]])
    if output_md:
        md = '| ' + ' | '.join(column_names) + ' |\n'
        md += '|:---:|:---:|:---:|:---:|:---:|\n'
        for algorithm, results in results_all.items():
            md += f'| {algorithm} | {results[0]} | {results[1]} | {results[2]} | {results[3]} |\n'
        with open('results.md', 'w', encoding='utf-8') as f:
            f.write(md)
        print(md)


if __name__ == '__main__':
    # TODO argparse for algorithm choice
    small = True
    run_comparison(small=small)
