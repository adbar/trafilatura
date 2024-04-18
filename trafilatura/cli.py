"""
Implementing a basic command-line interface.
"""

import argparse
import logging
import sys
import warnings
from platform import python_version

from . import __version__
from .cli_utils import (cli_crawler, cli_discovery, examine,
                        file_processing_pipeline, load_blacklist,
                        load_input_dict, probe_homepage,
                        url_processing_pipeline, write_result)
from .settings import PARALLEL_CORES

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


def add_args(parser):
    "Add argument groups and arguments to parser."

    group1 = parser.add_argument_group('Input', 'URLs, files or directories to process')
    group1_ex = group1.add_mutually_exclusive_group()
    group2 = parser.add_argument_group('Output', 'Determines if and how files will be written')
    group3 = parser.add_argument_group('Navigation', 'Link discovery and web crawling')
    group3_ex = group3.add_mutually_exclusive_group()
    group4 = parser.add_argument_group('Extraction', 'Customization of text and metadata processing')
    group5 = parser.add_argument_group('Format', 'Selection of the output format')
    group5_ex = group5.add_mutually_exclusive_group()

    group1_ex.add_argument("-i", "--input-file",
                        help="name of input file for batch processing",
                        type=str)
    group1_ex.add_argument("--inputfile",
                        help=argparse.SUPPRESS,
                        type=str)   # will be deprecated
    group1_ex.add_argument("--input-dir",
                        help="read files from a specified directory (relative path)",
                        type=str)
    group1_ex.add_argument("--inputdir",
                        help=argparse.SUPPRESS,
                        type=str)   # will be deprecated
    group1_ex.add_argument("-u", "--URL",
                        help="custom URL download",
                        type=str)

    group1.add_argument('--parallel',
                        help="specify a number of cores/threads for downloads and/or processing",
                        type=int, default=PARALLEL_CORES)
    group1.add_argument('-b', '--blacklist',
                        help="file containing unwanted URLs to discard during processing",
                        type=str)

    group2.add_argument("--list",
                        help="display a list of URLs without downloading them",
                        action="store_true")
    group2.add_argument("-o", "--output-dir",
                        help="write results in a specified directory (relative path)",
                        type=str)
    group2.add_argument("--outputdir",
                        help=argparse.SUPPRESS,
                        type=str)   # will be deprecated
    group2.add_argument('--backup-dir',
                        help="preserve a copy of downloaded files in a backup directory",
                        type=str)
    group2.add_argument('--keep-dirs',
                        help="keep input directory structure and file names",
                        action="store_true")
    group2.add_argument('--hash-as-name',
                        help=argparse.SUPPRESS,
                        action="store_true")   # will be deprecated

    group3_ex.add_argument("--feed",
                        help="look for feeds and/or pass a feed URL as input",
                        nargs='?', const=True, default=False)
    group3_ex.add_argument("--sitemap",
                        help="look for sitemaps for the given website and/or enter a sitemap URL",
                        nargs='?', const=True, default=False)
    group3_ex.add_argument("--crawl",
                        help="crawl a fixed number of pages within a website starting from the given URL",
                        nargs='?', const=True, default=False)
    group3_ex.add_argument("--explore",
                        help="explore the given websites (combination of sitemap and crawl)",
                        nargs='?', const=True, default=False)
    group3_ex.add_argument("--probe",
                        help="probe for extractable content (works best with target language)",
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
                        help=argparse.SUPPRESS,
                        action="store_false")  # will be deprecated
    group4.add_argument("--notables",
                        help=argparse.SUPPRESS,
                        action="store_false")  # will be deprecated
    group4.add_argument("--no-comments",
                        help="don't output any comments",
                        action="store_false")  # false = no comments
    group4.add_argument("--no-tables",
                        help="don't output any table elements",
                        action="store_false")  # false = no tables
    group4.add_argument("--only-with-metadata",
                        help="only output those documents with title, URL and date (for formats supporting metadata)",
                        action="store_true")
    group4.add_argument("--with-metadata",
                        help=argparse.SUPPRESS,
                        action="store_true")   # will be deprecated
    group4.add_argument("--target-language",
                        help="select a target language (ISO 639-1 codes)",
                        type=str)
    group4.add_argument("--deduplicate",
                        help="filter out duplicate documents and sections",
                        action="store_true")
    group4.add_argument("--config-file",
                        help="override standard extraction parameters with a custom config file",
                        type=str)
    group4.add_argument("--precision",
                        help="favor extraction precision (less noise, possibly less text)",
                        action="store_true")
    group4.add_argument("--recall",
                        help="favor extraction recall (more text, possibly more noise)",
                        action="store_true")

    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group
    group5_ex.add_argument('-out', '--output-format',
                        help="determine output format",
                        choices=['txt', 'csv', 'json', 'markdown', 'xml', 'xmltei'],
                        default='txt')
    group5_ex.add_argument("--csv",
                        help="shorthand for CSV output",
                        action="store_true")
    group5_ex.add_argument("--json",
                        help="shorthand for JSON output",
                        action="store_true")
    group5_ex.add_argument("--markdown",
                        help="shorthand for MD output",
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
    parser.add_argument(
        "--version",
        help="show version information and exit",
        action="version",
        version=f"Trafilatura {__version__} - Python {python_version()}",
    )

    return parser


def parse_args(args):
    """Define parser for command-line arguments"""
    parser = argparse.ArgumentParser(description='Command-line interface for Trafilatura')
    parser = add_args(parser)
    # wrap in mapping to prevent invalid input
    return map_args(parser.parse_args())


def map_args(args):
    '''Map existing options to format and output choices.'''
    # formats
    if args.csv:
        args.output_format = 'csv'
    elif args.json:
        args.output_format = 'json'
    elif args.markdown:
        args.output_format = 'markdown'
    elif args.xml:
        args.output_format = 'xml'
    elif args.xmltei:
        args.output_format = 'xmltei'
    # output configuration
    if args.nocomments is False:
        args.no_comments = False
        warnings.warn(
            """--nocomments will be deprecated in a future version,
               use --no-comments instead""",
             PendingDeprecationWarning
        )
    if args.notables is False:
        args.no_tables = False
        warnings.warn(
            """--notables will be deprecated in a future version,
               use --no-tables instead""",
             PendingDeprecationWarning
        )
    if args.with_metadata is True:
        args.only_with_metadata = True
        warnings.warn(
            """--with-metadata will be deprecated in a future version,
               use --only-with-metadata instead""",
             PendingDeprecationWarning
        )
    if args.inputfile:
        args.input_file = args.inputfile
        warnings.warn(
            """--inputfile will be deprecated in a future version,
               use --input-file instead""",
             PendingDeprecationWarning
        )
    if args.inputdir:
        args.input_dir = args.inputdir
        warnings.warn(
            """--inputdir will be deprecated in a future version,
               use --input-dir instead""",
             PendingDeprecationWarning
        )
    if args.outputdir:
        args.output_dir = args.outputdir
        warnings.warn(
            """--outputdir will be deprecated in a future version,
               use --output-dir instead""",
             PendingDeprecationWarning
        )
    if args.hash_as_name:
        warnings.warn(
            """--hash-as-name will be deprecated in a future version,
               hashes are now used by default.""",
             PendingDeprecationWarning
        )
    return args


def main():
    """ Run as a command-line utility. """
    args = parse_args(sys.argv[1:])
    process_args(args)


def process_args(args):
    """Perform the actual processing according to the arguments"""
    # init
    error_caught = False
    # verbosity
    if args.verbose == 1:
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    elif args.verbose >= 2:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if args.blacklist:
        args.blacklist = load_blacklist(args.blacklist)

    # processing according to mutually exclusive options
    # read url list from input file
    if args.input_file and all([not args.crawl, not args.explore, not args.feed, not args.probe, not args.sitemap]):
        url_store = load_input_dict(args)
        error_caught = url_processing_pipeline(args, url_store)

    # fetch urls from a feed or a sitemap
    elif args.explore or args.feed or args.sitemap:
        cli_discovery(args)

    # activate crawler/spider
    elif args.crawl:
        cli_crawler(args)

    # probe and print only
    elif args.probe:
        probe_homepage(args)

    # read files from an input directory
    elif args.input_dir:
        file_processing_pipeline(args)

    # process input URL
    elif args.URL:
        url_store = load_input_dict(args)
        error_caught = url_processing_pipeline(args, url_store)  # process single url

    # read input on STDIN directly
    else:
        # file type and unicode check
        try:
            htmlstring = sys.stdin.read()
        except UnicodeDecodeError:
            sys.exit('ERROR: system, file type or buffer encoding')
        # process
        result = examine(htmlstring, args, url=args.URL)
        write_result(result, args)

    # change exit code if there are errors
    if error_caught is True:
        sys.exit(1)


if __name__ == '__main__':
    main()
