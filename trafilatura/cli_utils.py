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
import traceback

from collections import defaultdict, deque, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from os import makedirs, path, walk
from time import sleep

from courlan import get_host_and_path, is_navigation_page, validate_url

from .core import extract
from .filters import content_fingerprint
from .settings import (use_config, DOWNLOAD_THREADS, FILENAME_LEN,
                       FILE_PROCESSING_CORES, MAX_FILES_PER_DIRECTORY)
from .spider import init_crawl, process_response
from .utils import fetch_url


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
    elif args.feed:
        input_urls = [args.feed]
    elif args.sitemap:
        input_urls = [args.sitemap]
    return input_urls


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


def add_to_compressed_dict(inputlist, blacklist=None, url_filter=None, inputdict=None):
    '''Filter, convert input URLs and add them to domain-aware processing dictionary'''
    # init
    if inputdict is None:
        inputdict = defaultdict(deque)
    # deduplicate while keeping order
    inputlist = list(OrderedDict.fromkeys(inputlist))
    # filter
    if blacklist:
        inputlist = [u for u in inputlist if re.sub(r'https?://', '', u) not in blacklist]
    if url_filter:
        filtered_list = []
        while inputlist:
            u = inputlist.pop()
            for f in url_filter:
                if f in u:
                    filtered_list.append(u)
                    break
        inputlist = filtered_list
    # validate and store in dict
    for url in inputlist:
        # validate URL
        if validate_url(url)[0] is False:
            continue
        # segment URL and add to domain dictionary
        try:
            hostinfo, urlpath = get_host_and_path(url)
            inputdict[hostinfo].append(urlpath)
        except ValueError:
            LOGGER.warning('Could not parse URL, discarding: %s', url)
    return inputdict


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
    output_path, filename = get_writable_path(destination_directory, '.html')
    # check the directory status
    if check_outputdir_status(destination_directory) is True:
        # write
        with open(output_path, mode='w', encoding='utf-8') as outputfile:
            outputfile.write(htmlstring)
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
    # process
    result = examine(htmlstring, args, url=url, config=config)
    write_result(result, args, orig_filename=fileslug, counter=counter, new_filename=fileslug)
    # increment written file counter
    if counter is not None and result is not None:
        counter += 1
    return counter


def draw_backoff_url(domain_dict, backoff_dict, sleeptime, i):
    '''Select a random URL from the domains pool and apply backoff rule'''
    host = random.choice(list(domain_dict))
    url = None
    if domain_dict[host]:
        # safeguard
        if host in backoff_dict and \
            (datetime.now() - backoff_dict[host]).total_seconds() < sleeptime:
            i += 1
            if i >= len(domain_dict)*3:
                LOGGER.debug('spacing request for host %s', host)
                sleep(sleeptime)
                i = 0
        # draw URL
        url = host + domain_dict[host].popleft()
        backoff_dict[host] = datetime.now()
    # clean registries
    if not domain_dict[host]:
        del domain_dict[host]
        if host in backoff_dict:
            del backoff_dict[host]
    return url, domain_dict, backoff_dict, i


def load_download_buffer(args, domain_dict, backoff_dict, config):
    '''Determine threading strategy and draw URLs respecting domain-based back-off rules.'''
    download_threads = args.parallel or DOWNLOAD_THREADS
    # the remaining list is too small, process it differently
    if len(domain_dict) < download_threads or \
       len({x for v in domain_dict.values() for x in v}) < download_threads:
        download_threads, i = 1, 3
    # populate buffer
    bufferlist = []
    while len(bufferlist) < download_threads and domain_dict:
        url, domain_dict, backoff_dict, i = draw_backoff_url(
            domain_dict, backoff_dict, config.getfloat('DEFAULT', 'SLEEP_TIME'), i
            )
        if url is not None:
            bufferlist.append(url)
    return bufferlist, download_threads, backoff_dict


def download_queue_processing(domain_dict, args, counter, config):
    '''Implement a download queue consumer, single- or multi-threaded'''
    backoff_dict, errors = dict(), []
    while domain_dict:
        bufferlist, download_threads, backoff_dict = load_download_buffer(args, domain_dict, backoff_dict, config)
        # start several threads
        with ThreadPoolExecutor(max_workers=download_threads) as executor:
            future_to_url = {executor.submit(fetch_url, url): url for url in bufferlist}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                # handle result
                if future.result() is not None:
                    counter = process_result(future.result(), args, url, counter, config)
                else:
                    LOGGER.debug('No result for URL: %s', url)
                    if args.archived is True:
                        errors.append(url)
    return errors, counter


def cli_crawler(args, n=10):
    '''Start a focused crawler which downloads a fixed number of URLs within a website
       and prints the links found in the process'''
    config = use_config(filename=args.config_file)
    counter, crawlinfo, backoff_dict = None, dict(), dict()
    # load input URLs
    domain_dict = load_input_dict(args)
    # load crawl data
    for website in domain_dict:
        homepage = website + domain_dict[website].popleft()
        crawlinfo[website] = dict()
        domain_dict[website], crawlinfo[website]['known'], crawlinfo[website]['base'], crawlinfo[website]['count'] = init_crawl(homepage, None, set(), language=args.target_language, shortform=True)
        # update info
        # TODO: register changes?
        # if base_url != website:
        # ...
    # iterate until the threshold is reached
    while domain_dict:
        bufferlist, download_threads, backoff_dict = load_download_buffer(args, domain_dict, backoff_dict, config)
        # start several threads
        # TODO: shorten code!
        with ThreadPoolExecutor(max_workers=download_threads) as executor:
            future_to_url = {executor.submit(fetch_url, url, decode=False): url for url in bufferlist}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                website, _ = get_host_and_path(url)
                crawlinfo[website]['count'] += 1
                #crawlinfo[website]['known'].add(url)
                # handle result
                if future.result() is not None:
                    domain_dict[website], crawlinfo[website]['known'], htmlstring = process_response(future.result(), domain_dict[website], crawlinfo[website]['known'], crawlinfo[website]['base'], args.target_language, shortform=True)
                    # only store content pages, not navigation
                    if not is_navigation_page(url): # + response.geturl()
                        if args.list:
                            write_result(url, args)
                        else:
                            counter = process_result(htmlstring, args, url, counter, config)
                #else:
                #    LOGGER.debug('No result for URL: %s', url)
                #    if args.archived is True:
                #        errors.append(url)
        # early exit if maximum count is reached
        if any(i >= n for i in [crawlinfo[site]['count'] for site in crawlinfo]):
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
        inputdict = dict()
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
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(config.getint('DEFAULT', 'EXTRACTION_TIMEOUT'))
        try:
            result = extract(htmlstring, url=url, no_fallback=args.fast,
                             include_comments=args.nocomments, include_tables=args.notables,
                             include_formatting=args.formatting, include_links=args.links,
                             include_images=args.images, with_metadata=args.with_metadata,
                             output_format=args.output_format, tei_validation=args.validate_tei,
                             target_language=args.target_language, deduplicate=args.deduplicate,
                             config=config) # settingsfile=args.config_file,
        # ugly but efficient
        except Exception as err:
            sys.stderr.write('ERROR: ' + str(err) + '\n' + traceback.format_exc() + '\n')
        # deactivate
        signal.alarm(0)
    return result
