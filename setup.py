"""
Scrapes the main text of web pages while preserving some structure
http://github.com/adbar/trafilatura
"""

# workaround for open() with encoding=''
from codecs import open

from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# some problems with installation solved this way
extras = {
    'all': [
        'cchardet == 2.1.4; python_version == "3.4"',
        'cchardet >= 2.1.6; python_version > "3.4"',
        'pycld3 >= 0.20',
    ],
}


def readme():
    with open(path.join(here, 'README.rst'), 'r', 'utf-8') as readmefile:
        return readmefile.read()


setup(
    name='trafilatura',
    version='0.5.2',
    description='Downloads web pages, scrapes main text and comments while preserving some structure, and converts to TXT, CSV, JSON and XML',
    long_description=readme(),
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
        "Coverage": "https://codecov.io/github/adbar/trafilatura",
        "Tracker": "https://github.com/adbar/trafilatura/issues",
    },
    author='Adrien Barbaresi',
    author_email='barbaresi@bbaw.de',
    license='GPLv3+',
    packages=['trafilatura'],
    package_data={'trafilatura': ['data/tei-schema.pickle']},
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=[
        'courlan >= 0.2.3',
        'htmldate >= 0.7.2',
        'justext >= 2.2.0',
        'lxml == 4.3.5; python_version == "3.4"',
        'lxml >= 4.5.2; python_version > "3.4"',
        'requests == 2.21.0; python_version == "3.4"',
        'requests >= 2.21.0; python_version > "3.4"',
        'readability-lxml >= 0.8.1',
    ],
    extras_require=extras,
    entry_points = {
        'console_scripts': ['trafilatura=trafilatura.cli:main'],
    },
    # platforms='any',
    tests_require=['pytest', 'tox'],
    zip_safe=False,
)
