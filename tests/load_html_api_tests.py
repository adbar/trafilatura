from typing import Final

import pytest
from lxml import etree, html
from urllib3.response import HTTPResponse

from trafilatura import extract, load_html
from trafilatura.dom import HtmlElement, fromstring
from trafilatura.settings import use_config
from trafilatura.utils import HtmlInput, Response, fromstring_bytes


def test_load_html_preserves_input_identity() -> None:
    tree: Final = html.fromstring('<div><a href="page">Page</a></div>', base_url="https://example.org/")
    assert load_html(tree) is tree


def test_load_html_supports_compiled_xpath() -> None:
    tree: Final = load_html('<html><body><a href="page">Page</a></body></html>')
    assert etree.XPath("string(//a/@href)")(tree) == "page"


def test_load_html_supports_lxml_serialization() -> None:
    tree: Final = load_html("<html><body><p>Garden</p></body></html>")
    assert etree.tostring(tree) == b"<html><body><p>Garden</p></body></html>"


def test_load_html_supports_link_resolution() -> None:
    tree: Final = load_html('<html><body><a href="page">Page</a></body></html>')
    assert tree is not None
    tree.make_links_absolute("https://example.org/garden/")
    assert [(element.tag, attribute, url, position) for element, attribute, url, position in tree.iterlinks()] == [
        ("a", "href", "https://example.org/garden/page", 0)
    ]


@pytest.mark.parametrize(
    "source",
    [
        pytest.param("<html><body><p>Garden</p></body></html>", id="text"),
        pytest.param(b"<html><body><p>Garden</p></body></html>", id="bytes"),
        pytest.param('<?xml version="1.0" encoding="UTF-8"?><html><body><p>Garden</p></body></html>', id="declaration"),
        pytest.param(Response(b"<html><body><p>Garden</p></body></html>", 200, "https://example.org/"), id="response"),
        pytest.param(HTTPResponse(body=b"<html><body><p>Garden</p></body></html>"), id="urllib3-response"),
        pytest.param(fromstring("<html><body><p>Garden</p></body></html>"), id="native-tree"),
    ],
)
def test_load_html_returns_lxml(source: str | bytes | Response | HTTPResponse | HtmlElement) -> None:
    tree: Final = load_html(source)
    assert isinstance(tree, html.HtmlElement)
    assert tree.text_content() == "Garden"


@pytest.mark.parametrize("source", [pytest.param("", id="empty"), pytest.param("<p>Garden</p>", id="fragment")])
def test_load_html_rejects_non_documents(source: str) -> None:
    assert load_html(source) is None


@pytest.mark.parametrize("source", [pytest.param(123, id="integer"), pytest.param(None, id="none")])
def test_load_html_rejects_unsupported_types(source: HtmlInput) -> None:
    with pytest.raises(TypeError, match="incompatible input type"):
        load_html(source)


def test_fromstring_bytes_returns_lxml() -> None:
    tree: Final = fromstring_bytes("<html><body><p>Garden</p></body></html>")
    assert isinstance(tree, html.HtmlElement)
    assert tree.text_content() == "Garden"


def test_fromstring_bytes_rejects_empty_input() -> None:
    assert fromstring_bytes("") is None


def test_extract_accepts_public_tree_without_mutating_it() -> None:
    tree: Final = load_html("<html><body><article><p>Garden soil and planting observations.</p></article></body></html>")
    config: Final = use_config()
    config["DEFAULT"]["MIN_OUTPUT_SIZE"] = "0"
    config["DEFAULT"]["MIN_EXTRACTED_SIZE"] = "0"
    before: Final = etree.tostring(tree)
    assert (extract(tree, fast=True, config=config), etree.tostring(tree)) == (
        "Garden soil and planting observations.",
        before,
    )
