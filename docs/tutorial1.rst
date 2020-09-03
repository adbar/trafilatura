Tutorial: From a list of links to a frequency list
==================================================


Get your system up and running
------------------------------

-  Installation: see `dedicated page <installation.html>`_
-  Ensure you have installed the latest version: ``pip install -U trafilatura``
-  Additional software for this tutorial should be installed with: ``pip install -U SoMaJo``

The following consists of command-line instructions. For general information see `Comment Prompt <https://www.lifewire.com/how-to-open-command-prompt-2618089>`_ (tutorial for Windows systems), `How to use the Terminal command line in macOS <https://macpaw.com/how-to/use-terminal-on-mac>`_, or `An introduction to the Linux Terminal <https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal>`_.


Process a list of links
-----------------------

For the collection and filtering of links see `this tutorial <tutorial0.html>`_ and this `blog post <http://adrien.barbaresi.eu/blog/using-sitemaps-crawl-websites.html>`_.

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

The `SoMaJo <https://github.com/tsproisl/SoMaJo>`_ tokenizer splits text into words and sentences. It works with Python and gets good results when applied to texts in German and English.

Assuming the output directory you are working with is called ``txtfiles``:

.. code-block:: bash

    # concatenate all files
    $ cat txtfiles/*.txt > txtfiles/all.txt
    # output all tokens
    $ somajo-tokenizer txtfiles/all.txt
    # sort the tokens by decreasing frequency and output up to 100 most frequent tokens
    $ somajo-tokenizer txtfiles/all.txt | sort | uniq -c | sort -nrk1 | head -100
    # store frequency information in a CSV-file
    $ somajo-tokenizer txtfiles/all.txt | sort | uniq -c | sort -nrk1 | sed -e "s|^ *||g" -e  "s| |\t|" > txtfiles/frequencies.csv


Additional information for XML files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming the output directory you are working with is called ``xmlfiles``:

.. code-block:: bash

    # tokenize a file
    $ somajo-tokenizer --xml xmlfiles/filename.xml
    # remove tags
    $ somajo-tokenizer --xml xmlfiles/filename.xml | sed -e "s|</*.*>||g" -e "/^$/d"
    # continue with the steps above...
