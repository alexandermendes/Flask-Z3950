# Flask-Z3950

A Flask plugin for Z39.50 integration.


## Configuration

Z39.50 connection details can be specified by adding the following variable to
your Flask configuration file:

```
Z3950_DATABASES = {'name': {'host': '', 'db': '', 'port': '', 'user': '',
                            'password': '', 'syntax': ''}}
```

The `user`, `password` and `syntax` keys are optional.

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


Multiple databases can be configured by adding additional dictionaries, for an
example of this see [settings_test.py](settings_test.py).


## Usage

Initialising the plugin and performing Z39.50 searches can be as simple as:

```
z3950_manager = Z3950Manager(flask_app)
z3950_db = z3950_manager.databases['loc']
records = z3950_db.search("ti=1066 and all that")
```

For all record types the raw data can be retrieved, for MARC records, additional
transformations can be provided, to MARCXML, HTML and JSON:

```
print records.data
print records.to_marcxml()
print records.to_html()
print records.to_json()
```


## Example

The [example.py](example.py) application shows how you might setup a Z39.50
gateway. To run the example application type:

```
$ python example.py
```

To retrieve raw data for the first ten records from the Library of Congress
database with the title "1066 and all that" enter the following URL into
your browser:

```
http://0.0.0.0:5000/search/loc?q=(ti=1066%20and%20all%20that)
```
