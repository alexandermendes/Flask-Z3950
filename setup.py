# -*- coding: utf8 -*-
"""
Flask-Z3950
-----------

A Flask plugin that provides Z39.50 integration.
"""

import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except:
    readme = ""

requirements=[
    "Flask>=0.10.1",
    "ply>=3.8.0, <4.0",
    "pymarc>=3.0.4, <4.0",
    "PyZ3950",
    ]

dependency_links=[
    # The version on PyPi seems to have issues with ply
    "git+https://github.com/asl2/PyZ3950.git#egg=PyZ3950"
    ]

tests_require = [
    "pytest-cov>=2.2.0, <3.0",
    "pytest>=2.8.4, <3.0",
]

setup(
    name="Flask-Z3950",
    version="0.0.1",
    author="Alexander Mendes",
    author_email="alexanderhmendes@gmail.com",
    description="A Flask plugin that provides Z39.50 integration.",
    license="BSD",
    url="https://github.com/alexandermendes/Flask-Z3950",
    packages=['flask_z3950'],
    long_description=readme,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
    dependency_links=dependency_links,
    classifiers=[
        "Development Status :: 4 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python 2.6",
        "Programming Language :: Python 2.7",
        "Programming Language :: Python 3.3",
        "Programming Language :: Python 3.4",
        "Programming Language :: Python 3.5",
        "Topic :: Internet :: Z39.50",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
