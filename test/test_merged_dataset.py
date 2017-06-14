import unittest2
from test.helpers.httpretty_extension import httpretty
import six
import datetime
import pandas
from quandl.model.dataset import Dataset
from quandl.model.data import Data
from quandl.model.merged_data_list import MergedDataList
from quandl.model.merged_dataset import MergedDataset
from mock import patch, call
from quandl.errors.quandl_error import ColumnNotFound
from test.helpers.merged_datasets_helper import setupDatasetsTest


class GetMergedDatasetTest(unittest2.TestCase):

    @classmethod
    def setUp(self):
        setupDatasetsTest(self, httpretty)

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.model.merged_dataset.MergedDataset._build_dataset_object')
    def test_merged_dataset_calls_merged_dataset_get_dataset(self, mock):
        mock.return_value = self.oil_obj
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        md.data_fields()

        expected_calls = [
            call(('NSE/OIL', {'column_index': [1, 2]})),
            call(('WIKI/AAPL', {'column_index': [1]})),
            call('WIKI/MSFT')
        ]
        self.assertEqual(mock.call_count, 3)
        for index, expected in enumerate(expected_calls):
            self.assertEqual(mock.mock_calls[index], expected)

    @patch('quandl.model.merged_dataset.MergedDataset._build_dataset_object')
    def test_removes_column_index_query_param(self, mock):
        self.oil_obj.requested_column_indexes = []
        mock.return_value = self.oil_obj
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]})], params={'column_index': 1})
        md.data_fields()
        expected = call(('NSE/OIL', {'column_index': [1, 2]}), params={})
        self.assertEqual(mock.call_args, expected)

    def test_sets_dataset_codes_for_the_datasets(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        self.assertEqual(md._datasets, None)
        self.assertItemsEqual([1, 2], md.dataset_codes[0][1]['column_index'])
        self.assertItemsEqual([1], md.dataset_codes[1][1]['column_index'])
        self.assertEqual('I', md.dataset_codes[2][1])

    def test_sets_column_index_on_each_dataset(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        md.data_fields()
        self.assertItemsEqual([1, 2], md._datasets[0].requested_column_indexes)
        self.assertItemsEqual([1], md._datasets[1].requested_column_indexes)
        self.assertItemsEqual([], md._datasets[2].requested_column_indexes)

    def test_merged_dataset_column_names(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        expected = [six.u('Date'), six.u('NSE/OIL - column.1'),
                    six.u('NSE/OIL - column.2'),
                    six.u('WIKI/AAPL - column.1'),
                    six.u('WIKI/MSFT - column.1'),
                    six.u('WIKI/MSFT - column.2'),
                    six.u('WIKI/MSFT - column.3')]
        self.assertItemsEqual(md.column_names, expected)

    def test_merged_dataset_oldest_available_date(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        self.assertEqual(md.oldest_available_date, datetime.date(2013, 1, 1))

    def test_merged_dataset_newest_available_date(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        self.assertEqual(md.newest_available_date, datetime.date(2015, 7, 30))

    def test_merged_dataset_database_codes(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        self.assertItemsEqual(md.database_code, ['NSE', 'WIKI'])

    def test_merged_dataset_dataset_codes(self):
        md = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')])
        self.assertItemsEqual(
            md.dataset_code, ['OIL', 'AAPL', 'MSFT'])

    def test_get_returns_merged_dataset_obj(self):
        md = MergedDataset(['NSE/OIL'])
        self.assertIsInstance(md, MergedDataset)

    def test_raise_error_when_datasets_arg_not_list(self):
        self.assertRaises(ValueError, lambda: MergedDataset('NSE/OIL').data_fields())

    def test_raise_error_when_datasets_arg_list_has_invalid_type(self):
        self.assertRaises(
            ValueError, lambda: MergedDataset(['NSE/OIL', {'blah': [1]}]).data_fields())

    def test_raise_error_when_column_index_specified_and_not_list(self):
        self.assertRaises(ValueError, lambda: MergedDataset(
            [('NSE/OIL', {'column_index': 'foo'})]).data_fields())

    def test_raise_error_when_column_index_greater_than_max(self):
        self.assertRaises(
            ColumnNotFound, lambda: MergedDataset([('NSE/OIL', {'column_index': [1, 10]})]).data())

    def test_raise_error_when_column_index_less_than_one(self):
        self.assertRaises(
            ColumnNotFound, lambda: MergedDataset([('NSE/OIL', {'column_index': [0, 1]})]).data())

    @patch.object(Dataset, 'data')
    def test_when_only_one_column_requested_adds_column_index_query_param(self, mock_method):
        mock_method.return_value = self.data_list_obj
        MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')]).data(params={'start_date': '2015-07-01'})
        expected_calls = [call(params={'start_date': '2015-07-01'}),
                          call(params={'column_index': 1, 'start_date': '2015-07-01'}),
                          call(params={'start_date': '2015-07-01'})]
        self.assertEqual(mock_method.mock_calls[0], expected_calls[0])
        self.assertEqual(mock_method.mock_calls[1], expected_calls[1])
        self.assertEqual(mock_method.mock_calls[2], expected_calls[2])

    @patch.object(Dataset, 'data')
    def test_data_forwards_requests_to_datset_data(self, mock_method):
        mock_method.return_value = self.data_list_obj
        MergedDataset(
            ['NSE/OIL', 'WIKI/AAPL',
             'WIKI/MSFT']).data(params={'start_date': '2015-07-01'})
        self.assertEqual(mock_method.call_count, 3)
        for actual in mock_method.mock_calls:
            self.assertEqual(actual, call(params={'start_date': '2015-07-01'}))

    def test_get_merged_dataset_data_returns_correct_types(self):
        data = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')]).data()
        self.assertIsInstance(data, MergedDataList)
        self.assertIsInstance(data[0], Data)

    def test_get_merged_dataset_creates_merged_pandas_dataframe(self):
        data = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('WIKI/AAPL', {'column_index': [1]}),
             ('WIKI/MSFT')]).data()
        self.assertIsInstance(data.to_pandas(), pandas.core.frame.DataFrame)

    def test_get_merged_dataset_data_returns_specified_columns(self):
        data = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('SINGLE/COLUMN', {'column_index': [1]}),
             ('WIKI/MSFT')]).data()
        actual = data.to_pandas().columns.tolist()
        expected = [six.u('NSE/OIL - column.1'),
                    six.u('NSE/OIL - column.2'),
                    six.u('SINGLE/COLUMN - column.1'),
                    six.u('WIKI/MSFT - column.1'),
                    six.u('WIKI/MSFT - column.2'),
                    six.u('WIKI/MSFT - column.3')]
        self.assertItemsEqual(actual, expected)

    def test_get_merged_dataset_data_to_list(self):
        data = MergedDataset(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('SINGLE/COLUMN', {'column_index': [1]}),
             'WIKI/MSFT']).data()
        results = data.to_list()
        # NSE/OIL two columns of data
        # SINGLE/COLUMN one column of data
        # WIKI/MSFT all 3 columns of data
        expected = [[datetime.datetime(2015, 7, 11, 0, 0), 444.3, 10, 444.3, 444.3, 10, 3],
                    [datetime.datetime(2015, 7, 13, 0, 0), 433.3, 4, 433.3, 433.3, 4, 3],
                    [datetime.datetime(2015, 7, 14, 0, 0), 437.5, 3, 437.5, 437.5, 3, 3],
                    [datetime.datetime(2015, 7, 15, 0, 0), 440.0, 2, 440.0, 440.0, 2, 3]]
        for index, expected_item in enumerate(expected):
            self.assertItemsEqual(results[index], expected_item)

    def test_get_merged_dataset_data_is_descending_when_specified_in_params(self):
        data = MergedDataset(['NSE/OIL', 'WIKI/AAPL',
                              'WIKI/MSFT']).data(params={'order': 'desc'})
        results = data.to_list()
        dates = list([x[0] for x in results])
        self.assertTrue(all(dates[i] >= dates[i + 1]
                            for i in range(len(dates) - 1)))
