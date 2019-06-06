# -*- coding: utf-8 -*-
"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/html-extractor
## under GNU GPL v3 license

import argparse
import logging
import sys

import chardet
import requests

from html_extractor import process_record

logger = logging.getLogger(__name__)


def fetch_url(url):
    """ Fetch page using requests """
    response = requests.get(url)
    if int(response.status_code) != 200:
        return None
    logger.debug('response encoding: %s', response.encoding)
    guessed_encoding = chardet.detect(response.content)['encoding']
    logger.debug('guessed encoding: %s', guessed_encoding)
    if guessed_encoding is not None:
        htmltext = response.content.decode(guessed_encoding)
    else:
        htmltext = response.text
    return htmltext


def examine(htmlstring, url, txtflag, xmlteiflag):
    """ Generic safeguards and triggers """
    # safety check
    if len(htmlstring) > 10000000:
        sys.stderr.write('# ERROR: file too large\n')
    elif len(htmlstring) < 10:
        sys.stderr.write('# ERROR: file too small\n')
    # proceed
    else:
        if txtflag is True:
            result = process_record(htmlstring, url, '0000', txt_output=True, tei_output=False)
        elif xmlteiflag is True:
            result = process_record(htmlstring, url, '0000', txt_output=False, tei_output=True)
        else:
            result = process_record(htmlstring, url, '0000', txt_output=False, tei_output=False)
        return result
    return None


def main():
    """ Run as a command-line utility. """
    # arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument("--txt", help="TXT output", action="store_true")
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

    result = examine(htmlstring, args.URL, args.txt, args.xmltei)
    if result is not None:
        sys.stdout.write(result + '\n')


if __name__ == '__main__':
    main()
