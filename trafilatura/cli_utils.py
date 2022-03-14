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

from collections import deque
from functools import partial
from multiprocessing import Pool
from os import makedirs, path, walk

# SIGALRM isn't present on Windows, detect it
try:
    from signal import signal, alarm, SIGALRM
    HAS_SIGNAL = True
except ImportError:
    HAS_SIGNAL = False

from time import sleep

from courlan import get_host_and_path, is_navigation_page, validate_url

from .core import extract
from .downloads import add_to_compressed_dict, buffered_downloads, load_download_buffer
from .filters import content_fingerprint
from .utils import uniquify_list
from .settings import (use_config, FILENAME_LEN,
                       FILE_PROCESSING_CORES, MAX_FILES_PER_DIRECTORY)
from .spider import get_crawl_delay, init_crawl, process_response


LOGGER = logging.getLogger(__name__)
random.seed(345)  # make generated file names reproducible
CHAR_CLASS = string.ascii_letters + string.digits


# try signal https://stackoverflow.com/questions/492519/timeout-on-a-function-call
def handler(signum, frame):
    '''Raise a timeout exception to handle rare malicious files'''
    raise Exception('unusual file processing time, aborting')


def load_input_urls(args):
    '''Read list of URLs to process or derive one from command-line arguments'''
    if args.inputfile:
        input_urls = []
        try:
            # optional: errors='strict', buffering=1
            with open(args.inputfile, mode='r', encoding='utf-8') as inputfile:
                for line in inputfile:
                    url_match = re.match(r'https?://[^\s]+', line)
                    if url_match:
                        input_urls.append(url_match.group(0))
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
        destination_directory = path.join(args.outputdir, orig_directory)
        # strip extension
        filename = re.sub(r'\.[a-z]{2,5}$', '', orig_filename)
        output_path = path.join(args.outputdir, filename + extension)
    else:
        destination_directory = determine_counter_dir(args.outputdir, counter)
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
    if args.outputdir is None:
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
    if args.backup_dir:
        fileslug = archive_html(htmlstring, args, counter)
    else:
        fileslug = None
    # suggested: fileslug = archive_html(htmlstring, args, counter) if args.backup_dir else None
    # process
    result = examine(htmlstring, args, url=url, config=config)
    write_result(result, args, orig_filename=fileslug, counter=counter, new_filename=fileslug)
    # increment written file counter
    if counter is not None and result is not None:
        counter += 1
    return counter


def download_queue_processing(domain_dict, args, counter, config):
    '''Implement a download queue consumer, single- or multi-threaded'''
    sleep_time = config.getfloat('DEFAULT', 'SLEEP_TIME')
    backoff_dict, errors = {}, []
    while domain_dict:
        bufferlist, download_threads, domain_dict, backoff_dict = load_download_buffer(domain_dict, backoff_dict, sleep_time, threads=args.parallel)
        # process downloads
        for url, result in buffered_downloads(bufferlist, download_threads):
            # handle result
            if result is not None and result != '':
                counter = process_result(result, args, url, counter, config)
            else:
                LOGGER.debug('No result for URL: %s', url)
                if args.archived is True:
                    errors.append(url)
    return errors, counter


def cli_crawler(args, n=30, domain_dict=None):
    '''Start a focused crawler which downloads a fixed number of URLs within a website
       and prints the links found in the process'''
    config = use_config(filename=args.config_file)
    sleep_time = config.getfloat('DEFAULT', 'SLEEP_TIME')
    counter, crawlinfo, backoff_dict = None, {}, {}
    # load input URLs
    if domain_dict is None:
        domain_dict = load_input_dict(args)
    # load crawl data
    for website in domain_dict:
        homepage = website + domain_dict[website].popleft()
        crawlinfo[website] = {}
        domain_dict[website], crawlinfo[website]['known'], crawlinfo[website]['base'], crawlinfo[website]['count'], crawlinfo[website]['rules'] = init_crawl(homepage, None, set(), language=args.target_language, shortform=True)
        # update info
        # TODO: register changes?
        # if base_url != website:
        # ...
    # iterate until the threshold is reached
    while domain_dict:
        bufferlist, download_threads, domain_dict, backoff_dict = load_download_buffer(domain_dict, backoff_dict, sleep_time, threads=args.parallel)
        # start several threads
        for url, result in buffered_downloads(bufferlist, download_threads, decode=False):
            website, _ = get_host_and_path(url)
            crawlinfo[website]['count'] += 1
            # handle result
            if result is not None and result != '':
                domain_dict[website], crawlinfo[website]['known'], htmlstring = process_response(result, domain_dict[website], crawlinfo[website]['known'], crawlinfo[website]['base'], args.target_language, shortform=True, rules=crawlinfo[website]['rules'])
                # only store content pages, not navigation
                if not is_navigation_page(url):  # + response.url
                    if args.list:
                        write_result(url, args)
                    else:
                        counter = process_result(htmlstring, args, url, counter, config)
                # just in case a crawl delay is specified in robots.txt
                sleep(get_crawl_delay(crawlinfo[website]['rules']))
                #else:
                #    LOGGER.debug('No result for URL: %s', url)
                #    if args.archived is True:
                #        errors.append(url)
        # early exit if maximum count is reached
        if any(i >= n for i in [dictvalue['count'] for _, dictvalue in crawlinfo.items()]):
            break
    # print results
    for website in sorted(domain_dict):
        for urlpath in sorted(domain_dict[website]):
            sys.stdout.write(website + urlpath +'\n')
    #return todo, known_links


def url_processing_pipeline(args, inputdict):
    '''Aggregated functions to show a list and download and process an input list'''
    # print list without further processing
    if args.list:
        for hostname in inputdict:
            for urlpath in inputdict[hostname]:
                write_result(hostname + urlpath, args)  # print('\n'.join(input_urls))
        return # sys.exit(0)
    # parse config
    config = use_config(filename=args.config_file)
    # initialize file counter if necessary
    counter, i = None, 0
    for hostname in inputdict:
        i += len(inputdict[hostname])
        if i > MAX_FILES_PER_DIRECTORY:
            counter = 0
            break
    # download strategy
    errors, counter = download_queue_processing(inputdict, args, counter, config)
    LOGGER.debug('%s URLs could not be found', len(errors))
    # option to retry
    if args.archived is True:
        inputdict = {}
        inputdict['https://web.archive.org'] = deque(['/web/20/' + e for e in errors])
        if len(inputdict['https://web.archive.org']) > 0:
            archived_errors, _ = download_queue_processing(inputdict, args, counter, config)
            LOGGER.debug('%s archived URLs out of %s could not be found', len(archived_errors), len(errors))


def file_processing_pipeline(args):
    '''Define batches for parallel file processing and perform the extraction'''
    filebatch, filecounter = [], None
    processing_cores = args.parallel or FILE_PROCESSING_CORES
    config = use_config(filename=args.config_file)
    # loop: iterate through file list
    for filename in generate_filelist(args.inputdir):
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
        # put timeout signal in place
        if HAS_SIGNAL is True:
            signal(SIGALRM, handler)
            alarm(config.getint('DEFAULT', 'EXTRACTION_TIMEOUT'))
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
            sys.stderr.write('ERROR: ' + str(err) + '\n' + traceback.format_exc() + '\n')
        # deactivate
        if HAS_SIGNAL is True:
            alarm(0)
    return result
