from __future__ import annotations

from typing import TYPE_CHECKING, Final, ParamSpec, TypeVar

from lxml.etree import SubElement as _SubElement
from lxml.etree import XPath as _XPath
from lxml.etree import strip_elements, strip_tags, tostring
from lxml.html import Element, HtmlElement, HTMLParser
from lxml.html import document_fromstring as _document_fromstring
from lxml.html import fragment_fromstring as _fragment_fromstring
from lxml.html import fromstring as _fromstring

if TYPE_CHECKING:
    from collections.abc import Callable

_PARAMS = ParamSpec("_PARAMS")
_RESULT = TypeVar("_RESULT")
_Element = HtmlElement
_TREE = TypeVar("_TREE", bound=_Element | None)
_PARSER: Final = HTMLParser(collect_ids=False, default_doctype=False, encoding="utf-8", remove_comments=True, remove_pis=True)


class XPath(_XPath):
    def __init__(self, path: str) -> None:
        super().__init__(path, namespaces={"re": "http://exslt.org/regular-expressions"})


def _sub_element(parent: HtmlElement, tag: str, attrib: dict[str, str] | None = None, **extra: str) -> HtmlElement:
    attributes: Final = (attrib or {}) | extra
    return _SubElement(parent, tag, attributes)


SubElement: Final = _sub_element


def document_context(function: Callable[_PARAMS, _RESULT]) -> Callable[_PARAMS, _RESULT]:
    return function


def document_fromstring(markup: str | bytes) -> HtmlElement:
    return _document_fromstring(markup, parser=_PARSER)


def fromstring(markup: str | bytes) -> HtmlElement:
    return _fromstring(markup, parser=_PARSER)


def fragment_fromstring(markup: str, create_parent: str | bool = False) -> HtmlElement:
    return _fragment_fromstring(markup, create_parent=create_parent, parser=_PARSER)


def from_lxml(tree: HtmlElement) -> HtmlElement:
    return tree


def to_lxml(tree: _TREE) -> _TREE:
    return tree


def to_lxml_html(tree: HtmlElement) -> HtmlElement:
    return tree


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
