class ModelBase(object):
    def __init__(self, code, raw_data=None, **options):
        self.code = code
        self._raw_data = raw_data
        self.options = options

    def to_list(self):
        if isinstance(self.__get_raw_data__(), dict):
            return list(self.__get_raw_data__().values())
        return self.__get_raw_data__()

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)
        elif k in self.__get_raw_data__():
            return self.__get_raw_data__()[k]
        else:
            raise AttributeError(k)

    def __getitem__(self, k):
        return self.__get_raw_data__()[k]

    def data_fields(self):
        return list(self.__get_raw_data__().keys())

    def __get_raw_data__(self):
        return self._raw_data
