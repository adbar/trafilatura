"""Canned-response fixture: opt in per module with
`pytestmark = pytest.mark.usefixtures("mock_network")`."""

from pathlib import Path

import pytest

import trafilatura.downloads as dl
from trafilatura.downloads import Response

RESOURCES_DIR = Path(__file__).parent / "resources"


def _resource(name):
    return (RESOURCES_DIR / name).read_bytes()


# URL -> response bytes, or (bytes, final_url) to model a redirect.
CANNED_RESPONSES = {
    "https://example.org/": _resource("httpbin_sample.html"),
    "https://httpbun.com/html": _resource("httpbin_sample.html"),
    "https://httpbun.com/links/2/2": (
        b'<html><head><title>Links</title></head><body>'
        b'<a href="/links/2/0">0</a> <a href="/links/2/1">1</a> 2</body></html>'
    ),
    "https://www.w3.org/blog/feed/": (
        b'<?xml version="1.0" encoding="utf-8"?>'
        b'<feed xmlns="http://www.w3.org/2005/Atom"><title>W3C Blog</title>'
        b'<entry><link href="https://www.w3.org/blog/2024/a-post/"/></entry></feed>'
    ),
    "https://httpbun.com/redirect-to?url=https://example.org": (
        b"<html><body>redirected</body></html>",
        "https://example.org",
    ),
    "https://www.sitemaps.org/robots.txt": b"Sitemap: https://www.sitemaps.org/sitemap.xml",
    "https://www.sitemaps.org/sitemap.xml": _resource("sitemap.xml"),
    "https://sitemaps.org/sitemap.xml": _resource("sitemap.xml"),
}


def _fake_send(url, no_ssl, with_headers, config):
    canned = CANNED_RESPONSES.get(url)
    if canned is None:
        return None
    data, final_url = canned if isinstance(canned, tuple) else (canned, url)
    return Response(data, 200, final_url)


def _fake_is_live(url):
    return any(known.startswith(url.rstrip("/")) for known in CANNED_RESPONSES)


@pytest.fixture
def mock_network(monkeypatch):
    monkeypatch.setattr(dl, "_send_urllib_request", _fake_send)
    monkeypatch.setattr(dl, "_send_pycurl_request", _fake_send)
    monkeypatch.setattr(dl, "_urllib3_is_live_page", _fake_is_live)
    monkeypatch.setattr(dl, "_pycurl_is_live_page", _fake_is_live)
