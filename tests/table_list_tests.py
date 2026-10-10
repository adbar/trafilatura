from pathlib import Path
from typing import TYPE_CHECKING, Final

import pytest

from trafilatura import extract
from trafilatura.settings import use_config

if TYPE_CHECKING:
    from configparser import ConfigParser


@pytest.mark.parametrize("fast", [pytest.param(True, id="fast"), pytest.param(False, id="fallback")])
def test_fifa_settings_keep_list_cell(fast: bool) -> None:
    source: Final[bytes] = (Path(__file__).parent / "eval" / "fifplay.com.settings.html").read_bytes()
    assert "Your Default Game Lanaguage" in (extract(source, fast=fast, include_comments=False) or "")


@pytest.fixture
def table_config() -> "ConfigParser":
    config: Final = use_config()
    config["DEFAULT"]["MIN_OUTPUT_SIZE"] = "0"
    config["DEFAULT"]["MIN_EXTRACTED_SIZE"] = "0"
    return config


@pytest.mark.parametrize(
    ("content", "focus", "expected"),
    [
        pytest.param("<ul><li>Garden value</li></ul>", "balanced", "Garden value", id="list-only"),
        pytest.param(
            "<ul><li>Garden value</li></ul><ul><li>Second value</li></ul>",
            "balanced",
            "Garden value Second value",
            id="multiple-lists",
        ),
        pytest.param(
            "<p>Garden description</p><ul><li>Garden value</li></ul>",
            "balanced",
            "Garden description",
            id="mixed-paragraph",
        ),
        pytest.param("Garden description<ul><li>Garden value</li></ul>", "balanced", "Garden description", id="mixed-text"),
        pytest.param("<ul><li>Garden value</li></ul>Garden description", "balanced", "Garden description", id="mixed-tail"),
        pytest.param("<ul><li>Garden value</li></ul>", "precision", "", id="precision-filters-list"),
        pytest.param(
            "<p>Garden description</p><ul><li>Garden value</li></ul>",
            "recall",
            "Garden description Garden value",
            id="recall-keeps-mixed-list",
        ),
    ],
)
def test_table_list_cells(content: str, focus: str, expected: str, table_config: "ConfigParser") -> None:
    source: Final[str] = (
        "<html><body><article><table><tr><th>Setting</th><th>Values</th></tr>"
        f"<tr><td>Garden setting</td><td>{content}</td></tr></table></article></body></html>"
    )
    assert (
        extract(
            source,
            fast=True,
            include_comments=False,
            favor_precision=focus == "precision",
            favor_recall=focus == "recall",
            config=table_config,
        )
        == f"| Setting | Values | \n|---|---|\n| Garden setting | {expected} |"
    )
