trafilatura: Scrapes the main text of web pages while preserving some structure
===============================================================================

.. image:: https://img.shields.io/pypi/v/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python package

.. image:: https://img.shields.io/pypi/l/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python versions

.. image:: https://img.shields.io/travis/adbar/trafilatura.svg
    :target: https://travis-ci.org/adbar/trafilatura
    :alt: Travis build status

.. image:: https://img.shields.io/codecov/c/github/adbar/trafilatura.svg
    :target: https://codecov.io/gh/adbar/trafilatura
    :alt: Code Coverage


:Code:           https://github.com/adbar/trafilatura
:Documentation:  see README file
:Issue tracker:  https://github.com/adbar/trafilatura/issues


*Trafilatura* scrapes the main text of web pages while preserving some structure. The extraction focuses on the main text content, which is usually the part displayed centrally, without the left or right bars, the header or the footer, but including potential titles and comments. All the operations needed from web page download to HTML parsing are handled seamlessly, including scraping and textual analysis.

In a nutshell, with Python:

.. code-block:: python

    >>> import requests, trafilatura
    >>> response = requests.get('https://www.iana.org/about')
    >>> trafilatura.extract(response.text)
    >>> # outputs main content in plain text format ...

On the command-line:

.. code-block:: bash

    $ trafilatura -u https://www.sueddeutsche.de/politik/usa-pompeo-maas-merkel-iran-nordstream-1.4434358
    $ # outputs main content in plain text format ...


.. contents:: **Contents**
    :backlinks: none


Description
-----------

This library performs a robust extraction of main text content and boilerplate removal based on a combination of DOM-based examination, XPath expressions and rules. *Trafilatura* can seamlessly download, parse and convert web documents. It scrapes the main body text while preserving part of the text formatting and page structure, a task also known as web scraping, boilerplate removal or boilerplate detection, DOM-based content extraction, main content identification, web page template detection, web page cleaning, web content extraction, or HTML text cleaning.

Distinguishing between whole page and essential parts can help to alleviate many quality problems related to web texts as it can help with the noise consisting of recurring elements (headers and footers, ads, links/blogroll, etc.) It has to be precise enough not to miss texts or discard valid documents, it also has to be reasonably fast, as it is expected to run in production on millions of documents.

URLs, HTML files or parsed HTML trees are given as input, the result is returned in plain text or XML format. In the latter case, basic formatting elements are preserved such as text formatting (bold, italic, etc.) and page structure (paragraphs, titles, lists), which can be used for further processing.


Features
--------

Because it relies on `lxml <http://lxml.de/>`_, trafilatura is comparatively fast. It is also robust, as the additional generic `jusText algorithm <http://corpus.tools/wiki/Justext>`_ is used as a backup solution.

The result of processing can be in plain text or XML format. In the latter case, basic formatting elements are preserved such as text formatting (bold, italic, etc.) and page structure (paragraphs, titles, lists), which can be used for further processing.

*Work in progress*, currently experimental features:

-  Separate extraction of main text and comments
-  Duplicate detection at paragraph level using a least recently used (LRU) cache
-  Language detection on the extracted content
-  XML output compatible with the recommendations of the Text Encoding Initiative (XML TEI)


Installation
------------

*trafilatura* is a Python package (compatible with Python 3.5 upwards) which is currently tested on Linux and macOS and to some extent on Windows. It is available on `PyPI <https://pypi.org/>`_ and can be installed using ``pip``. (Use ``pip3 install trafilatura`` on systems where both Python 2 and 3 are globally installed.)

Install from package repository: ``pip install trafilatura``

For all experimental functionality please use ``pip install trafilatura[all]``
Most notably: language detection and faster processing of downloads. The ``cchardet`` package is currently not working on some macOS versions.

Direct installation of the latest version (see `build status <https://travis-ci.org/adbar/trafilatura>`_):

``pip install git+https://github.com/adbar/trafilatura.git``

(For infos on dependency management of Python packages see `this discussion thread <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe>`_)


Usage
-----

With Python
~~~~~~~~~~~

Using trafilatura in a straightforward way:

.. code-block:: python

    >>> import requests, trafilatura
    >>> response = requests.get('https://www.iana.org/about')
    >>> result = trafilatura.extract(response.text)
    >>> print(result) # newlines preserved, TXT output
    >>> result = trafilatura.extract(response.text, xml_output=True)
    >>> print(result) # some formatting preserved in basic XML structure

The only required argument is the ``response`` element, the rest is optional.

The inclusion of tables and comments can be deactivated at a function call. The use of a fallback algorithm (currently `jusText <https://github.com/miso-belica/jusText>`_) can also be bypassed in *fast* mode:

.. code-block:: python

    >>> result = trafilatura.extract(response.text, include_comments=False) # no comments in output
    >>> result = trafilatura.extract(response.text, include_tables=True) # skip tables examination
    >>> result = trafilatura.extract(response.text, no_fallback=True) # skip justext algorithm used as fallback
    >>> result = trafilatura.extract(response.text, include_comments=False, include_tables=True, no_fallback=True) # probably the fastest execution

The input can consists of a previously parsed tree (i.e. a *lxml.html* object), which is then handled seamlessly:

.. code-block:: python

    >>> from lxml import html
    >>> mytree = html.fromstring('<html><body><article><p>Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></article></body></html>')
    >>> trafilatura.extract(mytree)
    'Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n'

Experimental feature: the target language can also be set using 2-letter codes (`ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_), there will be no output if the detected language of the result does not match and no such filtering if the identification component has not been installed (see above for installation instructions).

.. code-block:: python

    >>> result = trafilatura.extract(response.text, url, target_language='de')

For further configuration see the variables in ``settings.py``.


On the command-line
~~~~~~~~~~~~~~~~~~~

A command-line interface is included, for general instructions see `Comment Prompt <https://www.lifewire.com/how-to-open-command-prompt-2618089>`_ (tutorial for Windows systems), `How to use the Terminal command line in macOS <https://macpaw.com/how-to/use-terminal-on-mac>`_, or `An introduction to the Linux Terminal <https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal>`_.

URLs can be used directly (``-u/--URL``):

.. code-block:: bash

    $ trafilatura -u https://www.sueddeutsche.de/politik/usa-pompeo-maas-merkel-iran-nordstream-1.4434358
    $ # outputs main content in plain text format ...
    $ trafilatura --xml --URL "https://de.creativecommons.org/index.php/was-ist-cc/"
    $ # outputs main text with basic XML structure ...

You can also pipe a HTML document (and response body) to trafilatura:

.. code-block:: bash

    $ cat 
    $ wget -qO- "https://de.creativecommons.org/index.php/was-ist-cc/" | trafilatura # download 

The ``-i/--inputfile`` option allows for bulk download and processing of a list of URLs from a file listing one link per line. Beware that there should be a tacit scraping etiquette and that a server may block you after the download a certain number of pages from the same website/domain in a short period of time. In addition, some website may block the requests `user-agent <https://en.wikipedia.org/wiki/User_agent>`_. Thus, *trafilatura* waits a few seconds per default between requests.

For all usage instructions see ``trafilatura -h``:

``usage: trafilatura [-h] [-f] [-i INPUTFILE] [--nocomments] [--notables] [--xml] [--xmltei] [-u URL] [-v]``

optional arguments:
  -h, --help         show this help message and exit
  -f, --fast         fast (without fallback detection)
  -i INPUTFILE, --inputfile INPUTFILE
                     name of input file for batch processing
  --nocomments       don't output any comments
  --notables         don't output any table elements
  --xml              XML output
  --xmltei           XML TEI output
  -u URL, --URL URL  custom URL download
  -v, --verbose      increase output verbosity


Further documentation
~~~~~~~~~~~~~~~~~~~~~

To be released soon.

Tutorial video in German by Simon Meier-Vieracker: `Content von Webseiten laden mit Trafilatura <https://www.youtube.com/watch?v=Eei7-8ZQdTc>`_.


Additional information
----------------------

Scientific context
~~~~~~~~~~~~~~~~~~

This module is part of methods to derive information from web documents in order to build text databases for research (chiefly linguistic analysis and natural language processing). A significant challenge resides in the ability to extract and pre-process web texts to meet scientific expectations: Web corpus construction involves numerous design decisions, and this software packages can help facilitate collection and enhance corpus quality.

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg
   :target: https://doi.org/10.5281/zenodo.3460969

-  Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://corpora.linguistik.uni-erlangen.de/data/konvens/proceedings/papers/kaleidoskop/camera_ready_barbaresi.pdf>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, University of Erlangen, 2019.
-  Barbaresi, A. "`The Vast and the Focused: On the need for domain-focused web corpora <https://ids-pub.bsz-bw.de/files/9025/Barbaresi_The_Vast_and_the_Focused_2019.pdf>`_", Proceedings of the `7th Workshop on Challenges in the Management of Large Corpora (CMLC-7) <http://corpora.ids-mannheim.de/cmlc-2019.html>`_, IDS Mannheim, 2019.
-  Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, ACL, 2016.

Name
~~~~

*Trafilatura*: `Italian word <https://en.wiktionary.org/wiki/trafilatura>`_ for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_.

Kudos to...
~~~~~~~~~~~

-  `lxml <http://lxml.de/>`_
-  `jusText <https://github.com/miso-belica/jusText>`_
-  `cchardet <https://github.com/PyYoshi/cChardet>`_ & `ftfy <https://github.com/LuminosoInsight/python-ftfy>`_

Alternatives
~~~~~~~~~~~~

Most corresponding Python packages are not actively maintained, the following alternatives exist:

- `dragnet <https://github.com/dragnet-org/dragnet>`_ features combined and machine-learning approaches, but requires many dependencies as well as extensive tuning
- `python-readability <https://github.com/buriy/python-readability>`_ cleans the page and preserves some markup but is mostly geared towards news texts
- `goose <https://github.com/grangier/python-goose>`_ can extract information for embedded content but doesn't preserve markup and is not maintained
- `html2text <https://github.com/Alir3z4/html2text>`_ converts HTML pages to Markup language and thus keeps the structure, though it doesn't focus on main text extraction

Contact
~~~~~~~

Pull requests are welcome.

See my `contact page <http://adrien.barbaresi.eu/contact.html>`_ for additional details.
