Web crawling
============


*New in version 0.9. Still experimental.*


Concept
-------

Intra vs. inter
~~~~~~~~~~~~~~~

A necessary distinction has to be made between intra- and inter-domains crawling:

1. Focused crawling on web-page level: Finding sources within a web page is relatively easy if the page is not too big or too convoluted. For this Trafilatura offers functions to search for links in sitemaps and feeds.
2. Web crawling: Hopping between websites can be cumbersome. Discovering more domains without gathering too much junk or running into bugs is difficult without experience with the subject.

For practical reasons the first solution ("intra") is best, along with "good" (i.e. customized as needed) seeds/sources. As an alternative, prefix searches on the `Common Crawl index <https://index.commoncrawl.org/>`_ can be used.

See `information on finding sources <sources.html>`_ for more details. 


Operation
~~~~~~~~~

The focused crawler aims at the discovery of texts within a websites by exploration and retrieval of links.

This tool is commonly known as (web) `crawler or spider <https://en.wikipedia.org/wiki/Web_crawler>`_. A Web crawler starts with a list of URLs to visit, called the seeds. As the crawler visits these URLs, it identifies all the hyperlinks in the pages and adds them to the list of URLs to visit, called the crawl frontier.

The spider module implements politeness rules as defined by the `Robots exclusion_standard <https://en.wikipedia.org/wiki/Robots_exclusion_standard>`_ where applicable.

It prioritizes navigation pages (archives, categories, etc.) over the rest in order to gather as many links as possible in few iterations.


With Python
-----------

Focused crawler
~~~~~~~~~~~~~~~

The ``focused_crawler`` function integrates all necessary components. It can be adjusted by a series of arguments:

.. code-block:: python

    >>> from trafilatura.spider import focused_crawler

    # starting a crawl
    >>> to_visit, known_urls = focused_crawler('https://www.example.org', max_seen_urls=10, max_known_urls=100000)
    # resuming a crawl
    >>> to_visit, known_urls = focused_crawler(homepage, max_seen_urls=10, max_known_urls=100000, todo=to_visit, known_links=known_urls)

The collected links can then be downloaded and processed. The links to visit (crawl frontier) are stored as a `deque <https://docs.python.org/3/library/collections.html#collections.deque>`_ (a double-ended queue) which mostly works like a list. The known URLs are stored as a set. Both can also be converted to a list if necessary:

.. code-block:: python

    to_visit, known_urls = list(to_visit), sorted(known_urls)


Navigation
~~~~~~~~~~

.. hint::
    You may decide on the course of a crawl by determining if there are still navigation pages to visit:

.. code-block:: python

    from trafilatura.spider import is_still_navigation

    is_still_navigation(to_visit)
    # returns True or False

For more info please refer to the `core functions page <corefunctions.html>`_.


On the command-line
-------------------

On the CLI the crawler automatically works its way through a website, stopping at a maximum of 30 page visits or exhaustion of the total number of pages on the website, whichever comes first.

.. code-block:: bash

    $ trafilatura --crawl "https://www.example.org" > links.txt

It can also explore websites in parallel by reading a list of target sites from a list (``-i``/``--inputfile`` option).


References
----------

Cho, J., Garcia-Molina, H., & Page, L. (1998). Efficient crawling through URL ordering. Computer networks and ISDN systems, 30(1-7), 161-172.

