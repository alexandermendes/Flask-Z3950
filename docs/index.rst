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

Performing a database search via Z39.50 can be done like this:

.. code-block:: python

    from flask import Flask
    from flask.ext.z3950 import Z3950Manager

    app = Flask(__name__)
    db_config = {"db": "Voyager", "host": "z3950.loc.gov", "port": 7090}
    app.config["Z3950_DATABASES"] = {"loc": db_config}
    z3950_manager = Z3950Manager(app)

    z3950_db = z3950_manager.databases['loc']
    records = z3850_db.search("ti=1066 and all that")

    print records.data

The example above begins with a new Flask application being created and the
configuration details for the Library of Congress database specified. These
details are passed to an instance of :class:`Z3950Manager` and used to create a
new :class:`Z3950Database` object. This database object can then be
retrieved using the assigned identifier ('loc'). A search is performed that
will retrieve the first ten records in the Library of Congress database with
the title "1066 and all that" and the results are printed.


Configuration
=============

The following configuration settings exist for Flask-Z3950:

=================================== ======================================
`Z3950_DATABASES`                   A dictionary containing Z39.50
                                    database configuration details, where
                                    keys are database identifiers and
                                    values are nested dictionaries
                                    containing configuration details for
                                    that database.

                                    Each nested dictionary is used to
                                    initialise a new
                                    :class:`Z3950Database`, so the
                                    dictionary keys should be named the
                                    same as the parameters used to
                                    initialise that class.
=================================== ======================================


Query Syntax
============

The default query syntax is CCL but a number of alternative syntaxes are
provided, each with different complexities. The documentation for the most
common of these syntaxes can be found below:

- `CCL`_: ISO 8777
- `CQL`_: The Common Query Language
- `PQF`_: Index Data's Prefix Query Format
- `C2`_: Cheshire II query syntax


Transforming MARC records
=========================

Any raw MARC data returned from a database search can be transformed into a
variety of different formats, such as MARCXML, JSON and HTML. For more details,
see the API documentation for :class:`Dataset`.


Z39.50 Gateway
==============

Below is an example of setting up a Z39.50 gateway to return the results of a
database search as MARCXML:

.. code-block:: python

    @app.route('/search/<db>')
    def search(db):
        """Return Z39.50 search results as MARCXML."""
        z3950_db = z3950_manager.databases[db]
        query = request.args.get('query')
        records = z3950_db.search(query)
        xml = records.to_marcxml()

        return Response(xml, 200, mimetype="application/xml")

For additional search options see the API documentation for :class:`Z3950Database`.


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
.. _CQL: http://www.loc.gov/standards/sru/cql/
.. _PQF: http://www.indexdata.dk/yaz/doc/tools.tkl#PQF
.. _C2: http://cheshire.berkeley.edu/cheshire2.html#zfind