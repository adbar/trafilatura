Troubleshooting
===============

.. meta::
    :description lang=en:
        Solve common Trafilatura issues: empty output, noisy results, JavaScript pages, download failures, blocking, and performance problems.


.. hint::
    Make sure you have the latest version: ``pip install -U trafilatura``. See also the `list of open issues <https://github.com/adbar/trafilatura/issues>`_.


Debugging
---------

When extraction produces unexpected results, enable verbose logging to see what Trafilatura is doing internally:

**CLI:**

.. code-block:: bash

    # one -v for info messages, -vv for debug
    $ trafilatura -u "https://example.org" -vv

**Python:**

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.DEBUG)

    from trafilatura import fetch_url, extract
    html = fetch_url("https://example.org")
    result = extract(html)

Common log messages and what they mean:

- ``discarding data: ...``: the document was rejected, the preceding messages give the reason.
- ``text and comments not long enough: ...``: the main text is below ``MIN_OUTPUT_SIZE`` and the comments below ``MIN_OUTPUT_COMM_SIZE``. With the default values of 1, this means that no text was found. Try ``favor_recall=True``.
- ``parsed tree length: ..., wrong data type or not valid HTML`` or ``empty HTML tree: ...``: the input could not be parsed as HTML.
- ``too small/incorrect for URL ...`` or ``too large: length ... for URL ...``: the downloaded page or input file is outside the ``MIN_FILE_SIZE`` and ``MAX_FILE_SIZE`` bounds.


Extraction problems
-------------------


Output is empty or ``None``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Walk through these causes in order:

1. **Is the HTML valid?** Pass it to ``load_html()`` first. It returns ``None`` on empty or severely malformed input. It also rejects fragments such as ``<p>x</p>`` if "html" does not occur in the first 50 characters, so wrap them in ``<html><body>...</body></html>``. The parser is lenient, so a result other than ``None`` does not guarantee that the input was HTML.
2. **Is the page JavaScript-rendered?** Trafilatura works on raw HTML. See `Page requires JavaScript`_ below.
3. **Is language filtering active?** If ``target_language`` is set and the detected language doesn't match, ``extract()`` returns ``None``. Remove the filter to test.
4. **Is metadata filtering active?** With ``only_with_metadata=True``, pages missing a title, URL, or date are discarded. Try without it.
5. **Is the text too short?** A document is discarded if its main text is below ``MIN_OUTPUT_SIZE`` and its comments below ``MIN_OUTPUT_COMM_SIZE``. Both are 1 by default, so only empty results are discarded unless you raised them. ``MIN_EXTRACTED_SIZE`` only triggers the fallbacks, it does not discard anything. See `settings.cfg <settings.html#file-structure>`_.
6. **Try relaxing extraction:** ``favor_recall=True`` keeps more content. If the output is still empty, ``html2txt()`` extracts all the text of the page. If even that is empty, the HTML has no text.

.. note::
    Trafilatura is geared towards article pages, blog posts, and main text content. Results vary on link lists, galleries, or catalogs.


Output has too much noise
^^^^^^^^^^^^^^^^^^^^^^^^^

Escalate through these steps:

1. **Use precision mode:** ``extract(html, favor_precision=True)`` or ``--precision`` on the CLI. This prunes comments more aggressively and skips the baseline rescue and recall escalation.

2. **Prune specific elements:** pass XPath expressions to remove known noisy sections:

   .. code-block:: python

       extract(html, favor_precision=True, prune_xpath='//div[@class="sidebar"]')

3. **Modify the element lists:** for site-wide patterns, add elements to ``MANUALLY_CLEANED`` so they're stripped before extraction:

   .. doctest::

       >>> from trafilatura.settings import MANUALLY_CLEANED
       >>> MANUALLY_CLEANED.append("details")  # must use in-place methods

   .. testcleanup::

       MANUALLY_CLEANED.remove("details")

See `settings and customization <settings.html>`_ for more options.


Page requires JavaScript
^^^^^^^^^^^^^^^^^^^^^^^^

Trafilatura works on raw HTML. If a page uses JavaScript to render its content, render it first with a browser automation library and pass the resulting HTML to ``extract()``:

.. code-block:: python

    # example with Playwright
    from playwright.sync_api import sync_playwright
    from trafilatura import extract

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.org")
        html = page.content()
        browser.close()

    text = extract(html)

Alternatives: `nodriver <https://github.com/ultrafunkamsterdam/nodriver>`_ (undetected Chrome automation), `browserforge <https://github.com/daijro/browserforge>`_ (browser fingerprint management).

A browser automation library can also be combined with a paywall-bypass extension to handle cookie walls and paywalls.


Encoding issues
^^^^^^^^^^^^^^^

If the output contains garbled characters (mojibake), the HTML encoding was not detected correctly. Trafilatura handles encoding automatically via ``charset_normalizer``, but edge cases exist:

- **Check the declared charset:** download with ``fetch_response(url, decode=True)`` and look for a charset in ``response.headers.get("content-type")``. If you know the right encoding, decode ``response.data`` yourself and pass the string to ``extract()``.
- **Provide the HTML as a properly decoded string:** if you download with another tool, decode the bytes with the correct encoding before passing them to ``extract()``.
- **Install optional dependencies:** ``pip install trafilatura[all]`` includes ``faust-cchardet``, which adds a second encoding detector.


Download problems
-----------------


Downloads fail or return wrong content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Blocked user agent
  Trafilatura identifies itself in the `User-Agent header <https://en.wikipedia.org/wiki/User-Agent_header>`_. Some websites block it. Set custom user agents with ``USER_AGENTS`` in ``settings.cfg``.

Alternative download library
  ``pip install trafilatura[all]`` installs ``pycurl``, which is then used instead of ``urllib3``. Its different HTTP stack may succeed where ``urllib3`` fails.

Command-line alternatives
  Pipe from another tool: ``wget -O - "https://example.org" | trafilatura`` or ``curl -s "https://example.org" | trafilatura``.

.. note::
    Downloads may fail because your IP or user agent are blocked. Trafilatura's download functions do not bypass such restrictions.


Getting blocked or rate-limited
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Increase delay:** set ``SLEEP_TIME`` in `settings.cfg <settings.html#file-structure>`_ (seconds between requests to the same domain).
- **Set cookies:** in ``settings.cfg``, e.g. ``COOKIE = session=abc123; lang=en``, or point ``COOKIE_FILE`` to a ``cookies.txt`` file in Netscape format.
- **Separate download from extraction:** download pages with a different tool or IP, then process locally with ``--input-dir``. See `downloads page <downloads.html>`_.
- **Use custom user agents:** set ``USER_AGENTS`` in ``settings.cfg``, one is picked at random for each request.

For large-scale collection from existing archives, see `datatrove <https://github.com/huggingface/datatrove/blob/main/examples/process_common_crawl_dump.py>`_ for CommonCrawl processing.


Pages are gone (link rot)
^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``--archived`` on the CLI to automatically query the `Internet Archive <https://web.archive.org/>`_ when downloads fail.

In Python:

.. code-block:: python

    from trafilatura import fetch_url

    downloaded = fetch_url(url)
    if downloaded is None:
        downloaded = fetch_url("https://web.archive.org/web/20/" + url)


Performance problems
--------------------


Memory keeps growing
^^^^^^^^^^^^^^^^^^^^

Trafilatura uses internal caches (deduplication, URL processing) that grow over time. Call ``reset_caches()`` between unrelated batches:

.. doctest::

    >>> from trafilatura.meta import reset_caches
    >>> reset_caches()  # clears all internal caches and triggers garbage collection

See `deduplication <deduplication.html#clearing-the-cache>`_ for details.


Slow processing
^^^^^^^^^^^^^^^

- ``fast=True`` / ``--fast``: skips fallback algorithms, which is faster.
- Disable what you don't need: ``include_comments=False``, ``include_tables=False``.
- ``--parallel N``: use several threads for downloads and processes for extraction (CLI).
- In Python, combine ``load_download_buffer()`` and ``buffered_downloads()`` for parallel downloads, see `downloads <downloads.html>`_.


.. seealso::
    `FAQ <faq.html>`_, `Settings and customization <settings.html>`_, `How extraction works <extraction-overview.html>`_
