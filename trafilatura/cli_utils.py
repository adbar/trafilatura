"""
Functions dedicated to command-line processing.
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license


import gzip
import logging
import random
import re
import string
import sys
import traceback

from functools import partial
from multiprocessing import Pool
from os import makedirs, path, walk
from time import sleep

from courlan import get_host_and_path, validate_url, UrlStore

from trafilatura import spider

from .core import extract
from .downloads import add_to_compressed_dict, buffered_downloads, load_download_buffer
from .filters import content_fingerprint
from .utils import uniquify_list
from .settings import (use_config, FILENAME_LEN,
                       FILE_PROCESSING_CORES, MAX_FILES_PER_DIRECTORY)


LOGGER = logging.getLogger(__name__)

random.seed(345)  # make generated file names reproducible
CHAR_CLASS = string.ascii_letters + string.digits


def load_input_urls(args):
    '''Read list of URLs to process or derive one from command-line arguments'''
    if args.input_file:
        input_urls = []
        try:
            # optional: errors='strict', buffering=1
            with open(args.input_file, mode='r', encoding='utf-8') as inputfile:
                for line in inputfile:
                    url_match = re.match(r'https?://[^\s]+', line)
                    if url_match:
                        input_urls.append(url_match[0])

        except UnicodeDecodeError:
            sys.exit('ERROR: system, file type or buffer encoding')
    elif args.crawl:
        input_urls = [args.crawl]
    elif args.explore:
        input_urls = [args.explore]
    elif args.feed:
        input_urls = [args.feed]
    elif args.sitemap:
        input_urls = [args.sitemap]
    # uniq URLs while preserving order (important)
    return uniquify_list(input_urls)


def load_blacklist(filename):
    '''Read list of unwanted URLs'''
    blacklist = set()
    with open(filename, mode='r', encoding='utf-8') as inputfh:
        for line in inputfh:
            url = line.strip()
            if validate_url(url)[0] is True:
                blacklist.add(re.sub(r'^https?://', '', url))
    return blacklist


def load_input_dict(args):
    '''Read input list of URLs to process and
       build a domain-aware dictionary'''
    inputlist = load_input_urls(args)
    # deduplicate, filter and and convert to dict
    return add_to_compressed_dict(inputlist, args.blacklist) # args.filter


def check_outputdir_status(directory):
    '''Check if the output directory is within reach and writable'''
    # check the directory status
    if not path.exists(directory) or not path.isdir(directory):
        try:
            makedirs(directory, exist_ok=True)
        except OSError:
            # maybe the directory has already been created
            #sleep(0.25)
            #if not path.exists(directory) or not path.isdir(directory):
            sys.stderr.write('ERROR: Destination directory cannot be created: ' + directory + '\n')
            # raise OSError()
            return False
    return True


def determine_counter_dir(dirname, counter):
    '''Return a destination directory based on a file counter'''
    if counter is not None:
        counter_dir = str(int(counter/MAX_FILES_PER_DIRECTORY) + 1)
    else:
        counter_dir = ''
    return path.join(dirname, counter_dir)


def get_writable_path(destdir, extension):
    '''Find a writable path and return it along with its random file name'''
    filename = ''.join(random.choice(CHAR_CLASS) for _ in range(FILENAME_LEN))
    output_path = path.join(destdir, filename + extension)
    while path.exists(output_path):
        filename = ''.join(random.choice(CHAR_CLASS) for _ in range(FILENAME_LEN))
        output_path = path.join(destdir, filename + extension)
    return output_path, filename


def determine_output_path(args, orig_filename, content, counter=None, new_filename=None):
    '''Pick a directory based on selected options and a file name based on output type'''
    # determine extension
    extension = '.txt'
    if args.output_format in ('xml', 'xmltei'):
        extension = '.xml'
    elif args.output_format == 'csv':
        extension = '.csv'
    elif args.output_format == 'json':
        extension = '.json'
    # use cryptographic hash on file contents to define name
    if args.hash_as_name is True:
        new_filename = content_fingerprint(content)[:27].replace('/', '-')
    # determine directory
    if args.keep_dirs is True:
        # strip directory
        orig_directory = re.sub(r'[^/]+$', '', orig_filename)
        destination_directory = path.join(args.output_dir, orig_directory)
        # strip extension
        filename = re.sub(r'\.[a-z]{2,5}$', '', orig_filename)
        output_path = path.join(args.output_dir, filename + extension)
    else:
        destination_directory = determine_counter_dir(args.output_dir, counter)
        # determine file slug
        if new_filename is None:
            output_path, _ = get_writable_path(destination_directory, extension)
        else:
            output_path = path.join(destination_directory, new_filename + extension)
    return output_path, destination_directory


def archive_html(htmlstring, args, counter=None):
    '''Write a copy of raw HTML in backup directory'''
    destination_directory = determine_counter_dir(args.backup_dir, counter)
    output_path, filename = get_writable_path(destination_directory, '.html.gz')
    # check the directory status
    if check_outputdir_status(destination_directory) is True:
        # write
        with gzip.open(output_path, 'wb') as outputfile:
            outputfile.write(htmlstring.encode('utf-8'))
    return filename


def write_result(result, args, orig_filename=None, counter=None, new_filename=None):
    '''Deal with result (write to STDOUT or to file)'''
    if result is None:
        return
    if args.output_dir is None:
        sys.stdout.write(result + '\n')
    else:
        destination_path, destination_directory = determine_output_path(args, orig_filename, result, counter, new_filename)
        # check the directory status
        if check_outputdir_status(destination_directory) is True:
            with open(destination_path, mode='w', encoding='utf-8') as outputfile:
                outputfile.write(result)


def generate_filelist(inputdir):
    '''Walk the directory tree and output all file names'''
    for root, _, inputfiles in walk(inputdir):
        for fname in inputfiles:
            yield path.join(root, fname)


def file_processing(filename, args, counter=None, config=None):
    '''Aggregated functions to process a file in a list'''
    with open(filename, 'rb') as inputf:
        htmlstring = inputf.read()
    result = examine(htmlstring, args, url=args.URL, config=config)
    write_result(result, args, filename, counter, new_filename=None)


def process_result(htmlstring, args, url, counter, config):
    '''Extract text and metadata from a download webpage and eventually write out the result'''
    # backup option
    fileslug = archive_html(htmlstring, args, counter) if args.backup_dir else None
    # suggested: fileslug = archive_html(htmlstring, args, counter) if args.backup_dir else None
    # process
    result = examine(htmlstring, args, url=url, config=config)
    write_result(result, args, orig_filename=fileslug, counter=counter, new_filename=fileslug)
    # increment written file counter
    if counter is not None and result is not None:
        counter += 1
    return counter


def download_queue_processing(url_store, args, counter, config):
    '''Implement a download queue consumer, single- or multi-threaded'''
    sleep_time = config.getfloat('DEFAULT', 'SLEEP_TIME')
    errors = []
    while url_store.done is False:
        bufferlist, download_threads, url_store = load_download_buffer(url_store, sleep_time, threads=args.parallel)
        # process downloads
        for url, result in buffered_downloads(bufferlist, download_threads):
            # handle result
            if result is not None:
                counter = process_result(result, args, url, counter, config)
            else:
                LOGGER.warning('No result for URL: %s', url)
                errors.append(url)
    return errors, counter


def cli_crawler(args, n=30, url_store=None):
    '''Start a focused crawler which downloads a fixed number of URLs within a website
       and prints the links found in the process'''
    config = use_config(filename=args.config_file)
    sleep_time = config.getfloat('DEFAULT', 'SLEEP_TIME')
    # counter = None
    # load input URLs
    if url_store is None:
        spider.URL_STORE.add_urls(load_input_urls(args))
    else:
        spider.URL_STORE = url_store
    # load crawl data
    for hostname in spider.URL_STORE.get_known_domains():
        startpage = hostname + spider.URL_STORE.urldict[hostname].tuples[0].urlpath  # URL_STORE.get_url(hostname)
        # base_url, i, known_num, rules, is_on
        _ = spider.init_crawl(startpage, None, set(), language=args.target_language)
        # update info
        # TODO: register changes?
        # if base_url != hostname:
        # ...
    # iterate until the threshold is reached
    while spider.URL_STORE.done is False:
        bufferlist, download_threads, spider.URL_STORE = load_download_buffer(spider.URL_STORE, sleep_time, threads=args.parallel)
        # start several threads
        for url, result in buffered_downloads(bufferlist, download_threads, decode=False):
            website, _ = get_host_and_path(url)
            # handle result
            if result is not None:
                spider.process_response(result, website, args.target_language, rules=spider.URL_STORE.get_rules(website))
                # just in case a crawl delay is specified in robots.txt
                sleep(spider.get_crawl_delay(spider.URL_STORE.get_rules(website)))
        # early exit if maximum count is reached
        if any(spider.URL_STORE.urldict[d].count >= n for d in spider.URL_STORE.urldict):
            break
    # print results
    print('\n'.join(u for u in spider.URL_STORE.dump_urls()))
    #return todo, known_links


def url_processing_pipeline(args, url_store):
    '''Aggregated functions to show a list and download and process an input list'''
    # print list without further processing
    if args.list:
        for domain in url_store.urldict:
            # write_result('\n'.join(url_store.find_unvisited_urls(domain)), args)
            print('\n'.join(url_store.find_unvisited_urls(domain)))
        return False  # sys.exit(0)
    # parse config
    config = use_config(filename=args.config_file)
    # initialize file counter if necessary
    counter, i = None, 0
    for hostname in url_store.urldict:
        i += len(url_store.find_known_urls(hostname))
        if i > MAX_FILES_PER_DIRECTORY:
            counter = 0
            break
    # download strategy
    errors, counter = download_queue_processing(url_store, args, counter, config)
    LOGGER.debug('%s URLs could not be found', len(errors))
    # option to retry
    if args.archived is True:
        url_store = UrlStore()
        url_store.add_urls(['https://web.archive.org/web/20/' + e for e in errors])
        if len(url_store.find_known_urls('https://web.archive.org')) > 0:
            archived_errors, _ = download_queue_processing(url_store, args, counter, config)
            LOGGER.debug('%s archived URLs out of %s could not be found', len(archived_errors), len(errors))
            # pass information along if URLs are missing
            return bool(archived_errors)
    # pass information along if URLs are missing
    return bool(errors)


def file_processing_pipeline(args):
    '''Define batches for parallel file processing and perform the extraction'''
    filebatch, filecounter = [], None
    processing_cores = args.parallel or FILE_PROCESSING_CORES
    config = use_config(filename=args.config_file)
    # loop: iterate through file list
    for filename in generate_filelist(args.input_dir):
        filebatch.append(filename)
        if len(filebatch) > MAX_FILES_PER_DIRECTORY:
            if filecounter is None:
                filecounter = 0
            # multiprocessing for the batch
            with Pool(processes=processing_cores) as pool:
                pool.map(partial(file_processing, args=args, counter=filecounter, config=config), filebatch)
            filecounter += len(filebatch)
            filebatch = []
    # update counter
    if filecounter is not None:
        filecounter += len(filebatch)
    # multiprocessing for the rest
    with Pool(processes=processing_cores) as pool:
        pool.map(partial(file_processing, args=args, counter=filecounter, config=config), filebatch)


def examine(htmlstring, args, url=None, config=None):
    """Generic safeguards and triggers"""
    result = None
    if config is None:
        config = use_config(filename=args.config_file)
    # safety check
    if htmlstring is None:
        sys.stderr.write('ERROR: empty document\n')
    elif len(htmlstring) > config.getint('DEFAULT', 'MAX_FILE_SIZE'):
        sys.stderr.write('ERROR: file too large\n')
    elif len(htmlstring) < config.getint('DEFAULT', 'MIN_FILE_SIZE'):
        sys.stderr.write('ERROR: file too small\n')
    # proceed
    else:
        try:
            result = extract(htmlstring, url=url, no_fallback=args.fast,
                             include_comments=args.no_comments, include_tables=args.no_tables,
                             include_formatting=args.formatting, include_links=args.links,
                             include_images=args.images, only_with_metadata=args.only_with_metadata,
                             output_format=args.output_format, tei_validation=args.validate_tei,
                             target_language=args.target_language, deduplicate=args.deduplicate,
                             favor_precision=args.precision, favor_recall=args.recall, config=config)
            # settingsfile=args.config_file,
        # ugly but efficient
        except Exception as err:
            sys.stderr.write(f'ERROR: {str(err)}' + '\n' + traceback.format_exc() + '\n')
    return result
