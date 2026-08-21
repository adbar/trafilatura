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

- Graphical user interface removed (was deprecated since v1.12)
- Output format must be specified via ``--output-format`` or format shorthands (``--json``, ``--xml``, etc.)
- Explicit exports through ``__all__`` in the package


Changes in v2.1
^^^^^^^^^^^^^^^^

- Python 3.8 and 3.9 support dropped (minimum is now 3.10)


For the full version history, see the `changelog <https://github.com/adbar/trafilatura/blob/master/HISTORY.md>`_.

.. seealso::
    `Installation <installation.html>`_, `Python usage <usage-python.html>`_, `Command-line usage <usage-cli.html>`_
