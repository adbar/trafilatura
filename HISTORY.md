## History / Changelog


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
