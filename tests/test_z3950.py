# -*- coding: utf8 -*-

import pytest
from PyZ3950.zoom import QuerySyntaxError
from flask_z3950.z3950 import Z3950Manager


class TestZ3950Manager():


    def test_z3950_manager_state_stored(self, app):
        z3950_manager = app.extensions['z3950']['z3950_manager']

        assert type(z3950_manager) == type(Z3950Manager())


    def test_multiple_databases_loaded(self, app):
        z3950_manager = app.extensions['z3950']['z3950_manager']
        db_names = z3950_manager.databases.keys()

        assert db_names == ['loc', 'copac']


class TestZ3950Database():


    def test_connection_configured_with_defaults(self, z3950_db):
        conn = z3950_db._connect()
        config = [conn.user, conn.password, conn.preferredRecordSyntax,
                  conn.elementSetName]
        expected = [None, None, 'USMARC', 'F']

        assert config == expected


    def test_searching_with_bad_syntax_raises_error(self, z3950_db):
        with pytest.raises(QuerySyntaxError):
            msg = z3950_db.search('ti=')

            assert msg == "The query could not be parsed."
