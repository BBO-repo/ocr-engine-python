#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'ocrize'
DESCRIPTION = 'OCR for medical documents.'
URL = 'https://github.com/me/myproject'
EMAIL = 'info@sokle.ch'
AUTHOR = 'Sockle'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None
LICENSE = None
# Packages required for the module (automatically filled from requirements.txt) 
REQUIRED = None # [ 'requests', 'maya', 'records',] 

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    REQUIRED = f.read().splitlines()

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['ocr-engine-python'],

    entry_points={
        'console_scripts': ['ocrize=cli:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
)
