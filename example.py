# -*- coding: utf8 -*-
"""Example of using Flask-Z3950 to set up a Z39.50 gateway."""

from flask import Flask, request, abort
from flask_z3950 import Z3950Manager, Z3950Error
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

    size = request.args.get('s', 10)
    position = request.args.get('p', 1)
    return_format = request.args.get('f')

    z3950_db = z3950_manager.databases[db]
    records = z3950_db.search(query, position=position, size=size)

    if not return_format:
        return records.to_str()
    elif return_format.upper() == 'MARCXML':
        return records.to_marcxml()
    elif return_format.upper() == 'HTML':
        return records.to_marchtml()


if __name__ == '__main__':
    app.run(debug=True)
