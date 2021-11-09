Finding URLs for web corpora
============================


Webpages are used as sources to build corpora and also to gather links to start crawls from (i.e. "seeds"). Corpora can be focused on a given range of websites or topics or be merely language-minded and opportunistically take all seen texts into account. In the latter case, using diverse sources of URL seeds could ensure that there is not a potentially unknown bias.


Existing corpus resources
-------------------------

URL lists from corpus linguistic projects can be a starting ground to derive information from, either to recreate existing corpora or to re-crawl the websites and find new content. If the websites don't exist anymore, the links can still be useful as the corresponding web pages can be retrieved from archives.

- `Sources for the Internet Corpora <http://corpus.leeds.ac.uk/internet.html>`_ of the Leeds Centre for Translation Studies
- `Link data sets <https://corporafromtheweb.org/link-data-sets-cc-by/>`_  of the COW project
- `Coronakorpus links <https://github.com/adbar/coronakorpus>`_


URL directories
---------------

DMOZ (at the time of experiments) and Wikipedia work quite well as primary sources:

- `Challenges in web corpus construction for low-resource languages in a post-BootCaT world <https://halshs.archives-ouvertes.fr/halshs-00919410/file/Barbaresi_LTC13_Challenges-LRL_paper_v2.pdf>`_ (2013 paper)
- `Qualification of URLs extracted from DMOZ and Wikipedia <https://tel.archives-ouvertes.fr/tel-01167309/document#page=189>`_ (PhD thesis section)
- `Overview of the Web archiving community <https://github.com/pirate/ArchiveBox/wiki/Web-Archiving-Community>`_

..
   https://www.sketchengine.eu/guide/create-a-corpus-from-the-web/
   https://github.com/chiphuyen/lazynlp



Searching for URLs
~~~~~~~~~~~~~~~~~~

The Common Crawl is a good place to start looking for already known URLs, and possibly for the corresponding pages stored by the project. So is the Internet Archive (with a different focus):

- https://index.commoncrawl.org/
- `cdx_toolkit <https://github.com/cocrawler/cdx_toolkit/>`_: A toolkit for CDX indices such as Common Crawl and the Internet Archive's Wayback Machine
- `Python example <https://github.com/cocrawler/cdx_toolkit/blob/master/examples/iter-and-warc.py>`_ using cdx_toolkit

Related info: before retrieving them storing web documents in Internet archives can be fruitful, see for instance the tool `archivenow <https://github.com/oduwsdl/archivenow>`_.



.. code-block:: bash

    #!/bin/bash
    set -e
    url="https://aws-publicdatasets.s3.amazonaws.com/$1"
    dir="$(dirname "$1")"
    name="$(basename "$1")"
    fpath="$dir/${name}.urls.gz"

    mkdir -p "$dir"
    if [ ! -r "$fpath" ]; then
      curl -s --retry 5 "$url" \
        | zcat \
        | grep -i 'WARC-TARGET-URI:' \
        | awk '{print $2}' \
        | gzip > "$fpath"
    fi


If saved as dl-wat, one could then run it as follows:

``$ zcat wat.paths.gz | xargs -P32 -n1 dl-wat``

*source:* `https://blog.burntsushi.net/transducers/ <https://blog.burntsushi.net/transducers/>`_

..
    To look ooking for feeds:
    (<link[^>]*(?:\s(?:type=[\"']?(application\/rss\+xml|application\/atom\+xml|application\/rss|application\/atom|application\/rdf\+xml|application\/rdf|text\/rss\+xml|text\/atom\+xml|text\/rss|text\/atom|text\/rdf\+xml|text\/rdf|text\/xml|application\/xml)[\"']?|rel=[\"']?(?:alternate)[\"']?))[^>]*>)"
    source: https://draft.li/blog/2016/03/21/rss-usage-on-the-web/



Social Networks
---------------

Series of surface scrapers that crawl the networks without even logging in, thus circumventing the API restrictions. Development of such software solutions is fast-paced, so no links will be listed here at the moment.

Previously collected tweet IDs can be "hydrated", i.e. retrieved from Twitter in bulk. see for instance:

- `Twitter datasets for research and archiving <https://tweetsets.library.gwu.edu/>`_
- `Search GitHub for Tweet IDs <https://github.com/search?q=tweet+ids>`_

Links can be extracted from tweets with a regular expression such as ``re.findall(r'https://[^ ]+')``. They probably need to be resolved first to get actual link targets and not just shortened URLs (like t.co/…).


For further ideas from previous projects see:

- `Collection and indexing of tweets with a geographical focus <https://hal.archives-ouvertes.fr/hal-01323274/document>`_ (2016 paper)
- `Collection, description, and visualization of the German Reddit corpus <https://hal.archives-ouvertes.fr/hal-01207311/document>`_ (2016 paper) + `code <https://github.com/adbar/german-reddit>`_



Search Engines
--------------

The BootCat approach (Baroni & Bernardini 2004) grounds on the assumption that randomly generated search engines queries made of random words will lead to combined cross-domain text collections. The queries consist of several randomly combined word seeds, first coming from an initial list and later from unigram extraction in the corpus itself. As a result, seed URLs are gathered, which are used as a starting point for web crawlers.

Because of increasing limitations of the search engine APIs, the querying process with a very limited financial budget is not practical or slow. All in all, the APIs may be too expensive and/or too unstable in time to support large-scale corpus building projects. Moreover, the question whether the method used so far provides a good overview of a language is still open. Other technical difficulties include diverse and partly unknown search biases related to search engine optimization tricks as well as undocumented PageRank adjustments.

Marco Baroni and Silvia Bernardini. 2004. BootCaT: Bootstrapping corpora and terms from the web. Proceedings of LREC 2004.



Selecting random documents from the Web
---------------------------------------

A model for web texts is described along with some experiments in the PhD thesis preceding the work on this library. Here are criteria you could use:

- General text form, line and sentences lengths, etc.
- Proportion of discourse and temporal markers

For more see `Indicators for intrinsic quality assessment <https://tel.archives-ouvertes.fr/tel-01167309/document#page=212>`_ (section of PhD thesis).




Remarks and references
----------------------

A crawling method using diverse seeds for corpus building can yield better results and notably ensure better randomness in a population of web documents (see Henzinger et al. 2000).

Monika R. Henzinger, Allan Heydon, Michael Mitzenmacher, and Marc Najork. 2000. On near-uniform URL sampling. In Proceedings of the 9th International World Wide Web conference on Computer Networks, pages 295–308. North-Holland Publishing Company.

