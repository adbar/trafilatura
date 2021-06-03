Quickstart
==========


Primary installation method is with a Python package manager: ``pip install trafilatura``. See `installation documentation <installation.html>`_.


With Python
-----------

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

.. code-block:: python

    >>> import trafilatura
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> trafilatura.extract(downloaded)
    # outputs main content and comments as plain text ...
    >>> result = trafilatura.extract(downloaded, output_format="xml")
    >>> print(result)
    # formatting preserved in XML structure ...
    >>> trafilatura.extract(downloaded, xml_output=True, include_comments=False)
    # outputs main content without comments as XML ...


The use of fallback algorithms can also be bypassed in fast mode:

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, no_fallback=True)


.. code-block:: python

    # shorter alternative to import and use the functions
    >>> from trafilatura import fetch_url, extract
    >>> extract(fetch_url('...'))


On the command-line
-------------------


URLs can be used directly (-u/--URL):

.. code-block:: bash

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...
    $ trafilatura -h
    # displays help message

You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    $ cat myfile.html | trafilatura # use the contents of an already existing file
    $ < myfile.html trafilatura # same here


For more information please refer to `usage documentation <usage.html>`_ and `tutorials <tutorials.html>`_.

