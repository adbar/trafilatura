FAQ
===

.. meta::
    :description lang=en:
        Frequently asked questions about Trafilatura: choosing the right function, batch processing, and customizing extraction.


For diagnostic help (empty output, noisy results, download failures) see `troubleshooting <troubleshooting.html>`_. For JavaScript-rendered pages, see `troubleshooting: page requires JavaScript <troubleshooting.html#page-requires-javascript>`_.


How to extract text from a webpage in Python
--------------------------------------------

.. code-block:: python

    from trafilatura import fetch_url, extract

    downloaded = fetch_url('https://example.org')
    result = extract(downloaded)
    print(result)

``fetch_url()`` downloads the page and ``extract()`` returns its main text content as a string, or ``None`` if extraction fails. Add ``with_metadata=True`` to include title, author, and date in the output, or use ``output_format="json"`` for structured results.

See also: `quickstart <quickstart.html>`_, `Python usage <usage-python.html>`_.


Which extraction function should I use?
---------------------------------------

===============================  ===================  ===============  ===========================================
Function                         Returns              Speed            When to use
===============================  ===================  ===============  ===========================================
``extract()``                    ``str | None``        Standard         Default choice — full cascade, best quality
``extract_with_metadata()``      ``Document | None``   Standard         Shorthand for ``extract()`` with metadata on
``bare_extraction()``            ``Document | None``   Standard         Need structured access to fields (title, author, text, etc.)
``baseline()``                   tuple                 Fast             Quick paragraph extraction, no fallbacks
``html2txt()``                   ``str``               Very fast        All text including boilerplate — last resort
``extract_metadata()``           ``Document``          Fast             Metadata only, no text extraction
===============================  ===================  ===============  ===========================================

``extract()``, ``extract_with_metadata()``, and ``bare_extraction()`` all run the same extraction cascade. The difference is the return type and defaults.

See also: `core functions <corefunctions.html>`_, `how extraction works <extraction-overview.html>`_.


How does Trafilatura compare to BeautifulSoup or Scrapy?
--------------------------------------------------------

These tools solve different problems:

- **BeautifulSoup** is an HTML/XML parser. It gives you low-level access to the DOM — you write the rules to find and extract content yourself. It has no concept of "main content" vs. boilerplate.
- **Scrapy** is a web crawling framework. It handles request scheduling, retries, and pipelines, but extraction logic is up to you (often via CSS selectors or XPath).
- **Trafilatura** is a content extractor. Given an HTML page, it automatically identifies and returns the main text, stripping navigation, ads, and boilerplate. No selectors or rules needed.

Trafilatura can complement both: use Scrapy to crawl and Trafilatura to extract, or parse a page with BeautifulSoup for specific elements while using Trafilatura for the article body.

In `benchmarks <evaluation.html>`_, Trafilatura consistently outperforms other extraction libraries (newspaper3k, jusText, readability-lxml, etc.) in precision, recall, and accuracy on real-world web pages.


How to extract from local HTML files
------------------------------------

**CLI:**

.. code-block:: bash

    # process all files in a directory
    $ trafilatura --input-dir html_files/ -o output/

    # keep the original directory structure in the output
    $ trafilatura --input-dir html_files/ -o output/ --keep-dirs

**Python:**

.. code-block:: python

    from glob import glob
    from trafilatura import extract

    for filepath in glob("html_files/*.html"):
        with open(filepath, encoding="utf-8") as f:
            text = extract(f.read())
        if text:
            print(f"{filepath}: {len(text)} chars")

See also: `process files locally <usage-cli.html#process-files-locally>`_.


How to process many pages efficiently
-------------------------------------

**CLI:**

.. code-block:: bash

    # parallel processing with 4 threads, fast mode, no comments
    $ trafilatura --parallel 4 --fast --no-comments -i urls.txt -o output/

**Python:**

.. code-block:: python

    from trafilatura import extract
    from trafilatura.downloads import add_to_compressed_dict, buffered_downloads, load_download_buffer

    urls = [...]  # your URL list
    url_store = add_to_compressed_dict(urls)

    while url_store.done is False:
        bufferlist, url_store = load_download_buffer(url_store, sleep_time=5)
        for url, html in buffered_downloads(bufferlist, 4):
            if html:
                text = extract(html, fast=True, include_comments=False)

**Tips:**

- ``fast=True`` skips fallback algorithms — roughly 2× faster.
- Disable ``include_comments`` and ``include_tables`` if you don't need them.
- Call ``reset_caches()`` (``from trafilatura.meta import reset_caches``) between unrelated batches to free memory and avoid stale dedup state.
- Respect ``SLEEP_TIME`` in ``settings.cfg`` to avoid getting blocked.

See also: `downloads <downloads.html>`_, `deduplication <deduplication.html#clearing-the-cache>`_.


How to customize what gets extracted
------------------------------------

Three levels of customization, from simplest to most advanced:

**1. Function parameters** — toggle elements on/off per call:

.. code-block:: python

    extract(html, include_comments=False, include_tables=False, include_links=True)

**2. Configuration file** — change thresholds, timeouts, and dedup settings:

.. code-block:: python

    from trafilatura.settings import use_config
    config = use_config("my_settings.cfg")
    extract(html, config=config)

**3. Element lists** — add or remove HTML elements from the cleaning stage:

.. doctest::

    >>> from trafilatura.settings import MANUALLY_CLEANED, MANUALLY_STRIPPED
    >>> MANUALLY_CLEANED.append("section")   # remove <section> and its content
    >>> MANUALLY_STRIPPED.append("span")      # remove <span> tags but keep text

.. testcleanup::

    MANUALLY_CLEANED.remove("section")
    MANUALLY_STRIPPED.remove("span")

.. warning::
    Use in-place methods (``.append()``, ``.remove()``). Reassigning the variable has no effect.

See also: `settings and customization <settings.html>`_, `Extractor class <usage-python.html#function-parameters>`_.


How to use results with pandas or other tools
---------------------------------------------

Use ``bare_extraction()`` for direct access to structured fields:

.. code-block:: python

    from trafilatura import fetch_url, bare_extraction

    html = fetch_url("https://example.org")
    doc = bare_extraction(html)
    data = doc.as_dict()  # {'title': ..., 'author': ..., 'text': ..., ...}

The ``Document`` object has attributes for all extracted fields: ``title``, ``author``, ``date``, ``text``, ``comments``, ``sitename``, ``categories``, ``tags``, and more.

For a DataFrame from multiple URLs, use JSON output:

.. code-block:: python

    import json, pandas as pd
    from trafilatura import fetch_url, extract

    rows = [json.loads(r) for url in urls
            if (html := fetch_url(url))
            and (r := extract(html, output_format="json", with_metadata=True))]
    df = pd.DataFrame(rows)


How to handle large or slow pages
---------------------------------

Three settings in ``settings.cfg`` control resource limits:

- ``MAX_FILE_SIZE = 20000000``: reject input larger than this (bytes). Lower it to skip bloated pages.
- ``MAX_TREE_SIZE``: discard documents with more HTML elements than this (empty = no limit). For example, set it to ``50000`` to prevent extraction from running on huge DOM trees.
- ``EXTRACTION_TIMEOUT = 30``: CLI only — abort extraction after this many seconds. Set to ``0`` to disable (also needed if you see ``signal``-related errors on some platforms).

In Python, pass a custom config:

.. code-block:: python

    from copy import deepcopy
    from trafilatura import extract
    from trafilatura.settings import DEFAULT_CONFIG

    config = deepcopy(DEFAULT_CONFIG)
    config['DEFAULT']['MAX_TREE_SIZE'] = '50000'
    extract(html, config=config)

Using ``fast=True`` also helps — it skips the fallback cascade, which is where most time is spent on complex pages.

See also: `settings and customization <settings.html>`_.


What are common output format gotchas?
--------------------------------------

- **Images** render in every output format once ``include_images=True``, not just XML/Markdown — only the syntax differs: inline ``![alt](src)`` for txt/markdown/json, a dedicated ``<graphic>`` element for xml/xmltei.
- **``include_formatting`` has no effect on JSON output** — it is always serialized as plain text. Trafilatura logs a warning if you set it together with ``output_format="json"``.
- **Headings differ between XML and XML-TEI**: plain ``xml`` output keeps them as ``<head rend="h2">``, while ``xmltei`` converts them to ``<ab type="header">`` to conform to the TEI schema.
- **``favor_precision`` and ``favor_recall``** are not mutually exclusive at the API level — passing both to ``extract()`` (or ``--precision``/``--recall`` on the CLI) does not raise an error. ``favor_recall`` takes precedence, and a warning is logged when both are set.

.. seealso::
    `Troubleshooting <troubleshooting.html>`_, `How extraction works <extraction-overview.html>`_
