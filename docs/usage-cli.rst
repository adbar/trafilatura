On the command-line
===================

.. meta::
    :description lang=en:
        Trafilatura offers a robust CLI. Learn how to download and extract text from HTML web pages without writing code, including parallel processing and data mining capabilities.


Introduction
------------

Trafilatura offers a robust command-line interface and can be conveniently used without writing code.

For the very first steps:

- Multilingual `Introduction to the command-line interface <https://tutorial.djangogirls.org/en/intro_to_command_line/>`_
- Section of the `Introduction to Cultural Analytics & Python <https://melaniewalsh.github.io/Intro-Cultural-Analytics/01-Command-Line/01-The-Command-Line.html>`_


Quickstart
----------

All instructions for the terminal window are followed by pressing the enter key.


URLs can be used directly (``-u/--URL``):

.. code-block:: bash

    # outputs main content and comments as plain text ...
    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"

    # outputs main text with basic XML structure ...
    $ trafilatura --xml --URL "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"

    # displays help message
    $ trafilatura -h


You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    # use the contents of an already existing file
    $ cat myfile.html | trafilatura

    # alternative syntax
    $ < myfile.html trafilatura

    # use a custom download utility and pipe it to trafilatura
    $ wget -qO- "https://de.creativecommons.org/index.php/was-ist-cc/" | trafilatura


Extraction parameters
---------------------


Choice of HTML elements
~~~~~~~~~~~~~~~~~~~~~~~

Several elements can be included or discarded (see list of options below):

- Text elements
   - Comments and tables are extracted by default.
   - ``--no-comments`` and ``--no-tables`` deactivate these settings.

- Structural elements
   ``--formatting``
      Keep structural elements related to formatting (``<b>``/``<strong>``, ``<i>``/``<emph>`` etc.)
   ``--links``
      Keep link targets (in ``href="..."``), converting relative URLs to absolute where possible
   ``--images``
      Keep track of images along with their targets (``<img>`` attributes: alt, src, title)

.. note::
    Certain elements are only visible in the output if the chosen format allows it (e.g. images and XML). Including extra elements works best with conversion to XML/XML-TEI.

    The heuristics used by the main algorithm change according to the presence of certain elements in the HTML. If the output seems odd, try removing a constraint (e.g. formatting) to improve the result.


Output format
~~~~~~~~~~~~~

Output as TXT without metadata is the default, another format can be selected in two different ways:

-  ``--csv``, ``--html``, ``--json``, ``--markdown``, ``--xml`` or ``--xmltei``
-  ``--output-format`` {csv,json,html,markdown,txt,xml,xmltei}

.. hint::
    Combining TXT and CSV formats with certain structural elements (e.g. formatting or links) triggers output in Markdown format. Selecting Markdown automatically includes text formatting. Note: ``--formatting`` has no effect on JSON output.



Fast mode
~~~~~~~~~

The ``--fast`` or ``-f`` flag skips the fallback extraction cascade (readability and jusText), making extraction roughly twice as fast. Use it when speed matters more than completeness:

.. code-block:: bash

    $ trafilatura --fast -u "https://example.org"

See `how extraction works <extraction-overview.html>`_ for details on what is skipped.


Optimizing for precision and recall
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The arguments ``--precision`` or ``--recall`` can be passed to adjust the focus of the extraction process.

- ``--precision``: use when results contain too much boilerplate — comments are pruned more aggressively, link-heavy sections are discarded, and fallback stages are skipped.
- ``--recall``: use when parts of documents are missing — more elements are kept, link density thresholds are relaxed.
- If parts of the contents are still missing, see `troubleshooting <troubleshooting.html>`_.

For details on what each mode changes internally, see `how extraction works <extraction-overview.html#extraction-modes>`_.


Language identification
~~~~~~~~~~~~~~~~~~~~~~~

Passing the argument ``--target-language`` along with a 2-letter code (ISO 639-1) will trigger language filtering of the output if the identification component has been `installed <installation.html>`_ and if the target language is available.

.. note::
    Additional components are required: ``pip install trafilatura[all]``.
    This feature currently uses the `py3langid package <https://github.com/adbar/py3langid>`_ and is dependent on language availability and performance of the original model.



Metadata
~~~~~~~~

- ``--with-metadata``: extract metadata (title, author, date, etc.) and include it in the output. Off by default.
- ``--only-with-metadata``: only output documents that have all essential metadata (title, URL, date).


Deduplication
~~~~~~~~~~~~~

The ``--deduplicate`` flag activates duplicate detection across documents and within documents. Repeated segments (e.g. navigation text) are removed from the output. See `deduplication <deduplication.html>`_.


Blacklist
~~~~~~~~~

The ``-b`` / ``--blacklist`` flag accepts a file containing URLs to skip during batch processing (one URL per line).


Changing default settings
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``--config-file`` flag overrides extraction settings with a custom configuration file. See `documentation page on settings <settings.html>`_.



Process files locally
---------------------

In case web pages have already been downloaded and stored, it is possible to process single files or directories as a whole. It can be especially helpful to separate download and extraction to circumvent blocking mechanisms, either by scrambling IPs used to access the pages or by using web browser automation software to bypass issues related to cookies and paywalls.

Trafilatura will work as well provided web pages (HTML documents) are used as input. The following command line arguments are relevant:

-  ``--input-dir`` to select a directory to read files from
-  ``-o`` or ``--output-dir`` to define a directory to eventually store the results
-  ``--keep-dirs`` to mirror the input directory structure in the output (requires ``-o/--output-dir``)


.. note::
    In case no directory is selected, results are printed to standard output (*STDOUT*, e.g. in the terminal window).



Process a list of links
-----------------------

.. note::
    Beware that there should be a tacit scraping etiquette and that a server may block you after the download of a certain number of pages from the same website/domain in a short period of time.

    In addition, some websites may block the ``requests`` `user-agent <https://en.wikipedia.org/wiki/User_agent>`_. Thus, *trafilatura* waits a few seconds per default between requests.

    For more information see the `page on downloads <downloads.html>`_.


The following command line arguments are relevant:

-  ``-i`` or ``--input-file`` to select an input list to read links from.

   This option allows for bulk download and processing of a list of URLs from a file listing one link per line. The input list will be read sequentially, only lines beginning with a valid URL will be read, the file can thus contain other information which will be discarded.

-  ``-o`` or ``--output-dir`` to define a directory to eventually store the results.

   The output directory can be created on demand, but it must be writable.


.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles/		# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles/	# output in XML format
    $ trafilatura --parallel 4 -i list.txt -o txtfiles/	# use 4 threads


.. hint::
    Backup of HTML sources can be useful for archival and further processing:
    
    ``$ trafilatura --input-file links.txt --output-dir converted/ --backup-dir html-sources/ --xml``


Internet Archive
~~~~~~~~~~~~~~~~

Using the option ``--archived`` will trigger queries to the `Internet Archive <https://web.archive.org/>`_ for web pages which could not be downloaded.

There is a fair chance to find archived versions for larger websites, whereas pages of lesser-known websites may not have been preserved there. The retrieval process is slow as it depends on a single web portal only, it is best performed for a relatively small number of URLs.


Link discovery
--------------

Link discovery can be performed over `web feeds <https://en.wikipedia.org/wiki/Web_feed>`_ (Atom and RSS, mostly for fresh content), `sitemaps <https://en.wikipedia.org/wiki/Sitemaps>`_ for exhaustivity (all potential pages as listed by the owners), and discovery by web crawling (i.e. by following the internal links, more experimental).

Both the homepage and a particular page can be used as input depending on the selected options (e.g. a sitemap or feed URL).

The ``--list`` option is useful to list URLs prior to processing. This option can be combined with an input file (``-i``) containing a list of sources which will then be processed in parallel.

For more information please refer to the `tutorial on content discovery <tutorial0.html#content-discovery>`_.

Feeds
~~~~~

.. code-block:: bash

    # automatically detecting feeds starting from the homepage
    $ trafilatura --feed "https://www.dwds.de/" --list

    # already known feed
    $ trafilatura --feed "https://www.dwds.de/api/feed/themenglossar/Corona" --list

    # processing a list in parallel
    $ trafilatura -i mylist.txt --feed --list


.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/NW2ISdOx08M?start=406" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Youtube tutorial: `Extracting links from web feeds <https://www.youtube.com/watch?v=NW2ISdOx08M&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci&index=2&t=398s>`_


Sitemaps
~~~~~~~~

.. code-block:: bash

    # run link discovery through a sitemap for sitemaps.org and store the resulting links in a file
    $ trafilatura --sitemap "https://www.sitemaps.org/" --list > mylinks.txt

    # using an already known sitemap URL
    $ trafilatura --sitemap "https://www.sitemaps.org/sitemap.xml" --list

    # targeting webpages in German
    $ trafilatura --sitemap "https://www.sitemaps.org/" --list --target-language "de"


For more information on sitemap use and filters for lists of links see this blog post: `Using sitemaps to crawl websites <https://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.


.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/uWUyhxciTOs?start=330" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Youtube tutorial: `Listing all website contents with sitemaps <https://www.youtube.com/watch?v=uWUyhxciTOs&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci&index=3&t=330s>`_


Web crawling
~~~~~~~~~~~~

Selecting the ``--crawl`` option automatically looks for pages by following a fixed number of internal links on the website, starting from the given URL and returning a list of links.

See the `page on web crawling <crawls.html>`_ for more information.


Explore and probe
~~~~~~~~~~~~~~~~~

- ``--explore``: combines sitemap and crawl discovery for broader coverage.
- ``--probe``: probes pages for extractable content, works best with ``--target-language`` to find pages in a specific language.


URL inspection prior to download and processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: bash

    $ trafilatura --sitemap "https://www.sitemaps.org/" --list --url-filter "https://www.sitemaps.org/de"
    $ trafilatura --sitemap "https://www.sitemaps.org/" --list --url-filter "protocol"

Using a subpart of the site also acts like a filter, for example ``--sitemap "https://www.sitemaps.org/de/"``.

For more information on sitemap use and filters for lists of links see this blog post: `Using sitemaps to crawl websites <https://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_ and this `tutorial on link filtering <tutorial0.html#link-filtering>`_.


Deprecations
------------

See the `deprecations and migration <deprecations.html>`_ page for a full list of deprecated CLI arguments and migration instructions.



Further information
-------------------


.. hint::
    See also `how to modify the default settings <settings.html>`_.


For all usage instructions see ``trafilatura -h``:

.. program-output:: trafilatura -h

.. seealso::
    `Settings and customization <settings.html>`_, `With Python <usage-python.html>`_

