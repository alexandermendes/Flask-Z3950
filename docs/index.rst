Flask-Z3950
***********

.. module:: flask_z3950


A `Flask`_ plugin for `Z3950`_ integration.


Installation
------------

Flask-Z3950 is available on PyPi:

.. code-block:: console

    $ pip install Flask-Z3950


Quickstart
----------

Initialise a :class:`Z3950Manager` object and start performing searches with
your chosen Z39.50 database, like so:

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

   The default query syntax is `CCL`_, for a list of alternative syntaxes
   see the class :class:`Z3950Database`.


Configuration
-------------

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
                                    same as the __init__ parameters for
                                    that class, taking note of any
                                    optional and default values.
=================================== ======================================


API
---

.. module:: flask_z3950

.. autoclass:: Z3950Manager
   :members:

.. autoclass:: Dataset
   :members:

Changelog
---------

.. include:: ../CHANGES

.. _Flask: http://flask.pocoo.org/
.. _Z3950: https://en.wikipedia.org/wiki/Z39.50
.. _CCL: http://www.indexdata.dk/yaz/doc/tools.tkl#CCL
