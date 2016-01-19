# -*- coding: utf8 -*-
"""Blueprint module for Flask-Z3950."""

from flask import Blueprint
from .view import search


class Z3950Blueprint(Blueprint):
    """Blueprint to support additional views.

    :param ``**kwargs``: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        """Initialise blueprint instance and add URL rules."""
        defaults = {'name': 'z3950', 'import_name': __name__,
                    'template_folder': 'templates'}
        defaults.update(kwargs)

        super(Z3950Blueprint, self).__init__(**defaults)

        self.add_url_rule('/search/<db>', view_func=search)
