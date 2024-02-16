API
===

.. meta::
    :description lang=en:
        See how to use the official Trafilatura API to download and extract data for free or for larger volumes.


Introduction
------------

Simplify the process of turning URLs and HTML into structured, meaningful data. Use the last version of the software straight from the application programming interface.  The Trafilatura API gives you access to add its capabilities to your projects and apps.

This is especially useful if you want to try out Trafilatura without installing it or if you want to support the project while saving time.

- Download URLs or provide your own data, web scraping included
- Configurable output with conversion to supported formats


Endpoints
---------

The official API comes in two versions, available from two different gateways:

- `Free for demonstration purposes <https://trafilatura.mooo.com>`_ (including documentation page)
- `For a larger volume of requests <https://rapidapi.com/trafapi/api/trafilatura>`_ (documentation with code snippets and plans)


Examples
--------

The API takes JSON as input and a corresponding header is required. It then returns a JSON string with the result.


CLI
~~~

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

The API is still an early-stage product and the code is not available under an open-source license.

