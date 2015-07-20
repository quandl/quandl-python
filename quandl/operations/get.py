from inflection import singularize

from .operation import Operation
from quandl.connection import Connection
from quandl.util import Util


class GetOperation(Operation):
    @classmethod
    def get(cls, id, **options):
        params = {'id': str(id)}
        options = Util.merge_options('params', params, **options)
        path = Util.constructed_path(cls.get_path(), options['params'])
        r = Connection.request('get', path, **options)
        response_data = r.json()
        Util.convert_to_dates(response_data)
        data = response_data[singularize(cls.lookup_key())]
        resource = cls(data)
        return resource

    @classmethod
    def get_path(cls):
        return cls.default_path()
