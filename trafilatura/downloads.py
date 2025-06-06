# pylint:disable-msg=E0611,I1101
"""
All functions needed to steer and execute downloads of web documents.
"""

import logging
import os
import random

from concurrent.futures import ThreadPoolExecutor, as_completed
from configparser import ConfigParser
from functools import partial
from importlib.metadata import version
from io import BytesIO
from time import sleep
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import certifi
import urllib3

from courlan import UrlStore
from courlan.network import redirection_test

from .settings import DEFAULT_CONFIG, Extractor
from .utils import URL_BLACKLIST_REGEX, decode_file, is_acceptable_length, make_chunks

try:
    from urllib3.contrib.socks import SOCKSProxyManager

    PROXY_URL = os.environ.get("http_proxy")
except ImportError:
    PROXY_URL = None

try:
    import pycurl  # type: ignore

    CURL_SHARE = pycurl.CurlShare()
    # available options:
    # https://curl.se/libcurl/c/curl_share_setopt.html
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_DNS)
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_SSL_SESSION)
    # not thread-safe
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_CONNECT)
    HAS_PYCURL = True
except ImportError:
    HAS_PYCURL = False

LOGGER = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
HTTP_POOL = None
NO_CERT_POOL = None
RETRY_STRATEGY = None
_POOL_CACHE = {}  # key: (no_ssl, effective_proxy), value: pool



def create_pool(proxy: Optional[str] = None, **args: Any) -> Union[urllib3.PoolManager, Any]:
    "Configure urllib3 download pool according to user-defined settings."
    # Use the passed proxy if given, otherwise fall back to PROXY_URL.
    proxy_value = proxy if proxy is not None else PROXY_URL

    if proxy_value:
        # If the proxy URL indicates a SOCKS proxy, use SOCKSProxyManager.
        if proxy_value.lower().startswith("socks"):
            try:
                from urllib3.contrib.socks import SOCKSProxyManager
                manager_class = SOCKSProxyManager
            except ImportError as e:
                raise ImportError("SOCKSProxyManager is not available. "
                                  "Please install the required dependency (e.g., via pip install urllib3[socks]).") from e
        else:
            # Otherwise, assume it's an HTTP/HTTPS proxy and use ProxyManager.
            from urllib3 import ProxyManager
            manager_class = ProxyManager
        manager_args = {"proxy_url": proxy_value}
    else:
        # No proxy specified: use the default PoolManager.
        manager_class = urllib3.PoolManager
        manager_args = {}

    # Set the number of pools.
    manager_args["num_pools"] = 50  # type: ignore[assignment]
    return manager_class(**manager_args, **args)


DEFAULT_HEADERS = urllib3.util.make_headers(accept_encoding=True)  # type: ignore[no-untyped-call]
USER_AGENT = "trafilatura/" + version("trafilatura") + " (+https://github.com/adbar/trafilatura)"
DEFAULT_HEADERS["User-Agent"] = USER_AGENT

FORCE_STATUS = [
    429,
    499,
    500,
    502,
    503,
    504,
    509,
    520,
    521,
    522,
    523,
    524,
    525,
    526,
    527,
    530,
    598,
]

CURL_SSL_ERRORS = {35, 54, 58, 59, 60, 64, 66, 77, 82, 83, 91}


class Response:
    "Store information gathered in a HTTP response object."
    __slots__ = ["data", "headers", "html", "status", "url"]

    def __init__(self, data: bytes, status: int, url: str) -> None:
        self.data = data
        self.headers: Optional[Dict[str, str]] = None
        self.html: Optional[str] = None
        self.status = status
        self.url = url

    def __bool__(self) -> bool:
        return self.data is not None

    def __repr__(self) -> str:
        return self.html or decode_file(self.data)

    def store_headers(self, headerdict: Dict[str, str]) -> None:
        "Store response headers if required."
        # further control steps here
        self.headers = {k.lower(): v for k, v in headerdict.items()}

    def decode_data(self, decode: bool) -> None:
        "Decode the bytestring in data and store a string in html."
        if decode and self.data:
            self.html = decode_file(self.data)

    def as_dict(self) -> Dict[str, str]:
        "Convert the response object to a dictionary."
        return {attr: getattr(self, attr) for attr in self.__slots__}


def _parse_config(config: ConfigParser) -> Tuple[Optional[List[str]], Optional[str]]:
    "Read and extract HTTP header strings from the configuration file."
    # load a series of user-agents
    myagents = config.get("DEFAULT", "USER_AGENTS", fallback="").strip()
    agent_list = myagents.splitlines() if myagents else None
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
    # todo: support for several cookies?
    mycookie = config.get("DEFAULT", "COOKIE") or None
    return agent_list, mycookie


def _determine_headers(
    config: ConfigParser, headers: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    "Internal function to decide on user-agent string."
    if config != DEFAULT_CONFIG:
        myagents, mycookie = _parse_config(config)
        headers = {}
        if myagents:
            headers["User-Agent"] = random.choice(myagents)
        if mycookie:
            headers["Cookie"] = mycookie
    return headers or DEFAULT_HEADERS


def _get_retry_strategy(config: ConfigParser) -> urllib3.util.Retry:
    "Define a retry strategy according to the config file."
    global RETRY_STRATEGY
    if not RETRY_STRATEGY:
        # or RETRY_STRATEGY.redirect != config.getint("DEFAULT", "MAX_REDIRECTS")
        RETRY_STRATEGY = urllib3.util.Retry(
            total=config.getint("DEFAULT", "MAX_REDIRECTS"),
            redirect=config.getint("DEFAULT", "MAX_REDIRECTS"),
            connect=0,
            backoff_factor=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT") / 2,
            status_forcelist=FORCE_STATUS,
        )
    return RETRY_STRATEGY


def _initiate_pool(
    config: ConfigParser, no_ssl: bool = False, proxy: Optional[str] = None
) -> Union[urllib3.PoolManager, Any]:
    """
    Create (or retrieve from cache) a urllib3 pool manager according to options in the
    config file, taking into account SSL settings and the effective proxy to use.

    Args:
        config: The configuration object (ConfigParser) with settings.
        no_ssl: If True, do not use SSL certificates.
        proxy: Optional proxy URL to override the global PROXY_URL.

    Returns:
        A pool manager instance (e.g., ProxyManager or PoolManager) ready for requests.
    """
    # Determine the effective proxy: use the provided proxy if available,
    # otherwise fall back to the global PROXY_URL.
    effective_proxy = proxy if proxy is not None else PROXY_URL

    # Create a cache key based on the no_ssl flag and the effective proxy value.
    key = (no_ssl, effective_proxy)
    LOGGER.debug("Initiating pool with no_ssl=%s and effective_proxy=%s (cache key: %s)", no_ssl, effective_proxy, key)

    # If we already have a pool for this key, return it.
    if key in _POOL_CACHE:
        LOGGER.debug("Using cached pool for key: %s", key)
        return _POOL_CACHE[key]

    # Otherwise, create a new pool.
    pool = create_pool(
        proxy=effective_proxy,
        timeout=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"),
        ca_certs=None if no_ssl else certifi.where(),
        cert_reqs="CERT_NONE" if no_ssl else "CERT_REQUIRED",
    )
    _POOL_CACHE[key] = pool
    LOGGER.debug("Created new pool and cached for key: %s", key)
    return pool


def _send_urllib_request(
    url: str, no_ssl: bool, with_headers: bool, config: ConfigParser, proxy: Optional[str] = None
) -> Optional[Response]:
    "Internal function to robustly send a request (SSL or not) and return its result."
    try:
        pool_manager = _initiate_pool(config, no_ssl=no_ssl, proxy=proxy)
        response = pool_manager.request(
            "GET",
            url,
            headers=_determine_headers(config),
            retries=_get_retry_strategy(config),
            preload_content=False,
        )
        data = bytearray()
        for chunk in response.stream(2**17):
            data.extend(chunk)
            if len(data) > config.getint("DEFAULT", "MAX_FILE_SIZE"):
                raise ValueError("MAX_FILE_SIZE exceeded")
        response.release_conn()

        # necessary for standardization
        resp = Response(bytes(data), response.status, response.geturl())
        if with_headers:
            resp.store_headers(response.headers)
        return resp

    except urllib3.exceptions.SSLError:
        LOGGER.warning("retrying after SSLError: %s", url)
        return _send_urllib_request(url, True, with_headers, config, proxy=proxy)
    except Exception as err:
        LOGGER.error("download error: %s %s", url, err)
    return None


def _is_suitable_response(url: str, response: Response, options: Extractor) -> bool:
    "Check if the response conforms to formal criteria."
    lentest = len(response.html or response.data or "")
    if response.status != 200:
        LOGGER.error("not a 200 response: %s for URL %s", response.status, url)
        return False
    if not is_acceptable_length(lentest, options):
        return False
    return True


def _handle_response(
    url: str, response: Response, decode: bool, options: Extractor
) -> Optional[Union[Response, str]]:
    "Internal function to run safety checks on response result."
    if _is_suitable_response(url, response, options):
        return response.html if decode else response
    return None


def fetch_url(
    url: str,
    no_ssl: bool = False,
    config: ConfigParser = DEFAULT_CONFIG,
    options: Optional[Extractor] = None,
    proxy: Optional[str] = None,
) -> Optional[str]:
    """Downloads a web page and seamlessly decodes the response.

    Args:
        url: URL of the page to fetch.
        no_ssl: Do not try to establish a secure connection (to prevent SSLError).
        config: Pass configuration values for output control.
        options: Extraction options (supersedes config).
        proxy: Optional proxy URL to use for the request.

    Returns:
        Unicode string or None in case of failed downloads and invalid results.
    """
    config = options.config if options else config
    response = fetch_response(url, decode=True, no_ssl=no_ssl, config=config, proxy=proxy)
    if response and response.data:
        if not options:
            options = Extractor(config=config)
        if _is_suitable_response(url, response, options):
            return response.html
    return None


def fetch_response(
    url: str,
    *,
    decode: bool = False,
    no_ssl: bool = False,
    with_headers: bool = False,
    config: ConfigParser = DEFAULT_CONFIG,
    proxy: Optional[str] = None,
) -> Optional[Response]:
    """Downloads a web page and returns a full response object.

    Args:
        url: URL of the page to fetch.
        decode: Use html attribute to decode the data (boolean).
        no_ssl: Don't try to establish a secure connection (to prevent SSLError).
        with_headers: Keep track of the response headers.
        config: Pass configuration values for output control.
        proxy: Optional proxy URL to use for the request.

    Returns:
        Response object or None in case of failed downloads and invalid results.
    """
    dl_function = _send_urllib_request if not HAS_PYCURL else _send_pycurl_request
    LOGGER.debug("sending request: %s", url)
    response = dl_function(url, no_ssl, with_headers, config, proxy=proxy)
    if not response:
        LOGGER.debug("request failed: %s", url)
        return None
    response.decode_data(decode)
    return response


def _pycurl_is_live_page(url: str) -> bool:
    "Send a basic HTTP HEAD request with pycurl."
    page_exists = False
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url.encode("utf-8"))
    curl.setopt(pycurl.CONNECTTIMEOUT, 10)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.setopt(curl.NOBODY, True)
    if PROXY_URL:
        curl.setopt(pycurl.PRE_PROXY, PROXY_URL)
    try:
        curl.perform()
        page_exists = curl.getinfo(curl.RESPONSE_CODE) < 400
    except pycurl.error as err:
        LOGGER.debug("pycurl HEAD error: %s %s", url, err)
        page_exists = False
    curl.close()
    return page_exists


def _urllib3_is_live_page(url: str) -> bool:
    "Use courlan redirection test (based on urllib3) to send a HEAD request."
    try:
        _ = redirection_test(url)
    except Exception as err:
        LOGGER.debug("urllib3 HEAD error: %s %s", url, err)
        return False
    return True


def is_live_page(url: str) -> bool:
    "Send a HTTP HEAD request without taking anything else into account."
    result = _pycurl_is_live_page(url) if HAS_PYCURL else False
    return result or _urllib3_is_live_page(url)


def add_to_compressed_dict(
    inputlist: List[str],
    blacklist: Optional[Set[str]] = None,
    url_filter: Optional[str] = None,
    url_store: Optional[UrlStore] = None,
    compression: bool = False,
    verbose: bool = False,
) -> UrlStore:
    """Filter, convert input URLs and add them to domain-aware processing dictionary"""
    if url_store is None:
        url_store = UrlStore(compressed=compression, strict=False, verbose=verbose)

    inputlist = list(dict.fromkeys(inputlist))

    if blacklist:
        inputlist = [
            u for u in inputlist if URL_BLACKLIST_REGEX.sub("", u) not in blacklist
        ]

    if url_filter:
        inputlist = [u for u in inputlist if any(f in u for f in url_filter)]

    url_store.add_urls(inputlist)
    return url_store


def load_download_buffer(
    url_store: UrlStore, sleep_time: float = 5.0
) -> Tuple[List[str], UrlStore]:
    """Determine threading strategy and draw URLs respecting domain-based back-off rules."""
    while True:
        bufferlist = url_store.get_download_urls(time_limit=sleep_time, max_urls=10**5)
        if bufferlist or url_store.done:
            break
        sleep(sleep_time)
    return bufferlist, url_store


def _buffered_downloads(
    bufferlist: List[str],
    download_threads: int,
    worker: Callable[[str], Any],
    chunksize: int = 10000,
) -> Generator[Tuple[str, Any], None, None]:
    "Use a thread pool to perform a series of downloads."
    with ThreadPoolExecutor(max_workers=download_threads) as executor:
        for chunk in make_chunks(bufferlist, chunksize):
            future_to_url = {executor.submit(worker, url): url for url in chunk}
            for future in as_completed(future_to_url):
                yield future_to_url[future], future.result()


def buffered_downloads(
    bufferlist: List[str],
    download_threads: int,
    options: Optional[Extractor] = None,
    proxy: Optional[str] = None,
) -> Generator[Tuple[str, str], None, None]:
    """
    Download queue consumer, single- or multi-threaded.
    
    Args:
        bufferlist: A list of URLs to download.
        download_threads: The number of threads to use.
        options: Extraction options (contains config, etc.).
        proxy: Optional proxy URL to use for all downloads.
        
    Returns:
        A generator yielding tuples of (URL, downloaded HTML text).
    """
    worker = partial(fetch_url, options=options, proxy=proxy)
    return _buffered_downloads(bufferlist, download_threads, worker)


def buffered_response_downloads(
    bufferlist: List[str],
    download_threads: int,
    options: Optional[Extractor] = None,
    proxy: Optional[str] = None,
) -> Generator[Tuple[str, Response], None, None]:
    """
    Download queue consumer, returns full Response objects.
    
    Args:
        bufferlist: A list of URLs to download.
        download_threads: The number of threads to use.
        options: Extraction options (contains config, etc.).
        proxy: Optional proxy URL to use for all downloads.
        
    Returns:
        A generator yielding tuples of (URL, Response object).
    """
    config = options.config if options else DEFAULT_CONFIG
    worker = partial(fetch_response, config=config, proxy=proxy)
    return _buffered_downloads(bufferlist, download_threads, worker)


def _send_pycurl_request(
    url: str, no_ssl: bool, with_headers: bool, config: ConfigParser, proxy: Optional[str] = None
) -> Optional[Response]:
    """Experimental function using libcurl and pycurl to speed up downloads"""
    headerlist = [
        f"{header}: {content}" for header, content in _determine_headers(config).items()
    ]
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url.encode("utf-8"))
    # share data
    curl.setopt(pycurl.SHARE, CURL_SHARE)
    curl.setopt(pycurl.HTTPHEADER, headerlist)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, config.getint("DEFAULT", "MAX_REDIRECTS"))
    curl.setopt(pycurl.CONNECTTIMEOUT, config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"))
    curl.setopt(pycurl.TIMEOUT, config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"))
    curl.setopt(pycurl.MAXFILESIZE, config.getint("DEFAULT", "MAX_FILE_SIZE"))
    curl.setopt(pycurl.NOSIGNAL, 1)

    if no_ssl is True:
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    else:
        curl.setopt(pycurl.CAINFO, certifi.where())

    if with_headers:
        headerbytes = BytesIO()
        curl.setopt(pycurl.HEADERFUNCTION, headerbytes.write)

    # Use the passed proxy if available; otherwise, fall back to the global PROXY_URL.
    if proxy:
        curl.setopt(pycurl.PRE_PROXY, proxy)
    elif PROXY_URL:
        curl.setopt(pycurl.PRE_PROXY, PROXY_URL)

    try:
        bufferbytes = curl.perform_rb()
    except pycurl.error as err:
        LOGGER.error("pycurl error: %s %s", url, err)
        if no_ssl is False and err.args[0] in CURL_SSL_ERRORS:
            LOGGER.debug("retrying after SSL error: %s %s", url, err)
            return _send_pycurl_request(url, True, with_headers, config, proxy=proxy)
        return None

    resp = Response(
        bufferbytes, curl.getinfo(curl.RESPONSE_CODE), curl.getinfo(curl.EFFECTIVE_URL)
    )
    curl.close()

    if with_headers:
        respheaders = {}
        for line in (
            headerbytes.getvalue().decode("iso-8859-1", errors="replace").splitlines()
        ):
            if ":" not in line:
                continue
            name, value = line.split(":", 1)
            respheaders[name.strip()] = value.strip()
        resp.store_headers(respheaders)

    return resp
