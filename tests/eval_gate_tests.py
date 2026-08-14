"""
Unit tests for the CI gate's corpus pinning and re-pin mechanism
(tests/eval_gate.py). Does not run the corpus/extractors — that's the
dedicated CI step, not part of the default test suite.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import eval_gate
from eval_common import ConfusionMatrix

PINS = {"evaldata_sha": "newsha", "entries": 2, "chunks": [4, 4]}


def test_corpus_sha_is_stable_sha256_hex():
    docs = {"url1": ("eval/a.html", b"<html>a</html>"), "url2": ("cache/b.html", b"<html>b</html>")}
    assert eval_gate.corpus_sha(docs) == eval_gate.corpus_sha(docs)
    assert len(eval_gate.corpus_sha(docs)) == 64


def test_corpus_sha_reacts_to_content_and_path():
    docs = {"url": ("eval/a.html", b"<html>a</html>")}
    baseline = eval_gate.corpus_sha(docs)
    assert eval_gate.corpus_sha({"url": ("eval/a.html", b"<html>b</html>")}) != baseline
    assert eval_gate.corpus_sha({"url": ("cache/a.html", b"<html>a</html>")}) != baseline


def test_real_baseline_matches_runners():
    "The shipped pin file must cover exactly the gated runners."
    baseline = eval_gate.load_baseline()
    assert set(baseline) == {"floors", "evaldata_sha", "entries", "chunks"}
    assert set(baseline["floors"]) == set(eval_gate.RUNNERS)


def _fake_matrices():
    "Two independent matrices with different F1s, so a test can't pass by aliasing them."
    fast, fallback = ConfusionMatrix(), ConfusionMatrix()
    fast.add((3, 1, 1, 5))  # F1 0.75
    fallback.add((4, 1, 1, 5))  # F1 0.8
    return {"fast": fast, "fallback": fallback}


def _baseline_target(tmp_path, monkeypatch, floors):
    "A baseline dict backed by a tmp file that repin()'s save writes to."
    target = tmp_path / "eval_baseline.json"
    baseline = {"floors": floors, "evaldata_sha": "old", "entries": 1, "chunks": [1, 1]}
    target.write_text(json.dumps(baseline))
    monkeypatch.setattr(eval_gate, "BASELINE_PATH", str(target))
    return baseline, target


def test_repin_rewrites_floors_and_pins(tmp_path, monkeypatch):
    baseline, target = _baseline_target(tmp_path, monkeypatch, {"fast": 0.1, "fallback": 0.2})

    assert eval_gate.repin(baseline, _fake_matrices(), PINS) == 0

    written = json.loads(target.read_text())
    assert written["floors"] == {"fast": 0.75, "fallback": 0.8}
    assert written["evaldata_sha"] == "newsha"
    assert written["entries"] == 2


def test_repin_idempotent_when_values_unchanged(tmp_path, monkeypatch):
    "A re-pin that measures the same floors/sha must still succeed."
    baseline, target = _baseline_target(tmp_path, monkeypatch, {"fast": 0.75, "fallback": 0.8})

    assert eval_gate.repin(baseline, _fake_matrices(), PINS) == 0
    assert json.loads(target.read_text())["floors"] == {"fast": 0.75, "fallback": 0.8}


def test_repin_tolerates_a_drop_within_epsilon(tmp_path, monkeypatch):
    "Measurement noise below EPSILON must not require --allow-regression."
    baseline, target = _baseline_target(tmp_path, monkeypatch, {"fast": 0.7503, "fallback": 0.8})

    assert eval_gate.repin(baseline, _fake_matrices(), PINS) == 0
    assert json.loads(target.read_text())["floors"] == {"fast": 0.75, "fallback": 0.8}


def test_repin_refuses_to_lower_a_floor_but_still_pins_corpus(tmp_path, monkeypatch):
    "A corpus edit that also regresses quality must not ratchet the floor down."
    baseline, target = _baseline_target(tmp_path, monkeypatch, {"fast": 0.9, "fallback": 0.8})

    assert eval_gate.repin(baseline, _fake_matrices(), PINS) == 1

    written = json.loads(target.read_text())
    assert written["floors"] == {"fast": 0.9, "fallback": 0.8}  # untouched
    assert written["evaldata_sha"] == "newsha"  # still re-pinned


def test_repin_lowers_a_floor_when_regression_allowed(tmp_path, monkeypatch):
    baseline, target = _baseline_target(tmp_path, monkeypatch, {"fast": 0.9, "fallback": 0.8})

    assert eval_gate.repin(baseline, _fake_matrices(), PINS, allow_regression=True) == 0
    assert json.loads(target.read_text())["floors"] == {"fast": 0.75, "fallback": 0.8}


def test_repin_writes_new_runner_floor_only_on_accepted_update(tmp_path, monkeypatch):
    "A runner absent from the pinned floors gets its first measurement written."
    baseline, target = _baseline_target(tmp_path, monkeypatch, {"fast": 0.9})

    assert eval_gate.repin(baseline, _fake_matrices(), PINS) == 1  # fast still refused

    written = json.loads(target.read_text())
    assert written["floors"] == {"fast": 0.9}  # refuse keeps old floors, incl. no new entry
    assert eval_gate.repin(written, _fake_matrices(), PINS, allow_regression=True) == 0
    assert json.loads(target.read_text())["floors"] == {"fast": 0.75, "fallback": 0.8}
