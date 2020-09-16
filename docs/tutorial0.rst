Tutorial: Gathering a custom web corpus
=======================================


Get your system up and running
------------------------------

-  Installation: see `dedicated page <installation.html>`_
-  Ensure that you have installed the latest version: ``pip install -U trafilatura``

The following instructions use the `command-line interface <https://en.wikipedia.org/wiki/Command-line_interface>`_ (CLI):

- For the very most basic introduction, please refer to this excellent `step-by-step introduction to the CLI <https://tutorial.djangogirls.org/en/intro_to_command_line/>`_
- For general information see `this section <usage-cli.html#introduction>`_ of the documentation.


Find and filter sources
-----------------------


Finding subpages within a website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sources used by Trafilatura may consist of previously known web pages, as well as listed web pages. It can also be useful to operate on website level by downloading portions of a website programmatically. To this end, a sitemap is a file that lists the visible URLs for a given site. For more information, refer to this blog post explaining how to use sitemaps: `to retrieve URLs within a website <http://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.


Filtering with coURLan
~~~~~~~~~~~~~~~~~~~~~~

It is better to examine a list of URLs for content adequacy, most notably to make download and extraction more efficient by removing unwanted and redundant content. The `courlan <https://github.com/adbar/courlan>`_ software package is installed along with ``trafilatura``. It separates the wheat from the chaff by focusing on non-spam text-rich HTML pages, and can be used on the command-line:

``courlan --inputfile linkliste-roh.txt --outputfile linkliste-gefiltert.txt``


Custom filtering
~~~~~~~~~~~~~~~~

URL lists can be filtered manually or with `grep <https://en.wikipedia.org/wiki/Grep>`_, a command-line utility to search text data which operates on line-level and returns either matching or non-matching lines.

-  Matching relevant links: ``grep "/article/" mylist.txt > filtered-list.txt``
-  Exclusion criteria: ``grep -v "/video/" mylist.txt > filtered-list.txt``

For further filters in grep, see `grep tutorial <http://www.panix.com/~elflord/unix/grep.html>`_.

Other relevant utilities include `sort <https://en.wikipedia.org/wiki/Sort_(Unix)>`_ and `shuf <https://en.wikipedia.org/wiki/Shuf>`_:

.. code-block:: bash

    # sort the links and make sure they are unique
    sort -u myfile.txt > myfile-sorted.txt
    # alternatives to shuffle the URLs
    sort -R myfile.txt > myfile-random.txt
    shuf myfile.txt > myfile-random.txt

To draw a random sample of a list of URLs `head <https://en.wikipedia.org/wiki/Head_(Unix)>`_ or `tail <https://en.wikipedia.org/wiki/Tail_(Unix)>`_ come in handy after a random sorting: ``shuf myfile.txt | head -100 > myfile-random-sample.txt``

*Trafilatura* automatically sorts the input list to optimize the download order and make sure the input URLs are unique; it is not mandatory to perform these steps by yourself.


Process a list of links
-----------------------

Two major command line arguments are necessary here:

-  ``-i`` or ``--inputfile`` to select an input list to read links from
-  ``-o`` or ``--outputdir`` to define a directory to eventually store the results

The input list will be read sequentially, only lines beginning with a valid URL will be read, the file can thus contain other information which will be discarded.

The output directory can be created on demand, but it must be  writable.

.. code-block:: bash

    $ trafilatura -i list.txt -o txtfiles	# output as raw text
    $ trafilatura --xml -i list.txt -o xmlfiles	# output in XML format

The second instruction creates a collection of `XML files <https://en.wikipedia.org/wiki/XML>`_ which can be edited with a basic text editor or a full-fledged text-editing software or IDE such as `Atom <https://atom.io/>`_.

Alternatively, you can download a series of web documents with generic command-line tools such as `wget <https://en.wikipedia.org/wiki/Wget>`_ and (re-)process the downloaded files at a later stage:

.. code-block:: bash

    $ wget --directory-prefix=download/ --wait 5 --input-file=mylist.txt
    $ trafilatura --inputdir download/ --outputdir corpus/ --xmltei --nocomments


Work with the data
------------------

See `A Gentle Introduction to XML <https://tei-c.org/release/doc/tei-p5-doc/en/html/SG.html>`_ or the module `xmltodict <https://github.com/martinblech/xmltodict>`_ which provide ways to directly read the files and work with the data as if it were in JSON format.

The textometry platform `TXM <https://txm.gitpages.huma-num.fr/textometrie/en/>`_ can read both XML and TEI-XML files and perform annotation and exploration of corpus data.

Different solutions in Python:

-  `Natural Language Toolkit (NTLK) <https://www.nltk.org/>`_.
-  Topic modeling, including *word2vec* models: `Gensim tutorials <https://radimrehurek.com/gensim/auto_examples/>`_

For natural language processing see this list of open-source/off-the-shelf `NLP tools for German <https://github.com/adbar/German-NLP>`_ and `further lists for other languages <https://github.com/adbar/German-NLP#Comparable-lists>`_.

