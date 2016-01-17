# -*- coding: utf8 -*-
"""Z39.50 module to query databases via the Z39.50 protocol."""

import pymarc
import os
import time
from PyZ3950 import zoom

__author__ = 'Alexander Mendes'
__license__ = 'BSD License'
__version__ = '0.0.1'


class Z3950Error(Exception):
    """Error class to handle any errors raised from this module."""
    pass


class Z3950Manager(object):
    """Z39.50 manager class to configure and handle Z39.50 databases.

    Args:
        app: The Flask application.

    Attributes:
        databases: A dictionary of all configured Z3950 databases.
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)


    def init_app(self, app):
        """Configure the extension.

        Args:
            app: The Flask application.
        """
        db_config = app.config.get('Z3950_DATABASES', {})

        self.databases = {}
        for name, config in db_config.items():
            db = Z3950Database(**config)
            self.databases[name] = db


class Z3950Database(object):
    """Z39.50 database class to query a Z39.50 database.

    Args:
        db: The name of the database.
        host: The host.
        port: The port.
        user: The username (the default is None).
        password: The password (the default is None).
        syntax: Supported values are USMARC, SUTRS, XML, GRS-1, EXPLAIN, and
            OPAC (the default is USMARC).
        elem_set_name: Element set name, usually B for brief or F for full (the
            default is F).
    """

    def __init__(self, db, host, port, user=None, password=None,
                 syntax='USMARC', elem_set_name='F'):
        self.db = db
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.syntax = syntax
        self.elem_set_name = elem_set_name


    def _connect(self, position, size):
        """Return a database connection

        Args:
            position (int): The position of the first record to retrieve.
            max_records (int): The maximum number of records to retrieve.
            record_syntax (str): Supported values are USMARC, SUTRS, XML, SGML,
                GRS-1, OPAC and EXPLAIN.
        """
        conn = zoom.Connection(self.host, self.port, user=self.user,
                               password=self.password, maximumRecordSize=size)
        conn.databaseName = self.db
        conn.responsePosition = position
        conn.preferredRecordSyntax = self.syntax
        conn.elementSetName = self.elem_set_name

        return conn


    def search(self, query, position=1, size=10, syntax='CCL'):
        """Return the results of a database query.

        Args:
            query: The database query.
            position: The position of the first record (the default is 1).
            size: The maximum number of records to return (the default is 10).
            syntax: The syntax of the query, either CCL, S-CCL, CQL, S-CQL,
                PQF, C2, ZSQL or CQL-TREE (the default is CCL).
        Returns:
            list: A list of the raw data for each record.
        """
        conn = self._connect(position, size)
        try:
            q = zoom.Query(syntax, query)
        except (zoom.ZoomError, RuntimeError) as e:
            raise Z3950Error(e)

        rs = conn.search(q)

        return [r.data for r in rs]