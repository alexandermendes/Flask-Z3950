# -*- coding: utf8 -*-
"""Dataset module for Flask-Z3950."""

import json
import os
import pymarc
from lxml import etree


class Dataset(object):
    """Dataset class with functions for transforming raw record data.

    :param record_data: A list of raw record data.
    """

    def __init__(self, record_data):
        self.record_data = record_data


    def to_str(self):
        """Return a string representation of all raw record data."""
        return ''.join([r for r in self.record_data])


    def to_marcxml(self):
        """Return a MARCXML representation of any MARC records."""
        records = [pymarc.Record(data=r) for r in self.record_data]
        xmllist = [pymarc.record_to_xml(r) for r in records]
        xmlstr = "".join(xmllist)
        xmldoc = """<?xml version="1.0" encoding="utf-8"?>
                    <collection xmlns="http://www.loc.gov/MARC21/slim">
                        {0}
                    </collection>""".format(xmlstr)
        return self._transform(xmldoc, 'format-xml.xsl')


    def to_html(self):
        """Return an HTML representation of any MARC records."""
        records = [pymarc.Record(data=r) for r in self.record_data]
        xmllist = [pymarc.record_to_xml(r) for r in records]
        xslt = 'marcxml-to-html.xsl'
        html_list = [self._transform(xml, xslt) for xml in xmllist]
        return "".join(html_list)


    def to_json(self, **kwargs):
        """Return a JSON representation of any MARC records.

        :param ``**kwargs``: Arbitrary keyword arguments to add to the JSON.
        """
        reclist = [pymarc.Record(data=r).as_dict() for r in self.record_data]
        recdict = {"records": reclist}
        recdict.update(kwargs)
        return json.dumps(recdict)



    def _transform(self, xml, xslt_fn):
        """Return the result of an XSLT transformation."""
        here = os.path.dirname(os.path.abspath(__file__))
        xslt_path = os.path.join(here, 'xsl', xslt_fn)
        xslt = etree.parse(xslt_path)
        doc = etree.fromstring(xml)
        transform = etree.XSLT(xslt)
        newdoc = transform(doc)
        return etree.tostring(newdoc, pretty_print=True)
