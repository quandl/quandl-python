import re
import unittest2
import httpretty
import json
from quandl.model.datatable import Datatable
import pandas
from mock import patch
from test.factories.datatable import DatatableFactory
from test.factories.datatable_data import DatatableDataFactory
from test.factories.datatable_meta import DatatableMetaFactory
import quandl


class GetDataTableTest(unittest2.TestCase):

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
                                   'https://www.quandl.com/api/v3/datatables*'),
                               body=json.dumps(datatable))
        cls.datatable_instance = Datatable(datatable['datatable'])

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    @patch('quandl.connection.Connection.request')
    def test_datatable_returns_pandas_datatable_object(self, mock):
        df = quandl.get_table('ZACKS/FC')
        self.assertIsInstance(df, pandas.core.frame.DataFrame)

    @patch('quandl.connection.Connection.request')
    def test_datatable_returns_numpy_datatable_object(self, mock):
        df = quandl.get_table('ZACKS/FC', returns='numpy')
        self.assertEqual(type(df).__name__, 'recarray')

    @patch('quandl.connection.Connection.request')
    def test_datatable_returns_csv_datatable_object(self, mock):
        df = quandl.get_table('ZACKS/FC', returns='csv')
        self.assertEqual(type(df).__name__, 'str')
