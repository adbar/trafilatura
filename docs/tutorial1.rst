Tutorial: From a list of links to a frequency list
==================================================


.. meta::
    :description lang=en:
        This how-to explains how to easily extract text from HTML web pages and compute
        a list of the most frequent word forms.


This tutorial shows in a simple and accessible way how to extract extract text from web pages and compute frequency lists. You will learn how to use command-line tools to process the links, extract the content, and then break it down into individual words and phrases. From there, you can sort and filter the results to get a sense of what is most commonly found in the corpus.


Get your system up and running
------------------------------

-  Installation: Check out the `dedicated installation page <installation.html>`_
-  Update to the latest version: ``pip install -U trafilatura`` to ensure you have the latest version of ``trafilatura``
-  Additional software for tokenization: You will also need to install ``SoMaJo`` using ``pip install -U SoMaJo``


The following sections will use command-line instructions. If you're new to command-line interfaces, check out the `page on command-line usage <usage-cli.html#introduction>`_ for a brief overview.


Process a list of links
-----------------------

For the collection and filtering of links see `this tutorial <tutorial0.html>`_ and this `blog post <https://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.

Two major options are necessary here:

-  ``-i`` or ``--input-file`` to specify the input file containing the list of links
-  ``-o`` or ``--output-dir`` to define the directory where the results will be stored


Here is how it works:

- The input file will be read line by line, and only lines starting with a valid URL will be processed. Any other information in the file will be ignored.
- The output directory will be created if it does not exist, but it must be writable.


The first instruction uses TXT as output whereas the second one creates a collection of `XML files <https://en.wikipedia.org/wiki/XML>`_. Both file types can be edited with a basic text editor or a full-fledged text-editing package or IDE such as Atom.

.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles	# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles	# output in XML format



Build frequency lists
----------------------

Step-by-step
~~~~~~~~~~~~

Tokenization
^^^^^^^^^^^^

The `SoMaJo <https://github.com/tsproisl/SoMaJo>`_ tokenizer splits text into words and sentences. It works with Python and gets good results when applied to texts in German and English.

Assuming the output directory you are working with is called ``txtfiles``, let's concatenate all files and tokenize the text:

.. code-block:: bash

    $ cat txtfiles/*.txt > txtfiles/all.txt
    $ somajo-tokenizer txtfiles/all.txt > tokens.txt


Next, let's sort the tokens by decreasing frequency and output the top 10 most frequent tokens:

.. code-block:: bash

    $ sort tokens.txt | uniq -c | sort -nrk1 | head -10


Filtering words
^^^^^^^^^^^^^^^

Now, let's filter out punctuation, empty lines, convert the text to lowercase, and display the most frequent tokens:

.. code-block:: bash

    $ < tokens.txt sed -e "s/[[:punct:]]//g" -e "/^$/d" -e "s/.*/\L\0/" > tokens-filtered.txt
    # display most frequent tokens
    $ < tokens-filtered.txt sort | uniq -c | sort -nrk1 | head -20


Assuming the output is useful, let's store the frequency information in a CSV file for further processing:

.. code-block:: bash

    $ < tokens.txt sort | uniq -c | sort -nrk1 | sed -e "s|^ *||g" -e  "s| |\t|" > txtfiles/frequencies.csv


As an inspiration, here is how further filtering steps could look like:

- with a list of stopwords: ``egrep -vixFf stopwords.txt``
- alternative to convert to lower case: ``uconv -x lower``


N-gram lists
^^^^^^^^^^^^

Bigram and trigrams are groups of 2 or 3 words that appear together in a text. N-gram lists are collections of bigrams, trigrams, and other groups of words. They are like a snapshot of how words are used together in a particular context. By analyzing these lists, you can identify patterns, trends, and relationships between words that might not be immediately apparent.

These concepts help getting a first overview on how words work together in language, and how they create meaning beyond individual words. The commands below will output the most frequent word bigrams and trigrams in the texts gathered in the last section:


.. code-block:: bash

    # word bigrams
    $ < tokens-filtered.txt tr "\n" " " | awk '{for (i=1; i<NF; i++) print $i, $(i+1)}' | sort | uniq -c | sort -nrk1 | head -20
    # word trigrams
    $ < tokens-filtered.txt tr "\n" " " | awk '{for (i=1; i<NF; i++) print $i, $(i+1), $(i+2)}' | sort | uniq -c | sort -nrk1 | head -20


Further information
~~~~~~~~~~~~~~~~~~~

- `Unix™ for Poets <https://ftyers.github.io/079-osnov-programm/classes/01.html>`_ (count and sort words, compute ngram statistics, make a Concordance)
- `Collocations howto <https://www.nltk.org/howto/collocations.html>`_
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

