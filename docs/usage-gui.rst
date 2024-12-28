Graphical user interface
========================

For users who prefer a visual interface over writing scripts or typing commands, a graphical user interface (GUI) is the recommended option.

Note that the GUI was a feature in Trafilatura until version 1.8.1, but it is currently available in a limited capacity and is no longer actively being developed. Get in touch if you are interested in working towards a more robust or feature-complete version.

If installation fails, usage on the command-line is recommended.


.. hint::
    This interface is removed until further notice starting from Trafilatura version 2, mostly due to issues with cross-platform tests and maintenance.


Installation
~~~~~~~~~~~~


1. Open a terminal window (see the page on the command-line interface in this documentation)
2. Install Python (see the installation page)
3. Install the necessary software versions straight from the repositories by copying the following instructions into the terminal window (use ``pip3`` or ``pip`` otherwise):

   - ``pip3 install -U trafilatura==1.8.1[gui]``
   - Allow some time for the installation to run...



Getting started
~~~~~~~~~~~~~~~

Just type ``trafilatura_gui`` in a terminal window and press the enter key.



Troubleshooting
~~~~~~~~~~~~~~~


Mac OS X:

- ``This program needs access to the screen...`` This problem is related to the way you installed Python or the shell you're running:
    1. Clone the repository and start with "python trafilatura_gui/interface.py" (`source <https://docs.python.org/3/using/mac.html>`_)
    2. `Configure your virtual environment <https://wiki.wxpython.org/wxPythonVirtualenvOnMac>`_ (Python3 and wxpython 4.1.0)


Linux (Debian/Ubuntu):

- ``sudo apt install libgtk-3-dev``
- optional: to save compilation time, use a wxpython wheel from ``https://extras.wxpython.org/wxPython4/extras/`` (e.g. 4.1.0)



Screenshot
~~~~~~~~~~


.. image:: gui-screenshot.png
    :alt: Screenshot of the interface
    :align: center
    :width: 65%
