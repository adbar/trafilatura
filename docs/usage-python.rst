Usage with Python
=================



See here for a `beginner's guide <https://wiki.python.org/moin/BeginnersGuide>`_, a `Python Tutorial <https://docs.python.org/3/tutorial/index.html>`_, and `the Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_.

https://docs.python.org/3/tutorial/
https://www.techbeamers.com/python-tutorial-step-by-step/
https://www.freecodecamp.org/news/best-python-tutorial/



Quickstart
----------

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


Usage
-----


.. code-block:: python

    >>> import trafilatura
    >>> downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    >>> downloaded is None # assuming the download was successful
    False
    >>> result = trafilatura.extract(downloaded) # trafilatura.process_record is deprecated but works
    >>> print(result)
    # newlines preserved, TXT output ...
    >>> result = trafilatura.extract(downloaded, xml_output=True)
    >>> print(result)
    # some formatting preserved in basic XML structure ...

The only required argument is the input document (here a downloaded HTML file), the rest is optional.

The inclusion of tables and comments can be deactivated at a function call. The use of a fallback algorithm (currently `jusText <https://github.com/miso-belica/jusText>`_) can also be bypassed in *fast* mode:

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, include_comments=False) # no comments in output
    >>> result = trafilatura.extract(downloaded, include_tables=False) # skip tables examination
    >>> result = trafilatura.extract(downloaded, no_fallback=True) # skip justext algorithm used as fallback

This values combined probably provide the fastest execution times:

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)

The input can consist of a previously parsed tree (i.e. a *lxml.html* object), which is then handled seamlessly:

.. code-block:: python

    >>> from lxml import html
    >>> mytree = html.fromstring('<html><body><article><p>Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></article></body></html>')
    >>> trafilatura.extract(mytree)
    'Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n'

Experimental feature: the target language can also be set using 2-letter codes (`ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_), there will be no output if the detected language of the result does not match and no such filtering if the identification component has not been installed (see above for installation instructions).

.. code-block:: python

    >>> result = trafilatura.extract(downloaded, url, target_language='de')

All currently available options, along with their default values:

.. code-block:: python

    >>> trafilatura.extract(downloaded, url=None, record_id=None, no_fallback=False, include_comments=True, output_format='txt', csv_output=False, json_output=False, xml_output=False, tei_output=False, tei_validation=False, target_language=None, include_tables=True, include_formatting=False, deduplicate=True, date_extraction_params=None, with_metadata=False, url_blacklist={})

The function ``bare_extraction`` can be used to bypass output conversion, it returns Python variables for  metadata (dictionary) as well as main text and comments (both LXML objects).

.. code-block:: python

    >>> from trafilatura.core import bare_extraction
    >>> bare_extraction(downloaded)

For more see the `core functions <corefunctions.html>`_ page.

For further configuration see the variables in ``settings.py`` and re-compile the package locally.


Date extraction
---------------

Among metadata extraction, dates are handled by an external module: `htmldate <https://github.com/adbar/htmldate>`_. `Custom parameters <https://htmldate.readthedocs.io/en/latest/corefunctions.html#handling-date-extraction>`_ can be passed through the extraction function or through the ``extract_metadata`` function in ``trafilatura.metadata``, most notably: ``extensive_search`` (boolean), to activate pattern-based opportunistic text search,  ``original_date`` (boolean) to look for the original publication date, ``outputformat`` (string), to provide a custom datetime format, and ``max_date`` (string), to set the latest acceptable date manually (YYYY-MM-DD format).
