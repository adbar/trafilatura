Quickstart
==========


Primary installation method is with a Python package manager: ``pip install trafilatura``. See `installation documentation <installation.html>`_.


With Python
-----------

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

.. code-block:: python

    # import the package
    >>> import trafilatura
    # grab a HTML file to extract data from
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    # outputs main content and comments as plain text
    >>> result = trafilatura.extract(downloaded)
    # formatting preserved in XML structure
    >>> result = trafilatura.extract(downloaded, output_format="xml")
    # outputs main content without comments as JSON ...
    >>> trafilatura.extract(downloaded, output_format="json", include_comments=False)

The use of fallback algorithms can also be bypassed in fast mode:

.. code-block:: python

    # shorter alternative to import the function
    >>> from trafilatura import extract
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

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...
    $ trafilatura -h
    # displays help message with all possible options


You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    $ cat myfile.html | trafilatura # use the contents of an already existing file
    $ < myfile.html trafilatura # same here


Extraction options are also available on the command-line, they can be combined:

.. code-block:: bash

    $ < myfile.html trafilatura --json --no-tables


For more information please refer to `usage documentation <usage.html>`_ and `tutorials <tutorials.html>`_.

