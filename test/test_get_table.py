import re
import unittest
import httpretty
import json
from quandl.model.datatable import Datatable
import pandas
from mock import patch, call
from test.factories.datatable import DatatableFactory
from test.factories.datatable_data import DatatableDataFactory
from test.factories.datatable_meta import DatatableMetaFactory
import quandl
from quandl.utils.request_type_util import RequestType


class GetDataTableTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        datatable = {'datatable': DatatableFactory.build(
            vendor_code='ZACKS', datatable_code='FC')}
        data = DatatableDataFactory.build()
        datatable['datatable'].update(data)
        meta = {'meta': DatatableMetaFactory.build()}
        datatable.update(meta)
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/datatables*'),
                               body=json.dumps(datatable))
        cls.datatable_instance = Datatable(datatable['datatable'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def tearDown(self):
        RequestType.USE_GET_REQUEST = True

    @patch('quandl.connection.Connection.request')
    def test_datatable_returns_datatable_object(self, mock):
        df = quandl.get_table('ZACKS/FC', params={})
        self.assertIsInstance(df, pandas.core.frame.DataFrame)

    @patch('quandl.connection.Connection.request')
    def test_datatable_with_code_returns_datatable_object(self, mock):
        df = quandl.get_table('AR/MWCF', code="ICEP_WAC_Z2017_S")
        self.assertIsInstance(df, pandas.core.frame.DataFrame)

    @patch('quandl.connection.Connection.request')
    def test_get_table_calls_connection_with_no_params_for_get_request(self, mock):
        quandl.get_table('ZACKS/FC')
        expected = call('get', 'datatables/ZACKS/FC', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_get_table_calls_connection_with_no_params_for_post_request(self, mock):
        RequestType.USE_GET_REQUEST = False

        quandl.get_table('ZACKS/FC')
        expected = call('post', 'datatables/ZACKS/FC', json={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_get_table_calls_connection_with_params_for_get_request(self, mock):
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

        quandl.get_table('ZACKS/FC', **params)
        expected = call('get', 'datatables/ZACKS/FC', params=expected_params)
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_get_table_calls_connection_with_params_for_post_request(self, mock):
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

        quandl.get_table('ZACKS/FC', **params)
        expected = call('post', 'datatables/ZACKS/FC', json=expected_params)
        self.assertEqual(mock.call_args, expected)
