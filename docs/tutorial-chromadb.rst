Tutorial: Text embedding with ChromaDB
=======================================

.. meta::
    :description lang=en:
        This tutorial shows how to use Trafilatura with Chroma, a vector database to
        perform vector embedding and search.


Why perform text embedding with crawled data?
---------------------------------------------

If you are doing natural language research, you may want to perform text embeddings on text crawled with Trafilatura.

Text embedding involves converting text into numerical vectors, and is commonly used for

- Search (rank results by a query string)
- Clustering (group text strings by similarity)
- Anomaly detection (identify outliers)

In this tutorial, we will show you how to perform text embedding on results from Trafilatura. We will use
`Chroma <https://www.trychroma.com/>`_, an open source vector database for storing and searching vector embeddings. Chroma runs directly in Python, with no separate server to set up.

Alternatives include `Qdrant <https://github.com/qdrant/qdrant>`_, `Redis <https://redis.io/docs/get-started/vector-database/>`_, and `Epsilla <https://www.epsilla.com/?ref=trafilatura>`_. They mostly work in a similar way.


Setup Chroma
------------

We need to install the database client and a library to compute embeddings. You can do this with pip:

.. code-block:: bash

    $ pip install -U chromadb sentence-transformers

We can now create a Chroma client and a collection to hold our documents and their embeddings. By default Chroma keeps everything in memory; pass a ``path`` to ``chromadb.PersistentClient()`` instead if you want the collection to survive across runs.

.. code-block:: python

    import chromadb

    client = chromadb.Client()
    collection = client.create_collection(name="trafilatura")

See the `Chroma documentation <https://docs.trychroma.com/>`_ for a full quick start guide, including how to run Chroma as a standalone server instead of embedding it in your script.


Crawl project homepages and store their vector embeddings in Chroma
---------------------------------------------------------------------

Suppose we want to find the most relevant open source project based on a query string.

We will first crawl the homepage of many projects and store their vector embeddings in Chroma.

.. code-block:: python

    # import Trafilatura and the embedding model
    from trafilatura import fetch_url, extract
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("BAAI/bge-small-en")

    # download the homepages from a few open source projects
    urls = [
        'https://www.tensorflow.org/',
        'https://pytorch.org/',
        'https://getbootstrap.com/',
    ]
    results = [extract(fetch_url(url)) for url in urls]
    results = [text for text in results if text]

    # get the embedding vectors and store them in Chroma
    embeddings = model.encode(results).tolist()
    collection.add(
        ids=[str(idx) for idx in range(len(results))],
        embeddings=embeddings,
        documents=results,
    )

Now the vector embeddings are stored in Chroma. In the next section, we will perform a vector search.

.. hint::
    This loop is fine for a handful of pages. For a larger crawl, use `buffered downloads <faq.html#how-to-process-many-pages-efficiently>`_ instead of looping over ``fetch_url()``.


Perform vector search
----------------------

We have stored the homepages of PyTorch, TensorFlow and Bootstrap in the database.
We can now perform a vector search to find the most relevant project based on a query string.

.. code-block:: python

    query = "A modern frontend library"
    query_embedding = model.encode(query).tolist()
    response = collection.query(
        query_embeddings=[query_embedding],
        n_results=1,
    )
    print(response["documents"])

You will see the returned response is Bootstrap! That is the correct answer. Bootstrap is a modern frontend library, but PyTorch and Tensorflow are not.

.. seealso::
    `Tutorial: Retrieval-augmented generation (RAG) <tutorial-rag.html>`_ builds on this example to answer questions with a language model instead of just retrieving matching pages.
