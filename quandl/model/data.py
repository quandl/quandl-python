from collections import OrderedDict
from quandl.operations.data_list import DataListOperation
from quandl.util import Util
from .model_base import ModelBase
from .data_mixin import DataMixin


class Data(DataListOperation, DataMixin, ModelBase):
    def __init__(self, data, **options):
        self.meta = options['meta']
        if 'column_names' in options['meta'].keys():
            the_list = [Util.methodize(x) for x in options['meta']['column_names']]
            converted_column_names = list(the_list)
        else:
            converted_column_names = list([Util.methodize(x) for x in options['meta']['columns']])
        self._raw_data = Util.convert_to_dates(OrderedDict(list(zip(converted_column_names, data))))

    def __getattr__(self, k):
        if k[0] == '_' and k != '_raw_data':
            raise AttributeError(k)
        elif k in self.meta:
            return self.meta[k]
        return super(Data, self).__getattr__(k)
