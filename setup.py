#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import surcharge

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name=surcharge.__name__,
    version=surcharge.__version__,
    packages=find_packages(),
    author=surcharge.__author__,
    author_email="julien@thebault.co",
    description="Surcharge is a tool for benchmarking your web server",
    long_description=open('README.rst').read(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    url='https://github.com/Lujeni/Surcharge',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
    ],
    entry_points={
        'console_scripts': [
            'surcharge = surcharge.cli:main',
        ],
    },
)
