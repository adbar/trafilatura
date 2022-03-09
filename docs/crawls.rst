Web crawling
============

.. meta::
    :description lang=en:
        This tutorial shows how to perform web crawling tasks with Python and on the command-line.
        The Trafilatura package allows for easy focused crawling.



A crawler is a computer program that automatically and systematically visits web pages. Crawling implies to send robots across the Web in order to “read” web pages and collect information about them. A web crawler usually searches the visited pages for the links (i.e. URLs) that they entail and follows them through. It keeps track of and permanently sorts the URLs seen in order to get to new websites to visit. Essentially, a crawler is a sort of a virtual librarian which looks for info and catalogues it.

The most well-known operators of web crawlers are companies running web search engines. These programs feed search engines all the information they need to create a (giant) database, the search index.
Another use of web crawlers is in Web archiving, which involves large sets of webpages to be periodically collected and archived.
Other applications include data mining and text analytics, for example building web corpora for linguistic research.


This page shows how to perform certain web crawling tasks with Python and on the command-line. The `trafilatura` package allows for easy focused crawling (see definition below).

..
    Web crawlers require resources to run, so companies want to make sure they are using their resources as efficiently as possible, so they must be selective.


*New in version 0.9. Still experimental.*


Design decisions
----------------

Intra vs. inter
~~~~~~~~~~~~~~~

A necessary distinction has to be made between intra- and inter-domains crawling:

1. Focused crawling on web-page level: Finding sources within a web page is relatively easy if the page is not too big or too convoluted. For this Trafilatura offers functions to search for links in sitemaps and feeds.
2. Web crawling: Hopping between websites can be cumbersome. Discovering more domains without gathering too much junk or running into bugs is difficult without experience with the subject.

For practical reasons the first solution ("intra") is best, along with "good" (i.e. customized as needed) seeds/sources. As an alternative, prefix searches on the `Common Crawl index <https://index.commoncrawl.org/>`_ can be used.

See `information on finding sources <sources.html>`_ for more details. 


Concept and operation
~~~~~~~~~~~~~~~~~~~~~

The focused crawler aims at the discovery of texts within a websites by exploration and retrieval of links. This tool is commonly known as (web) `crawler or spider <https://en.wikipedia.org/wiki/Web_crawler>`_.

A Web crawler starts with a list of URLs to visit, called the seeds. As the crawler visits these URLs, a parsing module extracts specific elements from fetched web pages. The main part of Trafilatura focuses on metadata, text, and comments. The crawler component additionally targets links: it identifies all the hyperlinks present on the pages and adds them to the list of URLs to visit, called the `crawl frontier <https://en.wikipedia.org/wiki/Crawl_frontier>`_.

Initially, the URL frontier contains the seed set. As web pages are visited they are removed from it. The fetched pages are parsed and further internal links are extracted. A URL filter is used to determine whether the extracted links should be included based on one of several tests. It prioritizes navigation pages (archives, categories, etc.) over the rest in order to gather as many links as possible in few iterations. The resulting links are then added to the frontier.

The spider module implements politeness rules as defined by the `Robots exclusion standard <https://en.wikipedia.org/wiki/Robots_exclusion_standard>`_ where applicable.
Duplicate removal is included, which concerns both URL- and text-level analysis. It can register if a URL has already been visited or if a web page with the same content has already been seen at another URL.



With Python
-----------

Focused crawler
~~~~~~~~~~~~~~~

The ``focused_crawler()`` function integrates all necessary components. It can be adjusted by a series of arguments:

.. code-block:: python

    >>> from trafilatura.spider import focused_crawler

    homepage = 'https://www.example.org'
    # starting a crawl
    >>> to_visit, known_urls = focused_crawler(homepage, max_seen_urls=10, max_known_urls=100000)
    # resuming a crawl
    >>> to_visit, known_urls = focused_crawler(homepage, max_seen_urls=10, max_known_urls=100000, todo=to_visit, known_links=known_urls)

Here the crawler stops after seeing a maximum of 10 URLs or registering a total of 100000 URLs on the website, whichever comes first.

The collected links can then be downloaded and processed. The links to visit (crawl frontier) are stored as a `deque <https://docs.python.org/3/library/collections.html#collections.deque>`_ (a double-ended queue) which mostly works like a list. The known URLs are stored as a set. Both can also be converted to a list if necessary:

.. code-block:: python

    to_visit, known_urls = list(to_visit), sorted(known_urls)


You can also use a custom configuration and pass politeness rules to the crawler. For more information see the `documentation of the function <corefunctions.html#trafilatura.spider.focused_crawler>`_.


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

Two different options are available on the command-line:

* ``--crawl`` : crawl a fixed number of pages within the website
* ``--explore`` : combination of sitemap and crawl (uses sitemaps if possible)

On the CLI the crawler automatically works its way through a website, stopping at a maximum of 30 page visits or exhaustion of the total number of pages on the website, whichever comes first.

.. code-block:: bash

    $ trafilatura --crawl "https://www.example.org" > links.txt

It can also crawl websites in parallel by reading a list of target sites from a list (``-i``/``--inputfile`` option).

.. note::
    The ``--list`` option does not apply here. Unlike with the ``--sitemap`` or ``--feed`` options, the URLs are simply returned as a list instead of being retrieved and processed. This happens in order to give a chance to examine the collected URLs prior to further downloads.


References
----------

Boldi, P., Codenotti, B., Santini, M., & Vigna, S. (2004). Ubicrawler: A scalable fully distributed web crawler. Software: Practice and Experience, 34(8), 711-726.

Cho, J., Garcia-Molina, H., & Page, L. (1998). Efficient crawling through URL ordering. Computer networks and ISDN systems, 30(1-7), 161-172.

Cho, J. (2001). Crawling the Web: Discovery and Maintenance of a Large-Scale Web Data, PhD dissertation, Dept. of Computer Science, Stanford University.

Hirai, J., Raghavan, S., Garcia-Molina, H., & Paepcke, A. (2000). WebBase: A repository of web pages. Computer Networks, 33(1-6), 277-293.

Olston, C., & Najork, M. (2010). Web crawling. Now Publishers Inc.

Shkapenyuk, V., & Suel, T. (2002). Design and implementation of a high-performance distributed web crawler. In Proceedings 18th International Conference on Data Engineering (pp. 357-368). IEEE.

..
    <https://onlinelibrary.wiley.com/doi/pdf/10.1002/spe.587>`_
    <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.33.1540&rep=rep1&type=pdf>`_
    <https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.101.5295&rep=rep1&type=pdf>`_
    <https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.29.3140&rep=rep1&type=pdf>`_
    <https://dl.acm.org/doi/abs/10.1561/1500000017>`_
    <https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.13.4762&rep=rep1&type=pdf>`_
