Tutorial: Gathering a custom web corpus
=======================================


Get your system up and running
------------------------------

-  Installation: see `dedicated page <installation.html>`_
-  Making sure you have the latest version: ``pip install -U trafilatura``

The following instructions use the `command-line interface <https://en.wikipedia.org/wiki/Command-line_interface>`_ (CLI):

- For the very first steps please refer to this nice `step-by-step introduction to the CLI <https://tutorial.djangogirls.org/en/intro_to_command_line/>`_
- For general information see `this section <usage-cli.html#introduction>`_ of the documentation


Find and filter sources
-----------------------

The sources can consist of previously known and listed web pages. It can also be useful to operate on website-level by downloading portions of a website programmatically. A sitemap is a file that lists the visible URLs for a given site, for more information see this blog post explaining how to use sitemaps `to retrieve URLs within a website <http://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.

URL lists can be filtered manually or with `grep <https://en.wikipedia.org/wiki/Grep>`_, a command-line utility to search text data which operates on line-level and returns matching lines or non-matching ones:

-  Matching relevant links: ``grep "/article/" mylist.txt > filtered-list.txt``
-  Exclusion criteria: ``grep -v "/video/" mylist.txt > filtered-list.txt``

For further filters see this `grep tutorial <http://www.panix.com/~elflord/unix/grep.html>`_.

Other relevant utilities are `sort <https://en.wikipedia.org/wiki/Sort_(Unix)>`_ and `shuf <https://en.wikipedia.org/wiki/Shuf>`_:

.. code-block:: bash

    # sort the links and make sure they are unique
    sort -u myfile.txt > myfile-sorted.txt
    # alternatives to shuffle the URLs
    sort -R myfile.txt > myfile-random.txt
    shuf myfile.txt > myfile-random.txt

To draw a random sample of a list of URLs `head <https://en.wikipedia.org/wiki/Head_(Unix)>`_ or `tail <https://en.wikipedia.org/wiki/Tail_(Unix)>`_ come in handy after a random sorting: ``shuf myfile.txt | head -100 > myfile-random-sample.txt``

*Trafilatura* automatically sorts the input list to optimize the download order and make sure the input URLs are unique, it is not mandatory to perform these steps by yourself.


Process a list of links
-----------------------

Two major options are necessary here:

-  ``-i`` or ``--inputfile`` to select an input list to read links from
-  ``-o`` or ``--outputdir`` to define a directory to eventually store the results

The input list will be read sequentially, only lines beginning with a valid URL will be read, the file can thus contain other information which will be discarded.

The output directory can be created on demand, it has to be writable.

.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles	# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles	# output in XML format

The second instruction creates a collection of `XML files <https://en.wikipedia.org/wiki/XML>`_ which can be edited with a basic notepad or a full-fledged text-editing software such as `Atom <https://atom.io/>`_.

Alternatively, you can download a series of web documents with generic command-line tools such as `wget <https://en.wikipedia.org/wiki/Wget>`_ and (re-)process the downloaded files at a later stage:

.. code-block:: bash

    $ wget --directory-prefix=download/ --wait 5 --input-file=mylist.txt
    $ trafilatura --inputdir download/ --outputdir corpus/ --xmltei --nocomments


Work with the data
------------------

See `A Gentle Introduction to XML <https://tei-c.org/release/doc/tei-p5-doc/en/html/SG.html>`_ or the module `xmltodict <https://github.com/martinblech/xmltodict>`_ which provides a way to directly read the files and work with the data as if it were in JSON format.


The textometry platform `TXM <https://txm.gitpages.huma-num.fr/textometrie/en/>`_ can read both XML and TEI-XML files and perform annotation and exploration of corpus data.

Different solutions in Python:

-  `Natural Language Toolkit (NTLK) <https://www.nltk.org/>`_.
-  Topic modeling, including *word2vec* models: `Gensim tutorials <https://radimrehurek.com/gensim/auto_examples/>`_

For natural language processing see this list of open-source/off-the-shelf `NLP tools for German <https://github.com/adbar/German-NLP>`_ and `further lists for other languages <https://github.com/adbar/German-NLP#Comparable-lists>`_.

