import argparse
import json
import logging
import os
import sys
import time

from importlib.metadata import version

import pandas as pd
import tqdm
# from rouge_score import rouge_scorer

try:
    from cchardet import detect
except ImportError:
    from charset_normalizer import detect

import comparison


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
        'function': comparison.run_everything
    },
    'nothing': {
        'library': '-',
        'function': comparison.run_nothing
    },
    'baseline': {
        'library': '-',
        'function': comparison.run_baseline
    },
    'trafilatura fast': {
        'library': 'trafilatura',
        'function': comparison.run_trafilatura
    },
    'trafilatura': {
        'library': 'trafilatura',
        'function': comparison.run_trafilatura_fallback
    },
    'html2text': {
        'library': 'html2text',
        'function': comparison.run_html2text
    },
    'html_text': {
        'library': 'html_text',
        'function': comparison.run_html_text
    },
    'inscriptis': {
        'library': 'inscriptis',
        'function': comparison.run_inscriptis
    },
    'justext': {
        'library': 'justext',
        'function': comparison.run_justext
    },
    'goose': {
        'library': 'goose3',
        'function': comparison.run_goose
    },
    'newspaper': {
        'library': 'newspaper3k',
        'function': comparison.run_newspaper
    },
    'boilerpipe': {
        'library': 'boilerpy3',
        'function': comparison.run_boilerpipe
    },
    'newsplease': {
        'library': 'news-please',
        'function': comparison.run_newsplease
    },
    'readability': {
        'library': 'readability-lxml',
        'function': comparison.run_readability
    },
    'resiliparse': {
        'library': 'resiliparse',
        'function': comparison.run_resiliparse
    },
    'bs4': {
        'library': 'beautifulsoup4',
        'function': comparison.run_bs4
    },
    'trafilatura precision': {
        'library': 'trafilatura',
        'function': comparison.run_trafilatura_precision
    },
    'trafilatura recall': {
        'library': 'trafilatura',
        'function': comparison.run_trafilatura_recall
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
        with open(mypath, 'rb') as inputf:
            htmlbinary = inputf.read()
        # encoding fix for the tests
        try:
            guessed_encoding = detect(htmlbinary)['encoding']
            htmlstring = htmlbinary.decode(guessed_encoding)
        except (TypeError, UnicodeDecodeError):
            htmlstring = htmlbinary
        return htmlstring

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
                htmlstring = self.load_document_string(item['file'], test_dir='')
                if not htmlstring:
                    continue
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
