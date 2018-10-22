try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import re
import unittest
import httpretty
import json
import six
from quandl.model.datatable import Datatable
from mock import patch, call, mock_open
from test.factories.datatable import DatatableFactory
from test.test_retries import ModifyRetrySettingsTestCase
from quandl.api_config import ApiConfig
from quandl.errors.quandl_error import (InternalServerError, QuandlError)


class GetDatatableDatasetTest(ModifyRetrySettingsTestCase):

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


class ExportDataTableTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        datatable = {'datatable': DatatableFactory.build(
            vendor_code='AUSBS', datatable_code='D')}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datatables/*'),
                               body=json.dumps(datatable))
        cls.datatable_instance = Datatable(datatable['datatable'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def setUp(self):
        datatable = {'datatable': DatatableFactory.build(
            vendor_code='AUSBS', datatable_code='D')}
        self.datatable = Datatable(datatable['datatable']['vendor_code'] + '/' +
                                   datatable['datatable']['datatable_code'], datatable['datatable'])
        ApiConfig.api_key = 'api_token'
        ApiConfig.api_version = '2015-04-09'

    def test_download_get_file_info(self):
        url = self.datatable._download_request_path()
        parsed_url = urlparse(url)
        self.assertEqual(parsed_url.path, 'datatables/AUSBS/D.json')

    def test_download_generated_file(self):
        m = mock_open()

        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datatables/*'),
                               body=json.dumps({
                                   'datatable_bulk_download': {
                                       'file': {
                                           'status': 'fresh',
                                           'link': 'https://www.blah.com/download/db.zip'
                                       }
                                   }
                               }),
                               status=200)

        with patch('quandl.model.datatable.urlopen', m, create=True):
            self.datatable.download_file('.')

        self.assertEqual(m.call_count, 1)

    def test_bulk_download_raises_exception_when_no_path(self):
            self.assertRaises(
                QuandlError, lambda: self.datatable.download_file(None))

    def test_bulk_download_table_raises_exception_when_error_response(self):
        httpretty.reset()
        ApiConfig.number_of_retries = 2
        error_responses = [httpretty.Response(
            body=json.dumps({'quandl_error': {'code': 'QEMx01',
                                              'message': 'something went wrong'}}),
            status=500)]

        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datatables/*'),
                               responses=error_responses)

        self.assertRaises(
            InternalServerError, lambda: self.datatable.download_file('.'))
