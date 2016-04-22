import re
import unittest2
from test.helpers.httpretty_extension import httpretty
import json
import datetime
import pandas
import numpy
import six
from quandl.model.data import Data
from mock import patch, call
from test.factories.dataset_data import DatasetDataFactory
from quandl.errors.quandl_error import InvalidDataError


class DataTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_column_names = [six.u('Date'), six.u('column.1'),
                                     six.u('column.2'), six.u('column.3')]
        cls.data_object = Data(['2015-07-15', 440.0, 2, 3],
                               meta={'column_names': cls.expected_column_names})

    def test_to_pandas_returns_pandas_dataframe_object(self):

        data = self.data_object.to_pandas()
        self.assertIsInstance(data, pandas.core.frame.DataFrame)

    def test_pandas_dataframe_index_is_datetime(self):
        df = self.data_object.to_pandas()
        self.assertEqual(df.index.name, 'Date')
        self.assertIsInstance(df.index, pandas.DatetimeIndex)

    def test_to_numpys_returns_numpy_object(self):
        data = self.data_object.to_numpy()
        self.assertIsInstance(data, numpy.core.records.recarray)

    def test_to_csv_returns_expected_csv(self):
        data = self.data_object.to_csv()
        expected = "Date,column.1,column.2,column.3\n2015-07-15,440.0,2,3\n"
        self.assertEqual(data, expected)

    def test_column_names(self):
        actual = self.data_object.column_names
        self.assertEqual(actual, self.expected_column_names)

    def test_meta_exists(self):
        self.assertIsNotNone(self.data_object.meta)


class ListDataTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        dataset_data = {'dataset_data': DatasetDataFactory.build()}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datasets*'),
                               body=json.dumps(dataset_data))
        cls.expected_raw_data = [{'date': datetime.date(2015, 7, 11), 'column1': 444.3,
                                  'column2': 10, 'column3': 3},
                                 {'date': datetime.date(2015, 7, 13), 'column1': 433.3,
                                  'column2': 4, 'column3': 3},
                                 {'date': datetime.date(2015, 7, 14), 'column1': 437.5,
                                  'column2': 3, 'column3': 3},
                                 {'date': datetime.date(2015, 7, 15), 'column1': 440.0,
                                  'column2': 2, 'column3': 3}]

        cls.expected_list_values = [[datetime.date(2015, 7, 11), 444.3, 10, 3],
                                    [datetime.date(2015, 7, 13), 433.3, 4, 3],
                                    [datetime.date(2015, 7, 14), 437.5, 3, 3],
                                    [datetime.date(2015, 7, 15), 440.0, 2, 3]]

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.connection.Connection.request')
    def test_data_calls_connection(self, mock):
        Data.all(params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        expected = call('get', 'datasets/NSE/OIL/data', params={})
        self.assertEqual(mock.call_args, expected)

    def test_data_returned_are_data_objects(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        self.assertEqual(len(results), 4)
        for result in results:
            self.assertIsInstance(result, Data)

    def test_values_and_meta_exist(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        self.assertIsNotNone(results.values)
        self.assertIsNotNone(results.meta)

    def test_column_names_match(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        self.assertItemsEqual(
            results.column_names, ['Date', 'column.1', 'column.2', 'column.3'])

    def test_raw_data_is_zip_of_column_names_and_data(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        self.assertItemsEqual(results[0].__get_raw_data__(), self.expected_list_values[0])
        self.assertItemsEqual(results[1].__get_raw_data__(), self.expected_list_values[1])
        self.assertItemsEqual(results[2].__get_raw_data__(), self.expected_list_values[2])
        self.assertItemsEqual(results[3].__get_raw_data__(), self.expected_list_values[3])

    def test_data_to_list(self):
        list_data = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'}).to_list()
        self.assertItemsEqual(list_data[0], self.expected_list_values[0])
        self.assertItemsEqual(list_data[1], self.expected_list_values[1])
        self.assertItemsEqual(list_data[2], self.expected_list_values[2])
        self.assertItemsEqual(list_data[3], self.expected_list_values[3])

    def test_to_pandas_returns_pandas_dataframe_object(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        df = results.to_pandas()
        self.assertIsInstance(df, pandas.core.frame.DataFrame)

    def test_pandas_dataframe_index_is_datetime(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        df = results.to_pandas()
        self.assertEqual(df.index.name, 'Date')
        self.assertIsInstance(df.index, pandas.DatetimeIndex)

    def test_to_numpy_returns_numpy_object(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        data = results.to_numpy()
        self.assertIsInstance(data, numpy.core.records.recarray)

    def test_to_csv_returns_expected_csv(self):
        results = Data.all(
            params={'database_code': 'NSE', 'dataset_code': 'OIL'})
        data = results.to_csv()
        expected = "Date,column.1,column.2,column.3\n2015-07-11,444.3,10,3\n" + \
                   "2015-07-13,433.3,4,3\n2015-07-14,437.5,3,3\n2015-07-15,440.0,2,3\n"
        self.assertEqual(data, expected)

    def test_exception_raised_if_column_and_data_row_mistmatch(self):
        dataset_data = {
            'dataset_data': DatasetDataFactory.build(column_names=['blah'])}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datasets*'),
                               body=json.dumps(dataset_data))
        self.assertRaises(InvalidDataError, lambda: Data.all())
