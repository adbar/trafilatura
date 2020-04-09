Tutorial: from a list of links to a vocabulary list
===================================================


Get your system up and running
------------------------------

-  Installation: see `dedicated page <installation.html>`_
-  Making sure you have the latest version: ``pip install -U trafilatura``
-  Additional software for this tutorial: ``pip install -U SoMaJo``

*Temporary advice: parts of this tutorial require a cutting-edge version of the software which can be installed straight from the software repository:*

``pip install -U git+https://github.com/adbar/trafilatura.git``

The following consists of command-line instructions. For general information see `Comment Prompt <https://www.lifewire.com/how-to-open-command-prompt-2618089>`_ (tutorial for Windows systems), `How to use the Terminal command line in macOS <https://macpaw.com/how-to/use-terminal-on-mac>`_, or `An introduction to the Linux Terminal <https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal>`_.


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


Build frequency lists
----------------------

The `SoMaJo <https://github.com/tsproisl/SoMaJo>`_ tokenizer splits text into words and sentences. It works with Python and gets good results on German and English.

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

