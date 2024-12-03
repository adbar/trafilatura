## History / Changelog


## 2.0.0

Breaking changes:
- Python 3.6 and 3.7 deprecated (#709)
- `bare_extraction()`:
   - now returns an instance of the `Document` class by default
   - `as_dict` deprecation warning → use `.as_dict()` method on return value (#730)
- `bare_extraction()` and `extract()`: `no_fallback` deprecation warning → use `fast` instead (#730)
- downloads: remove `decode` argument in `fetch_url()` → use `fetch_response` instead (#724)
- deprecated graphical user interface now removed (#713)
- extraction: move `max_tree_size` parameter to `settings.cfg` (#742)
- use type hinting (#721, #723, #748)
- see [Python](https://trafilatura.readthedocs.io/en/latest/usage-python.html#deprecations) and [CLI](https://trafilatura.readthedocs.io/en/latest/usage-cli.html#deprecations) deprecations in the docs

Fixes:
- set `options.source` before raising error on empty doc tree by @dmoklaf (#707)
- robust encoding in `options.source` (#717)
- more robust mapping for conversion to HTML (#721)
- CLI downloads: use all information in settings file (#734)
- downloads: cleaner urllib3 code (#736)
- refine table markdown output by @unsleepy22 (#752)
- extraction fix: images in text nodes by @unsleepy22 (#757)

Metadata:
- more robust URL extraction (#710)

Command-line interface:
- CLI: print URLs early for feeds and sitemaps with `--list` with @gremid (#744)
- CLI: add 126 exit code for high error ratio (#747)

Maintenance:
- remove already deprecated functions and args (#716)
- add type hints (#723, #728)
- setup: use `pyproject.toml` file (#715)
- simplify code (#708, #709, #727)
- better debug messages in `main_extractor` (#714)
- evaluation: review data, update packages, add magic_html (#731)
- setup: explicit exports through `__all__` (#740)
- tests: extend coverage (#753)

Documentation:
- fix link in `docs/index.html` by @nzw0301 (#711)
- remove docs from published packages (#743)
- update docs (#745)


## 1.12.2

- downloads: add support for SOCKS proxies with @gremid (#682)
- extraction fix: ValueError in table spans (#685)
- spider: `prune_xpath` parameter added by @felipehertzer (#684)
- spider: relax strict parameter for link extraction (#687)
- sitemaps: `max_sitemaps` parameter added by @felipehertzer (#690)
- maintenance: make compression libraries optional (#691)
- metadata: review and lint code (#694)


### 1.12.1

Navigation:
- spider: restrict search to sections containing URL path (#673)
- crawler: add parameter class and types, **breaking change** for undocumented functions (#675)
- maintenance: simplify link discovery and extend tests (#674)
- CLI: review code, add types and tests (#677)

Bugfixes:
- fix `AttributeError` in element deletion (#668)
- fix `MemoryError` in table header columns (#665)

Docs:
- docs: fix variable name for extract_metadata in quickstart by @jpigla in #678


### 1.12.0

Breaking change:
- enforce fixed list of output formats, deprecate `-out` on the CLI (#647)

Faster, more accurate extraction:
- review link and structure checks (#653)
- improve justext fallback (#652)
- baseline: prevent LXML error in JSON-LD (#643), do not use as backup extraction (#646)
- review XPaths for undesirable content (#645)

Bugfixes and maintenance:
- CLI fix: markdown format should trigger `include_formatting` (#649)
- images fix: use a length threshold on src attribute (#654)
- XML-TEI: replace RelaxNG by DTD, remove pickle, and update (#655)
- formatting & markdown fix: add newlines (#656)
- table fix: prevent `MemoryError` & `ValueError` during conversion to text (#658)

Documentation:
- update `crawls.rst`: `known` is an unexpected argument, by @tommytyc in #638


### 1.11.0

Breaking change:
- metadata now skipped by default (#613), to trigger inclusion in all output formats:
   - `with_metadata=True` (Python)
   - `--with-metadata` (CLI)

Extraction:
- add HTML as output format (#614)
- better and faster baseline extraction (#619)
- better handling of HTML/XML elements (#628)
- XPath rules added with @felipehertzer (#540)
- fix: avoid faulty readability_lxml content (#635)

Evaluation:
- new scripts and data with @LydiaKoerber (#606, #615)
- additional data with @swetepete (#197)

Maintenance:
- docs extended and updated, added page on deduplication (#618)
- review code, add tests and types in part of the submodules (#620, #623, #624, #625)


### 1.10.0

Breaking changes:
- raise errors on deprecated CLI and function arguments (#581)
- regroup classes and functions linked to deduplication (#582)
``trafilatura.hashing`` → ``trafilatura.deduplication``

Extraction:
- port of is_probably_readerable from readability.js by @zirkelc in #587
- Markdown table fixes by @naktinis in #601
- fix list spacing in TXT output (#598)
- CLI fixes: file processing options, mtime, and tests (#605)
- CLI fix: read standard input as binary (#607)

Downloads:
- fix deflate and add optional zstd to accepted encodings (#594)
- spider fix: use internal download utilities for robots.txt (#590)

Maintenance:
- add author XPaths (#567)
- update justext and lxml dependencies (#593)
- simplify code: unique function for length tests (#591)

Docs:
- fix typos by @RainRat in #603


### 1.9.0

Extraction:
- add markdown as explicit output (#550)
- improve recall preset (#571)
- speedup for readability-lxml (#547)
- add global options object for extraction and use it in CLI (#552)
- fix: better encoding detection (#548)
- recall: fix for lists inside tables with @mikhainin (#534)
- add symbol to preserve vertical spacing in Markdown (#499)
- fix: table cell separators in non-XML output (#563)
- slightly better accuracy and execution speed overall

Metadata:
- add file creation date (date extraction, JSON & XML-TEI) (#561)
- fix: empty content in meta tag by @felipehertzer (#545)

Maintenance:
- restructure and simplify code (#543, #556)
- CLI & downloads: revamp and use global options (#565)
- eval: review code, add guidelines and small benchmark (#542)
- fix: raise error if config file does not exist (#554)
- deprecate `process_record()` (#549)
- docs: convert readme to markdown and update info (#564, #578)


### 1.8.1

Maintenance:
- Pin LXML to prevent broken dependency (#535)

Extraction:
- Improve extraction accuracy for major news outlets (#530)
- Fix formatting by correcting order of element generation and space handling with @dlwh (#528)
- Fix: prevent tail insertion before children in nested elements by @knit-bee (#536)


### 1.8.0

Extraction:
- Better precision by @felipehertzer (#509, #520)
- Code formatting in TXT/Markdown output added (#498)
- Improved CSV output (#496)
- LXML: compile XPath expressions (#504)
- Overall speedup about +5%

Downloads and Navigation:
- More robust scans with `is_live_page()` (#501)
- Better sitemap start and safeguards (#503, #506)
- Fix for headers in response object (#513)

Maintenance:
- License changed to Apache 2.0
- `Response` class: convenience functions added (#497)
- `lxml.html.Cleaner` removed (#491)
- CLI fixes: parallel cores and processing (#524)


### 1.7.0

Extraction:
- improved `html2txt()` function

Downloads:
- add advanced `fetch_response()` function
→ pending deprecation for `fetch_url(decode=False)`

Maintenance:
- support for LXML v5+ (#484 by @knit-bee, #485)
- update [htmldate](https://github.com/adbar/htmldate/releases/tag/v1.7.0)


### 1.6.4

Maintenance:
- MacOS: fix setup, update htmldate and add tests (#460)
- drop invalid XML element attributes with @vbarbaresi in #462
- remove cyclic imports (#458)

Navigation:
- introduce `MAX_REDIRECTS` config setting and fix urllib3 redirect handling by @vbarbaresi in #461
- improve feed detection (#457)

Documentation:
- enhancements to documentation and testing with @Maddesea in #456


### 1.6.3

Extraction:
- preserve space in certain elements with @idoshamun (#429)
- optional list of xPaths to prune by @HeLehm (#414)

Metadata:
- more precise date extraction (see [htmldate](https://github.com/adbar/htmldate/releases/tag/v1.6.0))
- new `htmldate` extensive search parameter in config (#434)
- changes in URLs: normalization, trackers removed (see [courlan](https://github.com/adbar/courlan/releases/tag/v0.9.5))

Navigation:
- reviewed code for feeds (#443)
- new config option: external URLs for feeds/sitemaps (#441)

Documentation:
- update, add page on text embeddings with @tonyyanga (#428, #435, #447)
- fix quickstart by @sashkab (#419)


### 1.6.2

Extraction:
- more lenient HTML parsing (#370)
- improved code block support with @idoshamun (#372, #401)
- conversion of relative links to absolute by @feltcat (#377)
- remove use of signal from core functions (#384)

Metadata:
- JSON-LD fix for sitenames by @felipehertzer (#383)

Command-line interface:
- more robust batch processing (#381)
- added `--probe` option to CLI to check for extractable content (#378, #392)

Maintenance:
- simplified code (#408)
- support for Python 3.12
- pinned LXML version for MacOS (#393)
- updated dependencies and parameters (notably `htmldate` and `courlan`)
- code cleaning by @marksmayo (#406)


### 1.6.1

Extraction:
- minor fixes: tables in figures (#301), headings (#354) and lists (#318)

Metadata:
- simplify and fully test JSON parsing code, with @felipehertzer (#352, #368)
- authors, JSON and unicode fixes by @felipehertzer in #365
- fix for authors without `additionalName` by @awwitecki in #363

Navigation:
- reviewed link processing in feeds and sitemaps (#340, #350)
- more robust spider (#359)
- updated underlying courlan package (#360)


### 1.6.0

Extraction:
- new content hashes and default file names (#314)
- fix deprecation warning with @sdondley in #321
- fix for metadata image by @andremacola in #328
- fix potential unicode issue in third-party extraction with @Korben00 in #331 
- review logging levels (#347)

Command-line interface:
- more efficient sitemap processing (#326)
- more efficient downloads (#338)
- fix for single URL processing (#324) and URL blacklisting (#339)

Navigation:
- additional safety check on domain similarity for feeds and sitemaps
- new function ``is_live test()`` using HTTP HEAD request (#327)
- code parts supported by new courlan version

Maintenance:
- allow ``urllib3`` version 2.0+
- minor code simplification and fixes


### 1.5.0

Extraction:
- fixes for metadata extraction with @felipehertzer (#295, #296),  @andremacola (#282, #310), and @edkrueger (#303)
- pagetype and image urls added to metadata by @andremacola (#282, #310)
- add as_dict method to Document class with @edkrueger in #306
- XML output fix with @knit-bee in #315
- various smaller fixes: lists (#309), XPaths, metadata hardening

Navigation:
- transfer URL management to courlan.UrlStore (#232, #312)
- fixes for spider module

Maintenance:
- simplify code and extend tests
- underlying packages htmldate and courlan, update setup and docs


### 1.4.1

Extraction:
- XML output improvements with @knit-bee (#273, #274)
- extraction bugs fixed (#263, #266), more robust HTML doctype parsing
- adjust thresholds for link density in paragraphs

Metadata:
- improved title and sitename detection (#284)
- faster author, categories, domain name, and tags extraction
- fixes to author emoji regexes by @felipehertzer (#269)

Command-line interface:
- review argument consistency and add deprecation warnings (#261)

Setup:
- make download timeout configurable (#263)
- updated dependencies, use of faust-cchardet for Python 3.11


### 1.4.0

Impact on extraction and output format:
- better extraction (#233, #243 & #250 with @knit-bee, #246 with @mrienstra, #258)
- XML: preserve list type as attribute (#229)
- XML TEI: better conformity with @knit-bee (#238, #242, #253, #254)
- faster text cleaning and shorter code (#237 with @deedy5, #245)
- metadata: add language when detector is activated (#224)
- metadata: extend fallbacks and test coverage for json_metadata functions by @felipehertzer (#235)
- TXT: change markdown formatting of headers by @LaundroMat (#257)

Smaller changes in convenience functions:
- add function to clear caches (#219)
- CLI: change exit code if download fails (#223)
- settings: use "\n" for multiple user agents by @k-sareen (#241)

Updates:
- docs updated (and #244 by @dsgibbons)
- package dependencies updated


### 1.3.0
- fast and robust `html2txt()` function added (#221)
- more robust parsing (#228)
- fixed bugs in metadata extraction, with @felipehertzer in #213 & #226 
- extraction about 10-20% faster, slightly better recall
- partial fixes for memory leaks (#216)
- docs extended and updated (#217, #225)
- prepared deprecation of old `process_record()` function
- more stable processing with updated dependencies


### 1.2.2
- more efficient rules for extraction
- metadata: further attributes used (with @felipehertzer)
- better baseline extraction
- issues fixed: #202, #204, #205
- evaluation updated


### 1.2.1
- ``--precision`` and ``--recall`` arguments added to the CLI
- better text cleaning: paywalls and comments
- improvements for Chinese websites (with @glacierck & @immortal-autumn): #186, #187, #188
- further bugs fixed: #189, #192 (with @felipehertzer), #200
- efficiency: faster module loading and improved RAM footprint


### 1.2.0
- efficiency: replaced module readability-lxml by trimmed fork
- bug fixed: (#179, #180, #183, #184)
- improved baseline extraction
- cleaner metadata (with @felipehertzer)


### 1.1.0
- encodings: better detection, output NFC-normalized Unicode
- maintenance and performance: more efficient code
- bugs fixed (#119, #136, #147, #160, #161, #162, #164, #167 and others)
- prepare compatibility with upcoming Python 3.11
- changed default settings
- extended documentation


### 1.0.0
- compress HTML backup files & seamlessly open .gz files
- support JSON web feeds
- graphical user interface integrated into main package
- faster downloads: reviewed backoff, compressed data
- optional modules: downloads with `pycurl`, language identification with `py3langid`
- bugs fixed (#111, #125, #132, #136, #140)
- minor optimizations and fixes by @vbarbaresi in [#124](https://github.com/adbar/trafilatura/pull/124) & [#130](https://github.com/adbar/trafilatura/pull/130)
- fixed array with single or multiples entries on json extractor by @felipehertzer in [#143](https://github.com/adbar/trafilatura/pull/143)
- code base refactored with @sourcery-ai [#121](https://github.com/adbar/trafilatura/pull/121), improved and optimized for Python 3.6+
- drop support for Python 3.5


### 0.9.3
- better, faster encoding detection: replaced `chardet` with `charset_normalizer`
- faster execution: updated `justext` to 3.0
- better extraction of sub-elements in tables (#78, #90)
- more robust web feed parsing
- further defined precision- and recall-oriented settings
- license extraction in footers (#118)


### 0.9.2
- first precision- and recall-oriented presets defined
- improvements in authorship extraction (thanks @felipehertzer)
- requesting TXT output with formatting now results in Markdown format
- bugs fixed: notably extraction robustness and consistency (#109, #111, #113)
- setting for cookies in request headers (thanks @muellermartin)
- better date extraction thanks to htmldate update


### 0.9.1
- improved author extraction (thanks @felipehertzer!)
- bugs fixed: HTML element handling, HTML meta attributes, spider, CLI, ...
- docs updated and extended
- CLI: option names normalized (heed deprecation warnings), new option `explore`


### 0.9.0
- focused crawling functions including politeness rules
- more efficient multi-threaded downloads + use as Python functions
- documentation extended
- bugs fixed: extraction and URL handling
- removed support for Python 3.4


### 0.8.2
- better handling of formatting, links and images, title type as attribute in XML formats
- more robust sitemaps and feeds processing
- more accurate extraction
- further consolidation: code simplified and bugs fixed


### 0.8.1
- extraction trade-off: slightly better recall
- code robustness: requests, configuration and navigation
- bugfixes: image data extraction


### 0.8.0
- improved link discovery and handling
- fixes in metadata extraction, feeds and sitemaps processing
- breaking change: the `extract` function now reads target format from `output_format` argument only
- new extraction option: preserve links, CLI options re-ordered
- more opportunistic backup extraction


### 0.7.0
- customizable configuration file to parametrize extraction and downloads
- better handling of feeds and sitemaps
- additional CLI options: crytographic hash for file name, use Internet Archive as backup
- more precise extraction
- faster downloads: `requests` replaced with bare `urllib3` and custom decoding
- consolidation: bug fixes and improvements, many thanks to the issues reporters!


### 0.6.1
- added `bare_extraction` function returning Python variables
- improved link discovery in feeds and sitemaps
- option to preserve image info
- fixes (many thanks to bug reporters!)


### 0.6.0
- link discovery in sitemaps
- compatibility with Python 3.9
- extraction coverage improved
- deduplication now optional
- bug fixes


### 0.5.2
- optional language detector changed: `langid` → `pycld3`
- helper function `bare_extraction()`
- optional deduplication off by default
- better URL handling (`courlan`), more complete metadata
- code consolidation (cleaner and shorter)


### 0.5.1
- extended and more convenient command-line options
- output in JSON format
- bug fixes


### 0.5.0
- faster and more robust text and metadata extraction
- more efficient batch processing (parallel processing, URL queues)
- extraction and processing of ATOM/RSS feeds
- complete command-line tool with corresponding options


### 0.4.1
- better metadata extraction and integration (XML & XML-TEI)
- more efficient processing
- output directory as CLI-option


### 0.4
- improved "fast" mode (accuracy and speed)
- better fallbacks with readability-lxml and justext
- metadata extraction added
- more robust processing (tests, encoding handling)


### 0.3.1
- support for Python 3.4 reactivated
- bugs in XML output and discarding sections solved
- new tests and documentation


### 0.3.0
- code base re-structured for clarity and readability
- streamlined HTML processing and conversion
- internal less-recently-used cache (LRU) for deduplication
- export as CSV
- better test coverage, extraction recall and precision
- further documentation (trafilatura.readthedocs.org)
- optional processing of text formatting
- more complete settings file


### 0.2.1
- added metadata to the XML output
- production of valid XML TEI for simple documents


### 0.2.0
- better handling of nested elements, quotes and tables
- validation of XML TEI documents
- bulk download and processing


### 0.1.1
- handling of line breaks
- element trimming simplified


### 0.1.0
- first release used in production and meant to be archived for reproducibility and citability
- better extraction precision


### 0.0.5: last version compatible with Python 3.4
- optional dependencies
- bugs in parsing removed


### 0.0.4
- code profiling and speed-up


### 0.0.3
- tables included in extraction
- bypass justext in arguments
- better handling of non-p elements


### 0.0.2
- better handling of text nodes
- improvements in extraction recall


### 0.0.1
- first release, minimum viable package
