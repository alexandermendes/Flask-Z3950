# -*- coding: utf8 -*-
"""Example of using Flask-Z3950 to set up a Z39.50 gateway."""

import json
from flask import Flask, request, abort, Response, render_template
from flask import current_app
from flask.ext.z3950 import ZoomError


def search(db):
    """Return the results of a Z39.50 database search.

    :param db: The identifier of the database to be searched.
    """
    fmt = request.args.get('format', '').upper()

    def response(code, msg=None, data=None, **kwargs):
        if fmt == 'MARCXML':
            return _marcxml_response(code, msg=msg, data=data, **kwargs)
        elif fmt == 'HTML':
            return _html_response(code, msg=msg, data=data, **kwargs)
        elif fmt == 'JSON':
            return _json_response(code, msg=msg, data=data, **kwargs)
        elif str(code)[0] in ['4', '5']:
            abort(code)

        return Response(data, code, mimetype="text/html")

    # Validate parameters
    query = request.args.get('query')
    if not query:
        return response(400, msg='A query is required')

    try:
        position = int(request.args.get('position', 1))
    except ValueError:
        return response(400, msg='Position must be a valid integer')

    if position < 1:
        return response(400, msg='Position must be greater than zero')

    try:
        size = int(request.args.get('size', 10))
    except ValueError:
        return response(400, msg='Size must be a valid integer')

    if size < 1:
        return response(400, msg='Size must be greater than zero')

    # Retrieve database
    z3950_manager = current_app.extensions['z3950']
    try:
        z3950_db = z3950_manager.databases[db]
    except KeyError:
        return response(400, msg='Database not found')

    # Perform search
    try:
        records = z3950_db.search(query, position=position, size=size)
    except ZoomError as e:
        return response(400, msg=e)

    # Transform records
    if fmt == 'MARCXML':
        data = records.to_marcxml()
    elif fmt == 'HTML':
        data = records.to_html()
    elif fmt == 'JSON':
        data = records.to_json()
    else:
        return Response(records.to_str(), 200, mimetype="text/html")

    # Collate response data
    total = records.metadata['total']
    created = records.metadata['created']
    n_records = records.metadata['n_records']
    next_url = _get_next_url(query, size, position, fmt, total)
    prev_url = _get_previous_url(query, size, position, fmt)
    resp = {'data': data, 'message': None, 'next': next_url,
            'previous': prev_url, 'created': created, 'total': total,
            'n_records': n_records, 'step_size': size, 'position': position}

    # Respond
    return response(200, **resp)


def _json_response(code, msg=None, data=None, **kwargs):
    """Return a JSON response."""
    resp = {'data': data, 'message': msg}

    if str(code)[0] in ['4', '5']:
        resp.update({'status': 'error'})
    else:
        resp.update({'status': 'success'})
        resp.update(kwargs)

    return Response(json.dumps(resp), code, mimetype="application/json")


def _marcxml_response(code, msg=None, data=None, **kwargs):
    """Return an XML response."""
    if str(code)[0] in ['4', '5']:
        xml = render_template('error.xml', msg=msg)
    else:
        xml = data
    return Response(xml, code, mimetype="application/xml")


def _html_response(code, msg=None, data=None, **kwargs):
    """Return an HTML response."""
    if str(code)[0] in ['4', '5']:
        abort(code)
    html = render_template('success.html', data=data, **kwargs)
    return Response(html, code, mimetype="text/html")


def _get_next_url(query, size, position, fmt, total):
    """Return the URL to retrieve the next chunk of results."""
    next_pos = position + size
    if next_pos >= total:
        return None

    url = '{0}?query={1}&position={2}&size={3}&format={4}'
    return url.format(request.base_url, query, next_pos, size, fmt)


def _get_previous_url(query, size, position, fmt):
    """Return the URL to retrieve the previous chunk of results."""
    if position < 2:
        return None

    prev_pos = position - size if position - size > 0 else 1
    url = '{0}?query={1}&position={2}&size={3}&format={4}'
    return url.format(request.base_url, query, prev_pos, size, fmt)
