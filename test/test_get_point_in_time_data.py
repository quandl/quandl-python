import re
import unittest
import httpretty
import json
import pandas
from mock import patch, call
import quandl
from quandl.utils.request_type_util import RequestType
from quandl.errors.quandl_error import InvalidRequestError
from datetime import date


class GetPointInTimeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET,
                               re.compile('https://data.nasdaq.com/api/v3/pit*'),
                               body=json.dumps({}))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def tearDown(self):
        RequestType.USE_GET_REQUEST = True

    @patch('quandl.connection.Connection.request')
    def test_get_point_in_time_returns_data_frame_object(self, mock):
        df = quandl.get_point_in_time('ZACKS/FC', interval='asofdate', date='2020-01-01')
        self.assertIsInstance(df, pandas.core.frame.DataFrame)

    @patch('quandl.connection.Connection.request')
    def test_asofdate_call_connection(self, mock):
        quandl.get_point_in_time('ZACKS/FC', interval='asofdate', date='2020-01-01')
        expected = call('get', 'pit/ZACKS/FC/asofdate/2020-01-01', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_asofdate_call_connection_with_datetimes(self, mock):
        quandl.get_point_in_time('ZACKS/FC', interval='asofdate', date='2020-01-01T12:55')
        expected = call('get', 'pit/ZACKS/FC/asofdate/2020-01-01T12:55', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_asofdate_call_without_date(self, mock):
        quandl.get_point_in_time('ZACKS/FC', interval='asofdate')
        expected = call('get', "pit/ZACKS/FC/asofdate/%s" % date.today(), params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_from_call_connection(self, mock):
        quandl.get_point_in_time(
            'ZACKS/FC',
            interval='from',
            start_date='2020-01-01',
            end_date='2020-01-02'
        )
        expected = call('get', 'pit/ZACKS/FC/from/2020-01-01/to/2020-01-02', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_from_call_connection_with_datetimes(self, mock):
        quandl.get_point_in_time(
            'ZACKS/FC',
            interval='from',
            start_date='2020-01-01T12:00',
            end_date='2020-01-02T14:00'
        )
        expected = call('get', 'pit/ZACKS/FC/from/2020-01-01T12:00/to/2020-01-02T14:00', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_between_call_connection(self, mock):
        quandl.get_point_in_time(
            'ZACKS/FC',
            interval='between',
            start_date='2020-01-01',
            end_date='2020-01-02'
        )
        expected = call('get', 'pit/ZACKS/FC/between/2020-01-01/2020-01-02', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_between_call_connection_with_datetimes(self, mock):
        quandl.get_point_in_time(
            'ZACKS/FC',
            interval='between',
            start_date='2020-01-01T12:00',
            end_date='2020-01-02T14:00'
        )
        expected = call('get', 'pit/ZACKS/FC/between/2020-01-01T12:00/2020-01-02T14:00', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('quandl.connection.Connection.request')
    def test_invalid_interval_connection(self, mock):
        self.assertRaises(InvalidRequestError, lambda: quandl.get_point_in_time('ZACKS/FC'))
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time('ZACKS/FC', interval='quandl')
        )

    @patch('quandl.connection.Connection.request')
    def test_invalid_from_connection(self, mock):
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time('ZACKS/FC', interval='from')
        )
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time('ZACKS/FC', interval='from', start_date='2020-01-01')
        )
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time('ZACKS/FC', interval='from', end_date='2020-01-02')
        )

    @patch('quandl.connection.Connection.request')
    def test_invalid_between_connection(self, mock):
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time('ZACKS/FC', interval='between')
        )
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time(
                'ZACKS/FC',
                interval='between',
                start_date='2020-01-01'
            )
        )
        self.assertRaises(
            InvalidRequestError,
            lambda: quandl.get_point_in_time('ZACKS/FC', interval='between', end_date='2020-01-02')
        )
