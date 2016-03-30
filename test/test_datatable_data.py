import re
import unittest2
import httpretty
import json
import pandas
import numpy
import six
from quandl.model.data import Data
from quandl.model.datatable import Datatable
from mock import patch, call
from test.factories.datatable_data import DatatableDataFactory
from test.factories.datatable_meta import DatatableMetaFactory


class DatatableDataTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_column_names = [six.u('per_end_date'),
                                     six.u('ticker'),
                                     six.u('tot_oper_exp')]
        cls.expected_column_types = [six.u('Date'),
                                     six.u('String'),
                                     six.u('String')]
        cls.data_object = Data(['2015-07-11', 'AAPL', 440.0],
                               meta={'columns': cls.expected_column_names,
                                     'column_types': cls.expected_column_types})

    def test_to_pandas_returns_pandas_dataframe_object(self):
        data = self.data_object.to_pandas()
        self.assertIsInstance(data, pandas.core.frame.DataFrame)

    # don't set dataFrame for datatable
    def test_pandas_dataframe_index_is_datetime(self):
        df = self.data_object.to_pandas()
        self.assertEqual(df.index.name, 'None')

    def test_to_numpys_returns_numpy_object(self):
        data = self.data_object.to_numpy()
        self.assertIsInstance(data, numpy.core.records.recarray)

    def test_to_csv_returns_expected_csv(self):
        data = self.data_object.to_csv()
        expected = "None,per_end_date,ticker,tot_oper_exp\n0,2015-07-11,AAPL,440.0\n"
        self.assertEqual(data, expected)

    def test_column_names(self):
        actual = self.data_object.columns
        self.assertEqual(actual, self.expected_column_names)

    def test_meta_exists(self):
        self.assertIsNotNone(self.data_object.meta)


class ListDatatableDataTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        datatable_data = {'datatable': DatatableDataFactory.build()}
        meta = {'meta': DatatableMetaFactory.build()}
        datatable_data.update(meta)
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datatables/*'),
                               body=json.dumps(datatable_data))
        cls.expected_raw_data = []
        cls.expected_list_values = []

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.connection.Connection.request')
    def test_data_calls_connection(self, mock):
        datatable = Datatable('ZACKS/FC')
        Data.page(datatable, params={'ticker': ['AAPL', 'MSFT'],
                                     'per_end_date': {'gte': {'2015-01-01'}},
                                     'qopts': {'columns': ['ticker', 'per_end_date']}})
        expected = call('get', 'datatables/ZACKS/FC', params={'ticker': ['AAPL', 'MSFT'],
                                                              'per_end_date':
                                                              {'gte': {'2015-01-01'}},
                                                              'qopts': {'columns':
                                                                        ['ticker',
                                                                         'per_end_date']}})
        self.assertEqual(mock.call_args, expected)

    def test_values_and_meta_exist(self):
        datatable = Datatable('ZACKS/FC')
        results = Data.page(datatable, params={})
        self.assertIsNotNone(results.values)
        self.assertIsNotNone(results.meta)

    def test_to_pandas_returns_pandas_dataframe_object(self):
        datatable = Datatable('ZACKS/FC')
        results = Data.page(datatable, params={})
        df = results.to_pandas()
        self.assertIsInstance(df, pandas.core.frame.DataFrame)

    # no index is set for datatable.to_pandas
    def test_pandas_dataframe_index_is_none(self):
        datatable = Datatable('ZACKS/FC')
        results = Data.page(datatable, params={})
        df = results.to_pandas()
        self.assertEqual(df.index.name, 'None')

    # if datatable has Date field then it should be convert to pandas datetime
    def test_pandas_dataframe_date_field_is_datetime(self):
        datatable = Datatable('ZACKS/FC')
        results = Data.page(datatable, params={})
        df = results.to_pandas()
        self.assertIsInstance(df['per_end_date'][0], pandas.datetime)
        self.assertIsInstance(df['per_end_date'][1], pandas.datetime)
        self.assertIsInstance(df['per_end_date'][2], pandas.datetime)
        self.assertIsInstance(df['per_end_date'][3], pandas.datetime)

    def test_to_numpy_returns_numpy_object(self):
        datatable = Datatable('ZACKS/FC')
        results = Data.page(datatable, params={})
        data = results.to_numpy()
        self.assertIsInstance(data, numpy.core.records.recarray)

    def test_to_csv_returns_expected_csv(self):
        datatable = Datatable('ZACKS/FC')
        results = Data.page(datatable, params={})
        data = results.to_csv()
        expected = "None,per_end_date,ticker,tot_oper_exp\n" + \
                   "0,2015-07-11,AAPL,456.9\n" + \
                   "1,2015-07-13,433.3,\n" + \
                   "2,2015-07-14,AAPL,419.1\n" + \
                   "3,2015-07-15,476.5,\n"
        self.assertEqual(data, expected)
