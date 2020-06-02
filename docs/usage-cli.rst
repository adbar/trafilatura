Usage on the command-line
=========================


Trafilatura includes a `command-line interface <https://en.wikipedia.org/wiki/Command-line_interface>`_ and can be conveniently used without writing code.

For general instructions see

- `Comment Prompt <https://www.lifewire.com/how-to-open-command-prompt-2618089>`_ (tutorial for Windows systems),
- `How to use the Terminal command line in macOS <https://macpaw.com/how-to/use-terminal-on-mac>`_,
- or `An introduction to the Linux Terminal <https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal>`_

as well as these compendia:

- `commands toolbox <http://cb.vu/unixtoolbox.xhtml>`_
- `Basic Bash Command Line Tips You Should Know <https://www.freecodecamp.org/news/basic-linux-commands-bash-tips-you-should-know/>`_



Quickstart
----------

.. code-block:: bash

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...
    $ trafilatura --xml --nocomments -u "URL..."
    # outputs main content without comments as XML ...
    $ trafilatura -h
    # displays help message


Usage
-----

URLs can be used directly (``-u/--URL``):

.. code-block:: bash

    $ trafilatura -u https://de.creativecommons.org/index.php/was-ist-cc/
    $ # outputs main content in plain text format ...
    $ trafilatura --xml --URL "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    $ # outputs main text with basic XML structure ...

You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    $ cat myfile.html | trafilatura # use the contents of an already existing file
    $ wget -qO- "https://de.creativecommons.org/index.php/was-ist-cc/" | trafilatura # use a custom download

The ``-i/--inputfile`` option allows for bulk download and processing of a list of URLs from a file listing one link per line. Beware that there should be a tacit scraping etiquette and that a server may block you after the download of a certain number of pages from the same website/domain in a short period of time. In addition, some website may block the requests `user-agent <https://en.wikipedia.org/wiki/User_agent>`_. Thus, *trafilatura* waits a few seconds per default between requests.

For all usage instructions see ``trafilatura -h``:

``usage: trafilatura [-h] [-v] [-i INPUTFILE] [--inputdir INPUTDIR] [-o OUTPUTDIR] [-u URL] [--feed FEED] [--list] [-b BLACKLIST] [--backup-dir BACKUP_DIR] [-out {txt,csv,xml,xmltei}] [--csv] [--xml] [--xmltei] [--validate] [-f] [--formatting] [--nocomments] [--notables]``

Command-line interface for Trafilatura

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity

I/O:
  Input and output options affecting processing

  -i INPUTFILE, --inputfile INPUTFILE
                        name of input file for batch processing
  --inputdir INPUTDIR   read files from a specified directory (relative path)
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        write results in a specified directory (relative path)
  -u URL, --URL URL     custom URL download
  --feed FEED           pass a feed URL as input
  --list                return a list of URLs without downloading them
  -b BLACKLIST, --blacklist BLACKLIST
                        name of file containing already processed or unwanted
                        URLs to discard during batch processing
  --backup-dir BACKUP_DIR
                        Preserve a copy of downloaded files in a backup
                        directory

Format:
  Selection of the output format

  -out {txt,csv,xml,xmltei}, --output-format {txt,csv,xml,xmltei}
                        determine output format
  --csv                 CSV output
  --xml                 XML output
  --xmltei              XML TEI output
  --validate            validate TEI output

Extraction:
  Customization of text and metadata extraction

  -f, --fast            fast (without fallback detection)
  --formatting          include text formatting (bold, italic, etc.)
  --nocomments          don't output any comments
  --notables            don't output any table elements
