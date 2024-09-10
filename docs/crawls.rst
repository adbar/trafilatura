Web crawling
============

.. meta::
    :description lang=en:
        Dive deep into the web with Python and on the command-line. Trafilatura supports
        focused crawling, enforces politeness rules, and navigates through websites.


A tool aiming at the discovery of links by exploration and retrieval is commonly known as (web) crawler or spider. This process involves traversing the web to extract information and identify hyperlinks (URLs) for further exploration. A crawler keeps track of and permanently sorts the links seen in order to get to new leads. Essentially, a crawler is a sort of a virtual librarian which catalogues information.

Prominent operators of web crawlers include search engine companies, which use them to build their search indexes. Additional applications include web archiving, data mining, and text analytics. In linguistic research, they can be used to build web corpora.

Efficient techniques are essential to optimize resource utilization. Trafilatura supports focused crawling, adhering to politeness rules, and efficiently navigating through links. This page shows how to perform these tasks with Python and on the command-line.



Design decisions
----------------

Intra vs. inter
~~~~~~~~~~~~~~~

A necessary distinction has to be made between intra-domain and inter-domains crawling:

1. Focused crawling on website level: Finding sources within a website is relatively straightforward if it is not too rich in links or too convoluted.
2. Broad web crawling: Hopping across multiple websites can be challenging as it requires navigating diverse domains without accumulating irrelevant data or running into technical issues.

Trafilatura offers functions to support both approaches. In practice, intra-domain crawling is often the more feasible option, especially when paired with carefully curated sources.

Another viable alternative is leveraging existing data from external crawling projects. See `information on finding sources <sources.html>`_ for more details. 


Concept and operation
~~~~~~~~~~~~~~~~~~~~~

Crawling starts with a seed list of URLs to visit. As these pages are downloaded, a parsing module extracts specific elements. The crawler identifies relevant hyperlinks present on the pages and adds them to the list of URLs to visit, called the frontier.

The crawl frontier is initially populated with the seed set. Visited pages are removed from the frontier. A filter is applied to determine whether the extracted links should be included, prioritizing navigation pages (such as archives or categories) to maximize link gathering in few iterations. The resulting links are then added to the frontier.


.. hint::
    See also the documentation page `Compendium: Web texts in linguistics and humanities <compendium.html>`_ for more details. 


Characteristics
~~~~~~~~~~~~~~~

The spider module implements politeness rules as defined by the Robots Exclusion Standard, where applicable.

Duplicate removal is also implemented, which involves both URL- and text-level analysis. This allows the crawler to detect and avoid revisiting previously crawled URLs or web pages with identical content.

It is safe to crawl a fairly high number of websites and pages per host, bounding factors are time (waiting between requests on the same host), bandwidth (for concurrent downloads), and RAM (above millions of URLs to track).


With Python
-----------

Focused crawler
~~~~~~~~~~~~~~~

The ``focused_crawler()`` function integrates all necessary components and can be customized using various arguments. To use it, you will need to import the corresponding module and call the function with a URL to start from (``homepage`` parameter). The function also accepts optional parameters:

* ``max_seen_urls``: the maximum number of pages to visit (default: 10)
* ``max_known_urls``: the maximum number of pages to "know" about (default: 100000)
* ``todo``: provide a previously generated list of pages to visit (i.e. a crawl frontier)
* ``known_links``: provide a list of previously known pages
* ``lang``: try to target links according to language heuristics (two-letter code)

The following example demonstrates how to set up a focused crawler to extract internal links from a given website:


.. code-block:: python

    >>> from trafilatura.spider import focused_crawler

    # perform the first iteration (will not work with this website, there are no internal links)
    >>> to_visit, known_links = focused_crawler("https://example.org", max_seen_urls=1)



Step by step
~~~~~~~~~~~~

The function returns two values, a snapshot of the current crawling state. Since the collected links can be downloaded and processed at a later time, it is recommended to progress in a step-by-step manner to save and examine data between runs.

The ``to_visit`` variable keeps track of what is ahead and the ``known_links`` variable ensures that the same pages are not visited twice. As this requirement can vary depending on the use case (e.g. checking new pages every day on a homepage) these variables are optional. Other parameters include ``config`` (see settings file) and ``rules`` (politeness rules, defaults to the ones provided by the website or safe values).


.. code-block:: python

    # perform another iteration using previously collected information
    >>> to_visit, known_links = focused_crawler("https://example.org", max_seen_urls=10, max_known_urls=100000, todo=to_visit, known_links=known_links)


In this example, the crawler stops after seeing a maximum of 10 URLs or registering a total of 100,000 URLs on the website, whichever comes first. Setting both parameters to high values can result in a significant increase in processing time.

You can also use a custom configuration and pass politeness rules to the crawler. For more information see the `documentation of the function <corefunctions.html#trafilatura.spider.focused_crawler>`_.

You can determine the course of a crawl by checking if there are still navigation pages to visit using the ``is_still_navigation()`` function:


.. code-block:: python

    >>> from trafilatura.spider import is_still_navigation

    >>> is_still_navigation(to_visit)
    # returns True or False

For more info please refer to the `core functions page <corefunctions.html>`_.



On the command-line
-------------------

Two options are available on the command-line:

* ``--crawl`` : crawl a fixed number of pages within the website
* ``--explore`` : combination of sitemap and crawl (uses sitemaps if possible)

On the CLI the crawler automatically works its way through a website, stopping at a maximum of 30 page visits or exhaustion of the total number of pages on the website, whichever comes first.

.. code-block:: bash

    $ trafilatura --crawl "https://www.example.org" > links.txt

It can also crawl websites in parallel by reading a list of target sites from a list using the ``-i``/``--input-file`` option.

.. note::
    The ``--list`` option does not apply here. Unlike with the ``--sitemap`` or ``--feed`` options, the URLs are simply returned as a list instead of being retrieved and processed. This allows for examination of the collected URLs prior to further downloads. For more information on refining and filtering URL collections, see the underlying `courlan package <https://github.com/adbar/courlan>`_.



Further reading
---------------

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
