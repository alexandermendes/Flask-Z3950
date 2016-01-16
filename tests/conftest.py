# -*- coding: utf8 -*-

import pytest
from flask import Flask
from flask_z3950 import Z3950

import settings_test


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object(settings_test)

    Z3950(app)
    return app
