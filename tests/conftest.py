# -*- coding: utf8 -*-

import os
import pytest
from flask import Flask
from flask_z3950.z3950 import Z3950Manager, Z3950Database
from flask_z3950.dataset import Dataset
import settings_test as settings
import dataset_test

@pytest.fixture(scope='session')
def app():
    app = Flask(__name__)
    app.config.from_object(settings)

    return app


@pytest.fixture
def z3950_manager(app):
    return Z3950Manager(app)


@pytest.fixture
def z3950_db():
    config = getattr(settings, 'Z3950_DATABASES').values()[0]
    return Z3950Database(**config)


@pytest.fixture
def dataset():
    records = getattr(dataset_test, 'DATASET')
    return Dataset(records)
