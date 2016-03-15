import re
import unittest2
from test.helpers.httpretty_extension import httpretty
import json
import datetime
from quandl.model.dataset import Dataset
from quandl.model.database import Database
from mock import patch, call
from test.factories.dataset import DatasetFactory
from test.factories.meta import MetaFactory


class GetDatasetTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        dataset = {'dataset': DatasetFactory.build(
            database_code='NSE', dataset_code='OIL')}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datasets/*'),
                               body=json.dumps(dataset))
        dataset_code = Dataset.get_code_from_meta(dataset['dataset'])
        cls.dataset_instance = Dataset(dataset_code, dataset['dataset'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.connection.Connection.request')
    def test_dataset_calls_connection(self, mock):
        d = Dataset('NSE/OIL')
        d.data_fields()
        expected = call('get', 'datasets/NSE/OIL/metadata', params={})
        self.assertEqual(mock.call_args, expected)

    def test_dataset_returns_dataset_object(self):
        dataset = Dataset('NSE/OIL')
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.dataset_code, 'OIL')

    def test_dataset_attributes_are_datetime_objects(self):
        dataset = Dataset('NSE/OIL')
        self.assertIsInstance(dataset.refreshed_at, datetime.datetime)
        self.assertIsInstance(dataset.newest_available_date, datetime.date)

    def test_dataset_column_names_match_expected(self):
        dataset = Dataset('NSE/OIL')
        self.assertItemsEqual(
            dataset.column_names, ['Date', 'column.1', 'column.2', 'column.3'])

    def test_dataset_database_gives_instance_of_database(self):
        database = self.dataset_instance.database()
        self.assertIsInstance(database, Database)

    @patch('quandl.model.data.Data.all')
    def test_dataset_data_calls_data_all(self, mock):
        self.dataset_instance.data(
            params={'start_date': '2015-07-01', 'end_date': '2015-07-10'})
        expected = call(params={'dataset_code': 'OIL', 'database_code': 'NSE',
                                'start_date': '2015-07-01', 'end_date': '2015-07-10',
                                'order': 'asc'})
        self.assertEqual(mock.call_args, expected)


class ListDatasetsTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        datasets = {'datasets': DatasetFactory.build_batch(3)}
        meta = {'meta': MetaFactory.build(current_page=1, total_pages=1)}
        datasets.update(meta)
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://www.quandl.com/api/v3/datasets*'),
                               body=json.dumps(datasets))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.connection.Connection.request')
    def test_datasets_calls_connection(self, mock):
        Dataset.all()
        expected = call('get', 'datasets', params={})
        self.assertEqual(mock.call_args, expected)

    def test_datasets_return_dataset_objects(self):
        results = Dataset.all()
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result, Dataset)

    def test_datasets_has_more_results(self):
        results = Dataset.all()
        self.assertFalse(results.has_more_results())

    def test_values_exist(self):
        results = Dataset.all()
        self.assertIsInstance(results.values, list)
        self.assertIsInstance(results.values[0], Dataset)

    def test_meta_attributes_can_be_accessed(self):
        results = Dataset.all()
        self.assertEqual(results.meta['current_page'], 1)
        self.assertEqual(results.current_page, 1)

    def test_to_list_returns_list(self):
        results = Dataset.all()
        data = results.to_list()
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], list)
