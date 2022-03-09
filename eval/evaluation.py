#!/usr/bin/env python3
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import re
import statistics
from typing import Any, Dict, Tuple, List


def main():
    """ Perform evaluation for all ``output/*.json`` files,
    loading ground truth from ``groud-truth.json``.
    Python3.6+ is required.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-bootstrap', type=int, default=1000)
    parser.add_argument('--bootstrap-differences', action='store_true',
                        help='run bootstrap for differences')
    parser.add_argument('--output', type=Path, help='output results as json')
    args = parser.parse_args()
    ground_truth = load_json(Path('benchmark/ground/output_pzh.json'))
    metrics_by_name = {}
    path = Path('benchmark/cleaned/result_pzh.json')
    name = path.stem
    print(load_json(path, encoding='gbk'))
    metrics = evaluate(ground_truth, load_json(path, encoding='gbk'), args.n_bootstrap)
    print('{name:<20} '
          'precision={precision:.3f} ± {precision_std:.3f}  '
          'recall={recall:.3f} ± {recall_std:.3f}  '
          'F1={f1:.3f} ± {f1_std:.3f} '
          'accuracy={accuracy:.3f} ± {accuracy_std:.3f} '
          .format(name=name, **metrics))
    metrics_by_name[name] = metrics

    if args.bootstrap_differences:
        # check differences with bootstrap
        for name, metrics in sorted(metrics_by_name.items()):
            tp_fp_fns = metrics['tp_fp_fns']
            for other_name, other_metrics in sorted(metrics_by_name.items()):
                if name >= other_name:
                    continue
                print(f'Comparison: {name} minus {other_name}')
                other_tp_fp_fns = other_metrics['tp_fp_fns']
                print_metrics_diff(tp_fp_fns, other_tp_fp_fns, args.n_bootstrap)

    if args.output:
        args.output.write_text(
            json.dumps(metrics_by_name, indent=4, sort_keys=True))


def evaluate(
        ground_truth: Dict[str, Dict],
        prediction: Dict[str, Dict],
        n_bootstrap: int,
        ) -> Dict[str, Any]:
    if ground_truth.keys() != prediction.keys():
        raise ValueError('prediction keys do not match ground truth')
    tp_fp_fns = []
    accuracies = []
    for key in ground_truth.keys():
        true = ground_truth[key].get('articleBody', '')
        pred = prediction[key].get('articleBody', '')
        tp_fp_fns.append(string_shingle_matching(true=true, pred=pred))
        accuracies.append(get_accuracy(true=true, pred=pred))
    metrics: Dict[str, Any] = metrics_from_tp_fp_fns(tp_fp_fns)
    metrics['tp_fp_fns'] = tp_fp_fns
    metrics['accuracy'] = statistics.mean(accuracies)

    # add bootstrap estimates of condifence intervals
    b_values: Dict[str, List[float]] = {}
    for _ in range(n_bootstrap):
        n = len(tp_fp_fns)
        indices = [random.randint(0, n - 1) for _ in range(n)]
        b_metrics = metrics_from_tp_fp_fns([tp_fp_fns[i] for i in indices])
        for key in b_metrics:
            b_values.setdefault(key, []).append(b_metrics[key])
        b_values.setdefault('accuracy', []).append(
            statistics.mean([accuracies[i] for i in indices]))
    for key, values in sorted(b_values.items()):
        metrics[f'{key}_std'] = statistics.stdev(values)

    return metrics


def print_metrics_diff(tp_fp_fns, other_tp_fp_fns, n_bootstrap):
    diffs = {}
    for _ in range(n_bootstrap):
        n = len(tp_fp_fns)
        indices = [random.randint(0, n - 1) for _ in range(n)]
        metrics = metrics_from_tp_fp_fns([tp_fp_fns[i] for i in indices])
        other_metrics = metrics_from_tp_fp_fns(
            [other_tp_fp_fns[i] for i in indices])
        for key in metrics:
            diffs.setdefault(key, []).append(metrics[key] - other_metrics[key])
    for key, values in sorted(diffs.items()):
        mean = statistics.mean(values)
        std = statistics.stdev(values)
        print(f'{key:<10} {mean:.3f} ± {std:.3f}')


TP_FP_FN = Tuple[float, float, float]


def metrics_from_tp_fp_fns(tp_fp_fns: List[TP_FP_FN]) -> Dict[str, float]:
    precision = statistics.mean([
        precision_score(tp, fp, fn) for tp, fp, fn in tp_fp_fns
        if tp + fp > 0])
    recall = statistics.mean([
        recall_score(tp, fp, fn) for tp, fp, fn in tp_fp_fns
        if tp + fn > 0])
    f1 = 2 * precision * recall / (precision + recall)
    return {
        'f1': f1,
        'precision': precision,
        'recall': recall,
    }


def precision_score(tp: float, fp: float, fn: float) -> float:
    if fp == fn == 0:
        return 1.
    if tp == fp == 0:
        return 0.
    return tp / (tp + fp)


def recall_score(tp: float, fp: float, fn: float) -> float:
    if fp == fn == 0:
        return 1.
    if tp == fn == 0:
        return 0.
    return tp / (tp + fn)


def get_accuracy(true: str, pred: str) -> float:
    return float(_tokenize(true) == _tokenize(pred))


def string_shingle_matching(
        true: str, pred: str, ngram_n: int = 4,
        ) -> TP_FP_FN:
    """ Compute TP/FP/FN across shingles (joined ngrams).
    Intended to be used for articleBody comparison,
    similar to the one used here (with shingles instead of tokens):
    https://moz.com/devblog/benchmarking-python-content-extraction-algorithms-dragnet-readability-goose-and-eatiht/
    """
    true_shingles = _all_shingles(true, ngram_n)
    pred_shingles = _all_shingles(pred, ngram_n)
    tp = fp = fn = 0.
    for key in (set(true_shingles) | set(pred_shingles)):
        true_count = true_shingles.get(key, 0)
        pred_count = pred_shingles.get(key, 0)
        tp += min(true_count, pred_count)
        fp += max(0, pred_count - true_count)
        fn += max(0, true_count - pred_count)
    tp_fp_fn = [tp, fp, fn]
    s = sum(tp_fp_fn)
    # Normalize metrics so that longer texts do not have more weight.
    if s > 0:
        tp_fp_fn = [x / s for x in tp_fp_fn]
    return tuple(tp_fp_fn)  # type: ignore


def _all_shingles(text: str, ngram_n: int) -> Dict[Tuple[str, ...], int]:
    return dict(Counter(_ngrams(text, ngram_n)))


_TOKEN_RE = re.compile(
    r'\w+', re.UNICODE | re.MULTILINE | re.IGNORECASE | re.DOTALL)


def _tokenize(text: str) -> List[str]:
    # Note that such simple tokenization will work ok for any language,
    # even if several words will be clumped together, as we expect
    # that extra predicted text will still be separated.
    return _TOKEN_RE.findall(text or '')


def _ngrams(text: str, n: int) -> List[Tuple[str, ...]]:
    tokens = _tokenize(text)
    result = []
    for i in range(0, max(1, len(tokens) - n + 1)):
        shingle = tuple(tokens[i: i + n])
        if shingle:
            result.append(shingle)
    return result


def load_json(path: Path, encoding='utf-8'):
    with path.open('rt', encoding=encoding) as f:
        return json.load(f)


if __name__ == '__main__':
    main()
