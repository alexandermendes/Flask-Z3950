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
```

|   Key         | Value                                                             |
|:-------------:|-------------------------------------------------------------------|
| name          | An identifier for the database                                    |
| host          | The host.                                                         |
| db            | The database.                                                     |
| port          | The port.                                                         |
| user          | The username (default None)                                       |
| password      | The password (default None)                                       |
| syntax        | USMARC, SUTRS, XML, SGML, GRS-1, OPAC or EXPLAIN (default USMARC) |
| elem_set_name | Element set name, usually B for brief or F for full (default F)   |

Note that the `user`, `password`, `syntax` and `elem_set_name` keys are optional.

Multiple databases can be configured by adding additional dictionaries, for an
example of such a configuration see [settings_test.py](settings_test.py).


## Usage

To initialise the the plugin and start performing Z39.50 searches:

```Python
z3950_manager = Z3950Manager(app)
z3950_db = z3950_manager.databases['loc']
records = z3950_db.search("ti=1066 and all that")
```

For all types of record the raw data can be retrieved:

```Python
print records.data
```

For MARC records, additional transformations are provided, to MARCXML, HTML and
JSON, for example:

```Python
print records.to_html()
```

The HTML is a basic Bootstrap 3 template that you can modify further in your
CSS and JS. For example, you could use the select button like this:

```JavaScript
$(document).delegate('.btn-marc', 'click', function (e) {
    alert("Record " + $(this).attr('data-control-num') + " selected!")
}
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
