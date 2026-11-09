"""
Functions dedicated to command-line processing.
"""

import argparse
import gzip
import logging
import os
import random
import re
import string
import sys
import traceback
from base64 import urlsafe_b64encode
from collections.abc import Callable, Generator, Iterable, Iterator
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime
from functools import partial
from hashlib import blake2b
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

# optional progress bar for batch processing
try:
    from tqdm import tqdm
    from tqdm.contrib.logging import logging_redirect_tqdm

    HAS_TQDM = True
except ImportError:  # pragma: no cover
    HAS_TQDM = False

from courlan import UrlStore, get_base_url  # validate_url

from trafilatura import spider

from .baseline import html2txt
from .core import extract
from .deduplication import generate_bow_hash
from .downloads import (
    add_to_compressed_dict,
    buffered_downloads,
    buffered_response_downloads,
    filter_blacklist,
    load_download_buffer,
)
from .feeds import find_feed_urls
from .meta import reset_caches
from .settings import (
    FILENAME_LEN,
    MAX_FILES_PER_DIRECTORY,
    Extractor,
    args_to_extractor,
)
from .sitemaps import sitemap_search
from .utils import (
    LANGID_FLAG,
    Response,
    detectable_languages,
    is_acceptable_length,
    language_classifier,
    make_chunks,
)

LOGGER = logging.getLogger(__name__)

_FILENAME_RANDOM = random.Random(345)  # reproducible names without changing caller RNG state
CHAR_CLASS = string.ascii_letters + string.digits

STRIP_EXTENSION = re.compile(r"\.[a-z]{2,5}$")

CLEAN_XML = re.compile(r"<[^<]+?>")

EXTENSION_MAPPING = {
    "csv": ".csv",
    "html": ".html",
    "json": ".json",
    "xml": ".xml",
    "xmltei": ".xml",
}


def load_input_urls(args: argparse.Namespace) -> list[str]:
    "Read list of URLs to process or derive one from command-line arguments."
    input_urls: list[str] = []

    if args.input_file:
        try:
            with Path(args.input_file).open(encoding="utf-8-sig") as inputfile:
                # cut at the first space or tab, the rest is a comment
                input_urls.extend(url for line in inputfile if (url := line.strip().replace("\t", " ").partition(" ")[0]))
        except UnicodeDecodeError:
            sys.exit("ERROR: system, file type or buffer encoding")
    elif args.URL:
        input_urls = [args.URL]

    if not input_urls:
        LOGGER.warning("No input provided")

    # uniq URLs while preserving order (important)
    return list(dict.fromkeys(input_urls))


def load_blacklist(filename: str) -> set[str]:
    "Read list of unwanted URLs."
    with Path(filename).open(encoding="utf-8-sig") as inputfh:
        return {line.strip() for line in inputfh}


def load_input_dict(args: argparse.Namespace) -> UrlStore:
    "Read input list of URLs to process and build a domain-aware dictionary."
    inputlist = load_input_urls(args)
    # deduplicate, filter and convert to dict
    url_store = add_to_compressed_dict(
        inputlist,
        blacklist=args.blacklist,
        compression=(args.sitemap and not args.list),
        url_filter=args.url_filter,
        verbose=args.verbose,
    )
    if inputlist and url_store.total_url_number() == 0:
        LOGGER.warning("No input URL left after validation, blacklist and URL filter")
    return url_store


def check_outputdir_status(directory: str) -> bool:
    "Check if the output directory is within reach and writable."
    # no is_dir precheck: unlike os.path.isdir, Path.is_dir raises on an unreadable parent
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
    except OSError:
        sys.stderr.write("ERROR: Destination directory cannot be created: " + directory + "\n")
        return False
    return True


def determine_counter_dir(dirname: str, c: int) -> str:
    "Return a destination directory based on a file counter."
    if c < 0:
        return dirname
    # os.path.join, not Path: pathlib rewrites the separators the caller passed in
    return os.path.join(dirname, str(int(c / MAX_FILES_PER_DIRECTORY) + 1))


def get_writable_path(destdir: str, extension: str) -> tuple[str, str]:
    "Find a writable path and return it along with its random file name."
    while True:
        filename = "".join(_FILENAME_RANDOM.choice(CHAR_CLASS) for _ in range(FILENAME_LEN))
        output_path = os.path.join(destdir, filename + extension)
        # not Path.exists: it raises on an unreadable parent, and the dir status is checked later
        if not os.path.exists(output_path):  # noqa: PTH110
            return output_path, filename


def generate_hash_filename(content: str) -> str:
    """Create a filename-safe string by hashing the given content
    after deleting potential XML tags."""
    return urlsafe_b64encode(generate_bow_hash(CLEAN_XML.sub("", content), 12)).decode()


def generate_url_filename(url: str) -> str:
    "Create a readable file name from a URL, with a hash suffix to distinguish URLs."
    parts = urlsplit(url)
    prefix = re.sub(r"[^\w.-]+", "_", f"{parts.hostname}{unquote(parts.path)}", flags=re.ASCII)[:120].strip("._-")
    return f"{prefix}-{blake2b(url.encode(), digest_size=8).hexdigest()}"


def determine_output_path(
    args: argparse.Namespace,
    orig_filename: str,
    content: str,
    counter: int = -1,
    new_filename: str | None = None,
) -> tuple[str, str]:
    "Pick a directory based on selected options and a file name based on output type."
    # determine extension, TXT by default
    extension = EXTENSION_MAPPING.get(args.output_format, ".txt")

    if args.keep_dirs:
        relative_filename = Path(os.path.relpath(orig_filename, args.input_dir))
        destination_dir = str(Path(args.output_dir) / relative_filename.parent)
        filename = STRIP_EXTENSION.sub("", relative_filename.name)
    else:
        destination_dir = determine_counter_dir(args.output_dir, counter)
        # use cryptographic hash on file contents to define name
        filename = new_filename or generate_hash_filename(content)

    output_path = os.path.join(destination_dir, filename + extension)
    return output_path, destination_dir


def archive_html(htmlstring: str, args: argparse.Namespace, counter: int = -1, new_filename: str | None = None) -> str:
    "Write a copy of raw HTML in backup directory."
    destination_directory = determine_counter_dir(args.backup_dir, counter)
    if new_filename:
        filename = new_filename
        output_path = os.path.join(destination_directory, filename + ".html.gz")
    else:
        output_path, filename = get_writable_path(destination_directory, ".html.gz")
    if check_outputdir_status(destination_directory):
        with gzip.open(output_path, "wb") as outputfile:
            outputfile.write(htmlstring.encode("utf-8"))
    return filename


def absolute_path(path: str) -> str:
    "Resolve a path through its filesystem aliases to compare destinations with inputs."
    return os.path.normcase(os.path.realpath(path))


def write_result(
    result: str | None,
    args: argparse.Namespace,
    orig_filename: str = "",
    counter: int = -1,
    new_filename: str | None = None,
) -> None:
    """Deal with result (write to STDOUT or to file)"""
    if result is None:
        return
    if args.output_dir is None:
        if args.output_format == "csv":
            # CSV rows end with \r\n, newline translation would add a \r on Windows
            if isinstance(sys.stdout, TextIOWrapper):
                sys.stdout.reconfigure(newline="")
            sys.stdout.write(result)
        else:
            sys.stdout.write(result + "\n")
    else:
        destination_path, destination_dir = determine_output_path(args, orig_filename, result, counter, new_filename)
        # a kept input file maps onto itself when the output format matches its extension (#1038)
        if orig_filename and absolute_path(destination_path) == absolute_path(orig_filename):
            LOGGER.error("Skipping %s: the output path would overwrite the input file", orig_filename)
            return
        if check_outputdir_status(destination_dir):
            newline = "" if args.output_format == "csv" else None
            with Path(destination_path).open(mode="w", encoding="utf-8", newline=newline) as outputfile:
                outputfile.write(result)


def generate_filelist(
    inputdir: str, onerror: Callable[[OSError], None] | None = None, exclude_dirs: Iterable[str | None] = ()
) -> Generator[str, None, None]:
    "Walk the directory tree and report errors without skipping readable paths."
    excluded = {absolute_path(path) for path in exclude_dirs if path}

    def handle_error(error: OSError) -> None:
        LOGGER.error("Cannot read input directory %s", error)
        if onerror is not None:
            onerror(error)

    # os.walk does not follow directory symlinks, unlike rglob on Python < 3.13
    for root, directories, files in os.walk(inputdir, onerror=handle_error):
        if excluded:
            directories[:] = [name for name in directories if absolute_path(os.path.join(root, name)) not in excluded]
        for filename in files:
            yield os.path.join(root, filename)


def file_processing(filename: str, args: argparse.Namespace, counter: int, options: Extractor) -> None:
    "Aggregated functions to process a file in a list."
    options.source = filename

    with Path(filename).open("rb") as inputf:
        htmlstring = inputf.read()

    file_stat = Path(filename).stat()
    ref_timestamp = min(file_stat.st_ctime, file_stat.st_mtime)
    options.date_params["max_date"] = datetime.fromtimestamp(ref_timestamp).astimezone().strftime("%Y-%m-%d")

    result = examine(htmlstring, args, options=options)
    write_result(result, args, filename, counter)


def process_result(htmlstring: str, args: argparse.Namespace, counter: int, options: Extractor, url: str | None = None) -> int:
    "Extract text and metadata from a download webpage and eventually write out the result."
    fileslug = generate_url_filename(url) if args.name_from_url and url else ""
    # backup option
    if args.backup_dir:
        fileslug = archive_html(htmlstring, args, counter, new_filename=fileslug)
    # process
    result = examine(htmlstring, args, options=options, url=url)
    write_result(result, args, counter=counter, new_filename=fileslug)
    # increment written file counter
    if counter >= 0 and result:
        counter += 1
    return counter


@contextmanager
def _progress_bar(args: argparse.Namespace, total: int | None, unit: str) -> Iterator[Any]:
    "Yield a tqdm progress bar if one was requested, else None."
    if not getattr(args, "progress", False):
        yield None
        return
    # print log messages above the bar instead of through it
    with logging_redirect_tqdm(), tqdm(total=total, unit=unit) as bar:
        yield bar


def download_queue_processing(
    url_store: UrlStore,
    args: argparse.Namespace,
    counter: int,
    options: Extractor,
    progress: Any = None,
) -> tuple[list[str], int]:
    "Implement a download queue consumer, single- or multi-threaded."
    errors = []
    sleep_time = options.config.getfloat("DEFAULT", "SLEEP_TIME")

    while not url_store.done:
        bufferlist, url_store = load_download_buffer(url_store, sleep_time)
        # process downloads
        for url, result in buffered_downloads(bufferlist, args.parallel, options=options):
            # handle result
            if result and isinstance(result, str):
                counter = process_result(result, args, counter, options, url)
            else:
                LOGGER.warning("No result for URL: %s", url)
                errors.append(url)
            if progress is not None:
                progress.update(1)
    return errors, counter


def cli_discovery(args: argparse.Namespace) -> int:
    "Group CLI functions dedicated to URL discovery."
    url_store = load_input_dict(args)
    input_urls = url_store.dump_urls()
    if not input_urls:
        return 1
    # only process the discovered URLs
    url_store.reset()

    options = args_to_extractor(args)
    func = partial(
        find_feed_urls if args.feed else sitemap_search,
        target_lang=args.target_language,
        external=options.config.getboolean("DEFAULT", "EXTERNAL_URLS"),
        sleep_time=options.config.getfloat("DEFAULT", "SLEEP_TIME"),
        config=options.config,
    )
    no_links = []

    # link discovery and storage
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = {executor.submit(func, url): url for url in input_urls}
        # process results from the parallel threads and add them
        # to the compressed URL dictionary for further processing
        for future in as_completed(futures):
            # all links blacklisted = no links
            links = filter_blacklist(future.result() or [], args.blacklist)
            if not links:
                no_links.append(futures[future])
                continue
            add_to_compressed_dict(links, url_store=url_store)
            # empty buffer in order to spare memory
            if args.list and len(url_store.get_known_domains()) >= args.parallel:
                url_store.print_unvisited_urls()
                url_store.reset()
                reset_caches()

    # process the (rest of the) links found
    exit_code = url_processing_pipeline(args, url_store)

    # the crawler takes over the seeds without links, keep the worse exit code
    if args.explore and no_links:
        return max(exit_code, cli_crawler(args, url_store=add_to_compressed_dict(no_links), options=options))

    # missing links are not download failures
    return max(exit_code, int(bool(no_links)))


def cli_crawler(
    args: argparse.Namespace,
    n: int = 30,
    url_store: UrlStore | None = None,
    options: Extractor | None = None,
) -> int:
    """Start a focused crawler which downloads a fixed number of URLs within a website
    and prints the links found in the process."""
    options = options or args_to_extractor(args)
    sleep_time = options.config.getfloat("DEFAULT", "SLEEP_TIME")
    param_dict = {}
    starts = []

    # load input URLs
    spider.URL_STORE = load_input_dict(args) if url_store is None else url_store

    # load crawl data
    for hostname in spider.URL_STORE.get_known_domains():
        startpage = spider.URL_STORE.get_url(hostname, as_visited=False)
        if startpage:
            params = spider.init_crawl(startpage, lang=args.target_language, config=options.config, blacklist=args.blacklist)
            # key by the crawl base: it may differ from hostname after a https upgrade,
            # but the store may still hold URLs under the original base
            param_dict[params.base] = params
            param_dict.setdefault(get_base_url(startpage), params)
            starts.append(params)

    # iterate until the threshold is reached
    while not spider.URL_STORE.done:
        bufferlist, spider.URL_STORE = load_download_buffer(spider.URL_STORE, sleep_time)
        for url, result in buffered_response_downloads(bufferlist, args.parallel, options=options):
            if result and isinstance(result, Response):
                # not necessarily registered, e.g. after a cross-host homepage redirect
                crawl_params = param_dict.get(get_base_url(url))
                if crawl_params is not None:
                    spider.process_response(result, crawl_params)
                else:
                    LOGGER.warning("no crawl parameters for %s", url)
        # early exit if maximum count is reached
        if any(c >= n for c in spider.URL_STORE.get_all_counts()):
            break

    print("\n".join(spider.URL_STORE.dump_urls()))
    if not starts:
        return 1
    # start pages that could not be fetched
    errors = [p.base for p in starts if p.i == 0]
    return _define_exit_code(errors, len(starts))


def probe_homepage(args: argparse.Namespace) -> int:
    "Probe websites for extractable content and print the fitting ones."
    input_urls = load_input_dict(args).dump_urls()
    if not input_urls:
        return 1
    options = args_to_extractor(args)
    available = detectable_languages()

    errors: list[str] = []
    for url, result in buffered_downloads(input_urls, args.parallel, options=options):
        if result is None:
            errors.append(url)
        else:
            result = html2txt(result)
            if result and len(result) > options.min_extracted_size and any(c.isalpha() for c in result):
                if (
                    not LANGID_FLAG
                    or not args.target_language
                    or (available is not None and args.target_language not in available)
                    or language_classifier(result, "") == args.target_language
                ):
                    print(url, flush=True)
    return _define_exit_code(errors, len(input_urls))


def _define_exit_code(errors: list[str], total: int) -> int:
    """Compute exit code based on the number of errors:
    0 if there are no errors, 126 if there are too many, 1 otherwise."""
    ratio = len(errors) / total if total > 0 else 0

    if ratio > 0.99:
        return 126
    if errors:
        return 1
    return 0


def url_processing_pipeline(args: argparse.Namespace, url_store: UrlStore) -> int:
    "Aggregated functions to show a list and download and process an input list."
    if args.list:
        url_store.print_unvisited_urls()
        return 0

    options = args_to_extractor(args)
    url_count = url_store.total_url_number()
    counter = 0 if url_count > MAX_FILES_PER_DIRECTORY else -1

    # download strategy
    with _progress_bar(args, url_count, "URL") as progress:
        errors, counter = download_queue_processing(url_store, args, counter, options, progress)
    LOGGER.debug("%s / %s URLs could not be found", len(errors), url_count)

    if args.archived and errors:
        url_store = UrlStore()
        url_store.add_urls(["https://web.archive.org/web/20/" + e for e in errors])
        with _progress_bar(args, url_store.total_url_number(), "URL") as progress:
            archived_errors, _ = download_queue_processing(url_store, args, counter, options, progress)
        LOGGER.debug("%s archived URLs out of %s could not be found", len(archived_errors), len(errors))
        # pass information along if URLs are missing
        return _define_exit_code(archived_errors, url_count)

    return _define_exit_code(errors, url_count)


def _process_file(filename: str, args: argparse.Namespace, counter: int, options: Extractor) -> str | None:
    "Report file failures without discarding the rest of a worker chunk."
    try:
        file_processing(filename, args, counter, options)
    except Exception as error:
        return f"{filename} {error}"
    return None


def _init_worker_logging(level: int | None) -> None:
    "Configure fresh worker logging when the parent has configured it."
    if level is not None:
        logging.basicConfig(stream=sys.stderr, level=level)


def file_processing_pipeline(args: argparse.Namespace) -> int:
    "Define batches for parallel file processing and perform the extraction."
    filecounter = -1
    exit_code = 0
    options = args_to_extractor(args)
    walk_errors: list[OSError] = []

    filelist: Iterable[str] = generate_filelist(
        args.input_dir, onerror=walk_errors.append, exclude_dirs=(args.output_dir, args.backup_dir)
    )
    total = None
    if getattr(args, "progress", False):
        # walk once and keep the paths, so the bar total matches the files processed
        files = list(filelist)
        total, filelist = len(files), files

    root_logger = logging.getLogger()
    log_level = root_logger.level if root_logger.handlers else None
    # max_tasks_per_child available in Python >= 3.11
    with (
        ProcessPoolExecutor(max_workers=args.parallel, initializer=_init_worker_logging, initargs=(log_level,)) as executor,
        _progress_bar(args, total, "file") as progress,
    ):
        # chunk input: https://github.com/python/cpython/issues/74028
        for filebatch in make_chunks(filelist, MAX_FILES_PER_DIRECTORY):
            if filecounter < 0 and len(filebatch) >= MAX_FILES_PER_DIRECTORY:
                filecounter = 0
            worker = partial(_process_file, args=args, counter=filecounter, options=options)
            for error in executor.map(worker, filebatch, chunksize=10):
                if error is not None:
                    LOGGER.error("Cannot process file %s", error)
                    exit_code = 1
                if progress is not None:
                    progress.update(1)
            # update counter
            if filecounter >= 0:
                filecounter += len(filebatch)

    return 1 if walk_errors else exit_code


def examine(
    htmlstring: str | bytes | None,
    args: argparse.Namespace,
    *,
    options: Extractor | None = None,
    url: str | None = None,
) -> str | None:
    "Generic safeguards and triggers around extraction function."
    result = None
    if not options:
        options = args_to_extractor(args)
    # safety check
    if htmlstring is None:
        sys.stderr.write("ERROR: empty document\n")
    elif not is_acceptable_length(len(htmlstring), options, url):
        sys.stderr.write("ERROR: file size\n")
    # proceed
    else:
        try:
            result = extract(htmlstring, url=url, options=options)
        # ugly but efficient
        except Exception as err:
            sys.stderr.write(f"ERROR: {err!s}\n{traceback.format_exc()}\n")
    return result
