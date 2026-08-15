FAQ
===

.. meta::
    :description lang=en:
        Frequently asked questions about Trafilatura: choosing the right function, batch processing, and customizing extraction.


For diagnostic help (empty output, noisy results, download failures) see `troubleshooting <troubleshooting.html>`_.


Which extraction function should I use?
---------------------------------------

===============================  ==============  ===============  ===========================================
Function                         Returns         Speed            When to use
===============================  ==============  ===============  ===========================================
``extract()``                    ``str | None``  Standard         Default choice — full cascade, best quality
``extract_with_metadata()``      ``str | None``  Standard         Shorthand for ``extract()`` with metadata on
``bare_extraction()``            ``Document``    Standard         Need structured access to fields (title, author, text, etc.)
``baseline()``                   tuple           Fast             Quick paragraph extraction, no fallbacks
``html2txt()``                   ``str``         Very fast        All text including boilerplate — last resort
``extract_metadata()``           ``Document``    Fast             Metadata only, no text extraction
===============================  ==============  ===============  ===========================================

``extract()``, ``extract_with_metadata()``, and ``bare_extraction()`` all run the same extraction cascade. The difference is the return type and defaults.

See also: `core functions <corefunctions.html>`_, `how extraction works <extraction-overview.html>`_.


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
- Call ``reset_caches()`` between unrelated batches to free memory and avoid stale dedup state.
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

.. code-block:: python

    from trafilatura.settings import MANUALLY_CLEANED, MANUALLY_STRIPPED
    MANUALLY_CLEANED.append("section")   # remove <section> and its content
    MANUALLY_STRIPPED.append("span")      # remove <span> tags but keep text

.. warning::
    Use in-place methods (``.append()``, ``.remove()``). Reassigning the variable has no effect.

See also: `settings and customization <settings.html>`_, `Extractor class <usage-python.html#function-parameters>`_.


How to extract from local HTML files
-------------------------------------

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


How to use results with pandas or other tools
----------------------------------------------

**JSON output to DataFrame:**

.. code-block:: python

    import json
    import pandas as pd
    from trafilatura import fetch_url, extract

    urls = ["https://example.org", ...]
    rows = []
    for url in urls:
        html = fetch_url(url)
        if html:
            result = extract(html, output_format="json", with_metadata=True)
            if result:
                rows.append(json.loads(result))

    df = pd.DataFrame(rows)

**Using ``bare_extraction()`` directly:**

.. code-block:: python

    from trafilatura import fetch_url, bare_extraction

    html = fetch_url("https://example.org")
    doc = bare_extraction(html)
    data = doc.as_dict()  # {'title': ..., 'author': ..., 'text': ..., ...}

The ``Document`` object has attributes for all extracted fields: ``title``, ``author``, ``date``, ``text``, ``comments``, ``sitename``, ``categories``, ``tags``, and more.


How to handle large or slow pages
----------------------------------

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


.. seealso::
    `Troubleshooting <troubleshooting.html>`_, `How extraction works <extraction-overview.html>`_
