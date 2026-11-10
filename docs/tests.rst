Running the tests
=================

.. meta::
    :description lang=en:
        How to run Trafilatura's test suite and code quality checks: pytest, mypy, ruff, and the evaluation gate.

This page regroups the instructions needed to run the test suite and the code
quality checks. Pull requests are only accepted if the changes are tested and if
there are no errors. See the `Contributing page
<https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_ for the
rules on issues, pull requests and AI tools.


Installation
------------

Install Trafilatura from the working tree along with the development
dependencies, in a virtual environment:

.. code-block:: bash

    $ uv venv && source .venv/bin/activate
    $ uv pip install -e ".[dev,all]"

Without uv, ``pip install -e ".[dev,all]"`` in any virtual environment works too.
On Windows, activate the environment with ``.venv\Scripts\activate``.

The ``dev`` extra pulls in everything required to run the tests and the checks:
``pytest`` (with ``pytest-cov``), ``mypy`` and ``ruff``. The ``all`` extra
matches the CI environment of the quality gate.


Running the test suite
----------------------

Run the whole test suite from the root of the repository:

.. code-block:: bash

    $ pytest

It is also possible to select a particular test suite, for example
``realworld_tests.py``:

.. code-block:: bash

    $ pytest tests/realworld_tests.py


Type checking and code style
----------------------------

Run static type checks with ``mypy``:

.. code-block:: bash

    $ mypy

Lint the code and check the formatting with ``ruff``:

.. code-block:: bash

    $ ruff check .
    $ ruff format --check .

Drop ``--check`` to let ``ruff format`` fix the formatting in place.


Documentation tests
-------------------

The documentation tests need the ``docs`` extra, which requires Python 3.12 or later:

.. code-block:: bash

    $ uv pip install -e ".[docs]"
    $ pytest docs/docs_tests.py


Benchmark and evaluation
------------------------

If you work on text extraction, report scores before and after on the external
benchmarks listed in `CONTRIBUTING.md
<https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md>`_. The
evaluation allows for comparing changes made to Trafilatura, for example in a
new version or pull request.

The quality gate scores the whole benchmark corpus with Trafilatura alone and
exits non-zero if the F1-scores fall below the pinned baseline. It needs no
other extractor and is also run in CI:

.. code-block:: bash

    $ python tests/eval_gate.py

The gate also checks metadata: for title, author, date, tags and categories,
the share of annotated values found by the metadata extraction must not fall
below its pinned floor.

Without the ``all`` extra, scores can differ slightly on non-UTF-8 pages.
Editing the annotations or an HTML input requires a re-pin with
``python tests/eval_gate.py --update``. A
re-pin never lowers the baseline on its own: a measured F1 below a pinned floor
keeps the floor and exits non-zero, and accepting a lower bar takes an explicit
``--allow-regression``.

On Windows, the corpus fingerprint requires the HTML inputs exactly as
committed: on a clone made before the ``.gitattributes`` rules were added, run
``git add --renormalize .`` and reset (or re-clone) so line endings match the
repository.

Comparing Trafilatura with other extractors needs the ``eval`` extra and Python 3.11+:

.. code-block:: bash

    $ uv pip install -e ".[eval]"
    $ python tests/evaluate.py --help

Each competitor library is imported only by the algorithm that uses it, so any
algorithm whose library is missing or does not import is reported and dropped
from the comparison instead of stopping the run. The ``magic-html`` package
requires Python 3.12 or later; on older versions it is skipped.

Use ``--small`` to run the Trafilatura-based components only, or ``--all`` to run
all supported algorithms. See the `tests README
<https://github.com/adbar/trafilatura/blob/master/tests/README.rst>`_ for more
information on the evaluation and its data sources.

Building the documentation
--------------------------

The documentation needs the ``docs`` extra, which requires Python 3.12 or later. From the root of the repository:

.. code-block:: bash

    $ uv pip install -e ".[docs]"
    $ sphinx-build -b html docs docs/_build


.. seealso::
    `Installation <installation.html>`_
