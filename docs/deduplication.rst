Deduplication
=============

.. meta::
    :description lang=en:
        Duplicate content can harm data quality and efficiency. Trafilatura detects similar texts
        and segments using a LRU cache and locality sensitive hashing (LSH). 



The presence of duplicate content on the web can have detrimental effects on data quality and computational efficiency.

Trafilatura offers two types of duplicate detection: identical segment detection, which works on exact same text parts, and near-duplicate removal, which uses locality-sensitive hashing to identify similar texts.

Duplicate tracking is performed on a per-thread basis. Each thread or process independently keeps track of its own list of duplicates, without relying on centralized information.


.. note::
    The functions habe been regrouped in ``trafilatura.deduplication`` in version 1.10.0 and are not accessible anymore from the ``filters`` or ``hashing`` submodules.


Element and paragraph level
---------------------------


When extracting multiple texts from a website, deduplication helps identify and remove redundant content, such as navigation menus or footers, which are often repeated across the site. This process can be thought of as an automated way to detect boilerplate elements.

While Trafilatura has built-in filters to remove these elements, websites can be highly variable, and some may slip through. The functions in this section provide a way to precisely target and remove repeated segments. Fine-tuning this feature allows for retrieval of more precise textual data..


Extraction functions
^^^^^^^^^^^^^^^^^^^^


The functions ``extract()`` and ``bare_extraction()`` include a parameter to allow for removal of duplicate segments. This option is not activated by default and can be set using two different methods:

- ``deduplicate = True``
- ``options.dedup = True`` (see ``settings.Extractor``)



Custom functions
^^^^^^^^^^^^^^^^

The ``duplicate_test()`` function checks for duplicate text content within an LXML element using a least recently used (LRU) cache mechanism. It evaluates whether the text content of an element has been encountered before and how many times, helping to identify and flag repetitive text based on specified criteria.

Parameters:

- element: LXML element whose text content is to be checked for duplicates.
- options (object): Extractor object containing configuration, must include:

  - ``min_duplcheck_size``: Minimum length of text content to be considered
  - ``max_repetitions``: Maximum number of repetitions allowed for the segment



This snippet sets up options to consider even short segments and not allow any repetitions. The first test returns *False* because the element is new, and the second returns *True* because the element is a duplicate of the previous one.


.. code-block:: python

    >>> from lxml.etree import fromstring
    >>> from trafilatura.deduplication import duplicate_test
    >>> from trafilatura.settings import Extractor

    >>> options = Extractor()
    >>> options.min_duplcheck_size = 0  # even short segments are considered
    >>> options.max_repetitions = 0  # no repetition allowed

    >>> elem = fromstring("<p>Here is text.</p>")
    >>> duplicate_test(elem, options)
    False
    >>> duplicate_test(elem, options)
    True


Document level
--------------


The process begins with text preprocessing, followed by hashing to generate a unique digital fingerprint for each text snippet. Metrics are then applied to quantify the degree of similarity between texts.


Hashing method
^^^^^^^^^^^^^^

The `SimHash <https://en.wikipedia.org/wiki/SimHash>`_ method, also known as Charikar's hash, is used to detect near-duplicate content. It implements a `locality-sensitive hashing <https://en.wikipedia.org/wiki/Locality-sensitive_hashing>`_ approach, which uses a rolling hash and hamming distance comparisons.

The process focuses on meaningful bits of data and allows for efficient comparison and identification of similar content. It offers a balance of speed and accuracy.


Simhash class
^^^^^^^^^^^^^

By setting a similarity threshold, you can use the Simhash class to determine whether two pieces of content are near duplicates.

The similarity method returns a value between 0 and 1, indicating the degree of similarity between the two texts.


.. code-block:: python

    >>> from trafilatura.deduplication import Simhash

    >>> first = Simhash("This is a text.")
    >>> second = Simhash("This is a test.")
    >>> second.similarity(first)
    0.84375


It is also possible to reuse an existing Simhash object by passing its hash value:


.. code-block:: python

    >>> first_copy = Simhash(existing_hash=first.hash)
    >>> first_copy.similarity(first)
    1.0


Hashing functions
^^^^^^^^^^^^^^^^^

The ``content_fingerprint()`` function generates a simhash value for any string without using the class. Instead of the internal integer representation the function returns the hash value as a string of hexadecimal characters.


.. code-block:: python

    >>> from trafilatura.deduplication import content_fingerprint
    >>> content_fingerprint("Here is text.")
    'd2ff47ba297cc254'


The ``generate_hash_filename()`` function takes a string as input and returns a file name-safe string generated by hashing the given content. This approach ensures that identical or nearly identical files receive the same or very similar file names, making it easy to identify and manage them.


.. code-block:: python

    # create a filename-safe string by hashing the given content
    >>> from trafilatura.deduplication import generate_hash_filename
    >>> generate_hash_filename("This is a text.")
    'qAgzZnskrcRgeftk'


Configuration
-------------

The deduplication process can be customized on two different levels:

- Extraction options with ``Extractor()`` object: see example above
- Package-wide settings in ``settings.py``: define cache size with ``LRU_SIZE`` variable
