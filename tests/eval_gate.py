"""CI quality gate: fails if own-benchmark F1 regresses below the pinned floors.

No competitor-extractor deps (unlike evaluate.py), so it's cheap to run in CI.
eval_baseline.json pins the floors plus a digest of evaldata.json and every
resolved HTML input — many double as unit-test mock pages in cache/, so a
refresh there would otherwise change scores unnoticed. After editing either,
re-pin with ``--update``: it re-pins the corpus but refuses to lower a floor
without ``--allow-regression``.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_common import RUNNERS, ConfusionMatrix, load_evaldata, read_corpus, report_first_error, run_and_count, validate

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE_PATH = os.path.join(HERE, "eval_baseline.json")

# one flipped segment moves F1 by ~0.0002; don't fail on measurement noise
EPSILON = 0.0005


def measured_f1(cm: ConfusionMatrix) -> float:
    "F1 at the floors' grain."
    return round(cm.f1(), 4)


def regressed(f1: float, floor: float) -> bool:
    "Below the floor by more than measurement noise."
    return f1 < floor - EPSILON


def load_baseline() -> dict[str, Any]:
    with open(BASELINE_PATH, encoding="utf-8") as f:
        baseline: dict[str, Any] = json.load(f)
    return baseline


def save_baseline(baseline: dict[str, Any]) -> None:
    "Atomic replace, so an interrupted --update can't truncate the pins."
    tmp = BASELINE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)
        f.write("\n")
    os.replace(tmp, BASELINE_PATH)


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

    matrices = score(evaldata, docs)
    if args.update:
        return repin(baseline, matrices, pins, allow_regression=args.allow_regression)

    regression = False
    for name, cm in matrices.items():
        f1, floor = measured_f1(cm), baseline["floors"][name]
        regression = regression or regressed(f1, floor)
        print(f"{name:>9}: F1={f1:.4f} (floor {floor:.4f})")
    return int(regression)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
