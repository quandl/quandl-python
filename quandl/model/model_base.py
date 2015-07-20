class ModelBase(object):
    def __init__(self, raw_data, **options):
        self.raw_data = raw_data

    def to_list(self):
        if isinstance(self.raw_data, dict):
            return list(self.raw_data.values())
        return self.raw_data

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)
        elif k in self.raw_data:
            return self.raw_data[k]
        raise AttributeError(k)

    def __getitem__(self, k):
        return self.raw_data[k]

    def data_fields(self):
        return list(self.raw_data.keys())
