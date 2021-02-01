"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import argparse
import logging
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed

from .cli_utils import (load_blacklist, load_input_dict, load_input_urls,
                        convert_inputlist,
                        file_processing_pipeline, url_processing_pipeline,
                        examine, write_result)
from .feeds import find_feed_urls
from .settings import DOWNLOAD_THREADS
from .sitemaps import sitemap_search


LOGGER = logging.getLogger(__name__)


# fix output encoding on some systems
try:
    # > Python 3.7
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'UTF-8':
        sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'UTF-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def parse_args(args):
    """Define parser for command-line arguments"""
    parser = argparse.ArgumentParser(description='Command-line interface for Trafilatura')
    group1 = parser.add_argument_group('Input', 'URLs, files or directories to process')
    group1_ex = group1.add_mutually_exclusive_group()
    group2 = parser.add_argument_group('Output', 'Determines if and how files will be written')
    group3 = parser.add_argument_group('Navigation', 'Link discovery and web crawling')
    group3_ex = group3.add_mutually_exclusive_group()
    group4 = parser.add_argument_group('Extraction', 'Customization of text and metadata processing')
    group5 = parser.add_argument_group('Format', 'Selection of the output format')
    group5_ex = group5.add_mutually_exclusive_group()

    group1_ex.add_argument("-i", "--inputfile",
                        help="name of input file for batch processing",
                        type=str)
    group1_ex.add_argument("--inputdir",
                        help="read files from a specified directory (relative path)",
                        type=str)
    group1_ex.add_argument("-u", "--URL",
                        help="custom URL download",
                        type=str)

    group1.add_argument('--parallel',
                        help="specify a number of cores/threads for downloads and/or processing",
                        type=int, default=DOWNLOAD_THREADS)
    group1.add_argument('-b', '--blacklist',
                        help="file containing unwanted URLs to discard during processing",
                        type=str)

    group2.add_argument("--list",
                        help="display a list of URLs without downloading them",
                        action="store_true")
    group2.add_argument("-o", "--outputdir",
                        help="write results in a specified directory (relative path)",
                        type=str)
    group2.add_argument('--backup-dir',
                        help="preserve a copy of downloaded files in a backup directory",
                        type=str)
    group2.add_argument('--keep-dirs',
                        help="keep input directory structure and file names",
                        action="store_true")
    group2.add_argument('--hash-as-name',
                        help="use hash value as output file name instead of random default",
                        action="store_true")

    group3_ex.add_argument("--feed",
                        help="look for feeds and/or pass a feed URL as input",
                        nargs='?', const=True, default=False)
    group3_ex.add_argument("--sitemap",
                        help="look for sitemaps for the given website and/or enter a sitemap URL",
                        nargs='?', const=True, default=False)
    group3.add_argument('--archived',
                        help='try to fetch URLs from the Internet Archive if downloads fail',
                        action="store_true")
    group3.add_argument('--url-filter',
                        help="only process/output URLs containing these patterns (space-separated strings)",
                        nargs='+', type=str)
    #group3.add_argument('--no-ssl',
    #                    help="Disable secure connections (to prevent SSLError)",
    #                    action="store_true")

    group4.add_argument("-f", "--fast",
                        help="fast (without fallback detection)",
                        action="store_true")
    group4.add_argument("--formatting",
                        help="include text formatting (bold, italic, etc.)",
                        action="store_true")
    group4.add_argument("--links",
                        help="include links along with their targets (experimental)",
                        action="store_true")
    group4.add_argument("--images",
                        help="include image sources in output (experimental)",
                        action="store_true")
    group4.add_argument("--nocomments",
                        help="don't output any comments",
                        action="store_false")  # false = no comments
    group4.add_argument("--notables",
                        help="don't output any table elements",
                        action="store_false")  # false = no tables
    group4.add_argument("--with-metadata",
                        help="only output those documents with necessary metadata: title, URL and date (CSV and XML formats)",
                        action="store_true")
    group4.add_argument("--target-language",
                        help="select a target language (ISO 639-1 codes)",
                        type=str)
    group4.add_argument("--deduplicate",
                        help="filter out duplicate documents and sections",
                        action="store_true")
    group4.add_argument("--config-file",
                        help="override standard extraction parameters with a custom config file",
                        type=str)

    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group
    group5_ex.add_argument('-out', '--output-format',
                        help="determine output format",
                        choices=['txt', 'csv', 'json', 'xml', 'xmltei'],
                        default='txt')
    group5_ex.add_argument("--csv",
                        help="shorthand for CSV output",
                        action="store_true")
    group5_ex.add_argument("--json",
                        help="shorthand for JSON output",
                        action="store_true")
    group5_ex.add_argument("--xml",
                        help="shorthand for XML output",
                        action="store_true")
    group5_ex.add_argument("--xmltei",
                        help="shorthand for XML TEI output",
                        action="store_true")
    group5.add_argument("--validate-tei",
                        help="validate XML TEI output",
                        action="store_true")

    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="increase logging verbosity (-v or -vv)",
                        )

    # wrap in mapping to prevent invalid input
    return map_args(parser.parse_args())


def map_args(args):
    '''Map existing options to format choice.'''
    if args.csv:
        args.output_format = 'csv'
    elif args.json:
        args.output_format = 'json'
    elif args.xml:
        args.output_format = 'xml'
    elif args.xmltei:
        args.output_format = 'xmltei'
    return args


def main():
    """ Run as a command-line utility. """
    args = parse_args(sys.argv[1:])
    process_args(args)


def process_args(args):
    """Perform the actual processing according to the arguments"""
    # verbosity
    if args.verbose == 1:
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    elif args.verbose >= 2:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if args.blacklist:
        args.blacklist = load_blacklist(args.blacklist)
    # processing according to mutually exclusive options
    # read url list from input file
    if args.inputfile and args.feed is False and args.sitemap is False:
        inputdict = load_input_dict(args.inputfile, args.blacklist)
        url_processing_pipeline(args, inputdict)
    # fetch urls from a feed or a sitemap
    elif args.feed or args.sitemap:
        # load input URLs
        if args.inputfile:
            input_urls = load_input_urls(args.inputfile)
        elif args.feed:
            input_urls = [args.feed]
        elif args.sitemap:
            input_urls = [args.sitemap]
        # link discovery and storage
        inputdict = None
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            if args.feed:
                future_to_url = {executor.submit(find_feed_urls, url, target_lang=args.target_language): url for url in input_urls}
            elif args.sitemap:
                future_to_url = {executor.submit(sitemap_search, url, target_lang=args.target_language): url for url in input_urls}
            # process results one-by-one, i.e. in parallel
            for future in as_completed(future_to_url):
                if future.result() is not None:
                    inputdict = convert_inputlist(args.blacklist, future.result(), args.url_filter, inputdict)
                    url_processing_pipeline(args, inputdict)
                    inputdict = None
    # read files from an input directory
    elif args.inputdir:
        file_processing_pipeline(args)
    # read from input directly
    else:
        # process input URL
        if args.URL:
            inputdict = convert_inputlist(args, [args.URL], None)
            url_processing_pipeline(args, inputdict)  # process single url
        # process input on STDIN
        else:
            # file type and unicode check
            try:
                htmlstring = sys.stdin.read()
            except UnicodeDecodeError:
                sys.exit('ERROR: system, file type or buffer encoding')
            # process
            result = examine(htmlstring, args, url=args.URL)
            write_result(result, args)


if __name__ == '__main__':
    main()
