Evaluation
==========

.. meta::
    :description lang=en:
        This benchmark tests how Python tools work on extraction of text from HTML code. Trafilatura
        performs significantly better than the other comparable libraries in internal and external
        evaluations.


Although text is ubiquitous on the Web, extracting information from web pages can prove to be difficult. Should the tooling be adapted to particular news outlets or blogs that are targeted (which often amounts to the development of web scraping tools) or should the extraction be as generic as possible to provide opportunistic ways of gathering information?

The extraction focuses on the main content, which is usually the part displayed centrally, without the left or right bars, the header or the footer, but including potential titles and (optionally) comments. This task is also known as web scraping, boilerplate removal, DOM-based content extraction, main content identification, or web page cleaning.


Alternatives
------------

Although a few corresponding Python packages are not actively maintained the following alternatives exist.

These packages keep the structure intact but don't focus on main text extraction:

- `html2text <https://github.com/Alir3z4/html2text>`_ converts HTML pages to Markup language
- `html_text <https://github.com/TeamHG-Memex/html-text>`_ converts HTML code to plain text
- `inscriptis <https://github.com/weblyzard/inscriptis>`_ converts HTML to text with a particular emphasis on nested tables

These packages focus on main text extraction:

- `boilerpy3 <https://github.com/jmriebold/BoilerPy3>`_ is a Python version of the `boilerpipe algorithm <https://github.com/kohlschutter/boilerpipe>`_ for boilerplate removal and fulltext extraction
- `dragnet <https://github.com/dragnet-org/dragnet>`_ features combined and machine-learning approaches, but requires more dependencies and potentially fine-tuning
- `goose3 <https://github.com/goose3/goose3>`_ can extract information for embedded content but doesn't preserve markup
- `jusText <https://github.com/miso-belica/jusText>`_ is designed to preserve mainly text containing full sentences along with some markup, it has been explicitly developed to create linguistic resources
- `newspaper <https://github.com/codelucas/newspaper>`_ is mostly geared towards newspaper texts, provides additional functions but no structured text or comment extraction
- `news-please <https://github.com/fhamborg/news-please>`_ is a news crawler that extracts structured information
- `python-readability <https://github.com/buriy/python-readability>`_ cleans the page and preserves some markup

Last but not least, `trafilatura <https://github.com/adbar/trafilatura>`_ is the library documented here. It downloads web pages, scrapes main text and comments while preserving some structure, and converts to TXT, CSV, XML & TEI-XML.

The tools are compared to the raw page source and to a meaningful baseline consisting of extracting all the text contained in paragraph, code or quoting elements.


Description
-----------

**Test set**: The experiments below are run on a collection of documents which are either typical for Internet articles (news outlets, blogs) or non-standard and thus harder to process. Some contain mixed content (lists, tables) and/or non-standard not fully valid HTML code. They were selected from `large collections of web pages in German <https://www.dwds.de/d/k-web>`_, for the sake of completeness a few documents in other languages are added (notably English, French, other European languages, Chinese and Arabic).

**Evaluation**: Decisive document segments are singled out which are not statistically representative but very significant in the perspective of working with the texts, most notably left/right columns, additional header, author or footer information such as imprints or addresses, as well as affiliated and social network links, in short boilerplate. Raw text segments are expected which is also a way to evaluate the quality of HTML extraction in itself.

**Time**: The execution time is not to be taken too seriously, the only conclusion at this stage is that *goose3* and *newspaper* are slower than the rest while *news-please*'s execution time isn't comparable because of operations unrelated to text extraction. Baseline extraction is simple and fast.

**Errors**: The *newspaper* and *boilerpipe* modules do not work without errors on every HTML file in the test set, probably because of malformed HTML, encoding or parsing bugs.

**Results**: The baseline beats a few systems, showing its interest. It turns out that rule-based approaches such as *trafilatura*'s obtain balanced results despite a lack of precision. Combined with an algorithmic approach they perform significantly better than the other tested solutions. *justext* is highly configurable and tweaking its configuration leads to better performance than its generic settings.

**Roadmap**: Further evaluations coming up, including additional tools and languages. Comment extraction still has to be evaluated, although most libraries don't offer this functionality.

The evaluation script is available on the project repository: `tests/comparison.py <https://github.com/adbar/trafilatura/blob/master/tests/comparison.py>`_. To reproduce the tests just clone the repository, install all necessary packages and run the evaluation script with the data provided in the *tests* directory.


Results (2021-06-07)
--------------------

=============================== =========  ========== ========= ========= ======
500 documents, 1487 text and 1496 boilerplate segments
--------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Diff.
=============================== =========  ========== ========= ========= ======
*raw HTML*                      0.527      0.878      0.547     0.659     0
html2text 2020.1.16             0.488      0.714      0.484     0.580     8.9x
html_text 0.5.2                 0.526      **0.958**  0.548     0.679     1.9x
inscriptis 1.1 (html to txt)    0.531      **0.958**  0.556     0.683     2.4x
justext 2.2.0 (custom)          0.870      0.584      0.749     0.699     6.1x
newspaper3k 0.2.8               0.921      0.574      0.763     0.708     12.9x
boilerpy3 1.0.2 (article mode)  0.851      0.696      0.788     0.766     4.8x
goose3 3.1.9                    **0.950**  0.644      0.806     0.767     18.8x
*baseline (text markup)*        0.746      0.804      0.766     0.774     **1x**
dragnet 2.0.4                   0.906      0.689      0.810     0.783     3.1x
readability-lxml 0.8.1          0.917      0.716      0.826     0.804     5.9x
news-please 1.5.21              0.924      0.718      0.830     0.808     60x
trafilatura 0.8.2 (fast)        0.925      0.868      0.899     0.896     3.9x
trafilatura 0.8.2               0.934      **0.890**  **0.914** **0.912** 8.4x
=============================== =========  ========== ========= ========= ======


External evaluations
--------------------

- Trafilatura is the most efficient open-source library in *ScrapingHub*'s `article extraction benchmark <https://github.com/scrapinghub/article-extraction-benchmark>`_.
- Best overall tool according to Gaël Lejeune & Adrien Barbaresi, `Bien choisir son outil d'extraction de contenu à partir du Web <https://hal.archives-ouvertes.fr/hal-02768510v3/document>`_ (2020, PDF, in French).
- Comparison on a small `sample of Polish news texts and forums <https://github.com/tsolewski/Text_extraction_comparison_PL>`_.



Older results (2020-11-06)
--------------------------

=============================== =========  ========== ========= ========= ======
500 documents, 1487 text and 1496 boilerplate segments
--------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Diff.
=============================== =========  ========== ========= ========= ======
*raw HTML*                      0.527      0.878      0.547     0.659     0
html2text 2020.1.16             0.488      0.714      0.484     0.580     8.9x
html_text 0.5.2                 0.526      **0.958**  0.548     0.679     1.9x
inscriptis 1.1 (html to txt)    0.531      **0.958**  0.556     0.683     2.4x
justext 2.2.0 (tweaked)         0.870      0.584      0.749     0.699     6.1x
newspaper3k 0.2.8               0.921      0.574      0.763     0.708     12.9x
goose3 3.1.6                    **0.950**  0.629      0.799     0.757     19.0x
boilerpy3 1.0.2 (article mode)  0.851      0.696      0.788     0.766     4.8x
*baseline (text markup)*        0.746      0.804      0.766     0.774     **1x**
dragnet 2.0.4                   0.906      0.689      0.810     0.783     3.1x
readability-lxml 0.8.1          0.917      0.716      0.826     0.804     5.9x
news-please 1.5.13              0.923      0.711      0.827     0.804     184x
trafilatura 0.6.0               0.924      0.849      0.890     0.885     3.9x
trafilatura 0.6.0 (+ fallbacks) 0.933      **0.877**  **0.907** **0.904** 8.4x
=============================== =========  ========== ========= ========= ======



Older results (2020-07-16)
--------------------------

=============================== =========  ========== ========= ========= ======
400 documents, 1186 text and 1198 boilerplate segments
--------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Diff.
=============================== =========  ========== ========= ========= ======
*raw HTML*                      0.524      0.879      0.543     0.657     0
html2text 2020.1.16             0.485      0.718      0.480     0.579     8.4x
html_text 0.5.1                 0.521      0.962      0.542     0.676     1.8x
inscriptis 1.0 (html to txt)    0.527      **0.965**  0.551     0.681     1.9x
newspaper3k 0.2.8               0.916      0.577      0.763     0.708     11.8x
justext 2.2.0 (tweaked)         0.867      0.651      0.777     0.744     4.9x
goose3 3.1.6                    **0.953**  0.635      0.803     0.762     17.3x
*baseline (text markup)*        0.738      0.804      0.760     0.770     **1x**
boilerpy3 1.0.2 (article mode)  0.847      0.711      0.792     0.773     4.4x
dragnet 2.0.4                   0.906      0.704      0.816     0.792     2.8x
readability-lxml 0.8.1          0.913      0.739      0.835     0.817     5.4x
news-please 1.4.25              0.918      0.739      0.837     0.819     56.4x
trafilatura 0.5.1               0.927      0.854      0.894     0.889     3.1x
trafilatura 0.5.1 (+ fallbacks) 0.933      0.885      **0.911** **0.908** 6.8x
=============================== =========  ========== ========= ========= ======


Older results (2020-03-19)
--------------------------

=============================== =========  ========== ========= ========= =====
300 documents, 869 text and 878 boilerplate segments
-------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Time
=============================== =========  ========== ========= ========= =====
*raw HTML*                      0.519      0.885      0.535     0.654     0
*baseline (text markup)*        0.726      0.776      0.742     0.750     1.14 
html2text 2020.1.16             0.499      0.787      0.501     0.611     11.00
inscriptis 1.0 (html to txt)    0.521      **0.962**  0.541     0.676     2.47
justext 2.2.0 (German stoplist) 0.849      0.529      0.719     0.652     6.37
newspaper 0.2.8                 0.923      0.591      0.772     0.721     14.80
goose3 3.1.6                    **0.957**  0.640      0.807     0.767     21.54
boilerpy3 1.0.2 (article mode)  0.841      0.734      0.799     0.784     5.65
dragnet 2.0.4                   0.909      0.722      0.825     0.804     3.64
readability-lxml 0.7.1          0.928      0.743      0.844     0.826     6.59
news-please 1.4.25              0.926      0.747      0.844     0.827     70.81
trafilatura 0.3.1 (rule-based)  0.901      0.831      0.871     0.865     5.43
trafilatura 0.3.1 (+ justext)   0.897      0.868      0.884     0.882     6.97
trafilatura 0.4                 0.914      0.869      0.894     0.891     4.87
trafilatura 0.4 (+ fallback)    0.925      0.904      **0.916** **0.914** 9.94
=============================== =========  ========== ========= ========= =====


Older results (2020-01-29)
--------------------------

=============================== =========  ========== ========= ========= =====
100 documents, 266 text and 294 boilerplate segments
-------------------------------------------------------------------------------
Python Package                  Precision  Recall     Accuracy  F-Score   Time
=============================== =========  ========== ========= ========= =====
*raw HTML*                      0.492      0.902      0.511     0.637     0
inscriptis 1.0 (html to txt)    0.504      **0.989**  0.532     0.668     0.87
justext 2.2.0 (German stoplist) 0.886      0.553      0.754     0.681     2.22
goose3 3.1.6                    **0.935**  0.594      0.787     0.726     7.64
newspaper 0.2.8                 0.920      0.609      0.789     0.733     5.34
boilerpy3 1.0.2 (default mode)  0.767      0.756      0.775     0.761     1.89
dragnet 2.0.4                   0.904      0.673      0.811     0.772     1.25
readability-lxml 0.7.1          0.894      0.699      0.818     0.785     2.34
news-please 1.4.25              0.900      0.714      0.827     0.797     22.99
trafilatura 0.3.1 (rule-based)  0.872      0.895      0.887     0.883     1.87
trafilatura 0.3.1 (+ justext)   0.889      0.936      **0.914** **0.912** 2.19
=============================== =========  ========== ========= ========= =====
