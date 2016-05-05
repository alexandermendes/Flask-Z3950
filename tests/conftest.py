# -*- coding: utf8 -*-

import os
import pytest
from flask import Flask
from flask_z3950.z3950 import Z3950Manager, Z3950Database
from flask_z3950.dataset import Dataset
import settings_test as settings


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.from_object(settings)
    z3950_manager = Z3950Manager(app)
    z3950_manager.register_blueprint()

    return app


@pytest.fixture
def z3950_db():
    config = getattr(settings, 'Z3950_DATABASES').values()[0]
    return Z3950Database(**config)


@pytest.fixture
def dataset():
    here = os.path.abspath(os.path.dirname(__file__))
    dataset_file = os.path.join(here, 'dataset.dat')
    with open(dataset_file, 'rb') as f:
        return Dataset([f.read()], total=1)


@pytest.fixture
def bad_unicode_dataset():
    here = os.path.abspath(os.path.dirname(__file__))
    dataset_file = os.path.join(here, 'bad_unicode_dataset.dat')
    with open(dataset_file, 'rb') as f:
        return Dataset([f.read()], total=1)


@pytest.fixture
def search_response(dataset):
    kwargs = {'message': None, 'next': 'example.com',
              'previous': 'example.com',
              'created': dataset.metadata['created'],
              'total': dataset.metadata['total'],
              'n_records': dataset.metadata['n_records'],
              'size': 10,
              'position': 1}
    return (None, dataset, kwargs)


@pytest.fixture
def bad_response(bad_unicode_dataset):
    return (None, bad_unicode_dataset, {})


@pytest.fixture
def client(app):
    return app.test_client()
