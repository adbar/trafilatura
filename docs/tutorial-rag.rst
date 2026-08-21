Tutorial: Retrieval-augmented generation (RAG)
================================================

.. meta::
    :description lang=en:
        This tutorial shows how to use Trafilatura with LlamaIndex to build a
        retrieval-augmented generation (RAG) pipeline over crawled web pages.


Why build a RAG pipeline with crawled data?
--------------------------------------------

Retrieval-augmented generation (RAG) lets a large language model answer questions using a specific set of documents rather than its training data alone. The model is given the most relevant passages retrieved from your own corpus, which reduces hallucinations and makes it possible to cite sources.

Trafilatura is a natural fit for the retrieval side of this pipeline: it turns crawled web pages into clean text, ready to be chunked, embedded, and indexed.

This tutorial builds on `the previous one on vector embeddings <tutorial-chromadb.html>`_ and uses `LlamaIndex <https://www.llamaindex.ai/>`_, a data framework for LLM applications, to handle chunking, embedding, and retrieval in a few lines of code. Alternatives include `LangChain <https://www.langchain.com/>`_ and `Haystack <https://haystack.deepset.ai/>`_, which cover similar ground.


Setup
-----

We need LlamaIndex along with an OpenAI-compatible client for the embedding model and the language model:

.. code-block:: bash

    $ pip install -U llama-index llama-index-llms-openai llama-index-embeddings-openai

This tutorial uses OpenAI's API, so you will need an API key set as an environment variable:

.. code-block:: bash

    $ export OPENAI_API_KEY="sk-..."

.. note::
    LlamaIndex also supports local, open-source models (for example through `Ollama <https://ollama.com/>`_ or `Hugging Face <https://huggingface.co/>`_ embeddings) if you would rather not rely on a paid API. See the `LlamaIndex documentation <https://docs.llamaindex.ai/>`_ for the corresponding integrations.


Crawl and extract a small corpus
---------------------------------

We first gather a handful of pages on a topic and extract their main text with Trafilatura. LlamaIndex works with lightweight ``Document`` objects, so we wrap each extraction result accordingly.

.. code-block:: python

    from trafilatura import fetch_url, extract
    from llama_index.core import Document

    urls = [
        'https://en.wikipedia.org/wiki/Web_scraping',
        'https://en.wikipedia.org/wiki/Data_mining',
        'https://en.wikipedia.org/wiki/Web_crawler',
    ]

    documents = []
    for url in urls:
        downloaded = fetch_url(url)
        text = extract(downloaded)
        if text:
            documents.append(Document(text=text, metadata={"source": url}))

    print(f'{len(documents)} documents ready for indexing')

.. hint::
    This loop is fine for a handful of pages. For a larger crawl, use `buffered downloads <faq.html#how-to-process-many-pages-efficiently>`_ instead of looping over ``fetch_url()``.


Build the index
----------------

LlamaIndex takes care of splitting the documents into chunks, computing embeddings, and storing them in an in-memory vector index:

.. code-block:: python

    from llama_index.core import VectorStoreIndex

    index = VectorStoreIndex.from_documents(documents)

.. hint::
    For a persistent or larger-scale setup, swap the default in-memory store for `Chroma <tutorial-chromadb.html>`_ or another vector database supported by LlamaIndex's `vector store integrations <https://docs.llamaindex.ai/en/stable/module_guides/storing/vector_stores/>`_.


Query with retrieval-augmented generation
-------------------------------------------

The query engine retrieves the most relevant chunks and passes them to the language model along with the question:

.. code-block:: python

    query_engine = index.as_query_engine()
    response = query_engine.query("What is the difference between web scraping and web crawling?")

    print(response)
    for node in response.source_nodes:
        print(f"- {node.metadata['source']} (score: {node.score:.2f})")

The answer is grounded in the pages you crawled, and the source pages used to generate it are listed alongside it — making it straightforward to check where the information comes from.
