# pylint:disable-msg=E0611,I1101
"""
All functions needed to steer and execute downloads of web documents.
"""

import ipaddress
import logging
import os
import random
import socket
from collections.abc import Callable, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from configparser import ConfigParser
from functools import partial
from importlib.metadata import version
from io import BytesIO
from time import sleep
from typing import Any
from urllib.parse import urljoin

import certifi
import urllib3
from courlan import UrlStore
from courlan.network import redirection_test

from .settings import DEFAULT_CONFIG, Extractor
from .utils import (
    URL_BLACKLIST_REGEX,
    Response,
    _capped,
    is_acceptable_length,
    make_chunks,
)

try:
    from urllib3.contrib.socks import SOCKSProxyManager

    PROXY_URL = os.environ.get("http_proxy")
except ImportError:
    PROXY_URL = None

try:
    import pycurl

    CURL_SHARE = pycurl.CurlShare()
    # available options:
    # https://curl.se/libcurl/c/curl_share_setopt.html
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_DNS)
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_SSL_SESSION)
    # not thread-safe
    # CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_CONNECT)
    HAS_PYCURL = True
except ImportError:
    HAS_PYCURL = False


LOGGER = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
HTTP_POOL = None
NO_CERT_POOL = None


def create_pool(ssrf_protection: bool = True, **args: Any) -> urllib3.PoolManager | Any:
    "Configure urllib3 download pool according to user-defined settings."
    if PROXY_URL:
        return SOCKSProxyManager(proxy_url=PROXY_URL, num_pools=50, **args)
    manager_class = _SafePoolManager if ssrf_protection else urllib3.PoolManager
    return manager_class(num_pools=50, **args)


def _apply_curl_proxy(curl: "pycurl.Curl") -> None:
    "Route the pycurl request through PROXY_URL when one is configured."
    if PROXY_URL:
        curl.setopt(pycurl.PRE_PROXY, PROXY_URL)


# advertises exactly the encodings urllib3 can decode
DEFAULT_HEADERS = urllib3.util.make_headers(accept_encoding=True)
USER_AGENT = "trafilatura/" + version("trafilatura") + " (+https://github.com/adbar/trafilatura)"
DEFAULT_HEADERS["User-Agent"] = USER_AGENT

# includes unofficial codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#Unofficial_codes
FORCE_STATUS = frozenset({429, 499, 500, 502, 503, 504, 509, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598})

CURL_SSL_ERRORS = {35, 54, 58, 59, 60, 64, 66, 77, 82, 83, 91}

# cap in seconds for backoff and Retry-After sleeps
MAX_BACKOFF = 30


class _SSLRetryError(Exception):
    "Internal signal: the secure transfer failed for SSL reasons, retry without verification."


def _normalize_ip(addr: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    "Parse an IP string, mapping IPv4-mapped IPv6 to plain IPv4."
    ip = ipaddress.ip_address(addr)
    return getattr(ip, "ipv4_mapped", None) or ip


def _ssrf_active(config: ConfigParser) -> bool:
    "SSRF filtering applies only to direct connections: with a proxy, the vetted address would be the proxy's."
    return not PROXY_URL and config.getboolean("DEFAULT", "SSRF_PROTECTION", fallback=True)


def _vet_peer(host: str) -> None:
    "Raise on a non-global peer address."
    if not _normalize_ip(host).is_global:
        raise OSError(f"SSRF protection: connection to non-public address blocked: {host}")


def _ssrf_opensocket(_purpose: int, address: Any) -> socket.socket:
    "pycurl OPENSOCKETFUNCTION that rejects non-global resolved IPs."
    _vet_peer(address.addr[0])
    return socket.socket(address.family, address.socktype, address.protocol)


class _SafeHTTPConnection(urllib3.connection.HTTPConnection):
    "Connection rejecting non-global peers, vetted post-connect so DNS rebinding cannot bypass it."

    def _new_conn(self) -> socket.socket:
        sock = super()._new_conn()
        try:
            _vet_peer(sock.getpeername()[0].split("%", 1)[0])  # strip IPv6 zone id
        except OSError as err:
            sock.close()
            # a connect error: aborts immediately under Retry(connect=0)
            raise urllib3.exceptions.NewConnectionError(self, str(err)) from err
        return sock


class _SafeHTTPSConnection(_SafeHTTPConnection, urllib3.connection.HTTPSConnection):
    pass


class _SafeHTTPConnectionPool(urllib3.HTTPConnectionPool):
    ConnectionCls = _SafeHTTPConnection


class _SafeHTTPSConnectionPool(urllib3.HTTPSConnectionPool):
    ConnectionCls = _SafeHTTPSConnection


class _SafePoolManager(urllib3.PoolManager):
    "PoolManager whose connections reject non-global IP addresses on every hop."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.pool_classes_by_scheme = {"http": _SafeHTTPConnectionPool, "https": _SafeHTTPSConnectionPool}


def _determine_headers(config: ConfigParser) -> dict[str, str]:
    "Overlay user-agent and cookie from the config file on the default headers."
    headers = dict(DEFAULT_HEADERS)
    # rotate over a series of user-agents
    if myagents := config.get("DEFAULT", "USER_AGENTS", fallback="").strip():
        headers["User-Agent"] = random.choice(myagents.splitlines())
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
    # todo: support for several cookies?
    if mycookie := config.get("DEFAULT", "COOKIE", fallback=None):
        headers["Cookie"] = mycookie
    return headers


def _get_retry_strategy(config: ConfigParser) -> urllib3.util.Retry:
    "Define a retry strategy according to the config file."
    max_redirects = config.getint("DEFAULT", "MAX_REDIRECTS")
    return urllib3.util.Retry(
        total=max_redirects,
        redirect=max_redirects,  # raise_on_redirect=False,
        connect=0,
        backoff_factor=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT") / 2,
        backoff_max=MAX_BACKOFF,
        retry_after_max=MAX_BACKOFF,
        status_forcelist=FORCE_STATUS,
    )


def _initiate_pool(config: ConfigParser, no_ssl: bool = False) -> urllib3.PoolManager | Any:
    "Create a urllib3 pool manager according to options in the config file and HTTPS setting."
    global HTTP_POOL, NO_CERT_POOL
    ssrf_protection = _ssrf_active(config)
    pool = NO_CERT_POOL if no_ssl else HTTP_POOL

    # never latch the SSRF setting
    if pool is None or isinstance(pool, _SafePoolManager) != ssrf_protection:
        pool = create_pool(
            ssrf_protection=ssrf_protection,
            ca_certs=None if no_ssl else certifi.where(),
            cert_reqs="CERT_NONE" if no_ssl else "CERT_REQUIRED",
        )
        if no_ssl:
            NO_CERT_POOL = pool
        else:
            HTTP_POOL = pool

    return pool


def _send_urllib_request(url: str, no_ssl: bool, config: ConfigParser) -> Response | None:
    "Internal function to robustly send a request (SSL or not) and return its result."
    try:
        pool_manager = _initiate_pool(config, no_ssl=no_ssl)

        # execute request, stop downloading as soon as MAX_FILE_SIZE is reached
        response = pool_manager.request(
            "GET",
            url,
            headers=_determine_headers(config),
            retries=_get_retry_strategy(config),
            timeout=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"),
            preload_content=False,
        )
        try:
            # stream() yields decoded chunks: the cap applies to decompressed bytes
            data = _capped(response.stream(2**17), config.getint("DEFAULT", "MAX_FILE_SIZE"))
        finally:
            response.release_conn()

        # necessary for standardization
        # geturl() returns the raw Location header after a redirect and the request
        # URI otherwise, both of which can be relative
        resp = Response(data, response.status, urljoin(url, response.geturl() or url))
        resp.store_headers(response.headers)
        return resp

    except (urllib3.exceptions.SSLError, urllib3.exceptions.MaxRetryError) as err:
        # handshake failures surface as MaxRetryError with an SSLError reason
        cause = err.reason if isinstance(err, urllib3.exceptions.MaxRetryError) else err
        if not no_ssl and isinstance(cause, urllib3.exceptions.SSLError):
            raise _SSLRetryError(str(err)) from err
        LOGGER.error("download error: %s %s", url, err)
    except Exception as err:
        LOGGER.error("download error: %s %s", url, err)  # sys.exc_info()[0]

    return None


def _is_suitable_response(url: str, response: Response, options: Extractor) -> bool:
    "Check if the response conforms to formal criteria."
    if response.status != 200:
        LOGGER.error("not a 200 response: %s for URL %s", response.status, url)
        return False
    return is_acceptable_length(len(response.html or response.data or ""), options)


def fetch_url(
    url: str,
    no_ssl: bool = False,
    config: ConfigParser = DEFAULT_CONFIG,
    options: Extractor | None = None,
) -> str | None:
    """Downloads a web page and seamlessly decodes the response.

    Args:
        url: URL of the page to fetch.
        no_ssl: Do not try to establish a secure connection (to prevent SSLError).
        config: Pass configuration values for output control.
        options: Extraction options (supersedes config).

    Returns:
        Unicode string or None in case of failed downloads and invalid results.

    """
    config = options.config if options else config
    response = fetch_response(url, decode=True, no_ssl=no_ssl, config=config)
    if not response or not response.data:
        return None
    options = options or Extractor(config=config)
    return response.html if _is_suitable_response(url, response, options) else None


def fetch_response(
    url: str,
    *,
    decode: bool = False,
    no_ssl: bool = False,
    with_headers: bool = False,  # noqa: ARG001  # deprecated, kept for API compatibility
    config: ConfigParser = DEFAULT_CONFIG,
) -> Response | None:
    """Downloads a web page and returns a full response object.

    Args:
        url: URL of the page to fetch.
        decode: Use html attribute to decode the data (boolean).
        no_ssl: Don't try to establish a secure connection (to prevent SSLError).
        with_headers: Deprecated and ignored, headers are always stored.
        config: Pass configuration values for output control.

    Returns:
        Response object or None in case of failed downloads and invalid results.

    """
    dl_function = _send_pycurl_request if HAS_PYCURL else _send_urllib_request
    LOGGER.debug("sending request: %s", url)
    try:
        response = dl_function(url, no_ssl, config)
    except _SSLRetryError as err:
        # senders raise only when verification was on, so this cannot recurse
        LOGGER.warning("retrying after SSL error: %s %s", url, err)
        response = dl_function(url, True, config)
    if not response:  # None or data missing
        LOGGER.debug("request failed: %s", url)
        return None
    response.decode_data(decode, config.getint("DEFAULT", "MAX_FILE_SIZE"))
    return response


def _pycurl_is_live_page(url: str) -> bool:
    "Send a basic HTTP HEAD request with pycurl."
    # Initialize pycurl object
    curl = pycurl.Curl()
    # Set the URL and HTTP method (HEAD)
    curl.setopt(pycurl.URL, url.encode("utf-8"))
    curl.setopt(pycurl.CONNECTTIMEOUT, 10)
    curl.setopt(pycurl.TIMEOUT, 30)
    curl.setopt(pycurl.USERAGENT, USER_AGENT)
    # follow redirects to test the final page, like the urllib3 fallback
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)
    # no SSL verification
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    # Set option to avoid getting the response body
    curl.setopt(pycurl.NOBODY, True)
    _apply_curl_proxy(curl)
    try:
        curl.perform()
        # int(): getinfo is untyped
        return int(curl.getinfo(pycurl.RESPONSE_CODE)) < 400
    except pycurl.error as err:
        LOGGER.debug("pycurl HEAD error: %s %s", url, err)
        return False
    finally:
        curl.close()


def _urllib3_is_live_page(url: str) -> bool:
    "Use courlan redirection test (based on urllib3) to send a HEAD request."
    try:
        redirection_test(url)
    except Exception as err:
        LOGGER.debug("urllib3 HEAD error: %s %s", url, err)
        return False
    return True


def is_live_page(url: str) -> bool:
    "Send a HTTP HEAD request without taking anything else into account."
    result = _pycurl_is_live_page(url) if HAS_PYCURL else False
    # use urllib3 as backup
    return result or _urllib3_is_live_page(url)


def add_to_compressed_dict(
    inputlist: list[str],
    blacklist: set[str] | None = None,
    url_filter: list[str] | None = None,
    url_store: UrlStore | None = None,
    compression: bool = False,
    verbose: bool = False,
) -> UrlStore:
    """Filter, convert input URLs and add them to domain-aware processing dictionary"""
    if url_store is None:
        url_store = UrlStore(compressed=compression, strict=False, verbose=verbose)

    inputlist = list(dict.fromkeys(inputlist))

    if blacklist:
        inputlist = [u for u in inputlist if URL_BLACKLIST_REGEX.sub("", u) not in blacklist]

    if url_filter:
        inputlist = [u for u in inputlist if any(f in u for f in url_filter)]

    url_store.add_urls(inputlist)
    return url_store


def load_download_buffer(url_store: UrlStore, sleep_time: float = 5.0) -> tuple[list[str], UrlStore]:
    """Determine threading strategy and draw URLs respecting domain-based back-off rules."""
    while True:
        bufferlist = url_store.get_download_urls(time_limit=sleep_time, max_urls=10**5)
        if bufferlist or url_store.done:
            break
        sleep(sleep_time)
    return bufferlist, url_store


def _buffered_downloads(
    bufferlist: list[str],
    download_threads: int,
    worker: Callable[[str], Any],
    chunksize: int = 10000,  # max URLs materialized per batch (bounds in-flight futures)
) -> Generator[tuple[str, Any], None, None]:
    "Use a thread pool to perform a series of downloads."
    with ThreadPoolExecutor(max_workers=download_threads) as executor:
        for chunk in make_chunks(bufferlist, chunksize):
            future_to_url = {executor.submit(worker, url): url for url in chunk}
            for future in as_completed(future_to_url):
                yield future_to_url[future], future.result()


def buffered_downloads(
    bufferlist: list[str],
    download_threads: int,
    options: Extractor | None = None,
) -> Generator[tuple[str, str], None, None]:
    "Download queue consumer, single- or multi-threaded."
    worker = partial(fetch_url, options=options)

    return _buffered_downloads(bufferlist, download_threads, worker)


def buffered_response_downloads(
    bufferlist: list[str],
    download_threads: int,
    options: Extractor | None = None,
) -> Generator[tuple[str, Response], None, None]:
    "Download queue consumer, returns full Response objects."
    config = options.config if options else DEFAULT_CONFIG
    worker = partial(fetch_response, config=config)

    return _buffered_downloads(bufferlist, download_threads, worker)


def _parse_curl_headers(raw: bytes) -> dict[str, str]:
    "Parse accumulated header bytes, keeping only the last response of a redirect chain."
    # https://github.com/pycurl/pycurl/blob/master/examples/quickstart/response_headers.py
    # This will botch headers that are split on multiple lines...
    headers: dict[str, str] = {}
    for line in raw.decode("iso-8859-1", errors="replace").splitlines():
        # a new status line marks the next response in a redirect chain
        if line.startswith("HTTP/"):
            headers = {}
            continue
        name, sep, value = line.partition(":")
        if sep:
            headers[name.strip()] = value.strip()
    return headers


def _send_pycurl_request(url: str, no_ssl: bool, config: ConfigParser) -> Response | None:
    """Experimental function using libcurl and pycurl to speed up downloads"""
    # https://github.com/pycurl/pycurl/blob/master/examples/retriever-multi.py

    # init, let libcurl advertise and decompress the encodings it supports
    headerlist = [
        f"{header}: {content}" for header, content in _determine_headers(config).items() if header.lower() != "accept-encoding"
    ]

    # prepare curl request
    # https://curl.haxx.se/libcurl/c/curl_easy_setopt.html
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url.encode("utf-8"))
    # share data
    curl.setopt(pycurl.SHARE, CURL_SHARE)
    curl.setopt(pycurl.HTTPHEADER, headerlist)
    curl.setopt(pycurl.ACCEPT_ENCODING, "")
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, config.getint("DEFAULT", "MAX_REDIRECTS"))
    curl.setopt(pycurl.REDIR_PROTOCOLS, pycurl.PROTO_HTTP | pycurl.PROTO_HTTPS)
    curl.setopt(pycurl.CONNECTTIMEOUT, config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"))
    curl.setopt(pycurl.TIMEOUT, config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"))
    # pre-transfer abort on a known Content-Length; the write callback is the actual enforcement
    max_file_size = config.getint("DEFAULT", "MAX_FILE_SIZE")
    curl.setopt(pycurl.MAXFILESIZE, max_file_size)
    curl.setopt(pycurl.NOSIGNAL, 1)

    # short write aborts the transfer once the decoded body exceeds the cap
    bodybytes = bytearray()

    def _capped_write(chunk: bytes) -> int | None:
        bodybytes.extend(chunk)
        return 0 if len(bodybytes) > max_file_size else None

    curl.setopt(pycurl.WRITEFUNCTION, _capped_write)

    if no_ssl:
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    else:
        curl.setopt(pycurl.CAINFO, certifi.where())

    headerbytes = BytesIO()
    curl.setopt(pycurl.HEADERFUNCTION, headerbytes.write)

    _apply_curl_proxy(curl)

    if _ssrf_active(config):
        curl.setopt(pycurl.OPENSOCKETFUNCTION, _ssrf_opensocket)

    # send request, retrying on transient statuses like the urllib3 retry strategy
    retries = config.getint("DEFAULT", "MAX_REDIRECTS")
    backoff_factor = config.getint("DEFAULT", "DOWNLOAD_TIMEOUT") / 2
    status = 0  # the loop is empty if MAX_REDIRECTS < 0
    try:
        for attempt in range(retries + 1):
            if attempt:
                sleep(min(MAX_BACKOFF, backoff_factor * 2 ** (attempt - 1)))
                headerbytes.seek(0)
                headerbytes.truncate()
                bodybytes.clear()
            curl.perform()
            status = curl.getinfo(pycurl.RESPONSE_CODE)
            if status not in FORCE_STATUS:
                break
            LOGGER.debug("retrying after status %s: %s", status, url)
        resp = Response(bytes(bodybytes), status, curl.getinfo(pycurl.EFFECTIVE_URL))
    except pycurl.error as err:
        # SSL-related error class, see https://curl.se/libcurl/c/libcurl-errors.html
        # additional error codes: 80, 90, 96, 98
        if not no_ssl and err.args[0] in CURL_SSL_ERRORS:
            raise _SSLRetryError(str(err)) from err
        LOGGER.error("pycurl error: %s %s", url, err)
        return None
    finally:
        curl.close()

    resp.store_headers(_parse_curl_headers(headerbytes.getvalue()))
    return resp
