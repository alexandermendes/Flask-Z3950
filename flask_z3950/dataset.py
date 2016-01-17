# -*- coding: utf8 -*-
"""Dataset module for Flask-Z3950."""

import json
import os
import pymarc
from lxml import etree


class Dataset(object):
    """Dataset class with functions for transforming raw record data.

    Args:
        record_data: A list of raw record data.
    """

    def __init__(self, record_data):
        self.record_data = record_data


    def to_str(self):
        """Return a string representation of all records in the the dataset.

        Returns
            str: The raw data.
        """
        return ''.join([r for r in self.record_data])


    def to_marcxml(self):
        """Return a MARCXML representation of any MARC records in the dataset.

        Returns:
            str: A well-formed MARCXML document as a string.
        """
        records = [pymarc.Record(data=r) for r in self.record_data]
        xmllist = [pymarc.record_to_xml(r) for r in records]
        xmlstr = "".join(xmllist)
        xmldoc = """<?xml version="1.0" encoding="utf-8"?>
                    <collection xmlns="http://www.loc.gov/MARC21/slim">
                        {0}
                    </collection>""".format(xmlstr)
        return self._transform(xmldoc, 'format-xml.xsl')


    def to_html(self):
        """Return an HTML representation of any MARC records in the dataset.

        Returns:
            str: A basic Bootstrap 3 representation of the records that can be
                modified further using CSS and JS on the client-side.
        """
        records = [pymarc.Record(data=r) for r in self.record_data]
        xmllist = [pymarc.record_to_xml(r) for r in records]
        xslt = 'marcxml-to-html.xsl'
        html_list = [self._transform(xml, xslt) for xml in xmllist]
        return "".join(html_list)


    def to_json(self, **kwargs):
        """Return a JSON representation of any MARC records in the dataset.

        Args:
            **kwargs: Arbitrary keyword arguments to add to the returned JSON.

        Returns:
            str: A JSON serialized representation of the dataset.
        """
        reclist = [pymarc.Record(data=r).as_dict() for r in self.record_data]
        recdict = {"records": reclist}
        recdict.update(kwargs)
        return json.dumps(recdict)



    def _transform(self, xml, xslt_fn):
        """Return the result of an XSLT transformation.

        Args:
            xml: The XML string to be transformed.
            xslt_fn: Name of the XSLT file to apply.

        Returns:
            The transformed XML as a string.
        """
        here = os.path.dirname(os.path.abspath(__file__))
        xslt_path = os.path.join(here, 'xsl', xslt_fn)
        xslt = etree.parse(xslt_path)
        doc = etree.fromstring(xml)
        transform = etree.XSLT(xslt)
        newdoc = transform(doc)
        return etree.tostring(newdoc, pretty_print=True)
