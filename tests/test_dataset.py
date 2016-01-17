# -*- coding: utf8 -*-


class TestDataset():


    def test_all_records_transformed_to_marcxml(self, dataset):
        data_size = len(dataset.record_data)
        xml = dataset.to_marcxml()

        assert xml.count('<record>') == data_size


    def test_string_transformation(self, dataset):
        expected = ''.join(dataset.record_data)

        assert dataset.to_str() == expected