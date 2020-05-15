"""
Functions dedicated to command-line processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import logging
import random
import string
import sys

from os import makedirs, path, walk
from time import sleep

from .core import extract
from .settings import MIN_FILE_SIZE, MAX_FILE_SIZE
from .utils import fetch_url


LOGGER = logging.getLogger(__name__)
random.seed(345)  # make generated file names reproducible


def load_input_urls(filename):
    '''Read list of URLs to process'''
    input_urls = list()
    try:
        # optional: errors='strict', buffering=1
        with open(filename, mode='r', encoding='utf-8') as inputfile:
            for line in inputfile:
                if not line.startswith('http'):
                    LOGGER.warning('Not an URL, discarding line: %s', line)
                    continue
                input_urls.append(line.strip())
    except UnicodeDecodeError:
        sys.exit('# ERROR: system, file type or buffer encoding')
    return input_urls


def load_blacklist(filename):
    '''Read list of unwanted URLs'''
    blacklist = set()
    with open(filename, mode='r', encoding='utf-8') as inputfh:
        for line in inputfh:
            blacklist.add(line.strip())
    return blacklist


def check_outputdir_status(directory):
    '''Check if the output directory is within reach and writable'''
    # check the directory status
    if not path.exists(directory) or not path.isdir(directory):
        try:
            makedirs(directory)
        except OSError:
            sys.stderr.write('# ERROR: Destination directory cannot be created: ' + directory + '\n')
            # raise OSError()
            return False
    return True


def determine_filename(args, fileslug=None):
    '''Pick a file name based on output type'''
    # determine extension
    extension = '.txt'
    if args.xml or args.xmltei or args.output_format == 'xml':
        extension = '.xml'
    elif args.csv or args.output_format == 'csv':
        extension = '.csv'
    # determine file slug
    if fileslug is None:
        output_path = path.join(args.outputdir, \
            ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6)) \
            + extension)
        while path.exists(output_path):
            output_path = path.join(args.outputdir, \
                ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6)) \
                + extension)
    else:
        output_path = path.join(args.outputdir, fileslug + extension)
    return output_path


def archive_html(htmlstring, args):
    '''Write a copy of raw HTML in backup directory'''
    # determine file name
    fileslug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    output_path = path.join(args.backup_dir, fileslug + '.html')
    while path.exists(output_path):
        fileslug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        output_path = path.join(args.backup_dir, fileslug + '.html')
    # check the directory status
    if check_outputdir_status(args.backup_dir) is True:
        # write
        with open(output_path, mode='w', encoding='utf-8') as outputfile:
            outputfile.write(htmlstring)
    return fileslug


def write_result(result, args, filename=None):
    '''Deal with result (write to STDOUT or to file)'''
    if result is None:
        return
    if args.outputdir is None:
        sys.stdout.write(result + '\n')
    else:
       # check the directory status
        if check_outputdir_status(args.outputdir) is True:
            # write
            with open(determine_filename(args, filename), mode='w', encoding='utf-8') as outputfile:
                outputfile.write(result)


def generate_filelist(inputdir):
    '''Walk the directory tree and output all file names'''
    for root, _, inputfiles in walk(inputdir):
        for fname in inputfiles:
            # filelist.append(path.join(root, fname))
            yield path.join(root, fname)


def file_processing_pipeline(filename, args):
    '''Aggregated functions to process a file list'''
    try:
        with open(filename, mode='r', encoding='utf-8') as inputfh:
            htmlstring = inputfh.read()
    except UnicodeDecodeError:
        LOGGER.warning('Discarding (file type issue): %s', filename)
    else:
        result = examine(htmlstring, args, url=args.URL)
        write_result(result, args)


def url_processing_pipeline(args, input_urls, sleeptime):
    '''Aggregated functions to show a list and download and process an input list'''
    # control blacklist
    if args.blacklist:
        input_urls = set(input_urls).difference(args.blacklist)
    # safety check
    if len(input_urls) == 0:
        return
    # process
    for url in input_urls:
        if args.list:
            write_result(url, args)  # print('\n'.join(input_urls))
        else:
            htmlstring = fetch_url(url)
            if args.backup_dir:
                filename = archive_html(htmlstring, args)
            else:
                filename = None
            result = examine(htmlstring, args, url=url)
            write_result(result, args, filename)
            # sleep between requests
            sleep(sleeptime)


def examine(htmlstring, args, url=None):
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
            result = extract(htmlstring, url, '0000', no_fallback=args.fast,
                             include_comments=args.nocomments, include_tables=args.notables,
                             include_formatting=args.formatting,
                             output_format=args.output_format, tei_validation=args.validate)
        # ugly but efficient
        except Exception as err:
            sys.stderr.write('# ERROR: ' + str(err) + '\nDetails: ' + str(sys.exc_info()[0]) + '\n')
    return result
