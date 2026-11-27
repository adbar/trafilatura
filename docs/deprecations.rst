Deprecations and migration
==========================

.. meta::
    :description lang=en:
        Overview of deprecated features and migration guide for upgrading to Trafilatura v2.


This page consolidates all deprecations and breaking changes to help users upgrade.


Python version support
----------------------

- **v2.1+**: requires Python ≥ 3.10
- **v2.0**: requires Python ≥ 3.8 (dropped 3.6 and 3.7)
- See `installation <installation.html>`_ for last supported versions per Python release.


Breaking changes by version
---------------------------

Changes that can break existing code or alter its results without an error message are in bold.

**2.4.0**

- **Text inside layout tables is removed when tables are turned off**, see `choice of HTML elements <usage-python.html#choice-of-html-elements>`_
- **CSV rows have 18 columns instead of 11**, see `metadata fields <usage-python.html#metadata-fields>`_
- **Without** ``--list``, **the feed or sitemap URL itself is no longer processed**, see `link discovery <usage-cli.html#link-discovery>`_
- **Custom date extraction parameters are merged with the defaults**, see `date <usage-python.html#date>`_
- JSON has no ``raw_text`` field, XML keeps only the attributes Trafilatura sets, the XML-TEI image source is in ``graphic/@url``, see `output formatting <extraction-overview.html#output-formatting>`_
- Revised fallback cascade, text output differs, see `fallback cascade <extraction-overview.html#fallback-cascade>`_
- ``try_justext()`` takes ``options`` instead of ``target_language``, see `core functions <corefunctions.html#try-justext>`_
- jusText is no longer installed with Trafilatura, ``settings.JUSTEXT_LANGUAGES``, ``external.jt_stoplist_init()`` and ``external.get_stoplist()`` are removed
- ``EXTRACTION_TIMEOUT`` is removed from the settings, it had no effect, see `settings <settings.html#file-structure>`_
- Unknown output formats raise a ``ValueError`` instead of an ``AttributeError``, see `output <usage-python.html#output>`_
- A malformed config file exits with code 2, see `exit codes <usage-cli.html#exit-codes>`_
- Removed internal helpers are listed in the `changelog <https://github.com/adbar/trafilatura/blob/master/HISTORY.md>`_

**2.3.0**

- **Requests to non-public addresses such as** ``localhost`` **are blocked by default**, see ``SSRF_PROTECTION`` in `settings <settings.html#file-structure>`_

**2.0.0**

- ``bare_extraction()`` returns a ``Document`` instead of a dict, see `Python objects as output <usage-python.html#python-objects-as-output>`_
- ``fetch_url()`` has no ``decode`` argument, see `Response object <downloads.html#response-object>`_
- The ``max_tree_size`` argument raises an error, use ``MAX_TREE_SIZE`` in `settings <settings.html#file-structure>`_
- See `Migrating to v2`_ below for the other changes

**1.12.0**

- Unknown output formats raise an error instead of falling back to TXT, ``-out`` is deprecated in favor of ``--output-format``

**1.11.0**

- **Metadata is no longer extracted by default**, see `metadata <extraction-overview.html#metadata>`_

**1.10.0**

- Deprecated command-line and function arguments raise an error, see `Command-line interface`_ below
- Deduplication functions moved to ``trafilatura.deduplication``, see `deduplication <deduplication.html>`_

**1.6.0**

- Content fingerprints use simhash instead of sha1, see `hashing functions <deduplication.html#hashing-functions>`_


Migrating to v2
----------------

Trafilatura 2.0 introduced several breaking changes. Here is what to update:


Python API
^^^^^^^^^^

**Removed** (will raise an error):

- ``process_record()`` → use ``extract()``
- ``csv_output()``, ``json_output()``, ``tei_output()``, ``xml_output()`` → use the ``output_format`` parameter on ``extract()``
- ``fetch_url(decode=...)`` → use ``fetch_response()`` instead
- ``decode_response()`` in utils → use ``decode_file()``
- ``trafilatura.hashing`` module → renamed to ``trafilatura.deduplication`` (since v1.10)
- ``max_tree_size`` parameter → moved to ``settings.cfg``

**Deprecated** (still works but will warn):

- ``no_fallback`` parameter on ``bare_extraction()`` and ``extract()`` → use ``fast`` instead
- ``bare_extraction(as_dict=True)`` → the function returns a ``Document`` object, use ``.as_dict()`` method on it

**Changed defaults:**

- ``bare_extraction()`` now returns a ``Document`` object instead of a dict. Use ``.as_dict()`` on the return value if you need a dictionary.
- Metadata is no longer included by default (since v1.11). Pass ``with_metadata=True`` to ``extract()`` or use ``--with-metadata`` on the CLI.

.. note::
    ``with_metadata`` previously had the effect of today's ``only_with_metadata`` (filtering to documents with necessary metadata). It now simply includes metadata in the output.

**Example migration:**

.. code-block:: python

    # Before (v1.x)
    from trafilatura import process_record, fetch_url
    response = fetch_url(url, decode=False)
    result = process_record(response, no_fallback=True)

    # After (v2.x)
    from trafilatura import extract, fetch_response
    response = fetch_response(url)
    result = extract(response.data, url=response.url, fast=True)


Command-line interface
^^^^^^^^^^^^^^^^^^^^^^

The following CLI arguments were renamed or removed:

================================ ================================
Old                              New
================================ ================================
``--nocomments``                 ``--no-comments``
``--notables``                   ``--no-tables``
``--inputfile``                  ``--input-file``
``--inputdir``                   ``--input-dir``
``--outputdir``                  ``--output-dir``
``-out``                         ``--output-format``
================================ ================================

- ``--hash-as-name`` was removed (hashes are used by default).

.. note::
    ``--with-metadata`` previously had the effect of today's ``--only-with-metadata`` (filtering to documents with necessary metadata). It now simply includes metadata in the output.


Other changes in v2
^^^^^^^^^^^^^^^^^^^

- Graphical user interface removed (last shipped with v1.12)
- Output format must be specified via ``--output-format`` or format shorthands (``--json``, ``--xml``, etc.)
- Explicit exports through ``__all__`` in the package


Changes in v2.1
^^^^^^^^^^^^^^^^

- Python 3.8 and 3.9 support dropped (minimum is now 3.10)


For the full version history, see the `changelog <https://github.com/adbar/trafilatura/blob/master/HISTORY.md>`_.

.. seealso::
    `Installation <installation.html>`_, `Python usage <usage-python.html>`_, `Command-line usage <usage-cli.html>`_
