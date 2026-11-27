How extraction works
====================

.. meta::
    :description lang=en:
        How Trafilatura extracts main content from HTML: cleaning, rule-based extraction, readability/jusText fallbacks, and boilerplate removal pipeline.


This page gives a high-level view of what happens when you call ``extract()``. Understanding the pipeline helps when tuning settings or diagnosing unexpected output.


Pipeline at a glance
--------------------

.. code-block:: text

    Input HTML
       │
       ▼
    1. Cleaning ─────────── strip scripts, styles, unwanted elements
       │
       ▼
    2. Main extraction ──── rule-based content detection
       │
       ▼
    3. Fallback cascade ─── comparison with readability + jusText (skipped in fast mode)
       │
       ▼
    4. Baseline rescue ──── if the text is still too short: broad extraction on the original tree
       │
       ▼
    5. Recall escalation ── if the text covers little of the page: jusText candidate,
       │                    then re-run of stages 1–3 with relaxed thresholds
       ▼
    Output text + metadata


Stages
------

Cleaning
^^^^^^^^

Before extraction begins, the HTML tree is simplified:

- Elements like ``<script>``, ``<style>``, ``<nav>``, ``<footer>`` are removed
- The lists ``MANUALLY_CLEANED`` (removed with content) and ``MANUALLY_STRIPPED`` (tags removed, text kept) control what is discarded — see `settings <settings.html>`_
- If comments are not requested, comment-related elements are pruned early


Main extraction
^^^^^^^^^^^^^^^

The core rule-based extractor walks the cleaned tree looking for content-bearing elements. It scores text nodes by length, link density, and position to separate main content from boilerplate.

For short documents, a "wild-text recovery" step looks for text nodes that the standard rules missed.


Fallback cascade
^^^^^^^^^^^^^^^^

The result of the main extraction is compared with two external algorithms:

- **readability** (a port of Mozilla's Readability.js) — good at identifying article bodies, tried on every page, its result is kept if it fits better
- **jusText** (a built-in minimal version) — classifies text blocks by length, link density and context, reaches content buried in nested structures, tried if the result is still too short (below ``MIN_EXTRACTED_SIZE`` in ``settings.cfg``) or contains boilerplate elements

In recall mode, the comparison is skipped for texts over ten times ``MIN_EXTRACTED_SIZE``.

This stage is **skipped entirely in fast mode** (``fast=True`` / ``--fast``), which is why fast mode is quicker but may miss content on difficult pages.

.. versionchanged:: 2.4.0
    Readability is compared on every page and jusText is built in, text output differs from earlier versions.


Baseline rescue
^^^^^^^^^^^^^^^

If the fallbacks still didn't produce enough text (below ``MIN_EXTRACTED_SIZE``), a broad extraction runs on the **original tree** (before the cleaning stage). It takes the first source with enough text among embedded JSON content (such as the article body), article elements, paragraph, code and quote elements, and finally the whole page body. Its result is kept if it is longer. This is a last resort with lower precision.


Recall escalation
^^^^^^^^^^^^^^^^^

If the result is still short relative to the page size, a jusText candidate is tried first, since its algorithm can reach content that rule-based approaches cannot. If it does not clearly outgrow the result, the entire cascade (stages 1–3) is re-run with relaxed thresholds.

In **standard mode**, the jusText candidate comes first (except in fast mode), then the re-run if the candidate is rejected. **Recall mode** only tries the jusText candidate and skips this stage in fast mode. **Precision mode** skips this stage.


Extraction modes
----------------

The ``favor_precision``/``favor_recall`` parameters (or CLI flags) shift the precision/recall balance:

========= ======================================= ==================================
Mode      Python                                  CLI
========= ======================================= ==================================
Standard  ``extract(html)``                       ``trafilatura -u URL``
Fast      ``extract(html, fast=True)``            ``trafilatura -u URL --fast``
Precision ``extract(html, favor_precision=True)`` ``trafilatura -u URL --precision``
Recall    ``extract(html, favor_recall=True)``    ``trafilatura -u URL --recall``
========= ======================================= ==================================

- **Standard** (balanced): runs all stages including recall escalation if needed. Best overall accuracy.
- **Fast**: skips fallback cascade entirely — faster but may miss content on difficult pages.
- **Precision**: less text, less noise. Concretely: more aggressive comment pruning, link-heavy sections discarded, baseline rescue and recall escalation skipped. Use this when results contain too much boilerplate.
- **Recall**: more text, potentially more noise. Concretely: lists inside discarded sections kept, text tails preserved, link density thresholds relaxed. Use this when parts of documents are missing.

.. hint::
    To see the difference on a given page, compare the output lengths::

        from trafilatura import fetch_url, extract
        html = fetch_url("https://example.org")
        for mode in [dict(), dict(favor_precision=True), dict(favor_recall=True)]:
            result = extract(html, **mode)
            label = "precision" if mode.get("favor_precision") else "recall" if mode.get("favor_recall") else "standard"
            print(f"{label:>10}: {len(result) if result else 0} chars")


Metadata
--------

Metadata extraction runs independently of text extraction. It looks for:

- **Title**: ``<title>``, Open Graph, JSON-LD, ``<h1>``
- **Author**: ``<meta>`` tags, JSON-LD, byline patterns
- **Date**: delegated to `htmldate <https://htmldate.readthedocs.io/>`_ which searches meta tags, JSON-LD, and the page text
- **Site name**: Open Graph, ``<meta>`` tags, domain name as fallback
- **Categories and tags**: meta tags, category and tag links in the page (e.g. ``rel="tag"``), JSON-LD
- **Image**: Open Graph and other meta tags, JSON-LD
- **Language**: detected in the text with ``py3langid`` if installed, otherwise as declared in the markup (``<html lang>``, meta tags, JSON-LD)

Metadata is **off by default**. Enable it with ``with_metadata=True`` (Python) or ``--with-metadata`` (CLI).

.. warning::
    .. versionchanged:: 1.11.0
        Metadata is no longer extracted by default.

.. versionchanged:: 2.4.0
    Image and language are in every output format, the language falls back to the one declared in the markup. Categories and tags also come from ``rel`` links, tags from JSON-LD ``keywords``.


Output formatting
-----------------

After extraction, the internal tree is serialized to the requested format:

- **TXT**: plain text, paragraphs separated by line breaks
- **JSON**: text fields plus metadata as a JSON object
- **Markdown**: headings, bold/italic, lists (formatting is automatically enabled with ``output_format='markdown'``), code blocks fenced with their language if the page declares it (e.g. ``class="language-python"``), links with ``include_links=True``
- **XML / XML-TEI**: structured document with paragraph and heading tags
- **CSV / HTML**: tabular or markup output

The metadata fields of each format are listed in `Python usage <usage-python.html#metadata-fields>`_.

.. versionadded:: 2.4.0
    Language of Markdown code blocks.

.. versionchanged:: 2.4.0
    JSON has no ``raw_text`` field, XML keeps only the attributes Trafilatura sets, the XML-TEI image source is in ``graphic/@url``.


.. seealso::
    `Settings and customization <settings.html>`_, `Python usage <usage-python.html>`_, `Benchmarks and evaluation <evaluation.html>`_, `FAQ <faq.html>`_
