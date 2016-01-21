# -*- coding: utf8 -*-

import pytest
from mock import patch, MagicMock
from PyZ3950.zoom import QuerySyntaxError
from flask_z3950.z3950 import Z3950Manager

mock_zoom = MagicMock()
mock_conn = MagicMock()
mock_zoom.Connection.return_value = mock_conn


class TestZ3950Manager():


    def test_extension_state_stored(self, app):
        z3950_manager = app.extensions['z3950']['z3950_manager']

        assert isinstance(z3950_manager, Z3950Manager)


    def test_multiple_databases_loaded(self, app):
        z3950_manager = app.extensions['z3950']['z3950_manager']
        db_names = z3950_manager.databases.keys()

        assert db_names == ['loc', 'copac']


class TestZ3950Database():

    def create_mocked_result_set(self, n):
        rs = []
        for i in range(n):
            mock_record = MagicMock()
            mock_record.data = 'data{}'.format(i)
            rs.append(mock_record)
        mock_conn.search.return_value = rs


    @patch('flask_z3950.z3950.zoom', new=mock_zoom)
    def test_connection_initialised_correctly(self, z3950_db):
        conn = z3950_db._connect()
        expected = ['Voyager', 'USMARC', 'F']
        returned = [mock_conn.databaseName, mock_conn.preferredRecordSyntax,
                    mock_conn.elementSetName ]

        assert expected == returned


    @patch('flask_z3950.z3950.zoom', new=mock_zoom)
    def test_successful_search_returns_dataset(self, z3950_db):
        self.create_mocked_result_set(2)
        ds = z3950_db.search('au=dead parrot')

        assert ds.record_data == ['data0', 'data1']


    @patch('flask_z3950.z3950.zoom', new=mock_zoom)
    def test_search_does_not_return_too_few_results(self, z3950_db):
        self.create_mocked_result_set(5)
        ds = z3950_db.search('au=dead parrot')

        assert len(ds.record_data) == 5


    @patch('flask_z3950.z3950.zoom', new=mock_zoom)
    def test_search_does_not_return_too_many_results(self, z3950_db):
        self.create_mocked_result_set(20)
        ds = z3950_db.search('au=dead parrot', size=15)

        assert len(ds.record_data) == 15
