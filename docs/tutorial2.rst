Tutorial: Validation of TEI files
=================================


Trafilatura can produce and validate XML documents according to the TEI guidelines. In this tutorial, you will see how to use it to ensure data integrity and interoperability.

The Text Encoding Initiative (TEI) provides a set of guidelines and schemas for encoding data in XML (Extensible Markup Language). In 1987, a group of scholars representing fields in humanities, linguistics, and computing convened at Vassar College to put forth a set of guidelines which would become the TEI. Since then it has become a widely adopted standard for encoding and exchanging cultural heritage data, such as texts, images, and other digital objects.

The TEI guidelines cover a wide range of topics, text encoding (how to represent text structures) and metadata (such as authorship and date) are particularly relevant in this context. They ensure that files can be preserved, shared, and accessed. 

TEI file validation is the process of checking a file against the TEI schema to ensure that it conforms to the guidelines. The TEI schema defines the structure and content of a valid TEI document, including the elements, attributes, and relationships that are allowed or required.


Producing TEI files
-------------------


Trafilatura can extract information from web pages and convert it into TEI-compliant XML files. Here is how to procude a TEI file in Python:

.. code-block:: python

    # load the necessary components
    from trafilatura import fetch_url, extract

    # download a file
    downloaded = fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')

    # extract information as XML TEI and validate the result
    result = extract(downloaded, output_format='xmltei', tei_validation=True)


The ``tei_validation=True`` parameter triggers the validatation process. Trafilatura checks the resulting XML file against the TEI schema, which defines the structure and content of a valid TEI document.

You can also achieve this from the command line using the following command:

.. code-block:: bash

    trafilatura --xmltei --validate --URL "https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/"



Validating existing files
-------------------------


If you already have a TEI file and want to validate it, you can use the ``validate_tei`` function from Trafilatura. The following code returns `True` if a document is valid and outputs a message related to the first error impeding validation otherwise:

.. code-block:: python

    # load the necessary components
    from lxml import etree
    from trafilatura.xml import validate_tei

    # open a file and parse it
    mytree = etree.parse('document-name.xml')

    # validate it
    validate_tei(mytree)
    # returns True or an error message


The ``validate_tei`` function takes an XML file as input and returns ``True`` if the file is valid according to the TEI schema. Otherwise, the function outputs an error message indicating the first error impeding validation.


For more information please refer to this blog post: `Validating TEI-XML documents with Python <https://adrien.barbaresi.eu/blog/validating-tei-xml-python.html>`_
