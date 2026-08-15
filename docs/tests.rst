Running the tests
=================

.. meta::
    :description lang=en:
        How to run Trafilatura's test suite and code quality checks: pytest, mypy, ruff, and the evaluation gate.

This page regroups the instructions needed to run the test suite and the code
quality checks. Pull requests are only accepted if the changes are tested and if
there are no errors.


Installation
------------

Install Trafilatura along with the development dependencies, ideally in a
virtual environment (for example with ``venv`` or ``pyenv``):

.. code-block:: bash

    $ pip install -e ".[dev]"

The ``dev`` extra pulls in everything required to run the tests and the checks:
``pytest`` (with ``pytest-cov``), ``mypy`` and ``ruff``.


Running the test suite
----------------------

Run the whole test suite from the root of the repository:

.. code-block:: bash

    $ pytest

It is also possible to select a particular test suite, for example
``realworld_tests.py``:

.. code-block:: bash

    $ pytest tests/realworld_tests.py

The test files can also be run directly with Python:

.. code-block:: bash

    $ python3 tests/realworld_tests.py


Type checking and code style
----------------------------

Run static type checks with ``mypy``:

.. code-block:: bash

    $ mypy trafilatura/

Lint and format the code with ``ruff``:

.. code-block:: bash

    $ ruff check .
    $ ruff format trafilatura tests


Benchmark and evaluation
------------------------

If you work on text extraction, it is useful to check whether the performance is
equal or better on the benchmark. The evaluation allows for comparing changes
made to Trafilatura, for example in a new version or pull request.

The quality gate scores the whole benchmark corpus with Trafilatura alone and
exits non-zero if the F1-scores fall below the pinned baseline. It needs no
other extractor and is also run in CI:

.. code-block:: bash

    $ pip install -e ".[all]"
    $ python3 tests/eval_gate.py

The ``all`` extra matches the environment of the CI gate cell; a plain install
can score slightly differently on non-UTF-8 pages. Editing the annotations or an
HTML input requires a re-pin with ``python3 tests/eval_gate.py --update``. A
re-pin never lowers the baseline on its own: a measured F1 below a pinned floor
keeps the floor and exits non-zero, and accepting a lower bar takes an explicit
``--allow-regression``.

On Windows, the corpus fingerprint requires the HTML inputs exactly as
committed: on a clone made before the ``.gitattributes`` rules were added, run
``git add --renormalize .`` and reset (or re-clone) so line endings match the
repository.

Comparing Trafilatura with other extractors needs the ``eval`` extra:

.. code-block:: bash

    $ pip install -e ".[eval]"
    $ python3 tests/evaluate.py --help

Each competitor library is imported only by the algorithm that uses it, so any
algorithm whose library is missing or does not import is reported and dropped
from the comparison instead of stopping the run. The ``magic-html`` package
requires Python 3.12 or later; on older versions it is skipped.

Use ``--small`` to run the Trafilatura-based components only, or ``--all`` to run
all supported algorithms. See the `tests README
<https://github.com/adbar/trafilatura/blob/master/tests/README.rst>`_ for more
information on the evaluation and its data sources.

.. seealso::
    `Installation <installation.html>`_
