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


Evaluation
----------

The following allows for comparing changes made to Trafilatura, for example in a new version or pull request:

1. Install Trafilatura
2. Run the script ``comparison_small.py``


A comparison with similar software is run periodically. As the packages tend to evolve the script may not always be up-to-date and all packages may not be available. If that happens, commenting out the corresponding sections is the most efficient solution. Fixes to the file can be submitted as pull requests.

Note: As numerous packages are installed it is recommended to create a virtual environment, for example with ``pyenv`` or ``venv``.

1. Install the packages specified in ``eval-requirements.txt``
2. Run the script ``evaluate.py``

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
