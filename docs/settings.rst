Default settings
================

.. meta::
    :description lang=en:
        This documentation page explains how to adjust Trafilatura's default settings
        for downloads and text extraction, along with examples for Python and the command-line.


There are two different files which can be edited in order to modify the default download and extraction settings:

1. ``settings.cfg`` (values designed to be adapted by the user)
2. ``settings.py`` (package-wide settings, advanced)


Configuration file
------------------

Text extraction can be parametrized by providing a custom configuration file which overrides the standard settings. Useful adjustments include download parameters, minimal extraction length, or de-duplication settings.


File structure
^^^^^^^^^^^^^^

The default file included in the package is `settings.cfg <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.cfg>`_ . Important values include:

- Download
   * ``DOWNLOAD_TIMEOUT = 30``: the time (in seconds) before requests are dropped
   * ``SLEEP_TIME = 5``: time between requests (higher is better to avoid detection)
   * ``USER_AGENTS`` and ``COOKIE`` are empty by default
- Extraction
   * ``MIN_EXTRACTED_SIZE = 250``: acceptable size in characters (used to trigger fallbacks)
   * ``MIN_OUTPUT_SIZE = 1``: absolute acceptable minimum for main text output
   * ``MIN_EXTRACTED_COMM_SIZE`` and ``MIN_OUTPUT_COMM_SIZE`` work the same for comment extraction
   * ``EXTRACTION_TIMEOUT = 30``: drop extraction after 30 seconds to prevent malicious HTML bombs, set to 0 if you see errors related to the ``signal`` module and/or use a module such as `defusedxml <https://github.com/tiran/defusedxml>`_
- Deduplication (not active by default)
   * ``MIN_DUPLCHECK_SIZE = 100``: minimum size in characters to run deduplication on
   * ``MAX_REPETITIONS = 2``: maximum number of duplicates allowed


Using a custom file on the command-line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the ``--config-file`` option, followed by the file name or path. All the required variables have to be present in the custom file.


Adapting settings in Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The standard `settings file <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.cfg>`_ can be modified, or a custom configuration file can be provided with the ``config`` parameter to the ``bare_extraction()`` and ``extract()`` functions.

In the following, a single default value is changed, which has an immediate effect on extraction. The resulting text is indeed too short and ends up being discarded. On the contrary, lowering default values can trigger a more opportunistic extraction.

.. code-block:: python

    # load necessary functions and data
    >>> from copy import deepcopy
    >>> from trafilatura import extract
    >>> from trafilatura.settings import DEFAULT_CONFIG

    # a very short HTML file
    >>> my_html = "<html><body><p>Text.</p></body></html>"

    # load the configuration and change the minimum output length
    >>> my_config = deepcopy(DEFAULT_CONFIG)
    >>> my_config['DEFAULT']['MIN_OUTPUT_SIZE'] = '1000'

    # apply new settings, extraction will fail
    >>> extract(my_html, config=my_config)
    >>>
    # default extraction works
    >>> extract(my_html)
    'Text.'


Alternatively, it is possible to override all standard settings by loading a new configuration file where all necessary values have been specified.

.. code-block:: python

    # load the required functions
    >>> from trafilatura import extract
    >>> from trafilatura.settings import use_config

    # load the new settings by providing a file name
    >>> newconfig = use_config("myfile.cfg")

    # use with a previously downloaded document
    >>> extract(downloaded, config=newconfig)

    # provide a file name directly (can be slower)
    >>> extract(downloaded, settingsfile="myfile.cfg")


.. note::
    Useful adjustments include download parameters, minimal extraction length, or de-duplication settings.
    User agent settings can also be specified in a custom ``settings.cfg`` file.


Package settings
----------------

For further configuration it is possible to edit package-wide variables contained in the `settings.py <https://github.com/adbar/trafilatura/blob/master/trafilatura/settings.py>`_ file provided with Trafilatura.

These settings notably include:

- Lists of HTML elements to accept or to discard
- Configuration of parallel processing
- Further download and deduplication settings
- Files written in CLI mode

Here is how to change them:

1. Find the locally installed version of the package or `clone the repository <https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository>`_
2. Edit ``settings.py``
3. Reinstall the package locally: ``pip install --no-deps -U .`` in the home directory of the cloned repository

These remaining variables greatly alter the functioning of the package!
