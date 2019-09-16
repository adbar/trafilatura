#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract the main text of web pages
http://github.com/adbar/trafilatura
"""

from codecs import open # python2
import os
from setuptools import setup # find_packages,

#try:
#    from setuptools import setup
#except ImportError:
#    from distutils.core import setup


here = os.path.abspath(os.path.dirname(__file__))
packages = ['trafilatura']

extras = {
    'all': [
        'cchardet',
        'langid',
    ]
}


def readme():
    with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as readmefile:
        return readmefile.read()

setup(
    name='trafilatura',
    version='0.0.4',
    description='Scrapes the main text of web pages while preserving some structure.',
    long_description=readme(),
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    keywords=['entity-extraction', 'html-extraction', 'html-parsing', 'text-mining', 'webarchives', 'web-scraping'],
    url='http://github.com/adbar/trafilatura',
    author='Adrien Barbaresi',
    author_email='barbaresi@bbaw.de',
    license='GPLv3+',
    packages=packages,
    include_package_data=True,
    install_requires=[
        'ftfy',
        'justext',
        'lru-dict',
        'lxml == 4.3.4', # CPython parser issue with version 4.3.1 # > 4.3.4 not compatible with Python 3.4 
        'requests >= 2.19.0',
    ],
    extras_require=extras,
    python_requires='>=3',
    entry_points = {
        'console_scripts': ['trafilatura=trafilatura.cli:main'],
    },
    # platforms='any',
    tests_require=['pytest', 'tox'],
    zip_safe=False,
)
