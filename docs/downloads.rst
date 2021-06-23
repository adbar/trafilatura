Download web pages
==================


*New in version 0.9: Functions exposed and made usable for convenience.*


With Python
-----------

Simple downloads
~~~~~~~~~~~~~~~~


Running simple downloads is straightforward. For efficiency reasons the ``fetch_url()`` fonction makes use of a connection pool where connections are kept open (unless too many websites are taken at once).

.. code-block:: python

    from trafilatura.downloads import fetch_url
    downloaded = fetch_url('https://www.example.org')

The decoding of pages to unicode string is optional, setting ``decode=False`` will return a urllib3 request object.


Using threads
~~~~~~~~~~~~~

Threads are a way to run several program parts at once, see for instance `An Intro to Threading in Python <https://realpython.com/intro-to-python-threading/>`_.

.. caution::
    This only makes sense if you are fetching pages from different websites and want the downloads to run in parallel. Otherwise you could hammer a website with requests and risk getting banned.

Multi-threaded downloads are a good option in order to make a more efficient use of the Internet connection. The threads download pages as they go.


.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, as_completed
    from trafilatura import fetch_url

    # buffer list of URLs
    bufferlist = [] # [url1, url2, ...]

    # download pool: 4 threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in bufferlist}
        # to detect encoding and decode yourself:
        # decode = False
        # future_to_url = {executor.submit(fetch_url, url, decode): url for url in bufferlist}
        for future in as_completed(future_to_url):
            # do something here:
            url = future_to_url[future]
            print(url, future.result())


.. hint::
    A safe but efficient option consists in throttling requests based on domains/websites from which content is downloaded. This method is recommended!

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


Asynchronous
~~~~~~~~~~~~

Asynchronous processing in probably even more efficient in the context of file downloads from a variety of websites. See for instance the `AIOHTTP library <https://docs.aiohttp.org/>`_.


On the command-line
-------------------

Downloads on the command-line are automatically run with threads and domain-aware throttling as described above.



Enforcing politeness rules
--------------------------

To prevent the execution of too many requests within too little time, the optional argument ``sleep_time`` can be passed to the ``load_download_buffer()``. It is the time in seconds between two requests for the same domain/website.

.. code-block:: python

    from trafilatura.downloads import load_download_buffer

    # 30 seconds is a safe choice
    mybuffer = load_download_buffer(dl_dict, backoff_dict, sleep_time=30)


The `Robots exclusion_standard <https://en.wikipedia.org/wiki/Robots_exclusion_standard>`_ is used by some websites to define a series of crawling rules. One of them is the delay, i.e. the time between two download requests for a given website. This delay (in seconds) can be retrieved as follows:


.. code-block:: python

    import urllib.robotparser
    from trafilatura import get_crawl_delay
    
    # define a website to look for rules
    base_url = 'https://www.example.org'
    
    # load the necessary components, fetch and parse the file
    rules = urllib.robotparser.RobotFileParser()
    rules.set_url(base_url + '/robots.txt')
    rules.read()

    # get the desired information
    seconds = get_crawl_delay(rules)
    # provide a backup value in case no rule exists (happens quite often)
    seconds = get_crawl_delay(rules, default=30)


.. info::
    Trafilatura's focused crawler implements the delay where applicable. For further info and rules see the `documentation page on crawling <crawls.html>`_.


.. hint::
    You can also decide to store the rules in a domain-based dictionary for convenience and later use:


.. code-block:: python

    from courlan import extract_domain

    rules_dict = dict()
    # storing information
    domain = extract_domain(base_url)
    rules_dict[domain] = rules
    # retrieving rules info
    seconds = get_crawl_delay(rules_dict[domain])

