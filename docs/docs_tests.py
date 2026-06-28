"""Build the documentation with Sphinx to catch broken pages or references
(GitHub issue #698). Run in CI for the Python version used on Read the Docs."""

import subprocess
from pathlib import Path

import pytest

DOCS = Path(__file__).parent


def test_docs_build(tmp_path):
    """The documentation compiles cleanly (warnings treated as errors)."""
    result = subprocess.run(
        ["sphinx-build", "-W", "-b", "html", str(DOCS), str(tmp_path)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Sphinx build failed (exit {result.returncode})\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    assert (tmp_path / "index.html").exists()
