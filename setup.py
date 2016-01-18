# -*- coding: utf8 -*-
"""
Flask-Z3950
-----------

A Flask plugin that provides Z39.50 integration.
"""

import os
from setuptools import setup

try:
    here = os.path.dirname(__file__)
    long_description = open(os.path.join(here, 'docs', 'long_desc.rst')).read()
except:
    long_description = ""

requirements = ["Flask>=0.10.1",
                "lxml>=3.5.0, <4.0",
                "ply>=3.8.0, <4.0",
                "pymarc>=3.0.4, <4.0",
                "PyZ3950",
                ]

dependency_links = ["git+https://github.com/asl2/PyZ3950.git#egg=PyZ3950"]

test_requirements = ["pytest-cov>=2.2.0, <3.0",
                     "pytest>=2.8.4, <3.0",
                     ]

setup(
    name="Flask-Z3950",
    version="0.1.2",
    author="Alexander Mendes",
    author_email="alexanderhmendes@gmail.com",
    description="A Flask plugin that provides Z39.50 integration.",
    license="BSD",
    url="https://github.com/alexandermendes/Flask-Z3950",
    packages=['flask_z3950'],
    long_description=long_description,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
    dependency_links=dependency_links,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: Z39.50",
    ],
    tests_require=test_requirements,
    test_suite="tests",
)
