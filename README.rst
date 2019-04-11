html-extractor: ...
==============================================

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


Description here.


.. contents:: **Contents**
    :backlinks: none


Features
--------

Robust text extraction and boilerplate removal based on a combination of rules, XPath expressions and HTML tree examination.


Installation
------------

Direct installation of the latest version over pip is possible (see `build status <https://travis-ci.org/adbar/html-extractor>`_):

``pip install git+https://github.com/adbar/html-extractor.git``


On the command-line
-------------------

A basic command-line interface is included:

.. code-block:: bash

    $ wget -qO- "https://de.creativecommons.org/index.php/was-ist-cc/" | html-extractor

For usage instructions see ``html-extractor -h``


With Python
-----------


Additional information
----------------------

Context
~~~~~~~

This module is part of methods to derive metadata from web documents in order to build text corpora for computational linguistic and NLP analysis. For more information:

-  Barbaresi, Adrien. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.

Kudos to...
~~~~~~~~~~~

-  `jusText <https://github.com/miso-belica/jusText>`_
-  `lxml <http://lxml.de/>`_


Contact
~~~~~~~

Pull requests are welcome.

See my `contact page <http://adrien.barbaresi.eu/contact.html>`_ for additional details.