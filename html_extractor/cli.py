# -*- coding: utf-8 -*-
"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/html-extractor
## under GNU GPL v3 license

import argparse
import logging
import sys

from html_extractor import process_record



def examine(htmlstring):
    """ Generic safeguards and triggers """
    # safety check
    if len(htmlstring) > 20000000:
        sys.stderr.write('# ERROR: file too large\n')
    elif len(htmlstring) < 10:
        sys.stderr.write('# ERROR: file too small\n')
    # proceed
    else:
        result = process_record(htmlstring, None, '0000', tei_output=True)
        return result
    return None



def main():
    """ Run as a command-line utility. """
    # arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = argsparser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    ## process input on STDIN
    # unicode check
    try:
        htmlstring = sys.stdin.read()
    except UnicodeDecodeError as err:
        sys.stderr.write('# ERROR system/buffer encoding: ' + str(err) + '\n')
        sys.exit(1)

    result = examine(htmlstring)
    if result is not None:
        sys.stdout.write(result + '\n')

if __name__ == '__main__':
    main()
