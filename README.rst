Trafilatura: Discover and Extract Text Data on the Web
======================================================


.. image:: https://raw.githubusercontent.com/adbar/trafilatura/master/docs/trafilatura-logo.png
   :alt: Trafilatura Logo
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

.. image:: https://raw.githubusercontent.com/adbar/trafilatura/master/docs/trafilatura-demo.gif
    :alt: Demo as GIF image
    :align: center
    :width: 85%
    :target: https://trafilatura.readthedocs.org/


Introduction
------------


Trafilatura is a cutting-edge **Python package and command-line tool** designed to **gather text on the Web and simplify the process of turning raw HTML into structured, meaningful data**. It includes all necessary discovery and text processing components to perform **web crawling, downloads, scraping, and extraction** of main texts, metadata and comments. It aims at staying **handy and modular**: no database is required, the output can be converted to commonly used formats.

Going from HTML bulk to essential parts can alleviate many problems related to text quality, by **focusing on the actual content**, **avoiding the noise** caused by recurring elements (headers, footers etc.), and **making sense of the data** with selected information. The extractor is designed to be **robust and reasonably fast**, it runs in production on millions of documents.

The tool's versatility makes it **useful for quantitative and data-driven approaches**. It is used in the academic domain and beyond (e.g. in natural language processing, computational social science, search engine optimization, and information security).


Features
~~~~~~~~

- Advanced web crawling and text discovery:
   - Support for sitemaps (TXT, XML) and feeds (ATOM, JSON, RSS)
   - Smart crawling and URL management (filtering and deduplication)
- Parallel processing of online and offline input:
   - Live URLs, efficient and polite processing of download queues
   - Previously downloaded HTML files and parsed HTML trees
- Robust and configurable extraction of key elements:
   - Main text (common patterns and generic algorithms like jusText and readability)
   - Metadata (title, author, date, site name, categories and tags)
   - Formatting and structure: paragraphs, titles, lists, quotes, code, line breaks, in-line text formatting
   - Optional elements: comments, links, images, tables
- Multiple output formats:
   - Text (minimal formatting or Markdown)
   - CSV (with metadata)
   - JSON (with metadata)
   - XML or `XML-TEI <https://tei-c.org/>`_ (with metadata, text formatting and page structure)
- Optional add-ons:
   - Language detection on extracted content
   - Graphical user interface (GUI)
   - Speed optimizations
- Actively maintained with support from the open-source community:
   - Regular updates, feature additions, and optimizations
   - Comprehensive documentation


Evaluation and alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trafilatura consistently outperforms other open-source libraries in text extraction benchmarks, showcasing its efficiency and accuracy in extracting web content. The extractor tries to strike a balance between limiting noise and including all valid parts.

For more information see the `benchmark section <https://trafilatura.readthedocs.io/en/latest/evaluation.html>`_ and the `evaluation readme <https://github.com/adbar/trafilatura/blob/master/tests/README.rst>`_ to reproduce the results.


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
- Best overall tool according to `Bien choisir son outil d'extraction de contenu à partir du Web <https://hal.archives-ouvertes.fr/hal-02768510v3/document>`_ (Lejeune & Barbaresi 2020)
- Best single tool by ROUGE-LSum Mean F1 Page Scores in `An Empirical Comparison of Web Content Extraction Algorithms <https://webis.de/downloads/publications/papers/bevendorff_2023b.pdf>`_ (Bevendorff et al. 2023)


Usage and documentation
-----------------------

`Getting started with Trafilatura <https://trafilatura.readthedocs.io/en/latest/quickstart.html>`_ is straightforward. For more information and detailed guides, visit `Trafilatura's documentation <https://trafilatura.readthedocs.io/>`_:

- `Installation <https://trafilatura.readthedocs.io/en/latest/installation.html>`_
- Usage: `On the command-line <https://trafilatura.readthedocs.io/en/latest/usage-cli.html>`_, `With Python <https://trafilatura.readthedocs.io/en/latest/usage-python.html>`_, `With R <https://trafilatura.readthedocs.io/en/latest/usage-r.html>`_
- `Core Python functions <https://trafilatura.readthedocs.io/en/latest/corefunctions.html>`_
- Interactive Python Notebook: `Trafilatura Overview <docs/Trafilatura_Overview.ipynb>`_
- `Tutorials and use cases <https://trafilatura.readthedocs.io/en/latest/tutorials.html>`_


Youtube playlist with video tutorials in several languages:

- `Web scraping tutorials and how-tos <https://www.youtube.com/watch?v=8GkiOM17t0Q&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci>`_


License
-------

This package is distributed under the `Apache 2.0 license <https://www.apache.org/licenses/LICENSE-2.0.html>`_.

Versions prior to v1.8.0 are under GPLv3+ license.


Contributing
------------

Contributions of all kinds are welcome. Visit the `Contributing page <https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ for more information. Bug reports can be filed on the `dedicated issue page <https://github.com/adbar/trafilatura/issues>`_.

Many thanks to the `contributors <https://github.com/adbar/trafilatura/graphs/contributors>`_ who extended the docs or submitted bug reports, features and bugfixes!


Context
-------

Developed with practical applications of academic research in mind, this software is part of a broader effort to derive information from web documents. Extracting and pre-processing web texts to the exacting standards of scientific research presents a substantial challenge. This software package simplifies text data collection and enhances corpus quality, it is currently used to build `text databases for linguistic research <https://www.dwds.de/d/k-web>`_.

*Trafilatura* is an Italian word for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_ symbolizing the refinement and conversion process. It is also the way shapes of pasta are formed.


Author
~~~~~~

Reach out via ia the software repository or the `contact page <https://adrien.barbaresi.eu/>`_ for inquiries, collaborations, or feedback. See also X or LinkedIn for the latest updates.

This work started as a PhD project at the crossroads of linguistics and NLP, this expertise has been instrumental in shaping Trafilatura over the years. It has first been released under its current form in 2019, its development is referenced in the following publications:

- Barbaresi, A. `Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction <https://aclanthology.org/2021.acl-demo.15/>`_, Proceedings of ACL/IJCNLP 2021: System Demonstrations, 2021, p. 122-131.
-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://hal.archives-ouvertes.fr/hal-02447264/document>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.


Citing Trafilatura
~~~~~~~~~~~~~~~~~~

Trafilatura is widely used in the academic domain, chiefly for data acquisition. Here is how to cite it:

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


Software ecosystem
~~~~~~~~~~~~~~~~~~

Case studies and publications are listed on the `Used By documentation page <https://trafilatura.readthedocs.io/en/latest/used-by.html>`_.

Jointly developed plugins and additional packages also contribute to the field of web data extraction and analysis:


.. image:: https://raw.githubusercontent.com/adbar/htmldate/master/docs/software-ecosystem.png
    :alt: Software ecosystem
    :align: center
    :width: 65%



Corresponding posts can be found on `Bits of Language <https://adrien.barbaresi.eu/blog/tag/trafilatura.html>`_. The blog covers a range of topics from technical how-tos, updates on new features, to discussions on text mining challenges and solutions.

Impressive, you have reached the end of the page: Thank you for your interest!
