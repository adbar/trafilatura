Web crawling
============


*New in version 0.9. Still experimental.*


Concept
-------


A necessary distinction has to be made between intra- and inter-domains crawling:

1. Focused crawling on web-page level: Finding sources within a web page is relatively easy if the page is not too big or too convoluted. For this Trafilatura offers functions to search for links in sitemaps and feeds.
2. Web crawling: Hopping between websites can be cumbersome. Discovering more domains without gathering too much junk or running into bugs is difficult without experience with the subject.

For practical reasons the first solution ("intra") is best, along with "good" (i.e. customized as needed) seeds/sources. As an alternative, prefix searches on the `Common Crawl index <https://index.commoncrawl.org/>`_ can be used.

See `information on finding sources <sources.html>`_ for more details. 


Operation
---------


With Python
~~~~~~~~~~~

The ``focused_crawler`` function implements politeness rules as defined by the `Robots exclusion_standard <https://en.wikipedia.org/wiki/Robots_exclusion_standard>`_ (where applicable). 

.. code-block:: python

    >>> from trafilatura.spider import focused_crawler

    # starting a crawl
    >>> to_visit, known_urls = focused_crawler('https://www.example.org', max_seen_urls=10, max_known_urls=100000)
    # resuming a crawl
    >>> to_visit, known_urls = focused_crawler(homepage, max_seen_urls=10, max_known_urls=100000, todo=to_visit, known_links=known_urls)

The collected links can then be downloaded and processed.

For more info please refer to the `core functions page <corefunctions.html>`_.


On the command-line
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ trafilatura --crawl "https://www.example.org" > links.txt


References
----------

Cho, J., Garcia-Molina, H., & Page, L. (1998). Efficient crawling through URL ordering. Computer networks and ISDN systems, 30(1-7), 161-172.

