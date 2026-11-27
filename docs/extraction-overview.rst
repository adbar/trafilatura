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
       │                    then re-run of stages 1–3 with the recall settings
       ▼
    Output text + metadata


Stages
------

Cleaning
^^^^^^^^

Before extraction begins, the HTML tree is simplified:

- Elements like ``<script>``, ``<style>``, ``<nav>``, ``<footer>`` are removed
- The lists ``MANUALLY_CLEANED`` (removed with content) and ``MANUALLY_STRIPPED`` (tags removed, text kept) control what is discarded, see `settings <settings.html>`_
- If comments are not requested, comment sections are removed at this stage (except on forum threads, where they may be the content)


Main extraction
^^^^^^^^^^^^^^^

The rule-based extractor uses XPath expressions to find the element holding the main content, such as an article body. It prunes boilerplate inside it, for example navigation and link-heavy sections, then keeps the content-bearing elements: paragraphs, headings, lists, tables, quotes and code.

If the result is empty or too short (below ``MIN_EXTRACTED_SIZE``), a "wild-text recovery" step collects paragraphs and other elements that these rules missed.


Fallback cascade
^^^^^^^^^^^^^^^^

The result of the main extraction is compared with two external algorithms:

- **readability** (a port of Mozilla's Readability.js) — good at identifying article bodies, tried on every page, its result is kept if it is much longer or if the main result lacks paragraphs
- **jusText** (a built-in minimal version) — classifies text blocks by length, link density and context, reaches content buried in nested structures, tried if the result is still too short (below ``MIN_EXTRACTED_SIZE`` in ``settings.cfg``) or contains boilerplate elements, its result is kept if it is longer or if it drops this boilerplate

In recall mode, the comparison is skipped for texts over ten times ``MIN_EXTRACTED_SIZE``.

This stage is **skipped in fast mode** (``fast=True`` / ``--fast``), which is why fast mode is quicker but may miss content on difficult pages.

.. versionchanged:: 2.4.0
    Readability is compared on every page and jusText is built in, text output differs from earlier versions.


Baseline rescue
^^^^^^^^^^^^^^^

If the text is still too short (below ``MIN_EXTRACTED_SIZE``), a broad extraction runs on the **original tree**, before the cleaning stage. It takes the first source with enough text among embedded JSON content (such as the article body), article elements, paragraph, code and quote elements, and finally the whole page body. Its result is kept if it is longer. This is a last resort with lower precision, skipped in precision mode.


Recall escalation
^^^^^^^^^^^^^^^^^

This stage runs if the text is short and covers only a small part of the page text, which suggests that content is missing. It has two steps:

1. A jusText candidate is tried on the whole page, since it can reach content that the rules miss. It is kept if it is clearly longer than the current text.
2. Otherwise, stages 1 to 3 are re-run with the recall settings. This result is kept if it is clearly longer and reaches ``MIN_EXTRACTED_SIZE``.

The steps depend on the mode:

- **Standard mode**: both steps, only the second one in fast mode
- **Recall mode**: only the first step, since stages 1 to 3 already ran with the recall settings, nothing in fast mode
- **Precision mode**: stage skipped


Extraction modes
----------------

The ``favor_precision`` and ``favor_recall`` parameters (or CLI flags) shift the balance between precision and recall. Fast mode is independent and can be combined with either of them.

========= ======================================= ==================================
Mode      Python                                  CLI
========= ======================================= ==================================
Standard  ``extract(html)``                       ``trafilatura -u URL``
Precision ``extract(html, favor_precision=True)`` ``trafilatura -u URL --precision``
Recall    ``extract(html, favor_recall=True)``    ``trafilatura -u URL --recall``
Fast      ``extract(html, fast=True)``            ``trafilatura -u URL --fast``
========= ======================================= ==================================

- **Standard**: runs all stages if needed, best overall accuracy
- **Precision**: less text, less noise. Comments and link-heavy sections are pruned more aggressively, baseline rescue and recall escalation are skipped. Use this when results contain too much boilerplate.
- **Recall**: more text, potentially more noise. Lists inside discarded sections and text tails are kept, link density thresholds are relaxed. Use this when parts of documents are missing.
- **Fast**: skips the fallback cascade and the jusText candidate of the recall escalation. It is faster but may miss content on difficult pages.

.. hint::
    To see the difference on a given page, compare the output lengths::

        from trafilatura import fetch_url, extract
        html = fetch_url("https://example.org")
        modes = {"standard": {}, "precision": {"favor_precision": True}, "recall": {"favor_recall": True}}
        for label, args in modes.items():
            result = extract(html, **args)
            print(f"{label:>10}: {len(result) if result else 0} chars")


Metadata
--------

Metadata extraction runs on the page before text extraction. Only the language depends on the extracted text. It looks for:

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
