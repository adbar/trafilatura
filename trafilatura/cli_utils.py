"""
Functions dedicated to command-line processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import logging
import random
import re
import signal
import string
import sys

from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from os import makedirs, path, walk
from time import sleep

from .core import extract
from .settings import (DOWNLOAD_THREADS, FILENAME_LEN, FILE_PROCESSING_CORES,
                       MIN_FILE_SIZE, MAX_FILE_SIZE, MAX_FILES_PER_DIRECTORY,
                       PROCESSING_TIMEOUT)
from .utils import fetch_url


LOGGER = logging.getLogger(__name__)
random.seed(345)  # make generated file names reproducible


# try signal https://stackoverflow.com/questions/492519/timeout-on-a-function-call
def handler(signum, frame):
    '''Raise a timeout exception to handle rare malicious files'''
    raise Exception('unusual file processing time, aborting')


def load_input_urls(filename):
    '''Read list of URLs to process'''
    input_urls = list()
    try:
        # optional: errors='strict', buffering=1
        with open(filename, mode='r', encoding='utf-8') as inputfile:
            for line in inputfile:
                url_match = re.match(r'https?://[^ ]+', line.strip())  # if not line.startswith('http'):
                try:
                    input_urls.append(url_match.group(0))
                except AttributeError:
                    LOGGER.warning('Not an URL, discarding line: %s', line)
                    continue
    except UnicodeDecodeError:
        sys.exit('# ERROR: system, file type or buffer encoding')
    return input_urls


def load_blacklist(filename):
    '''Read list of unwanted URLs'''
    blacklist = set()
    with open(filename, mode='r', encoding='utf-8') as inputfh:
        for line in inputfh:
            url = line.strip()
            blacklist.add(url)
            # add http/https URLs for safety
            if url.startswith('https'):
                blacklist.add(re.sub(r'^https', 'http', url))
            elif url.startswith('http'):
                blacklist.add(re.sub(r'^http:', 'https:', url))
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


def determine_filename(args, destination_directory, fileslug=None):
    '''Pick a file name based on output type'''
    # determine extension
    extension = '.txt'
    if args.xml or args.xmltei or args.output_format == 'xml':
        extension = '.xml'
    elif args.csv or args.output_format == 'csv':
        extension = '.csv'
    # determine file slug
    if fileslug is None:
        output_path = path.join(destination_directory, \
            ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(FILENAME_LEN)) \
            + extension)
        while path.exists(output_path):
            output_path = path.join(destination_directory, \
                ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(FILENAME_LEN)) \
                + extension)
    else:
        output_path = path.join(destination_directory, fileslug + extension)
    return output_path


def determine_counter_dir(dirname, counter):
    '''Return a destination directory based on a file counter'''
    if counter is not None:
        counter_dir = str(int(counter/MAX_FILES_PER_DIRECTORY) + 1)
    else:
        counter_dir = ''
    return path.join(dirname, counter_dir)


def archive_html(htmlstring, args, counter=None):
    '''Write a copy of raw HTML in backup directory'''
    destination_directory = determine_counter_dir(args.backup_dir, counter)
    fileslug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(FILENAME_LEN))
    output_path = path.join(destination_directory, fileslug + '.html')
    while path.exists(output_path):
        fileslug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(FILENAME_LEN))
        output_path = path.join(destination_directory, fileslug + '.html')
    # check the directory status
    if check_outputdir_status(destination_directory) is True:
        # write
        with open(output_path, mode='w', encoding='utf-8') as outputfile:
            outputfile.write(htmlstring)
    return fileslug


def write_result(result, args, filename=None, counter=None):
    '''Deal with result (write to STDOUT or to file)'''
    if result is None:
        return
    if args.outputdir is None:
        sys.stdout.write(result + '\n')
    else:
        destination_directory = determine_counter_dir(args.outputdir, counter)
        # check the directory status
        if check_outputdir_status(destination_directory) is True:
            # write
            destination_path = determine_filename(args, destination_directory, filename)
            with open(destination_path, mode='w', encoding='utf-8') as outputfile:
                outputfile.write(result)


def generate_filelist(inputdir):
    '''Walk the directory tree and output all file names'''
    for root, _, inputfiles in walk(inputdir):
        for fname in inputfiles:
            # filelist.append(path.join(root, fname))
            yield path.join(root, fname)


def file_processing(filename, args, counter=None):
    '''Aggregated functions to process a file in a list'''
    with open(filename, 'rb') as inputf:
        htmlstring = inputf.read()
    result = examine(htmlstring, args, url=args.URL)
    write_result(result, args, counter=counter)


def url_processing_checks(blacklist, input_urls):
    '''Filter and deduplicate input urls'''
    # control blacklist
    if blacklist:
        input_urls = [u for u in input_urls if u not in blacklist]
    # deduplicate
    input_urls = list(OrderedDict.fromkeys(input_urls))
    return input_urls


def extract_domain(url):
    '''Crude extraction of domain or host names from URLs'''
    # can be improved
    try:
        domain = re.search(r'^https?://([^/]+)', url).group(1)
    except AttributeError:
        domain = 'unknown'
    return domain


def process_result(htmlstring, args, url, counter):
    '''Extract text and metadata from a download webpage and eventually write out the result'''
    if htmlstring is not None:
        # backup option
        if args.backup_dir:
            filename = archive_html(htmlstring, args, counter)
        else:
            filename = None
        # process
        result = examine(htmlstring, args, url=url)
        write_result(result, args, filename, counter)
        # increment written file counter
        if counter is not None:
            counter += 1
    else:
        # log the error
        print('No result for URL: ' + url, file=sys.stderr)
    return counter


def single_threaded_processing(domain_dict, backoff_dict, args, sleeptime, counter):
    '''Implement a single threaded processing algorithm'''
    i = 0
    while len(domain_dict) > 0:
        domain = random.choice(list(domain_dict.keys()))
        if domain not in backoff_dict or \
        (datetime.now() - backoff_dict[domain]).total_seconds() > sleeptime:
            url = domain_dict[domain].pop()
            htmlstring = fetch_url(url)
            # register in backoff dictionary to ensure time between requests
            backoff_dict[domain] = datetime.now()
            # process result
            counter = process_result(htmlstring, args, url, counter)
            # clean registries
            if not domain_dict[domain]:
                del domain_dict[domain]
                del backoff_dict[domain]
        # safeguard
        else:
            i += 1
            if i > len(domain_dict)*3:
                LOGGER.debug('spacing request for domain name %s', domain)
                sleep(sleeptime)
                i = 0


def multi_threaded_processing(domain_dict, args, sleeptime, counter):
    '''Implement a single threaded processing algorithm'''
    i = 0
    backoff_dict = dict()
    if args.parallel is not None:
        download_threads = args.parallel
    else:
        download_threads = DOWNLOAD_THREADS
    while len(domain_dict) > 0:
        # the remaining list is too small, process it differently
        if len({x for v in domain_dict.values() for x in v}) < download_threads:
            single_threaded_processing(domain_dict, backoff_dict, args, sleeptime, counter)
            return
        # populate buffer
        bufferlist, bufferdomains = list(), set()
        while len(bufferlist) < download_threads:
            domain = random.choice(list(domain_dict.keys()))
            if domain not in backoff_dict or \
            (datetime.now() - backoff_dict[domain]).total_seconds() > sleeptime:
                bufferlist.append(domain_dict[domain].pop())
                bufferdomains.add(domain)
                backoff_dict[domain] = datetime.now()
            # safeguard
            else:
                i += 1
                if i > len(domain_dict)*3:
                    LOGGER.debug('spacing request for domain name %s', domain)
                    sleep(sleeptime)
                    i = 0
        # start several threads
        with ThreadPoolExecutor(max_workers=download_threads) as executor:
            future_to_url = {executor.submit(fetch_url, url): url for url in bufferlist}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                # register in backoff dictionary to ensure time between requests
                domain = extract_domain(url)
                backoff_dict[domain] = datetime.now()
                # handle result
                counter = process_result(future.result(), args, url, counter)
        # clean registries
        for domain in bufferdomains:
            if not domain_dict[domain]:
                del domain_dict[domain]
                del backoff_dict[domain]


def url_processing_pipeline(args, input_urls, sleeptime):
    '''Aggregated functions to show a list and download and process an input list'''
    input_urls = url_processing_checks(args.blacklist, input_urls)
    # print list without further processing
    if args.list:
        for url in input_urls:
            write_result(url, args)  # print('\n'.join(input_urls))
        return None
    # build domain-aware processing list
    domain_dict = dict()
    while len(input_urls) > 0:
        url = input_urls.pop()
        domain_name = extract_domain(url)
        if domain_name not in domain_dict:
            domain_dict[domain_name] = list()
        domain_dict[domain_name].append(url)
    # initialize file counter if necessary
    if len(input_urls) > MAX_FILES_PER_DIRECTORY:
        counter = 0
    else:
        counter = None
    if len(domain_dict) <= 5:
        backoff_dict = dict()
        single_threaded_processing(domain_dict, backoff_dict, args, sleeptime, counter)
    else:
        multi_threaded_processing(domain_dict, args, sleeptime, counter)


def file_processing_pipeline(args):
    '''Define batches for parallel file processing and perform the extraction'''
    #if not args.outputdir:
    #    sys.exit('# ERROR: please specify an output directory along with the input directory')
    # iterate through file list
    # init
    filebatch = []
    filecounter = None
    if args.parallel is not None:
        processing_cores = args.parallel
    else:
        processing_cores = FILE_PROCESSING_CORES
    # loop
    for filename in generate_filelist(args.inputdir):
        filebatch.append(filename)
        if len(filebatch) > MAX_FILES_PER_DIRECTORY:
            if filecounter is None:
                filecounter = 0
            # multiprocessing for the batch
            with Pool(processes=processing_cores) as pool:
                pool.map(partial(file_processing, args=args, counter=filecounter), filebatch)
            filecounter += len(filebatch)
            filebatch = []
    # update counter
    if filecounter is not None:
        filecounter += len(filebatch)
    # multiprocessing for the rest
    with Pool(processes=processing_cores) as pool:
        pool.map(partial(file_processing, args=args, counter=filecounter), filebatch)


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
        # put timeout signal in place
        if args.timeout is True:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(PROCESSING_TIMEOUT)
        try:
            result = extract(htmlstring, url, '0000', no_fallback=args.fast,
                             include_comments=args.nocomments, include_tables=args.notables,
                             include_formatting=args.formatting,
                             with_date=args.with_date,
                             output_format=args.output_format, tei_validation=args.validate,
                             target_language=args.target_language)
        # ugly but efficient
        except Exception as err:
            sys.stderr.write('# ERROR: ' + str(err) + '\nDetails: ' + str(sys.exc_info()[0]) + '\n')
        # deactivate
        if args.timeout is True:
            signal.alarm(0)
    return result
