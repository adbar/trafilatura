"""
Unit tests for the CI gate's corpus pinning and re-pin mechanism
(tests/eval_gate.py). Does not run the corpus/extractors — that's the
dedicated CI step, not part of the default test suite.
"""

import json
import os
import sys

import pytest

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


def test_real_meta_baseline_matches_fields():
    assert set(eval_gate.load_baseline(eval_gate.META_BASELINE_PATH)["floors"]) == set(eval_gate.META_FIELDS)


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("title", "", []),
        ("title", None, []),
        ("title", " A  Title ", ["a title"]),
        ("author", "Jane Doe; John Roe", ["jane doe", "john roe"]),
        ("author", "John Roe, Jane Doe", ["jane doe", "john roe"]),
        ("author", ["Jane Doe", "John Roe"], ["jane doe", "john roe"]),
        ("author", "John Roe and Jane Doe", ["jane doe", "john roe"]),
        ("tags", ["b", "A", ""], ["a", "b"]),
        ("date", "2020-01-02", ["2020-01-02"]),
    ],
)
def test_meta_values(field, value, expected):
    assert eval_gate.meta_values(field, value) == expected


def test_meta_scores_skip_empty_gold():
    html = b"<html><head><title>Head Line</title><meta name='author' content='Jane Doe'/></head><body/></html>"
    evaldata = {
        "https://example.org/a": {"title": "head line", "author": "", "date": "2020-01-02", "tags": [], "categories": []},
        "https://example.org/b": {"title": "Other", "author": "jane doe", "date": "", "tags": [], "categories": []},
        "https://example.org/c": {"title": "", "author": "", "date": "", "tags": [], "categories": []},
    }
    docs = dict.fromkeys(evaldata, ("eval/x.html", html))
    scores = eval_gate.meta_scores(evaldata, docs)
    assert scores["title"] == 0.5
    assert scores["author"] == 1.0
    assert scores["date"] == 0.0


def test_meta_scores_count_crash_as_miss(monkeypatch, capsys):
    def crash(*_args, **_kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(eval_gate, "extract_metadata", crash)
    evaldata = {"https://example.org/a": {"title": "Head Line", "author": "", "date": "", "tags": [], "categories": []}}
    docs = {"https://example.org/a": ("eval/x.html", b"<html><head><title>Head Line</title></head><body/></html>")}
    assert eval_gate.meta_scores(evaldata, docs)["title"] == 0.0
    assert "metadata: eval/x.html: ValueError: boom" in capsys.readouterr().out


def test_repin_meta(tmp_path, monkeypatch):
    target = tmp_path / "eval_meta_baseline.json"
    monkeypatch.setattr(eval_gate, "META_BASELINE_PATH", str(target))
    # first pin, then a raise
    assert eval_gate.repin_meta({"title": 0.5}) == 0
    assert eval_gate.repin_meta({"title": 0.6}) == 0
    # a drop beyond the noise is refused unless allowed
    assert eval_gate.repin_meta({"title": 0.5}) == 1
    assert json.loads(target.read_text())["floors"] == {"title": 0.6}
    assert eval_gate.repin_meta({"title": 0.5}, allow_regression=True) == 0
    assert json.loads(target.read_text())["floors"] == {"title": 0.5}
