import re
import unittest2
import httpretty
import json
import six
import datetime
import pandas
from quandl.model.data import Data
from quandl.model.data_list import DataList
from quandl.model.merged_data_list import MergedDataList
from quandl.model.dataset import Dataset
from quandl.model.merged_dataset import MergedDataset
from mock import patch, call
from test.factories.dataset import DatasetFactory
from test.factories.dataset_data import DatasetDataFactory


class GetMergedDatasetTest(unittest2.TestCase):

    @classmethod
    def setUp(self):
        httpretty.reset()
        httpretty.enable()

        self.dataset_data = {'dataset_data': DatasetDataFactory.build()}

        dataset_data = DatasetDataFactory.build()
        d_values = dataset_data.pop('data')
        d_metadata = dataset_data
        self.data_list_obj = DataList(Data, d_values, d_metadata)

        self.nse_oil = {'dataset': DatasetFactory.build(
            database_code='NSE', dataset_code='OIL')}

        self.goog_aapl = {'dataset': DatasetFactory.build(
            database_code='GOOG', dataset_code='NASDAQ_AAPL')}

        self.goog_msft = {'dataset': DatasetFactory.build(
            database_code='GOOG', dataset_code='NASDAQ_MSFT',
            newest_available_date='2015-07-30', oldest_available_date='2013-01-01')}

        self.oil_obj = Dataset(self.nse_oil['dataset'])
        self.aapl_obj = Dataset(self.goog_aapl['dataset'])
        self.goog_obj = Dataset(self.goog_msft['dataset'])

        self.dataset_objs = [self.oil_obj, self.aapl_obj, self.goog_obj]

        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datasets/.*/metadata'),
                               responses=[httpretty.Response(body=json.dumps(dataset))
                                          for dataset in
                                          [self.nse_oil, self.goog_aapl, self.goog_msft]])
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datasets/.*/data'),
                               body=json.dumps(self.dataset_data))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.model.dataset.Dataset.get')
    def test_merged_dataset_calls_Dataset_get(self, mock):
        mock.return_value = self.oil_obj
        MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        expected_calls = [
            call('NSE/OIL'), call('GOOG/NASDAQ_AAPL'), call('GOOG/NASDAQ_MSFT')]
        self.assertEqual(mock.call_count, 3)
        for index, expected in enumerate(expected_calls):
            self.assertEqual(mock.mock_calls[index], expected)

    @patch('quandl.model.merged_dataset.MergedDataset._get_dataset')
    def test_removes_column_index_query_param(self, mock):
        self.oil_obj.column_index = []
        mock.return_value = self.oil_obj
        MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]})], params={'column_index': 1})
        expected = call(('NSE/OIL', {'column_index': [1, 2]}), params={})
        self.assertEqual(mock.call_args, expected)

    def test_sets_column_index_on_each_dataset(self):
        md = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        self.assertItemsEqual([1, 2], md._datasets[0].column_index)
        self.assertItemsEqual([1], md._datasets[1].column_index)
        self.assertItemsEqual([], md._datasets[2].column_index)

    def test_merged_dataset_column_names(self):
        md = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        expected = [six.u('Date'), six.u('NSE/OIL - column.1'),
                    six.u('NSE/OIL - column.2'),
                    six.u('GOOG/NASDAQ_AAPL - column.1'),
                    six.u('GOOG/NASDAQ_MSFT - column.1'),
                    six.u('GOOG/NASDAQ_MSFT - column.2'),
                    six.u('GOOG/NASDAQ_MSFT - column.3')]
        self.assertItemsEqual(md.column_names, expected)

    def test_merged_dataset_oldest_available_date(self):
        md = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        self.assertEqual(md.oldest_available_date, datetime.date(2013, 1, 1))

    def test_merged_dataset_newest_available_date(self):
        md = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        self.assertEqual(md.newest_available_date, datetime.date(2015, 7, 30))

    def test_merged_dataset_database_codes(self):
        md = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        self.assertItemsEqual(md.database_code, ['NSE', 'GOOG'])

    def test_merged_dataset_dataset_codes(self):
        md = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')])
        self.assertItemsEqual(
            md.dataset_code, ['OIL', 'NASDAQ_AAPL', 'NASDAQ_MSFT'])

    def test_get_returns_merged_dataset_obj(self):
        md = MergedDataset.get(['NSE/OIL'])
        self.assertIsInstance(md, MergedDataset)

    def test_raise_error_when_datasets_arg_not_list(self):
        self.assertRaises(ValueError, lambda: MergedDataset.get('NSE/OIL'))

    def test_raise_error_when_datasets_arg_list_has_invalid_type(self):
        self.assertRaises(
            ValueError, lambda: MergedDataset.get(['NSE/OIL', {'blah': [1]}]))

    def test_raise_error_when_column_index_specified_and_not_list(self):
        self.assertRaises(ValueError, lambda: MergedDataset.get(
            [('NSE/OIL', {'column_index': 'foo'})]))

    def test_raise_error_when_column_index_greater_than_max(self):
        self.assertRaises(
            ValueError, lambda: MergedDataset.get([('NSE/OIL', {'column_index': [10]})]))

    def test_raise_error_when_column_index_less_than_one(self):
        self.assertRaises(
            ValueError, lambda: MergedDataset.get([('NSE/OIL', {'column_index': [0]})]))

    @patch.object(Dataset, 'data')
    def test_data_forwards_requests_to_datset_data(self, mock_method):
        mock_method.return_value = self.data_list_obj
        MergedDataset.get(
            ['NSE/OIL', 'GOOG/NASDAQ_AAPL',
             'GOOG/NASDAQ_MSFT']).data(params={'start_date': '2015-07-01'})
        self.assertEqual(mock_method.call_count, 3)
        for actual in mock_method.mock_calls:
            self.assertEqual(actual, call(params={'start_date': '2015-07-01'}))

    def test_get_merged_dataset_data_returns_correct_types(self):
        data = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')]).data()
        self.assertIsInstance(data, MergedDataList)
        self.assertIsInstance(data[0], Data)

    def test_get_merged_dataset_creates_merged_pandas_dataframe(self):
        data = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')]).data()
        self.assertIsInstance(data.to_pandas(), pandas.core.frame.DataFrame)

    def test_get_merged_dataset_data_returns_specified_columns(self):
        data = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT')]).data()
        actual = data.to_pandas().columns.tolist()
        expected = [six.u('NSE/OIL - column.1'),
                    six.u('NSE/OIL - column.2'),
                    six.u('GOOG/NASDAQ_AAPL - column.1'),
                    six.u('GOOG/NASDAQ_MSFT - column.1'),
                    six.u('GOOG/NASDAQ_MSFT - column.2'),
                    six.u('GOOG/NASDAQ_MSFT - column.3')]
        self.assertItemsEqual(actual, expected)

    def test_get_merged_dataset_data_to_list(self):
        data = MergedDataset.get(
            [('NSE/OIL', {'column_index': [1, 2]}),
             ('GOOG/NASDAQ_AAPL', {'column_index': [1]}),
             ('GOOG/NASDAQ_MSFT', {'column_index': [3]})]).data()
        results = data.to_list()
        expected = [[datetime.datetime(2015, 7, 11, 0, 0), 444.3, 10, 444.3, 3],
                    [datetime.datetime(2015, 7, 13, 0, 0), 433.3, 4, 433.3, 3],
                    [datetime.datetime(2015, 7, 14, 0, 0), 437.5, 3, 437.5, 3],
                    [datetime.datetime(2015, 7, 15, 0, 0), 440.0, 2, 440.0, 3]]
        for index, expected_item in enumerate(expected):
            self.assertItemsEqual(results[index], expected_item)

    def test_get_merged_dataset_data_is_descending_when_specified_in_params(self):
        data = MergedDataset.get(['NSE/OIL', 'GOOG/NASDAQ_AAPL',
                                  'GOOG/NASDAQ_MSFT']).data(params={'order': 'desc'})
        results = data.to_list()
        dates = list([x[0] for x in results])
        self.assertTrue(all(dates[i] >= dates[i + 1]
                            for i in range(len(dates) - 1)))
