"""
This script implements a basic guided user interface (GUI).
"""

## This file is available from https://github.com/adbar/trafilatura
## under GNU GPL v3 license

import sys

from gooey import Gooey, GooeyParser

from . import __version__
from .cli import process_args
from .settings import DOWNLOAD_THREADS

DESCRIPTION = 'Web scraping tool for text discovery and extraction'

@Gooey(
    program_name='Trafilatura Graphical User Interface',
    default_size=(840, 720),
    tabbed_groups=True,
    required_cols=1,
    optional_cols=1,
    run_validators=True,
    clear_before_run=True,
    menu=[{
        'name': 'File',
        'items': [{
                'type': 'AboutDialog',
                'menuTitle': 'About',
                'name': 'Trafilatura-GUI',
                'description': DESCRIPTION,
                'version': __version__,
                'copyright': '2021',
                'website': 'https://trafilatura.readthedocs.io',
                'developer': 'Adrien Barbaresi',
                'license': 'GNU GPL v3+'
            }, {
                'type': 'Link',
                'menuTitle': 'Visit the website',
                'url': 'https://trafilatura.readthedocs.io'
            }]
        },{
        'name': 'Help',
        'items': [{
            'type': 'Link',
            'menuTitle': 'Documentation',
            'url': 'https://trafilatura.readthedocs.io/'
        }]
    }]
)
def main():
    """ Run as a command-line utility. """
    parser = GooeyParser(description=DESCRIPTION)
    group1 = parser.add_argument_group('Input', 'URLs, files or directories to process')
    group1_ex = group1.add_mutually_exclusive_group()
    group2 = parser.add_argument_group('Output', 'Determines if and how files will be written')
    group3 = parser.add_argument_group('Navigation', 'Link discovery and web crawling')
    group3_ex = group3.add_mutually_exclusive_group()
    group4 = parser.add_argument_group('Extraction', 'Customization of text and metadata processing')
    group5 = parser.add_argument_group('Format', 'Selection of the output format')
    group5_ex = group5.add_mutually_exclusive_group()

    group1_ex.add_argument("-u", "--URL",
                        type=str, help="custom URL download",
                        gooey_options={
                            'validator':{
                                'test': 'len(user_input) < 1000',
                                'message': 'input too long'
                            }
                        })
    group1_ex.add_argument("-i", "--inputfile",
                        help="name of input file for batch processing",
                        widget='FileChooser')
    group1_ex.add_argument("--inputdir",
                        help="read files from a specified directory (relative path)",
                        widget='DirChooser')

    group1.add_argument('--parallel',
                        help="specify a number of cores/threads for downloads and/or processing",
                        type=int, default=DOWNLOAD_THREADS, widget='IntegerField')
    group1.add_argument('-b', '--blacklist',
                        help="file containing unwanted URLs to discard during processing",
                        widget='FileChooser')

    group2.add_argument("--list",
                        help="display a list of URLs without downloading them",
                        action="store_true")
    group2.add_argument("-o", "--outputdir",
                        help="write results in a specified directory (relative path)",
                        widget='DirChooser')
    group2.add_argument('--backup-dir',
                        help="preserve a copy of downloaded files in a backup directory",
                        widget='DirChooser')
    group2.add_argument('--keep-dirs',
                        help="keep input directory structure and file names",
                        action="store_true")
    group2.add_argument('--hash-as-name',
                        help="use hash value as output file name instead of random default",
                        action="store_true")
    group2.add_argument('--verbose', '-v', action='count', default=0,
                        help="increase logging verbosity (up to 2)",
                        gooey_options={
                            'validator':{
                                'test': '0 <= int(user_input) <= 2',
                                'message': '0, 1 or 2'
                            }
                        })

    group3_ex.add_argument("--feed",
                        help="look for feeds and/or pass a feed URL as input",
                        nargs='?', const=True, default=None)
    group3_ex.add_argument("--sitemap",
                        help="look for sitemaps for the given website and/or enter a sitemap URL",
                        nargs='?', const=True, default=None)
    group3_ex.add_argument("--crawl",
                        help="crawl a fixed number of pages within a website starting from the given URL",
                        nargs='?', const=True, default=None)
    group3_ex.add_argument("--explore",
                        help="explore the given websites (combination of sitemap and crawl)",
                        nargs='?', const=True, default=None)
    group3.add_argument('--archived',
                        help='try to fetch URLs from the Internet Archive if downloads fail',
                        action="store_true")
    group3.add_argument('--url-filter',
                        help="only process/output URLs containing these patterns (space-separated strings)",
                        nargs='+', type=str)

    group4.add_argument("-f", "--fast",
                        help="fast (without fallback detection)",
                        action="store_true")
    group4.add_argument("--formatting",
                        help="include text formatting (bold, italic, etc.)",
                        action="store_true")
    group4.add_argument("--links",
                        help="include links along with their targets",
                        action="store_true")
    group4.add_argument("--no-comments",
                        help="don't output any comments",
                        action="store_false")
    group4.add_argument("--no-tables",
                        help="don't output any table elements",
                        action="store_false")
    group4.add_argument("--only-with-metadata",
                        help="only output those documents with title, URL and date (for formats supporting metadata)",
                        action="store_true")
    group4.add_argument("--target-language",
                        help="select a target language (ISO 639-1 codes)",
                        type=str,
                        gooey_options={
                            'validator':{
                                'test': 'len(user_input) == 2',
                                'message': '2 characters only'
                            }
                        })
    group4.add_argument("--deduplicate",
                        help="filter out duplicate documents and sections",
                        action="store_true")
    group4.add_argument("--config-file",
                        help="override standard extraction parameters with a custom config file",
                        widget='FileChooser')

    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group
    group5_ex.add_argument('-out', '--output-format',
                        help="determine output format",
                        choices=['txt', 'csv', 'json', 'xml', 'xmltei'],
                        default='txt')
    group5.add_argument("--validate-tei",
                        help="validate TEI output",
                        action="store_true")

    # https://github.com/chriskiehl/Gooey/blob/master/docs/Gooey-Options.md
    args = parser.parse_args(sys.argv[1:])
    # safety: no input
    if not args.URL and not args.inputfile and not args.inputdir:
        sys.exit('Missing input, exiting.')
    # process
    process_args(args)


if __name__ == '__main__':
    main()
