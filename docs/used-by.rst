Uses & citations
================

.. meta::
    :description lang=en:
        Trafilatura now widely used, integrated into other software packages and cited in research publications. Notable projects and institutional users are listed on this page.


Initially released to collect data for linguistic research and lexicography at the Berlin-Brandenburg Academy of Sciences, Trafilatura is used by numerous institutions, integrated into other software packages and cited in research publications across fields such as linguistics, natural language processing, computational social science, search engine optimization, information security, and artificial intelligence (large language models).

The tool earns accolades as the most efficient open-source library in benchmarks and academic evaluations. It supports language modeling by providing high-quality text data, aids data mining with efficient web data retrieval, and streamlines information extraction from unstructured content. In SEO and business analytics it gathers online data for insights and in information security, it monitors websites for threat detection.


Notable projects using this software
------------------------------------

Companies and research centers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Allen Institute for AI with the `Dolma toolkit <https://github.com/allenai/dolma>`_ used to pre-train the OLMo LLM
- HuggingFace with `DataTrove <https://github.com/huggingface/datatrove>`_ to process, filter and deduplicate text data
- IBM's `Data-Prep-Kit <https://github.com/IBM/data-prep-kit>`_, a toolkit for data preparation in a LLM context
- `Media Cloud platform <https://www.mediacloud.org>`_ for media analysis
- SciencesPo médialab through its `Minet <https://github.com/medialab/minet>`_ webmining package
- Stanford Open Virtual Assistant Lab's `STORM <https://github.com/stanford-oval/storm>`_, a LLM system that writes Wikipedia-like articles
- Swedish national center for applied AI with `SWEB: A large dataset for Scandinavian languages <https://arxiv.org/pdf/2410.04456>`_
- Technology Innovation Institute Abu Dhabi with Falcon LLM and its underlying `RefinedWeb Dataset <https://arxiv.org/abs/2306.01116>`_
- `Teclis search engine <https://teclis.com/>`_ (related to Kagi)
- The Internet Archive's `sandcrawler <https://github.com/internetarchive/sandcrawler>`_ which crawls and processes the scholarly web
- Tokyo Institute of Technology with a `Japanese Web Corpus for Large Language Models <https://arxiv.org/pdf/2404.17733>`_
- Turku University, NLP department with `FinGPT <https://turkunlp.org/gpt3-finnish>`_ models
- University of Munich (LMU), Center for Language and Information Processing, `GlotWeb project <https://github.com/cisnlp/GlotWeb>`_

The Go port `go-trafilatura <https://github.com/markusmobius/go-trafilatura>`_ is used at Microsoft Research.


Various software repositories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `Benson <https://github.com/timoteostewart/benson>`_, to turn a list of URLs into mp3s of the contents of each web page
- `CommonCrawl downloader <https://github.com/leogao2/commoncrawl_downloader>`_, to derive massive amounts of language data
- `Ethical ad server <https://github.com/readthedocs/ethical-ad-server>`_ on ReadTheDocs (hosting these doc pages)
- `GLAM Workbench <https://glam-workbench.net/web-archives/>`_ for cultural heritage (web archives section)
- `LlamaIndex <https://github.com/run-llama/llama_index>`_, a data framework for LLM applications
- `Obsei <https://www.obsei.com/>`_, a text collection and analysis tool
- `Vulristics <https://github.com/leonov-av/vulristics>`_, a framework for analyzing publicly available information about vulnerabilities
- `Website-to-Chatbot <https://github.com/Anil-matcha/Chatbase-Alternative>`_, a personalized chatbot

For more see this list of `software using Trafilatura <https://github.com/adbar/trafilatura/network/dependents>`_.


Citations in papers
-------------------

Trafilatura as a whole
^^^^^^^^^^^^^^^^^^^^^^


**To reference this software in a publication please cite the following paper:**

- Barbaresi, A. "`Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction <https://aclanthology.org/2021.acl-demo.15/>`_", in *Proceedings of ACL/IJCNLP 2021: System Demonstrations*, 2021, p. 122-131. DOI: 10.18653/v1/2021.acl-demo.15


.. image:: https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue
    :target: https://aclanthology.org/2021.acl-demo.15/
    :alt: Reference DOI: 10.18653/v1/2021.acl-demo.15

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3460969.svg
   :target: https://doi.org/10.5281/zenodo.3460969
   :alt: Zenodo archive DOI: 10.5281/zenodo.3460969

.. code-block:: shell

    @inproceedings{barbaresi-2021-trafilatura,
      title = {{Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction}},
      author = "Barbaresi, Adrien",
      booktitle = "Proceedings of the Joint Conference of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
      pages = "122--131",
      publisher = "Association for Computational Linguistics",
      url = "https://aclanthology.org/2021.acl-demo.15",
      year = 2021,
    }


Date extraction (htmldate)
^^^^^^^^^^^^^^^^^^^^^^^^^^

The date extraction component ``htmldate`` is referenced in the following publication:

- Barbaresi, A. "`htmldate: A Python package to extract publication dates from web pages <https://doi.org/10.21105/joss.02439>`_", *Journal of Open Source Software*, 5(51), 2439, 2020. DOI: 10.21105/joss.02439

.. image:: https://joss.theoj.org/papers/10.21105/joss.02439/status.svg
   :target: https://doi.org/10.21105/joss.02439
   :alt: JOSS article

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3459599.svg
   :target: https://doi.org/10.5281/zenodo.3459599
   :alt: Zenodo archive

.. code-block:: shell

    @article{barbaresi-2020-htmldate,
      title = {{htmldate: A Python package to extract publication dates from web pages}},
      author = "Barbaresi, Adrien",
      journal = "Journal of Open Source Software",
      volume = 5,
      number = 51,
      pages = 2439,
      url = {https://doi.org/10.21105/joss.02439},
      publisher = {The Open Journal},
      year = 2020,
    }


Publications citing Trafilatura
-------------------------------


- Alakukku, L. (2022). "Domain specific boilerplate removal from web pages with entropy and clustering", Master's thesis, University of Aalto.
- Alexandrescu, A., & Butincu, C.N. (2023). Decentralized news-retrieval architecture using blockchain technology. Mathematics, 11(21), 4542.
- Alhamzeh, A., Bouhaouel, M., Egyed-Zsigmond, E., & Mitrović, J. (2021). "DistilBERT-based Argumentation Retrieval for Answering Comparative Questions", Proceedings of CLEF 2021 – Conference and Labs of the Evaluation Forum.
- Altinok, D. (2024). Bella Turca: A Large-Scale Dataset of Diverse Text Sources for Turkish Language Modeling. In International Conference on Text, Speech, and Dialogue (pp. 196-213). Cham: Springer Nature Switzerland.
- Bender, M., Bubenhofer, N., Dreesen, P., Georgi, C., Rüdiger, J. O., & Vogel, F. (2022). Techniken und Praktiken der Verdatung. Diskurse–digital, 135-158.
- Bevendorff, J., Gupta, S., Kiesel, J., & Stein, B. (2023). An Empirical Comparison of Web Content Extraction Algorithms.
- Book, L. (2023). Evaluating and comparing different key phrase-based web scraping methods for training domain-specific fasttext models, Master's thesis, KTH Royal Institute of Technology.
- Bozarth, L., & Budak, C. (2021). "An Analysis of the Partnership between Retailers and Low-credibility News Publishers", Journal of Quantitative Description: Digital Media, 1.
- Brandon, C., Doherty, A. J., Kelly, D., Leddin, D., & Margaria, T. (2023). HIPPP: Health Information Portal for Patients and Public. Applied Sciences, 13(16), 9453.
- Braun, D. (2021). "Automated Semantic Analysis, Legal Assessment, and Summarization of Standard Form Contracts", PhD Thesis, Technische Universität München.
- Chen, X., Zeynali, A., Camargo, C., Flöck, F., Gaffney, D., Grabowicz, P., ... & Samory, M. (2022). SemEval-2022 Task 8: Multilingual news article similarity. In Proceedings of the 16th International Workshop on Semantic Evaluation (SemEval-2022) (pp. 1094-1106).
- Cordeiro, J. P., Silvano, P. M., Leal, A., & Pais, S. (2024). TELP–Text Extraction with Linguistic Patterns. In Proceedings of the 3rd Annual Meeting of the Special Interest Group on Under-resourced Languages@ LREC-COLING 2024 (pp. 337-344).
- Crummett, L. T., & Aslam, M. H. (2023). Diabetes websites lack information on dietary causes, risk factors, and preventions for type 2 diabetes. Frontiers in Public Health, 11, 1159024.
- De Cesare, A. M. (2023). Assessing the quality of ChatGPT’s generated output in light of human-written texts: A corpus study based on textual parameters. CHIMERA: Revista de Corpus de Lenguas Romances y Estudios Lingüísticos, 10, 179-210.
- Di Giovanni, M., Tasca, T., & Brambilla, M. (2022). DataScience-Polimi at SemEval-2022 Task 8: Stacking Language Models to Predict News Article Similarity. In Proceedings of the 16th International Workshop on Semantic Evaluation (SemEval-2022) (pp. 1229-1234).
- Dumitru, V., Iorga, D., Ruseti, S., & Dascalu, M. (2023). Garbage in, garbage out: An analysis of HTML text extractors and their impact on NLP performance. In 2023 24th International Conference on Control Systems and Computer Science (CSCS) (pp. 403-410). IEEE.
- El Madbouly, M., Ahmed, Y. A., & Salem, M. A. M. (2023). Multimodality Web Page Analysis for Fake News Detection. In 2023 2nd International Conference on Smart Cities 4.0 (pp. 460-465). IEEE.
- Fröbe, M., Hagen, M., Bevendorff, J., Völske, M., Stein, B., Schröder, C., ... & Potthast, M. (2021). "The Impact of Main Content Extraction on Near-Duplicate Detection". arXiv preprint arXiv:2111.10864.
- Gao, L., Biderman, S., Black, S., Golding, L., Hoppe, T., Foster, C., ... & Leahy, C. (2020). "The Pile: An 800GB Dataset of Diverse Text for Language Modeling", arXiv preprint arXiv:2101.00027.
- Garifo, G., Sasso, S., Vetrò, A., & De Martin, J. C. Speakit: A Text-to-Speech Based Podcast Generator for Italian Texts. Available at SSRN 4821549.
- Gopalakrishnan, S., Chen, V. Z., Dou, W., Hahn-Powell, G., Nedunuri, S., & Zadrozny, W. W. (2023). Text to Causal Knowledge Graph: A Framework to Synthesize Knowledge from Unstructured Business Texts into Causal Graphs. Information, 14(7), 367.
- Harrando, I., & Troncy, R. (2021). "Explainable Zero-Shot Topic Extraction Using a Common-Sense Knowledge Graph", In 3rd Conference on Language, Data and Knowledge (LDK 2021). OpenAccess Series in Informatics, Dagstuhl Publishing.
- Hartmann, S. (2023). Open Corpus Linguistics–or How to overcome common problems in dealing with corpus data by adopting open research practices.
- Hunter, S. B., Mathews, F., & Weeds, J. (2023). Using hierarchical text classification to investigate the utility of machine learning in automating online analyses of wildlife exploitation. Ecological Informatics, 75, 102076.
- Hunter, S. B., Oedin, M., Weeds, J., & Mathews, F. (2024). Exploring the potential for online data sources to enhance species threat mapping through the case study of global bat exploitation. Conservation Biology, e14242.
- Indig, B., Sárközi-Lindner, Z., & Nagy, M. (2022). Use the Metadata, Luke!–An Experimental Joint Metadata Search and N-gram Trend Viewer for Personal Web Archives. In Proceedings of the 2nd International Workshop on Natural Language Processing for Digital Humanities (pp. 47-52).
- Johannsen, B. (2023). Fußball und safety: Eine framesemantische Perspektive auf Diskurse über trans Sportler* innen. Queere Vielfalt im Fußball, 176.
- Jung, G., Han, S., Kim, H., Kim, K., & Cha, J. (2022). Extracting the Main Content of Web Pages Using the First Impression Area. IEEE Access, 10, 129958-129969
- Jung, G., Cha, J. (2023). New Visual Features for HTML Main Content Extraction. Journal of Digital Contents Society.
- Karabulut, M., & Mayda, İ. (2020). "Development of Browser Extension for HTML Web Page Content Extraction", In 2020 International Congress on Human-Computer Interaction, Optimization and Robotic Applications (HORA) (pp. 1-6). IEEE.
- Khusainov, A., Suleymanov, D., Gilmullin, R., Minsafina, A., Kubedinova, L., & Abdurakhmonova, N. "First Results of the “TurkLang-7” Project: Creating Russian-Turkic Parallel Corpora and MT Systems", In CMCL (pp. 90-101).
- Kliche, F., Heid, U., Knackstedt, R., & Klupp, T. (2023). An educational Gamebook on computational linguistic methods for the development of taxonomies. In Proceedings of the 1st Workshop on Teaching for NLP (pp. 37-43).
- Küehn, P., Relke, D. N., & Reuter, C. (2023). Common Vulnerability Scoring System Prediction based on Open Source Intelligence Information Sources. Computers & Security, 103286.
- Kuehn, P., Schmidt, M., & Reuter, C. (2023). ThreatCrawl: A BERT-based Focused Crawler for the Cybersecurity Domain. arXiv preprint arXiv:2304.11960.
- Laippala, V., Rönnqvist, S., Hellström, S., Luotolahti, J., Repo, L., Salmela, A., ... & Pyysalo, S. (2020). "From Web Crawl to Clean Register-Annotated Corpora", Proceedings of the 12th Web as Corpus Workshop (pp. 14-22).
- Laippala, V., Salmela, A., Rönnqvist, S., Aji, A. F., Chang, L. H., Dhifallah, A., ... & Pyysalo, S. (2022). Towards better structured and less noisy Web data: Oscar with Register annotations. In Proceedings of the Eighth Workshop on Noisy User-generated Text (W-NUT 2022) (pp. 215-221).
- Li, Q., Chen, Z., Wang, W., Wang, W., Ye, S., Jin, Z., ... & Dai, J. (2024). OmniCorpus: An Unified Multimodal Corpus of 10 Billion-Level Images Interleaved with Text. arXiv preprint arXiv:2406.08418.
- Luukkonen, R., Komulainen, V., Luoma, J., Eskelinen, A., Kanerva, J., Kupari, H. M., ... & Pyysalo, S. (2023). FinGPT: Large Generative Models for a Small Language. arXiv preprint arXiv:2311.05640.
- Madrid-Morales, D. (2021). "Who Set the Narrative? Assessing the Influence of Chinese Media in News Coverage of COVID-19 in 30 African Countries", Global Media and China, 6(2), 129-151.
- Mannino, M., Garcia, J., Hazim, R., Abouzied, A., & Papotti, P. (2024). Data Void Exploits: Tracking & Mitigation Strategies. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management (pp. 1627-1637).
- Meier-Vieracker, S. (2022). "Fußballwortschatz digital–Korpuslinguistische Ressourcen für den Sprachunterricht." Korpora Deutsch als Fremdsprache (KorDaF), 2022/01 (pre-print).
- Meier-Vieracker, S. (2024). Klatsche oder Kantersieg? Framesemantische Analysen zur Perspektivierung in Fußballspielberichten. Journal für Medienlinguistik, 6(1), 10-38.
- Meng, K. (2021). "An End-to-End Computational System for Monitoring and Verifying Factual Claims" (pre-print).
- Miquelina, N., Quaresma, P., & Nogueira, V. B. (2022). Generating a European Portuguese BERT Based Model Using Content from Arquivo. pt Archive. In International Conference on Intelligent Data Engineering and Automated Learning (pp. 280-288). Springer, Cham.
- Naira, A. M., & Benelallam, I. (2023). Evaluating ESG Impacts in African Cities through Topic-Level Sentiment Analysis. In 2023 10th International Conference on Wireless Networks and Mobile Communications (WINCOM) (pp. 1-6). IEEE.
- Nayekoo, Y., Katrenko, S., Hoste, V., Maladry, A., & Lefever, E. (2024). Shared Task for Cross-lingual Classification of Corporate Social Responsibility (CSR) Themes and Topics. In Proceedings of the Joint Workshop of the 7th Financial Technology and Natural Language Processing, the 5th Knowledge Discovery from Unstructured Data in Financial Services, and the 4th Workshop on Economics and Natural Language Processing@ LREC-COLING 2024 (pp. 283-291).
- Nguyen, Q.C., et al. (2024). Rosie, a Health Education Question-and-Answer Chatbot for New Mothers: Randomized Pilot Study. JMIR Formative Research, 8(1), e51361.
- Nissopoulou, T. X. (2023). Web content classification analysis, MSc thesis, International Hellenic University.
- Nolda, A., Barbaresi, A., & Geyken, A. (2023). Korpora für die lexikographische Beschreibung diatopischer Variation in der deutschen Standardsprache. Korpora in der germanistischen Sprachwissenschaft: Mündlich, schriftlich, multimedial, 29.
- Norlund, T., Isbister, T., Gyllensten, A. C., Santos, P. D., Petrelli, D., Ekgren, A., & Sahlgren, M. (2024). SWEb: A Large Web Dataset for the Scandinavian Languages. arXiv preprint arXiv:2410.04456.
- Öhman, J., Verlinden, S., Ekgren, A., Gyllensten, A. C., Isbister, T., Gogoulou, E., ... & Sahlgren, M. (2023). The Nordic Pile: A 1.2 TB Nordic Dataset for Language Modeling. arXiv preprint arXiv:2303.17183.
- Okazaki, N., Hattori, K., Shota, H., Iida, H., Ohi, M., Fujii, K., ... & Mizuki, S. (2024). Building a Large Japanese Web Corpus for Large Language Models. arXiv preprint arXiv:2404.17733.
- Paster, K., Santos, M. D., Azerbayev, Z., & Ba, J. (2023). Openwebmath: An open dataset of high-quality mathematical web text. arXiv preprint arXiv:2310.06786.
- Pastor-Galindo, J., Sandlin, H. Â., Mármol, F. G., Bovet, G., & Pérez, G. M. (2024). A Big Data architecture for early identification and categorization of dark web sites. Future Generation Computer Systems, 157, 67-81.
- Penedo, G., Malartic, Q., Hesslow, D., Cojocaru, R., Alobeidli, H., Cappelli, A., ... & Launay, J. (2024). The RefinedWeb dataset for Falcon LLM: Outperforming curated corpora with web data only. Advances in Neural Information Processing Systems, 36, 79155-79172.
- Piskorski, J., Stefanovitch, N., Da San Martino, G., & Nakov, P. (2023). Semeval-2023 task 3: Detecting the category, the framing, and the persuasion techniques in online news in a multi-lingual setup. In Proceedings of the 17th International Workshop on Semantic Evaluation (SemEval-2023) (pp. 2343-2361).
- Pohlmann, J., Barbaresi, A., & Leinen, P. (2023). Platform regulation and “overblocking”–The NetzDG discourse in Germany. Communications, 48(3), 395-419.
- Qiu, J., Lv, H., Jin, Z., Wang, R., Ning, W., Yu, J., ... & He, C. (2024). Wanjuan-cc: A safe and high-quality open-sourced english webtext dataset. arXiv preprint arXiv:2402.19282.
- Rastislav, K. (2024). Backend platformy pro sdílené ověřování faktů (Master's thesis, České vysoké učení technické v Praze. Vypočetní a informační centrum.)
- Razuvayevskaya, O., Wu, B., Leite, J. A., Heppell, F., Srba, I., Scarton, C., ... & Song, X. (2024). Comparison between parameter-efficient techniques and full fine-tuning: A case study on multilingual news article classification. Plos one, 19(5), e0301738.
- Reina, L. A. V. (2023). NLP Meets Agronomy: Document Classification for Plant Health Surveillance, Master's thesis.
- Robertson, F., Lagus, J., & Kajava, K. (2021). "A COVID-19 news coverage mood map of Europe", Proceedings of the EACL Hackashop on News Media Content Analysis and Automated Report Generation (pp. 110-115).
- Salmela, A. (2022). "Distinguishing Noise and Main Text Content from Web-Sourced Plain Text Documents Using Sequential Neural Networks", Master's thesis, University of Turku.
- Sawczyn, A., Binkowski, J., Janiak, D., Augustyniak, Ł., & Kajdanowicz, T. (2021). "Fact-checking: relevance assessment of references in the Polish political domain", Procedia Computer Science, 192, 1285-1293.
- Schamel, T., Braun, D., & Matthes, F. (2022). Structured Extraction of Terms and Conditions from German and English Online Shops. In Proceedings of The Fifth Workshop on e-Commerce and NLP (ECNLP 5) (pp. 181-190).
- Srikanth, N., Sarkar, R., Mane, H., Aparicio, E., Nguyen, Q., Rudinger, R., & Boyd-Graber, J. (2024). Pregnant Questions: The Importance of Pragmatic Awareness in Maternal Health Question Answering. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers) (pp. 7246-7261).
- Sutter, T., Bozkir, A. S., Gehring, B., & Berlich, P. (2022). Avoiding the Hook: Influential Factors of Phishing Awareness Training on Click-Rates and a Data-Driven Approach to Predict Email Difficulty Perception. IEEE Access, 10, 100540-100565.
- Ter-Akopyan, B. (2022). "Identification of Political Leaning in German News", Master's thesis, Ludwig Maximilian University of Munich.
- Van Nooten, J., & Kosar, A. (2024). Advancing CSR Theme and Topic Classification: LLMs and Training Enhancement Insights. In Proceedings of the Joint Workshop of the 7th Financial Technology and Natural Language Processing, the 5th Knowledge Discovery from Unstructured Data in Financial Services, and the 4th Workshop on Economics and Natural Language Processing@ LREC-COLING 2024 (pp. 292-305).
- Varlamov, M., Galanin, D., Bedrin, P., Duda, S., Lazarev, V., & Yatskov, A. (2022). A Dataset for Information Extraction from News Web Pages. In 2022 Ivannikov Ispras Open Conference (ISPRAS) (pp. 100-106). IEEE.
- Waheed, A., Qunaibi, S., Barradas, D., & Weinberg, Z. (2022). Darwin's Theory of Censorship: Analysing the Evolution of Censored Topics with Dynamic Topic Models. In Proceedings of the 21st Workshop on Privacy in the Electronic Society (pp. 103-108).
- Xu, Z., Liu, Z., Yan, Y., Liu, Z., Xiong, C., & Yu, G. (2024). Cleaner Pretraining Corpus Curation with Neural Web Scraping. arXiv preprint arXiv:2402.14652.
- Yang, Y., & Wang, X. (2024). AcawebAgent: A Large Language Model-Powered Assistant for Early Academic Research. In 2024 5th International Conference on Computer Engineering and Application (ICCEA) (pp. 302-305). IEEE.
- Zinn, J. O., & Müller, M. (2021). "Understanding discourse and language of risk", Journal of Risk Research, 1-14.



Publications citing Htmldate
----------------------------

See `citation page of htmldate's documentation <https://htmldate.readthedocs.io/en/latest/used-by.html>`_.

