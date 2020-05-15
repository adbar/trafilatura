"""
Unit tests for the command-line interface.
"""

import logging
import os
import sys

from datetime import datetime
from unittest.mock import patch

from trafilatura import cli, cli_utils, utils


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def test_parser():
    '''test argument parsing for the command-line interface'''
    testargs = ['', '-fv', '--xmltei', '--notables', '-u', 'https://www.example.org']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert args.fast is True
    assert args.verbose is True
    assert args.notables is False
    assert args.xmltei is True
    assert args.URL == 'https://www.example.org'
    args = cli.map_args(args)
    assert args.output_format == 'xmltei'
    testargs = ['', '-out', 'csv', '-u', 'https://www.example.org']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert args.fast is False
    assert args.verbose is False
    args = cli.map_args(args)
    assert args.output_format == 'csv'


def test_climain():
    '''test arguments and main CLI entrypoint'''
    assert os.system('trafilatura --help') == 0  # exit status
    # assert os.system('trafilatura -f -u https://httpbin.org/html') == 0
    # assert os.system('curl -s https://httpbin.org/html | trafilatura') == 0
    # input directory walking and processing
    assert os.system('trafilatura --inputdir "trafilatura/data/"') == 0
    assert os.system('trafilatura --inputdir "tests/resources/"') == 0
    #testargs = ['--inputdir tests/resources/']
    #with patch.object(sys, 'argv', testargs):
    #    result = cli.main()
    #print(result)


def test_input_type():
    '''test input type errors'''
    testfile = 'docs/trafilatura-demo.gif'
    testargs = ['', '-v']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with open(testfile, 'rb') as f:
        teststring = f.read(1024)
    assert cli.examine(teststring, args) is None
    testfile = 'docs/index.rst'
    with open(testfile, 'r') as f:
        teststring = f.read()
    assert cli.examine(teststring, args) is None


def test_sysoutput():
    '''test command-line output with respect to CLI arguments'''
    testargs = ['', '--csv', '-o', '/root/forbidden/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    filename = cli_utils.determine_filename(args)
    assert len(filename) >= 10 and filename.endswith('.csv')
    assert cli_utils.check_outputdir_status(args.outputdir) is False
    testargs = ['', '--xml', '-o', '/tmp/you-touch-my-tralala']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli_utils.check_outputdir_status(args.outputdir) is True
    assert cli_utils.determine_filename(args).endswith('.xml')


def test_download():
    '''test page download and command-line interface'''
    testargs = ['', '-v']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli.examine(' ', args) is None
    assert cli.examine('0'*int(10e7), args) is None
    assert utils.fetch_url('https://httpbin.org/status/404') is None
    url = 'https://httpbin.org/status/200'
    teststring = utils.fetch_url(url)
    assert teststring is None  # too small
    assert cli.examine(teststring, args, url) is None
    url = 'https://httpbin.org/links/2/2'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, args, url) is None
    url = 'https://httpbin.org/html'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, args, url) is not None


def test_cli_pipeline():
    '''test command-line processing pipeline'''
    # test URL listing
    testargs = ['', '--list']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli_utils.url_processing_pipeline(args, [], 0) is None
    assert cli_utils.url_processing_pipeline(args, ['https://www.example.org/'], 0) is None
    # test inputlist + blacklist
    resources_dir = os.path.join(TEST_DIR, 'resources')
    testargs = ['', '-i', os.path.join(resources_dir, 'list-process.txt')]
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    my_urls = cli_utils.load_input_urls(args.inputfile)
    assert my_urls is not None and len(my_urls) == 2
    # test backoff between domain requests
    reftime = datetime.now()
    assert cli_utils.url_processing_pipeline(args, my_urls, 2) is None
    delta = (datetime.now() - reftime).total_seconds()
    assert delta > 2
    # URL in blacklist
    testargs = ['', '-i', os.path.join(resources_dir, 'list-process.txt'), '-b', os.path.join(resources_dir, 'list-discard.txt')]
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    print(cli_utils.url_processing_checks(args, my_urls))
    assert len(cli_utils.url_processing_checks(args, my_urls)) == 0
    # test backup
    testargs = ['', '--backup-dir', '/tmp/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli_utils.archive_html('00Test', args) is not None
    # assert cli_utils.url_processing_pipeline(args, my_urls, 2) is None


if __name__ == '__main__':
    test_parser()
    test_climain()
    test_input_type()
    test_sysoutput()
    test_cli_pipeline()
    test_download()
