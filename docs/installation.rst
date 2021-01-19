Installation
============


Python
------

Trafilatura runs using `Python <https://en.wikipedia.org/wiki/Python_%28programming_language%29>`_, currently one of the most frequently used programming languages.

This software library/package is tested on Linux, macOS and Windows systems. It is compatible with Python 3 (3.4 upwards):

-  `Installing Python 3 on Mac OS X <https://docs.python-guide.org/starting/install3/osx/>`_ (& `official documentation for Mac <https://docs.python.org/3/using/mac.html>`_)
-  `Installing Python 3 on Windows <https://docs.python-guide.org/starting/install3/win/>`_ (& `official documentation for Windows <https://docs.python.org/3/using/windows.html>`_)
-  `Installing Python 3 on Linux <https://docs.python-guide.org/starting/install3/linux/>`_ (& `official documentation for Unix <https://docs.python.org/3/using/unix.html>`_)
-  Beginners guide: `downloading Python <https://wiki.python.org/moin/BeginnersGuide/Download>`_


Trafilatura package
-------------------

Trafilatura is packaged as a software library available from the package repository `PyPI <https://pypi.org/>`_. As such it can notably be installed with ``pip`` or ``pipenv``.


Installing Python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Straightforward: `Installing packages in python using pip <https://thepythonguru.com/installing-packages-in-python-using-pip/>`_ (& `official documentation <https://pip.pypa.io/en/stable/>`_)
   -  `Using pip on Windows <https://projects.raspberrypi.org/en/projects/using-pip-on-windows/2>`_
-  Advanced: `Pipenv & Virtual Environments <https://docs.python-guide.org/dev/virtualenvs/>`_


Basics
~~~~~~

Please refer to `this section <usage-cli.html#introduction>`_ for an introduction on command-line usage.

.. code-block:: bash

    $ pip install trafilatura # pip3 install on systems where both Python 2 and 3 are installed

This project is under active development, please make sure you keep it up-to-date to benefit from latest improvements:

.. code-block:: bash

    $ pip install -U trafilatura # to make sure you have the latest version
    $ pip install -U git+https://github.com/adbar/trafilatura.git # latest available code (see build status above)

On **Mac OS** it can be necessary to install certificates by hand if you get errors like ``[SSL: CERTIFICATE_VERIFY_FAILED]`` while downloading webpages: execute ``pip install certifi`` and perform the post-installation step by clicking on ``/Applications/Python 3.X/Install Certificates.command``. For more information see this `document <https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error/42334357>`_.


Command-line tool
~~~~~~~~~~~~~~~~~

For local or user installations where trafilatura cannot be used from the command-line, please refer to `the official Python documentation <https://docs.python.org/3/library/site.html#cmdoption-site-user-base>`_ and this page on `finding executables from the command-line <https://stackoverflow.com/questions/35898734/pip-installs-packages-successfully-but-executables-not-found-from-command-line>`_.



Additional functionality
------------------------

A few additional libraries can be installed for extended functionality and faster processing: language detection and faster encoding detection: the ``cchardet`` package may not work on all systems but it is highly recommended.

.. code-block:: bash

    $ pip install cchardet # speed-up only
    $ pip install trafilatura[all] # all additional functionality

For extended date extraction you can use ``pip install htmldate[all]``.

You can also install or update relevant packages separately, *trafilatura* will detect which ones are present on your system and opt for the best available combination.

*For infos on dependency management of Python packages see* `this discussion thread <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe>`_


Graphical user interface
~~~~~~~~~~~~~~~~~~~~~~~~

See `this link <https://github.com/adbar/trafilatura_gui>`_ for installation instructions.
