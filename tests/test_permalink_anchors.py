"""
Regression test: heading permalink anchors must not leak into the output.

Sphinx-style sites embed a headerlink (pilcrow ¶) inside <h1>-<h6>; rustdoc
uses a section anchor (§). Before this fix, convert_tags() turned the <a> into
a <ref> whose symbol-only text was serialized into the heading.
"""

from trafilatura import extract
from trafilatura.settings import use_config

ZERO_CONFIG = use_config()  # fresh copy: must not mutate the package-global DEFAULT_CONFIG
ZERO_CONFIG["DEFAULT"]["MIN_OUTPUT_SIZE"] = "0"
ZERO_CONFIG["DEFAULT"]["MIN_EXTRACTED_SIZE"] = "0"


def _extract_heading(heading: str) -> str:
    """Extract a single heading followed by an intro paragraph, as plain text."""
    html = (
        "<html><body><article>"
        f"<h2>{heading}</h2>"
        "<p>Enough intro text here so the extractor has something to return.</p>"
        "</article></body></html>"
    )
    return extract(html, config=ZERO_CONFIG) or ""


def test_heading_permalink_anchor_dropped():
    "A symbol-only permalink anchor inside a heading must not leak into the text."
    # Sphinx-style headerlink: an <a> whose only text is the pilcrow
    sphinx = _extract_heading('<a class="headerlink" href="#section">¶</a>Section title')
    assert "¶" not in sphinx
    assert "Section title" in sphinx
    # rustdoc-style section anchor: an <a> whose only text is the section sign
    rustdoc = _extract_heading('<a class="anchor" href="#section">§</a>Section title')
    assert "§" not in rustdoc
    assert "Section title" in rustdoc
    # a real link with meaningful text inside a heading is still kept
    linked = _extract_heading('<a href="#section">anchor text</a>Section title')
    assert "anchor text" in linked
    assert "Section title" in linked
