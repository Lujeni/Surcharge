#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import surcharge

setup(
    name=surcharge.__name__,
    version=surcharge.__version__,
    packages=find_packages(),
    author=surcharge.__author__,
    author_email="julien@thebault.co",
    description="Surcharge is a tool for benchmarking your web serve",
    long_description=open('README.md').read(),
    install_requires=['requests', 'gevent'],
    include_package_data=True,
    url='https://github.com/Lujeni/Surcharge',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: French",
        "Operating System :: Unix",
        "Topic :: System :: Networking",
    ],
    entry_points={
        'console_scripts': [
            'surcharge = surcharge.surcharge:main',
        ],
    },
)
