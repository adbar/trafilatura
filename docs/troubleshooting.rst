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

- ``discarding document``: the extracted text was too short (below ``MIN_OUTPUT_SIZE``). Try ``favor_recall=True`` or lower the threshold in ``settings.cfg``.
- ``not a text document``: the input could not be parsed as HTML.
- ``downloaded document is too small/too large``: the page size is outside ``MIN_FILE_SIZE`` / ``MAX_FILE_SIZE`` bounds.


Extraction problems
-------------------


Output is empty or ``None``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Walk through these causes in order:

1. **Is the HTML valid?** Pass it to ``load_html()`` first — it returns ``None`` on unparseable input.
2. **Is the page JavaScript-rendered?** Trafilatura works on raw HTML. See `Page requires JavaScript`_ below.
3. **Is language filtering active?** If ``target_language`` is set and the detected language doesn't match, ``extract()`` returns ``None``. Remove the filter to test.
4. **Is metadata filtering active?** With ``only_with_metadata=True``, pages missing a title, URL, or date are discarded. Try without it.
5. **Is the text too short?** If the extracted text is below ``MIN_OUTPUT_SIZE`` (default: 1) or ``MIN_EXTRACTED_SIZE`` (default: 250, triggers fallbacks), the result may be empty. Lower these in a custom `settings.cfg <settings.html>`_.
6. **Try relaxing extraction:** ``favor_recall=True`` keeps more content. If still empty, ``html2txt()`` extracts everything — if even that is empty, the HTML has no text.

.. note::
    Trafilatura is geared towards article pages, blog posts, and main text content. Results vary on link lists, galleries, or catalogs.


Output has too much noise
^^^^^^^^^^^^^^^^^^^^^^^^^

Escalate through these steps:

1. **Use precision mode:** ``extract(html, favor_precision=True)`` or ``--precision`` on the CLI. This prunes comments more aggressively and skips fallback stages.

2. **Prune specific elements:** pass XPath expressions to remove known noisy sections:

   .. code-block:: python

       extract(html, favor_precision=True, prune_xpath='//div[@class="sidebar"]')

3. **Modify the element lists:** for site-wide patterns, add elements to ``MANUALLY_CLEANED`` so they're stripped before extraction:

   .. code-block:: python

       from trafilatura.settings import MANUALLY_CLEANED
       MANUALLY_CLEANED.append("aside")  # must use in-place methods

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

- **Force re-encoding:** download with ``fetch_response()`` and check ``response.encoding`` before extraction.
- **Provide the HTML as a properly decoded string:** if you download with another tool, make sure you decode the bytes with the correct encoding before passing to ``extract()``.
- **Install optional dependencies:** ``pip install trafilatura[all]`` includes ``pycurl`` which may handle encoding better for certain servers.


Download problems
-----------------


Downloads fail or return wrong content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Blocked user agent
  Trafilatura identifies itself in the `User-Agent header <https://en.wikipedia.org/wiki/User-Agent_header>`_. Some websites block it. Set a custom user agent in ``settings.cfg``.

Alternative download library
  ``pip install trafilatura[all]`` installs ``pycurl``, which uses a different HTTP stack and may succeed where the default library fails.

Command-line alternatives
  Pipe from another tool: ``wget -O - "https://example.org" | trafilatura`` or ``curl -s "https://example.org" | trafilatura``.

.. note::
    Downloads may fail because your IP or user agent are blocked. Trafilatura's download functions do not bypass such restrictions.


Getting blocked or rate-limited
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Increase delay:** set ``SLEEP_TIME`` in ``settings.cfg`` (default: 5 seconds between requests to the same domain).
- **Set cookies:** in ``settings.cfg``, e.g. ``COOKIE = session=abc123; lang=en``. Or use Python's `cookiejar <https://docs.python.org/3/library/http.cookiejar.html>`_ with ``urllib3``.
- **Separate download from extraction:** download pages with a different tool or IP, then process locally with ``--input-dir``. See `downloads page <downloads.html>`_.
- **Use a custom user agent:** set ``USER_AGENTS`` in ``settings.cfg``.

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

Trafilatura uses internal caches (deduplication, stopwords, URL processing) that grow over time. Call ``reset_caches()`` between unrelated batches:

.. code-block:: python

    from trafilatura.meta import reset_caches
    reset_caches()  # clears all internal caches and triggers garbage collection

See `deduplication <deduplication.html#clearing-the-cache>`_ for details.


Slow processing
^^^^^^^^^^^^^^^

- ``fast=True`` / ``--fast``: skips fallback algorithms, roughly 2× faster.
- Disable what you don't need: ``include_comments=False``, ``include_tables=False``.
- ``--parallel N``: use multiple threads for batch downloads (CLI).
- Use ``load_download_buffer()`` for parallel downloads in Python — see `downloads <downloads.html>`_.


.. seealso::
    `FAQ <faq.html>`_, `Settings and customization <settings.html>`_, `How extraction works <extraction-overview.html>`_
