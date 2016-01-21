# -*- coding: utf8 -*-

import json
import pytest
from mock import patch, MagicMock
from flask_z3950 import view, blueprint


class TestBlueprint():


    def test_all_search_view_functions_registered(self, app):
        funcs = [getattr(view, f) for f in dir(view) if f.startswith('search')]
        registered = [r for r in app.url_map.iter_rules()]

        assert not set(funcs).issubset(set(registered))


    def test_humanize_int_filter_humanises_integer_string(self):
        mock_context = MagicMock()
        bp = blueprint.Z3950Blueprint()

        assert bp.humanize_int(mock_context, "1234567890") == "1,234,567,890"


class TestView():


    def test_code_for_known_error_status_returned(self):
        e = ValueError()
        code = view.error_status(e)

        assert code == 400


    def test_server_error_code_returned_for_unknown_error_status(self):
        class NonsenseError():
            pass

        e = NonsenseError()
        code = view.error_status(e)

        assert code == 500


    @patch('flask_z3950.view._handle_search_request')
    def test_correct_raw_data_included_with_successful_query(self, handle_req,
                                                             search_response,
                                                             app):
        handle_req.return_value = search_response
        res = view.search_raw('db')

        assert res.data == ''.join(search_response[1].record_data)


    @patch('flask_z3950.view._handle_search_request')
    def test_correct_json_data_included_with_successful_query(self, handle_req,
                                                              search_response,
                                                              app):
        handle_req.return_value = search_response
        res = view.search_json('db')
        resp_data = json.loads(res.data)['data']
        original_data = json.loads(search_response[1].to_json())['data']

        assert resp_data == original_data


    @patch('flask_z3950.view._handle_search_request')
    def test_correct_xml_data_included_with_successful_query(self, handle_req,
                                                             search_response,
                                                             app):
        handle_req.return_value = search_response
        res = view.search_marcxml('db')

        assert res.data == search_response[1].to_marcxml()


    @patch('flask_z3950.view._handle_search_request')
    def test_correct_html_data_included_with_successful_query(self, handle_req,
                                                              search_response,
                                                              app):
        handle_req.return_value = search_response
        res = view.search_html('db')

        assert search_response[1].to_html() in res.data


    def test_next_url_constructed_when_end_not_reached(self, app):
        with app.test_request_context():
            url = view._get_next_url('q', 1, 10, 100)

            assert url == 'http://localhost/?query=q&position=11&size=10'


    def test_next_url_not_constructed_when_end_reached(self, app):
        with app.test_request_context():
            url = view._get_next_url('q', 90, 10, 100)

            assert url is None


    def test_prev_url_constructed_when_not_at_beginning(self, app):
        with app.test_request_context():
            url = view._get_previous_url('q', 2, 10)

            assert url == 'http://localhost/?query=q&position=1&size=10'


    def test_prev_url_not_constructed_when_not_at_beginning(self, app):
        with app.test_request_context():
            url = view._get_previous_url('q', 1, 10)

            assert url is None


    def test_raw_search_returns_error_when_bad_query(self, client):
        with client as c:
            resp = client.get('/search/loc/raw?q')

        assert resp.status_code == 400


    def test_json_search_returns_error_when_bad_query(self, client):
        with client as c:
            resp = client.get('/search/loc/json?q')

        assert resp.status_code == 400


    def test_json_error_contains_message(self, client):
        with client as c:
            resp = client.get('/search/loc/json?q')
            print resp.data

        msg = 'The "query" parameter is missing'
        assert json.loads(resp.data)['message'] == msg


    def test_marcxml_search_returns_error_when_bad_query(self, client):
        with client as c:
            resp = client.get('/search/loc/marcxml?q')

        assert resp.status_code == 400


    def test_marcxml_error_contains_message(self, client):
        with client as c:
            resp = client.get('/search/loc/marcxml?q')

        msg = 'The &#34;query&#34; parameter is missing'
        assert '<error>{0}</error>'.format(msg) in resp.data


    def test_html_search_returns_error_when_bad_query(self, client):
        with client as c:
            resp = client.get('/search/loc/html?q')

        assert resp.status_code == 400


    def test_search_raises_error_when_query_missing(self):
        kwargs = {'query': '', 'size': 10, 'position': 1}
        with pytest.raises(ValueError) as excinfo:
            view._handle_search_request('loc', kwargs)

        msg = 'The "query" parameter is missing'
        assert str(excinfo.value) == msg


    def test_search_raises_error_when_size_is_less_then_one(self):
        kwargs = {'query': 'q', 'size': 0, 'position': 1}
        with pytest.raises(ValueError) as excinfo:
            view._handle_search_request('loc', kwargs)

        msg = 'The "size" parameter must be a positive integer'
        assert str(excinfo.value) == msg


    def test_search_raises_error_when_size_is_not_a_number(self):
        kwargs = {'query': 'q', 'size': 'not a number', 'position': 1}
        with pytest.raises(ValueError) as excinfo:
            view._handle_search_request('loc', kwargs)

        msg = 'The "size" parameter must be a valid integer'
        assert str(excinfo.value) == msg


    def test_search_raises_error_when_position_is_less_then_one(self):
        kwargs = {'query': 'q', 'size': 10, 'position': 0}
        with pytest.raises(ValueError) as excinfo:
            view._handle_search_request('loc', kwargs)

        msg = 'The "position" parameter must be a positive integer'
        assert str(excinfo.value) == msg


    def test_search_raises_error_when_position_is_not_a_number(self):
        kwargs = {'query': 'q', 'size': 10, 'position': 'not a number'}
        with pytest.raises(ValueError) as excinfo:
            view._handle_search_request('loc', kwargs)

        msg = 'The "position" parameter must be a valid integer'
        assert str(excinfo.value) == msg


    def test_search_raises_error_when_z3950manager_not_initialised(self, app):
        app.extensions = {}
        kwargs = {'query': 'q', 'size': 10, 'position': 1}
        with pytest.raises(RuntimeError) as excinfo:
            view._handle_search_request('loc', kwargs)

        msg = 'The Z3950Manager has not been initialised'
        assert str(excinfo.value) == msg


    def test_search_raises_error_when_db_not_found(self, client):
        with client as c:
            kwargs = {'query': 'q', 'size': 10, 'position': 1}
            with pytest.raises(ValueError) as excinfo:
                view._handle_search_request('nope', kwargs)

            msg = 'No database with that identifier could be found'
            assert str(excinfo.value) == msg


    def test_successful_search_response_contains_correct_data(self, app,
                                                              dataset):
        mock_db = MagicMock()
        mock_db.search.return_value = dataset
        mock_manager = MagicMock()
        mock_manager.databases = {'db': mock_db}
        app.extensions['z3950']['z3950_manager'] = mock_manager
        kwargs = {'query': 'q', 'size': 10, 'position': 1}
        resp = view._handle_search_request('db', kwargs)
        metadata = set(dataset.metadata.values())

        assert resp[0] is None
        assert resp[1] == dataset
        assert metadata.issubset(set(resp[2].values()))
