from quandl.operations.data_list import DataListOperation
from quandl.util import Util
from .model_base import ModelBase
from .data_mixin import DataMixin


class Data(DataListOperation, DataMixin, ModelBase):

    def __init__(self, data, **options):
        self.meta = options['meta']
        self._raw_data = Util.convert_to_dates(data)

        # Optimization for when a list of data points are created from a
        # dataset (via the model_list class)
        if 'converted_column_names' in options.keys():
            self._converted_column_names = options['converted_column_names']

    # Need to override data_fields incase the way the Data class was populated
    # that it did not contain a converted_column_names option passed in when it was created.
    def data_fields(self):
        if not self._converted_column_names and self.meta:
            self._converted_column_names = Util.convert_column_names(self.meta)

        return self._converted_column_names

    def __getattr__(self, k):
        if k[0] == '_' and k != '_raw_data':
            raise AttributeError(k)
        elif k in self.meta:
            return self.meta[k]
        # Convenience method for accessing individual data point columns by name.
        elif k in self.data_fields():
            return self._raw_data[self.data_fields().index(k)]
        return super(Data, self).__getattr__(k)
