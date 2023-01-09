"""
Unit tests for the command-line interface.
"""

import io
import logging
import os
import re
import subprocess
import sys

from collections import deque
from contextlib import redirect_stdout
from datetime import datetime
from unittest.mock import patch

import pytest

from trafilatura import cli, cli_utils
from trafilatura.downloads import add_to_compressed_dict, fetch_url
from trafilatura.settings import DEFAULT_CONFIG


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')


def test_parser():
    '''test argument parsing for the command-line interface'''
    testargs = ['', '-fvv', '--xmltei', '--no-tables', '-u', 'https://www.example.org']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert args.fast is True
    assert args.verbose == 2
    assert args.no_tables is False
    assert args.xmltei is True
    assert args.URL == 'https://www.example.org'
    args = cli.map_args(args)
    assert args.output_format == 'xmltei'
    testargs = ['', '-out', 'csv', '--no-tables', '-u', 'https://www.example.org']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert args.fast is False
    assert args.verbose == 0
    assert args.output_format == 'csv'
    assert args.no_tables is False
    # test args mapping
    testargs = ['', '--xml', '--no-comments', '--precision', '--recall']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    args = cli.map_args(args)
    assert args.output_format == 'xml' and args.no_comments is False
    # combination possible (?)
    assert args.precision is True and args.recall is True
    args.xml, args.csv = False, True
    args = cli.map_args(args)
    assert args.output_format == 'csv'
    args.csv, args.json = False, True
    args = cli.map_args(args)
    assert args.output_format == 'json'
    testargs = ['', '--only-with-metadata']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    args = cli.map_args(args)
    assert args.only_with_metadata is True
    # process_args
    args.inputdir = '/dev/null'
    args.verbose = 1
    args.blacklist = os.path.join(RESOURCES_DIR, 'list-discard.txt')
    cli.process_args(args)
    assert len(args.blacklist) == 2
    # filter
    testargs = ['', '-i', 'resources/list-discard.txt', '--url-filter', 'test1', 'test2']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert args.inputfile == 'resources/list-discard.txt'
    assert args.url_filter == ['test1', 'test2']
    args.inputfile = os.path.join(RESOURCES_DIR, 'list-discard.txt')
    args.blacklist = os.path.join(RESOURCES_DIR, 'list-discard.txt')
    f = io.StringIO()
    with redirect_stdout(f):
        cli.process_args(args)
    assert len(f.getvalue()) == 0
    # version
    testargs = ['', '--version']
    with pytest.raises(SystemExit) as e, redirect_stdout(f):
        with patch.object(sys, 'argv', testargs):
            args = cli.parse_args(testargs)
    assert e.type == SystemExit
    assert e.value.code == 0
    assert re.match(r'Trafilatura [0-9]\.[0-9]\.[0-9] - Python [0-9]\.[0-9]+\.[0-9]', f.getvalue())
    # test future deprecations
    testargs = ['', '-u', 'TEST', '--with-metadata', '--outputdir', 'test', '--nocomments', '--notables']
    with patch.object(sys, 'argv', testargs):
        args = cli.map_args(cli.parse_args(testargs))
    assert args.no_comments is False and args.no_tables is False and args.only_with_metadata and args.output_dir


def test_climain():
    '''test arguments and main CLI entrypoint'''
    # exit status required: 0
    # Windows platforms
    if os.name == 'nt':
        trafilatura_bin = os.path.join(sys.prefix, "Scripts", "trafilatura")
    # other platforms
    else:
        trafilatura_bin = 'trafilatura'
    # help display
    assert subprocess.run([trafilatura_bin, '--help']).returncode == 0
    # piped input
    empty_input = b'<html><body></body></html>'
    assert subprocess.run([trafilatura_bin], input=empty_input).returncode == 0
    # input directory walking and processing
    env = os.environ.copy()
    if os.name == 'nt':
        # Force encoding to utf-8 for Windows (seem to be a problem only in GitHub Actions)
        env['PYTHONIOENCODING'] = 'utf-8'
    assert subprocess.run([trafilatura_bin, '--inputdir', RESOURCES_DIR], env=env).returncode == 0
    # dump urls
    inputdict = add_to_compressed_dict(['https://www.example.org'])
    f = io.StringIO()
    with redirect_stdout(f):
        cli.dump_on_exit(inputdict)
    assert f.getvalue() == 'todo: https://www.example.org/\n'


def test_input_type():
    '''test input type errors'''
    testfile = 'docs/trafilatura-demo.gif'
    testargs = ['', '-u', 'http']
    with patch.object(sys, 'argv', testargs):
        assert cli.main() is None
    testargs = ['', '-v']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with open(testfile, 'rb') as f:
        teststring = f.read(1024)
    assert cli.examine(teststring, args) is None
    testfile = 'docs/usage.rst'
    with open(testfile, 'r') as f:
        teststring = f.read()
    assert cli.examine(teststring, args) is None
    # test file list
    assert 10 <= len(list(cli_utils.generate_filelist(RESOURCES_DIR))) <= 20


def test_sysoutput():
    '''test command-line output with respect to CLI arguments'''
    testargs = ['', '--csv', '-o', '/root/forbidden/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    filepath, destdir = cli_utils.determine_output_path(args, args.output_dir, '')
    assert len(filepath) >= 10 and filepath.endswith('.csv')
    assert destdir == '/root/forbidden/'
    # doesn't work the same on Windows
    if os.name != 'nt':
        assert cli_utils.check_outputdir_status(args.output_dir) is False
    else:
        assert cli_utils.check_outputdir_status(args.output_dir) is True
    testargs = ['', '--xml', '-o', '/tmp/you-touch-my-tralala']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli_utils.check_outputdir_status(args.output_dir) is True
    # test fileslug for name
    filepath, destdir = cli_utils.determine_output_path(args, args.output_dir, '', new_filename='AAZZ')
    assert filepath.endswith('AAZZ.xml')
    # test json output
    args2 = args
    args2.xml, args2.json = False, True
    args2 = cli.map_args(args2)
    filepath2, destdir2 = cli_utils.determine_output_path(args, args.output_dir, '', new_filename='AAZZ')
    assert filepath2.endswith('AAZZ.json')
    # test directory counter
    # doesn't work the same on Windows
    if os.name != 'nt':
        assert cli_utils.determine_counter_dir('testdir', 0) == 'testdir/1'
    else:
        assert cli_utils.determine_counter_dir('testdir', 0) == 'testdir\\1'
    # test file writing
    testargs = ['', '--csv', '-o', '/dev/null/', '-b', '/dev/null/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    result = 'DADIDA'
    cli_utils.write_result(result, args)
    # process with backup directory and no counter
    assert cli_utils.process_result('DADIDA', args, None, None, DEFAULT_CONFIG) is None
    # test keeping dir structure
    testargs = ['', '-i', 'myinputdir/', '-o', 'test/', '--keep-dirs']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    filepath, destdir = cli_utils.determine_output_path(args, 'testfile.txt', '')
    assert filepath == 'test/testfile.txt'
    # test hash as output file name
    assert args.hash_as_name is False
    args.hash_as_name = True
    assert args.keep_dirs is True
    args.keep_dirs = False
    filepath, destdir = cli_utils.determine_output_path(args, 'testfile.txt', '')
    assert filepath == 'test/2jmj7l5rSw0yVb-vlWAYkK-YBwk.txt'


def test_download():
    '''test page download and command-line interface'''
    testargs = ['', '-v']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli.examine(None, args) is None
    assert cli.examine(' ', args) is None
    assert cli.examine('0'*int(10e7), args) is None
    #url = 'https://httpbin.org/status/200'
    #teststring = fetch_url(url)
    #assert teststring is None  # too small
    #assert cli.examine(teststring, args, url) is None
    #url = 'https://httpbin.org/links/2/2'
    #teststring = fetch_url(url)
    #assert teststring is not None
    #assert cli.examine(teststring, args, url) is None
    url = 'https://httpbin.org/html'
    teststring = fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, args, url) is not None
    # test exit code for faulty URLs
    testargs = ['', '-u', 'https://1234.yz/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with pytest.raises(SystemExit) as e:
        cli.process_args(args)
    assert e.type == SystemExit and e.value.code == 1


def test_cli_pipeline():
    '''test command-line processing pipeline'''
    # straight command-line input
    #testargs = ['', '<html><body>Text</body></html>']
    #with patch.object(sys, 'argv', testargs):
    #    args = cli.parse_args(testargs)
    #f = io.StringIO()
    #with redirect_stdout(f):
    #    cli.process_args(args)
    #assert len(f.getvalue()) == 0
    # test URL listing

    # Force encoding to utf-8 for Windows in future processes spawned by multiprocessing.Pool
    os.environ['PYTHONIOENCODING'] = "utf-8"

    testargs = ['', '--list']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert cli_utils.url_processing_pipeline(args, dict()) is False
    # test inputlist + blacklist
    testargs = ['', '-i', os.path.join(RESOURCES_DIR, 'list-process.txt')]
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    my_urls = cli_utils.load_input_urls(args)
    assert my_urls is not None and len(my_urls) == 2
    testargs = ['', '-i', os.path.join(RESOURCES_DIR, 'list-process.txt'), '--blacklist', os.path.join(RESOURCES_DIR, 'list-discard.txt'), '--archived']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    assert args.blacklist is not None
    # test backoff between domain requests
    inputdict = add_to_compressed_dict(my_urls, args.blacklist, None, None)
    reftime = datetime.now()
    cli_utils.url_processing_pipeline(args, inputdict)
    delta = (datetime.now() - reftime).total_seconds()
    assert delta > 2
    # test blacklist and empty dict
    args.blacklist = cli_utils.load_blacklist(args.blacklist)
    assert len(args.blacklist) == 2
    inputdict = add_to_compressed_dict(my_urls, args.blacklist, None, None)
    cli_utils.url_processing_pipeline(args, inputdict)
    # test backup
    testargs = ['', '--backup-dir', '/tmp/']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    cli_utils.archive_html('00Test', args)
    # test date-based exclusion
    testargs = ['', '-out', 'xml', '--only-with-metadata']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with open(os.path.join(RESOURCES_DIR, 'httpbin_sample.html'), 'r') as f:
        teststring = f.read()
    assert cli.examine(teststring, args) is None
    testargs = ['', '-out', 'xml', '--only-with-metadata', '--precision']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with open(os.path.join(RESOURCES_DIR, 'httpbin_sample.html'), 'r') as f:
        teststring = f.read()
    assert cli.examine(teststring, args) is None
    # test JSON output
    testargs = ['', '-out', 'json', '--recall']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with open(os.path.join(RESOURCES_DIR, 'httpbin_sample.html'), 'r') as f:
        teststring = f.read()
    assert cli.examine(teststring, args) is not None
    # dry-run file processing pipeline
    testargs = ['', '--parallel', '1', '--inputdir', '/dev/null']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    cli_utils.file_processing_pipeline(args)
    # file processing pipeline on resources/
    args.inputdir = RESOURCES_DIR
    cli_utils.file_processing_pipeline(args)
    # sitemaps
    testargs = ['', '--sitemap', 'https://httpbin.org/', '--list']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    f = io.StringIO()
    with redirect_stdout(f):
        cli.process_args(args)
    assert len(f.getvalue()) == 0
    # config file
    testargs = ['', '--inputdir', '/dev/null', '--config-file', 'newsettings.cfg']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    with open(os.path.join(RESOURCES_DIR, 'httpbin_sample.html'), 'r') as f:
        teststring = f.read()
    args.config_file = os.path.join(RESOURCES_DIR, args.config_file)
    # config = use_config(filename=args.config_file)
    assert cli.examine(teststring, args) is None
    # CLI options
    testargs = ['', '--links', '--images']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    #with open(os.path.join(RESOURCES_DIR, 'http_sample.html'), 'r') as f:
    #    teststring = f.read()
    #result = cli.examine(teststring, args)
    #assert '[link](testlink.html)' in result # and 'test.jpg' in result

    # Crawling
    testargs = ['', '--crawl', 'https://httpbin.org/html']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    f = io.StringIO()
    with redirect_stdout(f):
        cli_utils.cli_crawler(args)
    assert len(f.getvalue()) == 0
    # links permitted
    testargs = ['', '--crawl', 'https://httpbin.org/links/1/1', '--list', '--parallel', '1']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    f = io.StringIO()
    with redirect_stdout(f):
        cli_utils.cli_crawler(args)
    assert f.getvalue() == 'https://httpbin.org/links/1/0\n'
    # 0 links permitted
    args.crawl = 'https://httpbin.org/links/4/4'
    f = io.StringIO()
    with redirect_stdout(f):
        cli_utils.cli_crawler(args, n=0)
    # print(f.getvalue())
    assert len(f.getvalue().split('\n')) == 5

    # Exploration (Sitemap + Crawl)
    testargs = ['', '--explore', 'https://httpbin.org/html']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    f = io.StringIO()
    with redirect_stdout(f):
        cli.process_args(args)
    assert len(f.getvalue()) == 0


def test_input_filtering():
    '''test internal functions to filter urls'''
    testargs = ['']
    with patch.object(sys, 'argv', testargs):
        args = cli.parse_args(testargs)
    # load dictionary
    args.inputfile = os.path.join(RESOURCES_DIR, 'list-process.txt')
    inputdict = cli.load_input_dict(args)
    assert inputdict['https://httpbin.org'] == deque(['/status/200', '/status/404'])
    args.inputfile = os.path.join(RESOURCES_DIR, 'list-process.txt')
    args.blacklist = {'httpbin.org/status/404'}
    inputdict = cli.load_input_dict(args)
    assert inputdict['https://httpbin.org'] == deque(['/status/200'])
    # deduplication and filtering
    myinput = ['https://example.org/1', 'https://example.org/2', 'https://example.org/2', 'https://example.org/3', 'https://example.org/4', 'https://example.org/5', 'https://example.org/6']
    myblacklist = {'example.org/1', 'example.org/3', 'example.org/5'}
    inputdict = add_to_compressed_dict(myinput, myblacklist)
    assert inputdict['https://example.org'] == deque(['/2', '/4', '/6'])
    # URL in blacklist
    args.inputfile = os.path.join(RESOURCES_DIR, 'list-process.txt')
    my_urls = cli_utils.load_input_urls(args)
    my_blacklist = cli_utils.load_blacklist(os.path.join(RESOURCES_DIR, 'list-discard.txt'))
    inputdict = add_to_compressed_dict(my_urls, my_blacklist)
    assert len(inputdict) == 0
    # URL filter
    args.inputfile = os.path.join(RESOURCES_DIR, 'list-process.txt')
    my_urls = cli_utils.load_input_urls(args)
    assert len(add_to_compressed_dict(my_urls, None, ['status'], None)) == 1
    assert len(add_to_compressed_dict(my_urls, None, ['teststring'], None)) == 0
    assert len(add_to_compressed_dict(my_urls, None, ['status', 'teststring'], None)) == 1
    # malformed URLs
    inputdict = add_to_compressed_dict(['123345', 'https://www.example.org/1'], {}, None, None)
    assert len(inputdict) == 1
    # double URLs
    args.inputfile = os.path.join(RESOURCES_DIR, 'redundant-urls.txt')
    my_urls = cli_utils.load_input_urls(args)
    assert len(my_urls) == 5


if __name__ == '__main__':
    test_parser()
    test_climain()
    test_input_type()
    test_input_filtering()
    test_sysoutput()
    test_cli_pipeline()
    test_download()
