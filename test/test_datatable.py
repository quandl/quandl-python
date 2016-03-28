import re
import unittest2
import httpretty
import json
from quandl.model.datatable import Datatable
from mock import patch, call
from test.factories.datatable import DatatableFactory


class GetDatatableDatasetTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        datatable = {'datatable': DatatableFactory.build(
            vendor_code='ZACKS', datatable_code='FC')}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datatables/*'),
                               body=json.dumps(datatable))
        cls.datatable_instance = Datatable(datatable['datatable'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.connection.Connection.request')
    def test_datatable_meatadata_calls_connection(self, mock):
        Datatable('ZACKS/FC').data_fields()
        expected = call('get', 'datatables/ZACKS/FC/metadata', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_datatable_data_calls_connection(self, mock):
        Datatable('ZACKS/FC').data()
        expected = call('get', 'datatables/ZACKS/FC', params={})
        self.assertEqual(mock.call_args, expected)

    def test_datatable_returns_datatable_object(self):
        datatable = Datatable('ZACKS/FC')
        self.assertIsInstance(datatable, Datatable)
        self.assertEqual(datatable.vendor_code, 'ZACKS')
        self.assertEqual(datatable.datatable_code, 'FC')

    def test_dataset_column_names_match_expected(self):
        metadata = Datatable('ZACKS/FC').data_fields()
        self.assertItemsEqual(
            metadata, [u'datatable_code', u'id', u'name', u'vendor_code'])
