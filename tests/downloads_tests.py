# pylint:disable-msg=W1401
"""
Unit tests for download functions from the trafilatura library.
"""

import gzip
import logging
import os
import sys
import zlib

try:
    import brotli

    HAS_BROTLI = True
except ImportError:
    HAS_BROTLI = False

try:
    if sys.version_info >= (3, 14):
        from compression import zstd
    else:
        from backports import zstd

    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

from configparser import ConfigParser
from pathlib import Path
from time import sleep
from unittest.mock import MagicMock, patch

import pytest
from courlan import UrlStore

import trafilatura.downloads as dl
from trafilatura import utils
from trafilatura.cli import parse_args
from trafilatura.cli_utils import download_queue_processing, url_processing_pipeline
from trafilatura.core import Extractor, extract
from trafilatura.downloads import (
    DEFAULT_HEADERS,
    HAS_PYCURL,
    USER_AGENT,
    Response,
    _determine_headers,
    _initiate_pool,
    _is_suitable_response,
    _parse_curl_headers,
    _pycurl_is_live_page,
    _send_pycurl_request,
    _send_urllib_request,
    _urllib3_is_live_page,
    add_to_compressed_dict,
    fetch_url,
    is_live_page,
    load_download_buffer,
)
from trafilatura.settings import DEFAULT_CONFIG, args_to_extractor, use_config
from trafilatura.utils import MAX_MEMBERS, decode_file, handle_compressed_file, load_html

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# independent copy: must not mutate the session-wide DEFAULT_CONFIG
ZERO_CONFIG = use_config()
ZERO_CONFIG["DEFAULT"]["MIN_OUTPUT_SIZE"] = "0"
ZERO_CONFIG["DEFAULT"]["MIN_EXTRACTED_SIZE"] = "0"

RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources")
UA_CONFIG = use_config(filename=os.path.join(RESOURCES_DIR, "newsettings.cfg"))

DEFAULT_OPTS = Extractor(config=DEFAULT_CONFIG)


def _reset_downloads_global_objects():
    """
    Force global objects to be re-created
    """
    dl.PROXY_URL = None
    dl.HTTP_POOL = None
    dl.NO_CERT_POOL = None


@pytest.fixture(autouse=True)
def _reset_downloads_globals():
    "Reset cached download globals (pools, proxy) before and after every test."
    _reset_downloads_global_objects()
    yield
    _reset_downloads_global_objects()


def test_urllib_request_releases_conn_on_oversize():
    "regression: the connection is released even when MAX_FILE_SIZE aborts the stream mid-download."
    resp = MagicMock()
    resp.stream.return_value = iter([b"x" * (2**17)] * 1000)  # exceeds MAX_FILE_SIZE → ValueError mid-stream
    pool = MagicMock(request=MagicMock(return_value=resp))
    with patch.object(dl, "_initiate_pool", return_value=pool):
        assert _send_urllib_request("https://example.org", False, DEFAULT_CONFIG) is None
    resp.release_conn.assert_called_once()


@pytest.mark.parametrize(
    "geturl_result, expected",
    [
        # request URI passed down to the connection pool, no redirect involved
        ("/news/news", "https://example.org/news/news"),
        # raw Location header after a redirect, relative form is legal
        ("/section/", "https://example.org/section/"),
        ("https://example.com/elsewhere", "https://example.com/elsewhere"),
    ],
)
def test_urllib_request_resolves_relative_url(geturl_result, expected):
    "regression: a relative geturl() must not reach Response.url."
    resp = MagicMock(status=200)
    resp.stream.return_value = iter([b"<html><body><p>ABC</p></body></html>"])
    resp.geturl.return_value = geturl_result
    pool = MagicMock(request=MagicMock(return_value=resp))
    with patch.object(dl, "_initiate_pool", return_value=pool):
        result = _send_urllib_request("https://example.org/news/news", False, DEFAULT_CONFIG)
    assert result.url == expected


def test_response_object():
    "Test if the Response class is functioning as expected."
    my_html = b"<html><body><p>ABC</p></body></html>"
    resp = Response(my_html, 200, "https://example.org")
    assert bool(resp) is True
    resp.store_headers({"X-Header": "xyz"})
    assert "x-header" in resp.headers
    resp.decode_data(True)
    assert my_html.decode("utf-8") == resp.html == str(resp)
    my_dict = resp.as_dict()
    assert sorted(my_dict) == ["data", "headers", "html", "status", "url"]

    # response object: data, status, url
    response = Response("", 200, "https://httpbin.org/encoding/utf8")
    for size in (10000000, 1):
        response.data = b"ABC" * size
        assert _is_suitable_response(response.url, response, DEFAULT_OPTS) is False
    # straight handling of response object
    with open(os.path.join(RESOURCES_DIR, "utf8.html"), "rb") as filehandle:
        response.data = filehandle.read()
    assert _is_suitable_response(response.url, response, DEFAULT_OPTS) is True
    assert load_html(response) is not None
    # nothing to see here
    assert extract(response, url=response.url, config=ZERO_CONFIG) is None


@pytest.mark.filterwarnings("ignore::urllib3.exceptions.InsecureRequestWarning")
def test_is_live_page():
    """Test if pages are available on the network."""
    # is_live general tests
    assert _urllib3_is_live_page("https://httpbun.com/status/301") is True
    assert _urllib3_is_live_page("https://httpbun.com/status/404") is False
    assert is_live_page("https://httpbun.com/status/403") is False
    # is_live pycurl tests
    if HAS_PYCURL:
        assert _pycurl_is_live_page("https://httpbun.com/status/301") is True
        # connection failure exercises the pycurl HEAD error branch
        assert _pycurl_is_live_page("https://nonexistent.invalid.example/") is False


@pytest.mark.filterwarnings("ignore::urllib3.exceptions.InsecureRequestWarning")
# the empty-URL sanity check trips urllib3's scheme-less deprecation (v3 raises, downloads.py catches)
@pytest.mark.filterwarnings("ignore:URLs without a scheme:FutureWarning")
def test_fetch():
    """Test URL fetching."""
    # sanity check
    assert _send_urllib_request("", True, DEFAULT_CONFIG) is None

    # fetch_url
    assert fetch_url("#@1234") is None
    assert fetch_url("https://httpbun.com/status/404") is None

    # no SSL, no decoding
    url = "https://httpbun.com/status/200"
    for no_ssl in (True, False):
        response = _send_urllib_request(url, no_ssl, DEFAULT_CONFIG)
        assert b"200" in response.data
        assert b"OK" in response.data
        assert response.headers["x-powered-by"].startswith("httpbun")
    if HAS_PYCURL:
        response1 = _send_pycurl_request(url, True, DEFAULT_CONFIG)
        assert response1.headers["x-powered-by"].startswith("httpbun")
        assert _is_suitable_response(url, response1, DEFAULT_OPTS) is True
        assert _is_suitable_response(url, response, DEFAULT_OPTS) is True
        assert response1.data == response.data

    # test handling of redirects
    res = fetch_url("https://httpbun.com/redirect/2")
    assert len(res) > 100  # We followed redirects and downloaded something in the end
    new_config = use_config()  # get a new config instance to avoid mutating the default one
    # patch max directs: limit to 0. We won't fetch any page as a result
    new_config.set("DEFAULT", "MAX_REDIRECTS", "0")
    res = fetch_url("https://httpbun.com/redirect/1", config=new_config)
    assert res is None
    # also test max redir implementation on pycurl if available
    if HAS_PYCURL:
        assert _send_pycurl_request("https://httpbun.com/redirect/1", True, new_config) is None

    # test timeout
    new_config.set("DEFAULT", "DOWNLOAD_TIMEOUT", "1")
    args = ("https://httpbun.com/delay/2", True, new_config)
    assert _send_urllib_request(*args) is None
    if HAS_PYCURL:
        assert _send_pycurl_request(*args) is None

    # test MAX_FILE_SIZE
    size_config = use_config()
    size_config.set("DEFAULT", "MAX_FILE_SIZE", "1")
    args = ("https://httpbun.com/html", True, size_config)
    assert _send_urllib_request(*args) is None
    if HAS_PYCURL:
        assert _send_pycurl_request(*args) is None


def test_ssrf_protection():
    "SSRF filter blocks loopback, private, and link-local addresses."
    # unit: _normalize_ip
    import ipaddress
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    from trafilatura.downloads import _normalize_ip, _vet_peer

    assert _normalize_ip("127.0.0.1") == ipaddress.ip_address("127.0.0.1")
    assert _normalize_ip("::ffff:10.0.0.1") == ipaddress.ip_address("10.0.0.1")
    assert _normalize_ip("::1") == ipaddress.ip_address("::1")

    # unit: _vet_peer
    with pytest.raises(OSError, match="SSRF protection"):
        _vet_peer("10.0.0.1")
    _vet_peer("93.184.216.34")  # public: no exception

    # local server: the guard runs post-connect, so a live listener is needed
    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = b"<html><body><p>local</p></body></html>"
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/"
    config = ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    config.set("DEFAULT", "SSRF_PROTECTION", "off")

    try:
        # blocked by default
        assert _send_urllib_request(url, False, DEFAULT_CONFIG) is None
        # opt-out honored in the same process: no pool reset, the setting is not latched
        response = _send_urllib_request(url, False, config)
        assert response is not None
        assert response.status == 200
        # flipped back on without a reset: blocked again
        assert _send_urllib_request(url, False, DEFAULT_CONFIG) is None

        if HAS_PYCURL:
            assert _send_pycurl_request(url, False, DEFAULT_CONFIG) is None
            response = _send_pycurl_request(url, False, config)
            assert response is not None
            assert response.status == 200
            assert _pycurl_is_live_page(url) is False
            assert _pycurl_is_live_page(url, config) is True
        assert _urllib3_is_live_page(url) is False
        assert _urllib3_is_live_page(url, config) is True
        assert is_live_page(url) is False
        assert is_live_page(url, config) is True
    finally:
        server.shutdown()
        server.server_close()


def test_urllib3_live_page_retries(monkeypatch):
    "Long redirect chains count as live, transient statuses are retried, Retry-After sleeps are capped."
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    hits = []

    class _Handler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            hits.append(self.path)
            if self.path.startswith("/chain/") and self.path != "/chain/0":
                self.send_response(301)
                self.send_header("Location", f"/chain/{int(self.path[7:]) - 1}")
            elif (self.path == "/flaky" and hits.count("/flaky") == 1) or self.path == "/stall":
                self.send_response(503)
                self.send_header("Retry-After", "86400")
            else:
                self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    config = use_config()
    config.set("DEFAULT", "SSRF_PROTECTION", "off")
    naps = []
    monkeypatch.setattr(dl.urllib3.util.retry.time, "sleep", naps.append)

    try:
        assert _urllib3_is_live_page(f"{base}/chain/2", config) is True
        assert _urllib3_is_live_page(f"{base}/chain/3", config) is True
        assert _urllib3_is_live_page(f"{base}/flaky", config) is True
        assert naps == [dl.MAX_BACKOFF]
        naps.clear()
        assert _urllib3_is_live_page(f"{base}/stall", config) is False
        assert naps == [dl.MAX_BACKOFF, dl.MAX_BACKOFF]
    finally:
        server.shutdown()
        server.server_close()


def test_no_ssl_pool():
    "no_ssl skips cert verification in the urllib3 pool; the default verifies."
    insecure = _initiate_pool(DEFAULT_CONFIG, no_ssl=True)
    assert insecure.connection_pool_kw["cert_reqs"] == "CERT_NONE"
    assert insecure.connection_pool_kw["ca_certs"] is None
    secure = _initiate_pool(DEFAULT_CONFIG, no_ssl=False)
    assert secure.connection_pool_kw["cert_reqs"] == "CERT_REQUIRED"
    assert secure.connection_pool_kw["ca_certs"] is not None


def test_urllib_request_ssl_retry():
    "An SSLError triggers a retry with no_ssl=True, handled in fetch_response."
    import urllib3

    resp = MagicMock(status=200, headers={})
    resp.stream.return_value = [b"<html>ok</html>"]
    resp.geturl.return_value = "https://ssl.example/"
    # one pool, reused: first request raises SSLError, the retry succeeds
    pool = MagicMock(request=MagicMock(side_effect=[urllib3.exceptions.SSLError("bad cert"), resp]))
    with patch.object(dl, "_initiate_pool", return_value=pool), patch.object(dl, "HAS_PYCURL", False):
        assert dl.fetch_response("https://ssl.example/") is not None
    assert pool.request.call_count == 2

    # both attempts fail: None, exactly one retry
    pool = MagicMock(request=MagicMock(side_effect=urllib3.exceptions.SSLError("bad cert")))
    with patch.object(dl, "_initiate_pool", return_value=pool), patch.object(dl, "HAS_PYCURL", False):
        assert dl.fetch_response("https://ssl.example/") is None
    assert pool.request.call_count == 2

    # fallback disabled: no unverified retry
    config = use_config()
    config.set("DEFAULT", "INSECURE_SSL_FALLBACK", "off")
    pool = MagicMock(request=MagicMock(side_effect=[urllib3.exceptions.SSLError("bad cert"), resp]))
    with patch.object(dl, "_initiate_pool", return_value=pool), patch.object(dl, "HAS_PYCURL", False):
        assert dl.fetch_response("https://ssl.example/", config=config) is None
    assert pool.request.call_count == 1


def test_fetch_response_decode_cap():
    "The per-request MAX_FILE_SIZE reaches the decompression stage."
    body = gzip.compress(b"0" * 25_000_000)  # expands beyond the 20MB default cap

    def make_pool():
        resp = MagicMock(status=200, headers={})
        resp.stream.return_value = [body]
        resp.geturl.return_value = "https://example.org/"
        return MagicMock(request=MagicMock(return_value=resp))

    raised = ConfigParser()
    raised.read_dict(DEFAULT_CONFIG)
    raised.set("DEFAULT", "MAX_FILE_SIZE", "30000000")
    with patch.object(dl, "HAS_PYCURL", False), patch.object(dl, "_initiate_pool", return_value=make_pool()):
        assert dl.fetch_response("https://example.org/", decode=True, config=raised).html.startswith("000")
    with patch.object(dl, "HAS_PYCURL", False), patch.object(dl, "_initiate_pool", return_value=make_pool()):
        # default cap: decompression refused, raw bytes kept
        assert not dl.fetch_response("https://example.org/", decode=True).html.startswith("000")


def test_pycurl_ssl_retry(monkeypatch):
    "An SSL-class pycurl error triggers one retry with verification disabled."
    if not HAS_PYCURL:
        pytest.skip("pycurl not installed")
    import pycurl

    curl = MagicMock()  # one handle reused for both attempts
    state = {}

    def record_setopt(opt, value):
        if opt == pycurl.WRITEFUNCTION:
            state["write"] = value

    def perform():
        if "failed" not in state:
            state["failed"] = True
            raise pycurl.error(35, "SSL error")  # 35 ∈ CURL_SSL_ERRORS
        state["write"](b"<html>ok</html>")

    curl.setopt.side_effect = record_setopt
    curl.perform.side_effect = perform
    curl.getinfo.side_effect = [200, "https://ssl.example/"]  # consumed only by the retry's Response()
    monkeypatch.setattr(pycurl, "Curl", lambda: curl)

    resp = dl.fetch_response("https://ssl.example/")
    assert resp is not None
    assert resp.data == b"<html>ok</html>"
    assert curl.perform.call_count == 2


@pytest.mark.skipif(not HAS_PYCURL, reason="pycurl not installed")
def test_pycurl_status_retry(monkeypatch):
    "Transient statuses are retried with backoff."
    import pycurl

    curl = MagicMock()
    curl.getinfo.side_effect = [503, 200, "https://example.org/"]
    monkeypatch.setattr(pycurl, "Curl", lambda: curl)
    naps = []
    monkeypatch.setattr(dl, "sleep", naps.append)

    resp = _send_pycurl_request("https://example.org/", True, DEFAULT_CONFIG)
    assert resp is not None
    assert resp.status == 200
    assert curl.perform.call_count == 2
    assert naps == [15.0]  # backoff_factor = DOWNLOAD_TIMEOUT / 2


@pytest.mark.skipif(not HAS_PYCURL, reason="pycurl not installed")
def test_pycurl_proxy_skips_ssrf_hook(monkeypatch):
    "With a proxy, the SSRF opensocket hook must not be installed."
    import pycurl

    opts = {}
    curl = MagicMock()
    curl.setopt.side_effect = opts.__setitem__
    curl.getinfo.side_effect = [200, "https://example.org/"]
    monkeypatch.setattr(pycurl, "Curl", lambda: curl)
    monkeypatch.setattr(dl, "PROXY_URL", "socks5://localhost:1080")

    assert _send_pycurl_request("https://example.org/", True, DEFAULT_CONFIG) is not None
    assert pycurl.OPENSOCKETFUNCTION not in opts
    assert opts[pycurl.PRE_PROXY] == "socks5://localhost:1080"


def test_proxy_plumbing(monkeypatch):
    "PROXY_URL is honored: SOCKS manager gets the exact URL; unset -> plain pool."
    seen = {}
    monkeypatch.setattr(dl, "SOCKSProxyManager", lambda **kw: seen.update(kw), raising=False)
    monkeypatch.setattr(dl, "PROXY_URL", "socks5://user:pass@localhost:1080")
    dl.create_pool()
    assert seen["proxy_url"] == "socks5://user:pass@localhost:1080"
    monkeypatch.setattr(dl, "PROXY_URL", None)
    assert isinstance(dl.create_pool(), dl.urllib3.PoolManager)
    # proxy disables SSRF filtering on both backends
    assert dl._ssrf_active(DEFAULT_CONFIG) is True
    monkeypatch.setattr(dl, "PROXY_URL", "socks5://localhost:1080")
    assert dl._ssrf_active(DEFAULT_CONFIG) is False


@pytest.mark.skipif(not HAS_PYCURL, reason="pycurl not installed")
def test_pycurl_network(monkeypatch):
    "HTTP(S) only, PROXY_URL applied, SSRF hook skipped when libcurl reads a proxy from the environment."
    pycurl = dl.pycurl
    for var in dl.CURL_PROXY_VARS:
        monkeypatch.delenv(var, raising=False)

    def options():
        rec = {}
        dl._apply_curl_network(type("C", (), {"setopt": lambda s, o, v: rec.__setitem__(o, v)})(), DEFAULT_CONFIG)
        return rec

    rec = options()
    assert rec[pycurl.PROTOCOLS] == pycurl.PROTO_HTTP | pycurl.PROTO_HTTPS
    assert pycurl.PRE_PROXY not in rec
    assert rec[pycurl.OPENSOCKETFUNCTION] is dl._ssrf_opensocket
    monkeypatch.setenv("https_proxy", "http://10.0.0.5:3128")
    assert pycurl.OPENSOCKETFUNCTION not in options()
    monkeypatch.delenv("https_proxy")
    monkeypatch.setattr(dl, "PROXY_URL", "socks5://localhost:1080")
    rec = options()
    assert rec[pycurl.PRE_PROXY] == "socks5://localhost:1080"
    assert pycurl.OPENSOCKETFUNCTION not in rec


@pytest.mark.skipif(not HAS_PYCURL, reason="pycurl not installed")
def test_pycurl_local_schemes():
    "Non-HTTP schemes never reach the file system."
    assert _send_pycurl_request(Path(__file__).as_uri(), False, DEFAULT_CONFIG) is None
    assert dl._pycurl_is_live_page(Path(__file__).as_uri()) is False


def test_config():
    """Test how configuration options are read and stored."""
    # default accept-encoding
    accepted = ["deflate", "gzip"]
    if HAS_BROTLI:
        accepted.append("br")
    if HAS_ZSTD:
        accepted.append("zstd")
    # subset: urllib3/stdlib may advertise extra encodings (e.g. zstd on 3.14)
    assert set(accepted) <= set(DEFAULT_HEADERS["accept-encoding"].split(","))
    # default user-agent
    default = _determine_headers(DEFAULT_CONFIG)
    assert default["User-Agent"] == USER_AGENT
    assert "Cookie" not in default
    # user-agents rotation
    custom = _determine_headers(UA_CONFIG)
    assert custom["User-Agent"] in ["Chrome", "Firefox"]
    assert custom["Cookie"] == "yummy_cookie=choco; tasty_cookie=strawberry"


def zstd_stream_compress(data: bytes) -> bytes:
    "Compress data into a zstd frame which does not declare its content size."
    compressor = zstd.ZstdCompressor()
    return compressor.compress(data) + compressor.flush()


def test_partial_config_headers():
    "Configs missing USER_AGENTS or COOKIE must not crash header selection."
    partial = ConfigParser()
    partial.read_dict({"DEFAULT": {"USER_AGENTS": "Firefox"}})
    assert _determine_headers(partial) == {**DEFAULT_HEADERS, "User-Agent": "Firefox"}
    # nothing set: fall back to default headers
    assert _determine_headers(ConfigParser()) == DEFAULT_HEADERS


def test_parse_curl_headers():
    "Only the last response of a redirect chain should be kept."
    raw = (
        b"HTTP/1.1 301 Moved Permanently\r\n"
        b"Location: /final\r\n"
        b"\r\n"
        b"HTTP/2 200\r\n"
        b"Content-Type: text/html; charset=utf-8\r\n"
        b"X-Colon: a:b:c\r\n"
        b"junk line without separator\r\n"
        b"\r\n"
    )
    assert _parse_curl_headers(raw) == {
        "Content-Type": "text/html; charset=utf-8",
        "X-Colon": "a:b:c",
    }
    assert _parse_curl_headers(b"") == {}


def test_decode():
    """Test how responses are being decoded."""
    html_string = "<html><head/><body><div>ABC</div></body></html>"
    assert decode_file(b" ") is not None

    compressed_strings = [
        gzip.compress(html_string.encode("utf-8")),
        zlib.compress(html_string.encode("utf-8")),
    ]
    if HAS_BROTLI:
        compressed_strings.append(brotli.compress(html_string.encode("utf-8")))
    if HAS_ZSTD:
        compressed_strings.append(zstd.compress(html_string.encode("utf-8")))
        # servers compressing on the fly emit frames without a declared content
        # size, and concatenated frames are equally valid
        compressed_strings.append(zstd_stream_compress(html_string.encode("utf-8")))

    for compressed_string in compressed_strings:
        assert handle_compressed_file(compressed_string) == html_string.encode("utf-8")
        assert decode_file(compressed_string) == html_string

    # errors
    bad_files = ["äöüß", b"\x1f\x8b\x08abc", b"\x28\xb5\x2f\xfdabc"]
    if HAS_ZSTD:
        # a truncated frame decompresses to a prefix, which must not be mistaken
        # for the whole document
        truncated = zstd_stream_compress(html_string.encode("utf-8") * 500)
        bad_files.append(truncated[: len(truncated) // 2])
        # reserved bit set in the frame header descriptor (the byte after the
        # magic): rejected by the decompressor itself rather than by the
        # end-of-frame check
        frame = bytearray(zstd.compress(html_string.encode("utf-8")))
        frame[4] |= 0x08
        bad_files.append(bytes(frame))
    for bad_file in bad_files:
        assert handle_compressed_file(bad_file) == bad_file

    # multi-member gzip streams are concatenated (pigz/bgzip output)
    multi = gzip.compress(b"<html>part1 ") + gzip.compress(b"part2</html>")
    assert handle_compressed_file(multi) == b"<html>part1 part2</html>"

    # decompression-bomb guard: content expanding beyond MAX_FILE_SIZE is left unchanged
    bomb = gzip.compress(b"0" * 25_000_000)
    assert handle_compressed_file(bomb) == bomb
    # a raised per-request cap is honored
    assert handle_compressed_file(bomb, max_size=30_000_000) == b"0" * 25_000_000

    # member flood is rejected
    member = gzip.compress(b"a")
    flood = member * (MAX_MEMBERS + 1)
    assert handle_compressed_file(flood) == flood
    assert handle_compressed_file(member * MAX_MEMBERS) == b"a" * MAX_MEMBERS
    padded = gzip.compress(b"<html>a ") + b"\0" * 8 + gzip.compress(b"b</html>") + b"\0" * 8
    assert handle_compressed_file(padded) == b"<html>a b</html>"

    if HAS_ZSTD:
        multi_frame = zstd.compress(b"<html>a ") + zstd.compress(b"b</html>")
        assert handle_compressed_file(multi_frame) == b"<html>a b</html>"
        truncated = zstd.compress(html_string.encode("utf-8"))[:-4]
        assert handle_compressed_file(truncated) == truncated
        zstd_bomb = zstd.compress(b"0" * 25_000_000)
        assert handle_compressed_file(zstd_bomb) == zstd_bomb
    if HAS_BROTLI:
        brotli_bomb = brotli.compress(b"0" * 25_000_000)
        assert handle_compressed_file(brotli_bomb) == brotli_bomb
        # brotli < 1.2 is left unused: its output cannot be capped
        brotli_html = brotli.compress(b"<html>a</html>")
        assert handle_compressed_file(brotli_html) == b"<html>a</html>"
        with patch.object(utils, "HAS_BROTLI", False):
            assert handle_compressed_file(brotli_html) == brotli_html


@pytest.mark.usefixtures("mock_network")
def test_queue():
    "Test creation, modification and download of URL queues."
    # test conversion and storage
    url_store = add_to_compressed_dict(["ftps://www.example.org/", "http://"])
    assert isinstance(url_store, UrlStore)

    # blacklist and URL filter
    url_store = add_to_compressed_dict(
        ["https://example.org/page", "https://example.org/skip"], blacklist={"example.org/skip"}, url_filter=["/page"]
    )
    assert url_store.dump_urls() == ["https://example.org/page"]

    # response download buffer (empty input, no network)
    assert list(dl.buffered_response_downloads([], 1)) == []

    # download buffer
    inputurls = [f"https://test{i}.org/{j}" for i in range(1, 7) for j in range(1, 4)]
    url_store = add_to_compressed_dict(inputurls)
    bufferlist, _ = load_download_buffer(url_store, sleep_time=5)
    assert len(bufferlist) == 6
    sleep(0.25)
    bufferlist, _ = load_download_buffer(url_store, sleep_time=0.1)
    assert len(bufferlist) == 6

    # CLI args
    url_store = add_to_compressed_dict(["https://www.example.org/"])
    testargs = ["", "--list"]
    args = parse_args(testargs[1:])
    assert url_processing_pipeline(args, url_store) == 0

    # single/multiprocessing
    testargs = ["", "-v"]
    args = parse_args(testargs[1:])
    inputurls = [f"https://httpbun.com/status/{i}" for i in (301, 304, 200, 300, 400, 505)]
    url_store = add_to_compressed_dict(inputurls)
    args.archived = True
    args.config_file = os.path.join(RESOURCES_DIR, "newsettings.cfg")
    options = args_to_extractor(args)
    options.config["DEFAULT"]["SLEEP_TIME"] = "0.2"
    results = download_queue_processing(url_store, args, -1, options)
    assert len(results[0]) == 5
    assert results[1] == -1
