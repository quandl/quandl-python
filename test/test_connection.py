from quandl.connection import Connection
from quandl.api_config import ApiConfig
from quandl.errors.quandl_error import (
    QuandlError, LimitExceededError, InternalServerError,
    AuthenticationError, ForbiddenError, InvalidRequestError,
    NotFoundError, ServiceUnavailableError)
import unittest2
from test.helpers.httpretty_extension import httpretty
import json
from mock import patch, call


class ConnectionTest(unittest2.TestCase):

    @httpretty.activate
    def test_quandl_exceptions(self):
        quandl_errors = [('QELx04', 429, LimitExceededError),
                         ('QEMx01', 500, InternalServerError),
                         ('QEAx01', 400, AuthenticationError),
                         ('QEPx02', 403, ForbiddenError),
                         ('QESx03', 422, InvalidRequestError),
                         ('QECx05', 404, NotFoundError),
                         ('QEXx01', 503, ServiceUnavailableError),
                         ('QEZx02', 400, QuandlError)]

        httpretty.register_uri(httpretty.GET,
                               "https://www.quandl.com/api/v3/databases",
                               responses=[httpretty.Response(body=json.dumps(
                                   {'quandl_error':
                                    {'code': x[0], 'message': 'something went wrong'}}),
                                   status=x[1]) for x in quandl_errors]
                               )

        for expected_error in quandl_errors:
            self.assertRaises(
                expected_error[2], lambda: Connection.request('get', 'databases'))

    @httpretty.activate
    def test_parse_error(self):
        httpretty.register_uri(httpretty.GET,
                               "https://www.quandl.com/api/v3/databases",
                               body="not json", status=500)
        self.assertRaises(
            QuandlError, lambda: Connection.request('get', 'databases'))

    @httpretty.activate
    def test_non_quandl_error(self):
        httpretty.register_uri(httpretty.GET,
                               "https://www.quandl.com/api/v3/databases",
                               body=json.dumps(
                                {'foobar':
                                 {'code': 'blah', 'message': 'something went wrong'}}), status=500)
        self.assertRaises(
            QuandlError, lambda: Connection.request('get', 'databases'))

    @httpretty.activate
    @patch('quandl.connection.Connection.execute_request')
    def test_build_request(self, mock):
        ApiConfig.api_key = 'api_token'
        ApiConfig.api_version = '2015-04-09'
        params = {'per_page': 10, 'page': 2}
        headers = {'x-custom-header': 'header value'}
        Connection.request('get', 'databases', headers=headers, params=params)
        expected = call('get', 'https://www.quandl.com/api/v3/databases',
                        headers={'x-custom-header': 'header value',
                                 'x-api-token': 'api_token',
                                 'accept': ('application/json, '
                                            'application/vnd.quandl+json;version=2015-04-09'),
                                 'request-source': 'python',
                                 'request-source-version': '3.3.0'},
                        params={'per_page': 10, 'page': 2})
        self.assertEqual(mock.call_args, expected)
