## History / Changelog


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
