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

To set up a Z39.50 gateway you can do this:

.. code-block:: python

    from flask import Flask
    from flask.ext.z3950 import Z3950Manager

    app = Flask(__name__)
    db_config = {"db": "Voyager", "host": "z3950.loc.gov", "port": 7090}
    app.config["Z3950_DATABASES"] = {"loc": db_config}

    z3950_manager = Z3950Manager(app)
    z3950_manager.register_blueprint(url_prefix='/z3950')

You can now search multiple databases and retrieve records in a variety of
formats. For example, the following query will return all records in the
Library of Congress database with the title "1066 and all that", as JSON:

.. code-block::

    http://{your-base-url}/z3950/search/loc/json?query=(ti=1066 and all that)

.. note::

    See the :ref:`http-api` documentation for further details.

If you decide you don't want to make use of these pre-defined view functions,
just don't register the blueprint. You can still retrieve and perform searches
with your configured databases, like so:

.. code-block:: python

    z3950_db = z3950_manager.databases['loc']
    dataset = z3950_db.search('ti=1066 and all that')

    print dataset.to_str()


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
                                    :class:`Z3950Database`, so the nested
                                    dictionary keys should be named the
                                    same as the parameters used to
                                    initialise that class.
=================================== ======================================


Query Syntax
============

The default query syntax is CCL but a number of alternative syntaxes are
provided, each with different complexities. Documentation for the most
common of these syntaxes can be found below:

- `CCL`_: ISO 8777
- `CQL`_: The Common Query Language
- `PQF`_: Index Data's Prefix Query Format
- `C2`_: Cheshire II query syntax


Building a CCL query
====================

Many Z39.50 databases report their configurations in terms of attributes and
use values. So, while there are lots of valid ways to build a CCL query, below
is the style that I find the most effective.

The basic syntax for a query string is:

.. code-block:: python

    '(attribute, value)="item"'

Multiple attributes can be joined by using a comma:

.. code-block:: python

    '(attribute, value),(attribute, value)="item"'

Multiple fields can be searched by using logical operators:

.. code-block:: python

    '(attribute, value)="item"and(attribute, value)="item"'

Logical operators can also be used while searching within a particular field:

.. code-block:: python

    '(attribute, value)="item or another_item"'


Example
-------

Taking the British Library's `Z39.50 configuration`_ as an example, the
following query would print the result of searching the library's database for
the ISBN number 188012422X.

.. code-block:: python

    # Assumes z3950_db is a configured Z3950Database object
    query = '(1,7)="188012422X"'
    print z3950_db.search(query)

.. note::

   Implementations can very greatly, refer to the documentation for your
   chosen database for a list of accepted attributes.



Transforming MARC records
=========================

If raw MARC data is returned from a database search it can be transformed into
a variety of different formats, such as MARCXML, JSON and HTML. For more
details, see the API documentation for :class:`Dataset`.


API
===

Z39.50 Objects
----

.. module:: flask_z3950

.. autoclass:: Z3950Manager
   :members:

.. autoclass:: Z3950Database
   :members:

.. autoclass:: Dataset
   :members:


.. _http-api:


HTTP API
========

.. http:get:: /search/raw/(db)

    Query `db` and return the results.

   **Example request**:

   .. sourcecode:: http

      GET /search/loc?query HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      [
        {
          "post_id": 12345,
          "author_id": 123,
          "tags": ["server", "web"],
          "subject": "I tried Nginx"
        },
        {
          "post_id": 12346,
          "author_id": 123,
          "tags": ["html5", "standards", "web"],
          "subject": "We go to HTML 5"
        }
      ]

   :query sort: one of ``hit``, ``created-at``
   :query offset: offset number. default is 0
   :query limit: limit number. default is 30
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: optional OAuth token to authenticate
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request

   :statuscode 200: success
   :statuscode 400: bad request
   :statuscode 404: no records found
   :statuscode 500: server error


Changelog
=========

.. include:: ../CHANGES

.. _Flask: http://flask.pocoo.org/
.. _Z3950: https://en.wikipedia.org/wiki/Z39.50
.. _CCL: http://www.indexdata.dk/yaz/doc/tools.tkl#CCL
.. _CQL: http://www.loc.gov/standards/sru/cql/
.. _PQF: http://www.indexdata.dk/yaz/doc/tools.tkl#PQF
.. _C2: http://cheshire.berkeley.edu/cheshire2.html#zfind
.. _Z39.50 configuration: http://www.bl.uk/bibliographic/z3950configuration.html