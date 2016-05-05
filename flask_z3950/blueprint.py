# -*- coding: utf8 -*-
"""Blueprint module for Flask-Z3950."""

import re
import jinja2
from flask import Blueprint
from . import view


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

        url_map = self._url_map()

        for url, view_func in url_map.iteritems():
            self.add_url_rule(url, view_func=view_func)

        self.add_app_template_filter(self.humanize_int)

    def _url_map(self):
        """Return a dict of URLs and view functions."""
        return {'/search/<db>/marcxml': view.search_marcxml,
                '/search/<db>/html': view.search_html,
                '/search/<db>/json': view.search_json,
                '/search/<db>/raw': view.search_raw}

    @jinja2.contextfilter
    def humanize_int(self, context, n):
        """Add commas to a string of digits and return."""
        return re.sub(r'(\d)(?=(\d\d\d)+(?!\d))', r'\1,', str(n))
