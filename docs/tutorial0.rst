Tutorial: Gathering a custom web corpus
=======================================


Get your system up and running
------------------------------

-  Installation: see `dedicated page <installation.html>`_
-  Ensure that you have installed the latest version: ``pip install -U trafilatura``

The following consists of `command-line instructions <https://en.wikipedia.org/wiki/Command-line_interface>`_. For an introduction see the `page on command-line usage <usage-cli.html#introduction>`_.


Content discovery
-----------------

Sources used by Trafilatura can consist of previously known or listed web pages. Currently, functions to discover content within a website are available. Other methods include sifting through Wikipedia, social networks, or using lists of links gathered by other projects.


Finding subpages within a website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to gather web documents it can be useful to download the portions of a website programmatically, mostly to save time and resources. The retrieval and download of documents within a website is often called *web crawling* or *web spidering*. Web crawlers usually discover pages from links within the site and from other sites. Trafilatura supports two different ways to gather further links `web feeds <https://en.wikipedia.org/wiki/Web_feed>`_ (Atom and RSS) or `sitemaps <https://en.wikipedia.org/wiki/Sitemaps>`_. As a result, a comprehensive overview of the available documents can be obtained faster and more efficiently than by systematically extracting and following links within a website.

The formats supported are all machine-readable rather than human-readable they can also be used to automatically transfer information from one website to another without any human intervention. However, link inspection and filtering prior to systematic download is recommended to avoid undesired content or overstreching computing resources.

In addition, *trafilatura* includes support for multilingual and multinational sitemaps. For example, a site can target English language users through links like ``http://www.example.com/en/…`` and German language users through ``http://www.example.com/de/…``.


Sitemaps
~~~~~~~~

A `sitemap <https://en.wikipedia.org/wiki/Sitemaps>`_ is a file that lists the visible or whitelisted URLs for a given site, the main goal being to reveal where machines can look for content. Web crawlers usually discover pages from links within the site and from other sites, following a series of rules and protocols. Sitemaps supplement this data to allow crawlers that support Sitemaps to pick up all URLs in the Sitemap and learn about those URLs using the associated metadata.

The `sitemaps protocol <https://en.wikipedia.org/wiki/Sitemaps>`_ primarily allows webmasters to inform search engines about pages on their sites that are available for crawling. Crawlers can use it to pick up all URLs in the sitemap and learn about those URLs using the associated metadata. Sitemaps follow the `XML format <https://en.wikipedia.org/wiki/XML>`_, so each sitemap is or should be a valid XML file.

Sitemaps are particularly useful by large or complex websites since they are made so that machines can more intelligently crawl the site. This particularly true if there is a chance to overlook some of the new or recently updated content, for example because some areas of the website are not available through the browsable interface, or when websites have a huge number of pages that are isolated or not well linked together.


Feeds
~~~~~

A `web feed <https://en.wikipedia.org/wiki/Web_feed>`_  (or news feed) is a data format used for providing users with frequently updated content. This process is also called web syndication, meaning a form of syndication in which content is made available from one website to other sites.

Most commonly, feeds are made available to provide either summaries or full renditions of a website's recently added content. The term may also describe other kinds of content licensing for reuse. The kinds of content delivered by a web feed are typically HTML (webpage content) or links to webpages and other kinds of digital media. Many news websites, weblogs, schools, and podcasters operate web feeds. The `feed icon <https://en.wikipedia.org/wiki/File:Feed-icon.svg>`_ is commonly used to indicate that a web feed is available. 

*Trafilatura* supports XML-based feeds with the two common formats `Atom <https://en.wikipedia.org/wiki/Atom_(Web_standard)>`_ and `RSS <https://en.wikipedia.org/wiki/RSS>`_.


Gathering links
~~~~~~~~~~~~~~~

Features
^^^^^^^^

- Links can be gathered straight from the homepage (using heuristics) or using a particular URL if it is already known
- The ``--list`` option is useful to list URLs prior to processing
- Links discovery can start from an input file (``-i``) containing a list of sources which will then be processed in parallel

For usage with Python see `core functions documentation <corefunctions.html#link-discovery>`_.

The following examples return lists of links. If ``--list`` is absent the pages that have been found are directly retrieved, processed, and returned in the chosen output format (default: TXT and standard output).


Sitemaps
^^^^^^^^

.. code-block:: bash

    # run link discovery through a sitemap for sitemaps.org and store the resulting links in a file
    $ trafilatura --sitemap "https://www.sitemaps.org/" --list > mylinks.txt
    # using an already known sitemap URL
    $ trafilatura --sitemap "https://www.sitemaps.org/sitemap.xml" --list
    # targeting webpages in German
    $ trafilatura --sitemap "https://www.sitemaps.org/" --list --target-language "de"


Feeds
^^^^^

.. code-block:: bash

    # looking for feeds
    $ trafilatura --feed "https://www.dwds.de/" --list
    # already known feed
    $ trafilatura --feed "https://www.dwds.de/api/feed/themenglossar/Corona" --list
    # processing a list in parallel
    $ trafilatura -i mylist.txt --feed --list


Link filtering
--------------

Filtering with coURLan
~~~~~~~~~~~~~~~~~~~~~~

It is better to examine a list of URLs for content adequacy, most notably to make download and extraction more efficient by removing unwanted and redundant content. The `courlan <https://github.com/adbar/courlan>`_ software package is installed along with ``trafilatura``. It separates the wheat from the chaff by focusing on non-spam text-rich HTML pages, and can be used on the command-line:

``courlan --inputfile raw-linklist.txt --outputfile filtered-linklist.txt``


Custom filtering
~~~~~~~~~~~~~~~~

URL lists can be filtered manually or with `grep <https://en.wikipedia.org/wiki/Grep>`_, a command-line utility to search text data which operates on line-level and returns either matching or non-matching lines.

-  Matching relevant links: ``grep "/article/" mylist.txt > filtered-list.txt``
-  Exclusion criteria: ``grep -v "/video/" mylist.txt > filtered-list.txt``

For further filters in grep, see `grep tutorial <http://www.panix.com/~elflord/unix/grep.html>`_.

Other relevant utilities include `sort <https://en.wikipedia.org/wiki/Sort_(Unix)>`_ and `shuf <https://en.wikipedia.org/wiki/Shuf>`_:

.. code-block:: bash

    # sort the links and make sure they are unique
    sort -u myfile.txt > myfile-sorted.txt
    # alternatives to shuffle the URLs
    sort -R myfile.txt > myfile-random.txt
    shuf myfile.txt > myfile-random.txt

To draw a random sample of a list of URLs `head <https://en.wikipedia.org/wiki/Head_(Unix)>`_ or `tail <https://en.wikipedia.org/wiki/Tail_(Unix)>`_ come in handy after a random sorting: ``shuf myfile.txt | head -100 > myfile-random-sample.txt``

*Trafilatura* automatically sorts the input list to optimize the download order and make sure the input URLs are unique; it is not mandatory to perform these steps by yourself.


Process a list of links
-----------------------

Two major command line arguments are necessary here:

-  ``-i`` or ``--inputfile`` to select an input list to read links from
-  ``-o`` or ``--outputdir`` to define a directory to eventually store the results

The input list will be read sequentially, only lines beginning with a valid URL will be read, the file can thus contain other information which will be discarded.

The output directory can be created on demand, but it must be writable.

.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles	# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles	# output in XML format

The second instruction creates a collection of `XML files <https://en.wikipedia.org/wiki/XML>`_ which can be edited with a basic text editor or a full-fledged text-editing software or IDE such as the `Atom editor <https://atom.io/>`_.

Alternatively, you can download a series of web documents with generic command-line tools such as `wget <https://en.wikipedia.org/wiki/Wget>`_ and (re-)process the downloaded files at a later stage:

.. code-block:: bash

    $ wget --directory-prefix=download/ --wait 5 --input-file=mylist.txt
    $ trafilatura --inputdir download/ --outputdir corpus/ --xmltei --nocomments

