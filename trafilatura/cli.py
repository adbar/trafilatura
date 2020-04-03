"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import argparse
import codecs
import logging
import random
import string
import sys

from os import makedirs, path
from time import sleep

from .core import extract
from .utils import fetch_url
from .settings import MIN_FILE_SIZE, MAX_FILE_SIZE


# fix output encoding on some systems
try:
    # > Python 3.7
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'UTF-8':
        sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'UTF-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

LOGGER = logging.getLogger(__name__)


def examine(htmlstring, url=None, no_fallback=False, include_comments=True,
            include_tables=True, csv_output=False, xml_output=False,
            tei_output=False, validation=False, formatting=False):
    """Generic safeguards and triggers"""
    # safety check
    if htmlstring is None:
        sys.stderr.write('# ERROR: empty document\n')
    elif len(htmlstring) > MAX_FILE_SIZE:
        sys.stderr.write('# ERROR: file too large\n')
    elif len(htmlstring) < MIN_FILE_SIZE:
        sys.stderr.write('# ERROR: file too small\n')
    # proceed
    else:
        result = extract(htmlstring, url, '0000', no_fallback=no_fallback,
                         include_comments=include_comments, include_tables=include_tables,
                         csv_output=csv_output, xml_output=xml_output,
                         tei_output=tei_output, tei_validation=validation,
                         include_formatting=formatting)
        return result
    return None


def parse_args(args):
    """Define parser for command-line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fast",
                        help="fast (without fallback detection)",
                        action="store_true")
    parser.add_argument("--formatting",
                        help="include text formatting (bold, italic, etc.)",
                        action="store_true")
    parser.add_argument("-i", "--inputfile",
                        help="name of input file for batch processing",
                        type=str)
    parser.add_argument("-o", "--outputdir",
                        help="write results in a specified directory (relative path)",
                        type=str)
    parser.add_argument("--nocomments",
                        help="don't output any comments",
                        action="store_false")  # false = no comments
    parser.add_argument("--notables",
                        help="don't output any table elements",
                        action="store_false")  # false = no tables
    parser.add_argument("--csv",
                        help="CSV output",
                        action="store_true")
    parser.add_argument("--xml",
                        help="XML output",
                        action="store_true")
    parser.add_argument("--xmltei",
                        help="XML TEI output",
                        action="store_true")
    parser.add_argument("--validate",
                        help="validate TEI output",
                        action="store_true")
    parser.add_argument("-u", "--URL",
                        help="custom URL download")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    return parser.parse_args()


def write_result(url, result, args):
    '''Deal with result (write to STDOUT or to file)'''
    if result is None:
        sys.stdout.write('# ERROR: no valid result for url ' + url + '\n')
    else:
        if args.outputdir is None:
            sys.stdout.write(result + '\n')
        else:
            # check the directory status
            if not path.isdir(args.outputdir):
                try:
                    makedirs(args.outputdir)
                except OSError:
                    raise
            # determine file name
            randomslug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
            extension = '.txt'
            if args.xml or args.xmltei:
                extension = '.xml'
            elif args.csv:
                extension = '.csv'
            # write
            output_path = path.join(args.outputdir, randomslug + extension)
            with open(output_path, mode='w', encoding='utf-8') as outputfile:
                outputfile.write(result)


def main():
    """ Run as a command-line utility. """
    # arguments
    args = parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if args.inputfile:
        # optional: errors='strict', buffering=1
        with open(args.inputfile, mode='r', encoding='utf-8') as inputfile:
            for line in inputfile:
                url = line.strip()
                htmlstring = fetch_url(url)
                try:
                    result = examine(htmlstring, url=url, no_fallback=args.fast,
                                     include_comments=args.nocomments, include_tables=args.notables,
                                     csv_output=args.csv, xml_output=args.xml, tei_output=args.xmltei,
                                     validation=args.validate, formatting=args.formatting)
                # ugly but efficient
                except Exception as err:
                    result = '# ERROR:' + err + sys.exc_info()[0] + ' for url ' + url + '\n'
                write_result(url, result, args)
                # sleep 2 sec between requests
                sleep(2)
    else:
        # process input URL
        if args.URL:
            htmlstring = fetch_url(args.URL)
            if htmlstring is None:
                sys.exit('# ERROR no valid result for url: ' + args.URL + '\n')
        # process input on STDIN
        else:
            # unicode check
            try:
                htmlstring = sys.stdin.read()
            except UnicodeDecodeError as err:
                sys.exit('# ERROR system/buffer encoding: ' + err + '\n')
        # process
        result = examine(htmlstring, url=args.URL, no_fallback=args.fast,
                         include_comments=args.nocomments, include_tables=args.notables,
                         csv_output=args.csv, xml_output=args.xml, tei_output=args.xmltei,
                         validation=args.validate, formatting=args.formatting)
        write_result(args.URL, result, args)


if __name__ == '__main__':
    main()
