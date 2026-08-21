Tutorial: Building a web corpus
===============================

.. meta::
    :description lang=en:
        This how-to explains how to easily build text collections on the command-line using tools provided by Trafilatura. All steps from web crawling to text extraction are described.


Get your system up and running
------------------------------

1.  Installation: see `dedicated page <installation.html>`_
2.  Ensure that you have installed the latest version: ``pip install -U trafilatura`` (or ``pip3``)


.. note::
    Most examples below use the `command-line <https://en.wikipedia.org/wiki/Command-line_interface>`_; Python alternatives are shown where relevant. See also: `Command-line usage <usage-cli.html#introduction>`_, `Python usage <usage-python.html>`_.


Content discovery
-----------------

In order to gather web documents it can be useful to download the portions of a website programmatically, mostly to save time and resources. Trafilatura supports three different ways to gather further links:

1. **Sitemaps**: a `sitemap <https://en.wikipedia.org/wiki/Sitemaps>`_ is a file that lists the visible URLs for a given site, following the `XML format <https://en.wikipedia.org/wiki/XML>`_. Sitemaps are particularly useful for large or complex websites where some content may not be reachable through the browsable interface.
2. **Web feeds**: a `web feed <https://en.wikipedia.org/wiki/Web_feed>`_ provides users with frequently updated content. Trafilatura supports the two common XML-based formats `Atom <https://en.wikipedia.org/wiki/Atom_(Web_standard)>`_ and `RSS <https://en.wikipedia.org/wiki/RSS>`_.
3. **Web crawling**: discovering pages by following links from page to page (see the `crawling documentation <crawls.html>`_).

A comprehensive overview of the available documents can be obtained faster and more efficiently using sitemaps and feeds than by systematically crawling. These formats are machine-readable and can reveal content that may not be reachable through the browsable interface. However, link inspection and filtering prior to download is recommended to avoid undesired content — see `link filtering`_ below.

In addition, Trafilatura supports multilingual and multinational sitemaps, for example when a site targets different languages through paths like ``/en/…`` and ``/de/…``.

.. hint::
    Sources can also consist of previously known web pages, lists of links gathered by other projects, or content from Wikipedia and social networks. See the `sources page <sources.html>`_ for details.



Gathering links
~~~~~~~~~~~~~~~


.. note::
    The following examples use the command-line interface. For more information on the **usage with Python** please refer to this blog post: `Using RSS and Atom feeds to collect web pages with Python <https://adrien.barbaresi.eu/blog/using-feeds-text-extraction-python.html>`_.


Features
^^^^^^^^

- Links can be gathered straight from the homepage (using heuristics) or using a particular URL if it is already known
- The ``--list`` option is useful to list URLs prior to processing
- Links discovery can start from an input file (``-i``) containing a list of sources which will then be processed in parallel


The following examples return lists of links. If ``--list`` is absent the pages that have been found are directly retrieved, processed, and returned in the chosen output format (default: TXT and standard output).


.. note::
    Please refer to the `CLI documentation on link discovery <usage-cli.html#link-discovery>`_ for detailed information.


In a nutshell
^^^^^^^^^^^^^

- The ``--sitemap`` option followed by a homepage or a XML sitemap will search for sitemaps links:

  ``$ trafilatura --sitemap "https://www.sitemaps.org/" --list``

- The ``--feed`` option followed by a homepage or a feed URL will search for feed links:

  ``$ trafilatura --feed "https://www.dwds.de/" --list``

- The ``--crawl`` option will try to discover internal links by hopping from page to page


For more information on sitemap use and filters for lists of links see this blog post: `Using sitemaps to crawl websites <https://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.


Multilingual sites
~~~~~~~~~~~~~~~~~~

Trafilatura handles multilingual sitemaps and supports language-based filtering during extraction. To build a corpus from a specific language on a multilingual site:

.. code-block:: bash

    # discover links — multilingual sitemaps are resolved automatically
    $ trafilatura --sitemap "https://www.example.com/" --list > all-links.txt

    # extract only German-language pages
    $ trafilatura --target-language de -i all-links.txt -o corpus-de/

In Python, use the ``target_language`` parameter to discard pages that don't match:

.. code-block:: python

    from trafilatura import fetch_url, extract

    html = fetch_url("https://www.example.com/de/artikel")
    text = extract(html, target_language="de")  # None if language doesn't match

Language detection relies on the ``py3langid`` package (installed with trafilatura) and checks both HTML metadata and the extracted text. Use `ISO 639-1 codes <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ (e.g. ``de``, ``fr``, ``zh``).


Link filtering
--------------


.. note::
    For more information see also these blog posts:

    - `Filtering links to gather texts on the web <https://adrien.barbaresi.eu/blog/link-filtering-courlan-python.html>`_
    - `An easy way to save time and resources: content-aware URL filtering <https://adrien.barbaresi.eu/blog/easy-content-aware-url-filtering.html>`_.


Filtering with coURLan
~~~~~~~~~~~~~~~~~~~~~~

It is better to examine a list of URLs for content adequacy, most notably to make download and extraction more efficient by removing unwanted and redundant content. The `courlan <https://github.com/adbar/courlan>`_ software package is installed along with ``trafilatura``. It separates the wheat from the chaff by focusing on non-spam text-rich HTML pages, and can be used on the command-line:

.. code-block:: bash

    $ courlan --inputfile raw-linklist.txt --outputfile filtered-linklist.txt


Custom filtering
~~~~~~~~~~~~~~~~

For finer control, standard Unix tools work on URL lists:

.. code-block:: bash

    grep "/article/" mylist.txt > filtered-list.txt      # keep matching URLs
    grep -v "/video/" mylist.txt > filtered-list.txt      # exclude matching URLs
    shuf myfile.txt | head -100 > random-sample.txt       # random sample

.. note::
    Trafilatura automatically deduplicates and reorders input URLs for efficient downloading — manual sorting is not required.


Process a list of links
-----------------------


Seamless download and processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two major command line arguments are necessary here:

-  ``-i`` or ``--input-file`` to select an input list to read links from
-  ``-o`` or ``--output-dir`` to define a directory to eventually store the results

An additional argument can be useful in this context:

-  ``--backup-dir`` in order to keep a copy of downloaded pages

The input list will be read sequentially, only lines beginning with a valid URL will be read, the file can thus contain other information which will be discarded.



The output directory can be created on demand, but it must be writable.

.. code-block:: bash

    # output as raw text
    $ trafilatura -i list.txt -o txtfiles/
    # output in XML format
    $ trafilatura --xml -i list.txt -o xmlfiles/
    # output in XML format, backup of HTML files
    $ trafilatura --xml -i list.txt -o xmlfiles/ --backup-dir htmlfiles/

The second and third instructions create a collection of `XML files <https://en.wikipedia.org/wiki/XML>`_ which can be edited with a basic text editor or a full-fledged text-editing software or IDE.


.. hint::
    Trafilatura automatically throttles the requests made to a given server, making it the preferred method if you do not want to worry about downloads.

    See `documentation page on downloads <downloads.html>`_ for more information.


Alternative / existing archives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Alternatively, you can download a series of web documents with generic command-line tools such as `wget <https://en.wikipedia.org/wiki/Wget>`_ and (re-)process the downloaded files at a later stage:

.. code-block:: bash

    # download if necessary
    $ wget --directory-prefix=download/ --wait 5 --input-file=mylist.txt
    # process a directory with archived HTML files
    $ trafilatura --input-dir download/ --output-dir corpus/ --xmltei --no-comments

Storing and querying results with DuckDB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have a directory of extracted files, `DuckDB <https://duckdb.org/>`_ is a convenient way to load and query them without setting up a database server. It can read a directory of JSON files directly:

.. code-block:: bash

    # extract with metadata in JSON format
    $ trafilatura -i list.txt -o jsonfiles/ --json --with-metadata

.. code-block:: sql

    -- from the command line: duckdb
    SELECT hostname, title, date, length(text) AS chars
    FROM 'jsonfiles/*.json'
    ORDER BY date DESC
    LIMIT 10;

The same query works from Python via the ``duckdb`` package (``pip install duckdb``):

.. code-block:: python

    import duckdb

    duckdb.sql("SELECT hostname, count(*) FROM 'jsonfiles/*.json' GROUP BY hostname").show()


Storing results with SQLite
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer a zero-dependency solution, Python's built-in ``sqlite3`` module works well for smaller corpora:

.. code-block:: python

    import json, sqlite3
    from pathlib import Path

    db = sqlite3.connect("corpus.db")
    db.execute("""CREATE TABLE IF NOT EXISTS docs (
        url TEXT PRIMARY KEY, hostname TEXT, title TEXT,
        date TEXT, text TEXT)""")

    for f in Path("jsonfiles").glob("*.json"):
        doc = json.loads(f.read_text())
        db.execute("INSERT OR IGNORE INTO docs VALUES (?,?,?,?,?)",
                   (doc.get("url"), doc.get("hostname"),
                    doc.get("title"), doc.get("date"), doc.get("text")))
    db.commit()

    # query
    for row in db.execute("SELECT title, date FROM docs ORDER BY date DESC LIMIT 10"):
        print(row)


.. seealso::
    `Download web pages <downloads.html>`_, `Web crawling <crawls.html>`_


