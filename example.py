# -*- coding: utf8 -*-
"""Example of using Flask-Z3950 to set up a Z39.50 gateway."""

from flask import Flask
from flask.ext.z3950 import Z3950Manager
import settings_test as settings

# Setup Flask
app = Flask(__name__)
app.config.from_object(settings)

# Setup Flask-Z3950
z3950_manager = Z3950Manager(app)
z3950_manager.register_blueprint(url_prefix='/z3950')

if __name__ == '__main__':
    app.run(debug=True)
