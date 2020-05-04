Usage
=====


With Python
-----------

See here for a `beginner's guide <https://wiki.python.org/moin/BeginnersGuide>`_, a `Python Tutorial <https://docs.python.org/3/tutorial/index.html>`_, and `the Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_.

.. code-block:: python

    >>> import trafilatura
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> downloaded is None # assuming the download was successful
    False
    >>> result = trafilatura.extract(downloaded) # trafilatura.process_record is deprecated but works
    >>> print(result)
    # newlines preserved, TXT output ...
    >>> result = trafilatura.extract(downloaded, xml_output=True)
    >>> print(result)
    # some formatting preserved in basic XML structure ...

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

The inclusion of tables and comments can be deactivated at a function call. The use of a fallback algorithm (currently `jusText <https://github.com/miso-belica/jusText>`_) can also be bypassed in *fast* mode:

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, include_comments=False) # no comments in output
    >>> result = trafilatura.extract(downloaded, include_tables=False) # skip tables examination
    >>> result = trafilatura.extract(downloaded, no_fallback=True) # skip justext algorithm used as fallback

This values combined probably provide the fastest execution times:

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)

The input can consist of a previously parsed tree (i.e. a *lxml.html* object), which is then handled seamlessly:

.. code-block:: python

    >>> from lxml import html
    >>> mytree = html.fromstring('<html><body><article><p>Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></article></body></html>')
    >>> trafilatura.extract(mytree)
    'Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n'

Experimental feature: the target language can also be set using 2-letter codes (`ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_), there will be no output if the detected language of the result does not match and no such filtering if the identification component has not been installed (see above for installation instructions).

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, url, target_language='de')

All currently available options, along with their default values:

.. code-block:: python

    >>> trafilatura.extract(downloaded, url=None, record_id='0001', no_fallback=False, include_comments=True, csv_output=False, xml_output=False, tei_output=False, tei_validation=False, target_language=None, include_tables=True, include_formatting=False, date_extraction_params=None)

For further configuration see the variables in ``settings.py`` and re-compile the package locally.


Date extraction
^^^^^^^^^^^^^^^

Among metadata extraction, dates are handled by an external module: `htmldate <https://github.com/adbar/htmldate>`_. `Custom parameters <https://htmldate.readthedocs.io/en/latest/corefunctions.html#handling-date-extraction>`_ can be passed through the extraction function or through the ``extract_metadata`` function in ``trafilatura.metadata``, most notably: ``extensive_search`` (boolean), to activate pattern-based opportunistic text search,  ``original_date`` (boolean) to look for the original publication date, ``outputformat`` (string), to provide a custom datetime format, and ``max_date`` (string), to set the latest acceptable date manually (YYYY-MM-DD format).


On the command-line
-------------------


A command-line interface is included, for general instructions see `Comment Prompt <https://www.lifewire.com/how-to-open-command-prompt-2618089>`_ (tutorial for Windows systems), `How to use the Terminal command line in macOS <https://macpaw.com/how-to/use-terminal-on-mac>`_, or `An introduction to the Linux Terminal <https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal>`_.

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

``usage: trafilatura [-h] [-f] [--formatting] [-i INPUTFILE] [-i OUTPUTDIR] [--nocomments] [--notables] [--xml] [--xmltei] [-u URL] [-v]``

optional arguments:
  -h, --help         show this help message and exit
  -f, --fast         fast (without fallback detection)
  --formatting          include text formatting (bold, italic, etc.)
  -i INPUTFILE, --inputfile INPUTFILE
                     name of input file for batch processing
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                     write results in a specified directory (relative path)
  --nocomments       don't output any comments
  --notables         don't output any table elements
  --csv              CSV output
  --xml              XML output
  --xmltei           XML TEI output
  --validate         validate TEI output
  -u URL, --URL URL  custom URL download
  -v, --verbose      increase output verbosity
