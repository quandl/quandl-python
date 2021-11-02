import unittest
from nasdaqdatalink.utils.request_type_util import RequestType
from test.helpers.random_data_helper import generate_random_dictionary


class RequestTypeUtilTest(unittest.TestCase):

    def setUp(self):
        self.test_url = '/datables/WIKI/PRICES.json'
        RequestType.MAX_URL_LENGTH_FOR_GET = 200

    def tearDown(self):
        RequestType.MAX_URL_LENGTH_FOR_GET = 8000

    def test_no_params(self):
        request_type = RequestType.get_request_type(self.test_url, params={})
        self.assertEqual(request_type, 'get')

    def test_small_params(self):
        params = {'foo': 'bar', 'qopts': {'columns': 'date'}}
        request_type = RequestType.get_request_type(self.test_url, params=params)
        self.assertEqual(request_type, 'get')

    def test_long_params(self):
        params = generate_random_dictionary(20)
        request_type = RequestType.get_request_type(self.test_url, params=params)
        self.assertEqual(request_type, 'post')
