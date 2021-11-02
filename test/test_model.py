import unittest
from nasdaqdatalink.model.model_base import ModelBase

import six


class ModelTest(unittest.TestCase):

    def setUp(self):
        self.model = ModelBase('foo', {'foo': 'bar', 'here': 1})

    def test_data_fields_returns_list_of_attribute_keys(self):
        data_fields = self.model.data_fields()
        six.assertCountEqual(self, data_fields, ['foo', 'here'])

    def test_data_can_be_accessed_as_dict(self):
        self.assertEqual(self.model['foo'], 'bar')
        self.assertEqual(self.model['here'], 1)

    def test_data_can_be_accessed_by_attribute_name(self):
        self.assertEqual(self.model.foo, 'bar')
        self.assertEqual(self.model.here, 1)

    def test_throws_exception_when_attribute_does_not_exist(self):
        self.assertRaises(AttributeError, lambda: self.model.blah)

    def test_to_list_returns_values(self):
        results = self.model.to_list()
        six.assertCountEqual(self, results, ['bar', 1])
