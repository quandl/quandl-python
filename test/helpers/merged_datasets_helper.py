import re
import jsondate as json
import six

from quandl.model.dataset import Dataset
from quandl.model.data import Data
from quandl.model.data_list import DataList
from test.factories.dataset import DatasetFactory
from test.factories.dataset_data import DatasetDataFactory


def setupDatasetsTest(unit_test, httpretty):
    httpretty.reset()
    httpretty.enable()

    unit_test.dataset_data = {'dataset_data': DatasetDataFactory.build()}

    # mock out calls with column_index query param
    # NOTE: this will always return 'column.1' as the column name
    single_col_data = DatasetDataFactory.build(column_names=[six.u('Date'), six.u('column.1')],
                                               data=[['2015-07-11', 444.3], ['2015-07-13', 433.3],
                                                     ['2015-07-14', 437.5], ['2015-07-15', 440.0]])
    unit_test.single_dataset_data = {'dataset_data': single_col_data}

    dataset_data = DatasetDataFactory.build()
    d_values = dataset_data.pop('data')
    d_metadata = dataset_data
    unit_test.data_list_obj = DataList(Data, d_values, d_metadata)

    unit_test.nse_oil = {'dataset': DatasetFactory.build(
        database_code='NSE', dataset_code='OIL')}

    unit_test.goog_aapl = {'dataset': DatasetFactory.build(
        database_code='GOOG', dataset_code='NASDAQ_AAPL')}

    unit_test.goog_msft = {'dataset': DatasetFactory.build(
        database_code='GOOG', dataset_code='NASDAQ_MSFT',
        newest_available_date='2015-07-30', oldest_available_date='2013-01-01')}

    unit_test.single_col = {'dataset': DatasetFactory.build(
        database_code='SINGLE', dataset_code='COLUMN',
        newest_available_date='2015-07-30', oldest_available_date='2013-01-01')}

    unit_test.oil_obj = Dataset('NSE/OIL', unit_test.nse_oil['dataset'])
    unit_test.aapl_obj = Dataset('GOOG/AAPL', unit_test.goog_aapl['dataset'])
    unit_test.goog_obj = Dataset('GOOG/MSFT', unit_test.goog_msft['dataset'])
    unit_test.single_col_obj = Dataset('SINGLE/COLUMN', unit_test.single_col['dataset'])

    httpretty.register_uri(httpretty.GET,
                           re.compile(
                               'https://www.quandl.com/api/v3/datasets/.*/metadata'),
                           responses=[httpretty.Response(body=json.dumps(dataset))
                                      for dataset in
                                      [unit_test.nse_oil, unit_test.goog_aapl,
                                       unit_test.goog_msft]])
    # mock our query param column_index request
    httpretty.register_uri(httpretty.GET,
                           "https://www.quandl.com/api/v3/datasets/SINGLE/COLUMN/data",
                           body=json.dumps(unit_test.single_dataset_data))
    httpretty.register_uri(httpretty.GET,
                           "https://www.quandl.com/api/v3/datasets/GOOG/NASDAQ_AAPL/data",
                           body=json.dumps(unit_test.dataset_data))
    httpretty.register_uri(httpretty.GET,
                           re.compile(
                               'https://www.quandl.com/api/v3/datasets/NSE/OIL/data'),
                           body=json.dumps(unit_test.dataset_data))
    httpretty.register_uri(httpretty.GET,
                           re.compile(
                               'https://www.quandl.com/api/v3/datasets/GOOG/NASDAQ_MSFT/data'),
                           body=json.dumps(unit_test.dataset_data))
