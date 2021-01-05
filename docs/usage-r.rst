With R
======


Introduction
------------


`R <https://www.r-project.org/>`_ is a free software environment for statistical computing and graphics. The `reticulate <https://rstudio.github.io/reticulate>`_ package provides a comprehensive set of tools for interoperability between Python and R.

``Trafilatura`` has to be installed with `pip <installation.html>`_, `conda <https://docs.conda.io/en/latest/>`_, or `py_install <https://rstudio.github.io/reticulate/reference/py_install.html>`_. Skip the installation of  Miniconda if it doesn't seem necessary, you should only be prompted once; or see `Installing Python Packages <https://rstudio.github.io/reticulate/articles/python_packages.html>`_.

Complete vignette: `Calling Python from R <https://rstudio.github.io/reticulate/articles/calling_python.html>`_.


Download and extraction
-----------------------

Text extraction from HTML documents (including downloads) is available in a straightforward way:

.. code-block:: R

    # getting started
    > install.packages("reticulate")
    > library(reticulate)
    > trafilatura <- import("trafilatura")
    # get a HTML document as string
    > url <- "https://example.org/"
    > downloaded <- trafilatura$fetch_url(url)
    # extraction
    > trafilatura$extract(downloaded)
    [1] "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\nMore information..."
    # extraction with arguments
    > trafilatura$extract(downloaded, output_format="xml", url=url)
    [1] "<doc sitename=\"example.org\" title=\"Example Domain\" source=\"https://example.org/\" hostname=\"example.org\" categories=\"\" tags=\"\" fingerprint=\"lxZaiIwoxp80+AXA2PtCBnJJDok=\">\n  <main>\n    <div>\n      <head>Example Domain</head>\n      <p>This domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.</p>\n      <p>More information...</p>\n    </div>\n  </main>\n  <comments/>\n</doc>"

For a full list of arguments see `extraction documentation <corefunctions.html#extraction>`_.

Already stored documents can also be read directly from R, for example with CSV/TSV output and ``read_delim()``, see information on `data import in R <https://r4ds.had.co.nz/data-import.html>`_.


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
    ...
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
    ...


Going further
-------------

- `Basic Text Processing in R <https://programminghistorian.org/en/lessons/basic-text-processing-in-r>`_
- `Quanteda <https://quanteda.io>`_ is an R package for managing and analyzing text:
   - `Quickstart <https://quanteda.io/articles/pkgdown/quickstart.html>`_
   - `Quanteda tutorials <https://tutorials.quanteda.io/>`_
   - `Advancing Text Mining with R and quanteda <https://www.r-bloggers.com/2019/10/advancing-text-mining-with-r-and-quanteda/>`_

