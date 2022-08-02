Installation
============



Python
------

Trafilatura runs using `Python <https://en.wikipedia.org/wiki/Python_%28programming_language%29>`_, currently one of the most frequently used programming languages.

This software library/package is tested on Linux, macOS and Windows systems. It is compatible with all recent versions of Python:

-  `Installing Python 3 on Mac OS X <https://docs.python-guide.org/starting/install3/osx/>`_ (& `official documentation for Mac <https://docs.python.org/3/using/mac.html>`_)
-  `Installing Python 3 on Windows <https://docs.python-guide.org/starting/install3/win/>`_ (& `official documentation for Windows <https://docs.python.org/3/using/windows.html>`_)
-  `Installing Python 3 on Linux <https://docs.python-guide.org/starting/install3/linux/>`_ (& `official documentation for Unix <https://docs.python.org/3/using/unix.html>`_)
-  Beginners guide: `downloading Python <https://wiki.python.org/moin/BeginnersGuide/Download>`_


Then you need a version of Python to interact with as well as the Python packages needed for the task. A recent version of Python 3 is necessary. Some systems already have such an environment installed, to check it just run the following command in a terminal window:

.. code-block:: bash

    $ python3 --version
    Python 3.8.6 # version 3.6 or higher is fine

In case Python is not installed, please refer to the excellent `Djangogirls tutorial: Python installation <https://tutorial.djangogirls.org/en/python_installation/>`_.



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

    $ pip install trafilatura # pip3 where applicable

This project is under active development, please make sure you keep it up-to-date to benefit from latest improvements:

.. code-block:: bash

    # to make sure you have the latest version
    $ pip install -U trafilatura
    # latest available code base
    $ pip install -U git+https://github.com/adbar/trafilatura.git

On **Mac OS** it can be necessary to install certificates by hand if you get errors like ``[SSL: CERTIFICATE_VERIFY_FAILED]`` while downloading webpages: execute ``pip install certifi`` and perform the post-installation step by clicking on ``/Applications/Python 3.X/Install Certificates.command``. For more information see this `help page on SSL errors <https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error/42334357>`_.


Older Python versions
~~~~~~~~~~~~~~~~~~~~~

- Last version for Python 3.5: ``pip install trafilatura==0.9.3``
- Last version for Python 3.4: ``pip install trafilatura==0.8.2``


Command-line tool
~~~~~~~~~~~~~~~~~


If you installed the library successfully but cannot start the command-line tool, try adding the user-level ``bin`` directory to your ``PATH`` environment variable.
If you are using a Unix derivative (e.g. Linux, OS X), you can achieve this by running the following command: ``export PATH="$HOME/.local/bin:$PATH"``.

For local or user installations where trafilatura cannot be used from the command-line, please refer to `the official Python documentation <https://docs.python.org/3/library/site.html#cmdoption-site-user-base>`_ and this page on `finding executables from the command-line <https://stackoverflow.com/questions/35898734/pip-installs-packages-successfully-but-executables-not-found-from-command-line>`_.


Additional functionality
------------------------

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


cchardet
    Faster encoding detection, also possibly more accurate (especially for encodings used in Asia)
htmldate[all]
    Faster and more precise date extraction with a series of dedicated packages
py3langid
    Language detection on extracted main text
pycurl
    Faster downloads, possibly less robust though
urllib3[brotli]
    Potentially faster file downloads (not essential)



Graphical user interface
------------------------


.. toctree::
   :maxdepth: 2

   installation-gui
