Tutorial: Building a training corpus with Hugging Face Datasets
==================================================================

.. meta::
    :description lang=en:
        This tutorial shows how to use Trafilatura with Hugging Face Datasets to build
        a text corpus suitable for language model pre-training or fine-tuning.


Why build a corpus this way?
------------------------------

Trafilatura is already used to build large-scale training corpora for language models, for instance the Allen Institute for AI's `Dolma toolkit <https://github.com/allenai/dolma>`_, HuggingFace's own `DataTrove <https://github.com/huggingface/datatrove>`_, and the `RefinedWeb dataset <https://arxiv.org/abs/2306.01116>`_ behind the Falcon LLM. See the `uses & citations page <used-by.html>`_ for more examples.

This tutorial shows a small-scale version of the same idea: crawl a set of pages, extract clean text and metadata with Trafilatura, and assemble the result into a `Hugging Face Dataset <https://huggingface.co/docs/datasets/>`_ that can be filtered, saved, and later used for training or fine-tuning.


Setup
-----

.. code-block:: bash

    $ pip install -U datasets


Crawl, extract, and collect metadata
--------------------------------------

For a training corpus you typically want more than the bare text: language, title, and date are useful for filtering and deduplication later on. ``bare_extraction()`` returns all of this in one call.

.. code-block:: python

    from trafilatura import fetch_url, bare_extraction

    urls = [
        'https://www.tensorflow.org/',
        'https://pytorch.org/',
        'https://getbootstrap.com/',
    ]

    records = []
    for url in urls:
        downloaded = fetch_url(url)
        doc = bare_extraction(downloaded, url=url, with_metadata=True, target_language="en")
        if doc and doc.text:
            records.append({
                "url": url,
                "title": doc.title,
                "date": doc.date,
                "language": doc.language,
                "text": doc.text,
            })

    print(f'{len(records)} pages extracted')

.. hint::
    For a real corpus, gather your input URLs with `sitemaps or feeds <tutorial-corpus.html>`_, consider `courlan <https://github.com/adbar/courlan>`_ for link filtering, and use `buffered downloads <faq.html#how-to-process-many-pages-efficiently>`_ instead of looping over ``fetch_url()`` to crawl many pages efficiently.


Assemble and inspect the dataset
-----------------------------------

.. code-block:: python

    from datasets import Dataset

    dataset = Dataset.from_list(records)
    print(dataset)
    print(dataset[0]["title"], "—", len(dataset[0]["text"]), "characters")

``Dataset`` objects support the usual filtering, mapping, and shuffling operations, for example to drop very short pages before training:

.. code-block:: python

    dataset = dataset.filter(lambda row: len(row["text"]) > 500)


Save or share the dataset
---------------------------

Save it locally in a format that loads back instantly:

.. code-block:: python

    dataset.save_to_disk("trafilatura_corpus")

    # later on
    from datasets import load_from_disk
    dataset = load_from_disk("trafilatura_corpus")

Or push it to the `Hugging Face Hub <https://huggingface.co/docs/hub/datasets>`_ to share it (this requires being logged in with ``huggingface-cli login``):

.. code-block:: python

    dataset.push_to_hub("your-username/trafilatura-corpus")

.. seealso::
    `Tutorial: Building a web corpus <tutorial-corpus.html>`_, `Deduplication <deduplication.html>`_, `Uses & citations <used-by.html>`_
