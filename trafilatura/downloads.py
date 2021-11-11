# pylint:disable-msg=E0611,I1101
"""
All functions needed to steer and execute downloads of web documents.
"""


import logging
import random
import re

from collections import defaultdict, deque, namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from io import BytesIO
from time import sleep

import certifi
try:
    import pycurl
    CURL_SHARE = pycurl.CurlShare()
    # available options: https://pycurl.io/docs/latest/curlshareobject.html?highlight=lock_data_cookie
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_DNS)
    CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_SSL_SESSION)
    # not thread-safe
    # https://curl.se/libcurl/c/curl_share_setopt.html
    # CURL_SHARE.setopt(pycurl.SH_SHARE, pycurl.LOCK_DATA_CONNECT)
except ImportError:
    pycurl = None
import urllib3

from courlan import get_host_and_path, validate_url

from . import __version__
from .settings import DEFAULT_CONFIG, DOWNLOAD_THREADS, TIMEOUT
from .utils import decode_response, uniquify_list


NUM_CONNECTIONS = 50
MAX_REDIRECTS = 2

# customize headers
RETRY_STRATEGY = urllib3.util.Retry(
    total=0,
    redirect=MAX_REDIRECTS, # raise_on_redirect=False,
    connect=0,
    backoff_factor=TIMEOUT*2,
    status_forcelist=[429, 499, 500, 502, 503, 504, 509, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598],
    # unofficial: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#Unofficial_codes
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()
HTTP_POOL = urllib3.PoolManager(retries=RETRY_STRATEGY, timeout=TIMEOUT, ca_certs=certifi.where(), num_pools=NUM_CONNECTIONS)
NO_CERT_POOL = urllib3.PoolManager(retries=RETRY_STRATEGY, timeout=TIMEOUT, cert_reqs='CERT_NONE', num_pools=20)

USER_AGENT = 'trafilatura/' + __version__ + ' (+https://github.com/adbar/trafilatura)'
DEFAULT_HEADERS = {
    'User-Agent': USER_AGENT,
}

LOGGER = logging.getLogger(__name__)

RawResponse = namedtuple('RawResponse', ['data', 'status', 'url'])


# caching throws an error
# @lru_cache(maxsize=2)
def _parse_config(config):
    'Read and extract HTTP header strings from the configuration file.'
    # load a series of user-agents
    myagents = config.get('DEFAULT', 'USER_AGENTS') or None
    if myagents is not None and myagents != '':
        myagents = myagents.split(',')
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
    # todo: support for several cookies?
    mycookie = config.get('DEFAULT', 'COOKIE') or None
    return myagents, mycookie


def _determine_headers(config, headers=None):
    'Internal function to decide on user-agent string.'
    if config != DEFAULT_CONFIG:
        myagents, mycookie = _parse_config(config)
        headers = {}
        if myagents is not None:
            rnumber = random.randint(0, len(myagents) - 1)
            headers['User-Agent'] = myagents[rnumber]
        if mycookie is not None:
            headers['Cookie'] = mycookie
    return headers or DEFAULT_HEADERS


def _send_request(url, no_ssl, config):
    'Internal function to send a robustly (SSL) send a request and return its result.'
    try:
        # read by streaming chunks (stream=True, iter_content=xx)
        # so we can stop downloading as soon as MAX_FILE_SIZE is reached
        if no_ssl is False:
            response = HTTP_POOL.request('GET', url, headers=_determine_headers(config))
        else:
            response = NO_CERT_POOL.request('GET', url, headers=_determine_headers(config))
    except urllib3.exceptions.NewConnectionError as err:
        LOGGER.error('connection refused: %s %s', url, err)
        return ''  # raise error instead?
    except urllib3.exceptions.MaxRetryError as err:
        LOGGER.error('retries/redirects: %s %s', url, err)
        return ''  # raise error instead?
    except urllib3.exceptions.TimeoutError as err:
        LOGGER.error('connection timeout: %s %s', url, err)
    except urllib3.exceptions.SSLError:
        LOGGER.error('retrying after SSLError: %s', url)
        return _send_request(url, True, config)
    except Exception as err:
        logging.error('unknown error: %s %s', url, err) # sys.exc_info()[0]
    else:
        # necessary for standardization
        return RawResponse(response.data, response.status, response.geturl())
    # catchall
    return None


def _handle_response(url, response, decode, config):
    'Internal function to run safety checks on response result.'
    if response.status != 200:
        LOGGER.error('not a 200 response: %s for URL %s', response.status, url)
    elif response.data is None or len(response.data) < config.getint('DEFAULT', 'MIN_FILE_SIZE'):
        LOGGER.error('too small/incorrect for URL %s', url)
        return ''  # raise error instead?
    elif len(response.data) > config.getint('DEFAULT', 'MAX_FILE_SIZE'):
        LOGGER.error('too large: length %s for URL %s', len(response.data), url)
        return ''  # raise error instead?
    else:
        if decode is True:
            return decode_response(response.data)
        # else: return raw
        return response
    # catchall
    return None


def fetch_url(url, decode=True, no_ssl=False, config=DEFAULT_CONFIG):
    """Fetches page using urllib3 and decodes the response.

    Args:
        url: URL of the page to fetch.
        decode: Decode response instead of returning urllib3 response object (boolean).
        no_ssl: Don't try to establish a secure connection (to prevent SSLError).
        config: Pass configuration values for output control.

    Returns:
        HTML code as string, or Urllib3 response object (headers + body), or empty string in case
        the result is invalid, or None if there was a problem with the network.

    """
    if pycurl is None:
        response = _send_request(url, no_ssl, config)
    else:
        response = _send_pycurl_request(url, no_ssl, config)
    if response is not None:
        if response != '':
            return _handle_response(url, response, decode, config)
        # return '' (useful do discard further processing?)
        return response
    return None


def add_to_compressed_dict(inputlist, blacklist=None, url_filter=None, inputdict=None):
    '''Filter, convert input URLs and add them to domain-aware processing dictionary'''
    # init
    if inputdict is None:
        inputdict = defaultdict(deque)
    # deduplicate while keeping order
    inputlist = uniquify_list(inputlist)
    # filter
    if blacklist:
        inputlist = [u for u in inputlist if re.sub(r'https?://', '', u) not in blacklist]
    if url_filter:
        filtered_list = []
        while inputlist:
            u = inputlist.pop()
            for f in url_filter:
                if f in u:
                    filtered_list.append(u)
                    break
        inputlist = filtered_list
    # validate and store in dict
    for url in inputlist:
        # validate URL
        if validate_url(url)[0] is False:
            continue
        # segment URL and add to domain dictionary
        try:
            hostinfo, urlpath = get_host_and_path(url)
            inputdict[hostinfo].append(urlpath)
        except ValueError:
            LOGGER.warning('Could not parse URL, discarding: %s', url)
    return inputdict


def draw_backoff_url(domain_dict, backoff_dict, sleep_time, hosts):
    '''Select a random URL from the domains pool and apply backoff rule'''
    green_light = False
    while not green_light:
        # choose among a fresh pool of hosts
        host = random.choice([d for d in domain_dict if d not in hosts])
        # safeguard
        if host in backoff_dict and \
            (datetime.now() - backoff_dict[host]).total_seconds() < sleep_time:
            LOGGER.debug('spacing request for host %s', host)
            sleep(sleep_time)
        else:
            if domain_dict[host]:
                # draw URL
                url = host + domain_dict[host].popleft()
                backoff_dict[host] = datetime.now()
            else:
                url = None
            # release the chosen URL
            green_light = True
    # clean registries
    if not domain_dict[host]:
        del domain_dict[host]
        if host in backoff_dict:
            del backoff_dict[host]
    return url, domain_dict, backoff_dict, host


def load_download_buffer(domain_dict, backoff_dict, sleep_time=5, threads=DOWNLOAD_THREADS):
    '''Determine threading strategy and draw URLs respecting domain-based back-off rules.'''
    bufferlist, hosts = [], set()
    # the remaining list is too small, process it differently
    if len(domain_dict) < threads or \
       len({x for v in domain_dict.values() for x in v}) < threads:
        threads = 1
    # populate buffer until a condition is reached
    while domain_dict and [d for d in domain_dict if d not in hosts]:
        #print(len(domain_dict), len(hosts), len([d for d in domain_dict if d not in hosts]), len(bufferlist), threads)
        url, domain_dict, backoff_dict, host = draw_backoff_url(
            domain_dict, backoff_dict, sleep_time, hosts
            )
        hosts.add(host)
        if url is not None:
            bufferlist.append(url)
        #print(domain_dict)
        #print(bufferlist)
    return bufferlist, threads, domain_dict, backoff_dict


def buffered_downloads(bufferlist, download_threads, decode=True):
    '''Download queue consumer, single- or multi-threaded.'''
    # start several threads
    with ThreadPoolExecutor(max_workers=download_threads) as executor:
        future_to_url = {executor.submit(fetch_url, url, decode): url for url in bufferlist}
        for future in as_completed(future_to_url):
            # url and download result
            yield future_to_url[future], future.result()


def _send_pycurl_request(url, no_ssl, config):
    '''Experimental function using libcurl and pycurl to speed up downloads'''
    # https://github.com/pycurl/pycurl/blob/master/examples/retriever-multi.py

    # init
    bufferbytes = BytesIO()
    # headerbytes = BytesIO()
    headers = _determine_headers(config)
    headerlist = ['Accept-Encoding: gzip, deflate', 'Accept: */*']
    for header, content in headers.items():
        headerlist.append(header + ': ' + content)

    # prepare curl request
    # https://curl.haxx.se/libcurl/c/curl_easy_setopt.html
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url.encode('utf-8'))
    # share data
    curl.setopt(pycurl.SHARE, CURL_SHARE)
    curl.setopt(pycurl.HTTPHEADER, headerlist)
    # curl.setopt(pycurl.USERAGENT, '')
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, MAX_REDIRECTS)
    curl.setopt(pycurl.CONNECTTIMEOUT, TIMEOUT)
    curl.setopt(pycurl.TIMEOUT, TIMEOUT)
    curl.setopt(pycurl.NOSIGNAL, 1)
    if no_ssl is True:
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    else:
        curl.setopt(pycurl.CAINFO, certifi.where())
    curl.setopt(pycurl.MAXFILESIZE, config.getint('DEFAULT', 'MAX_FILE_SIZE'))
    #curl.setopt(pycurl.HEADERFUNCTION, headerbytes.write)
    #curl.setopt(pycurl.WRITEDATA, bufferbytes)
    # TCP_FASTOPEN
    # curl.setopt(pycurl.FAILONERROR, 1)
    # curl.setopt(pycurl.ACCEPT_ENCODING, '')

    # send request
    try:
        bufferbytes = curl.perform_rb()
    except pycurl.error as err:
        logging.error('pycurl: %s %s', url, err)
        # retry in case of SSL-related error
        # see https://curl.se/libcurl/c/libcurl-errors.html
        # errmsg = curl.errstr_raw()
        # additional error codes: 80, 90, 96, 98
        if no_ssl is False and err.args[0] in (35, 54, 58, 59, 60, 64, 66, 77, 82, 83, 91):
            LOGGER.error('retrying after SSL error: %s %s', url, err)
            return _send_pycurl_request(url, True, config)
        # traceback.print_exc(file=sys.stderr)
        # sys.stderr.flush()
        return None

    # https://github.com/pycurl/pycurl/blob/master/examples/quickstart/response_headers.py
    #respheaders = dict()
    #for header_line in headerbytes.getvalue().decode('iso-8859-1').splitlines(): # re.split(r'\r?\n',
    #    # This will botch headers that are split on multiple lines...
    #    if ':' not in header_line:
    #        continue
    #    # Break the header line into header name and value.
    #    name, value = header_line.split(':', 1)
    #    # Now we can actually record the header name and value.
    #    respheaders[name.strip()] = value.strip() # name.strip().lower() ## TODO: check
    # status
    respcode = curl.getinfo(curl.RESPONSE_CODE)
    # url
    effective_url = curl.getinfo(curl.EFFECTIVE_URL)
    # additional info
    # ip_info = curl.getinfo(curl.PRIMARY_IP)

    # tidy up
    curl.close()
    return RawResponse(bufferbytes, respcode, effective_url)
