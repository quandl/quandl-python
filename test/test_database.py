import json
import re
import unittest

import six
from mock import call, mock_open, patch
from six.moves.urllib.parse import parse_qs, urlparse

from nasdaqdatalink.api_config import ApiConfig
from nasdaqdatalink.connection import Connection
from nasdaqdatalink.errors.data_link_error import (InternalServerError, DataLinkError)
from nasdaqdatalink.model.database import Database
from test.factories.database import DatabaseFactory
from test.factories.meta import MetaFactory
from test.helpers.httpretty_extension import httpretty
from test.test_retries import ModifyRetrySettingsTestCase


class GetDatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        database = {'database': DatabaseFactory.build(database_code='NSE')}
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/databases/*'),
                               body=json.dumps(database))
        cls.db_instance = Database(Database.get_code_from_meta(
            database['database']), database['database'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_database_calls_connection(self, mock):
        database = Database('NSE')
        database.data_fields()
        expected = call('get', 'databases/NSE', params={})
        self.assertEqual(mock.call_args, expected)

    def test_database_returns_database_object(self):
        database = Database('NSE')
        self.assertIsInstance(database, Database)
        self.assertEqual(database.database_code, 'NSE')

    @patch('nasdaqdatalink.model.dataset.Dataset.all')
    def test_database_datasets_calls_datasets_all(self, mock):
        self.db_instance.datasets()
        expected = call(
            params={'query': '', 'database_code': 'NSE', 'page': 1})
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.model.dataset.Dataset.all')
    def test_database_datasets_accepts_query_params(self, mock):
        self.db_instance.datasets(params={'query': 'foo', 'page': 2})
        expected = call(
            params={'query': 'foo', 'database_code': 'NSE', 'page': 2})
        self.assertEqual(mock.call_args, expected)


class ListDatabasesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        databases = {'databases': DatabaseFactory.build_batch(10)}
        meta = {'meta': MetaFactory.build()}
        databases.update(meta)
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/databases*'),
                               body=json.dumps(databases))
        cls.expected_databases = databases

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_databases_calls_connection(self, mock):
        Database.all()
        expected = call('get', 'databases', params={})
        self.assertEqual(mock.call_args, expected)

    def test_databases_returns_database_objects(self):
        results = Database.all()
        self.assertEqual(len(results), 10)
        for result in results:
            self.assertIsInstance(result, Database)

    def test_databases_has_meta(self):
        results = Database.all()
        self.assertIsNotNone(results.meta)

    def test_databases_returns_expected_ids(self):
        results = Database.all()
        self.assertEqual(len(results), 10)
        six.assertCountEqual(self, [x.id for x in results],
                             [x['id'] for x in self.expected_databases['databases']])

    def test_databases_has_more(self):
        results = Database.all()
        self.assertTrue(results.has_more_results())


class BulkDownloadDatabaseTest(ModifyRetrySettingsTestCase):

    def setUp(self):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/databases/*'),
                               adding_headers={
                                   'Location': 'https://www.blah.com/download/db.zip'
                               },
                               body='{}', status=302)
        httpretty.register_uri(httpretty.GET,
                               re.compile('https://www.blah.com/'), body='{}')

        database = {'database': DatabaseFactory.build(database_code='NSE')}
        self.database = Database(database['database']['database_code'], database['database'])
        ApiConfig.api_key = 'api_token'
        ApiConfig.api_version = '2015-04-09'

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_get_bulk_downnload_url_with_download_type(self):
        url = self.database.bulk_download_url(params={'download_type': 'partial'})
        parsed_url = urlparse(url)
        self.assertEqual(parsed_url.scheme, 'https')
        self.assertEqual(parsed_url.netloc, 'data.nasdaq.com')
        self.assertEqual(parsed_url.path, '/api/v3/databases/NSE/data')
        self.assertDictEqual(parse_qs(parsed_url.query), {
                             'download_type': ['partial'],
                             'api_key': ['api_token'], 'api_version': ['2015-04-09']})

    def test_get_bulk_download_url_without_download_type(self):
        url = self.database.bulk_download_url()
        parsed_url = urlparse(url)
        self.assertDictEqual(parse_qs(parsed_url.query), {
                             'api_key': ['api_token'], 'api_version': ['2015-04-09']})

    def test_bulk_download_to_fileaccepts_download_type(self):
        m = mock_open()
        with patch.object(Connection, 'request') as mock_method:
            mock_method.return_value.url = 'https://www.blah.com/download/db.zip'
            with patch('nasdaqdatalink.model.database.open', m, create=True):
                self.database.bulk_download_to_file(
                    '.', params={'download_type': 'partial'})

        expected = call('get',
                        'databases/NSE/data',
                        params={'download_type': 'partial'},
                        stream=True)
        self.assertEqual(mock_method.call_args, expected)

    def test_bulk_download_to_file_writes_to_file(self):
        m = mock_open()
        with patch('nasdaqdatalink.model.database.open', m, create=True):
            self.database.bulk_download_to_file('.')

        m.assert_called_once_with(six.u('./db.zip'), 'wb')
        m().write.assert_called_once_with(six.b('{}'))

    def test_bulk_download_raises_exception_when_no_path(self):
        self.assertRaises(
            DataLinkError, lambda: self.database.bulk_download_to_file(None))

    def test_bulk_download_raises_exception_when_error_response(self):
        ApiConfig.retry_backoff_factor = 0
        httpretty.reset()
        httpretty.register_uri(httpretty.GET,
                               re.compile(
                                   'https://data.nasdaq.com/api/v3/databases/*'),
                               body=json.dumps(
                                   {'error':
                                    {'code': 'QEMx01', 'message': 'something went wrong'}}),
                               status=500)

        self.assertRaises(
            InternalServerError, lambda: self.database.bulk_download_to_file('.'))
