from collections import OrderedDict
from quandl.operations.data_list import DataListOperation
from quandl.util import Util
from .model_base import ModelBase
from .data_mixin import DataMixin


class Data(DataListOperation, DataMixin, ModelBase):

    def __init__(self, data, **options):
        self.meta = options['meta']
        self._converted_column_names = options['converted_column_names']
        self._raw_data = Util.convert_to_dates(data)

    def data_fields(self):
        if not self._converted_column_names:
            self._converted_column_names = Util.convert_column_names(self.meta)
        return self._converted_column_names

    def __getattr__(self, k):
        if k[0] == '_' and k != '_raw_data':
            raise AttributeError(k)
        elif k in self.meta:
            return self.meta[k]
        elif k in self.data_fields():
            return self._raw_data[self.data_fields().index(k)]
        return super(Data, self).__getattr__(k)
