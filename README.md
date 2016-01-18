# Flask-Z3950

[![Build Status](https://travis-ci.org/alexandermendes/Flask-Z3950.svg?branch=master)]
(https://travis-ci.org/alexandermendes/Flask-Z3950)
[![Coverage Status](https://coveralls.io/repos/alexandermendes/Flask-Z3950/badge.svg)]
(https://coveralls.io/github/alexandermendes/Flask-Z3950?branch=master)
[![Code Health](https://landscape.io/github/alexandermendes/Flask-Z3950/master/landscape.svg)]
(https://landscape.io/github/alexandermendes/Flask-Z3950/master)

A [Flask](http://flask.pocoo.org/) plugin for [Z39.50](https://en.wikipedia.org/wiki/Z39.50) integration.


## Installation

Flask-Z3950 is available on PyPi:

```
$ pip install Flask-Z3950
```

## Configuration

Z39.50 connection details can be specified by adding the following variable to
your Flask configuration file:

```
Z3950_DATABASES = {'name': {'host': '', 'db': '', 'port': '', 'user': '', 'password': '', 'syntax': ''}}

Multiple databases can be configured by adding additional dictionaries, for an
example of such a configuration see [settings_test.py](settings_test.py).


## Usage

To initialise the the plugin and start performing Z39.50 searches:

```Python
from flask import Flask
from flask_z3950 import Z3950Manager

app = Flask(__name__)
db_config = {"db": "Voyager", "host": "z3950.loc.gov", "port": 7090}
app.config["Z3950_DATABASES"] = {"loc": db_config}

z3950_manager = Z3950Manager(app)
z3950_db = z3950_manager.databases['loc']
records = z3850_db.search("ti=1066 and all that")

print records.data
```

## Testing

Just run the following command:

```
$ python setup.py test
```

## Example

The [example.py](example.py) application shows how you might setup a Z39.50
gateway that can return records in multiple formats, you can try it out by
typing:

```
$ python example.py
```

To retrieve the MARCXML data for the first ten records in the Library of
Congress database with the title "1066 and all that" enter the following
into your browser:

```
http://0.0.0.0:5000/search/loc?q=(ti=1066%20and%20all%20that)&f=MARCXML
```

## Documentation

See the [Flask-Z3950 documentation](Flask-Z3950 documentation: https://pythonhosted.org/Flask-Z3950/)
for further details.
