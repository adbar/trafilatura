import sys

if sys.version_info >= (3, 11):
    from ._turbohtml import (
        Element,
        HtmlElement,
        SubElement,
        XPath,
        _Element,
        document_context,
        document_fromstring,
        fragment_fromstring,
        from_lxml,
        fromstring,
        strip_elements,
        strip_tags,
        to_lxml,
        to_lxml_html,
        tostring,
    )
else:
    from ._lxml import (
        Element,
        HtmlElement,
        SubElement,
        XPath,
        _Element,
        document_context,
        document_fromstring,
        fragment_fromstring,
        from_lxml,
        fromstring,
        strip_elements,
        strip_tags,
        to_lxml,
        to_lxml_html,
        tostring,
    )


__all__ = [
    "Element",
    "HtmlElement",
    "SubElement",
    "XPath",
    "_Element",
    "document_context",
    "document_fromstring",
    "fragment_fromstring",
    "from_lxml",
    "fromstring",
    "strip_elements",
    "strip_tags",
    "to_lxml",
    "to_lxml_html",
    "tostring",
]
