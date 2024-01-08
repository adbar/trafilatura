Trafilatura: Discover and Extract Text Data on the Web
======================================================


.. image:: docs/trafilatura-logo.png
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

.. image:: docs/trafilatura-demo.gif
    :alt: Demo as GIF image
    :align: center
    :width: 85%
    :target: https://trafilatura.readthedocs.org/


Introduction
------------


Trafilatura is a cutting-edge **Python package and command-line tool** designed to **gather text on the Web and simplify the process of turning raw HTML into structured, meaningful data**. It includes all necessary discovery and text processing components to perform **web crawling, downloads, scraping, and extraction** of main texts, metadata and comments. It aims at staying **handy and modular**: no database is required, the output can be converted to multiple commonly used formats.

Smart navigation and going from HTML bulk to essential parts can alleviate many problems related to text quality, first by **focusing on the actual content**, second by **avoiding the noise** caused by recurring elements (headers, footers etc.), and third by **making sense of the data** with information such as author and publication date. The extractor tries to strike a balance between limiting noise and including all valid parts. It also has to be **robust and reasonably fast** as it runs in production on millions of documents.

The tool's versatility makes it useful for a wide range of applications leveraging web content for knowledge discovery such as **quantitative and data-driven approaches**. It is relevant to anyone interested in language modeling, data mining, information extraction. Scraping-intensive use cases include search engine optimization, business analytics and information security. Trafilatura is used in the academic domain, chiefly for data acquisition in corpus linguistics, natural language processing, and computational social science.


Features
~~~~~~~~

- Advanced web crawling and text discovery:
   - Focused crawling adhering to politeness rules
   - Support for sitemaps (TXT, XML) and feeds (ATOM, JSON, RSS)
   - Smart navigation and URL management (blacklists, filtering and deduplication)
- Parallel processing of online and offline input:
   - Live URLs, efficient and polite processing of download queues
   - Previously downloaded HTML files and parsed HTML trees
- Robust and customizable extraction of key elements:
   - Main text (common patterns and generic algorithms like jusText and readability)
   - Metadata (title, author, date, site name, categories and tags)
   - Formatting and structure: paragraphs, titles, lists, quotes, code, line breaks, in-line text formatting
   - Optional elements: comments, links, images, tables
   - Extensive configuration options
- Multiple output formats:
   - Text (minimal formatting or Markdown)
   - CSV (with metadata, tab-separated values)
   - JSON (with metadata)
   - XML (with metadata, text formatting and page structure) and `TEI-XML <https://tei-c.org/>`_
- Add-ons:
   - Language detection on extracted content
   - Graphical user interface (GUI)
   - Speed optimizations
- Actively maintained with support from the open-source community:
   - Regular updates, feature additions, and optimizations
   - Comprehensive documentation


Evaluation and alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trafilatura consistently outperforms other open-source libraries in text extraction benchmarks, showcasing its efficiency and accuracy in extracting web content.

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

`Getting started with Trafilatura <https://trafilatura.readthedocs.io/en/latest/quickstart.html>`_ is straightforward. For more information and detailed guides, visit `Trafilatura's documentation <https://trafilatura.readthedocs.io/>`_:

- `Installation <https://trafilatura.readthedocs.io/en/latest/installation.html>`_
- Usage: `On the command-line <https://trafilatura.readthedocs.io/en/latest/usage-cli.html>`_, `With Python <https://trafilatura.readthedocs.io/en/latest/usage-python.html>`_, `With R <https://trafilatura.readthedocs.io/en/latest/usage-r.html>`_
- `Core Python functions <https://trafilatura.readthedocs.io/en/latest/corefunctions.html>`_
- Interactive Python Notebook: `Trafilatura Overview <docs/Trafilatura_Overview.ipynb>`_
- `Tutorials and use cases <https://trafilatura.readthedocs.io/en/latest/tutorials.html>`_
   - `Text embedding for vector search <https://trafilatura.readthedocs.io/en/latest/tutorial-epsilla.html>`_
   - `Custom web corpus <https://trafilatura.readthedocs.io/en/latest/tutorial0.html>`_
   - `Word frequency list <https://trafilatura.readthedocs.io/en/latest/tutorial1.html>`_

For video tutorials see this Youtube playlist:

- `Web scraping tutorials and how-tos <https://www.youtube.com/watch?v=8GkiOM17t0Q&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci>`_


License
-------

*Trafilatura* is distributed under the `GNU General Public License v3.0 <https://github.com/adbar/trafilatura/blob/master/LICENSE>`_. This license promotes collaboration in software development and ensures that Trafilatura's code remains publicly accessible.

If you wish to redistribute this library but are concerned about the license conditions, consider interacting `at arm's length <https://www.gnu.org/licenses/gpl-faq.html#GPLInProprietarySystem>`_, multi-licensing with `compatible licenses <https://en.wikipedia.org/wiki/GNU_General_Public_License#Compatibility_and_multi-licensing>`_, or `contacting the author <#author>`_ for more options.

For insights into GPL and free software licensing with emphasis on a business context, see `GPL and Free Software Licensing: What's in it for Business? <https://web.archive.org/web/20230127221311/https://www.techrepublic.com/article/gpl-and-free-software-licensing-whats-in-it-for-business/>`_


Contributing
------------

Contributions of all kinds are welcome. Visit the `Contributing page <https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ for more information. Bug reports can be filed on the `dedicated issue page <https://github.com/adbar/trafilatura/issues>`_.

Many thanks to the `contributors <https://github.com/adbar/trafilatura/graphs/contributors>`_ who extended the docs or submitted bug reports, features and bugfixes!


Context
-------

Developed with practical applications of academic research in mind, this software is part of a broader effort to derive information from web documents. Extracting and pre-processing web texts to the exacting standards of scientific research presents a substantial challenge. Web corpus construction involves numerous design decisions, this software package simplifies text data collection and enhances corpus quality. It is currently used to build `text databases for linguistic research <https://www.dwds.de/d/k-web>`_.

*Trafilatura* is an Italian word for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_ symbolizing the industrial-grade extraction, refinement and conversion process.


Author
~~~~~~

Reach out via the `contact page <https://adrien.barbaresi.eu/>`_ for inquiries, collaborations, or feedback. See also `Twitter/X <https://x.com/adbarbaresi>`_ for the latest updates.

This work started as a PhD project at the crossroads of linguistics and NLP, this expertise has been instrumental in shaping Trafilatura over the years. It has first been released under its current form in 2019, its development is referenced in the following publications:

- Barbaresi, A. `Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction <https://aclanthology.org/2021.acl-demo.15/>`_, Proceedings of ACL/IJCNLP 2021: System Demonstrations, 2021, p. 122-131.
-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://hal.archives-ouvertes.fr/hal-02447264/document>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.


Citing Trafilatura
~~~~~~~~~~~~~~~~~~


If you use Trafilatura in your research or projects, we kindly ask you to cite this work, here is how:

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

This software is part of a larger ecosystem. It is employed in a variety of academic and development projects, demonstrating its versatility and effectiveness. Case studies and publications are listed on the `Used By documentation page <https://trafilatura.readthedocs.io/en/latest/used-by.html>`_.

Jointly developed plugins and additional packages also contribute to the field of web data extraction and analysis:


.. image:: docs/software-ecosystem.png
    :alt: Software ecosystem
    :align: center
    :width: 65%



Corresponding posts can be found on `Bits of Language <https://adrien.barbaresi.eu/blog/tag/trafilatura.html>`_. The blog covers a range of topics from technical how-tos, updates on new features, to discussions on text mining challenges and solutions.

Impressive, you have reached the end of the page: Thank you for your interest!
