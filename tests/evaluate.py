"""
Make extraction results comparable with other libraries of the same kind.
"""

import argparse
import json
import logging
import os
import sys
import time

from importlib.metadata import version

import html2text
import html_text
import justext
import pandas as pd
import tqdm
# from rouge_score import rouge_scorer

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

from boilerpy3 import extractors
from bs4 import BeautifulSoup
from goose3 import Goose
from inscriptis import get_text
from magic_html import GeneralExtractor
from newspaper import fulltext
from newsplease import NewsPlease
# from readabilipy import simple_json_from_html_string
from readability import Document
from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import bytes_to_str, detect_encoding
from resiliparse.parse.html import HTMLTree

from trafilatura import baseline, extract, html2txt
from trafilatura.external import jt_stoplist_init

# custom
from justext.core import (ParagraphMaker, classify_paragraphs,
                          preprocessor, revise_paragraph_classification)
from trafilatura.baseline import basic_cleaning
from trafilatura.htmlprocessing import tree_cleaning, prune_unwanted_nodes
from trafilatura.readability_lxml import Document as ReadabilityDocument
from trafilatura.settings import Extractor
from trafilatura.utils import load_html, trim


boilerpipe_extractor = extractors.ArticleExtractor()  # ArticleExtractor DefaultExtractor LargestContentExtractor

g = Goose()

magic_html_extractor = GeneralExtractor()

JT_STOPLIST = jt_stoplist_init()

OPTIONS = Extractor()


def convert_to_str(htmlbinary):
    "Conversion and encoding fix for the tests."
    try:
        guessed_encoding = detect(htmlbinary)['encoding']
        htmlstring = htmlbinary.decode(guessed_encoding)
    except (TypeError, UnicodeDecodeError):
        htmlstring = htmlbinary
    return htmlstring


def run_custom(htmlbinary):
    tree = load_html(htmlbinary)
    #tree = preprocessor(tree)
    tree = basic_cleaning(tree)
    #tree = tree_cleaning(load_html(htmlbinary), OPTIONS)
    try:
        paragraphs = ParagraphMaker.make_paragraphs(tree)
        classify_paragraphs(paragraphs, JT_STOPLIST, 50, 150, 0.1, 0.2, 0.3, True)
        revise_paragraph_classification(paragraphs, 150)
        return " ".join([p.text for p in paragraphs if not p.is_boilerplate])
    except ValueError:
        return ""


def run_custom_2(htmlbinary):
    tree = tree_cleaning(load_html(htmlbinary), OPTIONS)
    try:
        doc = ReadabilityDocument(tree, min_text_length=25, retry_length=250)
        return doc.summary()
    except Exception as err:
        return ""


def run_baseline(htmlbinary):
    '''run bare text extraction within lxml'''
    _, result, _ = baseline(htmlbinary)
    return result


def run_html2txt(htmlbinary):
    '''run Trafilatura's html2txt function'''
    return html2txt(htmlbinary)


def run_trafilatura(htmlbinary):
    '''run trafilatura (without fallback) on content'''
    return extract(
        htmlbinary,
        no_fallback=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_justext(htmlbinary):
    '''try with the generic algorithm justext'''
    paragraphs = justext.justext(
                     htmlbinary, JT_STOPLIST,
                     50, 200, 0.1, 0.2, 0.2, 200, True
                 )  # stop_words
    valid = [
        paragraph.text
        for paragraph in paragraphs
        if not paragraph.is_boilerplate
    ]

    return ' '.join(valid)


def run_trafilatura_fallback(htmlbinary):
    '''run trafilatura (with fallback) on content'''
    return extract(
        htmlbinary,
        no_fallback=False,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_trafilatura_precision(htmlbinary):
    '''run trafilatura with preference for precision'''
    return extract(
        htmlbinary,
        no_fallback=False,
        favor_precision=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_trafilatura_recall(htmlbinary):
    '''run trafilatura with preference for recall'''
    return extract(
        htmlbinary,
        no_fallback=False,
        favor_recall=True,
        include_comments=False,
        include_tables=True,
        include_formatting=False,
    )


def run_goose(htmlbinary):
    '''try with the goose algorithm'''
    try:
        article = g.extract(raw_html=htmlbinary)
        return article.cleaned_text
    except ValueError:
        return ''


def run_readability(htmlbinary):
    '''try with the Python3 port of readability.js'''
    try:
        doc = Document(htmlbinary)
        return doc.summary()
    except Exception as err:
        print('Exception:', err)
        return ''


def run_inscriptis(htmlbinary):
    '''try with the inscriptis module'''
    # conversion necessary
    htmlstring = convert_to_str(htmlbinary)
    try:
        text = get_text(htmlstring)
    except TypeError:
        text = ''
    return text


def run_html2text(htmlbinary):
    '''try with the html2text module'''
    # conversion necessary
    htmlstring = convert_to_str(htmlbinary)
    try:
        text = html2text.html2text(htmlstring)
    except TypeError:
        text = ''
    return text


def run_html_text(htmlbinary):
    '''try with the html2text module'''
    # conversion necessary
    htmlstring = convert_to_str(htmlbinary)
    try:
        text = html_text.extract_text(htmlstring, guess_layout=False)
    except TypeError:
        text = ''
    return text


def run_newspaper(htmlstring):
    '''try with the newspaper module'''
    try:
        text = fulltext(htmlstring)
    except AttributeError:
        return ''
    return text


def run_boilerpipe(htmlbinary):
    '''try with the boilerpipe algorithm'''
    # conversion necessary
    htmlstring = convert_to_str(htmlbinary)
    try:
        content = boilerpipe_extractor.get_content(htmlstring)
    except Exception:
        content = ''
    return content


def run_newsplease(htmlbinary):
    '''try with newsplease'''
    try:
        article = NewsPlease.from_html(htmlbinary, url=None)
        return article.maintext
    except Exception as err:
        #print('Newsplease exception:', err)
        return ''


#def run_readabilipy(htmlstring):
#    '''try with the readability.py module'''
#    try:
#        article = simple_json_from_html_string(htmlstring, use_readability=True)
#        returnlist = [textelem['text'] for textelem in article['plain_text']]
#        return '\n'.join(returnlist)
#    except Exception as err:
#        #print('Readabilipy exception:', err)
#        return ''


def run_resiliparse(htmlbinary):
    '''try with the resiliparse package'''
    # necessary
    try:
        htmlstring = bytes_to_str(htmlbinary, detect_encoding(htmlbinary))
    except TypeError:  # already a string
        htmlstring = htmlbinary
    tree = HTMLTree.parse(htmlstring)
    return extract_plain_text(tree, main_content=True)


def run_bs4(htmlbinary):
    '''try with the BeautifulSoup module'''
    return BeautifulSoup(htmlbinary, features='lxml').get_text(strip=True)


def run_magic_html(htmlbinary):
    '''try with the magic_html package'''
    return run_bs4(magic_html_extractor.extract(convert_to_str(htmlbinary), base_url="").get("html"))


def run_nothing(htmlstring):
    return ''


def run_everything(htmlbinary):
    return convert_to_str(htmlbinary)


TEMPLATE_DICT = {
    'true positives': 0,
    'false positives': 0,
    'true negatives': 0,
    'false negatives': 0,
    'time': 0,
    'skipped_instances': 0
}

# algorithm string, package, function, results
ALGORITHMS = {
    'everything': {
        'library': '-',
        'function': run_everything
    },
    'nothing': {
        'library': '-',
        'function': run_nothing
    },
    'custom': {
        'library': '-',
        'function': run_custom
    },
    'baseline': {
        'library': '-',
        'function': run_baseline
    },
    'html2txt': {
        'library': '-',
        'function': run_html2txt
    },
    'trafilatura fast': {
        'library': 'trafilatura',
        'function': run_trafilatura
    },
    'trafilatura': {
        'library': 'trafilatura',
        'function': run_trafilatura_fallback
    },
    'html2text': {
        'library': 'html2text',
        'function': run_html2text
    },
    'html_text': {
        'library': 'html_text',
        'function': run_html_text
    },
    'inscriptis': {
        'library': 'inscriptis',
        'function': run_inscriptis
    },
    'justext': {
        'library': 'justext',
        'function': run_justext
    },
    'goose': {
        'library': 'goose3',
        'function': run_goose
    },
    'newspaper': {
        'library': 'newspaper3k',
        'function': run_newspaper
    },
    'boilerpipe': {
        'library': 'boilerpy3',
        'function': run_boilerpipe
    },
    'newsplease': {
        'library': 'news-please',
        'function': run_newsplease
    },
    'readability': {
        'library': 'readability-lxml',
        'function': run_readability
    },
    'resiliparse': {
        'library': 'resiliparse',
        'function': run_resiliparse
    },
    'bs4': {
        'library': 'beautifulsoup4',
        'function': run_bs4
    },
    'magic_html': {
        'library': 'magic_html',
        'function': run_magic_html
    },
    'trafilatura precision': {
        'library': 'trafilatura',
        'function': run_trafilatura_precision
    },
    'trafilatura recall': {
        'library': 'trafilatura',
        'function': run_trafilatura_recall
    }
}

# Initialize the confusion matrix for each algorithm
for algorithm in ALGORITHMS.values():
    algorithm['confusion_matrix'] = TEMPLATE_DICT.copy()


class Evaluation():
    __slots__ = (
        "algorithms", "evaltype", "html_dir", "metadata", "metrics",
        "output", "output_df", "output_dir", "results", "test_data"
    )

    def __init__(self,
                 test_data: str,
                 html_dir: str,
                 algorithms: list,
                 metrics: list=['precision', 'recall', 'accuracy', 'f1'],
                 output: list=['csv', 'md'],
                 output_dir: str='results/',
                 metadata: bool=False) -> None:
        self.test_data = self.read_data(test_data)
        self.html_dir = html_dir
        self.algorithms = algorithms
        self.metrics = metrics
        self.metadata = metadata
        self.output = output
        # compute results
        self.results = self.compute_results()
        # store results
        self.output_df = self.create_df()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if 'csv' in output:
            self.output_csv()
        if 'md' in output:
            self.output_md()
        # print scores
        self.print_scores()
        # evaluate metadata
        if self.evaltype == 'chunks':
            self.evaluate_authors()

    def read_data(self, path):
        """read test data set from a file path"""
        if path.endswith('json'):  # json file
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'with' in list(data.items())[0][1]:
                self.evaltype = 'chunks'
            # scrapinghub and andythefactory
            elif 'articleBody' in list(data.items())[0][1]:
                self.evaltype = 'fullstring'
        # list of dicts or nested dict (?)
        if isinstance(data, (list, dict)):
            pass
        return data

    def load_document_binary(self, filename, test_dir=''):
        '''load mock page from samples'''
        if not test_dir:
            test_dir = os.path.abspath(os.path.dirname(__file__))
        mypath = os.path.join(test_dir, 'cache', filename)
        if not os.path.isfile(mypath):
            mypath = os.path.join(test_dir, self.html_dir, filename)
        # html file missing
        if not os.path.exists(mypath):
            print('HTML file not found:', mypath)
            return None
        with open(mypath, 'rb') as inputf:
            htmlbinary = inputf.read()
        return htmlbinary

    def evaluate_result(self, result, item):
        '''evaluate result contents'''
        true_positives = false_negatives = false_positives = true_negatives = 0

        # handcrafted with/without strings
        if self.evaltype == 'chunks':
            # report if problematic
            if len(item['with']) == 0 or len(item['with']) > 6:
                print('counter', item)
            if len(item['without']) == 0 or len(item['without']) > 6:
                print('counter', item)
            # examine
            if result is not None and isinstance(result, str):
                true_positives = sum(1 for to_include in item['with'] if to_include in result)
                false_negatives = len(item['with']) - true_positives
                false_positives = sum(1 for to_exclude in item['without'] if to_exclude in result)
                true_negatives = len(item['without']) - false_positives
            # add up as bulk counts
            else:
                false_negatives += len(item['with'])
                true_negatives += len(item['without'])
        # full article body in gold standard
        elif self.evaltype == 'fullstring':
            n_grams = None  # TODO ngram shingling
        return true_positives, false_negatives, false_positives, true_negatives

    def predict(self, dict_result, htmlstring):
        """parse an html string with the algorithm"""
        start = time.time()
        try:
            result = dict_result['function'](htmlstring)
        except Exception:
            result = ""
        dict_result['confusion_matrix']['time'] += time.time() - start
        # skip empty strings
        # in nothing null hypothesis always empty string
        if not result and dict_result['library'] != '-':
            dict_result['confusion_matrix']['skipped_instances'] += 1
        return dict_result['confusion_matrix'], result

    def compute_confusion_matrix(self, dict_result, result, item):
        """compute tp, fn, fp, tn for a dataset instance"""
        # TODO correlations between algorithms for instances?
        tp, fn, fp, tn = self.evaluate_result(result, item)
        dict_result['confusion_matrix']['true positives'] += tp
        dict_result['confusion_matrix']['false positives'] += fp
        dict_result['confusion_matrix']['true negatives'] += tn
        dict_result['confusion_matrix']['false negatives'] += fn
        return dict_result['confusion_matrix']

    #def compute_rouge(self, pred, gold):
    #    """compute rouge score between prediction and gold answer"""
    #    # TODO
    #    # rouge longest common substring
    #    scorer = rouge_scorer.RougeScorer(['rougeLsum'],
    #                                      use_stemmer=False,
    #                                      split_summaries=True)
    #    return scorer.score(pred, gold)

    @staticmethod
    def calculate_scores(mydict):
        '''output weighted result score'''
        tp, fn, fp, tn = mydict['true positives'], mydict['false negatives'], \
            mydict['false positives'], mydict['true negatives']
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        accuracy = (tp+tn)/(tp+tn+fp+fn)
        fscore = (2*tp)/(2*tp + fp + fn)
        return precision, recall, accuracy, fscore

    def compute_results(self):
        """compute results of all algorithms on the test dataset"""
        i = 0
        # intialize results dictionary
        results = {a: ALGORITHMS[a].copy() for a in self.algorithms}
        # iterate data, count true/false positives/negatives
        with tqdm.tqdm(total=len(self.test_data)) as pbar:
            for item in self.test_data.values():
                pbar.update(1)
                if not item['file']:
                    continue
                htmlbinary = self.load_document_binary(item['file'], test_dir='')
                if not htmlbinary:
                    continue
                i += 1
                for a in self.algorithms:
                    # run algorithm
                    try:
                        results[a]['confusion_matrix'], result = self.predict(results[a], htmlbinary)
                    except Exception as e:
                        print(item['file'], e)
                        continue
                    # compute confusion matrix
                    results[a]['confusion_matrix'] = self.compute_confusion_matrix(results[a], result, item)
                    # rouge score
                    #if self.evaltype == 'fullstring' and 'rouge' in self.metrics:
                    #    self.compute_rouge()
        print(f"{i} from {len(self.test_data)} files read")
        # compute scores
        for a in self.algorithms:
            try:
                results[a]['scores'] = self.calculate_scores(results[a]['confusion_matrix'])
            except ZeroDivisionError:
                print(a, results[a]['confusion_matrix'])
                results[a]['scores'] = tuple(0 for _ in self.metrics)
        return results

    def create_df(self):
        """results to pandas dataframe"""
        columns = ['algorithm', 'version'] + self.metrics + ['time difference',
                                                             'skipped instances']
        rows = []
        for algo in self.algorithms:
            algo_version = version(ALGORITHMS[algo]['library']) if ALGORITHMS[algo]['library'] != '-' else '-'
            results = self.results[algo]['scores']
            time_diff = self.results[algo]['confusion_matrix']['time'] / \
                self.results['baseline']['confusion_matrix']['time']
            row = [algo, algo_version] + list(results) + \
                [time_diff, self.results[algo]['confusion_matrix']['skipped_instances']]
            rows.append(row)
        df = pd.DataFrame(rows, columns=columns)
        # algorithm name as index
        df.set_index('algorithm', inplace=True)
        df = df.round(3)
        return df

    def output_csv(self, path='results.csv'):
        self.output_df.to_csv(os.path.join(self.output_dir, path))

    def output_md(self, path='results.md'):
        with open(os.path.join(self.output_dir, path), 'w', encoding="utf-8") as f:
            f.write(self.output_df.to_markdown())

    def print_scores(self):
        """print results"""
        print()
        separator = " | "
        for algo in self.results:
            print(algo)
            result = separator.join([f"{m}: {self.output_df.loc[algo][m]:.3f}" for m in self.metrics])
            print(result, f"time: {self.output_df.loc[algo]['time difference']:.2f}", sep=separator)
            print()

    def evaluate_authors(self):
        # TODO
        pass


def cmdparser():
    """Parse command line arguments"""
    # Command line arguments
    # script usage:
    # Trafilatura evaluation: python evaluate.py --small
    # full evaluation: python evaluate.py --all
    parser = argparse.ArgumentParser(description='Run an evaluation benchmark')
    parser.add_argument('--small', action='store_true', help='Evaluate trafilatura and baselines only.')
    parser.add_argument('--all', action='store_true', help='Evaluate all available algorithms.')
    # file path, metrics and algorithms as default
    parser.add_argument('--testfile', default='evaldata.json', help='File path to the test data.')
    parser.add_argument('--metrics', nargs='+', default=['precision', 'recall', 'accuracy', 'f1'],
                        help='Evaluation metrics, implemented: precision, recall, accuracy, f-score.')
    parser.add_argument('--algorithms',
                        nargs='+',
                        default=['everything', 'nothing', 'baseline'],
                        help=f'Algorithms to evaluate, implemented: {list(ALGORITHMS)}.')
    parser.add_argument('--verbose', action='store_true', help='increase verbosity')
    # print help and exit if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    # parse arguments
    return parser.parse_args()


if __name__ == '__main__':
    args = cmdparser()

    if not args.verbose:
        logging.basicConfig(level=logging.CRITICAL)

    algorithms = ['everything', 'nothing', 'baseline']
    if args.small:
        algorithms += ['trafilatura fast', 'trafilatura']
    elif args.all:
        algorithms = list(ALGORITHMS)
    else:
        algorithms += args.algorithms
        algorithms = sorted(set(algorithms))

    evaluation = Evaluation(test_data=args.testfile, html_dir='eval', algorithms=algorithms, metrics=args.metrics, output=['csv', 'md'])
