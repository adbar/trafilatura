Running the tests
=================

This page regroups the instructions needed to run the test suite and the code
quality checks. Pull requests are only accepted if the changes are tested and if
there are no errors.


Installation
------------

Install Trafilatura along with the development dependencies, ideally in a
virtual environment (for example with ``venv`` or ``pyenv``):

.. code-block:: bash

    $ pip install trafilatura[dev]

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

Install the evaluation dependencies and run the evaluation script:

.. code-block:: bash

    $ pip install -e ".[eval]"
    $ python3 tests/evaluate.py --help

Use ``--small`` to run the Trafilatura-based components only, or ``--all`` to run
all supported algorithms. See the `tests README
<https://github.com/adbar/trafilatura/blob/master/tests/README.rst>`_ for more
information on the evaluation and its data sources.
