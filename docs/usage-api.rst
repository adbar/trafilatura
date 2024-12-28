API
===

.. meta::
    :description lang=en:
        See how to use the official Trafilatura API to download and extract data.


Introduction
------------

With the Trafilatura API, you can:

- Download URLs or provide your own data, including web scraping capabilities
- Configure the output format to suit your needs, with support for multiple use cases

This is especially useful if you want to try out the software without installing it or if you want to support the project while saving time.


.. warning::
    The API is currently unavailable, feel free to get in touch for any inquiries.


..
    Endpoints
    ---------

    The Trafilatura API comes in two versions, available from two different gateways:

    - `Free for demonstration purposes <https://trafilatura.mooo.com>`_ (including documentation page)
    - `For a larger volume of requests <https://rapidapi.com/trafapi/api/trafilatura>`_ (documentation with code snippets and plans)


Making JSON requests
--------------------


To use the API, you will need to send a JSON request with the required headers. The API will then return a JSON string with the result.

A JSON (JavaScript Object Notation) request is a type of HTTP request that sends data in the JSON format, a lightweight, human-readable data interchange format that is widely used in web development.

Headers are sent with an HTTP request or response. They provide additional information about it, such as the type of data being sent or the authentication credentials. Common headers include ``content-type`` (format) or ``authorization`` (API key or token).

When you make a JSON request, you are sending a JSON object as the payload. This object typically contains key-value pairs that represent the data you want to process.


Examples
--------


Here are some examples of the Trafilatura API to get you started:


Command-line
~~~~~~~~~~~~

This example demonstrates how to send a POST request to the API on the command-line interface. The request specifies the URL of the webpage to extract text from and the output format as XML.

To run this example, you need to have ``curl`` installed on your system.


.. code-block:: bash

    $ curl -X POST "https://trafilatura.mooo.com/extract-demo" \
           -H "content-type: application/json" \
           --data '{
                    "url": "https://example.org",
                    "args": {
                      "output_format": "xml"
                     }
                  }'


Python
~~~~~~

This Python code snippet sends a POST request to the API to extract data from a webpage. The response is returned in JSON format.

To run this code, you need to have Python installed on your system, along with the ``requests`` library.


.. code-block:: python

    import requests

    url = "https://trafilatura.mooo.com/extract-demo"

    payload = {
	    "url": "https://example.org",
	    "args": { "output_format": "xml" }
    }
    headers = {
	    "content-type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())



Further information
-------------------

Please note that the underlying code is not currently open-sourced, feel free to reach out for specific use cases or collaborations.
