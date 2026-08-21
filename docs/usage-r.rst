Usage with R
============

.. meta::
    :description lang=en:
        Trafilatura extends its download and extractions capabilities to the R community.
        Discover how to use Trafilatura in your R projects with this dedicated guide.


Introduction
------------


R is a free software environment for statistical computing and graphics. `Reticulate <https://rstudio.github.io/reticulate/>`_ is an R package that enables easy interoperability between R and Python. With Reticulate, you can import Python modules as if they were R packages and call Python functions from R.

This allows R users to leverage the vast array of Python packages and tools and basically allows for execution of Python code inside an R session. Python packages can then be used with minimal adaptations rather than having to go back and forth between languages and environments.


Installation
------------

Both R and Python installed on your system, for the latter see `installation page <installation.html>`_.


Reticulate
^^^^^^^^^^

The reticulate package can be easily installed from CRAN and then loaded into your R session:

.. code-block:: R

    > install.packages("reticulate")
    > library(reticulate)


A recent version of Python is necessary. Some systems already have such an environment installed, to check it just run the following command in a terminal window:

.. code-block:: bash

    $ python3 --version
    Python 3.10.12 # version 3.10 or higher is fine


By default, reticulate will use the Python executable found on your system's PATH. You can use the ``use_python()`` function to set the Python version and path that you want to use: ``use_python("/path/to/python/executable")``.

You can also use the ``py_config()`` function to check your current Python configuration.


Trafilatura
^^^^^^^^^^^

The most convenient way to install Python packages is to use the `reticulate::py_install() <https://rstudio.github.io/reticulate/reference/py_install.html>`_ function. Of course ``Trafilatura`` can also be installed with `pip <installation.html>`_ as any other Python package. Skip the installation of Miniconda if it doesn't seem necessary, you should only be prompted once; or see `Installing Python Packages <https://rstudio.github.io/reticulate/articles/python_packages.html>`_.

Here is a simple example using the ``py_install()`` function included in ``reticulate``:

.. code-block:: R

    > library(reticulate)
    > py_install("trafilatura")

Here is how to do it with the ``pip`` Python package manager:

.. code-block:: bash

    $ pip install trafilatura


Once you have installed a Python package, you can use it from R with the ``import()`` function.


Download and extraction
-----------------------

This section demonstrates how to use functions in a R environment. Beyond the examples below, all functions in these documentation pages should be available as well.


R syntax
^^^^^^^^

Text extraction from HTML documents (including downloads) is available in a straightforward way:

.. code-block:: R

    # getting started
    > install.packages("reticulate")
    > library(reticulate)

    # loading the Trafilatura module
    > trafilatura <- import("trafilatura")

    # fetching a web page
    > url <- "https://example.org/"
    > downloaded <- trafilatura$fetch_url(url)

    # extracting the text content
    > text <- trafilatura$extract(downloaded)
    > cat(text)
    [1] "This domain is for use in documentation examples without needing permission. Avoid use in operations.\nLearn more"

    # extraction with arguments
    > trafilatura$extract(downloaded, output_format="xml", url=url)
    [1] "<doc fingerprint=\"bcbae6b725d8d3f0\">\n  <main>\n    <p>This domain is for use in documentation examples without needing permission. Avoid use in operations.</p>\n    <p>Learn more</p>\n  </main>\n  <comments/>\n</doc>"

For a full list of arguments see `extraction documentation <corefunctions.html#extraction>`_. R's ``TRUE``/``FALSE`` are passed through transparently as Python booleans, so extraction options work exactly as in Python:

.. code-block:: R

    > trafilatura$extract(downloaded, include_comments=FALSE, with_metadata=TRUE)

Already stored documents can also be read directly from R, for example with CSV/TSV output and ``read_delim()``, see information on `data import in R <https://r4ds.had.co.nz/data-import.html>`_.

The ``html2txt`` function extracts all possible text on the webpage, it can be used as follows:

.. code-block:: R

    > trafilatura$html2txt(downloaded)


Structured access with ``bare_extraction()``
""""""""""""""""""""""""""""""""""""""""""""

``bare_extraction()`` returns a ``Document`` object rather than a plain dict (since version 2.0, see the `deprecations page <deprecations.html>`_). Individual fields are readable directly through reticulate's generic attribute access, no conversion needed:

.. code-block:: R

    > doc <- trafilatura$bare_extraction(downloaded, with_metadata=TRUE)
    > doc$title
    [1] "Example Domain"

Printing the whole object directly only shows a generic Python reference (``<trafilatura.settings.Document object at 0x...>``); call ``$as_dict()`` first if you want a tidy R list of every field at once, as shown further below for ``extract_metadata()``.


Processing multiple pages
^^^^^^^^^^^^^^^^^^^^^^^^^^

Failed downloads return Python's ``None``, which reticulate converts to R's ``NULL`` — check for it before extracting. This is also the natural way to build a small corpus from R, using ``sapply()`` or ``lapply()``:

.. code-block:: R

    > urls <- c("https://www.tensorflow.org/", "https://pytorch.org/")
    > results <- sapply(urls, function(u) {
    +     downloaded <- trafilatura$fetch_url(u)
    +     if (is.null(downloaded)) return(NA)
    +     text <- trafilatura$extract(downloaded)
    +     if (is.null(text)) NA else nchar(text)
    + })
    > results
    https://www.tensorflow.org/        https://pytorch.org/
                            1739                        2836

For larger crawls, see `download web pages <downloads.html>`_ for throttled, multi-threaded downloads — the same functions are reachable from R as `Other functions`_ below. A custom configuration (e.g. adjusting extraction thresholds) can also be built and passed the same way, see `settings and customization <settings.html>`_.


Python syntax
^^^^^^^^^^^^^

For more complex operations beyond simple function calls, you can use ``py_run_string()`` to run arbitrary Python code:


.. code-block:: R

    > py_run_string("import trafilatura")
    > url <- "https://www.example.com"
    > py_run_string(paste0("result = trafilatura.fetch_url('", url, "')"))
    > py_run_string("result = trafilatura.extract(result)")
    > result <- py$result


Other functions
---------------

Specific parts of the package can also be imported on demand, which provides access to functions not directly exported by the package. For a list of relevant functions and arguments see `core functions <corefunctions.html>`_.


.. code-block:: R

    # using the code for link discovery in sitemaps
    > sitemapsfunc <- py_run_string("from trafilatura.sitemaps import sitemap_search")
    > sitemapsfunc$sitemap_search("https://www.sitemaps.org/")
    [1] "https://www.sitemaps.org"
    [2] "https://www.sitemaps.org/protocol.html"
    [3] "https://www.sitemaps.org/faq.html"
    [4] "https://www.sitemaps.org/terms.html"
    # and so on...

    # import the metadata part of the package as a function
    > metadatafunc <- py_run_string("from trafilatura.metadata import extract_metadata")
    > downloaded <- trafilatura$fetch_url("https://github.com/rstudio/reticulate")

    # extract_metadata() returns a Document object rather than a plain dict since
    # version 2.0 (see the deprecations page); call as_dict() to get a tidy R list
    > metadatafunc$extract_metadata(downloaded)$as_dict()
    $title
    [1] "GitHub - rstudio/reticulate: R Interface to Python"

    $author
    [1] "Rstudio"

    $url
    [1] "https://github.com/rstudio/reticulate"

    $hostname
    [1] "github.com"
    # and so on...


Going further
-------------

By combining the web scraping capabilities of Trafilatura with the data analysis capabilities of R, you can create powerful workflows for extracting and analyzing data from web pages.


Further resources:

- Complete vignette: `Calling Python from R <https://rstudio.github.io/reticulate/articles/calling_python.html>`_.
- Tutorial showing how to import a Python scraper and use the results directly with the usual R syntax: `Web scraping with R: Text and metadata extraction  <https://adrien.barbaresi.eu/blog/web-scraping-text-metadata-r.html>`_.


Working with the content:

- `Basic Text Processing in R <https://programminghistorian.org/en/lessons/basic-text-processing-in-r>`_

.. seealso::
    `Python usage <usage-python.html>`_, `Core functions <corefunctions.html>`_
