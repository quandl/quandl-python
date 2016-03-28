import unittest2
import datetime
import six
from quandl.util import Util


# use this function just for test This function is define in python 2 but not at python 3
def cmp(a, b):
    a = sorted(a)
    b = sorted(b)
    return (a > b) - (a < b)


class UtilTest(unittest2.TestCase):

    def test_methodize(self):
        self.assertEqual(
            Util.methodize(six.u('Hello World...Foo-Bar')), 'hello_worldfoo_bar')

    def test_convert_to_dates(self):
        d = '2015-04-09'
        dt = '2015-07-24T02:39:40.624Z'
        dic = {'foo': d, d: {'bar': dt}}
        result = Util.convert_to_dates(dic)
        self.assertIsInstance(result['foo'], datetime.date)
        self.assertIsInstance(result[d]['bar'], datetime.datetime)

    def test_merge_options_when_key_exists_in_options(self):
        params = {'foo': 'bar', 'foo2': 'bar2'}
        options = {'params': {'foo': 'bar3'}}
        merged = Util.merge_options('params', params, **options)
        self.assertDictEqual(
            merged, {'params': {'foo': 'bar3', 'foo2': 'bar2'}})

    def test_merge_options_when_key_doesnt_exist_in_options(self):
        params = {'foo': 'bar', 'foo2': 'bar2'}
        options = {'params': {'foo3': 'bar3'}}
        merged = Util.merge_options('params', params, **options)
        self.assertDictEqual(
            merged, {'params': {'foo': 'bar',
                                'foo2': 'bar2', 'foo3': 'bar3'}})

    def test_constructed_path(self):
        path = '/hello/:foo/world/:id'
        params = {'foo': 'bar', 'id': 1, 'another': 'a'}
        result = Util.constructed_path(path, params)
        self.assertEqual(result, '/hello/bar/world/1')
        self.assertDictEqual(params, {'another': 'a'})

    def test_convert_options(self):
        options = {'params': {'ticker': ['AAPL', 'MSFT'],
                              'per_end_date': {'gte': {'2015-01-01'}},
                              'qopts': {'columns': ['ticker', 'per_end_date'],
                                        'per_page': 5}}}
        expect_result = {'params': {'qopts.per_page': 5,
                                    'per_end_date.gte': set(['2015-01-01']),
                                    'ticker[]': ['AAPL', 'MSFT'],
                                    'qopts.columns[]': ['ticker', 'per_end_date']}}
        result = Util.convert_options(**options)
        self.assertEqual(cmp(result, expect_result), 0)

        options = {'params': {'ticker': 'AAPL', 'per_end_date': {'gte': {'2015-01-01'}},
                              'qopts': {'columns': ['ticker', 'per_end_date']}}}
        expect_result = {'params': {'per_end_date.gte': set(['2015-01-01']),
                                    'ticker': 'AAPL',
                                    'qopts.columns[]': ['ticker', 'per_end_date']}}
        result = Util.convert_options(**options)
        self.assertEqual(cmp(result, expect_result), 0)
