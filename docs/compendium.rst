Compendium: Web texts in linguistics and humanities
===================================================

.. meta::
    :description lang=en:
        This page summarizes essential information about building and operation of web text collections. It primarily addresses concerns in linguistics and humanities.


*A compendium is a concise collection of information pertaining to a body of knowledge.*


Web corpora as scientific objects
---------------------------------

In linguistics, a text corpus (plural corpora) is a language resource consisting of a structured set of texts. They can be considered to be a “collection of linguistic data that are directly observable” and as such “naturalistic data”, that is data “intended to be reflective of actual language use” (Good 2022).

Nowadays, corpora are usually electronically stored and processed. Web corpora are the heirs of established corpora and they mostly undergo the same construction process, with necessary adapations and novelties (Barbaresi 2015).



Corpus construction steps
-------------------------

In a `seminal article <https://aclanthology.org/J07-1010.pdf>`_, Adam Kilgarriff sums up issues related to the “low-entry-cost way to use the Web” which commercial search engines represent. He shows how an alternative can be developed within the academic community.


    “An alternative is to work like the search engines, downloading and indexing substantial
    proportions of the World Wide Web, but to do so transparently, giving reliable figures, and supporting
    language researchers’ queries.”

    “The process involves crawling, downloading, ’cleaning’ and de-duplicating the data, 
    then linguistically annotating it and loading it into a corpus query tool.”

Based on these steps, three distinct phases can be distinguished:
    1. Web crawling determines the range and the general contents of a web corpus
    2. Data pre-processing impacts all the other steps downstream
       see following section
    3. Linguistic annotation and query tools give profile to the data, they can make certain features noticeable while blurring others

Handling of steps (1) & (2) is the primary motivation behind the development of the Trafilatura software package.

.. hint::
    For more information on the article mentioned above see the blog post `“Googleology is bad science”: Anatomy of a web corpus infrastructure <https://adrien.barbaresi.eu/blog/googleology-anatomy-corpus-infrastructure.html>`_.


Crawling and download
~~~~~~~~~~~~~~~~~~~~~

- Find URLs (see `Finding sources for web corpora <sources.html>`_)
- Decide whether to retrieve a whole website or just targeted URLs

.. hint::
    See documentation on `crawls <crawls.html>`_ and `downloads <downloads.html>`_.


Web scraping and data cleaning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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



Corpus types and resulting methods
----------------------------------

    “Documentary and corpus data are generally likely to be usable to support a wide range of investigations across more than one linguistic subfield, though data of such kinds could also be collected to serve a fairly narrow purpose depending on the research practices adopted.” (Good 2022)


Major fault lines:
    - General vs. specialized (Gries & Newman 2014)
    - General-purpose vs. ad hoc web corpora (Barbaresi 2015)
    - Also: “Miniweb” vs. domain specific corpora in the `WebCorp LSE <https://web.archive.org/web/20200127124029/https://wse1.webcorp.org.uk/home/corpora.html>`_ typology


Corpus construction methods:
    1. Tailor-made corpus
        - use of already known sources only
    2. Partial control and/or “corpus seeds” (focused crawling)
        - use of search engines via focused searches or BootCaT method (Baroni & Bernardini 2004), see blog post `Replicating the BootCat method to build web corpora from search engines <https://adrien.barbaresi.eu/blog/replicate-bootcat-corpus-method.html>`_
        - known corpus seeds & use of criteria to restrict the search space (using structural properties like domains or content-aware criteria like topics)
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

    “Manually selecting, crawling and cleaning particular web sites with large and good-enough-quality textual content.” (Spoustová & Spousta 2012, see also `Review of the Czech Internet corpus <https://adrien.barbaresi.eu/blog/review-czech-internet-corpus-focused-corpus-construction.html>`_)

The purpose of focused web corpora is to complement existing collections, as they allow for better coverage of specific written text types and genres, especially the language evolution seen through the lens of user-generated content, which gives access to a number of variants, socio- and idiolects, for example in the case of blogs (Barbaresi 2019).

Corpus building comprises three phases:
    1. First, the texts are discovered and listed.
    2. Then they are downloaded, possibly using web crawling techniques which are not as extensive as in the other case since it is mainly about fetching and processing. 
    3. Finally a processed version is stored, which is in itself the linguistic corpus. It can be indexed by a corpus-query tool or be made available using standardized formats used by the research Community such as XML or XML TEI.


.. hint::
   For more information, see the tutorial `Gathering a custom web corpus <tutorial0.html>`_



References
----------

Anthony, L. (2013). A critical look at software tools in corpus linguistics. Linguistic Research, 30(2), 141-161.

Barbaresi, A. (2015). Ad hoc and general-purpose corpus construction from web sources (Doctoral dissertation, ENS Lyon).

Barbaresi, A. (2019). The Vast and the Focused: On the need for thematic web and blog corpora. In 7th Workshop on Challenges in the Management of Large Corpora (CMLC-7) (pp. 29-32). Leibniz-Institut für Deutsche Sprache.

Baroni, M., & Bernardini, S. (2004). BootCaT: Bootstrapping Corpora and Terms from the Web. In Proceedings of LREC 2004 (pp. 1313-1316).

Baroni, M., Bernardini, S., Ferraresi, A., & Zanchetta, E. (2009). The WaCky Wide Web: a collection of very large linguistically processed web-crawled corpora. Language Resources and Evaluation, 43(3), 209-226.

Berners-Lee, T., Hall, W., & Hendler, J. A. (2006). A Framework for Web Science. Foundations and Trends in Web Science, 1, 1, 1–130.

Good, J. (2022). "The Scope of Linguistic Data", In The Open Handbook of Linguistic Data Management, MIT Press, 27-47.

Gries, S. T., & Newman, J. (2014). Creating and using corpora. In Research methods in linguistics, Podesva, R.J., & Sharma, D. (eds.), 257-287.

Jauhiainen, H., Jauhiainen, T., & Lindén, K. (2020). Building web corpora for minority languages. In Proceedings of the 12th Web as Corpus Workshop (pp. 23-32).

Kilgarriff, A. (2007). Googleology is bad science. Computational linguistics, 33(1), 147-151.

Schäfer, R., Barbaresi, A., & Bildhauer, F. (2013). The Good, the Bad, and the Hazy: Design Decisions in Web Corpus Construction. In 8th Web as Corpus Workshop, pp. 7-15, ACL SIGWAC.

Spoustová, J., & Spousta, M. (2012). A High-Quality Web Corpus of Czech. In Proceedings of the Eighth International Conference on Language Resources and Evaluation (LREC'12) (pp. 311-315).

Tanguy, L. (2013). La ruée linguistique vers le Web. Texto! Textes et Cultures, 18(4).

