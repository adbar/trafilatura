URL management
==============

.. meta::
    :description lang=en:
        This page shows how to filter and refine a list of URLs, with Python and on the command-line,
        using the functions provided by the included courlan package.


It is essential to filter out unwanted or noisy URLs to ensure that only relevant and useful URLs are processed. This page shows how to do it with Python and on the command-line, using the functions provided by the ``courlan`` package which is included with Trafilatura.


Filtering input URLs is essential to avoid unwanted URLs, such as those with unnecessary tags (e.g. ``.../tags/abc``) or internationalized rubrics (e.g. ``.../en/....``). It is recommended to filter URLs before retrieving all pages and especially before performing massive downloads. This can help you save time and resources by only processing the URLs that are relevant to your needs.


.. hint::
    See the `Courlan documentation <https://github.com/adbar/courlan>`_ for more examples.


Filtering a list of URLs
------------------------

With Python
~~~~~~~~~~~

The  function ``check_url()`` returns a URL and a domain name if everything is fine. This function is particularly useful for filtering out URLs with specific characteristics, removing unnecessary query parameters, and targeting web pages in specific languages.

.. code-block:: python

    # load the function from the included courlan package
    >>> from courlan import check_url

    # checking a URL returns None or a tuple (cleaned url, hostname)
    >>> check_url('https://github.com/adbar/courlan')
    ('https://github.com/adbar/courlan', 'github.com')

    # noisy query parameters can be removed
    >>> check_url('https://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.org', strict=True)
    ('https://httpbin.org/redirect-to', 'httpbin.org')

    # optional argument targeting webpages in English or German
    >>> my_url = 'https://www.un.org/en/about-us'
    >>> url, domain_name = check_url(my_url, language='en')
    >>> url, domain_name = check_url(my_url, language='de')


The ``courlan`` package provides several other helper functions dedicated to URL cleaning and validation which can help removing unnecessary parts and converting URLs to a conform and standard representation.


Cleaning URLs removes unnecessary characters and normalizes them to a standard format, preventing errors and inconsistencies that can arise from malformed or duplicate URLs.

.. code-block:: python

    >>> from courlan import clean_url

    >>> clean_url('HTTPS://WWW.DWDS.DE:80/')
    'https://www.dwds.de'


Validation checks whether a URL conforms to the expected format, preventing errors further down the line:

.. code-block:: python

    >>> from courlan import validate_url

    >>> validate_url('http://1234')
    (False, None)
    >>> validate_url('http://www.example.org/')
    (True, ParseResult(scheme='http', netloc='www.example.org', path='/', params='', query='', fragment=''))




On the command-line
~~~~~~~~~~~~~~~~~~~

The package provides a command-line utility that allows you to perform most filtering and normalization operations. This utility takes advantage of multiprocessing by default, making it particularly useful for batch processing large lists of URLs.


To get started with the command-line utility, you can use the ``--help`` option to display a message listing all available options and parameters: ``courlan --help``.


The following examples show how to read from a file, filter and refine its contents, and write the results to another file.

.. code-block:: bash

    # simple filtering and normalization
    $ courlan --inputfile url-list.txt --outputfile cleaned-urls.txt

    # strict filtering
    $ courlan --language de --strict --inputfile mylist.txt --outputfile mylist-filtered.txt

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

    $ courlan --inputfile urls.txt --outputfile samples-urls.txt --sample --samplesize 50



Blacklisting
------------


You can provide a blacklist of URLs which will not be processed and included in the output.

- in Python: ``url_blacklist`` parameter (expects a set)
- on the CLI: ``--blacklist`` arguments (expects a file containing URLs)

In Python, you can also pass a blacklist of author names as argument, see `documentation <corefunctions.html>`_.

