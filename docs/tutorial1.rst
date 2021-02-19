Tutorial: From a list of links to a frequency list
==================================================


.. meta::
    :description lang=en:
        This how-to explains how to easily extract text from HTML web pages and compute
        a list of the most frequent word forms.



Get your system up and running
------------------------------

-  Installation: see `dedicated page <installation.html>`_
-  Ensure you have installed the latest version: ``pip install -U trafilatura``
-  Additional software for this tutorial: ``pip install -U SoMaJo``

The following consists of `command-line instructions <https://en.wikipedia.org/wiki/Command-line_interface>`_. For an introduction see the `page on command-line usage <usage-cli.html#introduction>`_.


Process a list of links
-----------------------

For the collection and filtering of links see `this tutorial <tutorial0.html>`_ and this `blog post <https://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.

Two major options are necessary here:

-  ``-i`` or ``--inputfile`` to select an input list to read links from
-  ``-o`` or ``--outputdir`` to define a directory to eventually store the results

The input list will be read sequentially, and only lines beginning with a valid URL will be read; any other information contained in the file will be discarded.

The output directory can be created on demand, but it has to be writable.

.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles	# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles	# output in XML format

The second instruction creates a collection of `XML files <https://en.wikipedia.org/wiki/XML>`_ which can be edited with a basic text editor or a full-fledged text-editing package or IDE such as `Atom <https://atom.io/>`_.


Build frequency lists
----------------------

Step-by-step
~~~~~~~~~~~~

Tokenization
^^^^^^^^^^^^

The `SoMaJo <https://github.com/tsproisl/SoMaJo>`_ tokenizer splits text into words and sentences. It works with Python and gets good results when applied to texts in German and English.

Assuming the output directory you are working with is called ``txtfiles``:

.. code-block:: bash

    # concatenate all files
    $ cat txtfiles/*.txt > txtfiles/all.txt
    # output all tokens
    $ somajo-tokenizer txtfiles/all.txt > tokens.txt
    # sort the tokens by decreasing frequency and output up to 10 most frequent tokens
    $ sort tokens.txt | uniq -c | sort -nrk1 | head -10


Filtering words
^^^^^^^^^^^^^^^

.. code-block:: bash

    # further filtering: remove punctuation, delete empty lines and lowercase strings
    $ < tokens.txt sed -e "s/[[:punct:]]//g" -e "/^$/d" -e "s/.*/\L\0/" > tokens-filtered.txt
    # display most frequent tokens
    $ < tokens-filtered.txt sort | uniq -c | sort -nrk1 | head -20
    # store frequency information in a CSV-file
    $ < tokens.txt sort | uniq -c | sort -nrk1 | sed -e "s|^ *||g" -e  "s| |\t|" > txtfiles/frequencies.csv

Further filtering steps:

- with a list of stopwords: ``egrep -vixFf stopwords.txt``
- alternative to convert to lower case: ``uconv -x lower``


Collocations and multi-word units
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # word bigrams
    $ < tokens-filtered.txt tr "\n" " " | awk '{for (i=1; i<NF; i++) print $i, $(i+1)}' | sort | uniq -c | sort -nrk1 | head -20
    # word trigrams
    $ < tokens-filtered.txt tr "\n" " " | awk '{for (i=1; i<NF; i++) print $i, $(i+1), $(i+2)}' | sort | uniq -c | sort -nrk1 | head -20


Further information
~~~~~~~~~~~~~~~~~~~

- `Unix™ for Poets <https://ftyers.github.io/079-osnov-programm/classes/01.html>`_ (count and sort words, compute ngram statistics, make a Concordance)
- `Word analysis and N-grams <https://developer.ibm.com/technologies/artificial-intelligence/articles/cc-patterns-artificial-intelligence-part2/>`_
- `N-Grams with NLTK <https://www.nltk.org/api/nltk.html#nltk.util.bigrams>`_ and `collocations howto <https://www.nltk.org/howto/collocations.html>`_
- `Analyzing Documents with Term Frequency - Inverse Document Frequency (tf-idf) <https://programminghistorian.org/en/lessons/analyzing-documents-with-tfidf>`_, both a corpus exploration method and a pre-processing step for many other text-mining measures and models



Additional information for XML files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming the output directory you are working with is called ``xmlfiles``:

.. code-block:: bash

    # tokenize a file
    $ somajo-tokenizer --xml xmlfiles/filename.xml
    # remove tags
    $ somajo-tokenizer --xml xmlfiles/filename.xml | sed -e "s|</*.*>||g" -e "/^$/d"
    # continue with the steps above...

