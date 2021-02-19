"""
Scrapes the main text of web pages while preserving some structure
http://github.com/adbar/trafilatura
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
        'cchardet == 2.1.4; python_version == "3.4"',
        'cchardet >= 2.1.7; python_version > "3.4"',
        'htmldate[speed]',
        'pycld3 >= 0.20',
    ],
}

setup(
    name='trafilatura',
    version=get_version('trafilatura'),
    description='Web scraping library and command-line tool for text discovery and retrieval. Downloads web pages, scrapes main text and comments while preserving some structure, and converts to TXT, CSV, JSON and XML',
    long_description=get_long_description(),
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    keywords=['html2text', 'nlp', 'scraper', 'tei-xml', 'text-extraction', 'webscraping', 'web-scraping'],
    url='http://github.com/adbar/trafilatura',
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
    python_requires='>=3.4',
    install_requires=[
        'chardet == 3.0.4; python_version < "3.6"',
        'chardet >= 3.0.4; python_version >= "3.6"',
        'courlan >= 0.3.1',
        'htmldate >= 0.8.0',
        'justext >= 2.2.0',
        'lxml == 4.3.5; python_version == "3.4"',
        'lxml >= 4.6.2; python_version > "3.4"',
        'readability-lxml >= 0.8.1',
        'urllib3>=1.25,<2',
    ],
    extras_require=extras,
    entry_points = {
        'console_scripts': ['trafilatura=trafilatura.cli:main'],
    },
    # platforms='any',
    tests_require=['pytest', 'tox'],
    zip_safe=False,
)
