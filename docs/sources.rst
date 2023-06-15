Finding sources for web corpora
===============================


.. meta::
    :description lang=en:
        This page explains how to look for web pages in a series of sources, from existing URL directories to social networks, including bibliographic and practical information.


From link lists to web corpora
------------------------------


URLs and corpora
~~~~~~~~~~~~~~~~

Getting a list of web pages to start from is essential in order to build document collections. The latter are often called *web corpora* by linguists.

The former lists of links (also known as URL lists) can be used in two different ways: first, to build a corpus straight from the pages they link to, and second, to start web crawls and hopefully discover other relevant pages. On the one hand, corpus sources are restricted to a fixed list, and on the other hand, one looks opportunistically for more content without knowing everything in advance.


The issue with the sources
~~~~~~~~~~~~~~~~~~~~~~~~~~

The question of web corpus sources does not stop there. Indeed, one does not necessarily know where to look for interesting websites, i.e. “seeds” to start from.

The answers to this issue that are frequently found in the literature are twofold: either one initiates a web crawling phase with a (small or large) list of websites, or one uses already existing link collections. Note that both strategies can also complement each other and be used alternatively during different corpus construction phases.


As with “traditional” corpora, web corpora can either focus on a given range of websites and topics, or be merely language-minded and opportunistically take all kinds of possible texts into account. In the latter case, using diverse sources for URL seeds could ensure there is no potentially unknown bias.


Existing resources
------------------

Corpora
~~~~~~~

URL lists from corpus linguistic projects can be a starting ground to derive information from, either to recreate existing corpora or to re-crawl the websites and find new content. If the websites do not exist anymore, the links can still be useful as the corresponding web pages can be retrieved from web archives.

- `Sources for the Internet Corpora <http://corpus.leeds.ac.uk/internet.html>`_ of the Leeds Centre for Translation Studies
- `Link data sets <https://www.webcorpora.org/opendata/links/>`_  of the COW project


URL directories
~~~~~~~~~~~~~~~

- `Overview of the Web archiving community <https://github.com/pirate/ArchiveBox/wiki/Web-Archiving-Community>`_
- `lazynlp list of sources <https://github.com/chiphuyen/lazynlp>`_

DMOZ (now an archive) and Wikipedia work quite well as primary sources:

- `Qualification of URLs extracted from DMOZ and Wikipedia <https://tel.archives-ouvertes.fr/tel-01167309/document#page=189>`_ (PhD thesis section)

..
   https://www.sketchengine.eu/guide/create-a-corpus-from-the-web/



Searching for URLs
~~~~~~~~~~~~~~~~~~

The Common Crawl is a good place to start looking for already known URLs, and possibly for the corresponding pages stored by the project. So is the Internet Archive (with a different focus):

- `CommonCrawl index <https://commoncrawl.org/2015/04/announcing-the-common-crawl-index/>`_
- `cdx_toolkit <https://github.com/cocrawler/cdx_toolkit/>`_ (toolkit for CDX indices such as Common Crawl and the Internet Archive's Wayback Machine) & `Python example <https://github.com/cocrawler/cdx_toolkit/blob/master/examples/iter-and-warc.py>`_
- `Python script <https://gist.github.com/mhmdiaa/adf6bff70142e5091792841d4b372050>`_ to extract all URLs known by the Internet Archive for a given domain


Related info: before retrieving them later, storing web documents in Internet archives can be fruitful, see for instance the tool `archivenow <https://github.com/oduwsdl/archivenow>`_.


With particular filters, one may look for specific kinds of sources as well, here is for instance a regular expression targeting feeds, as used in a `study on web syndication feeds <https://draft.li/blog/2016/03/21/rss-usage-on-the-web/>`_:

.. code-block:: bash

    "(<link[^>]*(?:\s(?:type=[\"']?(application\/rss\+xml|application\/atom\+xml|application\/rss|application\/atom|application\/rdf\+xml|application\/rdf|text\/rss\+xml|text\/atom\+xml|text\/rss|text\/atom|text\/rdf\+xml|text\/rdf|text\/xml|application\/xml)[\"']?|rel=[\"']?(?:alternate)[\"']?))[^>]*>)"

Discovering feeds on social networks can also be used for corpus construction (Minocha et al. 2013).


Search engines
--------------

The BootCat approach (Baroni & Bernardini 2004) uses randomly generated search engines queries and gathers the links in the results (seed URLs). The queries consist of several randomly combined word seeds.

Here is how to make this method work in a modular way:

1. First, you need a list of words in the target language(s). For German see for instance the `DWDS list <https://www.dwds.de/lemma/list>`_.
2. Then, draw random word tuples, e.g. with Python:

.. code-block:: python

    >>> import random
    # use the list gathered in (1)
    >>> wordlist = ['word1', 'word2', 'word3', 'word4']  # and so on
    # draw 3 random words from the list
    >>> selection = random.sample(wordlist, k=3)

3. Get URL results from search engines for the random tuples. Here are examples of Python modules to query search engines: `search-engine-parser <https://github.com/bisohns/search-engine-parser>`_ and `GoogleScraper <https://github.com/NikolaiT/GoogleScraper>`_.

One of the main drawbacks of the BootCaT method is that it is not stable in time, both search engines and scraper modules may not work as intended anymore. In that case it would be necessary to look for alternatives, look for concepts like “SERP” and “search engines scraping”.

4. Download and process the link list with Trafilatura, see `usage <usage.html>`_.


.. hint::
    For more information, see the corresponding blog post: `Replicating the BootCat method to build web corpora from search engines <https://adrien.barbaresi.eu/blog/replicate-bootcat-corpus-method.html>`_.



Selecting random documents from the Web
---------------------------------------



A model for web texts is described along with some experiments in the PhD thesis preceding the work on this library. Here are criteria you could use:

- General text form, line and sentences lengths, etc.
- Proportion of discourse and temporal markers

For more see `Indicators for intrinsic quality assessment <https://tel.archives-ouvertes.fr/tel-01167309/document#page=212>`_ (section of PhD thesis).

See also the blog post `What is good enough to become part of a web corpus?  <https://adrien.barbaresi.eu/blog/what-is-good-enough-to-become-part-of-a-web-corpus.html>`_



Social networks
---------------

Series of surface scrapers that crawl the networks without even logging in, thus circumventing the API restrictions. Development of such software solutions is fast-paced, so no links will be listed here at the moment.

Previously collected tweet IDs can be “hydrated”, i.e. retrieved from Twitter in bulk. see for instance:

- `Twitter datasets for research and archiving <https://tweetsets.library.gwu.edu/>`_
- `Search GitHub for Tweet IDs <https://github.com/search?q=tweet+ids>`_

Links can be extracted from tweets with a regular expression such as ``re.findall(r'https?://[^ ]+')``. They probably need to be resolved first to get actual link targets and not just shortened URLs (like t.co/…).


For further ideas from previous projects see references below.



Remarks
-------

For relatively small and focused corpora, human supervision is key. It is advisable to keep an eye on all steps of corpus construction.

A crawling method using diverse seeds for corpus building can yield better results and notably ensure better randomness in a population of web documents (see Henzinger et al. 2000).

Screening and refining the lists of URLs you use for your projects can also enhance corpus quality, see for example the implementation details in the papers mentioned below as well as the filtering tool `courlan <https://github.com/adbar/courlan>`_ included with Trafilatura.

The following blog posts give more insights on aspects of web corpus construction:

- `Challenges in web corpus construction for low-resource languages <https://adrien.barbaresi.eu/blog/challenges-web-corpus-construction-low-resource-languages.html>`_
- `Finding viable seed URLs for web corpora <https://adrien.barbaresi.eu/blog/finding-viable-seed-urls-web-corpora.html>`_




References
----------


* Barbaresi, A. (2014). Finding viable seed URLs for web corpora: a scouting approach and comparative study of available sources. In 9th Web as Corpus Workshop (WaC-9), 14th Conference of the European Chapter of the Association for Computational Linguistics (pp. 1-8).
* Barbaresi, A. (2015). Ad hoc and general-purpose corpus construction from web sources (Doctoral dissertation, ENS Lyon).
* Barbaresi, A. (2016). Collection and indexing of tweets with a geographical focus. In Proceedings of CMLC workshop, 10th International Conference on Language Resources and Evaluation (LREC 2016), pp. 24-27.
* Baroni, M., & Bernardini, S. (2004). BootCaT: Bootstrapping Corpora and Terms from the Web. In Proceedings of LREC 2004 (pp. 1313-1316).
* Berners-Lee, T., Hall, W., & Hendler, J. A. (2006). A framework for web science. Found. Trends Web Sci. 1, 1, 1–130.
* Blombach, A., Dykes, N., Heinrich, P., Kabashi, B., & Proisl, T. (2020). A corpus of German Reddit exchanges (GeRedE). In Proceedings of the 12th Language Resources and Evaluation Conference (pp. 6310-6316).
* Henzinger, M. R., Heydon, A., Mitzenmacher, M., & Najork, M. (2000). On near-uniform URL sampling. Computer Networks, 33(1-6), 295-308.
* Jauhiainen, H., Jauhiainen, T., & Lindén, K. (2020). Building web corpora for minority languages. In Proceedings of the 12th Web as Corpus Workshop (pp. 23-32).
* Minocha, A., Reddy, S., & Kilgarriff, A. (2014). Feed Corpus: an ever growing up-to-date corpus. *Proceedings of the 8th Web as Corpus Workshop*, pp. 1-4, ACL SIGWAC.
* Schäfer, R., Barbaresi, A., & Bildhauer, F. (2014). Focused web corpus crawling. In Proceedings of the 9th Web as Corpus workshop (WAC-9), pp. 9-15.
