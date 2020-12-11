Usage on the command-line
=========================


Introduction
------------

Trafilatura includes a `command-line interface <https://en.wikipedia.org/wiki/Command-line_interface>`_ and can be conveniently used without writing code.

For the very first steps please refer to this nice `step-by-step introduction <https://tutorial.djangogirls.org/en/intro_to_command_line/>`_ and for general instructions see:

- `Comment Prompt <https://www.lifewire.com/how-to-open-command-prompt-2618089>`_ (tutorial for Windows systems)
- `How to use the Terminal command line in macOS <https://macpaw.com/how-to/use-terminal-on-mac>`_
- or `An introduction to the Linux Terminal <https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal>`_

As well as these compendia:

- `Commands toolbox <http://cb.vu/unixtoolbox.xhtml>`_
- `Basic Bash Command Line Tips You Should Know <https://www.freecodecamp.org/news/basic-linux-commands-bash-tips-you-should-know/>`_


Quickstart
----------

URLs can be used directly (``-u/--URL``):

.. code-block:: bash

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...
    $ trafilatura --xml --URL "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    $ # outputs main text with basic XML structure ...
    $ trafilatura -h
    # displays help message

You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    $ cat myfile.html | trafilatura # use the contents of an already existing file
    $ wget -qO- "https://de.creativecommons.org/index.php/was-ist-cc/" | trafilatura # use a custom download


Output format
-------------

Output as TXT without metadata is the default, another format can be selected in two different ways:

-  ``--csv``, ``--json``, ``--xml`` or ``--xmltei``
-  ``-out`` or ``--output-format`` {txt,csv,json,xml,xmltei}


Process a list of links
-----------------------

The ``-i/--inputfile`` option allows for bulk download and processing of a list of URLs from a file listing one link per line. The input list will be read sequentially, only lines beginning with a valid URL will be read, the file can thus contain other information which will be discarded.

Beware that there should be a tacit scraping etiquette and that a server may block you after the download of a certain number of pages from the same website/domain in a short period of time. In addition, some website may block the ``requests`` `user-agent <https://en.wikipedia.org/wiki/User_agent>`_. Thus, *trafilatura* waits a few seconds per default between requests.

Two major command line arguments are necessary here:

-  ``-i`` or ``--inputfile`` to select an input list to read links from
-  ``-o`` or ``--outputdir`` to define a directory to eventually store the results

The output directory can be created on demand, but it must be writable.

.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles	# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles	# output in XML format


Backup of HTML sources can be useful for archival and further processing:

.. code-block:: bash

    $ trafilatura --inputfile links.txt --outputdir converted/ --backup-dir html-sources/ --xml


Link discovery
--------------

Link discovery can be performed over `web feeds <https://en.wikipedia.org/wiki/Web_feed>`_ (Atom and RSS) or `sitemaps <https://en.wikipedia.org/wiki/Sitemaps>`_.

Both homepages and particular sitemaps or feed URLs can be used as input.

The ``--list`` option is useful to list URLs prior to processing.

This option can be combined with an input file (``-i``) containing a list of sources which will then be processed in parallel.

For more information please refer to the `tutorial on content discovery <tutorial0.html#content-discovery>`_.

Feeds
^^^^^

-  ``trafilatura --feed "https://www.dwds.de/" --list``
-  ``trafilatura --feed "https://www.dwds.de/api/feed/themenglossar/Corona" --list``

Sitemaps
^^^^^^^^

-  ``trafilatura --sitemap "https://www.sitemaps.org/sitemap.xml" --list``
-  ``trafilatura --sitemap "https://www.sitemaps.org/" --list``


URL inspection prior to download and processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ trafilatura --sitemap "https://www.sitemaps.org/" --list > mylist.txt
    $ trafilatura -i mylist.txt -o myfiles/

For more information see `tutorial on link filtering <tutorial0.html#link-filtering>`_.


Further information
-------------------

For all usage instructions see ``trafilatura -h``:

.. code-block:: bash

    usage: trafilatura [-h] [-v] [-vv] [-i INPUTFILE] [--inputdir INPUTDIR]
                   [-o OUTPUTDIR] [-u URL] [--feed [FEED]]
                   [--sitemap [SITEMAP]] [--list] [-b BLACKLIST]
                   [--backup-dir BACKUP_DIR] [--timeout] [--parallel PARALLEL]
                   [--keep-dirs] [--hash-as-name]
                   [-out {txt,csv,json,xml,xmltei}] [--csv] [--json] [--xml]
                   [--xmltei] [--validate] [-f] [--formatting] [--nocomments]
                   [--notables] [--with-metadata]
                   [--target-language TARGET_LANGUAGE] [--deduplicate]


Command-line interface for Trafilatura

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -vv, --very-verbose   maximum output verbosity

I/O:
  Input and output options affecting processing

  -i, --inputfile INPUTFILE
                        name of input file for batch processing
  --inputdir INPUTDIR   read files from a specified directory (relative path)
  -o, --outputdir OUTPUTDIR
                        write results in a specified directory (relative path)
  -u, --URL URL         custom URL download
  --feed FEED           look for feeds and/or pass a feed URL as input
  --sitemap SITEMAP     look for sitemaps URLs for the given website
  --list                return a list of URLs without downloading them
  -b, --blacklist BLACKLIST
                        name of file containing already processed or unwanted
                        URLs to discard during batch processing
  --backup-dir BACKUP_DIR
                        Preserve a copy of downloaded files in a backup
                        directory
  --timeout             Use timeout for file conversion to prevent bugs
  --parallel PARALLEL   Specify a number of cores/threads for parallel
                        downloads and/or processing
  --keep-dirs           Keep input directory structure and file names
  --hash-as-name        Use file content hash as output file name (for
                        deduplication) instead of random default

Format:
  Selection of the output format

  -out, --output-format {txt,csv,json,xml,xmltei}
                        determine output format

  --csv                 CSV output
  --json                JSON output
  --xml                 XML output
  --xmltei              XML TEI output
  --validate            validate TEI output

Extraction:
  Customization of text and metadata extraction

  -f, --fast            fast (without fallback detection)
  --formatting          include text formatting (bold, italic, etc.)
  --nocomments          don't output any comments
  --notables            don't output any table elements
  --with-metadata       only output those documents with necessary metadata:
                        title, URL and date (CSV and XML formats)
  --target-language TARGET_LANGUAGE
                        select a target language (ISO 639-1 codes)
  --deduplicate         Filter out duplicate documents and sections
