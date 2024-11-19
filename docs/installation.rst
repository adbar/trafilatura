Installation
============

.. meta::
    :description lang=en:
        Setting up Trafilatura is straightforward. This installation guide walks you through the process step-by-step.


This installation guide entails all necessary steps to set up Trafilatura.


Python
------

Trafilatura runs using Python, currently one of the most frequently used programming languages.

It is tested on Linux, macOS and Windows systems and on all recent versions of Python.


- `Djangogirls Installation Tutorial: Python installation <https://tutorial.djangogirls.org/en/python_installation/>`_.
- `Installing Python 3 <https://docs.python-guide.org/starting/installation/>`_


Some systems already have such an environment installed, to check it just run the following command in a terminal window:

.. code-block:: bash

    $ python3 --version  # python can also work
    Python 3.10.12       # version 3.6 or higher is fine


Trafilatura package
-------------------

Trafilatura is packaged as a software library available from the package repository `PyPI <https://pypi.org/>`_. As such it can notably be installed with a package manager like ``pip`` or ``pipenv``.


Installing Python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Straightforward: `Official documentation <https://pip.pypa.io/en/stable/getting-started/>`_
- Advanced: `Pipenv & Virtual Environments <https://docs.python-guide.org/dev/virtualenvs/>`_


Basics
~~~~~~

Here is how to install Trafilatura using pip:

1. Open a terminal or command prompt. Please refer to `this section <usage-cli.html#introduction>`_ for an introduction on command-line usage.
2. Type the following command: ``pip install trafilatura`` (``pip3`` where applicable)
3. Press *Enter*: pip will download and install Trafilatura and its dependencies.

This project is under active development, please make sure you keep it up-to-date to benefit from latest improvements:

.. code-block:: bash

    # to make sure you have the latest version
    $ pip install --upgrade trafilatura
    # latest available code base
    $ pip install --force-reinstall -U git+https://github.com/adbar/trafilatura


.. hint::
    Installation on MacOS is generally easier with `brew <https://formulae.brew.sh/formula/trafilatura>`_.


Older Python versions
~~~~~~~~~~~~~~~~~~~~~

In case this does not happen automatically, specify the version number:

``pip install trafilatura==number``

- Last version for Python 3.6 and 3.7: ``1.12.2``
- Last version for Python 3.5: ``0.9.3``
- Last version for Python 3.4: ``0.8.2``


Command-line tool
~~~~~~~~~~~~~~~~~

If you installed the library successfully but cannot start the command-line tool, try adding the user-level ``bin`` directory to your ``PATH`` environment variable.
If you are using a Unix derivative (e.g. Linux, OS X), you can achieve this by running the following command: ``export PATH="$HOME/.local/bin:$PATH"``.

For local or user installations where trafilatura cannot be used from the command-line, please refer to `the official Python documentation <https://docs.python.org/3/library/site.html#cmdoption-site-user-base>`_ and this page on `finding executables from the command-line <https://stackoverflow.com/questions/35898734/pip-installs-packages-successfully-but-executables-not-found-from-command-line>`_.


Additional functionality
------------------------

Compression
~~~~~~~~~~~

Trafilatura works best if compression modules in the Python standard library are available. If this is not the case the following modules are impacted: processing of compressed HTML data (less coverage), backup HTML storage (CLI), and UrlStore in the underlying courlan library (lesser capacity).


Optional modules
~~~~~~~~~~~~~~~~

A few additional libraries can be installed for extended functionality and faster processing: language detection and faster encoding detection: the ``cchardet`` package may not work on all systems but it is highly recommended.

.. code-block:: bash

    $ pip install cchardet  # single package only
    $ pip install trafilatura[all]  # all additional functionality


*For infos on dependency management of Python packages see* `this discussion thread <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe>`_.


.. hint::
    Everything works even if not all packages are installed (e.g. because installation fails).

    You can also install or update relevant packages separately, *trafilatura* will detect which ones are present on your system and opt for the best available combination.


brotli
    Additional compression algorithm for downloads
cchardet / faust-cchardet (Python >= 3.11)
    Faster encoding detection, also possibly more accurate (especially for encodings used in Asia)
htmldate[all] / htmldate[speed]
    Faster and more precise date extraction with a series of dedicated packages
py3langid
    Language detection on extracted main text
pycurl
    Faster downloads, useful where urllib3 fails
urllib3[socks]
    Downloads through SOCKS proxy with urllib3
zstandard
    Additional compression algorithm for downloads
