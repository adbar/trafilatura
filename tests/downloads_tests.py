# pylint:disable-msg=W1401
"""
Unit tests for download functions from the trafilatura library.
"""

import os
import sys

from collections import deque
from datetime import datetime
from unittest.mock import patch

from trafilatura.cli import parse_args
from trafilatura.cli_utils import download_queue_processing, url_processing_pipeline
from trafilatura.core import extract
from trafilatura.downloads import add_to_compressed_dict, fetch_url, decode_response, draw_backoff_url, load_download_buffer, _determine_headers, _handle_response, _parse_config, _send_request
from trafilatura.settings import DEFAULT_CONFIG, use_config
from trafilatura.utils import load_html


ZERO_CONFIG = DEFAULT_CONFIG
ZERO_CONFIG['DEFAULT']['MIN_OUTPUT_SIZE'] = '0'
ZERO_CONFIG['DEFAULT']['MIN_EXTRACTED_SIZE'] = '0'

RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
UA_CONFIG = use_config(filename=os.path.join(RESOURCES_DIR, 'newsettings.cfg'))


def test_fetch():
    '''test URL fetching'''
    assert fetch_url('1234') == ''
    assert fetch_url('https://httpbin.org/status/404') is None
    assert decode_response(b'\x1f\x8babcdef') is not None
    assert fetch_url('https://expired.badssl.com/', no_ssl=True) is not None
    # no decoding
    response = fetch_url('https://httpbin.org/status/200', decode=False)
    assert response == ''
    # response object
    url = 'https://httpbin.org/encoding/utf8'
    response = _send_request(url, False, DEFAULT_CONFIG)
    myobject = _handle_response(url, response, False, DEFAULT_CONFIG)
    assert myobject.data.startswith(b'<h1>Unicode Demo</h1>')
    # straight handling of response object
    assert load_html(response) is not None
    # nothing to see here
    assert extract(response, url=response.geturl(), config=ZERO_CONFIG) is None
    # user-agents rotation
    assert _parse_config(UA_CONFIG) == ['Firefox', 'Chrome']
    custom = _determine_headers(UA_CONFIG)
    assert custom['User-Agent'] == 'Chrome' or custom['User-Agent'] == 'Firefox'


def test_queue():
    'Test creation, modification and download of URL queues.'
    # test conversion and storage
    inputdict = add_to_compressed_dict(['ftps://www.example.org/'])
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
    domain_dict = dict()
    domain_dict['https://httpbin.org'] = deque(['/status/301', '/status/304', '/status/200', '/status/300', '/status/400', '/status/505'])
    args.archived = True
    args.config_file = os.path.join(RESOURCES_DIR, 'newsettings.cfg')
    config = use_config(filename=args.config_file)
    results = download_queue_processing(domain_dict, args, None, config)
    assert len(results[0]) == 6 and results[1] is None
    # test backoff algorithm
    testdict = dict()
    backoffdict = dict()
    testdict['http://test.org'] = deque(['/1'])
    assert draw_backoff_url(testdict, backoffdict, 0, set()) == ('http://test.org/1', dict(), dict(), 'http://test.org')
    testdict['http://test.org'] = deque(['/1'])
    backoffdict['http://test.org'] = datetime(2019, 5, 18, 15, 17, 8, 132263)
    assert draw_backoff_url(testdict, backoffdict, 0, set()) == ('http://test.org/1', dict(), dict(), 'http://test.org')
    # code hangs, logical:
    #testdict['http://test.org'] = deque(['/1'])
    #backoffdict['http://test.org'] = datetime(2030, 5, 18, 15, 17, 8, 132263)
    #assert cli_utils.draw_backoff_url(testdict, backoffdict, 0, 3) == ('http://test.org/1', dict(), dict(), 0)
    # download buffer
    domain_dict = {'https://test.org': deque(['/1', '/2', '/3']), 'https://test2.org': deque(['/1', '/2', '/3']), 'https://test3.org': deque(['/1', '/2', '/3']), 'https://test4.org': deque(['/1', '/2', '/3']), 'https://test5.org': deque(['/1', '/2', '/3']), 'https://test6.org': deque(['/1', '/2', '/3'])}
    bufferlist, _, _, _ = load_download_buffer(domain_dict, dict(), 0, threads=1)
    assert len(bufferlist) == 6
    bufferlist, _, _, _ = load_download_buffer(domain_dict, dict(), 0, threads=2)
    assert len(bufferlist) == 6


if __name__ == '__main__':
    test_fetch()
    test_queue()
