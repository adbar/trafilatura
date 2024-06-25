# pylint:disable-msg=E0611,I1101
"""
All functions needed to steer and execute downloads of web documents.
"""

import logging
import random

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from io import BytesIO
from time import sleep
from typing import Any, ByteString, Dict, Generator, List, Optional, Set, Tuple, Union

import certifi
import urllib3

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

from courlan import UrlStore
from courlan.network import redirection_test

try:  # Python 3.8+
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from .settings import DEFAULT_CONFIG, Extractor
from .utils import URL_BLACKLIST_REGEX, decode_file, is_acceptable_length, make_chunks


LOGGER = logging.getLogger(__name__)

NUM_CONNECTIONS = 50

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
HTTP_POOL = None
NO_CERT_POOL = None
RETRY_STRATEGY = None

DEFAULT_HEADERS = urllib3.util.make_headers(accept_encoding=True)
USER_AGENT = (
    "trafilatura/" + version("trafilatura") + " (+https://github.com/adbar/trafilatura)"
)
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

    def __init__(self, data: ByteString, status: int, url: str) -> None:
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


# caching throws an error
# @lru_cache(maxsize=2)
def _parse_config(config: Any) -> Tuple[Optional[str], Optional[str]]:
    "Read and extract HTTP header strings from the configuration file."
    # load a series of user-agents
    myagents = config.get("DEFAULT", "USER_AGENTS").strip() or None
    if myagents is not None and myagents != "":
        myagents = myagents.split("\n")
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
    # todo: support for several cookies?
    mycookie = config.get("DEFAULT", "COOKIE") or None
    return myagents, mycookie


def _determine_headers(
    config: Any, headers: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    "Internal function to decide on user-agent string."
    if config != DEFAULT_CONFIG:
        myagents, mycookie = _parse_config(config)
        headers = {}
        if myagents is not None:
            rnumber = random.randint(0, len(myagents) - 1)
            headers["User-Agent"] = myagents[rnumber]
        if mycookie is not None:
            headers["Cookie"] = mycookie
    return headers or DEFAULT_HEADERS


def _send_urllib_request(
    url: str, no_ssl: bool, with_headers: bool, config: Any
) -> Optional[Response]:
    "Internal function to robustly send a request (SSL or not) and return its result."
    # customize headers
    global HTTP_POOL, NO_CERT_POOL, RETRY_STRATEGY
    if not RETRY_STRATEGY:
        RETRY_STRATEGY = urllib3.util.Retry(
            total=config.getint("DEFAULT", "MAX_REDIRECTS"),
            redirect=config.getint(
                "DEFAULT", "MAX_REDIRECTS"
            ),  # raise_on_redirect=False,
            connect=0,
            backoff_factor=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT") / 2,
            status_forcelist=FORCE_STATUS,
            # unofficial: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#Unofficial_codes
        )
    try:
        if no_ssl is False:
            if not HTTP_POOL:
                HTTP_POOL = urllib3.PoolManager(
                    retries=RETRY_STRATEGY,
                    timeout=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"),
                    ca_certs=certifi.where(),
                    num_pools=NUM_CONNECTIONS,
                )  # cert_reqs='CERT_REQUIRED'
            pool_manager = HTTP_POOL
        else:
            if not NO_CERT_POOL:
                NO_CERT_POOL = urllib3.PoolManager(
                    retries=RETRY_STRATEGY,
                    timeout=config.getint("DEFAULT", "DOWNLOAD_TIMEOUT"),
                    cert_reqs="CERT_NONE",
                    num_pools=NUM_CONNECTIONS,
                )
            pool_manager = NO_CERT_POOL
        # execute request
        # TODO: read by streaming chunks (stream=True)
        # stop downloading as soon as MAX_FILE_SIZE is reached
        response = pool_manager.request(
            "GET", url, headers=_determine_headers(config), retries=RETRY_STRATEGY
        )
    except urllib3.exceptions.SSLError:
        LOGGER.warning("retrying after SSLError: %s", url)
        return _send_urllib_request(url, True, with_headers, config)
    except Exception as err:
        LOGGER.error("download error: %s %s", url, err)  # sys.exc_info()[0]
    else:
        # necessary for standardization
        resp = Response(response.data, response.status, response.geturl())
        if with_headers:
            resp.store_headers(response.headers)
        return resp
    # catchall
    return None


def _handle_response(
    url: str, response: Response, decode: bool, options: Extractor
) -> Optional[Union[Response, str]]:
    "Internal function to run safety checks on response result."
    lentest = len(response.html or response.data or "")
    if response.status != 200:
        LOGGER.error("not a 200 response: %s for URL %s", response.status, url)
    # raise error instead?
    elif is_acceptable_length(lentest, options):
        return response.html if decode else response
    # catchall
    return None


def fetch_url(
    url: str,
    decode: bool = True,
    no_ssl: bool = False,
    config: Any = DEFAULT_CONFIG,
    options: Optional[Extractor] = None,
) -> Optional[str]:
    """Downloads a web page and seamlessly decodes the response.

    Args:
        url: URL of the page to fetch.
        no_ssl: Don't try to establish a secure connection (to prevent SSLError).
        config: Pass configuration values for output control.
        options: Extraction options (supersedes config).

    Returns:
        Unicode string or None in case of failed downloads and invalid results.

    """
    if not decode:
        raise ValueError(
            "Raw response objects are deprecated for fetch_url(), use fetch_response() instead."
        )
    response = fetch_response(url, decode=decode, no_ssl=no_ssl, config=config)
    if response and response.data:
        if not options:
            options = Extractor(config=config)
        return _handle_response(url, response, decode, options)
        # return '' (useful do discard further processing?)
        # return response
    return None


def fetch_response(
    url: str,
    *,
    decode: bool = False,
    no_ssl: bool = False,
    with_headers: bool = False,
    config: Any = DEFAULT_CONFIG,
) -> Optional[Response]:
    """Downloads a web page and returns a full response object.

    Args:
        url: URL of the page to fetch.
        decode: Use html attribute to decode the data (boolean).
        no_ssl: Don't try to establish a secure connection (to prevent SSLError).
        with_headers: Keep track of the response headers.
        config: Pass configuration values for output control.

    Returns:
        Response object or None in case of failed downloads and invalid results.

    """
    dl_function = _send_urllib_request if not HAS_PYCURL else _send_pycurl_request
    LOGGER.debug("sending request: %s", url)
    response = dl_function(url, no_ssl, with_headers, config)  # Response
    if not response:  # None or ""
        LOGGER.debug("request failed: %s", url)
        return None
    response.decode_data(decode)
    return response


def _pycurl_is_live_page(url: str) -> bool:
    "Send a basic HTTP HEAD request with pycurl."
    # Initialize pycurl object
    curl = pycurl.Curl()
    # Set the URL and HTTP method (HEAD)
    curl.setopt(pycurl.URL, url.encode("utf-8"))
    curl.setopt(pycurl.CONNECTTIMEOUT, 10)
    # no SSL verification
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    # Set option to avoid getting the response body
    curl.setopt(curl.NOBODY, True)
    # Perform the request
    try:
        curl.perform()
        # Get the response code
        page_exists = curl.getinfo(curl.RESPONSE_CODE) < 400
    except pycurl.error as err:
        LOGGER.debug("pycurl HEAD error: %s %s", url, err)
        page_exists = False
    # Clean up
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
    # use urllib3 as backup
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
    url_store: UrlStore, sleep_time: int = 5
) -> Tuple[List[str], UrlStore]:
    """Determine threading strategy and draw URLs respecting domain-based back-off rules."""
    while True:
        bufferlist = url_store.get_download_urls(time_limit=sleep_time, max_urls=10**5)
        if bufferlist or url_store.done:
            break
        sleep(sleep_time)
    return bufferlist, url_store


def buffered_downloads(
    bufferlist: List[str],
    download_threads: int,
    decode: bool = True,
    options: Optional[Extractor] = None,
) -> Generator[Tuple[str, str], None, None]:
    """Download queue consumer, single- or multi-threaded."""
    worker = partial(fetch_url, options=options) if decode else fetch_response
    with ThreadPoolExecutor(max_workers=download_threads) as executor:
        for chunk in make_chunks(bufferlist, 10000):
            future_to_url: Dict[Any, str] = {
                executor.submit(worker, url): url for url in chunk
            }
            for future in as_completed(future_to_url):
                # url and download result
                yield future_to_url[future], future.result()


def _send_pycurl_request(
    url: str, no_ssl: bool, with_headers: bool, config: Any
) -> Optional[Response]:
    """Experimental function using libcurl and pycurl to speed up downloads"""
    # https://github.com/pycurl/pycurl/blob/master/examples/retriever-multi.py

    # init
    headerlist = [
        f"{header}: {content}" for header, content in _determine_headers(config).items()
    ]

    # prepare curl request
    # https://curl.haxx.se/libcurl/c/curl_easy_setopt.html
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url.encode("utf-8"))
    # share data
    curl.setopt(pycurl.SHARE, CURL_SHARE)
    curl.setopt(pycurl.HTTPHEADER, headerlist)
    # curl.setopt(pycurl.USERAGENT, '')
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

    # TCP_FASTOPEN
    # curl.setopt(pycurl.FAILONERROR, 1)
    # curl.setopt(pycurl.ACCEPT_ENCODING, '')

    # send request
    try:
        bufferbytes = curl.perform_rb()
    except pycurl.error as err:
        LOGGER.error("pycurl error: %s %s", url, err)
        # retry in case of SSL-related error
        # see https://curl.se/libcurl/c/libcurl-errors.html
        # errmsg = curl.errstr_raw()
        # additional error codes: 80, 90, 96, 98
        if no_ssl is False and err.args[0] in CURL_SSL_ERRORS:
            LOGGER.debug("retrying after SSL error: %s %s", url, err)
            return _send_pycurl_request(url, True, with_headers, config)
        # traceback.print_exc(file=sys.stderr)
        # sys.stderr.flush()
        return None

    # additional info
    # ip_info = curl.getinfo(curl.PRIMARY_IP)

    resp = Response(
        bufferbytes, curl.getinfo(curl.RESPONSE_CODE), curl.getinfo(curl.EFFECTIVE_URL)
    )
    curl.close()

    if with_headers:
        respheaders = {}
        # https://github.com/pycurl/pycurl/blob/master/examples/quickstart/response_headers.py
        for line in (
            headerbytes.getvalue().decode("iso-8859-1", errors="replace").splitlines()
        ):
            # re.split(r'\r?\n') ?
            # This will botch headers that are split on multiple lines...
            if ":" not in line:
                continue
            # Break the header line into header name and value.
            name, value = line.split(":", 1)
            # Now we can actually record the header name and value.
            respheaders[name.strip()] = value.strip()  # name.strip().lower() ?
        resp.store_headers(respheaders)

    return resp
