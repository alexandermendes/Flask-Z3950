# -*- coding: utf8 -*-
"""Example of using Flask-Z3950 to set up a Z39.50 gateway."""

from flask import Flask, request, abort, Response
from flask.ext.z3950 import Z3950Manager, ZoomError
import settings_test as settings

# Setup Flask
app = Flask(__name__)
app.config.from_object(settings)

# Setup Flask-Z3950
z3950_manager = Z3950Manager(app)


@app.route('/search/<db>')
def search(db):
    """Return the results of a Z39.50 database search."""
    query = request.args.get('q')
    if not query:
        abort(400)

    # Optional parameters
    size = request.args.get('s', 10)
    position = request.args.get('p', 1)
    return_format = request.args.get('f')

    # Get the requested database
    z3950_db = z3950_manager.databases[db]

    try:
        # Perform the search
        records = z3950_db.search(query, position=position, size=size)
    except ZoomError as e:
        return Response(e, 400)

    # Return records in the requested format
    mimetype = "text/html"
    if not return_format:
        data = records.to_str()
    elif return_format.upper() == 'HTML':
        data = records.to_marchtml()
    elif return_format.upper() == 'MARCXML':
        mimetype = "application/xml"
        data = records.to_marcxml()
    elif return_format.upper() == 'JSON':
        mimetype = "application/json"
        data = records.to_json(status_code=200)
    else:
        return Response("Unknown format requested", 400)

    return Response(data, 200, mimetype=mimetype)


if __name__ == '__main__':
    app.run(debug=True)
