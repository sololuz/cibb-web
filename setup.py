# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import cibb
version = cibb.__version__

setup(
    name='cibb',
    version=version,
    author='Victor Aguilar - @jvacx',
    author_email='victor@jvacx.com',
    packages=[
        'cibb',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.3',
    ],
    zip_safe=False,
    scripts=['app/manage.py'],
)
