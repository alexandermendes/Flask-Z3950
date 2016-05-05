# -*- coding: utf8 -*-
"""Z39.50 module for Flask-Z3950."""

from PyZ3950 import zoom
from .dataset import Dataset


class Z3950Manager(object):
    """Z39.50 manager class to configure and handle Z39.50 databases.

    :param app: The Flask application.

    :ivar databases: All configured Z3950 databases.
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Configure the extension.

        :param app: The Flask application.
        """
        db_config = app.config.get('Z3950_DATABASES', {})

        self.databases = {}
        for name, config in db_config.items():
            db = Z3950Database(**config)
            self.databases[name] = db

        app.extensions['z3950'] = {'z3950_manager': self}

    def register_blueprint(self, *args, **kwargs):
        """Register blueprint.

        :param ``*args``: Variable length argument list.
        :param ``**kwargs``: Arbitrary keyword arguments.
        """
        from .blueprint import Z3950Blueprint
        blueprint = Z3950Blueprint()
        self.app.register_blueprint(blueprint, *args, **kwargs)


class Z3950Database(object):
    """Z39.50 database class to query a Z39.50 database.

    :param db: The database.
    :param host: The host.
    :param port: The port.
    :param user: The username.
    :param password: The password.
    :param syntax: Prefered record syntax, either USMARC, SUTRS, XML, GRS-1,
        EXPLAIN, or OPAC.
    :param elem_set_name: Element set name, usually B for brief or F for full.
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

    def _connect(self):
        """Return a connection to the configured database.

        :returns: A connection.
        """
        conn = zoom.Connection(self.host, self.port, user=self.user,
                               password=self.password)
        conn.databaseName = self.db
        conn.preferredRecordSyntax = self.syntax
        conn.elementSetName = self.elem_set_name

        return conn

    def search(self, query, position=0, size=10, syntax='CCL'):
        """Return the results of a database query.

        :param query: The database query.
        :param position: The position of the first record (zero-based index).
        :param size: The maximum number of records to return.
        :param syntax: The syntax of the query, either CCL, S-CCL, CQL, S-CQL,
            PQF, C2, ZSQL or CQL-TREE.

        :returns: A :class:`Dataset` object containing the raw record data.
        """
        conn = self._connect()
        try:
            q = zoom.Query(syntax, query)
        except (zoom.QuerySyntaxError) as e:  # pragma: no cover
            raise zoom.QuerySyntaxError("The query could not be parsed.")

        start = int(position)
        end = start + int(size)
        rs = conn.search(q)

        return Dataset([r.data for r in rs[start:end]], total=len(rs))
