Flask-Z3950
***********

.. module:: flask_z3950


A `Flask`_ plugin for `Z3950`_ integration.


Installation
============

Flask-Z3950 is available on PyPi:

.. code-block:: console

    $ pip install Flask-Z3950


Quickstart
==========

Initialise a :class:`Z3950Manager` object and start performing searches with
your chosen :class:`Z3950Database`, like so:

.. code-block:: python

    from flask import Flask
    from flask_z3950 import Z3950Manager

    app = Flask(__name__)
    db_config = {"db": "Voyager", "host": "z3950.loc.gov", "port": 7090}
    app.config["Z3950_DATABASES"] = {"loc": db_config}

    z3950_manager = Z3950Manager(app)
    z3950_db = z3950_manager.databases['loc']
    records = z3850_db.search("ti=1066 and all that")

    print records.data

.. note::

   The default query syntax is `CCL`_, see :class:`Z3950Database` for all
   accepted syntaxes.


Configuration
=============

The following configration settings exist for Flask-Z3950:

=================================== ======================================
`Z3950_DATABASES`                   A dictionary containing Z39.50
                                    database configuration details, where
                                    keys are database identifiers and
                                    values a nested dictionaries
                                    containing configuration details for
                                    that database.

                                    Each nested dictionary is used to
                                    initialise a new
                                    :class:`Z3950Database`, so the
                                    dictionary keys should be named the
                                    same as the parameters used to
                                    initialise that class, taking note of
                                    any default values.
=================================== ======================================

Example
=======

An `example application`_ is provided to show how you might setup a Z39.50
gateway capable of returning records in multiple formats, you can try it out by
typing:

.. code-block:: console

    $ python example.py

To retrieve a MARCXML document containing the first ten records in the Library
of Congress database with the title "1066 and all that" enter the following
into your browser::

    http://0.0.0.0:5000/search/loc?q=(ti=1066%20and%20all%20that)&f=MARCXML

API
===

.. autoclass:: Z3950Manager
   :members:

.. autoclass:: Z3950Database
   :members:

.. autoclass:: Dataset
   :members:


Changelog
=========

.. include:: ../CHANGES

.. _Flask: http://flask.pocoo.org/
.. _Z3950: https://en.wikipedia.org/wiki/Z39.50
.. _CCL: http://www.indexdata.dk/yaz/doc/tools.tkl#CCL
.. _example application: https://github.com/alexandermendes/Flask-Z3950/blob/master/example.py
