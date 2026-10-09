from typing import Final

import pytest

from trafilatura import extract
from trafilatura.settings import use_config


@pytest.mark.parametrize(
    "include_tables",
    [pytest.param(False, id="exclude-tables"), pytest.param(True, id="include-tables")],
)
def test_readability_preserves_table_filter(include_tables: bool) -> None:
    rows: Final[list[str]] = [f"Garden plot {index}, soil measurements and planting observations." for index in range(10)]
    source: Final[str] = (
        "<html><body><table><tbody>" + "".join(f"<tr><td>{row}</td></tr>" for row in rows) + "</tbody></table></body></html>"
    )
    config = use_config()
    config["DEFAULT"]["MIN_OUTPUT_SIZE"] = "0"
    config["DEFAULT"]["MIN_EXTRACTED_SIZE"] = "0"
    expected: Final[str] = "\n".join(f"| {row} | " for row in rows).rstrip() if include_tables else ""
    assert extract(source, fast=False, include_tables=include_tables, config=config) == expected


def test_readability_summary_serializes_article() -> None:
    from trafilatura.dom import fromstring
    from trafilatura.readability_lxml import Document

    text: Final[str] = "Garden measurements, planting observations and soil analysis. " * 5
    tree = fromstring(f"<html><body><article><p>{text}</p></article></body></html>")
    assert Document(tree).summary() == f"<div><article><p>{text}</p></article></div>"
