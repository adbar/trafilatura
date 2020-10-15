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

For a list of arguments accepted by the ``extract`` function, see `core functions <corefunctions.html>`_.


On the command-line
-------------------

.. code-block:: bash

    $ trafilatura -u "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"
    # outputs main content and comments as plain text ...
    $ trafilatura --xml --nocomments -u "URL..."
    # outputs main content without comments as XML ...
    $ trafilatura -h
    usage: trafilatura [-h] [-v] [-vv] [-i INPUTFILE] [--inputdir INPUTDIR]
                   [-o OUTPUTDIR] [-u URL] [--feed [FEED]]
                   [--sitemap [SITEMAP]] [--list] [-b BLACKLIST]
                   [--backup-dir BACKUP_DIR] [--timeout] [--parallel PARALLEL]
                   [--keep-dirs] [-out {txt,csv,json,xml,xmltei}] [--csv]
                   [--json] [--xml] [--xmltei] [--validate] [-f]
                   [--formatting] [--nocomments] [--notables]
                   [--with-metadata] [--target-language TARGET_LANGUAGE]
                   [--deduplicate]


Going further
-------------

For more information, please refer to `usage documentation <usage.html>`_ and `tutorials <tutorials.html>`_.
