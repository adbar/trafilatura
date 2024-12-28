With R
======

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
    Python 3.10.12 # version 3.6 or higher is fine


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
    [1] "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\nMore information..."

    # extraction with arguments
    > trafilatura$extract(downloaded, output_format="xml", url=url)
    [1] "<doc sitename=\"example.org\" title=\"Example Domain\" source=\"https://example.org/\" hostname=\"example.org\" categories=\"\" tags=\"\" fingerprint=\"lxZaiIwoxp80+AXA2PtCBnJJDok=\">\n  <main>\n    <div>\n      <head>Example Domain</head>\n      <p>This domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.</p>\n      <p>More information...</p>\n    </div>\n  </main>\n  <comments/>\n</doc>"

For a full list of arguments see `extraction documentation <corefunctions.html#extraction>`_.

Already stored documents can also be read directly from R, for example with CSV/TSV output and ``read_delim()``, see information on `data import in R <https://r4ds.had.co.nz/data-import.html>`_.

The ``html2txt`` function extracts all possible text on the webpage, it can be used as follows:

.. code-block:: R

    > trafilatura$html2txt(downloaded)


Python syntax
^^^^^^^^^^^^^

You can also use Python functions and objects from R. For example:


.. code-block:: R

    > py_run_string("import trafilatura")
    > url <- "https://www.example.com"
    > py_df <- py_run_string("trafilatura.extract(url)")
    > df <- py_to_r(py_df)


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
    > metadatafunc$extract_metadata(downloaded)
    $title
    [1] "rstudio/reticulate"

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
