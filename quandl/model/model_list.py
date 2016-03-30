from quandl.util import Util


class ModelList(object):

    def __init__(self, klass, values, meta):
        self.klass = klass
        if 'columns' in meta.keys():
            meta['column_types'] = Util.convert_to_columns_list(meta['columns'], 'type')
            meta['columns'] = Util.convert_to_columns_list(meta['columns'], 'name')

        # Since we are iterating over a list of data be sure to only compute the
        # methodized column names once and pass that down to the objects that are being created.
        converted_column_names = Util.convert_column_names(meta)

        if hasattr(klass, 'get_code_from_meta'):
            self.values = list([klass(
                klass.get_code_from_meta(x),
                x,
                meta=meta,
                converted_column_names=converted_column_names
            ) for x in values])
        else:
            self.values = list([klass(
                x,
                meta=meta,
                converted_column_names=converted_column_names
            ) for x in values])
        self.meta = meta

    def to_list(self):
        l = list([x.to_list() for x in self.values])
        return l

    def __getattr__(self, k):
        if k in self.meta:
            return self.meta[k]
        elif k == 'column_names':
            # keep datatable compatible with dataset
            return self.meta['columns']
        elif hasattr(self.values, k):
            return getattr(self.values, k)
        raise AttributeError(k)

    def __getitem__(self, k):
        return self.values[k]

    def __len__(self):
        return len(self.values)
