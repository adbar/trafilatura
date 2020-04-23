Quickstart
==========


With Python
-----------

.. code-block:: python

    >>> import trafilatura
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> trafilatura.extract(downloaded)
    # outputs main content and comments as plain text ...
    >>> trafilatura.extract(downloaded, xml_output=True, include_comments=False)
    # outputs main content without comments as XML ...

For arguments of the ``extract`` function see `core functions <corefunctions.html>`_.


On the command-line
-------------------

.. code-block:: bash

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...
    $ trafilatura --xml --nocomments -u "URL..."
    # outputs main content without comments as XML ...
    $ trafilatura -h
    usage: trafilatura [-h] [-f] [--formatting] [-i INPUTFILE] [-o OUTPUTDIR]
                   [--nocomments] [--notables] [--csv] [--xml] [--xmltei]
                   [--validate] [-u URL] [-v]


For more information please refer to `usage documentation <usage.html>`_ and `tutorials <tutorial1.html>`_.
