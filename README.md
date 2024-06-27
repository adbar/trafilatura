# Trafilatura: Discover and Extract Text Data on the Web

<br/>

<img alt="Trafilatura Logo" src="https://raw.githubusercontent.com/adbar/trafilatura/master/docs/trafilatura-logo.png" align="center" width="60%"/>

<br/>

[![Python package](https://img.shields.io/pypi/v/trafilatura.svg)](https://pypi.python.org/pypi/trafilatura)
[![Python versions](https://img.shields.io/pypi/pyversions/trafilatura.svg)](https://pypi.python.org/pypi/trafilatura)
[![Documentation Status](https://readthedocs.org/projects/trafilatura/badge/?version=latest)](http://trafilatura.readthedocs.org/en/latest/?badge=latest)
[![Code Coverage](https://img.shields.io/codecov/c/github/adbar/trafilatura.svg)](https://codecov.io/gh/adbar/trafilatura)
[![Downloads](https://static.pepy.tech/badge/trafilatura/month)](https://pepy.tech/project/trafilatura)
[![Reference DOI: 10.18653/v1/2021.acl-demo.15](https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue)](https://aclanthology.org/2021.acl-demo.15/)

<br/>

<img alt="Demo as GIF image" src="https://raw.githubusercontent.com/adbar/trafilatura/master/docs/trafilatura-demo.gif" align="center" width="80%"/>

<br/>


## Introduction

Trafilatura is a cutting-edge **Python package and command-line tool**
designed to **gather text on the Web and simplify the process of turning
raw HTML into structured, meaningful data**. It includes all necessary
discovery and text processing components to perform **web crawling,
downloads, scraping, and extraction** of main texts, metadata and
comments. It aims at staying **handy and modular**: no database is
required, the output can be converted to commonly used formats.

Going from HTML bulk to essential parts can alleviate many problems
related to text quality, by **focusing on the actual content**,
**avoiding the noise** caused by recurring elements (headers, footers
etc.), and **making sense of the data** with selected information. The
extractor is designed to be **robust and reasonably fast**, it runs in
production on millions of documents.

The tool's versatility makes it **useful for quantitative and
data-driven approaches**. It is used in the academic domain and beyond
(e.g. in natural language processing, computational social science,
search engine optimization, and information security).


### Features

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
   - TXT and Markdown
   - CSV
   - JSON
   - HTML, XML and [XML-TEI](https://tei-c.org/)

- Optional add-ons:
   - Language detection on extracted content
   - Graphical user interface (GUI)
   - Speed optimizations

- Actively maintained with support from the open-source community:
   - Regular updates, feature additions, and optimizations
   - Comprehensive documentation


### Evaluation and alternatives

Trafilatura consistently outperforms other open-source libraries in text
extraction benchmarks, showcasing its efficiency and accuracy in
extracting web content. The extractor tries to strike a balance between
limiting noise and including all valid parts.

For more information see the [benchmark section](https://trafilatura.readthedocs.io/en/latest/evaluation.html)
and the [evaluation readme](https://github.com/adbar/trafilatura/blob/master/tests/README.rst)
to run the evaluation with the latest data and packages.

**750 documents, 2236 text & 2250 boilerplate segments (2022-05-18), Python 3.8**

| Python Package | Precision | Recall | Accuracy | F-Score | Diff. |
|----------------|-----------|--------|----------|---------|-------|
| html_text 0.5.2 | 0.529 | **0.958** | 0.554 | 0.682 | 2.2x |
| inscriptis 2.2.0 (html to txt) | 0.534 | **0.959** | 0.563 | 0.686 | 3.5x |
| newspaper3k 0.2.8 | 0.895 | 0.593 | 0.762 | 0.713 | 12x |
| justext 3.0.0 (custom) | 0.865 | 0.650 | 0.775 | 0.742 | 5.2x |
| boilerpy3 1.0.6 (article mode) | 0.814 | 0.744 | 0.787 | 0.777 | 4.1x |
| *baseline (text markup)* | 0.757 | 0.827 | 0.781 | 0.790 | **1x** |
| goose3 3.1.9 | **0.934** | 0.690 | 0.821 | 0.793 | 22x |
| readability-lxml 0.8.1 | 0.891 | 0.729 | 0.820 | 0.801 | 5.8x |
| news-please 1.5.22 | 0.898 | 0.734 | 0.826 | 0.808 | 61x |
| readabilipy 0.2.0 | 0.877 | 0.870 | 0.874 | 0.874 | 248x |
| trafilatura 1.2.2 (standard) | 0.914 | 0.904 | **0.910** | **0.909** | 7.1x |


#### Other evaluations:

- Most efficient open-source library in *ScrapingHub*'s [article extraction benchmark](https://github.com/scrapinghub/article-extraction-benchmark)
- Best overall tool according to [Bien choisir son outil d'extraction de contenu à partir du Web](https://hal.archives-ouvertes.fr/hal-02768510v3/document)
  (Lejeune & Barbaresi 2020)
- Best single tool by ROUGE-LSum Mean F1 Page Scores in [An Empirical Comparison of Web Content Extraction Algorithms](https://webis.de/downloads/publications/papers/bevendorff_2023b.pdf)
  (Bevendorff et al. 2023)


## Usage and documentation

[Getting started with Trafilatura](https://trafilatura.readthedocs.io/en/latest/quickstart.html)
is straightforward. For more information and detailed guides, visit
[Trafilatura's documentation](https://trafilatura.readthedocs.io/):

- [Installation](https://trafilatura.readthedocs.io/en/latest/installation.html)
- Usage:
  [On the command-line](https://trafilatura.readthedocs.io/en/latest/usage-cli.html),
  [With Python](https://trafilatura.readthedocs.io/en/latest/usage-python.html),
  [With R](https://trafilatura.readthedocs.io/en/latest/usage-r.html)
- [Core Python functions](https://trafilatura.readthedocs.io/en/latest/corefunctions.html)
- Interactive Python Notebook: [Trafilatura Overview](docs/Trafilatura_Overview.ipynb)
- [Tutorials and use cases](https://trafilatura.readthedocs.io/en/latest/tutorials.html)

Youtube playlist with video tutorials in several languages:

- [Web scraping tutorials and how-tos](https://www.youtube.com/watch?v=8GkiOM17t0Q&list=PL-pKWbySIRGMgxXQOtGIz1-nbfYLvqrci)


## License

This package is distributed under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).

Versions prior to v1.8.0 are under GPLv3+ license.


## Contributing

Contributions of all kinds are welcome. Visit the [Contributing
page](https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md)
for more information. Bug reports can be filed on the [dedicated issue
page](https://github.com/adbar/trafilatura/issues).

Many thanks to the
[contributors](https://github.com/adbar/trafilatura/graphs/contributors)
who extended the docs or submitted bug reports, features and bugfixes!


## Context

Developed with practical applications of academic research in mind, this
software is part of a broader effort to derive information from web
documents. Extracting and pre-processing web texts to the exacting
standards of scientific research presents a substantial challenge. This
software package simplifies text data collection and enhances corpus
quality, it is currently used to build [text databases for linguistic
research](https://www.dwds.de/d/k-web).

*Trafilatura* is an Italian word for [wire
drawing](https://en.wikipedia.org/wiki/Wire_drawing) symbolizing the
refinement and conversion process. It is also the way shapes of pasta
are formed.

### Author

Reach out via ia the software repository or the [contact
page](https://adrien.barbaresi.eu/) for inquiries, collaborations, or
feedback. See also X or LinkedIn for the latest updates.

This work started as a PhD project at the crossroads of linguistics and
NLP, this expertise has been instrumental in shaping Trafilatura over
the years. It has first been released under its current form in 2019,
its development is referenced in the following publications:

-   Barbaresi, A. [Trafilatura: A Web Scraping Library and Command-Line
    Tool for Text Discovery and
    Extraction](https://aclanthology.org/2021.acl-demo.15/), Proceedings
    of ACL/IJCNLP 2021: System Demonstrations, 2021, p. 122-131.
-   Barbaresi, A. "[Generic Web Content Extraction with Open-Source
    Software](https://hal.archives-ouvertes.fr/hal-02447264/document)",
    Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
-   Barbaresi, A. "[Efficient construction of metadata-enhanced web
    corpora](https://hal.archives-ouvertes.fr/hal-01371704v2/document)",
    Proceedings of the [10th Web as Corpus Workshop
    (WAC-X)](https://www.sigwac.org.uk/wiki/WAC-X), 2016.


### Citing Trafilatura

Trafilatura is widely used in the academic domain, chiefly for data
acquisition. Here is how to cite it:

[![Reference DOI: 10.18653/v1/2021.acl-demo.15](https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue)](https://aclanthology.org/2021.acl-demo.15/)
[![Zenodo archive DOI: 10.5281/zenodo.3460969](https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg)](https://doi.org/10.5281/zenodo.3460969)

``` shell
@inproceedings{barbaresi-2021-trafilatura,
  title = {{Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction}},
  author = "Barbaresi, Adrien",
  booktitle = "Proceedings of the Joint Conference of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
  pages = "122--131",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/2021.acl-demo.15",
  year = 2021,
}
```


### Software ecosystem

Case studies and publications are listed on the [Used By documentation
page](https://trafilatura.readthedocs.io/en/latest/used-by.html).

Jointly developed plugins and additional packages also contribute to the
field of web data extraction and analysis:

<img alt="Software ecosystem" src="https://raw.githubusercontent.com/adbar/htmldate/master/docs/software-ecosystem.png" align="center" width="65%"/>

Corresponding posts can be found on [Bits of
Language](https://adrien.barbaresi.eu/blog/tag/trafilatura.html). The
blog covers a range of topics from technical how-tos, updates on new
features, to discussions on text mining challenges and solutions.

Impressive, you have reached the end of the page: Thank you for your
interest!
