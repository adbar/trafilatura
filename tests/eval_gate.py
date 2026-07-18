"""CI quality gate: fail if the own-benchmark F1-score regresses below baseline.

Run from the repo root: ``python tests/eval_gate.py``. Self-contained (only
depends on trafilatura, not on evaluate.py's heavy multi-extractor imports) so
the gate doesn't drag competitor-extractor dependencies into CI.

Reproducibility: pinned to ``tests/evaldata.json`` at the commit that sets
FLOORS below (any corpus edit that changes matched chunks moves the score and
must re-pin). Scorer matches evaluate.py: whitespace-normalized substring
match, both sides, deterministic given the corpus and extractor code.
"""

import json
import os
import re
import sys

from trafilatura import extract

HERE = os.path.dirname(os.path.abspath(__file__))

# current full-corpus baseline; no regression allowed
FLOORS = {"fast": 0.9204, "fallback": 0.9273}


def load_evaldata():
    with open(os.path.join(HERE, "evaldata.json"), encoding="utf-8") as f:
        return json.load(f)


def resolve(filename):
    "cache/ before eval/, matching evaluate.py's load_document_binary."
    for subdir in ("cache", "eval"):
        path = os.path.join(HERE, subdir, filename)
        if os.path.isfile(path):
            return path
    return None


def norm(text):
    "whitespace-normalize so ws variants don't cost recall (evaluate.py parity)."
    return re.sub(r"\s+", " ", text).strip()


def run_fast(htmlbinary):
    return extract(htmlbinary, fast=True, include_comments=False, include_tables=True, include_formatting=False)


def run_fallback(htmlbinary):
    return extract(htmlbinary, fast=False, include_comments=False, include_tables=True, include_formatting=False)


RUNNERS = {"fast": run_fast, "fallback": run_fallback}


def count_item(item, result):
    "Per-item (tp, fp, fn, tn) with whitespace-normalized substring matching."
    if result and isinstance(result, str):
        resn = norm(result)
        tp = sum(1 for w in item["with"] if norm(w) in resn)
        fp = sum(1 for w in item["without"] if norm(w) in resn)
    else:
        tp = fp = 0
    return tp, fp, len(item["with"]) - tp, len(item["without"]) - fp


def score_function(func, evaldata):
    tp = fp = fn = 0
    for item in evaldata.values():
        path = resolve(item["file"])
        if path is None:
            continue
        try:
            result = func(open(path, "rb").read())
        except Exception:
            result = None
        t, f, n, _ = count_item(item, result)
        tp, fp, fn = tp + t, fp + f, fn + n
    return 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0


def main():
    evaldata = load_evaldata()
    regression = False
    for name, func in RUNNERS.items():
        score, floor = round(score_function(func, evaldata), 4), FLOORS[name]
        regression = regression or score < floor
        print(f"{name:>9}: F1={score:.4f} (floor {floor:.4f})")
    return int(regression)


if __name__ == "__main__":
    sys.exit(main())
