Tutorial: Text embedding
========================

.. meta::
    :description lang=en:
        This tutorial shows how to use Trafilatura with Epsilla, a vector database to
        perform vector embedding and search.


Why perform text embedding with crawled data?
---------------------------------------------

If you are doing natural language research, you may want to perform text embeddings on text crawled with Trafilatura. 

Text embedding involves converting text into numerical vectors, and is commonly used for 

- Search (rank results by a query string)
- Clustering (group text strings by similarity)
- Anomaly detection (identify outliers)

In this tutorial, we will show you how to perform text embedding on results from Trafilatura. We will use
`Epsilla <https://www.epsilla.com/?ref=trafilatura>`_, an open source vector database for storing and searching vector embeddings.

Alternatives include `Qdrant <https://github.com/qdrant/qdrant>`_, `Redis <https://redis.io/docs/get-started/vector-database/>`, and `ChromaDB <https://docs.trychroma.com/>`_. They mostly work in a similar way.


.. note::
    For a hands-on version of this tutorial, try out the `Colab Notebook <https://colab.research.google.com/drive/1eFHO0dHyPhEF9Sm_HXcMFmJZnvP9a-aX?usp=sharing>`_.



Setup Epsilla
-------------

In this tutorial, we will need an Epsilla database server. There are two ways to get one: use the free cloud version or start one locally.

Epsilla has a `cloud version <https://cloud.epsilla.com//?ref=trafilatura>`_ with a free tier. You can sign up and get a server running in a few steps.

Alternatively, you can start one locally with a `Docker <https://docs.docker.com/get-started/>`_ image.

.. code-block:: bash

    $ docker pull epsilla/vectordb
    $ docker run --pull=always -d -p 8888:8888 epsilla/vectordb

See `Epsilla documentation <https://epsilla-inc.gitbook.io/epsilladb/quick-start>`_ for a full quick start guide.

The rest of this guide assumes you are running a local Epsilla server on port 8888. If you are using the cloud version, replace the host and port with the cloud server address.

We need to install the database client. You can do this with pip:

.. code-block:: bash

    $ pip install -U pyepsilla

We will also install langchain to use the open source BGE embedding model.

.. code-block:: bash

    $ pip install -U langchain sentence_transformers    

We can now connect to the demo server.

.. code-block:: python

    from pyepsilla import vectordb
    client = vectordb.Client(
        # replace with a production server if not running a local docker container
        host='localhost',
        port='8888'
    )

    status_code, response = client.load_db(
        db_name="TrafilaturaDB",
        db_path="/tmp/trafilatura_store"
    )
    print(response)
    
    client.use_db(db_name="TrafilaturaDB")

    # creates a table called Trafilatura
    client.drop_table('Trafilatura')
    client.create_table(
      table_name="Trafilatura",
      table_fields=[
        {"name": "ID", "dataType": "INT"},
        {"name": "Doc", "dataType": "STRING"},
        {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": 384}
      ]
    )


Crawl project homepages and store their vector embeddings in Epsilla
--------------------------------------------------------------------

Suppose we want to find the most relevant open source project based on a query string.

We will first crawl the homepage of many projects and store their vector embeddings in Epsilla.

.. code-block:: python

    # import Trafilatura and embedding model
    from trafilatura import fetch_url, extract
    from langchain.embeddings import HuggingFaceBgeEmbeddings

    model_name = "BAAI/bge-small-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}

    hf = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    # download the homepages from a few open source projects
    urls = [
        'https://www.tensorflow.org/',
        'https://pytorch.org/',
        'https://react.dev/',
    ]
    results = [extract(fetch_url(url)) for url in urls]
    
    # get the embedding vector and store it in Epsilla
    embeddings = [hf.embed_query(result) for result in results]
    records = [
        {"ID": idx, "Doc": results[idx], "Embedding": embeddings[idx]} 
        for idx in range(len(results))
    ]
    client.insert(
       table_name="Trafilatura",
       records=records
    )

Now the vector embeddings are stored in Epsilla. In the next section, we will perform a vector search.


Perform vector search
---------------------

We have stored the homepages of PyTorch, TensorFlow and React in the database. 
We can now perform a vector search to find the most relevant project based on a query string.

.. code-block:: python

    query = "A modern frontend library"
    query_embedding = hf.embed_query(query)
    status_code, response = client.query(
        table_name="Trafilatura",
        query_field="Embedding",
        query_vector=query_embedding,
        limit=1
    )
    print(response)

You will see the returned response is React! That is the correct answer. React is a modern frontend library, but PyTorch and Tensorflow are not.

.. image:: https://static.scarf.sh/a.png?x-pxid=51f549d1-aabf-473c-b971-f8d9c3ac8ac5
    :alt: 


