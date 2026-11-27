Deprecations and migration
==========================

.. meta::
    :description lang=en:
        Overview of deprecated features, breaking changes and their replacements, to help upgrade Trafilatura.


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

- ``bare_extraction()`` returns a ``Document`` instead of a dict, use ``.as_dict()`` on it if you need a dictionary, see `Python objects as output <usage-python.html#python-objects-as-output>`_
- ``fetch_url()`` has no ``decode`` argument, use ``fetch_response()`` instead, see `Response object <downloads.html#response-object>`_
- The ``max_tree_size`` argument raises an error, use ``MAX_TREE_SIZE`` in `settings <settings.html#file-structure>`_
- The ``no_fallback`` and ``as_dict`` arguments are deprecated, see `Deprecated arguments`_ below
- Functions and command-line arguments deprecated in 1.x are removed, see `Removed functions and arguments`_ below
- The graphical user interface is removed (last shipped with v1.12)
- The package exports are explicit through ``__all__``

**1.12.0**

- Unknown output formats raise an error instead of falling back to TXT
- ``-out`` is deprecated in favor of ``--output-format`` or format shorthands such as ``--json`` and ``--xml``

**1.11.0**

- **Metadata is no longer extracted by default**, pass ``with_metadata=True`` to ``extract()`` or use ``--with-metadata`` on the CLI, see `metadata <extraction-overview.html#metadata>`_
- ``with_metadata`` and ``--with-metadata`` used to keep only documents with the necessary metadata, this is now ``only_with_metadata`` and ``--only-with-metadata``

**1.10.0**

- Deprecated command-line and function arguments raise an error
- Deduplication functions moved from ``trafilatura.hashing`` to ``trafilatura.deduplication``, see `deduplication <deduplication.html>`_

**1.6.0**

- Content fingerprints use simhash instead of sha1, see `hashing functions <deduplication.html#hashing-functions>`_


Deprecated arguments
--------------------

These arguments still work but issue a warning:

- ``no_fallback`` on ``bare_extraction()`` and ``extract()`` → use ``fast`` instead
- ``bare_extraction(as_dict=True)`` → use the ``.as_dict()`` method on the returned ``Document``


Removed functions and arguments
-------------------------------

Python API:

- ``process_record()`` → use ``extract()``
- ``csv_output()``, ``json_output()``, ``tei_output()``, ``xml_output()`` → use the ``output_format`` parameter on ``extract()``
- ``fetch_url(decode=...)`` → use ``fetch_response()``
- ``decode_response()`` in utils → use ``decode_file()``
- ``trafilatura.hashing`` module → use ``trafilatura.deduplication``
- ``max_tree_size`` parameter → use ``MAX_TREE_SIZE`` in ``settings.cfg``

Command-line interface:

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

- ``--hash-as-name`` is removed, hashes are used as file names by default


For the full version history, see the `changelog <https://github.com/adbar/trafilatura/blob/master/HISTORY.md>`_.

.. seealso::
    `Installation <installation.html>`_, `Python usage <usage-python.html>`_, `Command-line usage <usage-cli.html>`_
