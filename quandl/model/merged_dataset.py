from more_itertools import unique_everseen
import pandas as pd
from six import string_types
from .model_base import ModelBase
from .merged_data_list import MergedDataList
from .data import Data
from .dataset import Dataset


class MergedDataset(ModelBase):

    def __init__(self, datasets, **options):
        self._datasets = datasets
        raw_data = self._initialize_raw_data()
        super(MergedDataset, self).__init__(raw_data)

    @classmethod
    def get(cls, dataset_codes, **options):
        if not isinstance(dataset_codes, list):
            raise ValueError('dataset codes must be specified in a list')
        # column_index is handled by individual dataset get's
        if 'params' in options:
            options['params'].pop("column_index", None)
        datasets = list([cls._get_dataset(dataset_code, **options)
                         for dataset_code in dataset_codes])
        # raw data will be initialized internally
        return MergedDataset(datasets)

    @classmethod
    def _get_dataset(cls, dataset_code, **options):
        options_copy = options.copy()
        # data_codes are tuples e.g., ('GOOG/NASDAQ_AAPL', {'column_index":
        # [1,2]}) or strings 'NSE/OIL'
        code = cls._get_request_dataset_code(dataset_code)

        dataset = Dataset.get(code, **options_copy)
        dataset.column_index = []
        # ensure if column_index dict is specified, value is a list
        params = cls._get_request_params(dataset_code)
        if 'column_index' in params:
            column_index = params['column_index']
            if not isinstance(column_index, list):
                raise ValueError(
                    "%s : column_index needs to be a list of integer indexes" % code)
            dataset.column_index = column_index
        # if column_indexes are specified, check that they actually exist
        max_column_index = len(dataset.column_names) - 1
        for index in dataset.column_index:
            if index > max_column_index or index < 1:
                raise ValueError("%s : requested index %s is out of range. \
                                  Min index is 1 and Max index is %s" % (code, index,
                                                                         max_column_index))
        return dataset

    @classmethod
    def _get_request_dataset_code(cls, dataset_code):
        if isinstance(dataset_code, tuple):
            return dataset_code[0]
        elif isinstance(dataset_code, string_types):
            return dataset_code
        else:
            raise ValueError("Arguments in list must be tuple or string")

    @classmethod
    def _get_request_params(cls, dataset_code):
        if isinstance(dataset_code, tuple):
            return dataset_code[1]
        return {}

    @property
    def column_names(self):
        return list(unique_everseen(
            [self._rename_columns(dataset, column_name) if index > 0 else column_name
             for dataset in self._datasets
             for index, column_name in
             enumerate(dataset.raw_data['column_names']) if self._include_column(dataset, index)]))

    @property
    def oldest_available_date(self):
        return min(self._get_dataset_attribute('oldest_available_date'))

    @property
    def newest_available_date(self):
        return max(self._get_dataset_attribute('newest_available_date'))

    def data(self, **options):
        dataset_data_list = [dataset.data(**options)
                             for dataset in self._datasets]

        data_frames = [dataset_data.to_pandas(
            keep_column_indexes=self._datasets[index].column_index)
            for index, dataset_data in enumerate(dataset_data_list)]

        merged_data_frames = pd.DataFrame()

        for index, data_frame in enumerate(data_frames):
            metadata = self._datasets[index]
            data_frame.rename(
                columns=lambda x: self._rename_columns(metadata, x), inplace=True)
            merged_data_frames = pd.merge(
                merged_data_frames, data_frame, right_index=True, left_index=True, how='outer')

        merged_data_metadata = {}

        # for sanity check if list has items
        if dataset_data_list:
            # meta should be the same for every individual Dataset
            # request, just take the first one
            merged_data_metadata = dataset_data_list[0].meta.copy()
            merged_data_metadata['column_names'] = self.column_names

            # response will contain query param dates, if specified
            # otherwise take the merged earliest/latest dates
            if not self._in_query_param('start_date', **options):
                merged_data_metadata['start_date'] = self.oldest_available_date

            if not self._in_query_param('end_date', **options):
                merged_data_metadata['end_date'] = self.newest_available_date

        # check if descending was explicitly set
        return MergedDataList(
            Data, merged_data_frames, merged_data_metadata,
            ascending=self._order_is_ascending(**options))

    def _rename_columns(self, dataset_metadata, original_column_name):
        return "%s/%s" % (dataset_metadata.database_code,
                          dataset_metadata.dataset_code) + ' - ' + original_column_name

    def _get_dataset_attribute(self, k):
        return list(unique_everseen([dataset.raw_data[k] for dataset in self._datasets]))

    def _initialize_raw_data(self):
        raw_data = {}
        if not self._datasets:
            return raw_data
        raw_data = self._datasets[0].raw_data.copy()
        for k, v in list(raw_data.items()):
            raw_data[k] = getattr(self, k)
        return raw_data

    def _include_column(self, dataset_metadata, column_index):
        # non-pandas/dataframe:
        # keep column 0 around because we want to keep Date
        if len(dataset_metadata.column_index) > 0 and column_index != 0:
            return column_index in dataset_metadata.column_index
        return True

    def _order_is_ascending(self, **options):
        return not (self._in_query_param('order', **options) and
                    options['params']['order'] == 'desc')

    def _in_query_param(self, name, **options):
        return ('params' in options and
                name in options['params'])

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)
        elif k in self._datasets[0].raw_data:
            return self._get_dataset_attribute(k)
        return super(MergedDataset, self).__getattr__(k)
