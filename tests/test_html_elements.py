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
        assert isinstance(xml_tag, str), f"Non-string mapping for '{html_tag}': {xml_tag}"
        assert xml_tag.islower(), f"Non-lowercase mapping for '{html_tag}': {xml_tag}"


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
            f"Expected {html_tag} -> {expected_xml_tag}, got {HTML_EL_TO_XML_EL[html_tag]}"


def test_identity_mappings_for_unspecified_elements() -> None:
    """Verify that elements without explicit mapping get identity mapping."""
    # Elements that should have identity mappings (tag -> tag)
    identity_elements = {
        "article", "section", "aside", "nav", "main", "header", "footer", 
        "plaintext", "content", "image", "menuitem", "shadow", "selectedcontent"
    }
    
    for element in identity_elements:
        assert element in HTML_EL_TO_XML_EL, f"Element '{element}' missing from mapping"
        assert HTML_EL_TO_XML_EL[element] == element, \
            f"Expected identity mapping for '{element}', got '{HTML_EL_TO_XML_EL[element]}'"