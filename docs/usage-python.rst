With Python
===========


The Python programming language
-------------------------------

Python can be easy to pick up whether you're a first time programmer or you're experienced with other languages:

-  Official `Python Tutorial <https://docs.python.org/3/tutorial/>`_
-  `The Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_
-  `Learn Python Programming Step by Step <https://www.techbeamers.com/python-tutorial-step-by-step/>`_
-  `The Best Python Tutorials (freeCodeCamp) <https://www.freecodecamp.org/news/best-python-tutorial/>`_


Usage
-----

Quickstart
^^^^^^^^^^

.. code-block:: python

    >>> import trafilatura
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> trafilatura.extract(downloaded)
    # outputs main content and comments as plain text ...
    >>> trafilatura.extract(downloaded, xml_output=True, include_comments=False)
    # outputs main content without comments as XML ...

.. code-block:: python

    # shorter alternative to import and use the functions
    >>> from trafilatura import fetch_url, extract
    >>> extract(fetch_url('...'))


Step-by-step
^^^^^^^^^^^^


.. code-block:: python

    >>> from trafilatura import fetch_url, extract
    >>> downloaded = fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> downloaded is None # assuming the download was successful
    False
    >>> result = extract(downloaded)
    >>> print(result)
    # newlines preserved, TXT output ...
    >>> result = extract(downloaded, xml_output=True)
    >>> print(result)
    # some formatting preserved in basic XML structure ...

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

The inclusion of tables and comments can be deactivated at a function call. The use of a fallback algorithm (currently `jusText <https://github.com/miso-belica/jusText>`_) can also be bypassed in *fast* mode:

.. code-block:: python

    # no comments in output
    >>> result = extract(downloaded, include_comments=False)
    # skip tables examination
    >>> result = extract(downloaded, include_tables=False)
    # skip justext algorithm used as fallback
    >>> result = extract(downloaded, no_fallback=True)

This values combined probably provide the fastest execution times:

.. code-block:: python

    >>> result = extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)


LXML objects
^^^^^^^^^^^^

The input can consist of a previously parsed tree (i.e. a *lxml.html* object), which is then handled seamlessly:

.. code-block:: python

    >>> from lxml import html
    >>> mytree = html.fromstring('<html><body><article><p>Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></article></body></html>')
    >>> extract(mytree)
    'Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n'


Language identification
^^^^^^^^^^^^^^^^^^^^^^^

Experimental feature: the target language can also be set using 2-letter codes (`ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_), there will be no output if the detected language of the result does not match and no such filtering if the identification component has not been installed (see above for installation instructions).

.. code-block:: python

    >>> result = extract(downloaded, url, target_language='de')


Customization
^^^^^^^^^^^^^

All currently available options, along with their default values:

``trafilatura.extract(downloaded, url=None, record_id=None, no_fallback=False, include_comments=True, output_format='txt', csv_output=False, json_output=False, xml_output=False, tei_output=False, tei_validation=False, target_language=None, include_tables=True, include_images=False, include_formatting=False, deduplicate=False, date_extraction_params=None, with_metadata=False, max_tree_size=None, url_blacklist=None, settingsfile=None, config=<configparser.ConfigParser object>)``

The function ``bare_extraction`` can be used to bypass output conversion, it returns Python variables for  metadata (dictionary) as well as main text and comments (both LXML objects).

.. code-block:: python

    >>> from trafilatura import bare_extraction
    >>> bare_extraction(downloaded)

For more see the `core functions <corefunctions.html>`_ page.

The standard `settings file <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.cfg>`_ can be modified. It currently entails variables related to text extraction.

.. code-block:: python

    >>> from trafilatura.settings import use_config
    >>> myconfig = use_config('path/to/myfile')
    >>> extract(downloaded, config=myconfig)

For further configuration `clone the repository <https://docs.github.com/en/free-pro-team@latest/github/using-git/which-remote-url-should-i-use>`_, edit ``settings.py`` and reinstall the package locally (``pip install -U .`` in the home directory of the cloned repository).


Extraction settings
-------------------

Text extraction
^^^^^^^^^^^^^^^

Text extraction can be parametrized by providing a custom configuration file (that is a variant of `settings.cfg <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.cfg>`_) with the ``config`` parameter in ``bare_extraction`` or ``extract``, which overrides the standard settings:

.. code-block:: python

    >>> from trafilatura import extract
    >>> from trafilatura.settings import use_config
    # load the new settings by providing a file name
    >>> newconfig = use_config("myfile.cfg")
    # use with a previously downloaded document
    >>> extract(downloaded, config=newconfig)
    # provide a file name directly (can be slower)
    >>> extract(downloaded, settingsfile="myfile.cfg")


Date extraction
^^^^^^^^^^^^^^^

Among metadata extraction, dates are handled by an external module: `htmldate <https://github.com/adbar/htmldate>`_. `Custom parameters <https://htmldate.readthedocs.io/en/latest/corefunctions.html#handling-date-extraction>`_ can be passed through the extraction function or through the ``extract_metadata`` function in ``trafilatura.metadata``, most notably:

-  ``extensive_search`` (boolean), to activate pattern-based opportunistic text search,
-  ``original_date`` (boolean) to look for the original publication date,
-  ``outputformat`` (string), to provide a custom datetime format,
-  ``max_date`` (string), to set the latest acceptable date manually (YYYY-MM-DD format).

.. code-block:: python

    >>> from trafilatura import extract
    # pass the new parameters as dict, with a previously downloaded document
    >>> extract(downloaded, output_format="xml", date_extraction_params={"extensive_search": True, "max_date": "2018-07-01"})

