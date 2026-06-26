"""
Checks for the documentation, e.g. that a page explaining how to run the
tests is present and wired into the documentation tree (GitHub issue #698).
"""

from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"


def test_tests_doc_exists():
    """A dedicated documentation page on running the tests is present and
    regroups the core instructions previously scattered across the repository."""
    doc = DOCS_DIR / "tests.rst"
    assert doc.is_file()
    content = doc.read_text(encoding="utf-8")
    for instruction in ("pytest", "mypy", "ruff", "trafilatura[dev]"):
        assert instruction in content


def test_tests_doc_in_toctree():
    """The page is referenced in the documentation tree."""
    index = (DOCS_DIR / "index.rst").read_text(encoding="utf-8")
    assert "\n   tests\n" in index
