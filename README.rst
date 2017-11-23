Flask-Z3950
***********

|travis| |coveralls| |pypi| |doi|

`Z39.50`_ integration for Flask applications.

See the `Flask-Z3950 documentation`_
for full details of installation, configuration and usage.

Build setup
===========

.. code-block:: bash

    # install development packages
    $ sudo apt-get install libxml2-dev libxslt-dev python-dev lib32z1-dev

    # install Flask-Z3950
    pip install Flask-Z3950

    # test
    python setup.py test

.. _Flask: http://flask.pocoo.org/
.. _Z39.50: https://en.wikipedia.org/wiki/Z39.50
.. _Flask-Z3950 documentation: https://pythonhosted.org/Flask-Z3950/
.. _CONTRIBUTING: https://github.com/alexandermendes/Flask-Z3950/blob/master/CONTRIBUTING.md

.. |travis| image:: https://travis-ci.org/alexandermendes/Flask-Z3950.svg?branch=master
    :target: https://travis-ci.org/alexandermendes/Flask-Z3950
    :alt: Test success

.. |coveralls| image:: https://coveralls.io/repos/github/alexandermendes/Flask-Z3950/badge.svg?branch=master
    :target: https://coveralls.io/github/alexandermendes/Flask-Z3950?branch=master
    :alt: Test coverage

.. |pypi| image:: https://img.shields.io/pypi/v/Flask-Z3950.svg?label=latest%20version
    :target: https://pypi.python.org/pypi/Flask-Z3950
    :alt: Latest version released on PyPi

.. |doi| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.888145.svg
   :target: https://doi.org/10.5281/zenodo.888145
   :alt: DOI
