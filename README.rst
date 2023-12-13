Trafilatura: Advanced Web Data Extraction and Analysis
======================================================

Trafilatura is a cutting-edge Python package and command-line tool, meticulously designed for advanced web data extraction and analysis. It offers a comprehensive solution for extracting text, metadata, and comments from web pages, making it an indispensable tool for researchers, developers, data scientists, and anyone involved in web scraping, data mining, and content analysis.

.. image:: docs/trafilatura-logo.png
   :alt: Trafilatura Logo
   :align: center
   :width: 60%

|

.. image:: https://img.shields.io/pypi/v/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python package

.. image:: https://img.shields.io/pypi/pyversions/trafilatura.svg
    :target: https://pypi.python.org/pypi/trafilatura
    :alt: Python versions

.. image:: https://readthedocs.org/projects/trafilatura/badge/?version=latest
    :target: http://trafilatura.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/codecov/c/github/adbar/trafilatura.svg
    :target: https://codecov.io/gh/adbar/trafilatura
    :alt: Code Coverage

.. image:: https://static.pepy.tech/badge/trafilatura/month
    :target: https://pepy.tech/project/trafilatura
    :alt: Downloads

.. image:: https://img.shields.io/badge/DOI-10.18653%2Fv1%2F2021.acl--demo.15-blue
    :target: https://aclanthology.org/2021.acl-demo.15/
    :alt: Reference DOI: 10.18653/v1/2021.acl-demo.15

|

.. image:: docs/trafilatura-demo.gif
    :alt: Demo as GIF image
    :align: center
    :width: 85%
    :target: https://trafilatura.readthedocs.org/

Introduction
------------

Trafilatura is not just a tool; it's a comprehensive ecosystem designed for the modern web. It goes beyond traditional scraping methods to offer a nuanced approach to data extraction. With its advanced algorithms and modular design, Trafilatura simplifies the process of turning raw HTML into structured, meaningful data. It's built to handle the complexities of today's web, including dynamic content, various data formats, and multilingual text.

The tool's versatility makes it ideal for a wide range of applications, from academic research in linguistics and social sciences to practical uses in SEO, business analytics, and cybersecurity. Trafilatura is more than a scraper; it's a gateway to understanding and leveraging web content for knowledge discovery and data-driven insights.

Features
~~~~~~~~

Trafilatura comes packed with a plethora of features, each designed to tackle specific challenges in web data extraction:

- **Advanced Web Crawling**: Dive deep into the web with sophisticated crawling techniques. Trafilatura supports focused crawling, adhering to politeness rules, and efficiently navigates through sitemaps and feeds (including ATOM, JSON, and RSS formats).

- **Seamless Online and Offline Processing**: Whether you're working with live URLs or offline HTML files, Trafilatura handles it all. Its parallel processing capabilities ensure efficient queue management and data conversion.

- **Robust Text and Metadata Extraction**: At its core, Trafilatura excels in extracting main text and metadata. Leveraging LXML and a blend of common patterns and algorithms (like jusText and a fork of readability-lxml), it achieves a fine balance between precision and recall.

- **Rich Output Formats**: Catering to diverse needs, Trafilatura supports multiple output formats. Choose from plain text, Markdown, CSV (with metadata), JSON, XML (including text formatting and page structure), and TEI-XML for scholarly needs.

- **Language Detection**: Trafilatura automatically detects the language of extracted content, adding an extra layer of intelligence to your data processing workflow.

- **Graphical User Interface (GUI)**: For those who prefer a visual approach, Trafilatura offers a user-friendly GUI, making web scraping accessible to everyone.

- **Performance Optimizations**: Speed is of the essence. Trafilatura is optimized for performance, ensuring quick and efficient processing even for large-scale data extraction tasks.

- **Customizability and Extensibility**: Tailor Trafilatura to your needs. Its modular design and extensive configuration options allow for customization and extensibility.

- **Community-Driven Development**: Trafilatura thrives on community input. Regular updates, feature additions, and optimizations are driven by user feedback and contributions.

- **Comprehensive Documentation and Support**: Get started quickly and dive deep into advanced features with our extensive documentation. The community and developers are always ready to provide support and guidance.

Evaluation and Alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~

Trafilatura stands out in the landscape of web scraping and data extraction tools. Its performance and capabilities have been rigorously evaluated against other popular tools in the domain:

- **Benchmarking Excellence**: Trafilatura consistently outperforms other open-source libraries in benchmarks, showcasing its efficiency and accuracy in extracting web content.

- **Comparative Analysis**: Detailed comparisons with tools like html_text, inscriptis, newspaper3k, and others highlight Trafilatura's superior precision, recall, and overall performance.

- **Recognition and Endorsements**: The tool has received accolades for its effectiveness, including being recognized as the most efficient open-source library in ScrapingHub's article extraction benchmark and receiving high praise in academic evaluations.

For a detailed breakdown of these evaluations and to see how Trafilatura compares with alternatives, visit our benchmark and evaluation pages.

[Include the existing benchmark table and other evaluations here]

Usage and Documentation
-----------------------

Getting started with Trafilatura is straightforward, thanks to its well-structured documentation and easy-to-follow guides:

- **Installation**: Setting up Trafilatura is a breeze. Install it using pip with just a few commands. Our installation guide walks you through the process step-by-step.

- **Command-Line Interface**: For those who prefer working directly from the command line, Trafilatura offers a robust CLI. Learn how to perform various tasks and leverage the full power of the tool from the terminal.

- **Python Integration**: Integrate Trafilatura into your Python projects with ease. Our documentation provides examples and best practices for using Trafilatura as a Python library.

- **R Language Support**: Trafilatura extends its capabilities to the R community. Discover how to use Trafilatura in your R projects with our dedicated guide.

- **Core Python Functions**: Dive into the core functionalities of Trafilatura. Understand the key functions and how to use them effectively in your projects.

- **Interactive Python Notebook**: Explore Trafilatura's features interactively with our Python Notebook. It's a great way to get hands-on experience and see real-world examples.

- **Tutorials and Use Cases**: Learn through practical examples. Our tutorials cover various scenarios, from text embedding for vector search to building custom web corpora and generating word frequency lists.

- **Video Tutorials**: Prefer learning through videos? Check out our YouTube playlist for a series of web scraping tutorials and how-tos.

For more information and detailed guides, visit [Trafilatura's Documentation](https://trafilatura.readthedocs.io/).

License
-------

*Trafilatura* is distributed under the `GNU General Public License v3.0 <https://github.com/adbar/trafilatura/blob/master/LICENSE>`_. This license promotes freedom and openness in software development, ensuring that Trafilatura remains a community-driven and accessible tool.

If you wish to redistribute this library but are concerned about the license conditions, consider interacting at arm's length, multi-licensing with compatible licenses, or contacting the author for more options.

For insights into GPL and free software licensing, especially in a business context, see [GPL and Free Software Licensing: What's in it for Business?](https://web.archive.org/web/20230127221311/https://www.techrepublic.com/article/gpl-and-free-software-licensing-whats-in-it-for-business/)

Context
-------

Trafilatura is more than just a software package; it's a solution born out of the need for high-quality, reliable web data extraction. Developed with scientific research and practical applications in mind, it addresses the challenges faced in web corpus construction and data analysis. The tool's development is guided by the principles of accuracy, efficiency, and user-friendliness, making it a valuable asset in various fields.

Whether it's for linguistic analysis, natural language processing, social science research, or practical applications like SEO and business analytics, Trafilatura provides the means to extract and process web data effectively. Its development is an ongoing process, with each update bringing enhancements and new features based on user feedback and technological advancements.

Contributing
~~~~~~~~~~~~

Your contributions make Trafilatura better. We encourage community involvement and welcome contributions of all forms:

- **Bug Reports and Feature Requests**: Encountered an issue or have an idea for a new feature? File a bug report or feature request on our [GitHub Issues page](https://github.com/adbar/trafilatura/issues).

- **Code Contributions**: Interested in contributing code? Whether it's fixing bugs, adding new features, or improving documentation, your code contributions are invaluable. Check out our [Contributing Guide](https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md) for guidelines on how to contribute.

- **Community Support and Discussion**: Join the conversation and connect with other users and contributors. Engage with the community on [Twitter](https://twitter.com/adbarbaresi), participate in discussions, and share your experiences and insights.

- **Documentation and Tutorials**: Help improve our documentation by writing guides, tutorials, or translating existing content. Good documentation is key to making the tool accessible to a wider audience.

A special thanks to all the [contributors](https://github.com/adbar/trafilatura/graphs/contributors) who have played a part in developing and enhancing Trafilatura.

Roadmap
~~~~~~~

Trafilatura is continuously evolving, with development guided by user needs and technological advancements. Our roadmap outlines planned enhancements, new features, and milestones:

- **Upcoming Features**: Stay tuned for upcoming features that will further enhance Trafilatura's capabilities. We're constantly working on adding new functionalities and optimizations.

- **Community Feedback and Requests**: User feedback is a driving force behind our development process. We prioritize features and improvements based on community input and requests.

- **Long-Term Goals**: Our long-term vision for Trafilatura includes expanding its applications, improving performance, and ensuring it remains at the forefront of web data extraction technology.

For detailed information on upcoming enhancements and milestones, visit our [Issues Page](https://github.com/adbar/trafilatura/milestones).

Author
~~~~~~

Trafilatura is the brainchild of Adrien Barbaresi, a researcher and developer with a passion for linguistics, natural language processing, and data science. The project is part of his broader efforts to develop methods for extracting information from web documents to build text databases for research.

Adrien's work focuses on the challenges of extracting and pre-processing web texts to meet the rigorous standards of scientific research. His expertise in web corpus construction and text data analysis has been instrumental in shaping Trafilatura into a tool that meets the needs of both researchers and practitioners.

For more about Adrien Barbaresi's work and contributions:

- Barbaresi, A. [Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction](https://aclanthology.org/2021.acl-demo.15/), Proceedings of ACL/IJCNLP 2021: System Demonstrations, 2021, p. 122-131.
- Barbaresi, A. "`Generic Web Content Extraction with Open-Source Software <https://hal.archives-ouvertes.fr/hal-02447264/document>`_", Proceedings of KONVENS 2019, Kaleidoscope Abstracts, 2019.
- Barbaresi, A. "`Efficient construction of metadata-enhanced web corpora <https://hal.archives-ouvertes.fr/hal-01371704v2/document>`_", Proceedings of the `10th Web as Corpus Workshop (WAC-X) <https://www.sigwac.org.uk/wiki/WAC-X>`_, 2016.

Software Ecosystem
~~~~~~~~~~~~~~~~~~

Trafilatura is part of a larger ecosystem of tools and libraries, each contributing to the field of web data extraction and analysis. This ecosystem includes:

- **Complementary Tools**: A range of tools that work alongside Trafilatura to provide additional functionalities like advanced data processing, visualization, and integration with other data analysis frameworks.

- **Community Projects**: Projects and initiatives by the community that extend the capabilities of Trafilatura, including plugins, extensions, and integrations with other software.

- **Research and Development**: Ongoing research projects that utilize Trafilatura for data collection and analysis, contributing to advancements in fields such as linguistics, social sciences, and computer science.

.. image:: docs/software-ecosystem.png
    :alt: Software ecosystem 
    :align: center
    :width: 65%

*Trafilatura*: An Italian word for `wire drawing <https://en.wikipedia.org/wiki/Wire_drawing>`_, symbolizing the extraction and refinement process in web scraping.

For more information on the software ecosystem and how Trafilatura integrates with other tools, visit our [Ecosystem Page](https://trafilatura.readthedocs.io/en/latest/ecosystem.html).

Known Uses and Case Studies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trafilatura has been employed in a variety of contexts and projects, demonstrating its versatility and effectiveness. Some of the known uses include:

- **Academic Research**: Utilized in numerous research projects for web corpus construction, linguistic analysis, and data-driven studies in social sciences.

- **Commercial Applications**: Employed in business analytics, market research, and SEO optimization, providing valuable insights from web data.

- **Open-Source Contributions**: An active part of the open-source community, with contributions and collaborations that enhance its features and usability.

Explore detailed case studies and user experiences on our [Used By page](https://trafilatura.readthedocs.io/en/latest/used-by.html).

Corresponding Blog Posts
~~~~~~~~~~~~~~~~~~~~~~~~

Stay updated with the latest developments, tutorials, and insights related to Trafilatura through our blog, `Bits of Language`. The blog covers a range of topics from technical how-tos, updates on new features, to discussions on web scraping challenges and solutions.

- [Bits of Language Blog](https://adrien.barbaresi.eu/blog/tag/trafilatura.html)

Citing Trafilatura
~~~~~~~~~~~~~~~~~~

If you use Trafilatura in your research or projects, we kindly ask you to cite our work. This helps us to continue developing and improving the tool. Here's how you can cite Trafilatura:

.. code-block:: bibtex

    @inproceedings{barbaresi-2021-trafilatura,
      title = {{Trafilatura: A Web Scraping Library and Command-Line Tool for Text Discovery and Extraction}},
      author = "Barbaresi, Adrien",
      booktitle = "Proceedings of the Joint Conference of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
      pages = "122--131",
      publisher = "Association for Computational Linguistics",
      year = 2021,
    }

Contact and Community
~~~~~~~~~~~~~~~~~~~~~

We believe in the power of community and collaboration. Whether you have questions, suggestions, or just want to discuss web scraping and data extraction, we're here for you:

- **Contact the Author**: Reach out to Adrien Barbaresi for inquiries, collaborations, or feedback. Visit his [contact page](https://adrien.barbaresi.eu/) for more information.

- **GitHub Community**: Engage with the Trafilatura community on GitHub. Share your experiences, contribute to discussions, and collaborate on new features.

- **Social Media**: Follow us on [Twitter](https://twitter.com/adbarbaresi) for the latest updates, tips, and community highlights.

- **Issue Tracker**: Encounter a bug or have a feature request? File it on our [GitHub Issues page](https://github.com/adbar/trafilatura/issues).

Contributing to Trafilatura
~~~~~~~~~~~~~~~~~~~~~~~~~~

Your contributions are what make Trafilatura a robust and versatile tool. We welcome contributions of all kinds, from code to documentation:

- **Code Contributions**: Enhance Trafilatura by contributing code. Whether it's bug fixes, new features, or performance improvements, your code makes a difference.

- **Documentation**: Help us improve our documentation. Write tutorials, guides, or translate existing content to make Trafilatura more accessible.

- **Feedback and Suggestions**: Share your feedback and suggestions. Your insights are valuable in shaping the future of Trafilatura.

- **Community Engagement**: Be part of our community. Participate in discussions, share your use cases, and help others get the most out of Trafilatura.

Visit our [Contributing Guide](https://github.com/adbar/trafilatura/blob/master/CONTRIBUTING.md) for more information on how you can contribute.

Acknowledgments
~~~~~~~~~~~~~~~

We extend our heartfelt thanks to all the contributors, users, and supporters of Trafilatura. Your contributions, feedback, and encouragement have been instrumental in the growth and success of this project.

- [List of Contributors](https://github.com/adbar/trafilatura/graphs/contributors)

License and Copyright
~~~~~~~~~~~~~~~~~~~~~

Trafilatura is licensed under the GNU General Public License v3.0, promoting freedom and collaboration in software development. This license ensures that Trafilatura remains open-source and community-driven.

- [GNU General Public License v3.0](https://github.com/adbar/trafilatura/blob/master/LICENSE)

For any inquiries regarding licensing or to discuss alternative licensing options, please [contact us](https://github.com/adbar/trafilatura#author).

Final Notes
~~~~~~~~~~~

Trafilatura is a dynamic project, continually evolving to meet the challenges of web data extraction and analysis. We're committed to maintaining its quality, reliability, and accessibility. Join us in this journey to unlock the full potential of web data.

For the latest updates, features, and resources, visit our [official website](https://trafilatura.readthedocs.io/) and [GitHub repository](https://github.com/adbar/trafilatura).

Thank you for choosing Trafilatura for your web scraping and data extraction needs!
