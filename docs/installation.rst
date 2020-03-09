Installation
============


Python
------

Trafilatura runs using `Python <https://en.wikipedia.org/wiki/Python_%28programming_language%29>`_, currently one of the most frequently used programming languages.

This software library/package is tested on Linux, macOS and Windows systems. It is compatible with Python 3 (3.4 upwards):

-  `Installing Python 3 on Mac OS X <https://docs.python-guide.org/starting/install3/osx/>`_ (& `official documentation <https://docs.python.org/3/using/mac.html>`_)
-  `Installing Python 3 on Windows <https://docs.python-guide.org/starting/install3/win/>`_ (& `official documentation <https://docs.python.org/3/using/windows.html>`_)
-  `Installing Python 3 on Linux <https://docs.python-guide.org/starting/install3/linux/>`_ (& `official documentation <https://docs.python.org/3/using/unix.html>`_)
-  Beginners guide: `downloading Python <https://wiki.python.org/moin/BeginnersGuide/Download>`_


Trafilatura package
-------------------

Trafilatura is packaged as a software library available from the package repository `PyPI <https://pypi.org/>`_. As such it can notably be installed with ``pip`` or ``pipenv``.


Installing Python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Straightforward: `Installing packages in python using pip <https://thepythonguru.com/installing-packages-in-python-using-pip/>`_ (& `official documentation <https://pip.pypa.io/en/stable/>`_)
-  Advanced: `Pipenv & Virtual Environments <https://docs.python-guide.org/dev/virtualenvs/>`_


Basics
~~~~~~

.. code-block:: bash

    $ pip install trafilatura # pip3 install on systems where both Python 2 and 3 are installed

This project is under active development, please make sure you keep it up-to-date to benefit from latest improvements:

.. code-block:: bash

    $ pip install -U trafilatura # to make sure you have the latest version
    $ pip install -U git+https://github.com/adbar/trafilatura.git # latest available code (see build status above)


Additional functionality
~~~~~~~~~~~~~~~~~~~~~~~~

A few additional libraries can be installed for extended functionality and faster processing: language detection (``langid``) and faster processing of downloads (``cchardet``, may not work on all systems).

.. code-block:: bash

    $ pip install trafilatura[all] # all additional functionality

For extended date extraction you can use ``pip install htmldate[all]``.

You can also install or update relevant packages separately, *trafilatura* will detect which ones are present on your system and opt for the best available combination.

*For infos on dependency management of Python packages see* `this discussion thread <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe>`_
