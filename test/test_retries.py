import unittest
import json

from nasdaqdatalink.connection import Connection
from nasdaqdatalink.api_config import ApiConfig
from test.factories.datatable import DatatableFactory
from test.helpers.httpretty_extension import httpretty
from nasdaqdatalink.errors.data_link_error import InternalServerError


class ModifyRetrySettingsTestCase(unittest.TestCase):

    def setUp(self):
        self.default_use_retries = ApiConfig.use_retries
        self.default_number_of_retries = ApiConfig.number_of_retries
        self.default_retry_backoff_factor = ApiConfig.retry_backoff_factor
        self.default_max_wait_between_retries = ApiConfig.max_wait_between_retries
        self.default_retry_status_codes = ApiConfig.retry_status_codes

    def tearDown(self):
        ApiConfig.use_retries = self.default_use_retries
        ApiConfig.number_of_retries = self.default_number_of_retries
        ApiConfig.retry_backoff_factor = self.default_retry_backoff_factor
        ApiConfig.max_wait_between_retries = self.default_max_wait_between_retries
        ApiConfig.retry_status_codes = self.default_retry_status_codes


class TestRetries(ModifyRetrySettingsTestCase):

    def setUp(self):
        ApiConfig.use_retries = True
        super(TestRetries, self).setUp()

    @classmethod
    def setUpClass(cls):
        cls.datatable = {'datatable': DatatableFactory.build(
            vendor_code='ZACKS',
            datatable_code='FC')}

        cls.error_response = httpretty.Response(
            body=json.dumps(
              {'error': {'code': 'QEMx01', 'message': 'something went wrong'}}
            ),
            status=500)
        cls.success_response = httpretty.Response(body=json.dumps(cls.datatable), status=200)

    def test_modifying_use_retries(self):
        ApiConfig.use_retries = False

        retries = Connection.get_session().get_adapter(ApiConfig.api_protocol).max_retries
        self.assertEqual(retries.total, 0)

    def test_modifying_number_of_retries(self):
        ApiConfig.number_of_retries = 3000

        retries = Connection.get_session().get_adapter(ApiConfig.api_protocol).max_retries

        self.assertEqual(retries.total, ApiConfig.number_of_retries)
        self.assertEqual(retries.connect, ApiConfig.number_of_retries)
        self.assertEqual(retries.read, ApiConfig.number_of_retries)

    def test_modifying_retry_backoff_factor(self):
        ApiConfig.retry_backoff_factor = 3000

        retries = Connection.get_session().get_adapter(ApiConfig.api_protocol).max_retries
        self.assertEqual(retries.backoff_factor, ApiConfig.retry_backoff_factor)

    def test_modifying_retry_status_codes(self):
        ApiConfig.retry_status_codes = [1, 2, 3]

        retries = Connection.get_session().get_adapter(ApiConfig.api_protocol).max_retries
        self.assertEqual(retries.status_forcelist, ApiConfig.retry_status_codes)

    def test_modifying_max_wait_between_retries(self):
        ApiConfig.max_wait_between_retries = 3000

        retries = Connection.get_session().get_adapter(ApiConfig.api_protocol).max_retries
        self.assertEqual(retries.BACKOFF_MAX, ApiConfig.max_wait_between_retries)

    @httpretty.enabled
    def test_correct_response_returned_if_retries_succeed(self):
        ApiConfig.number_of_retries = 3
        ApiConfig.retry_status_codes = [self.error_response.status]

        mock_responses = [self.error_response] + [self.error_response] + [self.success_response]
        httpretty.register_uri(httpretty.GET,
                               "https://data.nasdaq.com/api/v3/databases",
                               responses=mock_responses)

        response = Connection.request('get', 'databases')
        self.assertEqual(response.json(), self.datatable)
        self.assertEqual(response.status_code, self.success_response.status)

    @httpretty.enabled
    def test_correct_response_exception_raised_if_retries_fail(self):
        ApiConfig.number_of_retries = 2
        ApiConfig.retry_status_codes = [self.error_response.status]
        mock_responses = [self.error_response] * 3
        httpretty.register_uri(httpretty.GET,
                               "https://data.nasdaq.com/api/v3/databases",
                               responses=mock_responses)

        self.assertRaises(InternalServerError, Connection.request, 'get', 'databases')

    @httpretty.enabled
    def test_correct_response_exception_raised_for_errors_not_in_retry_status_codes(self):
        ApiConfig.retry_status_codes = []
        mock_responses = [self.error_response]
        httpretty.register_uri(httpretty.GET,
                               "https://data.nasdaq.com/api/v3/databases",
                               responses=mock_responses)

        self.assertRaises(InternalServerError, Connection.request, 'get', 'databases')
