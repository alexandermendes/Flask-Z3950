# -*- coding: utf8 -*-
"""
Flask-Z3950
-----------

Z39.50 integration for Flask applications.
"""

import re
import os
from setuptools import setup


version = re.search('^__version__\s*=\s*"(.*)"',
                    open('flask_z3950/__init__.py').read(),
                    re.M).group(1)


try:
    here = os.path.dirname(__file__)
    long_description = open(os.path.join(here, 'docs', 'readme.rst')).read()
except:
    long_description = ""


requirements = ["Flask>=0.7.0",
                "lxml>=3.5.0, <4.0",
                "ply>=3.8.0, <4.0",
                "pymarc>=3.0.4, <4.0",
                "mollyZ3950==2.04-molly1",  # PyZ3950 on pypi is broken
                ]

setup_requirements = ["pytest-runner>=2.7.1, <3.0"]

test_requirements = ["mock",
                     "pytest>=2.8.0, <3.0",
                     "pytest-cov>=2.2.0, <3.0",
                     ]


setup(
    name="Flask-Z3950",
    version=version,
    author="Alexander Mendes",
    author_email="alexanderhmendes@gmail.com",
    description="Z39.50 integration for Flask applications.",
    license="BSD",
    url="https://github.com/alexandermendes/Flask-Z3950",
    packages=['flask_z3950'],
    long_description=long_description,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    test_suite="tests",
)
