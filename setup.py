#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='sanuli-konuli',
    version='0.1',
    license='GPLv2',
    author='Jari Turkia',
    author_email='jatu@hqcodeshop.fi',
    description='Sanuli konuli',
    url='https://github.com/HQJaTu/sanuli-konuli',
    classifiers=[ # https://pypi.org/classifiers/
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        # License:
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        # Topic
        'Topic :: Games/Entertainment',
    ],
    python_requires='>=3.8, <4',

    install_requires=[
        'lxml==4.7.1',
    ],
    scripts=['cli-utils/find-matching-word.py',
             'cli-utils/get-initial-word.py',
             'cli-utils/kotus-5-letter-words.py'],
    packages=find_packages()
)
