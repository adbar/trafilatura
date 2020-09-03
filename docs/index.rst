Welcome to Trafilatura's documentation!
=======================================

.. image:: https://img.shields.io/pypi/v/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python package

.. image:: https://img.shields.io/pypi/pyversions/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python versions

.. image:: https://img.shields.io/travis/adbar/trafilatura.svg
    :target: https://travis-ci.org/adbar/trafilatura
    :alt: Travis build status

.. image:: https://img.shields.io/codecov/c/github/adbar/trafilatura.svg
    :target: https://codecov.io/gh/adbar/trafilatura
    :alt: Code Coverage

|

:Code:           https://github.com/adbar/trafilatura
:Documentation:  https://trafilatura.readthedocs.io/
:Issue tracker:  https://github.com/adbar/trafilatura/issues

|

.. image:: trafilatura-demo.gif
    :alt: Demo as GIF image
    :align: center
    :width: 85%
    :target: https://trafilatura.readthedocs.org/


Description
-----------

*Trafilatura* is a Python package and command-line tool which seamlessly downloads, parses, and scrapes web page data: it can extract metadata, main body text and comments while preserving part of the text formatting and page structure. The output can then be converted to different formats.

Distinguishing between a whole page and its essential parts can help to alleviate many quality problems related to web texts by dealing with noise caused by recurring elements, such as headers and footers, ads, links/blogroll, and so on.

The extractor has to be precise enough not to miss texts or discard valid documents; it should robust but also reasonably fast. Trafilatura is designed to run in production on millions of web documents.


Features
~~~~~~~~

- Seamless online (including page retrieval) or parallelized offline processing with URLs, HTML files or parsed HTML trees as input
- Several output formats supported:
   - Plain text (minimal formatting)
   - CSV (with metadata, `tab-separated values <https://en.wikipedia.org/wiki/Tab-separated_values>`_)
   - JSON (with metadata)
   - XML (for metadata and structure)
   - `TEI-XML <https://tei-c.org/>`_
- Robust extraction algorithm, using `readability <https://github.com/buriy/python-readability>`_ and `jusText <http://corpus.tools/wiki/Justext>`_ as fallback, reasonably efficient with `lxml <http://lxml.de/>`_:
    - Focuses on main text and/or comments
    - Structural elements preserved: paragraphs, titles, lists, quotes, code, line breaks, in-line text formatting (experimental)
    - Extraction of metadata (title, author, date, site name, categories and tags)
- URL lists:
    - Generation of link lists from ATOM/RSS feeds
    - Efficient processing of URL queue
    - Blacklists or already processed URLs
- Optional language detection on the extracted content


Evaluation and alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The extraction focuses on the main content: usually the part displayed centrally, without left or right bars, header or footer, but including potential titles and (optionally) comments. These tasks are also known as web scraping, boilerplate removal, DOM-based content extraction, main content identification, or web page cleaning.

For reproducible results see the `evaluation page <evaluation.html>`_ and the `evaluation script <https://github.com/adbar/trafilatura/blob/master/tests/comparison.py>`_.

External evaluations:
^^^^^^^^^^^^^^^^^^^^^

- Trafilatura is the most efficient open-source library in *ScrapingHub*'s `article extraction benchmark <https://github.com/scrapinghub/article-extraction-benchmark>`_.
- Best overall tool according to Gaël Lejeune & Adrien Barbaresi, `Bien choisir son outil d'extraction de contenu à partir du Web <https://hal.archives-ouvertes.fr/hal-02768510v3/document>`_ (2020, PDF, French).


Installation
------------

Primarily, with Python package manager: ``pip install --upgrade trafilatura``.

For more details please read the `installation documentation <installation.html>`_.


Usage
-----

With Python or on the command-line.

In a nutshell, with Python:

.. code-block:: python

    >>> import trafilatura
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> trafilatura.extract(downloaded)
    # outputs main content and comments as plain text ...

On the command-line:

.. code-block:: bash

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...

For more information please refer to `quickstart <quickstart.html>`_, `usage documentation <usage.html>`_ and `tutorials <tutorials.html>`_.


License
-------

*trafilatura* is distributed under the `GNU General Public License v3.0 <https://github.com/adbar/htmldate/blob/master/LICENSE>`_. If you wish to redistribute this library but feel bounded by the license conditions please try interacting `at arms length <https://www.gnu.org/licenses/gpl-faq.html#GPLInProprietarySystem>`_, `multi-licensing <https://en.wikipedia.org/wiki/Multi-licensing>`_ with `compatible licenses <https://en.wikipedia.org/wiki/GNU_General_Public_License#Compatibility_and_multi-licensing>`_, or `contacting me <https://github.com/adbar/trafilatura#author>`_.

See also `GPL and free software licensing: What's in it for business? <https://www.techrepublic.com/blog/cio-insights/gpl-and-free-software-licensing-whats-in-it-for-business/>`_


Going further
-------------

*Trafilatura*: `Italian word <https://en.wiktionary.org/wiki/trafilatura>`_ for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_.

-  In order to gather web documents it can be useful to download the portions of a website programmatically, here is `how to use sitemaps to crawl websites <http://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_
-  `Download von Web-Daten <https://www.bubenhofer.com/korpuslinguistik/kurs/index.php?id=eigenes_wwwdownload.html>`_ & `Daten aufbereiten und verwalten <https://www.bubenhofer.com/korpuslinguistik/kurs/index.php?id=eigenes_aufbereitenXML.html>`_ (Tutorials in German by Noah Bubenhofer)


Roadmap
~~~~~~~

-  [X] Language detection on the extracted content
-  [-] Duplicate detection at sentence, paragraph and document level using a least recently used (LRU) cache
-  [-] URL lists and document management
-  [ ] Sitemaps processing
-  [ ] Interaction with web archives (notably WARC format)
-  [ ] Configuration and extraction parameters
-  [ ] Integration of natural language processing tools


Contributing
~~~~~~~~~~~~

`Contributions <https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ are welcome!

Feel free to file issues on the `dedicated page <https://github.com/adbar/trafilatura/issues>`_. Thanks to the `contributors <https://github.com/adbar/trafilatura/graphs/contributors>`_ who submitted features and bugfixes!


Author
------

This effort is part of methods to derive information from web documents in order to build `text databases for research <https://www.dwds.de/d/k-web>`_ (chiefly linguistic analysis and natural language processing). Extracting and pre-processing web texts presents a substantial challenge for those who must meet scientific expectations. Web corpus construction involves numerous design decisions, and this software package can help facilitate collection and enhance corpus quality and thus aid in these decisions.

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg
   :target: https://doi.org/10.5281/zenodo.3460969

-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://konvens.org/proceedings/2019/papers/kaleidoskop/camera_ready_barbaresi.pdf>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.

You can contact me via my `contact page <https://adrien.barbaresi.eu/>`_ or `GitHub <https://github.com/adbar>`_.


Further documentation
=====================

.. toctree::
   :maxdepth: 1

   installation
   quickstart
   usage
   tutorials
   evaluation
   corefunctions


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
