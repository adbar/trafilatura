Evaluation
==========

Introduction
^^^^^^^^^^^^

Focus
-----

The multilingual evaluation features a wide array of different websites: news outlets, online magazines, blogs, government or company pages. Archived versions of the pages are sometimes used to test if the extraction is consistent through time.

The benchmark focuses on decisive text parts, mostly at the beginning and the end of the main text where errors often happen. Other difficult segments throughout the document are chosen to enhance detection of false positives, and segments in particular sections (e.g. quotes or lists) are taken to see if all necessary parts of a document are present in the output.

These decisions are prompted by the need to find cost-efficient ways to define a gold standard and annotate a series of documents.


Caveats
-------

This type of evaluation does not probe for duplicate segments, but Trafilatura features a LRU cache for detection of duplicate text parts.

It is not evaluated whether the extracted segments are in the right order, although they are generally few and far apart.


Running the code
^^^^^^^^^^^^^^^^

The results and a list of comparable benchmarks are available on the `evaluation page of the docs <https://trafilatura.readthedocs.io/en/latest/evaluation.html>`_.


Quality gate
------------

The following allows for comparing changes made to Trafilatura, for example in a new version or pull request:

1. Install Trafilatura from the working tree: ``pip install -e .`` (from the repository root)
2. Run ``python tests/eval_gate.py``

``eval_gate.py`` scores the whole corpus with Trafilatura alone and compares the F1-scores with the pinned baseline, exiting non-zero on a regression. It needs no competitor library and is also run in CI.

After editing the annotations or an HTML input, re-pin the corpus hash with ``python tests/eval_gate.py --update``. A re-pin never lowers the baseline on its own: an F1 below a pinned floor keeps the floor and exits non-zero, and accepting a lower bar takes an explicit ``--allow-regression``.


Comparison with other software
------------------------------

``evaluate.py`` additionally runs other extractors. Each competitor library is imported by the algorithm that uses it, not at module level, so ``pip install -e ".[eval]"`` is enough to get started and an algorithm whose library is missing or does not import is reported and dropped from the comparison rather than stopping the run. ``--small`` needs no competitor at all.

Note: As numerous packages are installed it is recommended to create a virtual environment, for example with ``pyenv`` or ``venv``.

1. Install the evaluation dependencies from the repository root: ``pip install -e ".[eval]"`` (``magic-html`` requires Python 3.12+ and is skipped on older versions)
2. For ``news-please``, download the NLTK tokenizer data once: ``python -m nltk.downloader punkt punkt_tab`` (otherwise it attempts a network download per document)
3. Run the script ``evaluate.py``

The published results record the version of each package next to its name, since the packages evolve and their output changes with them.

Options:

- ``--all``: Run all the supported algorithms (some packages are slow, it can be a while)
- ``--small``: Run Trafilatura-based components
- ``--algorithms "html2txt" "html_text"`` (for example): Compare Trafilatura's ``html2txt`` extractor with the ``html_text`` package

``python3 evaluate.py --help``: Display all algorithms and further options.

More comprehensive evaluations are available, mostly focusing on English and/or a particular text type. With minimal adaptations, the evaluation can support the use gold standard files in JSON format.


Sources
^^^^^^^

Annotated HTML documents
------------------------

- BBAW collection (multilingual): Adrien Barbaresi, Lukas Kozmus, Lena Klink.
- Polish news: `tsolewski <https://github.com/tsolewski/Text_extraction_comparison_PL>`_.

HTML archives
-------------

- Additional German news sites: diskursmonitor.de, courtesy of Jan Oliver Rüdiger.

Evaluation scripts
------------------

Adrien Barbaresi, Lydia Körber.
