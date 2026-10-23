# pylint: disable=redefined-outer-name
"""
Tests for the ``include_spans`` extraction option (keeps <span> elements
and their attributes for HTML output).
"""

import pytest

from trafilatura import extract


HTML = """<html><head><title>Span test</title></head><body>
<article>
<p>This is a normal paragraph with enough words to be considered real content and not boilerplate.</p>
<p>The important value is <span style="color:red" class="hl">RED: 42 units</span> and more text follows to fill it out.</p>
<p>A final concluding sentence that adds length to the extracted body text overall here.</p>
</article>
</body></html>"""


def test_spans_stripped_by_default():
    "span tags are removed by default, but their text content survives."
    result = extract(HTML, output_format="html")
    assert "<span" not in result
    assert "RED: 42 units" in result


def test_spans_kept_with_attributes():
    "include_spans keeps the element and its attributes verbatim (HTML output)."
    result = extract(HTML, output_format="html", include_spans=True)
    assert '<span style="color:red" class="hl">RED: 42 units</span>' in result


def test_spans_plain_text():
    "For plain text output no span tags appear, content is kept."
    assert "<span" not in extract(HTML, include_spans=True)
    assert "RED: 42 units" in extract(HTML, include_spans=True)


def test_spans_markdown():
    "Markdown output carries no span tags."
    result = extract(HTML, output_format="markdown", include_spans=True)
    assert "<span" not in result
    assert "RED: 42 units" in result


def test_spans_xmltei():
    "TEI output must stay conforming and never include raw span tags."
    result = extract(HTML, output_format="xmltei", include_spans=True)
    assert "span" not in result
    assert "RED: 42 units" in result


def test_spans_nested():
    "Nested spans are kept with their attributes."
    doc = (
        "<html><body><article><p>"
        'A <span class="outer">outer <span style="color:blue">inner value</span> tail</span>'
        " with enough following words to make a real non-boilerplate paragraph here now."
        "</p></article></body></html>"
    )
    result = extract(doc, output_format="html", include_spans=True)
    assert 'class="outer"' in result
    assert 'style="color:blue"' in result
    assert "inner value" in result


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))  # noqa: F821
