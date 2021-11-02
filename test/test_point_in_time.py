import json
import re

import httpretty
from mock import call, patch

from nasdaqdatalink.model.point_in_time import PointInTime
from test.test_retries import ModifyRetrySettingsTestCase
from nasdaqdatalink.utils.request_type_util import RequestType


class GetPointInTimeTest(ModifyRetrySettingsTestCase):

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET,
                               re.compile('https://data.nasdaq.com/api/v3/pit/*'),
                               body=json.dumps({}))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def tearDown(self):
        RequestType.USE_GET_REQUEST = True

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_asofdate_call_connection(self, mock):
        PointInTime(
            'ZACKS/FC',
            pit={
                'interval': 'asofdate',
                'date': '2020-01-01'
            }
        ).data()
        expected = call('get', 'pit/ZACKS/FC/asofdate/2020-01-01', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_from_call_connection(self, mock):
        PointInTime(
            'ZACKS/FC',
            pit={
                'interval': 'from',
                'start_date': '2020-01-01',
                'end_date': '2020-01-02'
            }
        ).data()
        expected = call('get', 'pit/ZACKS/FC/from/2020-01-01/to/2020-01-02', params={})
        self.assertEqual(mock.call_args, expected)

    @patch('nasdaqdatalink.connection.Connection.request')
    def test_between_call_connection(self, mock):
        PointInTime(
            'ZACKS/FC',
            pit={
                'interval': 'between',
                'start_date': '2020-01-01',
                'end_date': '2020-01-02'
            }
        ).data()
        expected = call('get', 'pit/ZACKS/FC/between/2020-01-01/2020-01-02', params={})
        self.assertEqual(mock.call_args, expected)
