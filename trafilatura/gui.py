"""
This script implements a basic guided user interface (GUI).
"""

import sys

from gooey import Gooey, GooeyParser

from . import __version__
from .cli import add_args, process_args


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
                'license': "Apache 2.0"
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
    "Run as a Gooey/GUI utility."
    parser = GooeyParser(description=DESCRIPTION)
    parser = add_args(parser)

    # https://github.com/chriskiehl/Gooey/blob/master/docs/Gooey-Options.md
    args = parser.parse_args(sys.argv[1:])
    # safety: no input
    if not args.URL and not args.inputfile and not args.inputdir:
        sys.exit("Missing input, exiting.")
    # process
    process_args(args)


if __name__ == '__main__':
    main()
