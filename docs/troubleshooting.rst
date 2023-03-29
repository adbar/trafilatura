Troubleshooting
===============

.. meta::
    :description lang=en:
        This page explains how to solve common issues about content extraction and downloads.
        They include missing content, paywalls, cookies, and networks.


Content extraction
------------------

Something is missing
^^^^^^^^^^^^^^^^^^^^

The extractor uses several fallbacks to make sure enough text is returned. Content extraction is a tradeoff between precision and recall, that is between desired and undesirable content. Being ready to accept more unwanted text makes it easier to gather more of the relevant text in the output. Here are ways to tackle the issue:

- Opting for ``favor_recall`` (Python) or ``--recall`` (CLI)
- Changing the minimum acceptable length in the settings
- Using the more basic `baseline <corefunctions.html#baseline>`_ or `html2txt <corefunctions.html#html2txt>`_ functions instead (which is also faster)

(see also `reported issues with The New Yorker <https://github.com/adbar/trafilatura/issues?q=is%3Aissue+newyorker>`_)


Beyond raw HTML
^^^^^^^^^^^^^^^

While downloading and processing raw HTML documents is much faster, it can be necessary to fully render the web page before further processing, e.g. because a page makes exhaustive use of JavaScript or because content is injected from multiple sources.

In such cases the way to go is to use a browser automation library like `Playwright <https://playwright.dev/python/>`_. For available alternatives see this `list of headless browsers <https://github.com/dhamaniasad/HeadlessBrowsers>`_.


Bypassing paywalls
^^^^^^^^^^^^^^^^^^

A browser automation library can also be useful to bypass issues related to cookies and paywalls as it can be combined with a corresponding browser extension, e.g. `bypass-paywalls-chrome <https://github.com/iamadamdev/bypass-paywalls-chrome>`_.



Downloads
---------

HTTP library
^^^^^^^^^^^^

Using another download utility (see ``pycurl`` with Python and ``wget`` or ``curl`` on the command-line).

- Installing the additional download utility ``pycurl`` manually or using ``pip3 install trafilatura[all]`` can alleviate the problem: another download library is used, leading to different results.
- Several alternatives are available on the command-line, e.g. ``wget -O - "my_url" | trafilatura`` instead of ``trafilatura -u "my_url"``.

.. note::
    Downloads may fail because your IP or user agent are blocked. Trafilatura's crawling and download capacities do not bypass such restrictions.


Managing cookies
^^^^^^^^^^^^^^^^

The standard library `cookiejar <https://docs.python.org/3/library/http.cookiejar.html>`_ can be used along ``urllib3`` in order to use cookies along with HTTP requests, see this `documentation pull request <https://github.com/urllib3/urllib3/pull/2474/files>`_.

Alternatively, cookies can be manually specified in a ``settings.cfg`` config file, separated by semicolons, e.g. ``COOKIE = yummy_cookie=choco; tasty_cookie=strawberry``.


Web page no longer available on the Internet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download issues can be addressed by retrieving the files somewhere else, i.e. from already existing internet archives like the Internet Archive or the CommonCrawl.


Download first and extract later
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since the they have distinct characteristics it can be useful to separate the infrastructure needed for download from the extraction. Using a custom IP or network infrastructure can also prevent your usual IP from getting banned.

