A Python package & command-line tool to gather text on the Web
==============================================================


.. image:: docs/trafilatura-logo.png
    :alt: Logo as PNG image
    :align: center
    :width: 60%

|

.. image:: https://img.shields.io/pypi/v/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python package

.. image:: https://img.shields.io/pypi/pyversions/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python versions

.. image:: https://readthedocs.org/projects/trafilatura/badge/?version=latest
    :target: http://trafilatura.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/codecov/c/github/adbar/trafilatura.svg
    :target: https://codecov.io/gh/adbar/trafilatura
    :alt: Code Coverage

.. image:: https://static.pepy.tech/badge/trafilatura/month
    :target: https://pepy.tech/project/trafilatura
    :alt: Downloads

.. image:: https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue
    :target: https://aclanthology.org/2021.acl-demo.15/
    :alt: Reference DOI: 10.18653/v1/2021.acl-demo.15


|

.. image:: docs/trafilatura-demo.gif
    :alt: Demo as GIF image
    :align: center
    :width: 85%
    :target: https://trafilatura.readthedocs.org/


Description
-----------

Trafilatura is a **Python package and command-line tool** designed gather text on the Web. It includes discovery, extraction and text processing components. Its main applications are **web crawling, downloads, scraping, and extraction** of main texts, comments and metadata. It aims at staying **handy and modular**: no database is required, the output can be converted to various commonly used formats.

Going from raw HTML to essential parts can alleviate many problems related to text quality, first by avoiding the **noise caused by recurring elements** (headers, footers, links/blogroll etc.) and second by including information such as author and date in order to **make sense of the data**. The extractor tries to strike a balance between limiting noise (precision) and including all valid parts (recall). It also has to be **robust and reasonably fast**, it runs in production on millions of documents.

This tool can be **useful for quantitative research** in corpus linguistics, natural language processing, computational social science and beyond: it is also relevant to anyone interested in data science, information extraction, text mining, and in scraping-intensive use cases like search engine optimization, business analytics or information security.


Features
~~~~~~~~

- Seamless and parallel online/offline processing:
   - Download and conversion utilities included
   - URLs, HTML files or parsed HTML trees as input
- Robust and efficient extraction:
   - Main text (with LXML, common patterns and generic algorithms: jusText, fork of readability-lxml)
   - Metadata (title, author, date, site name, categories and tags)
   - Formatting and structural elements: paragraphs, titles, lists, quotes, code, line breaks, in-line text formatting
   - Comments (if applicable)
- Output formats:
   - Text (minimal formatting or Markdown)
   - CSV (with metadata, `tab-separated values <https://en.wikipedia.org/wiki/Tab-separated_values>`_)
   - JSON (with metadata)
   - XML (with metadata, text formatting and page structure) and `TEI-XML <https://tei-c.org/>`_
- Link discovery and URL management:
   - Focused crawling and politeness rules
   - Support for sitemaps (TXT, XML) and feeds (ATOM, JSON, RSS)
   - Efficient and polite processing of URL queues
   - Blacklisting
- Optional add-ons:
   - Language detection on extracted content
   - Graphical user interface (GUI)


Evaluation and alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For more detailed results see the `benchmark <https://trafilatura.readthedocs.io/en/latest/evaluation.html>`_ and `evaluation script <https://github.com/adbar/trafilatura/blob/master/tests/comparison.py>`_. To reproduce the tests just clone the repository, install all necessary packages and run the evaluation script with the data provided in the *tests* directory.

=============================== =========  ========== ========= ========= ======
750 documents, 2236 text & 2250 boilerplate segments (2022-05-18), Python 3.8
--------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Diff.
=============================== =========  ========== ========= ========= ======
html_text 0.5.2                 0.529      **0.958**  0.554     0.682     2.2x
inscriptis 2.2.0 (html to txt)  0.534      **0.959**  0.563     0.686     3.5x
newspaper3k 0.2.8               0.895      0.593      0.762     0.713     12x
justext 3.0.0 (custom)          0.865      0.650      0.775     0.742     5.2x
boilerpy3 1.0.6 (article mode)  0.814      0.744      0.787     0.777     4.1x
*baseline (text markup)*        0.757      0.827      0.781     0.790     **1x**
goose3 3.1.9                    **0.934**  0.690      0.821     0.793     22x
readability-lxml 0.8.1          0.891      0.729      0.820     0.801     5.8x
news-please 1.5.22              0.898      0.734      0.826     0.808     61x
readabilipy 0.2.0               0.877      0.870      0.874     0.874     248x
trafilatura 1.2.2 (standard)    0.914      0.904      **0.910** **0.909** 7.1x
=============================== =========  ========== ========= ========= ======

Other evaluations:
^^^^^^^^^^^^^^^^^^

- Most efficient open-source library in *ScrapingHub*'s `article extraction benchmark <https://github.com/scrapinghub/article-extraction-benchmark>`_
- Best overall tool according to Gaël Lejeune & Adrien Barbaresi, `Bien choisir son outil d'extraction de contenu à partir du Web <https://hal.archives-ouvertes.fr/hal-02768510v3/document>`_ (2020, PDF, French)


Usage and documentation
-----------------------

For more information please refer to `the documentation <https://trafilatura.readthedocs.io/>`_:

- `Installation <https://trafilatura.readthedocs.io/en/latest/installation.html>`_
- Usage: `On the command-line <https://trafilatura.readthedocs.io/en/latest/usage-cli.html>`_, `With Python <https://trafilatura.readthedocs.io/en/latest/usage-python.html>`_, `With R <https://trafilatura.readthedocs.io/en/latest/usage-r.html>`_
- `Core Python functions <https://trafilatura.readthedocs.io/en/latest/corefunctions.html>`_
- Python Notebook `Trafilatura Overview <docs/Trafilatura_Overview.ipynb>`_
- `Tutorials <https://trafilatura.readthedocs.io/en/latest/tutorials.html>`_

For video tutorials see this Youtube playlist:

- `Web scraping how-tos and tutorials <https://www.youtube.com/watch?v=8GkiOM17t0Q&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci>`_


License
-------

*Trafilatura* is distributed under the `GNU General Public License v3.0 <https://github.com/adbar/trafilatura/blob/master/LICENSE>`_. If you wish to redistribute this library but feel bounded by the license conditions please try interacting `at arms length <https://www.gnu.org/licenses/gpl-faq.html#GPLInProprietarySystem>`_, `multi-licensing <https://en.wikipedia.org/wiki/Multi-licensing>`_ with `compatible licenses <https://en.wikipedia.org/wiki/GNU_General_Public_License#Compatibility_and_multi-licensing>`_, or `contacting me <https://github.com/adbar/trafilatura#author>`_.

See also `GPL and free software licensing: What's in it for business? <https://www.techrepublic.com/blog/cio-insights/gpl-and-free-software-licensing-whats-in-it-for-business/>`_



Context
-------


Contributing
~~~~~~~~~~~~

Contributions are welcome! See `CONTRIBUTING.md <https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ for more information. Bug reports can be filed on the `dedicated page <https://github.com/adbar/trafilatura/issues>`_.

Many thanks to the `contributors <https://github.com/adbar/trafilatura/graphs/contributors>`_ who submitted features and bugfixes!


Roadmap
~~~~~~~

For planned enhancements and relevant milestones see `issues page <https://github.com/adbar/trafilatura/milestones>`_.


Author
~~~~~~

This effort is part of methods to derive information from web documents in order to build `text databases for research <https://www.dwds.de/d/k-web>`_ (chiefly linguistic analysis and natural language processing). Extracting and pre-processing web texts to the exacting standards of scientific research presents a substantial challenge for those who conduct such research. Web corpus construction involves numerous design decisions, and this software package can help facilitate text data collection and enhance corpus quality.


- Barbaresi, A. `Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction <https://aclanthology.org/2021.acl-demo.15/>`_, Proceedings of ACL/IJCNLP 2021: System Demonstrations, 2021, p. 122-131.
-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://hal.archives-ouvertes.fr/hal-02447264/document>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.


.. image:: https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue
    :target: https://aclanthology.org/2021.acl-demo.15/
    :alt: Reference DOI: 10.18653/v1/2021.acl-demo.15

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg
   :target: https://doi.org/10.5281/zenodo.3460969
   :alt: Zenodo archive DOI: 10.5281/zenodo.3460969


.. code-block:: shell

    @inproceedings{barbaresi-2021-trafilatura,
      title = {{Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction}},
      author = "Barbaresi, Adrien",
      booktitle = "Proceedings of the Joint Conference of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
      pages = "122--131",
      publisher = "Association for Computational Linguistics",
      url = "https://aclanthology.org/2021.acl-demo.15",
      year = 2021,
    }


You can contact me via my `contact page <https://adrien.barbaresi.eu/>`_ or on `GitHub <https://github.com/adbar>`_.


Software ecosystem
~~~~~~~~~~~~~~~~~~


.. image:: docs/software-ecosystem.png
    :alt: Software ecosystem 
    :align: center
    :width: 65%


*Trafilatura*: `Italian word <https://en.wiktionary.org/wiki/trafilatura>`_ for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_.

`Known uses of the software <https://trafilatura.readthedocs.io/en/latest/used-by.html>`_.

Corresponding posts on `Bits of Language <https://adrien.barbaresi.eu/blog/tag/trafilatura.html>`_ (blog).
