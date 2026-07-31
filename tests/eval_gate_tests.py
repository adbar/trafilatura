"""
Unit tests for the CI gate's corpus pinning and re-pin mechanism
(tests/eval_gate.py). Does not run the corpus/extractors — that's the
dedicated CI step, not part of the default test suite.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import eval_gate  # noqa: E402
from eval_common import ConfusionMatrix  # noqa: E402


def test_corpus_sha_is_stable_sha256_hex():
    docs = {"url1": ("eval/a.html", b"<html>a</html>"), "url2": ("cache/b.html", b"<html>b</html>")}
    assert eval_gate.corpus_sha(docs) == eval_gate.corpus_sha(docs)
    assert len(eval_gate.corpus_sha(docs)) == 64


def test_corpus_sha_reacts_to_content_and_path():
    docs = {"url": ("eval/a.html", b"<html>a</html>")}
    baseline = eval_gate.corpus_sha(docs)
    assert eval_gate.corpus_sha({"url": ("eval/a.html", b"<html>b</html>")}) != baseline
    assert eval_gate.corpus_sha({"url": ("cache/a.html", b"<html>a</html>")}) != baseline


def test_corpus_sha_rejects_unresolvable_file():
    with pytest.raises(ValueError):
        eval_gate.read_corpus({"url": {"file": "does-not-exist.html"}})


def _fake_matrices():
    "Two independent matrices with different F1s, so a test can't pass by aliasing them."
    fast, fallback = ConfusionMatrix(), ConfusionMatrix()
    fast.add((3, 1, 1, 5))  # F1 0.75
    fallback.add((4, 1, 1, 5))  # F1 0.8
    return {"fast": fast, "fallback": fallback}


def _repin_target(tmp_path, monkeypatch, text, floors=None):
    "A fake eval_gate.py source that repin() rewrites, with module FLOORS kept in sync."
    target = tmp_path / "fake_eval_gate.py"
    target.write_text(text)
    monkeypatch.setattr(eval_gate, "__file__", str(target))
    monkeypatch.setattr(eval_gate, "FLOORS", floors or {"fast": 0.1, "fallback": 0.2})
    return target


def test_repin_rewrites_floors_and_sha(tmp_path, monkeypatch):
    target = _repin_target(tmp_path, monkeypatch, 'FLOORS = {"fast": 0.1, "fallback": 0.2}\nEVALDATA_SHA = "old"\n')

    assert eval_gate.repin(_fake_matrices(), "newsha") == 0

    text = target.read_text()
    assert 'FLOORS = {"fast": 0.75, "fallback": 0.8}' in text
    assert 'EVALDATA_SHA = "newsha"' in text


def test_repin_raises_if_floors_line_not_matched(tmp_path, monkeypatch):
    "Regression test: repin() must not silently no-op if FLOORS isn't on one line."
    original = 'FLOORS = {\n    "fast": 0.1,\n}\nEVALDATA_SHA = "old"\n'
    target = _repin_target(tmp_path, monkeypatch, original)

    with pytest.raises(RuntimeError):
        eval_gate.repin(_fake_matrices(), "newsha")
    assert target.read_text() == original


def test_repin_raises_if_sha_line_not_matched(tmp_path, monkeypatch):
    _repin_target(tmp_path, monkeypatch, 'FLOORS = {"fast": 0.1, "fallback": 0.2}\nEVALDATA_SHA = old_no_quotes\n')

    with pytest.raises(RuntimeError):
        eval_gate.repin(_fake_matrices(), "newsha")


def test_repin_idempotent_when_values_unchanged(tmp_path, monkeypatch):
    "A re-pin that measures the same floors/sha must still succeed, not raise."
    target = _repin_target(
        tmp_path,
        monkeypatch,
        'FLOORS = {"fast": 0.75, "fallback": 0.75}\nEVALDATA_SHA = "newsha"\n',
        floors={"fast": 0.75, "fallback": 0.75},
    )

    assert eval_gate.repin(_fake_matrices(), "newsha") == 0  # must not raise
    assert 'FLOORS = {"fast": 0.75, "fallback": 0.8}' in target.read_text()


def test_repin_refuses_to_lower_a_floor_but_still_pins_sha(tmp_path, monkeypatch):
    "A corpus edit that also regresses quality must not ratchet the floor down."
    target = _repin_target(
        tmp_path,
        monkeypatch,
        'FLOORS = {"fast": 0.9, "fallback": 0.8}\nEVALDATA_SHA = "old"\n',
        floors={"fast": 0.9, "fallback": 0.8},  # measured fast F1 is 0.75, below its floor
    )

    assert eval_gate.repin(_fake_matrices(), "newsha") == 1

    text = target.read_text()
    assert 'FLOORS = {"fast": 0.9, "fallback": 0.8}' in text  # untouched
    assert 'EVALDATA_SHA = "newsha"' in text  # still re-pinned


def test_repin_lowers_a_floor_when_regression_allowed(tmp_path, monkeypatch):
    target = _repin_target(
        tmp_path,
        monkeypatch,
        'FLOORS = {"fast": 0.9, "fallback": 0.8}\nEVALDATA_SHA = "old"\n',
        floors={"fast": 0.9, "fallback": 0.8},
    )

    assert eval_gate.repin(_fake_matrices(), "newsha", allow_regression=True) == 0
    assert 'FLOORS = {"fast": 0.75, "fallback": 0.8}' in target.read_text()
