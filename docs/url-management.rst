URL management
==============


Filtering and managing a URL queue
----------------------------------


Filtering of input URLs is useful to avoid hodgepodges like ``.../tags/abc`` or "internationalized" rubrics like ``.../en/....``. It is best used on URL lists, before retrieving all pages and especially before massive downloads.

The Courlan library is included with Trafilatura, it can be useful to deal with such cases:

``courlan --language de --strict --inputfile linkliste-roh.txt --outputfile linkliste-gefiltert.txt``


See the `Courlan documentation <https://github.com/adbar/courlan>`_ for examples.



..
  Blacklisting
  ------------






