Quickstart
==========


Primary installation method is with a Python package manager: ``pip install trafilatura``. See `installation documentation <installation.html>`_.


With Python
-----------

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

.. code-block:: python

    # import the necessary functions
    >>> from trafilatura import fetch_url, extract

    # grab a HTML file to extract data from
    >>> downloaded = fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')

    # output main content and comments as plain text
    >>> result = trafilatura.extract(downloaded)

    # change the output format to XML (allowing for preservation of document structure)
    >>> result = trafilatura.extract(downloaded, output_format="xml")

    # discard potential comment and change the output to JSON
    >>> trafilatura.extract(downloaded, output_format="json", include_comments=False)

The use of fallback algorithms can also be bypassed in fast mode:

.. code-block:: python

    # faster mode without backup extraction
    >>> result = extract(downloaded, no_fallback=True)


For a full list of options see `Python usage <usage-python.html>`_.

The extraction targets the main text part of a webpage. To extract all text content in a ``html2txt`` manner use this function:

.. code-block:: python

    >>> from trafilatura import html2txt
    >>> html2txt(downloaded)


On the command-line
-------------------


URLs can be used directly (-u/--URL):

.. code-block:: bash

    # outputs main content and comments as plain text
    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"

    # displays help message with all possible options
    $ trafilatura -h

You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    $ cat myfile.html | trafilatura # use the contents of an already existing file
    $ < myfile.html trafilatura # same here


Extraction options are also available on the command-line, they can be combined:

.. code-block:: bash

    $ < myfile.html trafilatura --json --no-tables


For more information please refer to `usage documentation <usage.html>`_ and `tutorials <tutorials.html>`_.

