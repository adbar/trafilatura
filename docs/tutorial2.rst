Tutorial: Validation of TEI files
=================================


*Trafilatura* can produce and validate XML documents according to the guidelines of the `Text Encoding Initiative <https://tei-c.org/>`_ (XML-TEI).


Producing TEI files
--------------------

In Python:

.. code-block:: python

    # load the necessary components
    import trafilatura
    # open a file and parse it
    downloaded = trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
    result = trafilatura.extract(downloaded, tei_output=True, tei_validation=True)


From the command line:

.. code-block:: bash

    trafilatura --xmltei --validate --URL "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"



Validating existing files
-------------------------


The following code returns `True` if a document is valid and outputs a message related to the first error impeding validation otherwise:

.. code-block:: python

    # load the necessary components
    from lxml import etree
    from trafilatura.xml import validate_tei
    # open a file and parse it
    mytree = etree.parse('document-name.xml')
    # validate it
    validate_tei(mytree)
    # returns True or an error message


For more information please refer to this blog post: `Validating TEI-XML documents with Python <https://adrien.barbaresi.eu/blog/validating-tei-xml-python.html>`_
