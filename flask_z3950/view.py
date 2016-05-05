# -*- coding: utf8 -*-
"""View module for Flask-Z3950."""

import json
from flask import Flask, request, abort, Response, render_template
from flask import current_app
from flask.ext.z3950 import ZoomError


def error_status(e):
    """Return the HTTP status code associated with an exception"""
    codes = {"ZoomError": 400,
             "ValueError": 400,
             "RuntimeError": 500,
             "UnicodeDecodeError": 500
             }
    name = e.__class__.__name__
    if name not in codes.keys():
        return 500

    return codes[name]


def search_marcxml(db):
    """Return the results of a Z39.50 database search as MARCXML.

    :param db: The identifier of the database to be searched.
    """
    def error_response(e):
        resp = render_template('error.xml', msg=str(e))
        return Response(resp, error_status(e), mimetype="application/xml")

    try:
        dataset = _handle_search_request(db, request.args)[1]
    except (ZoomError, ValueError, RuntimeError) as e:
        return error_response(e)

    try:
        resp = dataset.to_marcxml()
    except UnicodeDecodeError as e:
        return error_response(e)

    return Response(resp, 200, mimetype="application/xml")


def search_raw(db):
    """Return the results of a Z39.50 database search as raw data.

    :param db: The identifier of the database to be searched.
    """
    try:
        (msg, dataset, kwargs) = _handle_search_request(db, request.args)
    except (ZoomError, ValueError, RuntimeError) as e:
        abort(error_status(e))

    try:
        resp = dataset.to_str()
    except UnicodeDecodeError as e:  # pragma: no cover
        abort(error_status(e))

    return Response(resp, 200, mimetype="text/html")


def search_html(db):
    """Return the results of a Z39.50 database search as HTML.

    :param db: The identifier of the database to be searched.
    """
    try:
        (msg, dataset, kwargs) = _handle_search_request(db, request.args)
    except (ZoomError, ValueError, RuntimeError) as e:
        abort(error_status(e))

    try:
        data = dataset.to_html()
    except UnicodeDecodeError as e:  # pragma: no cover
        abort(error_status(e))

    resp = render_template('success.html', data=data, **kwargs)
    return Response(resp, 200, mimetype="text/html")


def search_json(db):
    """Return the results of a Z39.50 database search as JSON.

    :param db: The identifier of the database to be searched.
    """
    def error_response(e):
        code = error_status(e)
        resp = {'status': 'error', 'data': None, 'message': str(e)}
        json_resp = json.dumps(resp, indent=4, sort_keys=True)
        return Response(json_resp, code, mimetype="application/json")

    try:
        (msg, dataset, kwargs) = _handle_search_request(db, request.args)
    except (ZoomError, ValueError, RuntimeError) as e:
        return error_response(e)

    try:
        data = dataset.to_json()
    except UnicodeDecodeError as e:
        return error_response(e)

    data = json.loads(data)['data']
    resp = {'status': 'success', 'data': data, 'message': msg}
    resp.update(kwargs)
    json_resp = json.dumps(resp, indent=4, sort_keys=True)
    return Response(json_resp, 200, mimetype="application/json")


def _handle_search_request(db, kwargs):
    """Handle a search request and return the result.

    :returns: A tuple containing status code, message, data and any arbitrary
        keyword arguments.
    """
    query = kwargs.get('query')
    if not query:
        raise ValueError('The "query" parameter is missing')

    try:
        position = int(kwargs.get('position', 1))
    except ValueError:
        raise ValueError('The "position" parameter must be a valid integer')
    if position < 1:
        raise ValueError('The "position" parameter must be a positive integer')

    try:
        size = int(kwargs.get('size', 10))
    except ValueError:
        raise ValueError('The "size" parameter must be a valid integer')
    if size < 1:
        raise ValueError('The "size" parameter must be a positive integer')

    try:
        z3950_manager = current_app.extensions['z3950']['z3950_manager']
    except KeyError:  # pragma: no cover
        raise RuntimeError('The Z3950Manager has not been initialised')

    try:
        z3950_db = z3950_manager.databases[db]
    except KeyError:
        raise ValueError('No database with that identifier could be found')

    # Perform search
    dataset = z3950_db.search(query, position=position - 1, size=size)

    # Collate metadata
    created = dataset.metadata['created']
    total = dataset.metadata['total']
    n_records = dataset.metadata['n_records']
    next_url = _get_next_url(query, position, size, total)
    prev_url = _get_previous_url(query, position, size)
    metadata = {'message': None, 'next': next_url, 'previous': prev_url,
                'created': created, 'total': total, 'n_records': n_records,
                'size': size, 'position': position}

    return (None, dataset, metadata)


def _get_next_url(query, position, size, total):
    """Return the URL to retrieve the next chunk of results."""
    next_pos = position + size
    if next_pos >= total:
        return None
    url = '{0}?query={1}&position={2}&size={3}'
    return url.format(request.base_url, query, next_pos, size)


def _get_previous_url(query, position, size):
    """Return the URL to retrieve the previous chunk of results."""
    if position < 2:
        return None
    prev_pos = position - size if position - size > 0 else 1
    url = '{0}?query={1}&position={2}&size={3}'
    return url.format(request.base_url, query, prev_pos, size)
