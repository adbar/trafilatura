Validation
==========


*Trafilatura* can validate XML documents according to the guidelines of the `Text Encoding Initiative <https://tei-c.org/>`_ (XML-TEI).

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


For more information see this blog post: `Validating TEI-XML documents with Python <http://adrien.barbaresi.eu/blog/validating-tei-xml-python.html>`_
