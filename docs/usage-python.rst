With Python
===========

.. meta::
    :description lang=en:
        This tutorial focuses on text extraction from web pages with Python code snippets.
        Data mining with this library encompasses HTML parsing and language identification.



The Python programming language
-------------------------------

Python can be easy to pick up whether you're a first time programmer or you're experienced with other languages:

-  Official `Python Tutorial <https://docs.python.org/3/tutorial/>`_
-  `The Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_
-  `Learn Python Programming Step by Step <https://www.techbeamers.com/python-tutorial-step-by-step/>`_
-  `The Best Python Tutorials (freeCodeCamp) <https://www.freecodecamp.org/news/best-python-tutorial/>`_



Step-by-step
------------


.. code-block:: python

    >>> from trafilatura import fetch_url, extract
    >>> url = 'https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/'
    >>> downloaded = fetch_url(url)
    >>> downloaded is None # assuming the download was successful
    False
    >>> result = extract(downloaded)
    >>> print(result)
    # newlines preserved, TXT output ...
    # source URL provided for metadata
    >>> result = extract(downloaded, xml_output=True, url=url)
    >>> print(result)
    # some formatting preserved in basic XML structure ...

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

..hint:
    The inclusion of tables and comments can be deactivated at a function call. The use of fallback algorithms can also be bypassed in *fast* mode:

.. code-block:: python

    # no comments in output
    >>> result = extract(downloaded, include_comments=False)
    # skip tables examination
    >>> result = extract(downloaded, include_tables=False)
    # skip justext algorithm used as fallback
    >>> result = extract(downloaded, no_fallback=True)

This values combined probably provide the fastest execution times:

.. code-block:: python

    >>> result = extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)


See also Python Notebook `Trafilatura Overview <Trafilatura_Overview.ipynb>`_.


Extraction settings
-------------------

Text extraction
^^^^^^^^^^^^^^^

Text extraction can be parametrized by providing a custom configuration file (that is a variant of `settings.cfg <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.cfg>`_) with the ``config`` parameter in ``bare_extraction`` or ``extract``, which overrides the standard settings:

.. code-block:: python

    >>> from trafilatura import extract
    >>> from trafilatura.settings import use_config
    # load the new settings by providing a file name
    >>> newconfig = use_config("myfile.cfg")
    # use with a previously downloaded document
    >>> extract(downloaded, config=newconfig)
    # provide a file name directly (can be slower)
    >>> extract(downloaded, settingsfile="myfile.cfg")


Output Python objects
^^^^^^^^^^^^^^^^^^^^^

The extraction can be customized using a series of parameters, for more see the `core functions <corefunctions.html>`_ page.

The function ``bare_extraction`` can be used to bypass output conversion, it returns Python variables for  metadata (dictionary) as well as main text and comments (both LXML objects).

.. code-block:: python

    >>> from trafilatura import bare_extraction
    >>> bare_extraction(downloaded)


Choice of HTML elements
^^^^^^^^^^^^^^^^^^^^^^^

Including extra elements works best with conversion to XML formats (``output_format="xml"``) or ``bare_extraction()``. Both ways allow for direct display and manipulation of the elements.

- ``include_formatting=True``: Keep structural elements related to formatting (``<b>``/``<strong>``, ``<i>``/``<emph>`` etc.)
- ``include_links=True``: Keep link targets (in ``href="..."``)
- ``include_images=True``: Keep track of images along with their targets (``<img>`` attributes: alt, src, title)
- ``include_tables=True``: Extract text from HTML ``<table>`` elements.

Only ``include_tables`` is activated by default.


Language identification
^^^^^^^^^^^^^^^^^^^^^^^

Experimental feature: the target language can also be set using 2-letter codes (`ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_), there will be no output if the detected language of the result does not match and no such filtering if the identification component has not been installed (see above for installation instructions).

.. code-block:: python

    >>> result = extract(downloaded, url, target_language='de')


Date extraction
^^^^^^^^^^^^^^^

Among metadata extraction, dates are handled by an external module: `htmldate <https://github.com/adbar/htmldate>`_. By default, focus is on original dates and the extraction replicates the *fast/no_fallback* option.

`Custom parameters <https://htmldate.readthedocs.io/en/latest/corefunctions.html#handling-date-extraction>`_ can be passed through the extraction function or through the ``extract_metadata`` function in ``trafilatura.metadata``, most notably:

-  ``extensive_search`` (boolean), to activate pattern-based opportunistic text search,
-  ``original_date`` (boolean) to look for the original publication date,
-  ``outputformat`` (string), to provide a custom datetime format,
-  ``max_date`` (string), to set the latest acceptable date manually (YYYY-MM-DD format).

.. code-block:: python

    >>> from trafilatura import extract
    # pass the new parameters as dict, with a previously downloaded document
    >>> extract(downloaded, output_format="xml", date_extraction_params={"extensive_search": True, "max_date": "2018-07-01"})


Passing URLs
^^^^^^^^^^^^

Even if the page to process has already been downloaded it can still be useful to pass the URL as an argument. See this `previous bug <https://github.com/adbar/trafilatura/issues/75>`_ for an example:

.. code-block:: python

    >>> url = "https://www.thecanary.co/feature/2021/05/19/another-by-election-headache-is-incoming-for-keir-starmer"
    >>> downloaded = fetch_url(url)
    >>> bare_extraction(downloaded, with_metadata=True)
    # content discarded since necessary metadata couldn't be extracted
    >>> url = "https://www.thecanary.co/feature/2021/05/19/another-by-election-headache-is-incoming-for-keir-starmer"
    >>> bare_extraction(downloaded, with_metadata=True, url=url)
    # date found in URL, extraction successful


Customization
-------------


Settings file
^^^^^^^^^^^^^


The standard `settings file <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.cfg>`_ can be modified. It currently entails variables related to text extraction.

.. code-block:: python

    >>> from trafilatura.settings import use_config
    >>> myconfig = use_config('path/to/myfile')
    >>> extract(downloaded, config=myconfig)


User agent settings can also be specified in a custom ``settings.cfg`` file. Then you can apply the changes by parsing it beforehand and using the config argument.


Raw HTTP response objects
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``fetch_url()`` function can pass a urllib3 response object straight to the extraction by setting the optional ``decode`` argument to ``False``.

This can be useful to get the final redirection URL with ``response.geturl()`` and then pass is directly as a URL argument to the extraction function:

.. code-block:: python

    >>> from trafilatura import fetch_url, bare_extraction
    >>> response = fetch_url(url, decode=False)
    >>> bare_extraction(response, url=response.geturl()) # here is the redirection URL


LXML objects
^^^^^^^^^^^^

The input can consist of a previously parsed tree (i.e. a *lxml.html* object), which is then handled seamlessly:

.. code-block:: python

    >>> from lxml import html
    >>> mytree = html.fromstring('<html><body><article><p>Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></article></body></html>')
    >>> extract(mytree)
    'Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n'


Package settings
^^^^^^^^^^^^^^^^

For further configuration (if the ``settings.cfg`` file is not enough) you can edit package-wide variables contained in the `settings.py <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.py>`_ file:

1. `Clone the repository <https://docs.github.com/en/free-pro-team@latest/github/using-git/which-remote-url-should-i-use>`_
2. Edit ``settings.py``
3. Reinstall the package locally: ``pip install --no-deps -U .`` in the home directory of the cloned repository

These remaining variables greatly alter the functioning of the package!


Navigation
----------

Feeds
^^^^^


The function ``find_feed_urls`` is a all-in-one utility that attemps to discover the feeds from a webpage if required and/or downloads and parses feeds. It returns the extracted links as list, more precisely as a sorted list of unique links.

.. code-block:: python

    >>> from trafilatura import feeds
    >>> mylist = feeds.find_feed_urls('https://www.theguardian.com/')
    # https://www.theguardian.com/international/rss has been found
    >>> mylist
    ['https://www.theguardian.com/...', '...'] # and so on
    # use a feed URL directly
    >>> mylist = feeds.find_feed_urls('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')
    >>> mylist is not []
    True # it's not empty


.. note::
    The links are seamlessly filtered for patterns given by the user, e.g. using ``https://www.un.org/en/`` as argument implies taking all URLs corresponding to this category.


An optional argument ``target_lang`` makes it possible to filter links according to their expected target language. A series of heuristics are applied on the link path and parameters to try to discard unwanted URLs, thus saving processing time and download bandwidth.


.. code-block:: python

    >>> from trafilatura import feeds
    >>> mylist = feeds.find_feed_urls('https://www.un.org/en/rss.xml', target_lang='en')
    >>> mylist is not []
    True # links found as expected
    >>> mylist = feeds.find_feed_urls('https://www.un.org/en/rss.xml', target_lang='ja')
    >>> mylist
    [] # target_lang set to Japanese, the English links were discarded this time

For more information about feeds and web crawling see:

- This blog post: `Using RSS and Atom feeds to collect web pages with Python <https://adrien.barbaresi.eu/blog/using-feeds-text-extraction-python.html>`_
- This Youtube tutorial: `Extracting links from ATOM and RSS feeds <https://www.youtube.com/watch?v=NW2ISdOx08M&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci&index=2&t=136s>`_


Sitemaps
^^^^^^^^

- Youtube tutorial: `Learn how to process XML sitemaps to extract all texts present on a website <https://www.youtube.com/watch?v=uWUyhxciTOs>`_

.. code-block:: python

    >>> from trafilatura import sitemaps
    >>> mylinks = sitemaps.sitemap_search('https://www.theguardian.com/')
    # this function also accepts a target_lang argument
    >>> mylinks = sitemaps.sitemap_search('https://www.un.org/', target_lang='en')

The links are also seamlessly filtered for patterns given by the user, e.g. using ``https://www.theguardian.com/society`` as argument implies taking all URLs corresponding to the society category.


