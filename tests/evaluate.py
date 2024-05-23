import argparse
from importlib.metadata import version
import json
import os
import sys
import time

import pandas as pd
from rouge_score import rouge_scorer

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

import comparison


class Evaluation():

    template_dict = {'true positives': 0,
                    'false positives': 0,
                    'true negatives': 0,
                    'false negatives': 0,
                    'time': 0,
                    'skipped_instances': 0}
    # algorithm string, package, function, results
    ALGORITHMS = {
        'everything': {'library': '-',
                       'function': comparison.run_everything,
                       'confusion_matrix': template_dict.copy()},
        'nothing': {'library': '-',
                       'function': comparison.run_nothing,
                       'confusion_matrix': template_dict.copy()},
        'baseline': {'library': '-',
                       'function': comparison.run_baseline,
                       'confusion_matrix': template_dict.copy()},
        'trafilatura': {'library': 'trafilatura',
                       'function': comparison.run_trafilatura,
                       'confusion_matrix': template_dict.copy()},
        'trafilatura + X': {'library': 'trafilatura',
                       'function': comparison.run_trafilatura_fallback,
                       'confusion_matrix': template_dict.copy()},
        'html2text': {'library': 'html2text',
                       'function': comparison.run_html2text,
                       'confusion_matrix': template_dict.copy()},
        'html_text': {'library': 'html_text',
                       'function': comparison.run_html_text,
                       'confusion_matrix': template_dict.copy()},
        'inscriptis': {'library': 'inscriptis',
                       'function': comparison.run_inscriptis,
                       'confusion_matrix': template_dict.copy()},
        'justext': {'library': 'justext',
                       'function': comparison.run_justext,
                       'confusion_matrix': template_dict.copy()},
        'goose': {'library': 'goose3',
                       'function': comparison.run_goose,
                       'confusion_matrix': template_dict.copy()},
        'newspaper': {'library': 'newspaper3k',
                       'function': comparison.run_newspaper,
                       'confusion_matrix': template_dict.copy()},
        'boilerpipe': {'library': 'boilerpy3',
                       'function': comparison.run_boilerpipe,
                       'confusion_matrix': template_dict.copy()},
        'newsplease': {'library': 'news-please',
                       'function': comparison.run_newsplease,
                       'confusion_matrix': template_dict.copy()},
        'readability': {'library': 'readability-lxml',
                       'function': comparison.run_readability,
                       'confusion_matrix': template_dict.copy()},
        'readabilipy': {'library': 'readabilipy',
                       'function': comparison.run_readabilipy,
                       'confusion_matrix': template_dict.copy()},
        'resiliparse': {'library': 'resiliparse',
                       'function': comparison.run_resiliparse,
                       'confusion_matrix': template_dict.copy()},
        'bs4': {'library': 'beautifulsoup4',
                       'function': comparison.run_bs4,
                       'confusion_matrix': template_dict.copy()},
        'trafilatura precision': {'library': 'trafilatura',
                       'function': comparison.run_trafilatura_precision,
                       'confusion_matrix': template_dict.copy()},
        'trafilatura recall': {'library': 'trafilatura',
                       'function': comparison.run_trafilatura_recall,
                       'confusion_matrix': template_dict.copy()}
        }

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
        # store algorithm predictions
        self.predictions = None  # TODO
        # compute results
        self.results = self.compute_results()
        # store results
        self.output_df = self.create_df()
        self.output_dir = output_dir
        if 'csv' in output:
            self.output_csv()
        if 'md' in output:
            self.output_md()
        # print scores
        self.print_scores()

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
        if type(data) == list:  # list of dicts
            pass
        elif type(data) == dict:  # nested dict
            pass
        return data

    def load_document_string(self, filename, test_dir=''):
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

    @staticmethod
    def load_html(directory, filename):
        pass

    def evaluate_result(self, result, item):
        '''evaluate result contents'''
        true_positives = 0
        false_negatives = 0
        false_positives = 0
        true_negatives = 0

        # handcrafted with/without strings
        if self.evaltype == 'chunks':
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
        # full article body in gold standard
        elif self.evaltype == 'fullstring':
            n_grams = None  # TODO ngram shingling
        return true_positives, false_negatives, false_positives, true_negatives

    def predict(self, dict_result, htmlstring):
        start = time.time()
        result = dict_result['function'](htmlstring)
        dict_result['confusion_matrix']['time'] += time.time() - start
        # skip empty strings
        # in nothing null hypothesis always empty string
        if not result and (dict_result['library'] != '-'):
            dict_result['confusion_matrix']['skipped_instances'] += 1
        return dict_result['confusion_matrix'], result

    def compute_confusion_matrix(self, dict_result, result, item):
        # TODO correlations between algorithms for instances?
        tp, fn, fp, tn = self.evaluate_result(result, item)
        dict_result['confusion_matrix']['true positives'] += tp
        dict_result['confusion_matrix']['false positives'] += fp
        dict_result['confusion_matrix']['true negatives'] += tn
        dict_result['confusion_matrix']['false negatives'] += fn
        return dict_result['confusion_matrix']

    def compute_rouge(self, pred, gold):
        # rouge longest common substring
        scorer = rouge_scorer.RougeScorer(['rougeLsum'],
                                          use_stemmer=False,
                                          split_summaries=True)
        return scorer.score(pred, gold)

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
        results = dict()
        for a in self.algorithms:
            results[a] = Evaluation.ALGORITHMS[a].copy()
        # iterate data, count true/false positives/negatives
        for _, item in self.test_data.items():
            if len(item['file']) == 0:
                continue
            htmlstring = self.load_document_string(item['file'],
                                                   test_dir='')
            if htmlstring is None:
                continue
            # counter
            i += 1
            for a in self.algorithms:
                # run algorithm
                try:
                    results[a]['confusion_matrix'], result = self.predict(
                        results[a], htmlstring)
                except Exception as e:
                    print(item['file'], e)
                    continue
                # compute confusion matrix
                results[a]['confusion_matrix'] = self.compute_confusion_matrix(
                    results[a], result, item)
                # rouge score
                if self.evaltype == 'fullstring' and 'rouge' in self.metrics:
                    self.compute_rouge()
        #  compute scores
        for a in self.algorithms:
            try:
                results[a]['scores'] = self.calculate_scores(
                    results[a]['confusion_matrix'])
            except ZeroDivisionError:
                print(a, results[a]['confusion_matrix'])
                results[a]['scores'] = tuple(0 for _ in self.metrics)
        return results

    def create_df(self):
        """results to pandas dataframe"""
        columns = ['algorithm', 'version'] + self.metrics + ['time difference']
        rows = []
        for algo in self.algorithms:
            # package version
            if Evaluation.ALGORITHMS[algo]['library'] != '-':
                algo_version = version(Evaluation.ALGORITHMS[algo]['library'])
            else:  # no library listed
                algo_version = '-'
            print(self.results[algo])
            results = self.results[algo]['scores']
            time_diff = self.results[algo]['confusion_matrix']['time'] / \
                self.results['baseline']['confusion_matrix']['time']
            row = [algo, algo_version] + list(results) + \
                [time_diff]
            rows.append(row)
        df = pd.DataFrame(rows, columns=columns)
        # algorithm name as index
        df.set_index('algorithm', inplace=True)
        # round floats
        float_columns = df.select_dtypes(include=['float']).columns
        df[float_columns] = df[float_columns].round(3)
        return df

    def output_csv(self, path='results.csv'):
        """save results to a csv file"""
        self.output_df.to_csv(self.output_dir + path)

    def output_md(self, path='results.md'):
        """save and print results in markdown format"""
        md = self.output_df.to_markdown()
        print(md)
        with open(self.output_dir + path, 'w') as f:
            f.write(md)

    def print_scores(self):
        """print results"""
        for algo, infos in self.results.items():
            print(algo)
            print(infos)
            print(f"time diff.: {self.output_df.loc[algo]['time difference']:.2f}")
            for m in self.metrics:
                print(f"{m}: {self.output_df.loc[algo][m]:.2f}")


def cmdparser():
    """Parse command line arguments"""
    # Command line arguments
    # script usage: python evaluate.py
    parser = argparse.ArgumentParser(description='Run an evaluation benchmark')
    parser.add_argument('--small', action='store_true', help='Evaluate trafilatura and baselines only.')
    parser.add_argument('--all', action='store_true', help='Evaluate all available algorithms.')
    # file path, metrics and algorithms as default
    parser.add_argument('--testfile', default='evaldata.json', help='File path to the test data.')
    parser.add_argument('--metrics', nargs='+', default=['precision', 'recall', 'accuracy', 'f1'],
                        help='Evaluation metrics, implemented: precision, recall, accuracy, f-score.')
    parser.add_argument('--algorithms',
                        nargs='+',
                        default=['trafilatura', 'trafilatura + X', 'everything', 'nothing', 'baseline'],
                        help='Further tools/algorithms to evaluate, implemented: .')
    # Print help and exit if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    # parse arguments
    return parser.parse_args()


if __name__ == '__main__':
    args = cmdparser()
    # minimum number of algorithms
    algorithms = ['trafilatura', 'trafilatura + X', 'everything', 'nothing',
                  'baseline']
    if not args.small:  # more algorithms given
        algorithms += args.algorithms
    if args.all:
        algorithms = Evaluation.ALGORITHMS.keys()
    test_file = args.testfile
    metrics = args.metrics
    eval = Evaluation(test_data='evaldata.json', html_dir='eval', algorithms=algorithms,
                      metrics=metrics, output=['csv', 'md'])
    print(eval.output_df)
