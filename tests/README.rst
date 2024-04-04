Evaluation
==========

Basics
^^^^^^

The multilingual evaluation features a wide array of different websites: news outlets, online magazines, blogs, government and company pages. Archived versions of the pages are sometimes used to test if the extraction is consistent throughout time.

It focuses on decisive segments, mostly at the beginning and the end of the main text where errors often happen. Other difficult segments throughout the document are chosen to enhance detection of false positives, and segments in particular sections (e.g. quotes or lists) are taken to see if all parts of a documents are present.


Caveats
^^^^^^^

This type of evaluation does not probe for duplicate segments, but Trafilatura features a LRU cache for detection of duplicate text parts.

It is not evaluated whether the extracted segments are in the right order, although they are generally few and far apart.

The reasons behind these design decisions are mostly related to finding cost-efficient ways to define a gold standard. More comprehensive evaluations are available, mostly focusing on English and/or a particular text type.


Reproducing the evaluation
--------------------------

Trafilatura evaluation
^^^^^^^^^^^^^^^^^^^^^^

This allows for comparing changes made to Trafilatura, e.g. in a new version or pull request:

1. Install Trafilatura
2. Run the script ``comparison_small.py``


Full evaluation
^^^^^^^^^^^^^^^

A comparison with similar software is run periodically. As the packages tend to evolve the script may not always be up-to-date or all packages may not be available. Commenting out the corresponding segments is the most efficient solution.


1. Install the packages specified in ``eval-requirements.txt``
2. Run the script ``comparison.py``


Sources
-------

Annotated HTML documents
^^^^^^^^^^^^^^^^^^^^^^^^

- BBAW collection (multilingual): Adrien Barbaresi, Lukas Kozmus, Lena Klink.
- Polish news: `tsolewski <https://github.com/tsolewski/Text_extraction_comparison_PL>`_.

HTML archives
^^^^^^^^^^^^^

- Additional German news sites: diskursmonitor.de, courtesy of Jan Oliver Rüdiger.

