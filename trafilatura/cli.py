# -*- coding: utf-8 -*-
"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import argparse
import logging
import sys

from .core import process_record
from .utils import fetch_url
from .settings import MIN_FILE_SIZE, MAX_FILE_SIZE

LOGGER = logging.getLogger(__name__)


def examine(htmlstring, url, no_fallback=False, include_comments=True, include_tables=True, xml_output=False, tei_output=False):
    """ Generic safeguards and triggers """
    # safety check
    if htmlstring is None:
        sys.stderr.write('# ERROR: empty document\n')
    elif len(htmlstring) > MAX_FILE_SIZE:
        sys.stderr.write('# ERROR: file too large\n')
    elif len(htmlstring) < MIN_FILE_SIZE:
        sys.stderr.write('# ERROR: file too small\n')
    # proceed
    else:
        result = process_record(htmlstring, url, '0000', no_fallback=no_fallback, include_comments=include_comments, include_tables=include_tables, xml_output=xml_output, tei_output=tei_output)
        return result
    return None


def main():
    """ Run as a command-line utility. """
    # arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument("-f", "--fast", help="Fast (without fallback detection)", action="store_true")
    argsparser.add_argument("--nocomments", help="Don't output any comments", action="store_false")
    argsparser.add_argument("--notables", help="Don't output any table elements", action="store_false")
    argsparser.add_argument("--xml", help="XML output", action="store_true")
    argsparser.add_argument("--xmltei", help="XML TEI output", action="store_true")
    argsparser.add_argument("-u", "--URL", help="custom URL download")
    argsparser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = argsparser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # process input URL
    if args.URL:
        htmlstring = fetch_url(args.URL)
        if htmlstring is None:
            sys.stderr.write('# ERROR no valid result for url: ' + args.URL + '\n')
            sys.exit(1)
    # process input on STDIN
    else:
        # unicode check
        try:
            htmlstring = sys.stdin.read()
        except UnicodeDecodeError as err:
            sys.stderr.write('# ERROR system/buffer encoding: ' + str(err) + '\n')
            sys.exit(1)

    result = examine(htmlstring, url=args.url, no_fallback=args.fast, include_comments=args.nocomments, include_tables=args.notables, xml_output=args.xml, tei_output=args.xmltei)
    if result is not None:
        sys.stdout.write(result + '\n')


if __name__ == '__main__':
    main()
