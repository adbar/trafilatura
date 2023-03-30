URL management
==============

.. meta::
    :description lang=en:
        This page shows how to filter a list of URLs, with Python and on the command-line,
        using the functions provided by the included courlan package.


This page shows how to filter a list of URLs, with Python and on the command-line, using the functions provided by the ``courlan`` package which is included with Trafilatura.

Filtering of input URLs is useful to avoid hodgepodges like ``.../tags/abc`` or "internationalized" rubrics like ``.../en/....``. It is best used on URL lists, before retrieving all pages and especially before massive downloads.


.. hint::
    See the `Courlan documentation <https://github.com/adbar/courlan>`_ for more examples.


Filtering a list of URLs
------------------------

With Python
~~~~~~~~~~~

The  function ``check_url()`` returns a URL and a domain name if everything is fine:

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


Other useful functions include URL cleaning and validation:

.. code-block:: python

    # helper function to clean URLs
    >>> from courlan import clean_url

    >>> clean_url('HTTPS://WWW.DWDS.DE:80/')
    'https://www.dwds.de'

    # URL validation
    >>> from courlan import validate_url
    >>> validate_url('http://1234')
    (False, None)
    >>> validate_url('http://www.example.org/')
    (True, ParseResult(scheme='http', netloc='www.example.org', path='/', params='', query='', fragment=''))




On the command-line
~~~~~~~~~~~~~~~~~~~

Most fonctions are also available through a command-line utility:

.. code-block:: bash

    # display a message listing all options
    $ courlan --help

    # simple filtering and normalization
    $ courlan --inputfile url-list.txt --outputfile cleaned-urls.txt

    # strict filtering
    $ courlan --language de --strict --inputfile mylist.txt --outputfile mylist-filtered.txt

    # strict filtering including language filter
    $ courlan --language de --strict --inputfile mylist.txt --outputfile mylist-filtered.txt




Sampling by domain name
-----------------------


This sampling methods allows for restricting the number of URLs to keep per host, for example:

Before
    ``website1.com``: 1000 URLs; ``website2.net``: 50 URLs

After
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

