"""CI quality gate: fails if own-benchmark F1 regresses below FLOORS.

No competitor-extractor deps (unlike evaluate.py), so it's cheap to run in CI.
EVALDATA_SHA pins evaldata.json plus every resolved HTML input — many double
as unit-test mock pages in cache/, so a refresh there would otherwise change
scores unnoticed. After editing either, re-pin with ``--update``: it re-pins the
SHA but refuses to lower a floor without ``--allow-regression``.
"""

import hashlib
import os
import re
import sys
from typing import Any

from eval_common import ConfusionMatrix, load_evaldata, make_runners, resolve, run_and_count, validate

from trafilatura import extract

HERE = os.path.dirname(os.path.abspath(__file__))

# full-corpus baseline
FLOORS = {"fast": 0.918, "fallback": 0.9245}
EVALDATA_SHA = "b443dcaae4d0aa2097a1abc780495635786b5cb2b33a01787f20879a25a8e133"

RUNNERS = make_runners(extract)


def read_corpus(evaldata: dict[str, dict[str, Any]]) -> dict[str, tuple[str, bytes]]:
    "Read every resolved HTML input once; returns {url: (posix relpath, bytes)}."
    docs = {}
    for url in sorted(evaldata):
        path = resolve(HERE, evaldata[url]["file"])
        if path is None:
            raise ValueError(f"{url}: HTML file not found: {evaldata[url]['file']}")
        # records which copy won the cache/eval lookup; posix, so the pin isn't OS-dependent
        relpath = os.path.relpath(path, HERE).replace(os.sep, "/")
        with open(path, "rb") as f:
            docs[url] = (relpath, f.read())
    return docs


def corpus_sha(docs: dict[str, tuple[str, bytes]]) -> str:
    "Digest annotations + every resolved HTML input, so a mock-page refresh trips the gate too."
    hashsum = hashlib.sha256()
    with open(os.path.join(HERE, "evaldata.json"), "rb") as f:
        hashsum.update(f.read())
    for relpath, htmlbinary in docs.values():
        hashsum.update(relpath.encode())
        hashsum.update(htmlbinary)
    return hashsum.hexdigest()


def score(evaldata: dict[str, dict[str, Any]], docs: dict[str, tuple[str, bytes]]) -> dict[str, ConfusionMatrix]:
    matrices = {name: ConfusionMatrix() for name in RUNNERS}
    reported: set[str] = set()  # runners whose first exception was printed
    for url, item in evaldata.items():
        relpath, htmlbinary = docs[url]
        for name, fn in RUNNERS.items():
            _, counts, err = run_and_count(fn, htmlbinary, item)
            if err is not None and name not in reported:
                # a crash already costs recall; name it so CI shows more than a lower F1
                reported.add(name)
                print(f"{name}: {relpath}: {type(err).__name__}: {err}")
            matrices[name].add(counts)
    return matrices


def repin(matrices: dict[str, ConfusionMatrix], sha: str, allow_regression: bool = False) -> int:
    "Rewrite EVALDATA_SHA and, unless that lowers a floor, FLOORS; returns the exit code."
    measured = {name: round(cm.f1(), 4) for name, cm in matrices.items()}
    drops = [
        f"{name}: F1={f1:.4f} vs floor {FLOORS[name]:.4f} ({f1 - FLOORS[name]:+.4f})"
        for name, f1 in measured.items()
        if name in FLOORS and f1 < FLOORS[name]
    ]
    floors = "{" + ", ".join(f'"{name}": {f1}' for name, f1 in measured.items()) + "}"

    # the SHA only records "corpus seen"; the floors are the quality bar
    substitutions = [(r'^EVALDATA_SHA = ".*"$', f'EVALDATA_SHA = "{sha}"', "EVALDATA_SHA")]
    if not drops or allow_regression:
        substitutions.append((r"^FLOORS = \{.*\}$", f"FLOORS = {floors}", "FLOORS"))

    # newline="" so a Windows run doesn't rewrite the whole file to CRLF
    with open(__file__, encoding="utf-8", newline="") as f:
        text = f.read()
    for pattern, replacement, name in substitutions:
        text, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
        if n == 0:
            raise RuntimeError(f"repin: {name} line not found/matched — check formatting")
    with open(__file__, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    if drops and not allow_regression:
        print("\n".join(["re-pinned EVALDATA_SHA only — refusing to lower the floor:", *drops]))
        print("fix the regression, or re-run with --allow-regression to accept the lower bar")
        return 1
    print(f"re-pinned FLOORS={floors} EVALDATA_SHA={sha}")
    return 0


def main(argv: list[str]) -> int:
    update = "--update" in argv
    evaldata = load_evaldata(HERE)
    validate(evaldata)

    docs = read_corpus(evaldata)
    sha = corpus_sha(docs)
    if not update and sha != EVALDATA_SHA:
        sys.exit("corpus changed (annotations or HTML) — re-measure and re-pin:\n    python tests/eval_gate.py --update")

    matrices = score(evaldata, docs)
    if update:
        return repin(matrices, sha, allow_regression="--allow-regression" in argv)

    regression = False
    for name, cm in matrices.items():
        f1, floor = round(cm.f1(), 4), FLOORS[name]
        regression = regression or f1 < floor
        print(f"{name:>9}: F1={f1:.4f} (floor {floor:.4f})")
    return int(regression)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
