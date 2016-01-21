Flask-Z3950
***********

.. module:: flask_z3950

`Z3950`_ integration for Flask applications.


Installation
============

Install the required development packages:

.. code-block:: console

    $ sudo apt-get install libxml2-dev libxslt-dev python-dev lib32z1-dev


Now, install Flask-Z3950:

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

.. code-block:: http

    http://{your-base-url}/z3950/search/loc/json?query=(ti=1066 and all that)

.. note::

    See the :ref:`http-api` documentation for further details.

If you decide you don't want to make use of the pre-defined view functions,
simply don't register the blueprint. You can still retrieve and perform searches
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

   Implementations can vary greatly so refer to the documentation for your
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

Search
------

The following query parameters apply to all search functions:

    - **query:** The Z39.50 database query.
    - **position:** Position of the first record (default is 1).
    - **size:** Maximum number of records (default is 10).

The following status codes could be returned from all search functions:

    - `200`_: OK
    - `400`_: Bad Request
    - `500`_: Server Error

.. http:get:: /search/(db)/raw

    Query `db` and return the results as raw data.

    **Example request**:

    .. sourcecode:: http

        GET /search/loc/raw?query=(ti="cheese%20shop") HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/html

        01488cam 22003733a 450000100090000000500170000900800410002690600450
        0067925006400112955003700176010001700213042001400230035002400244040
        0032002680200025003000200022003250350021003470500029003681000018003
        9724500440041525000400045926000440049930000270054349000310057049000
        2600601500004200627500003200669500006100701520019500762650002700...
        aAames, Avery. 14 aThe long quiche goodbye /cAvery Aames.
        aBerkley Prime Crime mass-market ed. aNew York : bBerkley Prime ...


.. http:get:: /search/(db)/json

    Query `db` and return the results as JSON.

    **Example request**:

    .. sourcecode:: http

        GET /search/loc/json?query=(ti="cheese%20shop") HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "created": 1453334119.273325,
            "data": [
                {
                    "fields": [
                        {
                            "001": "18392793"
                        },
                        ...
                        {
                            "245": {
                                "ind1": "1",
                                "ind2": "0",
                                "subfields": [
                                    {
                                        "a": "Days of wine and roquefort /"
                                    },
                                    {
                                        "c": "Avery Aames."
                                    }
                                ]
                            }
                        },
                        ...
                    ]
                    "leader": "02373cam  22004453i 4500"
                },
                ...
            ],
            "message": null,
            "n_records": 10,
            "next": ".../search/loc/json?query=ok&position=11&size=10",
            "position": 1,
            "previous": null,
            "size": 10,
            "status": "success",
            "total": 10000
        }

.. http:get:: /search/(db)/html

    Query `db` and return the results as HTML.

    **Example request**:

    .. sourcecode:: http

        GET /search/loc/html?query=(ti="cheese%20shop") HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/html

        <div class="z3950-records">
          <div class="row z3950-record">
            <div class="col-xs-8" id="18187332">
              <p>
                <span class="title"> To brie or not to brie / </span>
                <br/>
                <span class="author"> Aames, Avery.     </span>
                <br/>
                <small>
                  <span class="publisher"> Berkley Prime Crime,   </span>
                  <span class="pubyear">2013.  </span>
                  <br/>
                  <span class="physdesc">x, 325 p. ; </span>
                  <br/>
                </small>
              </p>
            </div>
            <div class="col-xs-4">
              <a href="#" data-control-num="18187332"
              class="btn btn-success btn-z3950 pull-right">Select</a>
            </div>
          </div>
          ...
        </div>


.. http:get:: /search/(db)/marcxml

    Query `db` and return the results as MARCXML.

    **Example request**:

    .. sourcecode:: http

        GET /search/loc/marcxml?query=(ti="cheese%20shop") HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/xml

        <collection xmlns="http://www.loc.gov/MARC21/slim">
          <record>
            <leader>01200cam 2200349 a 4500</leader>
            <controlfield tag="001">17349144</controlfield>
            ...
            <datafield ind1="1" ind2="0" tag="245">
              <subfield code="a">Clobbered by Camembert /</subfield>
              <subfield code="c">Avery Aames.</subfield>
            </datafield>
            ...
          </record>
          ...
        </collection>

Errors
------

.. http:get:: /search/(db)/json

    Query `db` and return the results as JSON.

    **Example request**:

    .. sourcecode:: http

        GET /search/loc/json?query= HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 400 BAD REQUEST
        Content-Type: application/json

        {
            "data": null,
            "message": "The \"query\" parameter is missing",
            "status": "error"
        }

.. http:get:: /search/(db)/marcxml

    Query `db` and return the results as MARCXML.

    **Example request**:

    .. sourcecode:: http

        GET /search/loc/marcxml?query= HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 400 BAD REQUEST
        Content-Type: application/xml

        <?xml version="1.0" encoding="utf-8"?>
        <errors>
          <error>The "query" parameter is missing</error>
        </errors>


.. note::

    If an error occurs while sending a request to the HTML or RAW data
    endpoints the request is aborted with a 400 or 500 status code
    (depending on the cause of the error).

Changelog
=========

.. include:: ../CHANGES

.. _Flask: http://flask.pocoo.org/
.. _Z3950: https://en.wikipedia.org/wiki/Z39.50
.. _Z39.50 configuration: http://www.bl.uk/bibliographic/z3950configuration.html

.. _CCL: http://www.indexdata.dk/yaz/doc/tools.tkl#CCL
.. _CQL: http://www.loc.gov/standards/sru/cql/
.. _PQF: http://www.indexdata.dk/yaz/doc/tools.tkl#PQF
.. _C2: http://cheshire.berkeley.edu/cheshire2.html#zfind

.. _200: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1
.. _400: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.1
.. _500: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.1
