import unittest2
from test.helpers.httpretty_extension import httpretty
from test.helpers.merged_datasets_helper import setupDatasetsTest
import pandas
import numpy
from mock import patch, call, Mock
from quandl.model.dataset import Dataset
from quandl.model.merged_dataset import MergedDataset
from quandl.get import get
from quandl.api_config import ApiConfig
from quandl.connection import Connection


class GetSingleDatasetTest(unittest2.TestCase):
    @classmethod
    def setUp(self):
        # ensure api key is not set
        ApiConfig.api_key = None
        setupDatasetsTest(self, httpretty)

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def test_returns_pandas_by_default(self):
        result = get('NSE/OIL')
        self.assertIsInstance(result, pandas.core.frame.DataFrame)

    def test_returns_pandas_when_requested(self):
        result = get('NSE/OIL', returns='pandas')
        self.assertIsInstance(result, pandas.core.frame.DataFrame)

    def test_returns_numpys_when_requested(self):
        result = get('NSE/OIL', returns='numpy')
        self.assertIsInstance(result, numpy.core.records.recarray)

    def test_setting_api_key_config(self):
        mock_connection = Mock(wraps=Connection)
        with patch('quandl.connection.Connection.execute_request',
                   new=mock_connection.execute_request) as mock:
            ApiConfig.api_key = 'api_key_configured'
            get('NSE/OIL')
            # extract the headers passed to execute_request
            actual_request_headers = mock.call_args[1]['headers']
            self.assertEqual(actual_request_headers['x-api-token'], 'api_key_configured')

    def test_sets_api_key_using_authtoken_arg(self):
        get('NSE/OIL', authtoken='api_key')
        self.assertEqual(ApiConfig.api_key, 'api_key')

    def test_sets_api_key_using_api_key_arg(self):
        get('NSE/OIL', api_key='api_key')
        self.assertEqual(ApiConfig.api_key, 'api_key')

    @patch.object(Dataset, 'data')
    def test_query_params_are_formed_with_old_arg_names(self, mock_method):
        get('NSE/OIL', authtoken='authtoken', trim_start='2001-01-01',
            trim_end='2010-01-01', collapse='annual',
            transformation='rdiff', rows=4, sort_order='desc')
        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(mock_method.mock_calls[0],
                         call(handle_column_not_found=True,
                              params={'start_date': '2001-01-01', 'end_date': '2010-01-01',
                                      'collapse': 'annual', 'transform': 'rdiff',
                                      'rows': 4, 'order': 'desc'}))

    @patch.object(Dataset, 'data')
    def test_query_params_are_formed_with_new_arg_names(self, mock_method):
        get('NSE/OIL', api_key='authtoken', start_date='2001-01-01',
            end_date='2010-01-01', collapse='annual',
            transform='rdiff', rows=4, order='desc')
        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(mock_method.mock_calls[0],
                         call(handle_column_not_found=True,
                              params={'start_date': '2001-01-01', 'end_date': '2010-01-01',
                                      'collapse': 'annual', 'transform': 'rdiff',
                                      'rows': 4, 'order': 'desc'}))

    @patch('quandl.model.data.Data.all')
    def test_code_is_parsed(self, mock):
        get('NSE/OIL')
        expected = call(
            params={'dataset_code': 'OIL', 'order': 'asc',
                    'database_code': 'NSE'})
        self.assertEqual(mock.call_args, expected)

    @patch.object(Dataset, 'data')
    def test_number_becomes_column_index(self, mock_method):
        get('NSE/OIL.1')
        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(mock_method.mock_calls[0],
                         call(handle_column_not_found=True, params={'column_index': 1}))

    @patch('quandl.model.data.Data.all')
    def test_code_and_column_is_parsed_and_used(self, mock):
        get('NSE/OIL.1')
        expected = call(
            params={'dataset_code': 'OIL', 'order': 'asc',
                    'database_code': 'NSE', 'column_index': 1})
        self.assertEqual(mock.call_args, expected)

    def test_raise_error_when_non_numeric_column_index(self):
        self.assertRaises(ValueError, lambda: get('NSE/OIL.notanumber'))


class GetMultipleDatasetsTest(unittest2.TestCase):
    @classmethod
    def setUp(self):
        # ensure api key is not set
        ApiConfig.api_key = None
        setupDatasetsTest(self, httpretty)

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.model.merged_dataset.MergedDataset._build_dataset_object')
    def test_multiple_datasets_args_formed(self, mock):
        # requested_column_indexes is a dynamically added attribute
        self.oil_obj.requested_column_indexes = []
        mock.return_value = self.oil_obj
        get(['WIKI/AAPL.1', 'WIKI/MSFT.2', 'NSE/OIL'])
        expected = [call(('WIKI/AAPL', {'column_index': [1]})),
                    call(('WIKI/MSFT', {'column_index': [2]})),
                    call('NSE/OIL')]
        self.assertEqual(mock.call_args_list, expected)

    @patch.object(MergedDataset, 'data')
    def test_query_params_are_formed_with_old_arg_names(self, mock_method):
        get(['WIKI/AAPL.1', 'WIKI/MSFT.2', 'NSE/OIL'],
            authtoken='authtoken', trim_start='2001-01-01',
            trim_end='2010-01-01', collapse='annual',
            transformation='rdiff', rows=4, sort_order='desc')

        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(mock_method.mock_calls[0],
                         call(handle_not_found_error=True, handle_column_not_found=True,
                              params={'start_date': '2001-01-01', 'end_date': '2010-01-01',
                                      'collapse': 'annual', 'transform': 'rdiff',
                                      'rows': 4, 'order': 'desc'}))

    @patch.object(MergedDataset, 'data')
    def test_query_params_are_formed_with_new_arg_names(self, mock_method):
        get(['WIKI/AAPL.1', 'WIKI/MSFT.2', 'NSE/OIL'],
            api_key='authtoken', start_date='2001-01-01',
            end_date='2010-01-01', collapse='annual',
            transform='rdiff', rows=4, order='desc')
        self.assertEqual(mock_method.call_count, 1)
        self.assertEqual(mock_method.mock_calls[0],
                         call(handle_not_found_error=True, handle_column_not_found=True,
                              params={'start_date': '2001-01-01', 'end_date': '2010-01-01',
                                      'collapse': 'annual', 'transform': 'rdiff',
                                      'rows': 4, 'order': 'desc'}))
