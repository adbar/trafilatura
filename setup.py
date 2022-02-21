"""
Scrapes the main text of web pages while preserving some structure
https://github.com/adbar/trafilatura
"""

import re
from pathlib import Path
from setuptools import setup



def get_version(package):
    "Return package version as listed in `__version__` in `init.py`"
    # version = Path(package, '__init__.py').read_text() # Python >= 3.5
    with open(str(Path(package, '__init__.py')), 'r', encoding='utf-8') as filehandle:
        initfile = filehandle.read()
    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', initfile).group(1)


def get_long_description():
    "Return the README"
    with open('README.rst', 'r', encoding='utf-8') as filehandle:
        long_description = filehandle.read()
    #long_description += "\n\n"
    #with open("CHANGELOG.md", encoding="utf8") as f:
    #    long_description += f.read()
    return long_description


# some problems with installation solved this way
extras = {
    'all': [
        'cchardet >= 2.1.7',
        'htmldate[speed] >= 1.1.0',
        'py3langid >= 0.2.0',
        'pycurl >= 7.44.1',
        'urllib3[brotli]',
    ],
    'gui': [
        'Gooey >= 1.0.1',
    ],
}

setup(
    name='trafilatura',
    version=get_version('trafilatura'),
    description='Web scraping library and command-line tool for text discovery and retrieval. Downloads web pages, scrapes main text and comments while preserving some structure, and converts to TXT, CSV, JSON and XML',
    long_description=get_long_description(),
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Security',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: Markdown',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities',
    ],
    keywords=['corpus', 'html2text', 'news-crawler', 'natural-language-processing', 'scraper', 'tei-xml', 'text-extraction', 'webscraping', 'web-scraping'],
    url='https://trafilatura.readthedocs.io',
    project_urls={
        "Documentation": "https://trafilatura.readthedocs.io",
        "Source": "https://github.com/adbar/trafilatura",
        "Blog": "https://adrien.barbaresi.eu/blog/tag/trafilatura.html",
    },
    author='Adrien Barbaresi',
    author_email='barbaresi@bbaw.de',
    license='GPLv3+',
    packages=['trafilatura'],
    package_data={'trafilatura': ['data/tei-schema.pickle', 'settings.cfg']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'certifi',
        'charset_normalizer >= 2.0.12',
        'courlan >= 0.6.0',
        'htmldate >= 1.1.0',
        'justext >= 3.0.0',
        'lxml >= 4.6.4',
        'readability-lxml >= 0.8.1',
        'urllib3 >= 1.26, < 2',
    ],
    extras_require=extras,
    entry_points = {
        'console_scripts': [
            'trafilatura=trafilatura.cli:main',
            'trafilatura_gui=trafilatura.gui:main',
        ],
    },
    # platforms='any',
    tests_require=['pytest'],
    zip_safe=False,
)
