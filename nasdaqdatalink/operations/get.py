from inflection import singularize

from .operation import Operation
from nasdaqdatalink.connection import Connection
from nasdaqdatalink.util import Util


class GetOperation(Operation):

    @classmethod
    def get_path(cls):
        return cls.default_path()

    def __get_raw_data__(self):
        if self._raw_data:
            return self._raw_data

        cls = self.__class__
        params = {'id': str(self.code)}
        options = Util.merge_options('params', params, **self.options)

        path = Util.constructed_path(cls.get_path(), options['params'])

        r = Connection.request('get', path, **options)
        response_data = r.json()
        Util.convert_to_dates(response_data)
        self._raw_data = response_data[singularize(cls.lookup_key())]
        return self._raw_data
