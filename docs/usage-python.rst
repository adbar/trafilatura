Python usage
============

.. meta::
    :description lang=en:
        This tutorial focuses on text extraction from web pages with Python code snippets.
        Data mining with this library encompasses HTML parsing and language identification.



The Python programming language
-------------------------------

Python can be easy to pick up whether you're a first time programmer or you're experienced with other languages:

-  Official `Python Tutorial <https://docs.python.org/3/tutorial/>`_
-  `The Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_
-  `The Best Python Tutorials (freeCodeCamp) <https://www.freecodecamp.org/news/best-python-tutorial/>`_



Step-by-step
------------

Quickstart
^^^^^^^^^^

For the basics see `quickstart documentation page <quickstart.html>`_.

.. note::
    For a hands-on tutorial see also the Python Notebook `Trafilatura Overview <https://github.com/adbar/trafilatura/blob/master/docs/Trafilatura_Overview.ipynb>`_.


Extraction functions
^^^^^^^^^^^^^^^^^^^^

The functions can be imported using ``from trafilatura import ...`` and used on raw documents (strings) or parsed HTML (LXML elements).

Main text extraction, good balance between precision and recall:

- ``extract``: Main extraction function — runs Trafilatura's own rule-based extractor, then compares its result with readability, and with jusText if the result is short or contains boilerplate elements (see `how extraction works <extraction-overview.html#fallback-cascade>`_)
- ``bare_extraction``: Same cascade as ``extract()``, but returns a ``Document`` object with structured access to text, comments, and metadata
- ``extract_with_metadata``: Same as ``extract()`` with ``with_metadata=True``, but returns a ``Document`` object, the output is in its ``.text`` attribute

.. versionadded:: 2.1.0
    ``extract_with_metadata()``

Simpler alternatives (no cascade, faster):

- ``baseline``: Takes the first source with enough text among embedded JSON content, article elements and text paragraphs, otherwise the whole page body
- ``html2txt``: Extracts all text in the document including navigation, with ``clean=False`` also footers, asides, cookie banners, scripts and styles


.. note::

    For article lists or category pages, discover URLs with
    `Courlan's link extraction <url-management.html#extracting-links-from-a-page>`_
    or Trafilatura's `feeds`_, `sitemaps`_ and
    `web crawler <crawls.html>`_, then extract each article separately.
    ``include_links=True`` only keeps links in the extracted content; it is not
    a link discovery function.



Output
^^^^^^

By default, the output is in plain text (TXT) format without metadata. The following additional formats are available:

- CSV
- HTML
- JSON
- Markdown
- XML and XML-TEI (following the guidelines of the Text Encoding Initiative)

To specify the output format, use one of the following strings: ``"csv", "json", "html", "markdown", "txt", "xml", "xmltei"``. Another value raises a ``ValueError``.

.. versionchanged:: 2.4.0
    Unknown formats raise a ``ValueError`` instead of an ``AttributeError``.

The ``bare_extraction`` function uses the ``python`` format by default and returns a ``Document`` object for direct use in Python, see `Python objects as output`_.

To extract and include metadata in the output, use the ``with_metadata=True`` argument.

.. warning::
    .. versionchanged:: 1.11.0
        Metadata is no longer extracted by default.

Metadata fields
~~~~~~~~~~~~~~~

With ``with_metadata=True``, every output format carries the same fields. TXT and Markdown output start with a YAML header, XML and HTML use attributes and ``<meta>`` elements, XML-TEI fills the ``teiHeader``. Three fields have another name in JSON.

==============  =====================  ================================================
Field           JSON key               Content
==============  =====================  ================================================
title                                  title of the page
author                                 author names
url             ``source``             URL of the page
hostname                               domain name
description     ``excerpt``            description of the page
sitename        ``source-hostname``    name of the website
date                                   publication date
categories                             categories, separated by ``;``, a list in YAML, one ``<term>`` each in XML-TEI
tags                                   tags, separated by ``;``, a list in YAML, one ``<term>`` each in XML-TEI
fingerprint                            hash of the title and text, see `deduplication <deduplication.html>`_
id                                     value of ``record_id``
license                                free license, e.g. ``CC BY 4.0``
language                               language code
image                                  URL of the main image
pagetype                               type of page, e.g. ``article``
filedate                               ``max_date`` of the date extraction: the day of the extraction by default, of the file with ``--input-dir``
==============  =====================  ================================================

CSV output is a tab-separated row without header, in this order: url, id, fingerprint, hostname, title, image, date, text, comments, license, pagetype, author, description, sitename, categories, tags, language, filedate.

.. warning::
    .. versionchanged:: 2.4.0
        CSV rows have 18 columns instead of 11, the new columns are appended.

.. versionchanged:: 2.4.0
    Image and language are in every output format, the language falls back to the one declared in the markup.

Examples
~~~~~~~~

.. code-block:: python

    # some formatting preserved in basic XML structure
    >>> extract(downloaded, output_format="xml")

    # output in JSON format with metadata extracted
    >>> extract(downloaded, output_format="json", with_metadata=True)


Note that combining TXT and CSV formats with certain structural elements (e.g. formatting or links) triggers output in Markdown format (plain text with additional elements). ``include_formatting`` has no effect on JSON output.



Choice of HTML elements
^^^^^^^^^^^^^^^^^^^^^^^

Customize the extraction process by including or excluding specific HTML elements:


- Text elements:
   ``include_comments=True``
       Include comment sections at the bottom of articles.
   ``include_tables=True``
       Extract text from HTML ``<table>`` elements.

- Structural elements:
   ``include_formatting=True``
        Keep structural elements related to formatting (``<b>``/``<strong>``, ``<i>``/``<emph>`` etc.)
   ``include_links=True``
        Keep link targets (in ``href="..."``)
   ``include_images=True``
        Keep track of images along with their targets (``<img>`` attributes: alt, src, title), also from lazy-loading attributes, ``srcset``, ``<picture>`` and ``<noscript>``

.. warning::
    .. versionchanged:: 2.4.0
        With ``include_tables=False``, text inside layout tables is removed as well.

.. versionadded:: 2.4.0
    Images from more lazy-loading attributes (``data-lazy-src``, ``data-original``), ``srcset``, ``<picture>`` and ``<noscript>``.


To operate on these elements, pass the corresponding parameters to the ``extract()`` function:

.. code-block:: python

    # exclude comments from the output
    >>> result = extract(downloaded, include_comments=False)

    # skip tables and include links in the output
    >>> result = extract(downloaded, include_tables=False, include_links=True)

    # convert relative links to absolute links where possible
    # (pass the same URL used to fetch "downloaded")
    >>> extract(downloaded, output_format='xml', include_links=True, url="https://www.example.org")


Important notes
~~~~~~~~~~~~~~~

- ``include_comments`` and ``include_tables`` are activated by default.
- Including extra elements works best with conversion to XML formats or using ``bare_extraction()``. This allows for direct display and manipulation of the elements.
- Certain elements may not be visible in the output if the chosen format does not allow it.
- Selecting Markdown automatically includes text formatting.


.. hint::
    The heuristics used by the main algorithm change according to the presence of certain elements in the HTML. If the output seems odd, try removing a constraint (e.g. formatting) to improve the result.



The precision and recall presets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main extraction functions offer two presets to adjust the focus of the extraction process:

.. code-block:: python

    # less noise, possibly less text
    >>> result = extract(downloaded, favor_precision=True)

    # more text, possibly more noise
    >>> result = extract(downloaded, favor_recall=True)


Precision
~~~~~~~~~

- Use when your results contain too much boilerplate or irrelevant content.
- Comments are pruned more aggressively, link-heavy sections are discarded, and the baseline rescue and recall escalation are skipped.
- Additionally, you can use the ``prune_xpath`` parameter to target specific HTML elements using a list of XPath expressions:

.. code-block:: python

    # remove elements matching a custom XPath before extraction
    >>> extract(downloaded, prune_xpath='//div[@class="ad"]')


Recall
~~~~~~

- Use when parts of your documents are missing.
- Lists inside discarded sections are kept, text tails are preserved, and link density thresholds are relaxed.
- If content is still missing, try ``html2txt()`` or refer to the `troubleshooting guide <troubleshooting.html>`_.

For a detailed comparison of what each mode changes, see `how extraction works <extraction-overview.html#extraction-modes>`_.



Additional functions for text extraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``html2txt`` and ``baseline`` functions offer simpler approaches to extracting text from HTML content, prioritizing performance over precision.


html2txt()
~~~~~~~~~~

The ``html2txt`` function serves as a last resort for extracting text from HTML content. It emulates the behavior of similar functions in other packages and can be used to output all possible text from a given HTML source, maximizing recall. Footers, asides, cookie banners, scripts and styles are left out unless ``clean=False`` is passed. However, it may not always produce accurate or meaningful results, as it does not consider the context of the extracted sections.

.. code-block:: python

    >>> from trafilatura import html2txt
    >>> html2txt(downloaded)


baseline()
~~~~~~~~~~

For a better balance between precision and recall, as well as improved performance, consider using the ``baseline`` function instead. This function returns a tuple containing an LXML element with the body, the extracted text as a string, and the length of the text.  It uses a set of heuristics to extract text from the HTML content, which generally produces more accurate results than ``html2txt``.

.. code-block:: python

    >>> from trafilatura import baseline
    >>> postbody, text, len_text = baseline(downloaded)

For more advanced use cases, consider using other functions in the package that provide more control and customization over the text extraction process.


Guessing if text can be found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The function ``is_probably_readerable()`` (ported from Mozilla's Readability.js) provides a way to guess if a page probably has a main text to extract.

.. code-block:: python

    >>> from trafilatura.readability_lxml import is_probably_readerable
    >>> is_probably_readerable(downloaded)  # HTML string or already parsed tree


Language identification
^^^^^^^^^^^^^^^^^^^^^^^

The target language can also be set using 2-letter codes (ISO 639-1), there will be no output if the detected language of the result does not match and no such filtering if the identification component has not been installed (see above `installation instructions <installation.html>`_) or if the target language is not available.

.. note::
    This feature requires additional components: ``pip install trafilatura[all]``.
    It currently uses the `py3langid package <https://github.com/adbar/py3langid>`_ and is dependent on language availability and performance of the original model.

.. code-block:: python

    >>> result = extract(downloaded, target_language="de")


Optimizing for speed
^^^^^^^^^^^^^^^^^^^^

Execution speed not only depends on the platform and on supplementary packages (``trafilatura[all]``, ``htmldate[speed]``), but also on the extraction strategy.

By default, ``extract()`` runs a cascade: its own rule-based extractor first, then a comparison with readability and jusText. These fallbacks improve accuracy but are slower. In *fast* mode they are skipped entirely, making extraction faster:

.. code-block:: python

    # skip algorithms used as fallback
    >>> result = extract(downloaded, fast=True)

.. versionchanged:: 2.0.0
    ``fast`` replaces ``no_fallback``.

The following combination usually leads to shorter processing times:

.. code-block:: python

    >>> result = extract(downloaded, include_comments=False, include_tables=False, fast=True)


Extraction settings
-------------------

.. hint::
    See also `settings page <settings.html>`_.


Function parameters
^^^^^^^^^^^^^^^^^^^

The ``Extractor`` class provides a convenient way to define and manage extraction parameters. It is useful when reusing the same settings across multiple extractions or when configuring options not exposed as ``extract()`` parameters.

Here is how to use the class:

.. code-block:: python

    # import the Extractor class from the settings module
    >>> from trafilatura.settings import Extractor

    # set multiple options at once
    >>> options = Extractor(output_format="json", with_metadata=True)

    # add or adjust settings as needed
    >>> options.formatting = True  # same as include_formatting
    >>> options.source = "My Source"  # useful for debugging

    # use the options in an extraction function
    >>> extract(downloaded, options=options)

With ``options``, the other extraction parameters are ignored, except ``url``, ``record_id`` and ``prune_xpath``. The ``url`` argument applies on a copy of the options.

.. versionchanged:: 2.4.0
    ``url`` also applies when ``options`` are passed.


Metadata extraction
^^^^^^^^^^^^^^^^^^^

- ``with_metadata=True``: extract metadata fields and include them in the output
- ``only_with_metadata=True``: only output documents featuring all essential metadata (date, title, url)
- ``record_id``: attach a custom ID to the ``id`` metadata field, useful for tracking documents through a corpus-building pipeline (see `building a training corpus <tutorial-datasets.html>`_)

.. code-block:: python

    >>> extract(downloaded, record_id="doc-042", output_format="json", with_metadata=True)


Date
~~~~

Among metadata extraction, dates are handled by an external module: `htmldate <https://github.com/adbar/htmldate>`_. Dates are only extracted with ``with_metadata=True``. By default, focus is on original dates and the extensive search is activated (``EXTENSIVE_DATE_SEARCH`` in ``settings.cfg``).

`Custom parameters <https://htmldate.readthedocs.io/en/latest/corefunctions.html#handling-date-extraction>`_ can be passed through the extraction function or through the ``extract_metadata`` function in ``trafilatura.metadata``, most notably:

-  ``extensive_search`` (boolean), to activate further heuristics (higher recall, lower precision)
-  ``original_date`` (boolean) to look for the original publication date,
-  ``outputformat`` (string), to provide a custom datetime format,
-  ``max_date`` (string), to set the latest acceptable date manually (YYYY-MM-DD format).

.. code-block:: python

    # import the extract() function, use a previously downloaded document
    # pass the new parameters as dict
    >>> extract(downloaded, output_format="xml", with_metadata=True, date_extraction_params={
            "extensive_search": True, "max_date": "2018-07-01"
        })

Custom parameters are merged with the defaults, only the values to change need to be passed.

.. warning::
    .. versionchanged:: 2.4.0
        Custom parameters are merged with the defaults. Before, they replaced them, and passing any of them turned ``original_date`` off.


URL
~~~

Even if the page to process has already been downloaded it can still be useful to pass the URL as an argument. See this `previous bug <https://github.com/adbar/trafilatura/issues/75>`_ for an example:

.. code-block:: python

    # define a URL and download the example
    >>> url = "https://web.archive.org/web/20210613232513/https://www.thecanary.co/feature/2021/05/19/another-by-election-headache-is-incoming-for-keir-starmer/"
    >>> downloaded = fetch_url(url)

    # content discarded since necessary metadata couldn't be extracted
    >>> bare_extraction(downloaded, only_with_metadata=True)
    >>>

    # date found in URL, extraction successful
    >>> bare_extraction(downloaded, only_with_metadata=True, url=url)


Memory use
^^^^^^^^^^

Trafilatura uses caches to speed up extraction and cleaning processes. This may lead to memory leaks in some cases, particularly in large-scale applications. If that happens you can reset all cached information in order to release RAM:

.. doctest::

    # import the function
    >>> from trafilatura.meta import reset_caches

    # use it at any given point
    >>> reset_caches()


Input/Output types
------------------

Python objects as output
^^^^^^^^^^^^^^^^^^^^^^^^

The extraction can be customized using a series of parameters, for more see the `core functions <corefunctions.html>`_ page.

The function ``bare_extraction`` can be used to bypass output conversion. It returns a ``Document`` object with the text and metadata as attributes (``.title``, ``.author``, ``.text``, ``.comments``, etc., strings except the lists of ``.categories`` and ``.tags``) and the extracted content as LXML elements (``.body``, ``.commentsbody``). Call ``.as_dict()`` on the result to get a plain dictionary.

.. versionchanged:: 2.0.0
    ``bare_extraction()`` returns a ``Document`` instead of a dict.

The metadata attributes are only filled with ``with_metadata=True``, which ``only_with_metadata``, ``url_blacklist``, ``author_blacklist`` and XML-TEI output also turn on. They are ``None`` otherwise. ``fingerprint`` and ``id`` are only set by ``extract()``.

.. code-block:: python

    >>> from trafilatura import bare_extraction
    >>> bare_extraction(downloaded, with_metadata=True)


Raw HTTP response objects
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``fetch_response()`` function can pass a response object straight to the extraction.

This can be useful to get the final redirection URL with ``response.url`` and then pass it directly as a URL argument to the extraction function:

.. code-block:: python

    # necessary components
    >>> from trafilatura import fetch_response, bare_extraction

    # load an example
    >>> response = fetch_response("https://www.example.org")

    # perform extract() or bare_extraction() on Trafilatura's response object
    >>> bare_extraction(response.data, url=response.url)  # here is the redirection URL


LXML objects
^^^^^^^^^^^^

The input can consist of a previously parsed tree (i.e. a *lxml.html* object), which is then handled seamlessly:

.. doctest::

    # define document and load it with LXML
    >>> from trafilatura import extract
    >>> from lxml import html
    >>> my_doc = """<html><body><article><p>
    ...                 Here is the main text.
    ...                 </p></article></body></html>"""
    >>> mytree = html.fromstring(my_doc)

    # extract from the already loaded LXML tree
    >>> extract(mytree)
    'Here is the main text.'


Interaction with BeautifulSoup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trafilatura works with LXML trees, not BeautifulSoup objects. If you already have a BS4 parse tree, convert it first:

.. doctest::

    >>> from bs4 import BeautifulSoup
    >>> from lxml.html.soupparser import convert_tree
    >>> from lxml import etree, html
    >>> from trafilatura import extract

    >>> soup = BeautifulSoup("<html><body><article><p>The date is Feb 2, 2024.</p></article></body></html>", "lxml")
    >>> lxml_tree = convert_tree(soup)[0]

.. warning::
    ``convert_tree()`` returns a tree rooted at ``<body>``, not ``<html>``. Passing it to ``extract()`` as-is returns ``None`` regardless of content, since the extractor expects a document rooted at ``<html>``. Re-wrap it first:

.. doctest::

    >>> wrapped = html.fromstring("<html>" + etree.tostring(lxml_tree).decode() + "</html>")
    >>> extract(wrapped)
    'The date is Feb 2, 2024.'


Navigation
----------

Trafilatura can discover URLs to extract from via three strategies:

- **Feeds** (Atom, RSS, JSON Feed): mostly for fresh content
- **Sitemaps**: for exhaustivity — all potential pages as listed by the site owners
- **Web crawling**: follow internal links to discover pages

``find_feed_urls()`` and ``sitemap_search()`` wait ``SLEEP_TIME`` seconds (see `settings <settings.html#file-structure>`_) before each further feed or sitemap of the same website, pass ``sleep_time`` to change it.

.. versionchanged:: 2.4.0
    The default wait went from 2 to 5 seconds and is read from ``SLEEP_TIME``.

The ``Disallow`` rules of ``robots.txt`` are not applied to links found in feeds and sitemaps, only the crawler follows them. See `downloads <downloads.html#robots-exclusion-standard>`_ to filter a list of links.


Feeds
^^^^^

The function ``find_feed_urls`` is a all-in-one utility that attempts to discover the feeds from a webpage if required and/or downloads and parses feeds. It returns the extracted links as list, more precisely as a sorted list of unique links.

.. code-block:: python

    # import the feeds module
    >>> from trafilatura import feeds

    # use the homepage to automatically retrieve feeds
    >>> mylist = feeds.find_feed_urls('https://www.theguardian.com/')
    >>> mylist
    ['https://www.theguardian.com/international/rss', '...'] # and so on

    # use a predetermined feed URL directly
    >>> mylist = feeds.find_feed_urls('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')
    >>> bool(mylist)
    True # it's not empty


.. note::
    The links are seamlessly filtered for patterns given by the user, e.g. using ``https://www.un.org/en/`` as argument implies taking all URLs corresponding to this category.


An optional argument ``target_lang`` makes it possible to filter links according to their expected target language. A series of heuristics are applied on the link path and parameters to try to discard unwanted URLs, thus saving processing time and download bandwidth.

An optional ``external`` argument controls whether URLs from other domains are included. By default, only URLs matching the input domain are returned (``external=False``).


.. code-block:: python

    # the feeds module has to be imported
    # search for feeds in English
    >>> mylist = feeds.find_feed_urls('https://www.un.org/en/rss.xml', target_lang='en')
    >>> bool(mylist)
    True # links found as expected

    # target_lang set to Japanese, the English links are discarded
    >>> mylist = feeds.find_feed_urls('https://www.un.org/en/rss.xml', target_lang='ja')
    >>> mylist
    []

For more information about feeds and web crawling see:

- This blog post: `Using RSS and Atom feeds to collect web pages with Python <https://adrien.barbaresi.eu/blog/using-feeds-text-extraction-python.html>`_
- This Youtube tutorial: `Extracting links from ATOM and RSS feeds <https://www.youtube.com/watch?v=NW2ISdOx08M&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci&index=2&t=136s>`_


Sitemaps
^^^^^^^^

- Youtube tutorial: `Learn how to process XML sitemaps to extract all texts present on a website <https://www.youtube.com/watch?v=uWUyhxciTOs>`_

.. code-block:: python

    # load sitemaps module
    >>> from trafilatura import sitemaps

    # automatically find sitemaps by providing the homepage
    >>> mylinks = sitemaps.sitemap_search('https://developer.mozilla.org/')

    # the target_lang argument works as explained above
    >>> mylinks = sitemaps.sitemap_search('https://developer.mozilla.org/', target_lang='en')

The links are also seamlessly filtered for patterns given by the user, e.g. using ``https://developer.mozilla.org/en-US/docs/Web/CSS`` as argument implies taking all URLs corresponding to the CSS documentation category.

An optional ``external`` argument controls whether URLs from other domains are included. By default, only URLs matching the input domain are returned (``external=False``).

Pass your HTTP client's decoded response text or a cached sitemap to ``parse_sitemap()`` to parse one file without network requests:

.. code-block:: python

    from pathlib import Path
    from trafilatura.sitemaps import parse_sitemap

    sitemap_text = Path("sitemap.xml").read_text(encoding="utf-8")
    links = parse_sitemap(sitemap_text, "https://example.org/sitemap.xml")

The result contains sorted unique links. For a sitemap index, these are nested sitemap addresses. Fetch and parse those separately with your own HTTP client. The ``target_lang`` and ``external`` options apply the existing link filters.

.. versionadded:: 2.4.0
    ``parse_sitemap()``


Web crawling
^^^^^^^^^^^^

See the `documentation page on web crawling <crawls.html>`_ for more information.


.. hint::
    For more information on how to refine and filter a URL collection, see the underlying `courlan <https://github.com/adbar/courlan>`_ library.


Deprecations
------------

See the `deprecations and migration <deprecations.html>`_ page for a full list of deprecated functions, arguments, and migration instructions.

.. seealso::
    `Settings and customization <settings.html>`_, `Command-line usage <usage-cli.html>`_, `Core functions <corefunctions.html>`_
