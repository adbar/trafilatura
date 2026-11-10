"""CI quality gate: fails if own-benchmark F1 regresses below the pinned floors.

No competitor-extractor deps (unlike evaluate.py), so it's cheap to run in CI.
eval_baseline.json pins the floors plus a digest of evaldata.json and every
resolved HTML input — many double as unit-test mock pages in cache/, so a
refresh there would otherwise change scores unnoticed. eval_meta_baseline.json
pins the metadata floors: the share of annotated values matched by
extract_metadata. After editing either, re-pin with ``--update``: it re-pins
the corpus but refuses to lower a floor without ``--allow-regression``.
"""

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_common import (
    RUNNERS,
    ConfusionMatrix,
    load_evaldata,
    norm,
    read_corpus,
    report_first_error,
    run_and_count,
    validate,
)

from trafilatura.json_metadata import AUTHOR_SPLIT
from trafilatura.metadata import extract_metadata
from trafilatura.utils import load_html

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE_PATH = os.path.join(HERE, "eval_baseline.json")
META_BASELINE_PATH = os.path.join(HERE, "eval_meta_baseline.json")
# fields with enough annotations, empty gold values are not annotated and skipped
META_FIELDS = ("title", "author", "date", "tags", "categories")

# one flipped segment moves F1 by ~0.0002; don't fail on measurement noise
EPSILON = 0.0005


def measured_f1(cm: ConfusionMatrix) -> float:
    "F1 at the floors' grain."
    return round(cm.f1(), 4)


def regressed(f1: float, floor: float) -> bool:
    "Below the floor by more than measurement noise."
    return f1 < floor - EPSILON


def load_baseline(path: str | None = None) -> dict[str, Any]:
    with open(path or BASELINE_PATH, encoding="utf-8") as f:
        baseline: dict[str, Any] = json.load(f)
    return baseline


def save_baseline(baseline: dict[str, Any], path: str | None = None) -> None:
    "Atomic replace, so an interrupted --update can't truncate the pins."
    path = path or BASELINE_PATH
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def corpus_sha(docs: dict[str, tuple[str, bytes]]) -> str:
    "Digest annotations + every resolved HTML input, so a mock-page refresh trips the gate too."
    hashsum = hashlib.sha256()
    with open(os.path.join(HERE, "evaldata.json"), "rb") as f:
        hashsum.update(f.read())
    for relpath, htmlbinary in docs.values():
        hashsum.update(relpath.encode())
        hashsum.update(htmlbinary)
    return hashsum.hexdigest()


def corpus_pins(evaldata: dict[str, dict[str, Any]], docs: dict[str, tuple[str, bytes]]) -> dict[str, Any]:
    "Corpus fingerprint: the SHA records 'corpus seen', the counts make a shrink reviewable."
    return {
        "evaldata_sha": corpus_sha(docs),
        "entries": len(evaldata),
        "chunks": [
            sum(len(item["with"]) for item in evaldata.values()),
            sum(len(item["without"]) for item in evaldata.values()),
        ],
    }


def score(evaldata: dict[str, dict[str, Any]], docs: dict[str, tuple[str, bytes]]) -> dict[str, ConfusionMatrix]:
    matrices = {name: ConfusionMatrix() for name in RUNNERS}
    reported: set[str] = set()  # runners whose first exception was printed
    for url, item in evaldata.items():
        relpath, htmlbinary = docs[url]
        for name, fn in RUNNERS.items():
            _, counts, err = run_and_count(fn, htmlbinary, item)
            if err is not None:
                report_first_error(reported, name, relpath, err)
            matrices[name].add(counts)
    return matrices


def meta_values(field: str, value: Any) -> list[str]:
    "Comparable form: case- and whitespace-insensitive, authors and lists as sorted items."
    if not value:
        return []
    if field == "author":
        value = AUTHOR_SPLIT.split("; ".join(value) if isinstance(value, list) else value)
    elif not isinstance(value, list):
        value = [value]
    return sorted(item for item in (norm(v).casefold() for v in value) if item)


def meta_scores(evaldata: dict[str, dict[str, Any]], docs: dict[str, tuple[str, bytes]]) -> dict[str, float]:
    "Share of annotated values matched, per metadata field."
    hits: Counter[str] = Counter()
    totals: Counter[str] = Counter()
    reported: set[str] = set()
    for url, item in evaldata.items():
        gold = {field: meta_values(field, item.get(field)) for field in META_FIELDS}
        if not any(gold.values()):
            continue
        tree = load_html(docs[url][1])
        try:
            metadata = extract_metadata(tree, default_url=url) if tree is not None else None
        except Exception as err:
            report_first_error(reported, "metadata", docs[url][0], err)
            metadata = None
        for field, expected in gold.items():
            if expected:
                totals[field] += 1
                hits[field] += expected == meta_values(field, getattr(metadata, field, None))
    return {field: round(hits[field] / max(totals[field], 1), 4) for field in META_FIELDS}


def repin_meta(measured: dict[str, float], allow_regression: bool = False) -> int:
    "Rewrite the metadata floors unless that lowers one, returns the exit code."
    floors = load_baseline(META_BASELINE_PATH)["floors"] if os.path.exists(META_BASELINE_PATH) else {}
    drops = [
        f"meta {name}: {measured[name]:.4f} vs floor {floors[name]:.4f}"
        for name in measured
        if name in floors and regressed(measured[name], floors[name])
    ]
    if drops and not allow_regression:
        print("\n".join(["refusing to lower a metadata floor:", *drops]))
        return 1
    save_baseline({"floors": measured}, META_BASELINE_PATH)
    print(f"re-pinned metadata floors={measured}")
    return 0


def repin(
    baseline: dict[str, Any],
    matrices: dict[str, ConfusionMatrix],
    pins: dict[str, Any],
    allow_regression: bool = False,
) -> int:
    "Rewrite the corpus pins and, unless that lowers a floor, the floors; returns the exit code."
    measured = {name: measured_f1(cm) for name, cm in matrices.items()}
    floors = baseline["floors"]
    drops = [
        f"{name}: F1={f1:.4f} vs floor {floors[name]:.4f} ({f1 - floors[name]:+.4f})"
        for name, f1 in measured.items()
        if name in floors and regressed(f1, floors[name])
    ]

    baseline.update(pins)
    if not drops or allow_regression:
        baseline["floors"] = measured
    save_baseline(baseline)

    if drops and not allow_regression:
        print("\n".join(["re-pinned the corpus only — refusing to lower the floor:", *drops]))
        print("fix the regression, or re-run with --update --allow-regression to accept the lower bar")
        return 1
    print(f"re-pinned floors={measured} sha={pins['evaldata_sha']}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="re-measure and re-pin eval_baseline.json")
    parser.add_argument("--allow-regression", action="store_true", help="let --update lower a pinned floor")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    evaldata = load_evaldata(HERE)
    validate(evaldata)
    baseline = load_baseline()

    docs = read_corpus(HERE, evaldata)
    pins = corpus_pins(evaldata, docs)
    if not args.update:
        if {key: baseline.get(key) for key in pins} != pins:
            sys.exit("corpus changed (annotations or HTML) — re-measure and re-pin:\n    python tests/eval_gate.py --update")
        if set(RUNNERS) != set(baseline["floors"]):
            sys.exit("runners and pinned floors disagree — re-pin:\n    python tests/eval_gate.py --update")
        meta_floors = load_baseline(META_BASELINE_PATH)["floors"]
        if set(META_FIELDS) != set(meta_floors):
            sys.exit("metadata fields and pinned floors disagree — re-pin:\n    python tests/eval_gate.py --update")

    matrices = score(evaldata, docs)
    meta = meta_scores(evaldata, docs)
    if args.update:
        code = repin(baseline, matrices, pins, allow_regression=args.allow_regression)
        return code | repin_meta(meta, allow_regression=args.allow_regression)

    regression = False
    for name, cm in matrices.items():
        f1, floor = measured_f1(cm), baseline["floors"][name]
        regression = regression or regressed(f1, floor)
        print(f"{name:>9}: F1={f1:.4f} (floor {floor:.4f})")
    for field, value in meta.items():
        regression = regression or regressed(value, meta_floors[field])
        print(f"{field:>10}: {value:.4f} (floor {meta_floors[field]:.4f})")
    return int(regression)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
