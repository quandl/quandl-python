try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode
    from urllib import urlopen

import re
import unittest
import httpretty
import json
import six
from quandl.model.datatable import Datatable
from mock import patch, call, mock_open
from quandl.connection import Connection
from test.factories.datatable import DatatableFactory
from quandl.api_config import ApiConfig
from quandl.errors.quandl_error import (InternalServerError, QuandlError)
from test.helpers.httpretty_extension import httpretty

class GetDatatableDatasetTest(unittest.TestCase):

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
        six.assertCountEqual(self,
                             metadata, [u'datatable_code', u'id', u'name', u'vendor_code'])


class BulkDownloadDataTableTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datatables/*'),
                               adding_headers={
                                   'Location': 'https://www.blah.com/download/db.zip'
                               },
                               body='{}', status=302)
        httpretty.register_uri(httpretty.GET,
                               re.compile('https://www.blah.com/'), body='{}')

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def setUp(self):
        datatable = {'datatable': DatatableFactory.build(
            vendor_code='ZACKS', datatable_code='FC')}
        self.datatable = Datatable(datatable['datatable']['datatable_code'], datatable['datatable'])
        ApiConfig.api_key = 'api_token'
        ApiConfig.api_version = '2015-04-09'

    def test_bulk_download_raises_exception_when_no_path(self):
        self.assertRaises(
            QuandlError, lambda: self.datatable.bulk_download_file(None))
