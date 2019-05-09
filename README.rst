html-extractor: Extract the main text content of web pages
==========================================================

.. image:: https://img.shields.io/pypi/v/html-extractor.svg
    :target: https://pypi.python.org/pypi/html-extractor

.. image:: https://img.shields.io/pypi/l/html-extractor.svg
    :target: https://pypi.python.org/pypi/html-extractor

.. image:: https://img.shields.io/pypi/pyversions/html-extractor.svg
    :target: https://pypi.python.org/pypi/html-extractor

.. image:: https://img.shields.io/travis/adbar/html-extractor.svg
    :target: https://travis-ci.org/adbar/html-extractor

.. image:: https://img.shields.io/codecov/c/github/adbar/html-extractor.svg
    :target: https://codecov.io/gh/adbar/html-extractor


Robust text extraction and boilerplate removal based on a combination of rules, XPath expressions and HTML tree examination.
Extract the main text content of web pages, including text formatting and page structure. Given a HTML document, it parses it, retrieves the main body text and converts it to XML or plain text.

*Work in progress, first package release ahead.*

:Code:           https://github.com/adbar/html-extractor
:Issue tracker:  https://github.com/adbar/html-extractor/issues
:License:        GNU GPL v3; see LICENSE file

.. contents:: **Contents**
    :backlinks: none


Features
--------

Robust text extraction and boilerplate removal based on a combination of rules, XPath expressions and HTML tree examination.

Because it relies on lxml_, html_extractor is robust and fast.

Preserves text formatting (bold, italic, etc.) and page structure (titles, lists).


Installation
------------

html_extractor is a Python 3 package that is available on PyPI_ and can be installed using ``pip``:

``pip install html_extractor``

(Or use pip3 install ftfy on systems where Python 2 and 3 are both globally installed and pip refers to Python 2.)

Direct installation of the latest version over pip is possible (see `build status <https://travis-ci.org/adbar/html-extractor>`_):

``pip install git+https://github.com/adbar/html-extractor.git``


With Python
-----------

Basic use
~~~~~~~~~

The simplest way to use html_extractor is:


.. code-block:: python

    >>> import html_extractor

    >>> ...




On the command-line
-------------------

A basic command-line interface is included, URLs can be directly used

.. code-block:: bash

    $ html_extractor --URL "https://de.creativecommons.org/index.php/was-ist-cc/"
    $ ... outputs text ...

A HTML response body can also be piped to html-extractor:

.. code-block:: bash

    $ wget -qO- "https://de.creativecommons.org/index.php/was-ist-cc/" | html_extractor

For usage instructions see ``html-extractor -h``


Additional information
----------------------

Context
~~~~~~~

This module is part of methods to derive metadata from web documents in order to build text corpora for computational linguistic and NLP analysis. For more information:

-  Barbaresi, Adrien. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.

Kudos to...
~~~~~~~~~~~

-  `ftfy <https://github.com/LuminosoInsight/python-ftfy>`_
-  `jusText <https://github.com/miso-belica/jusText>`_
-  `lxml <http://lxml.de/>`_


Contact
~~~~~~~

Pull requests are welcome.

See my `contact page <http://adrien.barbaresi.eu/contact.html>`_ for additional details.