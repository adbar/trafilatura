"""Test HTML elements coverage against MDN reference."""

from trafilatura.htmlprocessing import HTML_EL_TO_XML_EL
from trafilatura.html_elements_reference import MDN_ELEMENTS


def test_every_mdn_tag_is_mapped() -> None:
    """Regression guard for GH-720: no MDN element may be forgotten."""
    missing = sorted(MDN_ELEMENTS - HTML_EL_TO_XML_EL.keys())
    assert not missing, f"Tags without conversion rule: {missing}"

    # Verify the mapping has reasonable values (no empty strings, etc.)
    for html_tag, xml_tag in HTML_EL_TO_XML_EL.items():
        assert xml_tag, f"Empty mapping for '{html_tag}'"
        assert isinstance(xml_tag, str), \
            f"Non-string mapping for '{html_tag}': {xml_tag}"
        assert xml_tag.islower(), \
            f"Non-lowercase mapping for '{html_tag}': {xml_tag}"


def test_explicit_mappings_preserved() -> None:
    """Verify that explicit conversions are preserved correctly."""
    # Test some key explicit mappings
    expected_mappings = {
        "h1": "head",
        "h2": "head",
        "h3": "head",
        "ul": "list",
        "ol": "list",
        "li": "item",
        "br": "lb",
        "hr": "lb",
        "blockquote": "quote",
        "a": "ref",
        "img": "graphic",
        "em": "hi",
        "strong": "hi",
        "p": "p",
        "div": "div",
    }

    for html_tag, expected_xml_tag in expected_mappings.items():
        assert HTML_EL_TO_XML_EL[html_tag] == expected_xml_tag, \
            f"Expected {html_tag} -> {expected_xml_tag}, " \
            f"got {HTML_EL_TO_XML_EL[html_tag]}"


def test_identity_mappings_for_unspecified_elements() -> None:
    """Verify that elements without explicit mapping get identity mapping."""
    # Elements that should have identity mappings (tag -> tag)
    identity_elements = {
        "article", "section", "aside", "nav", "main", "header",
        "footer", "plaintext", "content", "image", "menuitem",
        "shadow", "selectedcontent"
    }

    for element in identity_elements:
        assert element in HTML_EL_TO_XML_EL, \
            f"Element '{element}' missing from mapping"
        assert HTML_EL_TO_XML_EL[element] == element, \
            f"Expected identity mapping for '{element}', " \
            f"got '{HTML_EL_TO_XML_EL[element]}'"


def test_lesser_known_elements_preservation() -> None:
    """Test lesser-known HTML elements are preserved during processing."""
    from lxml import html, etree
    from trafilatura.htmlprocessing import convert_tags
    from trafilatura.core import Extractor

    # HTML snippet with lesser-known and legacy elements
    test_html = """<html><body>
        <article>
            <ruby>漢<rt>kan</rt>字<rt>ji</rt></ruby>
            <p>The <abbr title="HTML">HTML</abbr> spec includes
            <dfn>semantic elements</dfn> for meaning.</p>
            <p>Event: <data value="2025-01-15T14:30:00">2:30 PM</data></p>
            <p>Please <mark>remember this</mark> information.</p>
            <p>Arabic: <bdi>مرحبا</bdi> means hello.</p>
            <blockquote>Quote text <cite>Author</cite></blockquote>

            <!-- Legacy elements -->
            <center>Centered text</center>
            <nobr>Non-breaking text</nobr>
            <big>Bigger text</big>

            <!-- Modern elements -->
            <search>Search content</search>
            <fencedframe src="example.html">Fallback</fencedframe>
            <progress value="70" max="100">70%</progress>
            <meter value="6" max="10">6/10</meter>

            <template id="tmpl">Template content</template>

            <details>
                <summary>Expandable</summary>
                <p>Hidden content</p>
            </details>
        </article>
    </body></html>"""

    # Parse the HTML
    doc = html.fromstring(test_html)

    # Apply tag conversion with minimal necessary options
    options = Extractor()
    options.formatting = True  # Only formatting is needed for this test

    # Before the patch, many elements would be stripped or ignored.
    # With the patch, they're preserved due to MDN element mapping.
    converted_doc = convert_tags(doc, options)
    result_html = etree.tostring(converted_doc, encoding='unicode')

    # Verify specific lesser-known elements are preserved
    # These demonstrate elements that would have been lost before the patch
    assert '<ruby>' in result_html and '</ruby>' in result_html
    assert '<rt>' in result_html and '</rt>' in result_html
    assert '<abbr' in result_html and '</abbr>' in result_html
    assert '<dfn>' in result_html and '</dfn>' in result_html
    assert '<data' in result_html and '</data>' in result_html
    assert '<mark>' in result_html and '</mark>' in result_html
    assert '<bdi>' in result_html and '</bdi>' in result_html
    assert '<cite>' in result_html and '</cite>' in result_html

    # Legacy elements that are now preserved
    assert '<center>' in result_html and '</center>' in result_html
    assert '<nobr>' in result_html and '</nobr>' in result_html
    assert '<big>' in result_html and '</big>' in result_html

    # Modern elements that are now preserved
    assert '<search>' in result_html and '</search>' in result_html
    assert '<fencedframe' in result_html and '</fencedframe>' in result_html
    assert '<progress' in result_html and '</progress>' in result_html
    assert '<meter' in result_html and '</meter>' in result_html
    assert '<template' in result_html and '</template>' in result_html

    # Verify text content is still accessible
    text_content = converted_doc.text_content()
    assert '漢' in text_content and '字' in text_content  # Ruby characters
    assert 'kan' in text_content and 'ji' in text_content  # Ruby text
    assert 'HTML' in text_content  # Abbreviation text
    assert 'semantic elements' in text_content  # Definition text
    assert '2:30 PM' in text_content  # Data element text
    assert 'remember this' in text_content  # Mark element text
    assert 'مرحبا' in text_content  # Bidirectional text
    assert 'Quote text' in text_content  # Blockquote text
    assert 'Author' in text_content  # Citation text
    assert 'Centered text' in text_content  # Legacy center text
    assert 'Non-breaking text' in text_content  # Legacy nobr text
    assert 'Bigger text' in text_content  # Legacy big text
    assert 'Search content' in text_content  # Search element text
    assert 'Fallback' in text_content  # Fencedframe fallback
    assert '70%' in text_content  # Progress text
    assert '6/10' in text_content  # Meter text
    assert 'Template content' in text_content  # Template text
    assert 'Expandable' in text_content  # Summary text
    assert 'Hidden content' in text_content  # Details content


def test_comprehensive_tag_conversion_before_after() -> None:
    """Demonstrate before/after behavior of comprehensive tag conversion."""
    from lxml import html, etree
    from trafilatura.htmlprocessing import HTML_EL_TO_XML_EL, convert_tags
    from trafilatura.core import Extractor

    # Simple HTML with elements that weren't handled before the patch
    simple_html = ('<body><search>Search</search><ruby>Ruby</ruby>'
                   '<nobr>NoBreak</nobr></body>')

    # Parse HTML
    doc = html.fromstring(simple_html)

    # Apply tag conversion using the public API
    options = Extractor()
    converted_doc = convert_tags(doc, options)
    converted_html = etree.tostring(converted_doc, encoding='unicode')

    # Verify that:
    # 1. Elements are preserved (not stripped)
    # 2. Identity mappings work (element stays the same)
    # 3. All elements from MDN list have mappings
    assert '<search>' in converted_html  # Should be preserved
    assert '<ruby>' in converted_html    # Should be preserved
    assert '<nobr>' in converted_html    # Should be preserved

    # Verify elements have proper mappings
    assert HTML_EL_TO_XML_EL['search'] == 'search'  # Identity mapping
    assert HTML_EL_TO_XML_EL['ruby'] == 'ruby'      # Identity mapping
    assert HTML_EL_TO_XML_EL['nobr'] == 'nobr'      # Identity mapping


def test_table_elements_excluded_from_conversion() -> None:
    """Ensure table elements are not converted to avoid conflicts."""
    from lxml import html, etree
    from trafilatura.htmlprocessing import convert_tags
    from trafilatura.core import Extractor

    # HTML with table elements that should NOT be converted
    table_html = '''<body>
        <table>
            <tr><td>Cell 1</td><th>Header 1</th></tr>
            <tr><td>Cell 2</td><th>Header 2</th></tr>
        </table>
    </body>'''

    # Parse HTML
    doc = html.fromstring(table_html)

    # Apply tag conversion
    options = Extractor()
    converted_doc = convert_tags(doc, options)
    result_html = etree.tostring(converted_doc, encoding='unicode')

    # Verify that table elements are NOT converted (remain as-is)
    # This prevents conflicts with main_extractor's table processing logic
    assert '<table>' in result_html and '</table>' in result_html
    assert '<tr>' in result_html and '</tr>' in result_html
    assert '<td>' in result_html and '</td>' in result_html
    assert '<th>' in result_html and '</th>' in result_html

    # Verify they did NOT get converted to their XML equivalents
    assert '<row>' not in result_html  # tr should NOT be converted to row
    assert '<cell>' not in result_html  # td/th should NOT be converted


def test_conversions_consistency() -> None:
    """Ensure all CONVERSIONS keys are excluded to maintain consistency."""
    from trafilatura.htmlprocessing import (
        CONVERSIONS, _EXCLUDED_TAGS  # test-hook
    )

    # All CONVERSIONS keys must be in _EXCLUDED_TAGS to prevent conflicts
    conversions_keys = set(CONVERSIONS.keys())
    missing_exclusions = conversions_keys - _EXCLUDED_TAGS

    assert not missing_exclusions, \
        f"CONVERSIONS keys not in _EXCLUDED_TAGS: {missing_exclusions}. " \
        f"This will cause conflicts in convert_tags processing."


def test_unsafe_tags_are_cleaned() -> None:
    """Verify potentially unsafe HTML elements are handled."""
    from trafilatura.htmlprocessing import (
        _CONVERSION_TAGS  # test-hook
    )
    from trafilatura.settings import MANUALLY_CLEANED

    # Tags that could pose security risks if preserved unchecked
    unsafe_tags = {'embed', 'object', 'svg', 'math', 'canvas', 'script',
                   'iframe', 'frame', 'frameset', 'applet'}

    preserved_unsafe = unsafe_tags & set(_CONVERSION_TAGS)
    manually_cleaned = set(MANUALLY_CLEANED)
    risky_tags = preserved_unsafe - manually_cleaned

    assert not risky_tags, \
        f"Potentially unsafe tags are preserved but not in " \
        f"MANUALLY_CLEANED: {risky_tags}. Consider adding them to " \
        f"MANUALLY_CLEANED or removing from MDN_ELEMENTS."
