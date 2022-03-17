# pylint:disable-msg=W1401
"""
Unit tests for download functions from the trafilatura library.
"""

import logging
import os
import sys

try:
    import pycurl
except ImportError:
    pycurl = None

try:
    try:
        import brotlicffi as brotli
    except ImportError:
        import brotli
except ImportError:
    brotli = None

from collections import deque
from datetime import datetime
from unittest.mock import Mock, patch

from trafilatura.cli import parse_args
from trafilatura.cli_utils import download_queue_processing, url_processing_pipeline
from trafilatura.core import extract
from trafilatura.downloads import DEFAULT_HEADERS, USER_AGENT, add_to_compressed_dict, fetch_url, draw_backoff_url, load_download_buffer, _determine_headers, _handle_response, _parse_config, _send_request, _send_pycurl_request
from trafilatura.settings import DEFAULT_CONFIG, use_config
from trafilatura.utils import decode_response, load_html


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
UA_CONFIG = use_config(filename=os.path.join(RESOURCES_DIR, 'newsettings.cfg'))


def test_fetch():
    '''Test URL fetching.'''
    # pycurl tests
    if pycurl is not None:
        assert fetch_url('1234') is None
    # urllib3 tests
    else:
        assert fetch_url('1234') == ''
    assert fetch_url('https://httpbin.org/status/404') is None
    # empty request?
    #assert _send_request('') is None
    # test if the fonctions default to no_ssl
    assert _send_request('https://expired.badssl.com/', False, DEFAULT_CONFIG) is not None
    if pycurl is not None:
        assert _send_pycurl_request('https://expired.badssl.com/', False, DEFAULT_CONFIG) is not None
    # no SSL, no decoding
    url = 'https://httpbin.org/status/200'
    response = _send_request('https://httpbin.org/status/200', True, DEFAULT_CONFIG)
    assert response.data == b''
    if pycurl is not None:
        response1 = _send_pycurl_request('https://httpbin.org/status/200', True, DEFAULT_CONFIG)
        assert _handle_response(url, response1, False, DEFAULT_CONFIG) == _handle_response(url, response, False, DEFAULT_CONFIG)
        assert _handle_response(url, response1, True, DEFAULT_CONFIG) == _handle_response(url, response, True, DEFAULT_CONFIG)
    # response object
    url = 'https://httpbin.org/encoding/utf8'
    response = _send_request(url, False, DEFAULT_CONFIG)
    myobject = _handle_response(url, response, False, DEFAULT_CONFIG)
    assert myobject.data.startswith(b'<h1>Unicode Demo</h1>')
    # too large response object
    mock = Mock()
    mock.status = 200
    # too large
    mock.data = (b'ABC'*10000000)
    assert _handle_response(url, mock, False, DEFAULT_CONFIG) == ''
    # too small
    mock.data = (b'ABC')
    assert _handle_response(url, mock, False, DEFAULT_CONFIG) == ''
    # straight handling of response object
    assert load_html(response) is not None
    # nothing to see here
    assert extract(response, url=response.url, config=ZERO_CONFIG) is None


def test_config():
    '''Test how configuration options are read and stored.'''
    # default config is none
    assert _parse_config(DEFAULT_CONFIG) == (None, None)
    # default accept-encoding
    if brotli is None:
        assert DEFAULT_HEADERS['accept-encoding'].endswith(',deflate')
    else:
        assert DEFAULT_HEADERS['accept-encoding'].endswith(',br')
    # default user-agent
    default = _determine_headers(DEFAULT_CONFIG)
    assert default['User-Agent'] == USER_AGENT
    assert 'Cookie' not in default
    # user-agents rotation
    assert _parse_config(UA_CONFIG) == (['Firefox', 'Chrome'], 'yummy_cookie=choco; tasty_cookie=strawberry')
    custom = _determine_headers(UA_CONFIG)
    assert custom['User-Agent'] in ['Chrome', 'Firefox']
    assert custom['Cookie'] == 'yummy_cookie=choco; tasty_cookie=strawberry'


def test_decode():
    '''Test how responses are being decoded.'''
    assert decode_response(b'\x1f\x8babcdef') is not None
    assert decode_response(b'\x1f\x8babcdef') is not None
    mock = Mock()
    mock.data = (b' ')
    assert decode_response(mock) is not None


def test_queue():
    'Test creation, modification and download of URL queues.'
    # test conversion and storage
    inputdict = add_to_compressed_dict(['ftps://www.example.org/', 'http://'])
    assert inputdict == dict()
    inputdict = add_to_compressed_dict(['https://www.example.org/'])
    # CLI args
    testargs = ['', '--list']
    with patch.object(sys, 'argv', testargs):
        args = parse_args(testargs)
    assert url_processing_pipeline(args, inputdict) is None
    # single/multiprocessing
    testargs = ['', '-v']
    with patch.object(sys, 'argv', testargs):
        args = parse_args(testargs)
    domain_dict = {
        'https://httpbin.org': deque(
            [
                '/status/301',
                '/status/304',
                '/status/200',
                '/status/300',
                '/status/400',
                '/status/505',
            ]
        )
    }
    args.archived = True
    args.config_file = os.path.join(RESOURCES_DIR, 'newsettings.cfg')
    config = use_config(filename=args.config_file)
    config['DEFAULT']['SLEEP_TIME'] = '0.2'
    results = download_queue_processing(domain_dict, args, None, config)
    assert len(results[0]) == 6 and results[1] is None
    # test backoff algorithm
    backoffdict = {}
    testdict = {'http://test.org': deque(['/1'])}
    assert draw_backoff_url(testdict, backoffdict, 0) == ('http://test.org/1', dict(), dict())
    testdict['http://test.org'] = deque(['/1'])
    backoffdict['http://test.org'] = datetime(2019, 5, 18, 15, 17, 8, 132263)
    assert draw_backoff_url(testdict, backoffdict, 0) == ('http://test.org/1', dict(), dict())
    # concurrent domains
    testdict = {}
    backoffdict = {}
    testdict['http://test.org'] = deque(['/1'])
    testdict['http://example.org'] = deque(['/1'])
    # simulate recent request
    backoffdict['http://test.org'] = datetime.now()
    # must return the other domain
    test = draw_backoff_url(testdict, backoffdict, 5)
    assert test[0], test[1] == ('http://example.org/1', {'http://test.org': deque(['/1'])})
    print(test)
    assert test[2] != {}
    # sleeps and returns the rest
    assert draw_backoff_url(testdict, backoffdict, 1) == ('http://test.org/1', {}, {})
    # code hangs, logical:
    #testdict['http://test.org'] = deque(['/1'])
    #backoffdict['http://test.org'] = datetime(2030, 5, 18, 15, 17, 8, 132263)
    #assert draw_backoff_url(testdict, backoffdict, 0) == ('http://test.org/1', dict(), dict())
    # download buffer
    domain_dict = {'https://test.org': deque(['/1', '/2', '/3']), 'https://test2.org': deque(['/1', '/2', '/3']), 'https://test3.org': deque(['/1', '/2', '/3']), 'https://test4.org': deque(['/1', '/2', '/3']), 'https://test5.org': deque(['/1', '/2', '/3']), 'https://test6.org': deque(['/1', '/2', '/3'])}
    bufferlist, _, _, _ = load_download_buffer(domain_dict, dict(), sleep_time=5, threads=1)
    assert len(bufferlist) == 6
    bufferlist, _, _, _ = load_download_buffer(domain_dict, dict(), sleep_time=5, threads=2)
    assert len(bufferlist) == 6


if __name__ == '__main__':
    test_fetch()
    test_config()
    test_decode()
    test_queue()
