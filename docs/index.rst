trafilatura: Scrapes the main text of web pages while preserving some structure
===============================================================================

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

|

*Trafilatura* downloads web pages, scrapes main text and comments while preserving some structure, and converts to TXT, CSV, XML & TEI-XML. All the operations needed are handled seamlessly.

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


Description
-----------

This library performs a robust extraction which focuses on the main content, which is usually the part displayed centrally, without the left or right bars, the header or the footer, but including potential titles and comments. *Trafilatura* can seamlessly download, parse and convert web documents. It scrapes the main body text while preserving part of the text formatting and page structure, a task also known as web scraping, boilerplate removal, DOM-based content extraction, main content identification, or web page cleaning.

Distinguishing between whole page and essential parts can help to alleviate many quality problems related to web texts as it can help with the noise consisting of recurring elements (headers and footers, ads, links/blogroll, etc.) It has to be precise enough not to miss texts or discard valid documents, it also has to be reasonably fast, as it is expected to run in production on millions of documents.


Features
~~~~~~~~

-  Seamless download and extraction: URLs, HTML files or parsed HTML trees as input
-  Focus on main text and/or comments
-  Formatting and structural elements preserved: paragraphs, titles, lists, quotes, code, line breaks, in-line text formatting (experimental)
-  Output in plain text (minimal formatting), CSV (with metadata, `tab-separated values <https://en.wikipedia.org/wiki/Tab-separated_values>`_) or XML format (for metadata and structure)
-  Extraction of metadata (currently title and date, more to come)
-  Computationally efficient (relies on `lxml <http://lxml.de/>`_)
-  Robust extraction and generic `jusText algorithm <http://corpus.tools/wiki/Justext>`_ used as fallback
-  Optional language detection on the extracted content


Evaluation and alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For first experimental results see the `evaluation page <evaluation.html>`_.


Installation
------------

This `Python <https://wiki.python.org/moin/BeginnersGuide/Overview>`_ package is tested on Linux, macOS and Windows systems, it is compatible with Python 3.4 upwards (see `install Python guide <https://wiki.python.org/moin/BeginnersGuide/Download>`_). It is available on the package repository `PyPI <https://pypi.org/>`_ and can notably be installed with ``pip`` or ``pipenv``:

.. code-block:: bash

    $ pip install trafilatura # pip3 install on systems where both Python 2 and 3 are installed

This project is under active development, please make sure you keep it up-to-date to benefit from latest improvements:

.. code-block:: bash

    $ pip install -U trafilatura # to make sure you have the latest version
    $ pip install -U git+https://github.com/adbar/trafilatura.git # latest available code (see build status above)

A few additional libraries can be installed for extended functionality and faster processing: extraction of publication date (``htmldate``), language detection (``langid``), and faster processing of downloads (``cchardet``, currently not working on some macOS versions).

.. code-block:: bash

    $ pip install trafilatura[metadata] # metadata extraction (work in progress)
    $ pip install trafilatura[all] # all additional functionality

You can also install or update the packages separately, *trafilatura* will detect which ones are present on your system and opt for the best available combination.

*For infos on dependency management of Python packages see* `this discussion thread <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe>`_


Usage
-----

See `usage documentation <usage.html>`_.


License
-------

*trafilatura* is distributed under the `GNU General Public License v3.0 <https://github.com/adbar/htmldate/blob/master/LICENSE>`_

`GPL and free software licensing: What's in it for business? <https://www.techrepublic.com/blog/cio-insights/gpl-and-free-software-licensing-whats-in-it-for-business/>`_


Going further
-------------

*Trafilatura*: `Italian word <https://en.wiktionary.org/wiki/trafilatura>`_ for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_.

In order to gather web documents it can be useful to download the portions of a website programmatically, here is `how to use sitemaps to crawl websites <http://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.

Tutorial video in German by Simon Meier-Vieracker: `Content von Webseiten laden mit Trafilatura <https://www.youtube.com/watch?v=9RPrVE0hHgI>`_.

Tutorials in German by Noah Bubenhofer: `Download von Web-Daten <https://www.bubenhofer.com/korpuslinguistik/kurs/index.php?id=eigenes_wwwdownload.html>`_ & `Daten aufbereiten und verwalten <https://www.bubenhofer.com/korpuslinguistik/kurs/index.php?id=eigenes_aufbereitenXML.html>`_.


Roadmap
~~~~~~~

-  [-] Duplicate detection at sentence, paragraph and document level using a least recently used (LRU) cache
-  [-] XML output compatible with the recommendations of the `Text Encoding Initiative <https://tei-c.org/>`_
-  [-] Metadata integration
-  [-] Language detection on the extracted content
-  [-] Preservation of in-line text formatting (bold, italic, etc.)
-  [ ] Configuration and extraction parameters


Contributing
~~~~~~~~~~~~

`Contributions <https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ are welcome!

Feel free to file bug reports on the `issues page <https://github.com/adbar/htmldate/issues>`_.

Thanks to these contributors who submitted features and bugfixes:

-  `DerKozmonaut <https://github.com/DerKozmonaut>`_
-  `vbarbaresi <https://github.com/vbarbaresi>`_

Kudos to the following software libraries:

-  `lxml <http://lxml.de/>`_, `jusText <https://github.com/miso-belica/jusText>`_, `cchardet <https://github.com/PyYoshi/cChardet>`_


Author
------

This effort is part of methods to derive information from web documents in order to build text databases for research (chiefly linguistic analysis and natural language processing). A significant challenge resides in the ability to extract and pre-process web texts to meet scientific expectations: Web corpus construction involves numerous design decisions, and this software packages can help facilitate collection and enhance corpus quality.

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg
   :target: https://doi.org/10.5281/zenodo.3460969

-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://konvens.org/proceedings/2019/papers/kaleidoskop/camera_ready_barbaresi.pdf>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.

You can contact me via my `contact page <http://adrien.barbaresi.eu/contact.html>`_ or `GitHub <https://github.com/adbar>`_.


Further documentation
=====================

.. toctree::
   :maxdepth: 2
   
   corefunctions
   evaluation
   usage


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
