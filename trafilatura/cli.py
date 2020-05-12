"""
Implementing a basic command-line interface.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import argparse
import logging
import random
import string
import sys

from os import makedirs, path, walk
from time import sleep

from .core import extract
from .feeds import find_feed_urls
from .utils import fetch_url
from .settings import MIN_FILE_SIZE, MAX_FILE_SIZE, SLEEP_TIME


LOGGER = logging.getLogger(__name__)
random.seed(345)  # make generated file names reproducible

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


def examine(htmlstring, url=None, no_fallback=False, include_comments=True,
            include_tables=True, csv_output=False, xml_output=False,
            tei_output=False, validation=False, formatting=False):
    """Generic safeguards and triggers"""
    result = None
    # safety check
    if htmlstring is None:
        sys.stderr.write('# ERROR: empty document\n')
    elif len(htmlstring) > MAX_FILE_SIZE:
        sys.stderr.write('# ERROR: file too large\n')
    elif len(htmlstring) < MIN_FILE_SIZE:
        sys.stderr.write('# ERROR: file too small\n')
    # proceed
    else:
        try:
            result = extract(htmlstring, url, '0000', no_fallback=no_fallback,
                             include_comments=include_comments, include_tables=include_tables,
                             csv_output=csv_output, xml_output=xml_output,
                             tei_output=tei_output, tei_validation=validation,
                             include_formatting=formatting)
        # ugly but efficient
        except Exception as err:
            sys.stderr.write('# ERROR: ' + str(err) + '\nDetails: ' + str(sys.exc_info()[0]) + '\n')
    return result


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
    parser.add_argument("--inputdir",
                        help="read files from a specified directory (relative path)",
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
    parser.add_argument("--feed",
                        help="pass a feed URL as input",
                        type=str)
    parser.add_argument("--list",
                        help="return a list of URLs without downloading them",
                        action="store_true")
    return parser.parse_args()


def check_outputdir_status(args):
    '''Check if the output directory is within reach and writable'''
    # check the directory status
    if not path.exists(args.outputdir) or not path.isdir(args.outputdir):
        try:
            makedirs(args.outputdir)
        except OSError:
            sys.stderr.write('# ERROR: Destination directory cannot be created: ' + args.outputdir + '\n')
            # raise OSError()
            return False
    return True


def determine_filename(args):
    '''Pick a file name based on output type'''
    randomslug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    extension = '.txt'
    if args.xml or args.xmltei:
        extension = '.xml'
    elif args.csv:
        extension = '.csv'
    return path.join(args.outputdir, randomslug + extension)


def write_result(result, args):
    '''Deal with result (write to STDOUT or to file)'''
    if result is None:
        return
    if args.outputdir is None:
        sys.stdout.write(result + '\n')
    else:
       # check the directory status
        if check_outputdir_status(args) is True:
            # pick a new file name
            output_path = determine_filename(args)
            while path.exists(output_path):
                output_path = determine_filename(args)
            # write
            with open(output_path, mode='w', encoding='utf-8') as outputfile:
                outputfile.write(result)


def processing_pipeline(args, input_urls, sleeptime):
    '''Aggregated functions to show a list and download and process an input list'''
    if input_urls is None or len(input_urls) == 0:
        return
    for url in input_urls:
        if args.list:
            write_result(url, args)  # print('\n'.join(input_urls))
        else:
            htmlstring = fetch_url(url)
            result = examine(htmlstring, url=url, no_fallback=args.fast,
                             include_comments=args.nocomments, include_tables=args.notables,
                             csv_output=args.csv, xml_output=args.xml, tei_output=args.xmltei,
                             validation=args.validate, formatting=args.formatting)
            write_result(result, args)
            # sleep between requests
            sleep(sleeptime)


def main():
    """ Run as a command-line utility. """
    # arguments
    args = parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # processing according to mutually exclusive options
    # read url list from input file
    if args.inputfile:
        input_urls = list()
        try:
            # optional: errors='strict', buffering=1
            with open(args.inputfile, mode='r', encoding='utf-8') as inputfile:
                for line in inputfile:
                    if not line.startswith('http'):
                        LOGGER.warning('Not an URL, discarding line: %s', line)
                        continue
                    input_urls.append(line.strip())
        except UnicodeDecodeError:
            sys.exit('# ERROR: system, file type or buffer encoding')
        processing_pipeline(args, input_urls, SLEEP_TIME)
    # fetch urls from a feed
    elif args.feed:
        links = find_feed_urls(args.feed)
        processing_pipeline(args, links, SLEEP_TIME)
    # read files from an input directory
    elif args.inputdir:
        #if not args.outputdir:
        #    sys.exit('# ERROR: please specify an output directory along with the input directory')
        # walk the directory tree
        for root, _, inputfiles in walk(args.inputdir):
            for fname in inputfiles:
                try:
                    with open(path.join(root, fname), mode='r', encoding='utf-8') as inputfh:
                        htmlstring = inputfh.read()
                except UnicodeDecodeError:
                    LOGGER.warning('Discarding (file type issue): %s', path.join(root, fname))
                else:
                    result = examine(htmlstring, url=args.URL, no_fallback=args.fast,
                                     include_comments=args.nocomments, include_tables=args.notables,
                                     csv_output=args.csv, xml_output=args.xml, tei_output=args.xmltei,
                                     validation=args.validate, formatting=args.formatting)
                    write_result(result, args)
    # read from input directly
    else:
        # process input URL
        if args.URL:
            htmlstring = fetch_url(args.URL)
            if htmlstring is None:
                sys.exit('# ERROR: no valid result for url: ' + args.URL + '\n')
        # process input on STDIN
        else:
            # file type and unicode check
            try:
                htmlstring = sys.stdin.read()
            except UnicodeDecodeError:
                sys.exit('# ERROR: system, file type or buffer encoding')
        # process
        result = examine(htmlstring, url=args.URL, no_fallback=args.fast,
                         include_comments=args.nocomments, include_tables=args.notables,
                         csv_output=args.csv, xml_output=args.xml, tei_output=args.xmltei,
                         validation=args.validate, formatting=args.formatting)
        write_result(result, args)


if __name__ == '__main__':
    main()
