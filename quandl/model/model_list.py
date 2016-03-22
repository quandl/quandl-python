class ModelList(object):
    def __init__(self, klass, values, meta):
        self.klass = klass
        if hasattr(klass, 'get_code_from_meta'):
            self.values = list([klass(klass.get_code_from_meta(x), x, meta=meta) for x in values])
        else:
            self.values = list([klass(x, meta=meta) for x in values])
        self.meta = meta

    def to_list(self):
        l = list([x.to_list() for x in self.values])
        return l

    def __getattr__(self, k):
        if k in self.meta:
            return self.meta[k]
        elif hasattr(self.values, k):
            return getattr(self.values, k)
        raise AttributeError(k)

    def __getitem__(self, k):
        return self.values[k]

    def __len__(self):
        return len(self.values)
