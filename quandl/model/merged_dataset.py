from more_itertools import unique_everseen
import pandas as pd
from six import string_types
from .model_base import ModelBase
from quandl.util import Util
from .merged_data_list import MergedDataList
from .data import Data
from quandl.message import Message
from .dataset import Dataset


class MergedDataset(ModelBase):

    def __init__(self, dataset_codes, **options):
        self.dataset_codes = dataset_codes
        self._datasets = None
        self._raw_data = None
        self.options = options

    @property
    def column_names(self):
        return self._merged_column_names_from(self.__dataset_objects__())

    @property
    def oldest_available_date(self):
        return min(self._get_dataset_attribute('oldest_available_date'))

    @property
    def newest_available_date(self):
        return max(self._get_dataset_attribute('newest_available_date'))

    def data(self, **options):
        # if there is only one column_index, use the api to fetch
        # else fetch all the data and filter column indexes requested locally
        dataset_data_list = [self._get_dataset_data(dataset, **options)
                             for dataset in self.__dataset_objects__()]

        # build data frames and filter locally when necessary
        data_frames = [dataset_data.to_pandas(
            keep_column_indexes=self._keep_column_indexes(index))
            for index, dataset_data in enumerate(dataset_data_list)]

        merged_data_frame = pd.DataFrame()

        for index, data_frame in enumerate(data_frames):
            metadata = self.__dataset_objects__()[index]
            # use code to prevent metadata api call
            data_frame.rename(
                columns=lambda x: self._rename_columns(metadata.code, x), inplace=True)
            merged_data_frame = pd.merge(
                merged_data_frame, data_frame, right_index=True, left_index=True, how='outer')

        merged_data_metadata = self._build_data_meta(dataset_data_list, merged_data_frame)

        # check if descending was explicitly set
        # if set we need to sort in descending order
        # since panda merged dataframe will
        # by default sort everything in ascending
        return MergedDataList(
            Data, merged_data_frame, merged_data_metadata,
            ascending=self._order_is_ascending(**options))

    # for MergeDataset data calls
    def _get_dataset_data(self, dataset, **options):
        updated_options = options
        # if we have only one column index, let the api
        # handle the column filtering since the api supports this
        if len(dataset.requested_column_indexes) == 1:
            params = {'column_index': dataset.requested_column_indexes[0]}
            # only change the options per request
            updated_options = options.copy()
            updated_options = Util.merge_options('params', params, **updated_options)
        return dataset.data(**updated_options)

    def _build_data_meta(self, dataset_data_list, df):
        merged_data_metadata = {}
        # for sanity check if list has items
        if dataset_data_list:
            # meta should be the same for every individual Dataset
            # request, just take the first one
            merged_data_metadata = dataset_data_list[0].meta.copy()

            # set the start_date and end_date to
            # the actual values we got back from data
            num_rows = len(df.index)
            if num_rows > 0:
                merged_data_metadata['start_date'] = df.index[0].date()
                merged_data_metadata['end_date'] = df.index[num_rows - 1].date()

            # remove column_index if it exists because this would be per request data
            merged_data_metadata.pop('column_index', None)

            # don't use self.column_names to prevent metadata api call
            # instead, get the column_names from the dataset_data_objects
            merged_data_metadata['column_names'] = self._merged_column_names_from(dataset_data_list)
        return merged_data_metadata

    def _keep_column_indexes(self, index):
        # no need to filter if we only have one column_index
        # since leveraged the server to do the filtering
        col_index = self.__dataset_objects__()[index].requested_column_indexes
        if len(self.__dataset_objects__()[index].requested_column_indexes) == 1:
            # empty array for no filtering
            col_index = []
        return col_index

    def _rename_columns(self, code, original_column_name):
        return code + ' - ' + original_column_name

    def _get_dataset_attribute(self, k):
        elements = []
        for dataset in self.__dataset_objects__():
            elements.append(dataset.__get_raw_data__()[k])

        return list(unique_everseen(elements))

    def _order_is_ascending(self, **options):
        return not (self._in_query_param('order', **options) and
                    options['params']['order'] == 'desc')

    def _in_query_param(self, name, **options):
        return ('params' in options and
                name in options['params'])

    # can take in a list of dataset_objects
    # or a list of dataset_data_objects
    def _merged_column_names_from(self, dataset_list):
        elements = []
        for idx_dataset, dataset in enumerate(dataset_list):
            # require getting the code from the dataset object always
            code = self.__dataset_objects__()[idx_dataset].code
            for index, column_name in enumerate(dataset.column_names):
                # only include column names that are not filtered out
                # by specification of the column_indexes list
                if self._include_column(dataset, index):
                    # first index is the date, don't modify the date name
                    if index > 0:
                        elements.append(self._rename_columns(code, column_name))
                    else:
                        elements.append(column_name)
        return list(unique_everseen(elements))

    def _include_column(self, dataset_metadata, column_index):
        # non-pandas/dataframe:
        # keep column 0 around because we want to keep Date
        if (hasattr(dataset_metadata, 'requested_column_indexes') and
            len(dataset_metadata.requested_column_indexes) > 0 and
                column_index != 0):
            return column_index in dataset_metadata.requested_column_indexes
        return True

    def _initialize_raw_data(self):
        datasets = self.__dataset_objects__()
        self._raw_data = {}
        if not datasets:
            return self._raw_data
        self._raw_data = datasets[0].__get_raw_data__().copy()
        for k, v in list(self._raw_data.items()):
            self._raw_data[k] = getattr(self, k)
        return self._raw_data

    def _build_dataset_object(self, dataset_code, **options):
        options_copy = options.copy()
        # data_codes are tuples
        # e.g., ('GOOG/NASDAQ_AAPL', {'column_index": [1,2]})
        # or strings
        # e.g., 'NSE/OIL'
        code = self._get_request_dataset_code(dataset_code)

        dataset = Dataset(code, None, **options_copy)
        # save column_index param requested dynamically
        # used later on to determine:
        # if column_index is an array, fetch all data and use locally to filter columns
        # if column_index is an empty array, fetch all data and don't filter columns
        dataset.requested_column_indexes = self._get_req_dataset_col_indexes(dataset_code, code)
        return dataset

    def _get_req_dataset_col_indexes(self, dataset_code, code_str):
        # ensure if column_index dict is specified, value is a list
        params = self._get_request_params(dataset_code)
        if 'column_index' in params:
            column_index = params['column_index']
            if not isinstance(column_index, list):
                raise ValueError(
                    Message.ERROR_COLUMN_INDEX_LIST % code_str)
            return column_index
        # default, no column indexes to filter
        return []

    def _get_request_dataset_code(self, dataset_code):
        if isinstance(dataset_code, tuple):
            return dataset_code[0]
        elif isinstance(dataset_code, string_types):
            return dataset_code
        else:
            raise ValueError(Message.ERROR_ARGUMENTS_LIST_FORMAT)

    def _get_request_params(self, dataset_code):
        if isinstance(dataset_code, tuple):
            return dataset_code[1]
        return {}

    def __getattr__(self, k):
        if k[0] == '_' and k != '_raw_data':
            raise AttributeError(k)
        elif hasattr(MergedDataset, k):
            return super(MergedDataset, self).__getattr__(k)
        elif k in self.__dataset_objects__()[0].__get_raw_data__():
            return self._get_dataset_attribute(k)
        return super(MergedDataset, self).__getattr__(k)

    def __get_raw_data__(self):
        if self._raw_data is None:
            self._initialize_raw_data()
        return ModelBase.__get_raw_data__(self)

    def __dataset_objects__(self):
        if self._datasets:
            return self._datasets

        if not isinstance(self.dataset_codes, list):
            raise ValueError('dataset codes must be specified in a list')
        # column_index is handled by individual dataset get's
        if 'params' in self.options:
            self.options['params'].pop("column_index", None)
        self._datasets = list([self._build_dataset_object(dataset_code, **self.options)
                               for dataset_code in self.dataset_codes])

        return self._datasets
