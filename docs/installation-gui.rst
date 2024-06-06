Installation of graphical user interface
========================================


For users who prefer a visual interface over writing scripts or typing commands, a graphical user interface (GUI) is the recommended option.

Note that the GUI was a feature in Trafilatura until version 1.8.1, but it is currently available in a limited capacity and is no longer actively being developed. Get in touch if you are interested in working towards a more robust or feature-complete version.


Installation
~~~~~~~~~~~~


1. Open a terminal window:
    - `Open the command-line interface <https://tutorial.djangogirls.org/en/intro_to_command_line/#open-the-command-line-interface>`_
2. Install Python:
    - Enter ``python3 --version`` (or if doesn't work ``python --version``) in the terminal window to see if it's already installed (the answer should read ``Python 3.X.X`` where X is a number)
    - `Python installation <https://tutorial.djangogirls.org/en/python_installation/#python-installation>`_
3. Install the necessary software versions straight from the repositories by copying the following instructions into the terminal window (use ``pip3`` or ``pip`` otherwise):
    - ``pip3 install -U trafilatura==1.8.1[gui]``

All instructions for the terminal window are followed by pressing the `enter key <https://en.wikipedia.org/wiki/Enter_key>`_.


.. hint::
    Allow some time for the installation to run.


Getting started
~~~~~~~~~~~~~~~

Just type ``trafilatura_gui`` in a terminal window and press the `enter key <https://en.wikipedia.org/wiki/Enter_key>`_.



Troubleshooting
~~~~~~~~~~~~~~~


Installation and terminal:

- `Introduction to the command-line <https://melaniewalsh.github.io/Intro-Cultural-Analytics/Command-Line/The-Command-Line.html>`_
    - `How to Open a Terminal Window in Mac <https://www.wikihow.com/Open-a-Terminal-Window-in-Mac>`_
    - `How to Open Terminal in Windows <https://www.wikihow.com/Open-Terminal-in-Windows>`_
    - `How to Start Using the Linux Terminal <https://www.howtogeek.com/140679/beginner-geek-how-to-start-using-the-linux-terminal/>`_
- `Installation instructions <https://trafilatura.readthedocs.io/en/latest/installation.html>`_ for *trafilatura*


Mac OS X:

- ``This program needs access to the screen...`` This problem is related to the way you installed Python or the shell you're running:
    1. Clone the repository and start with "pythonw trafilatura_gui/interface.py" (`source <https://docs.python.org/3/using/mac.html#running-scripts-with-a-gui>`_)
    2. `Configure your virtual environment <https://wiki.wxpython.org/wxPythonVirtualenvOnMac>`_ (Python3 and wxpython 4.1.0)


Linux (Debian/Ubuntu):

- ``sudo apt install libgtk-3-dev``
- optional: to save compilation time, use a wxpython wheel from https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ (according to Linux distribution, ``wxpython`` version 4.1.0)


Screenshot
~~~~~~~~~~

.. image:: gui-screenshot.png
    :alt: Screenshot of the interface
    :align: center
    :width: 65%
