"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import argparse
import logging
import sys

from functools import partial
from multiprocessing import cpu_count, Pool

from .cli_utils import (load_blacklist, load_input_urls, generate_filelist,
                        file_processing_pipeline, url_processing_pipeline,
                        examine, write_result)
from .feeds import find_feed_urls
from .settings import SLEEP_TIME


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
    group1 = parser.add_argument_group('I/O', 'Input and output options affecting processing')
    group2 = parser.add_argument_group('Format', 'Selection of the output format')
    group3 = parser.add_argument_group('Extraction', 'Customization of text and metadata extraction')
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    group1.add_argument("-i", "--inputfile",
                        help="name of input file for batch processing",
                        type=str)
    group1.add_argument("--inputdir",
                        help="read files from a specified directory (relative path)",
                        type=str)
    group1.add_argument("-o", "--outputdir",
                        help="write results in a specified directory (relative path)",
                        type=str)
    group1.add_argument("-u", "--URL",
                        help="custom URL download")
    group1.add_argument("--feed",
                        help="pass a feed URL as input",
                        type=str)
    group1.add_argument("--list",
                        help="return a list of URLs without downloading them",
                        action="store_true")
    group1.add_argument('-b', '--blacklist',
                        help="""name of file containing already processed or
                                unwanted URLs to discard during batch processing""",
                        type=str)
    group1.add_argument('--backup-dir',
                        help="Preserve a copy of downloaded files in a backup directory",
                        type=str)

    group2.add_argument('-out', '--output-format',
                        help="determine output format",
                        choices=['txt', 'csv', 'xml', 'xmltei'],
                        default='txt')
    group2.add_argument("--csv",
                        help="CSV output",
                        action="store_true")
    group2.add_argument("--xml",
                        help="XML output",
                        action="store_true")
    group2.add_argument("--xmltei",
                        help="XML TEI output",
                        action="store_true")
    group2.add_argument("--validate",
                        help="validate TEI output",
                        action="store_true")

    group3.add_argument("-f", "--fast",
                        help="fast (without fallback detection)",
                        action="store_true")
    group3.add_argument("--formatting",
                        help="include text formatting (bold, italic, etc.)",
                        action="store_true")
    group3.add_argument("--nocomments",
                        help="don't output any comments",
                        action="store_false")  # false = no comments
    group3.add_argument("--notables",
                        help="don't output any table elements",
                        action="store_false")  # false = no tables
    return parser.parse_args()


def map_args(args):
    '''Map existing options to format choice.'''
    if args.csv:
        args.output_format = 'csv'
    elif args.xml:
        args.output_format = 'xml'
    elif args.xmltei:
        args.output_format = 'xmltei'
    return args


def main():
    """ Run as a command-line utility. """
    # arguments
    args = parse_args(sys.argv[1:])
    args = map_args(args)
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if args.blacklist:
        args.blacklist = load_blacklist(args.blacklist)
    # processing according to mutually exclusive options
    # read url list from input file
    if args.inputfile and not args.feed:
        input_urls = load_input_urls(args.inputfile)
        url_processing_pipeline(args, input_urls, SLEEP_TIME)
    # fetch urls from a feed
    elif args.feed:
        if args.inputfile:
            links = list()
            for feed_url in load_input_urls(args.inputfile):
                links.extend(find_feed_urls(feed_url))
        else:
            links = find_feed_urls(args.feed)
        url_processing_pipeline(args, links, SLEEP_TIME)
    # read files from an input directory
    elif args.inputdir:
        #if not args.outputdir:
        #    sys.exit('# ERROR: please specify an output directory along with the input directory')
        # multiprocessing
        with Pool(processes=min(cpu_count(), 16)) as pool:  # 16 processes at most
            pool.map(partial(file_processing_pipeline, args=args), generate_filelist(args.inputdir))
    # read from input directly
    else:
        # process input URL
        if args.URL:
            url_processing_pipeline(args, [args.URL], 0)  # process single url
            #if htmlstring is None:
            #    sys.exit('# ERROR: no valid result for url: ' + args.URL + '\n')
        # process input on STDIN
        else:
            # file type and unicode check
            try:
                htmlstring = sys.stdin.read()
            except UnicodeDecodeError:
                sys.exit('# ERROR: system, file type or buffer encoding')
            # process
            result = examine(htmlstring, args, url=args.URL)
            write_result(result, args)


if __name__ == '__main__':
    main()
