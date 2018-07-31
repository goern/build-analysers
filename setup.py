#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup


def get_version():
    with open(os.path.join('thoth_build_analysers', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]
    raise ValueError("No version identifier found")


setup(
    name='thoth-build-analysers',
    version=get_version(),
    author='Christoph Görn',
    author_email='goern@redhat.com',
    packages=['thoth_build_analysers', ],
    license='GPLv3+',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 2 - Pre - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
