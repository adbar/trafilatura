Evaluation
==========


Although text is ubiquitous on the Web, extracting information from web pages can prove to be difficult. Should the tooling be adapted to particular news outlets or blogs that are targeted (which often amounts to the development of web scraping tools) or should the extraction be as generic as possible to provide opportunistic ways of gathering information?


Alternatives
------------

Although a few corresponding Python packages are not actively maintained the following alternatives exist.

These packages keep the structure intact but don't focus on main text extraction:

- `html2text <https://github.com/Alir3z4/html2text>`_ converts HTML pages to Markup language
- `inscriptis <https://github.com/weblyzard/inscriptis>`_ converts HTML to text with a particular emphasis on nested tables

These packages focus on main text extraction:

- `boilerpy3 <https://github.com/jmriebold/BoilerPy3>`_ is a Python version of the `boilerpipe algorithm <https://github.com/kohlschutter/boilerpipe>`_ for boilerplate removal and fulltext extraction
- `dragnet <https://github.com/dragnet-org/dragnet>`_ features combined and machine-learning approaches, but requires more dependencies and potentially fine-tuning
- `goose3 <https://github.com/goose3/goose3>`_ can extract information for embedded content but doesn't preserve markup
- `jusText <https://github.com/miso-belica/jusText>`_ is designed to preserve mainly text containing full sentences along with some markup, it has been explicitly developed to create linguistic resources
- `newspaper3k <https://github.com/codelucas/newspaper>`_ is mostly geared towards newspaper texts, provides additional functions but no structured text or comment extraction
- `news-please <https://github.com/fhamborg/news-please>`_ is a news crawler that extracts structured information
- `python-readability <https://github.com/buriy/python-readability>`_ cleans the page and preserves some markup


Description
-----------

**Test set**: the experiments below are run on a collection of documents which are either typical for Internet articles (news outlets, blogs) or non-standard and thus harder to process. Some contain mixed content (lists, tables) and/or non-standard not fully valid HTML code. They were selected from `large collections of web pages in German <https://www.dwds.de/d/k-web>`_, for the sake of completeness a few documents in English are added.

**Evaluation**: decisive document segments are singled out which are not statistically representative but very significant in the perspective of working with the texts, most notably left/right columns, additional header, author or footer information such as imprints or addresses, as well as affiliated and social network links, in short boilerplate. Raw text segments are expected which is also a way to evaluate the quality of HTML extraction in itself.

**Time**: the execution time is not to be taken too seriously, the only conclusion at this stage is that *goose3* and *newspaper3k* are slower than the rest while *news-please* performs a whole series of operations unrelated to text extraction.

**Errors**: the *newspaper* and *boilerpipe* modules do not work without errors on every HTML file in the test set, probably because of malformed HTML or parsing bugs

**Results**: it turns out that rule-based approaches such as *trafilatura*'s obtain balanced results despite a lack of precision. Combined with an algorithmic approach they perform significantly better than the other tested solutions.

**Roadmap**: further evaluations coming up, including additional tools and languages. Comment extraction still has to be evaluated, although most libraries don't offer this functionality.

The evaluation script is available on the project repository: `tests/comparison.py <https://github.com/adbar/trafilatura/blob/master/tests/comparison.py>`_. To reproduce the tests just clone the repository, install all necessary packages and run the evaluation script with the data provided in the *tests* directory.


Results (2020-01-29)
--------------------

=============================== =========  ========== ========= ========= =====
100 documents, 266 text and 294 boilerplate segments
-------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Time
=============================== =========  ========== ========= ========= =====
*everything with markup*        0.492      0.902      0.511     0.637     0
inscriptis 1.0 (html to txt)    0.504      **0.989**  0.532     0.668     0.87
justext 2.2.0                   0.886      0.553      0.754     0.681     2.22
goose3 3.1.6                    **0.935**  0.594      0.787     0.726     7.64
newspaper3k 0.2.8               0.920      0.609      0.789     0.733     5.34
boilerpy3 1.0.2                 0.767      0.756      0.775     0.761     1.89
dragnet 2.0.4                   0.904      0.673      0.811     0.772     1.25
readability-lxml 0.7.1          0.894      0.699      0.818     0.785     2.34
news-please 1.4.25              0.900      0.714      0.827     0.797     22.99
trafilatura 0.3.1 (rule-based)  0.872      0.895      0.887     0.883     1.87
trafilatura 0.3.1 (+ justext)   0.889      0.936      **0.914** **0.912** 2.19
=============================== =========  ========== ========= ========= =====


Results (2020-01-24)
--------------------

=============================== =========  ========== ========= ========
50 documents, 123 positive and 142 negative segments
------------------------------------------------------------------------
Python Package                  Precision  Recall     F-Score   Time
=============================== =========  ========== ========= ========
*everything with markup*        0.481      0.902      0.627     0
inscriptis 1.0 (html to txt)    0.494      **0.992**  0.659     0.44
newspaper3k 0.2.8               0.893      0.545      0.677     2.53
justext 2.2.0                   0.880      0.593      0.709     1.21
goose3 3.1.6                    **0.915**  0.610      0.732     3.88
readability-lxml 0.7.1          0.873      0.724      0.791     1.15
trafilatura 0.3.1 (rule-based)  0.853      0.894      0.873     0.86
trafilatura 0.3.1 (+ justext)   0.873      0.951      **0.911** 1.09
=============================== =========  ========== ========= ========
