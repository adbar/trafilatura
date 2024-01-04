Trafilatura: A one-stop shop to gather text on the Web
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

Trafilatura is a cutting-edge **Python package and command-line tool** designed to gather text on the Web. It offers a comprehensive solution for extracting text, metadata, and comments from web pages, making it an indispensable tool for researchers, developers, data scientists, and anyone involved in web scraping, data mining, and content analysis.

designed to gather text on the Web. It includes discovery, extraction and text processing components. Its main applications are **web crawling, downloads, scraping, and extraction** of main texts, metadata and comments. It aims at staying **handy and modular**: no database is required, the output can be converted to various commonly used formats.


Trafilatura is not just a tool; it's a comprehensive ecosystem designed for the modern web. It goes beyond traditional scraping methods to offer a nuanced approach to data extraction. With its advanced algorithms and modular design, Trafilatura simplifies the process of turning raw HTML into structured, meaningful data. It's built to handle the complexities of today's web, including dynamic content, various data formats, and multilingual text.

Going from raw HTML to essential parts can alleviate many problems related to text quality, first by avoiding the **noise caused by recurring elements** (headers, footers, links/blogroll etc.) and second by including information such as author and date in order to **make sense of the data**. The extractor tries to strike a balance between limiting noise (precision) and including all valid parts (recall). It also has to be **robust and reasonably fast**, it runs in production on millions of documents.


The tool's versatility makes it ideal for a wide range of applications, from academic research in linguistics and social sciences to practical uses in SEO, business analytics, and cybersecurity. Trafilatura is more than a scraper; it's a gateway to understanding and leveraging web content for knowledge discovery and data-driven insights.

This tool can be **useful for quantitative research** in corpus linguistics, natural language processing, computational social science and beyond: it is relevant to anyone interested in data science, information extraction, text mining, and scraping-intensive use cases like search engine optimization, business analytics or information security.




Features
~~~~~~~~

Trafilatura comes packed with a plethora of features, each designed to tackle specific challenges in web data extraction:

- **Advanced Web Crawling**: Dive deep into the web with sophisticated crawling techniques. Trafilatura supports focused crawling, adhering to politeness rules, and efficiently navigates through sitemaps and feeds (including ATOM, JSON, and RSS formats).

- **Seamless Online and Offline Processing**: Whether you're working with live URLs or offline HTML files, Trafilatura handles it all. Its parallel processing capabilities ensure efficient queue management and data conversion.

- **Robust Text and Metadata Extraction**: At its core, Trafilatura excels in extracting main text and metadata. Leveraging LXML and a blend of common patterns and algorithms (like jusText and a fork of readability-lxml), it achieves a fine balance between precision and recall.

- **Rich Output Formats**: Catering to diverse needs, Trafilatura supports multiple output formats. Choose from plain text, Markdown, CSV (with metadata), JSON, XML (including text formatting and page structure), and TEI-XML for scholarly needs.

- **Language Detection**: Trafilatura automatically detects the language of extracted content, adding an extra layer of intelligence to your data processing workflow.

- **Graphical User Interface (GUI)**: For those who prefer a visual approach, Trafilatura offers a user-friendly GUI, making web scraping accessible to everyone.

- **Performance Optimizations**: Speed is of the essence. Trafilatura is optimized for performance, ensuring quick and efficient processing even for large-scale data extraction tasks.

- **Customizability and Extensibility**: Tailor Trafilatura to your needs. Its modular design and extensive configuration options allow for customization and extensibility.

- **Community-Driven Development**: Trafilatura thrives on community input. Regular updates, feature additions, and optimizations are driven by user feedback and contributions.

- **Comprehensive Documentation and Support**: Get started quickly and dive deep into advanced features with our extensive documentation. The community and developers are always ready to provide support and guidance.


- Web crawling and text discovery:
   - Focused crawling and politeness rules
   - Support for sitemaps (TXT, XML) and feeds (ATOM, JSON, RSS)
   - URL management (blacklists, filtering and de-duplication)
- Seamless and parallel processing, online and offline:
   - URLs, HTML files or parsed HTML trees usable as input
   - Efficient and polite processing of download queues
   - Conversion of previously downloaded files
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
- Optional add-ons:
   - Language detection on extracted content
   - Graphical user interface (GUI)
   - Speed optimizations


Evaluation and alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trafilatura consistently outperforms other open-source libraries in benchmarks, showcasing its efficiency and accuracy in extracting web content.

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
- `Key Python functions <https://trafilatura.readthedocs.io/en/latest/corefunctions.html>`_
- Interactive Python Notebook: `Trafilatura Overview <docs/Trafilatura_Overview.ipynb>`_
- `Tutorials and use cases <https://trafilatura.readthedocs.io/en/latest/tutorials.html>`_
   - `Text embedding for vector search <https://trafilatura.readthedocs.io/en/latest/tutorial-epsilla.html>`_
   - `Custom web corpus <https://trafilatura.readthedocs.io/en/latest/tutorial0.html>`_
   - `Word frequency list <https://trafilatura.readthedocs.io/en/latest/tutorial1.html>`_
- `YouTube playlist of web scraping tutorials and how-tos <https://www.youtube.com/watch?v=8GkiOM17t0Q&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci>`_


License
-------

*Trafilatura* is distributed under the `GNU General Public License v3.0 <https://github.com/adbar/trafilatura/blob/master/LICENSE>`_. This license promotes collaboration in software development, ensuring that Trafilatura remains an accessible tool.

If you wish to redistribute this library but are concerned about the license conditions, consider interacting `at arm's length <https://www.gnu.org/licenses/gpl-faq.html#GPLInProprietarySystem>`_, `multi-licensing <https://en.wikipedia.org/wiki/Multi-licensing>`_ with `compatible licenses <https://en.wikipedia.org/wiki/GNU_General_Public_License#Compatibility_and_multi-licensing>`_, or `contacting the author <https://github.com/adbar/trafilatura#author>`_ for more options.

For insights into GPL and free software licensing, especially in a business context, see [GPL and Free Software Licensing: What's in it for Business?](https://web.archive.org/web/20230127221311/https://www.techrepublic.com/article/gpl-and-free-software-licensing-whats-in-it-for-business/)


Context
-------

This effort is part of a broader effort to derive information from web documents. Extracting and pre-processing web texts to the exacting standards of scientific research presents a substantial challenge. Web corpus construction involves numerous design decisions, and this software package can help facilitate text data collection and enhance corpus quality.

Developed with scientific research and practical applications in mind, it addresses the challenges faced in web corpus construction and data analysis. Whether it's for linguistic analysis, natural language processing, social science research, or practical applications like SEO and business analytics, Trafilatura provides the means to extract and process web data effectively.


Contributing
~~~~~~~~~~~~

Contributions are welcome! See `CONTRIBUTING.md <https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ for more information. Bug reports can be filed on the `dedicated page <https://github.com/adbar/trafilatura/issues>`_.

Many thanks to the `contributors <https://github.com/adbar/trafilatura/graphs/contributors>`_ who submitted features and bugfixes!


Your contributions are what make Trafilatura a robust and versatile tool. We welcome contributions of all kinds, from code to documentation:

- **Code Contributions**: Enhance Trafilatura by contributing code. Whether it's bug fixes, new features, or performance improvements, your code makes a difference.

- **Documentation**: Help us improve our documentation. Write tutorials, guides, or translate existing content to make Trafilatura more accessible.

- **Feedback and Suggestions**: Share your feedback and suggestions. Your insights are valuable in shaping the future of Trafilatura.

- **Community Engagement**: Be part of our community. Participate in discussions, share your use cases, and help others get the most out of Trafilatura.

Visit our [Contributing Guide](https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md) for more information on how you can contribute.


Your contributions make Trafilatura better. We encourage community involvement and welcome contributions of all forms:

- **Bug Reports and Feature Requests**: Encountered an issue or have an idea for a new feature? File a bug report or feature request on our [GitHub Issues page](https://github.com/adbar/trafilatura/issues).

- **Code Contributions**: Interested in contributing code? Whether it's fixing bugs, adding new features, or improving documentation, your code contributions are invaluable. Check out our [Contributing Guide](https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md) for guidelines on how to contribute.

- **Community Support and Discussion**: Join the conversation and connect with other users and contributors. Engage with the community on [Twitter](https://twitter.com/adbarbaresi), participate in discussions, and share your experiences and insights.

- **Documentation and Tutorials**: Help improve our documentation by writing guides, tutorials, or translating existing content. Good documentation is key to making the tool accessible to a wider audience.

A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in developing and enhancing Trafilatura.



Roadmap
~~~~~~~

Trafilatura is continuously evolving, with development guided by user needs and technological advancements. Our roadmap outlines planned enhancements, new features, and milestones:

- **Upcoming Features**: Stay tuned for upcoming features that will further enhance Trafilatura's capabilities. We're constantly working on adding new functionalities and optimizations.

- **Community Feedback and Requests**: User feedback is a driving force behind our development process. We prioritize features and improvements based on community input and requests.

- **Long-Term Goals**: Our long-term vision for Trafilatura includes expanding its applications, improving performance, and ensuring it remains at the forefront of web data extraction technology.

For detailed information on upcoming enhancements and milestones, visit our [Issues Page](https://github.com/adbar/trafilatura/milestones).


Author
~~~~~~

This work started as a PhD project at the crossroads of linguistics, natural language processing, and data science. This expertise has been instrumental in shaping Trafilatura over the years. It has first been released as an open-source package in 2019. It is currently used to build `text databases for research <https://www.dwds.de/d/k-web>`_ (chiefly linguistic analysis and natural language processing). For more about Adrien Barbaresi's work and contributions:

- Barbaresi, A. `Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction <https://aclanthology.org/2021.acl-demo.15/>`_, Proceedings of ACL/IJCNLP 2021: System Demonstrations, 2021, p. 122-131.
-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://hal.archives-ouvertes.fr/hal-02447264/document>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.


.. image:: https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue
    :target: https://aclanthology.org/2021.acl-demo.15/
    :alt: Reference DOI: 10.18653/v1/2021.acl-demo.15

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg
   :target: https://doi.org/10.5281/zenodo.3460969
   :alt: Zenodo archive DOI: 10.5281/zenodo.3460969



Citing Trafilatura
~~~~~~~~~~~~~~~~~~

If you use Trafilatura in your research or projects, we kindly ask you to cite our work. This helps us to continue developing and improving the tool. Here's how you can cite Trafilatura:

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


Contact and Community
~~~~~~~~~~~~~~~~~~~~~

We believe in the power of community and collaboration. Whether you have questions, suggestions, or just want to discuss web scraping and data extraction, we're here for you:

- **Contact the Author**: Reach out via the `contact page <https://adrien.barbaresi.eu/>`_ for inquiries, collaborations, or feedback.

- **GitHub Community**: Engage with the Trafilatura community on GitHub. Share your experiences, contribute to discussions, and collaborate on new features.

- **Social Media**: Follow us on `Twitter <https://twitter.com/adbarbaresi>`_ for the latest updates, tips, and community highlights.

- **Issue Tracker**: Encounter a bug or have a feature request? File it on our [GitHub Issues page](https://github.com/adbar/trafilatura/issues).


Corresponding posts can be found on the `Bits of Language <https://adrien.barbaresi.eu/blog/tag/trafilatura.html>`_ blog.

Stay updated with the latest developments, tutorials, and insights related to Trafilatura through our blog, `Bits of Language`. The blog covers a range of topics from technical how-tos, updates on new features, to discussions on web scraping challenges and solutions.


Software ecosystem
~~~~~~~~~~~~~~~~~~

This software is part of a larger ecosystem of tools and libraries, each contributing to the field of web data extraction and analysis. This ecosystem includes complementary plugins and advanced functionalities.

*Trafilatura* is an Italian word for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_, symbolizing the industrial-grade extraction, refinement and conversion process.


.. image:: docs/software-ecosystem.png
    :alt: Software ecosystem
    :align: center
    :width: 65%


The package is also employed in a variety of contexts and projects, demonstrating its versatility and effectiveness. Case studies and publications are listed on the `Used By page <https://trafilatura.readthedocs.io/en/latest/used-by.html>`_.

Thank you for choosing Trafilatura!
