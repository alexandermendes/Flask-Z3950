# -*- coding: utf8 -*-

import json


class TestDataset():

    def test_all_records_transformed_to_marcxml(self, dataset):
        data_size = len(dataset.record_data)
        xml = dataset.to_marcxml()
        assert xml.count('<record>') == data_size

    def test_all_records_transformed_to_html(self, dataset):
        data_size = len(dataset.record_data)
        html = dataset.to_html()
        assert html.count('class="row z3950-record"') == data_size

    def test_all_records_transformed_to_json(self, dataset):
        original_size = len(dataset.record_data)
        transformed_size = len(json.loads(dataset.to_json()).get('data'))
        assert original_size == transformed_size

    def test_correct_str_returned_from_str_transformation(self, dataset):
        expected = ''.join(dataset.record_data)
        assert dataset.to_str() == expected

    def test_additional_kwargs_included_in_json(self, dataset):
        json_data = dataset.to_json(number=42)
        assert json.loads(json_data).get('number') == 42

    def test_dataset_metadata_included_in_json(self, dataset):
        base_keys = json.loads(dataset.to_json()).keys()
        assert set(dataset.metadata.keys()).issubset(set(base_keys))
