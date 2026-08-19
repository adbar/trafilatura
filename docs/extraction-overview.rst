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
       ├─ enough text? ──→ done
       │
       ▼
    3. Fallback cascade ─── readability + jusText (skipped in fast mode)
       │
       ├─ enough text? ──→ done
       │
       ▼
    4. Baseline rescue ──── broad text extraction on the original tree
       │
       ├─ enough text? ──→ done
       │
       ▼
    5. Recall escalation ── re-run stages 1–3 with relaxed thresholds
       │
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

If the main extraction produced too little text (below ``MIN_EXTRACTED_SIZE`` in ``settings.cfg``), two external algorithms are tried:

- **readability** (a port of Mozilla's Readability.js) — good at identifying article bodies
- **jusText** — good at preserving full sentences, reaches content buried in nested structures

This stage is **skipped entirely in fast mode** (``fast=True`` / ``--fast``), which is why fast mode is roughly twice as quick but may miss content on difficult pages.


Baseline rescue
^^^^^^^^^^^^^^^

If the fallbacks still didn't produce enough text, a broad extraction runs on the **original tree** (before the cleaning stage), grabbing text from paragraph, code, and quote elements. This is a last resort with lower precision.


Recall escalation
^^^^^^^^^^^^^^^^^

If the result is still short relative to the page size, the entire cascade (stages 1–3) is re-run with relaxed thresholds. A separate jusText candidate is also tried, since its algorithm can reach content that rule-based approaches cannot.

This stage only activates in **standard mode** — not in precision or recall mode.


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
- **Fast**: skips fallback cascade entirely — roughly twice as fast but may miss content on difficult pages.
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
- **Categories and tags**: extracted from meta tags and JSON-LD

Metadata is **off by default**. Enable it with ``with_metadata=True`` (Python) or ``--with-metadata`` (CLI).


Output formatting
-----------------

After extraction, the internal tree is serialized to the requested format:

- **TXT**: plain text, paragraphs separated by blank lines
- **JSON**: text fields plus metadata as a JSON object
- **Markdown**: headings, bold/italic, lists, links (formatting is automatically enabled with ``output_format='markdown'``)
- **XML / XML-TEI**: structured document with paragraph and heading tags
- **CSV / HTML**: tabular or markup output


.. seealso::
    `Settings and customization <settings.html>`_, `Python usage <usage-python.html>`_, `Benchmarks and evaluation <evaluation.html>`_, `FAQ <faq.html>`_
