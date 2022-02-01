Compendium: Web texts in linguistics and humanities
===================================================

.. meta::
    :description lang=en:
        This page summarizes essential information about building and operation of web text collections. It primarily addresses concerns in linguistics and humanities.


*A compendium is a concise collection of information pertaining to a body of knowledge.*


Web corpora as scientific objects
---------------------------------

In linguistics, a text corpus (plural corpora) is a language resource consisting of a structured set of texts.  Nowadays, corpora are mostly electronically stored and processed. They can be considered to be a “collection of linguistic data that are directly observable” and as such “naturalistic data”, that is data “intended to be reflective of actual language use” (Good 2022).


    “A corpus is simply described as a large body of linguistic evidence typically composed of attested language use. […] The term corpus should properly only be applied to a well-organized collection of data.” (McEnery 2003, p. 449)


How well defined corpora should be, depends on research tradition and practices. Web corpora are the heirs of established corpora and they mostly undergo the same construction process, with necessary adapations and novelties (see Barbaresi 2015, chapter 1).

For Baroni & Ueyama (2006), corpora bring “actual usage evidence”, “collections of language samples produced in natural contexts and without experimental interference”. They distinguish four main cases where such evidence is needed: theoretical and applied linguistic questions, simulations of language acquisition, lexicography, and a large number of tasks in natural language processing.



Corpus types and resulting methods
----------------------------------

    “Documentary and corpus data are generally likely to be usable to support a wide range of investigations across more than one linguistic subfield, though data of such kinds could also be collected to serve a fairly narrow purpose depending on the research practices adopted.” (Good 2022)


Major fault lines:
    - General vs. specialized corpora (Gries & Newman 2014)
    - General-purpose vs. special-purpose (Baroni & Ueyama 2006), ad hoc vs. general-purpose web corpora (Barbaresi 2015)
    - “Miniweb” vs. domain specific web corpora (`WebCorp LSE <https://web.archive.org/web/20200127124029/https://wse1.webcorp.org.uk/home/corpora.html>`_ typology)


Corpus construction methods:
    1. Tailor-made corpus
        - use of already known sources only
    2. Partial control and/or “corpus seeds” (focused crawling)
        - known corpus seeds & use of criteria to restrict the search space (using structural properties like domains or content-aware criteria like topics)
        - use of search engines via focused searches or BootCaT method (Baroni & Bernardini 2004), see blog post `Replicating the BootCat method to build web corpora from search engines <https://adrien.barbaresi.eu/blog/replicate-bootcat-corpus-method.html>`_
    3. “Open-end” approach & automated web browsing (web crawling, broad crawls)
        - needs “crawling seeds”, hops from page to page and from one website to another



General-purpose corpora
~~~~~~~~~~~~~~~~~~~~~~~

General-purpose corpora are supposed to encompass a large amount of texts and a gamut of text types and text genres. Their significance arises from it, which can make them representative in some way. Corpus designers usually rely on the fact that potential small irregularities are going to be smoothed out by the sheer number of texts, so that empirical findings in the corpus are expected to be statistically relevant all the same. The goal for linguists is to get a statistical perspective on norms.

Such corpora can also strive to be representative of a genre or of a particular source, in the case of web corpus, like a Mini web, because the Web is too large to be completely retrieved and stored in a database (see Tanguy 2013).

They are often found at dedicated research institutions, as the building and maintenance is costly in time and resources. In the case of web corpora, this involves first an extensive web crawling phase, using mostly breadth-first techniques. Second, the text pre-processed. Meaning that a selection of resources of the documents or relevant extracts. Finally, loaded into corpus tool, which in that case, mostly involves tailored database applications.


Specialized corpora
~~~~~~~~~~~~~~~~~~~


On the second hand, there are specialized corpora which focus on a particular genre or or a particular source. They can be opportunistic in nature but they mostly involve prior knowledge of the contents and also a certain amount of control over what comes into the corpus. Contrarily to open ended-corpora, the goal for linguists is to get a better coverage of particular linguistic settings or phenomena:

The purpose of focused web corpora is to complement existing collections, as they allow for better coverage of specific written text types and genres, especially the language evolution seen through the lens of user-generated content, which gives access to a number of variants, socio- and idiolects, for example in the case of blogs (Barbaresi 2019).

Corpus building comprises three phases:
    1. First, the texts are discovered and listed.
    2. Then they are downloaded, possibly using web crawling techniques which are not as extensive as in the other case since it is mainly about fetching and processing. 
    3. Finally a processed version is stored, which is in itself the linguistic corpus. It can be indexed by a corpus-query tool or be made available using standardized formats used by the research Community such as XML or XML TEI.


.. hint::
   For more information, see the tutorial `Gathering a custom web corpus <tutorial0.html>`_


In-between
~~~~~~~~~~

The distinction is not always clear-cut, web corpora can target a particular set of web pages while keeping a more generalist approach:

    “Manually selecting, crawling and cleaning particular web sites with large and good-enough-quality textual content.” (Spoustová & Spousta 2012, see also `Review of the Czech Internet corpus <https://adrien.barbaresi.eu/blog/review-czech-internet-corpus-focused-corpus-construction.html>`_)



Corpus construction steps
-------------------------

In a `seminal article <https://aclanthology.org/J07-1010.pdf>`_, Adam Kilgarriff sums up issues related to the “low-entry-cost way to use the Web” which commercial search engines represent. He shows how an alternative can be developed within the academic community.


    “An alternative is to work like the search engines, downloading and indexing substantial
    proportions of the World Wide Web, but to do so transparently, giving reliable figures, and supporting
    language researchers’ queries.”

    “The process involves crawling, downloading, ’cleaning’ and de-duplicating the data, 
    then linguistically annotating it and loading it into a corpus query tool.” (Kilgarriff 2007)

Based on these steps, three distinct phases can be distinguished:
    1. Web crawling determines the range and the general contents of a web corpus
    2. Data pre-processing impacts all the other steps downstream
       see following section
    3. Linguistic annotation and query tools give profile to the data, they can make certain features noticeable while blurring others (Anthony 2013)

Handling of steps (1) & (2) is the primary motivation behind the development of the Trafilatura software package.

.. hint::
    For more information on the article mentioned above see the blog post `“Googleology is bad science”: Anatomy of a web corpus infrastructure <https://adrien.barbaresi.eu/blog/googleology-anatomy-corpus-infrastructure.html>`_.


Crawling and download
~~~~~~~~~~~~~~~~~~~~~

If web pages are to be discovered, an automatic way of navigating the Web is needed, that is `web crawling <https://en.wikipedia.org/wiki/Web_crawler>`_. It is possible to crawl a given website or the Web as a whole.


    “A crawler starts off with the URL for an initial page :math:`P_0`. It retrieves :math:`P_0`, extracts any URLs in it, and adds them to a queue of URLs to be scanned. Then the crawler gets URLs from the queue (in some order), and repeats the process.” (Cho et al. 1998)


Suitable texts for inclusion into corpora are not evenly distributed across the Internet. Pre-selecting documents according to certain criteria can be crucial. This concerns both content discovery and corpus creation
for which URLs are the most practical hint (see `Finding sources for web corpora <sources.html>`_).


    “It is important for the crawler to visit "important" pages first, so that the fraction of the Web that is visited […] is more meaningful.” (Cho et al. 1998)


The corpus construction strategy usually follows from the chosen corpus type, one can decide to retrieve a whole website or just targeted URLs.


    “Given that the bandwidth for conducting crawls is neither infinite nor free, it is becoming essential to crawl the Web in not only a scalable, but efficient way, if some reasonable measure of quality or freshness is to be maintained.” (Edwards et al. 2001)


Certain indicators can be applied while scouting the Web and potentially affect the course of events, such as language identification in order to keep the crawl language-focused (Jauhiainen et al. 2020).


.. hint::
    See documentation on `crawls <crawls.html>`_ and `downloads <downloads.html>`_ as well as the “brain” for web crawling tasks: the library `courlan <https://github.com/adbar/courlan>`_.


Web scraping and data cleaning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While web crawling focuses on hopping from page to page, retrieving the content and collecting especially links and potentially other information, web scraping describes the automatic extraction of targeted information on particular sections of a page.

In the context of web corpora, one's interest resides in finding texts and relevant metadata. Web scraping thus implies to download web pages (or to open locally stored ones) and to strip them of all unnecessary content in order to obtain a clean document which can be passed to linguistic analysis tools.


    “Cleaning is a low-level, unglamorous task, yet crucial: The better it is done, the better the outcomes. All further layers of linguistic processing depend on the cleanliness of the data.” (Kilgarriff 2007)


When confronted with web pages, the main issues affecting the content can be summarized as follows:

- How do we detect and get rid of navigation bars, headers, footers, etc.?
- How do we identify metadata, paragraphs and other structural information?
- How do we produce output in a standard form suitable for further processing?

On site level, recurring elements are called boilerplate. Removing them allow for avoiding hundreds of occurrences of phrases like “back to the main page” or “Copyright 2022 (site name)”.

Preserving some elements of the page structure can be useful to distinguish main text, quotes and comments. Authorship definitely is meaningful in a humanities context. Metadata such as the page title or the publication date are also quite relevant.

*Optional step: further post-processing (notably removal of near duplicates).*

For concrete steps see `usage <usage.html>`_.


Post hoc evaluation
~~~~~~~~~~~~~~~~~~~


For practical reasons, web corpus construction partly relies on the assumption that “the Web is a space in which resources are identified by Uniform Resource Identifiers (URIs).” (Berners-Lee et al., 2006) The Web is however changing faster than the researchers’ ability to observe it (Hendler et al., 2008), and a constant problem faced by web resources resides in meta-information and categorization.


The actual contents of a web corpus can only be listed with certainty once the corpus is complete. In addition to the potential lack of information concerning the metadata of the texts, there is a lack of information regarding the content, whose adequacy, focus and quality has to be assessed in a post hoc evaluation (Baroni et al., 2009).


That is why web texts can and should be further examined and prepared for inclusion into a linguistic corpus. The gathered documents should be controlled at least on a sample basis. Ideally, the corpus should undergo a qualitative screening, examination using quantitative criteria is easier to handle using machines, be it with statistical indicators (such as text length, frequent n-grams) or with content-based heuristics (for example using metadata or text analysis). Language identification is also best performed on clean text.


.. note::
    Further text quality criteria are discussed in Schäfer & Bildhauer (2013) chapter 5, and Barbaresi (2015) chapter 2.


A different series of questions arise when randomly searching for text on the Internet: What is a text? When does input stop to be a text? What should be included in the corpus? Sometimes the results are bounded by certain texts types (like classified ads) or by the toolchain (with scraps of text coming from the tools). See the challenges and indicators described in Schäfer et al. (2013).




Methodological issues
---------------------


Data sparsity
~~~~~~~~~~~~~

The above deals with texts published in the form of web pages. There are also a number of platforms and social networks which sadly cannot be comprehensively studied without the agreement of the company running them. It is although possible to gather data on a smaller scale (Barbaresi 2016).

The Web constantly evolves and hyperlinks cannot be expected to remain stable in time. Page display is also affected by technological or commercial evolutions, for example prominent news outlets may disappear behind pay walls. See the Wikipedia page on `link rot <https://en.wikipedia.org/wiki/Link_rot>`_ for ideas on how to prevent it (chiefly using clean URLs and web archives).


Technicalities
~~~~~~~~~~~~~~


Technical problems are mostly related to communications over the network and text processing. For smaller projects running from a single computer, bandwidth and RAM are two main limitations. For larger projects, the capacity to scale crawling and processing operations across servers is paramount. This notably includes the capacity to control when web servers are contacted, to what extent web pages can be processed on the fly, and how the resulting corpus data is stored and eventually indexed.



References
----------

Anthony, L. (2013). A critical look at software tools in corpus linguistics. *Linguistic Research*, 30(2), 141-161.

Barbaresi, A. (2015). Ad hoc and general-purpose corpus construction from web sources (Doctoral dissertation, ENS Lyon).

Barbaresi, A. (2016). Collection and indexing of tweets with a geographical focus. In *Proceedings of the 4th Workshop on Challenges in the Management of Large Corpora (CMLC-4)*, pp. 24-27.

Barbaresi, A. (2019). The Vast and the Focused: On the need for thematic web and blog corpora. In *Proceedings of the 7th Workshop on Challenges in the Management of Large Corpora (CMLC-7)*, Leibniz-Institut für Deutsche Sprache, pp. 29-32.

Baroni, M., & Bernardini, S. (2004). BootCaT: Bootstrapping Corpora and Terms from the Web. In *Proceedings of LREC 2004*, pp. 1313-1316.

Baroni, M., & Ueyama, M. (2006). Building general- and special-purpose corpora by Web crawling. In *Proceedings of the 13th NIJL international symposium, Language Corpora: Their compilation and application* (pp. 31–40).

Baroni, M., Bernardini, S., Ferraresi, A., & Zanchetta, E. (2009). The WaCky Wide Web: a collection of very large linguistically processed web-crawled corpora. *Language Resources and Evaluation*, 43(3), 209-226.

Berners-Lee, T., Hall, W., & Hendler, J. A. (2006). A Framework for Web Science. *Foundations and Trends in Web Science*, 1, 1, 1–130.

Cho, J., Garcia-Molina, H., & Page, L. (1998). Efficient crawling through URL ordering. *Computer networks and ISDN systems*, 30(1-7), 161–172.

Edwards, J., McCurley, K. S., and Tomlin, J. A. (2001). "An adaptive model for optimizing performance of an incremental web crawler". In *Proceedings of the 10th international conference on World Wide Web - WWW '01*, pp. 106–113.

Good, J. (2022). "The Scope of Linguistic Data", In *The Open Handbook of Linguistic Data Management*, MIT Press, 27-47.

Gries, S. T., & Newman, J. (2014). Creating and using corpora. In *Research methods in linguistics*, Podesva, R.J., & Sharma, D. (eds.), 257-287.

Jauhiainen, H., Jauhiainen, T., & Lindén, K. (2020). Building web corpora for minority languages. In *Proceedings of the 12th Web as Corpus Workshop*, pp. 23-32.

Kilgarriff, A. (2007). Googleology is bad science. *Computational linguistics*, 33(1), 147-151.

McEnery, T. (2003). Corpus Linguistics. In R. Mitkov (Ed.), *The Oxford Handbook of Computational Linguistics* (pp. 448–463). Oxford University Press.

Schäfer, R., Barbaresi, A., & Bildhauer, F. (2013). The Good, the Bad, and the Hazy: Design Decisions in Web Corpus Construction. In *8th Web as Corpus Workshop*, pp. 7-15, ACL SIGWAC.

Schäfer, R., & Bildhauer, F. (2013). Web Corpus Construction. Morgan & Claypool.

Spoustová, J., & Spousta, M. (2012). A High-Quality Web Corpus of Czech. In *Proceedings of the Eighth International Conference on Language Resources and Evaluation (LREC'12)*, pp. 311-315.

Tanguy, L. (2013). La ruée linguistique vers le Web. *Texto! Textes et Cultures*, 18(4).

