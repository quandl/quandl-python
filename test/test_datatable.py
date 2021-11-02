import json
import re
import unittest

import httpretty
import six
from mock import call, mock_open, patch
from six.moves.urllib.parse import urlparse

from nasdaqdatalink.api_config import ApiConfig
from nasdaqdatalink.errors.data_link_error import (InternalServerError, DataLinkError)
from nasdaqdatalink.model.datatable import Datatable
from test.factories.datatable import DatatableFactory
from test.test_retries import ModifyRetrySettingsTestCase
from nasdaqdatalink.utils.request_type_util import RequestType
from parameterized import parameterized


class GetDatatableDatasetTest(ModifyRetrySettingsTestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        datatable = {'datatable': DatatableFactory.build(
            vendor_code='ZACKS', datatable_code='FC')}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/datatables/*'),
                               body=json.dumps(datatable))
        cls.datatable_instance = Datatable(datatable['datatable'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def tearDown(self):
        RequestType.USE_GET_REQUEST = True

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_datatable_metadata_calls_connection(self, mock):
        Datatable('ZACKS/FC').data_fields()
        expected = call('get', 'datatables/ZACKS/FC/metadata', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_datatable_data_calls_connection_with_no_params_for_get_request(self, mock):
        Datatable('ZACKS/FC').data()
        expected = call('get', 'datatables/ZACKS/FC', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_datatable_data_calls_connection_with_no_params_for_post_request(self, mock):
        RequestType.USE_GET_REQUEST = False
        Datatable('ZACKS/FC').data()
        expected = call('post', 'datatables/ZACKS/FC', json={})
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_datatable_calls_connection_with_params_for_get_request(self, mock):
        params = {'ticker': ['AAPL', 'MSFT'],
                  'per_end_date': {'gte': '2015-01-01'},
                  'qopts': {'columns': ['ticker', 'per_end_date']},
                  'foo': 'bar',
                  'baz': 4
                  }

        expected_params = {'ticker[]': ['AAPL', 'MSFT'],
                           'per_end_date.gte': '2015-01-01',
                           'qopts.columns[]': ['ticker', 'per_end_date'],
                           'foo': 'bar',
                           'baz': 4
                           }

        Datatable('ZACKS/FC').data(params=params)
        expected = call('get', 'datatables/ZACKS/FC', params=expected_params)
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_datatable_calls_connection_with_params_for_post_request(self, mock):
        RequestType.USE_GET_REQUEST = False
        params = {'ticker': ['AAPL', 'MSFT'],
                  'per_end_date': {'gte': '2015-01-01'},
                  'qopts': {'columns': ['ticker', 'per_end_date']},
                  'foo': 'bar',
                  'baz': 4
                  }

        expected_params = {'ticker': ['AAPL', 'MSFT'],
                           'per_end_date.gte': '2015-01-01',
                           'qopts.columns': ['ticker', 'per_end_date'],
                           'foo': 'bar',
                           'baz': 4
                           }

        Datatable('ZACKS/FC').data(params=params)
        expected = call('post', 'datatables/ZACKS/FC', json=expected_params)
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
                                   'https://data.nasdaq.com/api/v3/datatables/*'),
                               body=json.dumps(datatable))

        httpretty.register_uri(httpretty.POST,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/datatables/*'),
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

    def tearDown(self):
        RequestType.USE_GET_REQUEST = True

    def test_download_get_file_info(self):
        url = self.datatable._download_request_path()
        parsed_url = urlparse(url)
        self.assertEqual(parsed_url.path, 'datatables/AUSBS/D.json')

    @parameterized.expand(['GET', 'POST'])
    def test_download_generated_file(self, request_method):
        m = mock_open()

        httpretty.register_uri(getattr(httpretty, request_method),
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/datatables/*'),
                               body=json.dumps({
                                   'datatable_bulk_download': {
                                       'file': {
                                           'status': 'fresh',
                                           'link': 'https://www.blah.com/download/db.zip'
                                       }
                                   }
                               }),
                               status=200)

        with patch('nasdaqdatalink.model.datatable.urlopen', m, create=True):
            self.datatable.download_file('.', params={})

        self.assertEqual(m.call_count, 1)

    @parameterized.expand(['GET', 'POST'])
    def test_bulk_download_raises_exception_when_no_path(self, request_method):
        if request_method == 'POST':
            RequestType.USE_GET_REQUEST = False
        self.assertRaises(
            DataLinkError, lambda: self.datatable.download_file(None, params={}))

    @parameterized.expand(['GET', 'POST'])
    def test_bulk_download_table_raises_exception_when_error_response(self, request_method):
        print("request_method: ", request_method)
        if request_method == 'POST':
            RequestType.USE_GET_REQUEST = False
        httpretty.reset()
        ApiConfig.number_of_retries = 2
        error_responses = [httpretty.Response(
            body=json.dumps(
              {'error': {'code': 'QEMx01', 'message': 'something went wrong'}}
            ),
            status=500)]

        httpretty.register_uri(getattr(httpretty, request_method),
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/datatables/*'),
                               responses=error_responses)

        self.assertRaises(
            InternalServerError, lambda: self.datatable.download_file('.', params={}))
