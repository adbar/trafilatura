"""Shared scoring primitives for evaluate.py and eval_gate.py.

Needs trafilatura but no competitor library, so eval_gate can import it
without evaluate.py's heavy deps.
"""

import json
import os
import re
from dataclasses import dataclass
from functools import partial
from typing import Any, TypedDict

from trafilatura import extract


class _ExtractOpts(TypedDict):
    "Typed so editors and local mypy catch a renamed extract() keyword; CI checks trafilatura only."

    include_comments: bool
    include_tables: bool
    include_formatting: bool


# canonical trafilatura settings, shared so gate and benchmarks can't drift apart
EXTRACT_OPTS: _ExtractOpts = {"include_comments": False, "include_tables": True, "include_formatting": False}


# canonical trafilatura runners, shared so the CI gate can't drift from the benchmark
RUNNERS = {
    "fast": partial(extract, fast=True, **EXTRACT_OPTS),
    "fallback": partial(extract, fast=False, **EXTRACT_OPTS),
}


def load_evaldata(path: str) -> dict[str, dict[str, Any]]:
    "Load the corpus annotations from path, or from path/evaldata.json if path is a directory."
    if os.path.isdir(path):
        path = os.path.join(path, "evaldata.json")
    with open(path, encoding="utf-8") as f:
        data: dict[str, dict[str, Any]] = json.load(f)
    return data


def norm(text: str) -> str:
    "Whitespace-normalize so ws variants don't cost recall."
    return re.sub(r"\s+", " ", text).strip()


# annotation bound per side, keeps single documents from dominating the scores
MAX_CHUNKS = 6


def validate(evaldata: Any) -> None:
    "Fail loudly on a malformed corpus edit."
    if not isinstance(evaldata, dict) or not evaldata:
        raise ValueError("unrecognized corpus format: expected a non-empty dict of annotations")
    for url, item in evaldata.items():
        if not item.get("file"):
            raise ValueError(f"{url}: missing or empty 'file'")
        for key in ("with", "without"):
            chunks = item.get(key)
            if not isinstance(chunks, list) or not all(isinstance(c, str) and c.strip() for c in chunks):
                raise ValueError(f"{url}: {key!r} must be a list of non-empty strings")
            if not 0 < len(chunks) <= MAX_CHUNKS:
                raise ValueError(f"{url}: {key!r} must hold 1 to {MAX_CHUNKS} chunks, found {len(chunks)}")
            if len({norm(c) for c in chunks}) != len(chunks):
                raise ValueError(f"{url}: duplicate entry in {key!r}")
        # a 'without' chunk contained in a 'with' chunk can never be scored as a true negative
        withs = [norm(w) for w in item["with"]]
        for without in map(norm, item["without"]):
            if any(without in w for w in withs):
                raise ValueError(f"{url}: {without[:50]!r} in 'without' also occurs inside 'with'")


def resolve(here: str, filename: str) -> str | None:
    "Find filename under here/cache or here/eval; None if neither exists."
    for subdir in ("cache", "eval"):
        path = os.path.join(here, subdir, filename)
        if os.path.isfile(path):
            return path
    return None


def read_document(here: str, filename: str) -> bytes | None:
    "Read the binary content of a corpus file; None if it can't be found."
    path = resolve(here, filename)
    if path is None:
        return None
    with open(path, "rb") as f:
        return f.read()


def read_corpus(here: str, evaldata: dict[str, dict[str, Any]]) -> dict[str, tuple[str, bytes]]:
    "Read every resolved HTML input once; returns {url: (posix relpath, bytes)}."
    docs = {}
    for url in sorted(evaldata):
        path = resolve(here, evaldata[url]["file"])
        if path is None:
            raise ValueError(f"{url}: HTML file not found: {evaldata[url]['file']}")
        # records which copy won the cache/eval lookup; posix, so the pin isn't OS-dependent
        relpath = os.path.relpath(path, here).replace(os.sep, "/")
        with open(path, "rb") as f:
            docs[url] = (relpath, f.read())
    return docs


def count_item(item: dict[str, Any], result: str | None) -> tuple[int, int, int, int]:
    "Per-item (tp, fp, fn, tn) via whitespace-normalized substring matching."
    if isinstance(result, str):
        resn = norm(result)
        tp = sum(1 for w in item["with"] if norm(w) in resn)
        fp = sum(1 for w in item["without"] if norm(w) in resn)
    else:
        tp = fp = 0
    return tp, fp, len(item["with"]) - tp, len(item["without"]) - fp


def report_first_error(reported: set[str], name: str, label: str, err: BaseException) -> None:
    "Print a runner's first exception only; a crash already costs recall, this names it."
    if name not in reported:
        reported.add(name)
        print(f"{name}: {label}: {type(err).__name__}: {err}")


def run_and_count(
    fn: Any, htmlbinary: bytes, item: dict[str, Any]
) -> tuple[str | None, tuple[int, int, int, int], BaseException | None]:
    """Run fn(htmlbinary) and score it; a crash counts as a full miss, matching how a
    real library failing in production would be treated. Returns (result, counts, exception)
    so a caller can still report/time the exception without duplicating the try/except."""
    try:
        result = fn(htmlbinary)
    except Exception as exc:
        return None, count_item(item, None), exc
    return result, count_item(item, result), None


# column labels for ConfusionMatrix.scores(), in return order
METRICS = ["precision", "recall", "accuracy", "f1"]


@dataclass
class ConfusionMatrix:
    "Accumulated (tp, fp, fn, tn) counts with derived scores."

    tp: int = 0
    fp: int = 0
    fn: int = 0
    tn: int = 0

    def add(self, counts: tuple[int, int, int, int]) -> None:
        tp, fp, fn, tn = counts
        self.tp += tp
        self.fp += fp
        self.fn += fn
        self.tn += tn

    def f1(self) -> float:
        denom = 2 * self.tp + self.fp + self.fn
        return 2 * self.tp / denom if denom else 0.0

    def scores(self) -> tuple[float, float, float, float]:
        "precision, recall, accuracy, f1 (each 0.0 when its denominator is empty)."
        precision = self.tp / (self.tp + self.fp) if self.tp + self.fp else 0.0
        recall = self.tp / (self.tp + self.fn) if self.tp + self.fn else 0.0
        total = self.tp + self.tn + self.fp + self.fn
        accuracy = (self.tp + self.tn) / total if total else 0.0
        return precision, recall, accuracy, self.f1()
