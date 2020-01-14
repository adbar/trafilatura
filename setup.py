"""
Seamlessly extract the metadata of web pages based on header or body.
http://github.com/adbar/kontext
"""

# workaround for open() with encoding=''
from codecs import open

from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))
packages = ['kontext']


# some problems with installation solved this way
#extras = {
#    'all': [
#        'regex >= 2019.08.19',
#        ],
#}


def readme():
    with open(path.join(here, 'README.rst'), 'r', 'utf-8') as readmefile:
        return readmefile.read()

setup(
    name='kontext',
    version='0.0.0',
    description='',
    long_description=readme(),
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    keywords=['html-extraction', 'html-parsing', 'metadata-extraction',  'webarchives', 'web-scraping'],
    url='http://github.com/adbar/kontext',
    author='Adrien Barbaresi',
    author_email='barbaresi@bbaw.de',
    license='GPLv3+',
    packages=packages,
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'htmldate >= 0.6.0',
        'lxml >= 4.4.2',
        'requests >= 2.22.0',
    ],
    extras_require=extras,
    entry_points = {
        'console_scripts': ['kontext=kontext.cli:main'],
    },
    # platforms='any',
    tests_require=['pytest'],
    zip_safe=False,
)
