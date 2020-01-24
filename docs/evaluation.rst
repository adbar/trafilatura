Evaluation
==========


Most corresponding Python packages are not actively maintained, the following alternatives exist.

These packages keep the structure intact but don't focus on main text extraction:

- `html2text <https://github.com/Alir3z4/html2text>`_ converts HTML pages to Markup language
- `inscriptis <https://github.com/weblyzard/inscriptis>`_ converts HTML to text with a particular emphasis on nested tables

These packages focus on main text extraction:

- `dragnet <https://github.com/dragnet-org/dragnet>`_ features combined and machine-learning approaches, but requires many dependencies as well as extensive tuning
- `goose <https://github.com/goose3/goose3>`_ can extract information for embedded content but doesn't preserve markup and is not maintained
- `newspaper <https://github.com/codelucas/newspaper>`_ is mostly geared towards newspaper texts, provides additional functions but no structured text or comment extraction
- `python-readability <https://github.com/buriy/python-readability>`_ cleans the page and preserves some markup but is mostly geared towards news texts


Description
-----------

**Test set**: the experiments below are run on a small collection of documents that are non-standard and thus harder to process. They contain mixed content forms (lists, tables) and/or non-standard not fully valid HTML code. They were selected from large collections of web pages in German.

**Evaluation**: decisive document segments are singled out which are not statistically representative but very significant in the perspective of working with the texts, most notably left/right columns, additional header, author or footer information such as imprints or addresses.

**Results**: tt turns out that rule-based approaches such as *trafilatura*'s obtain balanced results despite a lack of precision. Combined with an algorithmic approach they perform better than the other tested software.

**Time**: the execution time is not to be taken too seriously, the only conclusion at this stage is that *goose3* is slower than the rest.

**Roadmap**: further evaluations coming up, including further tools and languages. I couldn't get the *newspaper* module to work without errors on every HTML file in the test set. Comment extraction still has to be evaluated, although most libraries don't offer this functionality.

The evaluation script is available on the project repository: `tests/comparison.py <https://github.com/adbar/trafilatura/blob/master/tests/comparison.py>`_.


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
trafilatura 0.3.1 (+ fallback)  0.873      0.951      **0.911** 1.09
=============================== =========  ========== ========= ========
