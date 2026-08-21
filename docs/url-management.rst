URL management
==============

.. meta::
    :description lang=en:
        This page shows how to filter and refine a list of URLs, with Python and on the command-line,
        using the functions provided by the included courlan package.


It is essential to filter out unwanted or noisy URLs to ensure that only relevant and useful URLs are processed. This page shows how to do it with Python and on the command-line, using the functions provided by the ``courlan`` package which is included with Trafilatura.


Filtering input URLs is essential to avoid unwanted URLs, such as those with unnecessary tags (e.g. ``.../tags/abc``) or internationalized rubrics (e.g. ``.../en/....``). It is recommended to filter URLs before retrieving all pages and especially before performing massive downloads. This can help you save time and resources by only processing the URLs that are relevant to your needs.


.. hint::
    See the `Courlan documentation <https://courlan.readthedocs.io/en/latest/>`_ for more examples.


Extracting links from a page
-----------------------------

Before a list of URLs can be filtered, it usually has to be gathered from a page in the first place. The ``extract_links()`` function pulls candidate links out of a HTML document and applies the same heuristics used elsewhere in ``courlan`` (language, navigation pages, etc.):

.. code-block:: python

    >>> from trafilatura import fetch_url
    >>> from courlan import extract_links

    >>> url = 'https://www.sitemaps.org/'
    >>> html = fetch_url(url)
    >>> extract_links(html, url=url, language='en')
    {'https://www.sitemaps.org/protocol.php', 'https://www.sitemaps.org/faq.php', ...}

For more granular control, ``filter_links()`` additionally consults ``robots.txt`` rules and returns two separate lists, one to keep and one to discard:

.. code-block:: python

    >>> from courlan import filter_links
    >>> good_links, discarded_links = filter_links(html, url)

This is the same mechanism used internally for `web crawling <crawls.html>`_.


Filtering a list of URLs
------------------------

With Python
~~~~~~~~~~~

The  function ``check_url()`` returns a URL and a domain name if everything is fine. This function is particularly useful for filtering out URLs with specific characteristics, removing unnecessary query parameters, and targeting web pages in specific languages.

.. doctest::

    # load the function from the included courlan package
    >>> from courlan import check_url

    # checking a URL returns None or a tuple (cleaned url, hostname)
    >>> check_url('https://github.com/adbar/courlan')
    ('https://github.com/adbar/courlan', 'github.com')

    # noisy query parameters can be removed
    >>> check_url('https://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.org', strict=True)
    ('https://httpbin.org/redirect-to', 'httpbin.org')

    # optional argument targeting webpages in a given language; returns None
    # if the URL doesn't match (here /en/ doesn't match the German filter)
    >>> my_url = 'https://www.un.org/en/about-us'
    >>> check_url(my_url, language='en')
    ('https://www.un.org/en/about-us', 'un.org')
    >>> check_url(my_url, language='de')


The ``courlan`` package provides several other helper functions dedicated to URL cleaning and validation which can help removing unnecessary parts and converting URLs to a conform and standard representation.


Cleaning URLs removes unnecessary characters and normalizes them to a standard format, preventing errors and inconsistencies that can arise from malformed or duplicate URLs.

.. doctest::

    >>> from courlan import clean_url

    >>> clean_url('HTTPS://WWW.DWDS.DE:80/')
    'https://www.dwds.de:80'


Validation checks whether a URL conforms to the expected format, preventing errors further down the line:

.. doctest::

    >>> from courlan import validate_url

    >>> validate_url('http://1234')
    (False, None)
    >>> validate_url('http://www.example.org/')
    (True, SplitResult(scheme='http', netloc='www.example.org', path='/', query='', fragment=''))


Filtering by pattern and diagnosing rejections
++++++++++++++++++++++++++++++++++++++++++++++

To filter an existing list of links by a substring pattern (e.g. after discovering them with ``extract_links()`` or a sitemap), use ``filter_urls()``:

.. doctest::

    >>> from courlan import filter_urls

    >>> links = ['https://www.sitemaps.org/de/', 'https://www.sitemaps.org/terms.html']
    >>> filter_urls(links, 'de')
    ['https://www.sitemaps.org/de/']

.. note::
    This is what the CLI's ``--url-filter`` flag would do on discovered links; on the command-line the flag instead filters the *seed* URLs given via ``-i``/``--input-file``, see the `command-line documentation <usage-cli.html#url-inspection-prior-to-download-and-processing>`_.

Two additional helpers can explain why a given URL might be rejected during filtering:

.. doctest::

    >>> from courlan import is_navigation_page, is_not_crawlable

    >>> is_navigation_page('https://www.example.org/category/news/')
    True
    >>> is_not_crawlable('https://www.example.org/login')
    True


On the command-line
~~~~~~~~~~~~~~~~~~~

The package provides a command-line utility that allows you to perform most filtering and normalization operations. This utility takes advantage of multiprocessing by default, making it particularly useful for batch processing large lists of URLs.


To get started with the command-line utility, you can use the ``--help`` option to display a message listing all available options and parameters: ``courlan --help``.


The following examples show how to read from a file, filter and refine its contents, and write the results to another file.

.. code-block:: bash

    # simple filtering and normalization
    $ courlan --inputfile url-list.txt --outputfile cleaned-urls.txt

    # strict filtering
    $ courlan --strict --inputfile mylist.txt --outputfile mylist-filtered.txt

    # strict filtering including language filter
    $ courlan --language de --strict --inputfile mylist.txt --outputfile mylist-filtered.txt




Sampling by domain name
-----------------------


URL sampling involves selecting a subset from a larger collection of URLs to analyze or crawl. It can improve data quality by reducing biases and outliers, alleviating issues related to overrepresentation (certain websites or domains dominate the dataset) and noise (duplicate or irrelevant URLs clutter the dataset).


Sampling by domain name allows you to control the number of URLs from each website:

Before sampling
    ``website1.com``: 1000 URLs; ``website2.net``: 50 URLs

After sampling
    ``website1.com``: 50 URLs; ``website2.net``: 50 URLs


With Python
~~~~~~~~~~~

.. code-block:: python

    >>> from courlan import sample_urls
    >>> my_urls = ['…', '…', '…', ]  # etc.
    >>> my_sample = sample_urls(my_urls, 50)
    # optional: exclude_min=None, exclude_max=None, strict=False, verbose=False
    

On the command-line
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ courlan --inputfile urls.txt --outputfile samples-urls.txt --sample 50



Internal vs. external links
----------------------------

When gathering links from a page it is often useful to know whether a link stays on the same website or leads elsewhere; this is what the ``external`` argument of ``feeds.find_feed_urls()`` and ``sitemaps.sitemap_search()`` relies on (see `Python usage <usage-python.html#feeds>`_). The underlying function can be used directly:

.. doctest::

    >>> from courlan import is_external

    >>> is_external('https://other.com/page', 'https://www.sitemaps.org/')
    True
    >>> is_external('https://www.sitemaps.org/de/', 'https://www.sitemaps.org/')
    False


Blacklisting
------------


You can provide a blacklist of URLs which will not be processed and included in the output.

- in Python: ``url_blacklist`` parameter (expects a set)
- on the CLI: ``--blacklist`` arguments (expects a file containing URLs)

In Python, you can also pass a blacklist of author names as argument, see `documentation <corefunctions.html>`_.


Storing and reusing URL lists
------------------------------

Internally, ``trafilatura`` and ``courlan`` keep track of URLs with a domain-aware ``UrlStore`` object rather than plain lists — this is what powers throttled, multi-threaded downloads. See `download web pages <downloads.html#trafilatura-backed-parallel-threads>`_ for how to build and use one directly.

.. seealso::
    `Download web pages <downloads.html>`_, `Web crawling <crawls.html>`_

