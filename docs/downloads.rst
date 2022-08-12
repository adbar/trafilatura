Download web pages
==================


.. meta::
    :description lang=en:
        This Python documentation page shows how to run simple downloads and how to configure and execute
        parallel downloads with threads. The use of politeness rules is also described.

This documentation page shows how to run simple downloads and how to configure and execute parallel downloads with threads. Both single and concurrent downloads should respect basic “politeness” rules which are described below.


A main objective of data collection over the Internet such as web crawling is to efficiently gather as many useful web pages as possible. In order to retrieve multiples web pages at once it makes sense to retrieve as many domains as possible in parallel. However, particular rules apply then.


*New in version 0.9: Functions exposed and made usable for convenience.*


With Python
-----------

Simple downloads
~~~~~~~~~~~~~~~~


Running simple downloads is straightforward with the ``fetch_url()`` fonction. This method is also known as single-threaded downloads as they are processed sequentially.


.. code-block:: python

    from trafilatura.downloads import fetch_url

    # single download
    downloaded = fetch_url('https://www.example.org')

    # sequential downloads using a list
    mylist = ["https://www.example.org", "https://httpbin.org"]
    for url in mylist:
        downloaded = fetch_url(url)
        # do something with it


For efficiency reasons the function makes use of a connection pool where connections are kept open (unless too many websites are retrieved at once). You may see warnings in logs about it which you can safely ignore.


.. note::
    The content (stored here in the variable ``downloaded``) is seamlessly decoded to a Unicode string. This default setting can be bypassed. With the ``decode=False`` parameter ``fetch_url()`` will return a `urllib3 response object <https://urllib3.readthedocs.io/en/latest/user-guide.html#response-content>`_ which can then be processed in a custom fashion.



Trafilatura-backed parallel threads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Threads are a way to run several program parts at once, see for instance `An Intro to Threading in Python <https://realpython.com/intro-to-python-threading/>`_. Multi-threaded downloads are a good option in order to make a more efficient use of the Internet connection. The threads download pages as they go.

.. hint::
    This only makes sense if you are fetching pages from different websites and want the downloads to run in parallel.

The following variant of multi-threaded downloads with throttling is implemented, it also uses a compressed dictionary to store URLs and possibly save space. Both happen seamlessly, here is how to run it:


.. code-block:: python	        

    from trafilatura.downloads import add_to_compressed_dict, buffered_downloads, load_download_buffer

    # list of URLs
    mylist = ['https://www.example.org', 'https://www.httpbin.org/html']
    # number of threads to use
    threads = 4

    backoff_dict = dict() # has to be defined first
    # converted the input list to an internal format
    dl_dict = add_to_compressed_dict(mylist)
    # processing loop
    while dl_dict:
        buffer, threads, dl_dict, backoff_dict = load_download_buffer(dl_dict, backoff_dict)
        for url, result in buffered_downloads(buffer, threads):
            # do something here
            print(result)


This safe but efficient option consists in throttling requests based on domains/websites from which content is downloaded. It is highly recommended!


Asynchronous downloads
~~~~~~~~~~~~~~~~~~~~~~

Asynchronous processing in probably even more efficient in the context of file downloads from a variety of websites. See for instance the `AIOHTTP library <https://docs.aiohttp.org/>`_.


Managing cookies
~~~~~~~~~~~~~~~~

The standard library `cookiejar <https://docs.python.org/3/library/http.cookiejar.html>`_ can be used along ``urllib3`` in order to use cookies along with HTTP requests, see this `documentation pull request <https://github.com/urllib3/urllib3/pull/2474/files>`_.

Alternatively, cookies (ideally not many) can be manually specified in ``settings.cfg``.



On the command-line
-------------------

Downloads on the command-line are automatically run with threads and domain-aware throttling as described above. The following will read URLs from a file, process the results and save them accordingly:

.. code-block:: bash

    # basic output as raw text with backup directory
    $ trafilatura -i list.txt -o txtfiles/ --backup-dir htmlbackup/

For more information, see `page on command-line use <usage-cli.html>`_.


Troubleshooting
---------------

Download issues can be addressed by retrieving the files somewhere else (i.e. from already existing internet archives) or by using another download utility (see ``pycurl`` with Python and ``wget`` or ``curl`` on the command-line), and another IP or network infrastructure.

- Installing the additional download utility ``pycurl`` manually or using ``pip3 install trafilatura[all]`` can alleviate the problem: another download library is used, leading to different results.
- Several alternatives are available on the command-line, e.g. ``wget -O - "my_url" | trafilatura`` instead of ``trafilatura -u "my_url"``.

.. note::
    Downloads may fail because your IP or user agent are blocked. Trafilatura's crawling and download capacities do not bypass such restrictions.


Enforcing politeness rules
--------------------------

Machines consume resources on the visited systems and they often visit sites unprompted. That is why issues of schedule, load, and politeness come into play. Mechanisms exist for public sites not wishing to be crawled to make this known to the crawling agent.

- We want to space out requests to any given server and not request the same content multiple times in a row
- We also should avoid parts of a server that are restricted
- We save time for us and the others if we do not request unnecessary information (see `content-aware URL selection <https://adrien.barbaresi.eu/blog/easy-content-aware-url-filtering.html>`_)



.. note::
    Beware that there should be a tacit scraping etiquette and that a server may block you after the download of a certain number of pages from the same website/domain in a short period of time.

    In addition, some websites may block Trafilatura's `user agent <https://en.wikipedia.org/wiki/User_agent>`_. Thus, the software waits a few seconds between requests per default.


This additional constraint means we have to not only care for download speed but also manage a register of known websites and apply the rules so as to keep maximizing speed while not being too intrusive. Here is how to keep an eye on it.


Robots exclusion standard
~~~~~~~~~~~~~~~~~~~~~~~~~


The `robots.txt` file is usually available at the root of a website (e.g. *www.example.com/robots.txt*). It describes what a crawler should or should not crawl according to the `Robots exclusion_standard <https://en.wikipedia.org/wiki/Robots_exclusion_standard>`_. Certain websites indeed restrict access for machines, for example by the number of web pages or site sections which are open to them.

The file lists a series of rules which define how bots can interact with the websites. It should be fetched from a website in order to test whether the URL under consideration passes the robot restrictions, and these politeness policies should be respected.

Python features a module addressing the issue in its core packages, the gist of its operation is described below, for more see `urllib.robotparser <https://docs.python.org/3/library/urllib.robotparser.html>`_ in the official Python documentation.


.. code-block:: python

    import urllib.robotparser
    from trafilatura import get_crawl_delay
    
    # define a website to look for rules
    base_url = 'https://www.example.org'
    
    # load the necessary components, fetch and parse the file
    rules = urllib.robotparser.RobotFileParser()
    rules.set_url(base_url + '/robots.txt')
    rules.read()

    # determine if a page can be fetched by all crawlers
    rules.can_fetch("*", "https://www.example.org/page1234.html")
    # returns True or False


In addition, some websites may block certain user agents. By replacing the star with one's user agent (e.g. bot name) we can check if we have been explicitly banned from certain sections or from all the website, which can happen when rules are ignored.



Spacing downloads
~~~~~~~~~~~~~~~~~


There should an interval in successive requests to avoid burdening the web servers of interest. That way, you will not slow them down and/or risk getting banned. In addition, Trafilatura includes URLs deduplication.

To prevent the execution of too many requests within too little time, the optional argument ``sleep_time`` can be passed to the ``load_download_buffer()`` function. It is the time in seconds between two requests for the same domain/website.


.. code-block:: python

    from trafilatura.downloads import load_download_buffer

    # 30 seconds is a safe choice
    mybuffer, threads, domain_dict, backoff_dict = load_download_buffer(dl_dict, backoff_dict, sleep_time=30)
    # then proceed as instructed above...


One of the rules that can be defined by a ``robots.txt`` file is the crawl delay (``Crawl-Delay``), i.e. the time between two download requests for a given website. This delay (in seconds) can be retrieved as follows:


.. code-block:: python

    # get the desired information
    seconds = get_crawl_delay(rules)
    # provide a backup value in case no rule exists (happens quite often)
    seconds = get_crawl_delay(rules, default=30)


.. note::
    Trafilatura's focused crawler implements the delay where applicable. For further info and rules see the `documentation page on crawling <crawls.html>`_.



Storing rules
~~~~~~~~~~~~~

You can also decide to store the rules for convenience and later use, for example in a domain-based dictionary:


.. code-block:: python

    # this module comes with trafilatura
    from courlan import extract_domain

    rules_dict = dict()
    # storing information
    domain = extract_domain(base_url)
    rules_dict[domain] = rules
    # retrieving rules info
    seconds = get_crawl_delay(rules_dict[domain])


You can then use such rules with the `crawling module <crawls.html>`_.


Summary
-------

Here is the simplest way to stay polite while taking all potential constraints into account:


1. Read ``robots.txt`` files, filter your URL list accordingly and care for crawl delay
2. Use the framework described above and set the throttling variable to a safe value (your main bottleneck is your connection speed anyway)
3. Optional: for longer crawls, keep track of the throttling info and revisit ``robots.txt`` regularly

