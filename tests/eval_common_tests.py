"""
Unit tests for the shared eval scorer (tests/eval_common.py).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eval_common import ConfusionMatrix, count_item, load_evaldata, norm, run_and_count, validate  # noqa: E402


def test_load_evaldata_reports_a_missing_file_as_such(tmp_path):
    "A typo'd path must not be reinterpreted as a directory holding evaldata.json."
    with pytest.raises(FileNotFoundError):
        load_evaldata(str(tmp_path / "typo.json"))


def test_validate_accepts_well_formed_corpus():
    validate({"url": {"file": "a.html", "with": ["x"], "without": ["y"]}})


def test_validate_rejects_missing_file():
    with pytest.raises(ValueError):
        validate({"url": {"file": "", "with": [], "without": []}})


@pytest.mark.parametrize(
    "item",
    [
        {"file": "a.html", "with": [None], "without": []},  # non-string chunk
        {"file": "a.html", "with": ["x"]},  # missing 'without'
        {"file": "a.html", "with": "x", "without": []},  # string instead of list
        {"file": "a.html", "with": [" "], "without": ["y"]},  # blank chunk always matches
        {"file": "a.html", "with": [], "without": ["y"]},  # nothing to score
        {"file": "a.html", "with": [str(n) for n in range(7)], "without": ["y"]},  # over the annotation bound
        {"file": "a.html", "with": ["x", " x "], "without": []},  # duplicate double-counts
        {"file": "a.html", "with": ["hello world"], "without": ["world"]},  # unsatisfiable
    ],
)
def test_validate_rejects_malformed_item(item):
    with pytest.raises(ValueError):
        validate({"url": item})


def test_norm_collapses_whitespace():
    assert norm("hello   world\n\n") == "hello world"


def test_count_item_matches_both_sides():
    item = {"with": ["hello world", "second chunk"], "without": ["boiler plate"]}
    assert count_item(item, "hello world text second chunk here") == (2, 0, 0, 1)


def test_count_item_whitespace_normalized():
    item = {"with": ["hello   world"], "without": []}
    assert count_item(item, "prefix hello world suffix") == (1, 0, 0, 0)


def test_count_item_none_result_counts_as_full_miss():
    item = {"with": ["a", "b"], "without": ["c"]}
    assert count_item(item, None) == (0, 0, 2, 1)


def test_count_item_non_string_result_counts_as_full_miss():
    item = {"with": ["a", "b"], "without": ["c"]}
    assert count_item(item, 123) == (0, 0, 2, 1)


def test_confusion_matrix_add_accumulates():
    cm = ConfusionMatrix()
    cm.add((2, 1, 0, 3))
    cm.add((1, 0, 1, 2))
    assert (cm.tp, cm.fp, cm.fn, cm.tn) == (3, 1, 1, 5)


def test_confusion_matrix_f1_matches_hand_computation():
    cm = ConfusionMatrix()
    cm.add((1, 0, 1, 2))
    assert cm.f1() == pytest.approx(2 / 3)


def test_confusion_matrix_f1_guarded_on_empty():
    assert ConfusionMatrix().f1() == 0.0


def test_confusion_matrix_scores_zero_on_empty():
    assert ConfusionMatrix().scores() == (0.0, 0.0, 0.0, 0.0)


def test_run_and_count_scores_a_successful_run():
    item = {"with": ["hello world"], "without": ["boiler plate"]}
    result, counts, err = run_and_count(lambda htmlbinary: "hello world here", b"", item)
    assert result == "hello world here"
    assert counts == (1, 0, 0, 1)
    assert err is None


def test_run_and_count_treats_a_crash_as_a_full_miss():
    item = {"with": ["a", "b"], "without": ["c"]}

    def boom(htmlbinary):
        raise RuntimeError("synthetic failure")

    result, counts, err = run_and_count(boom, b"", item)
    assert result is None
    assert counts == (0, 0, 2, 1)
    assert isinstance(err, RuntimeError)
