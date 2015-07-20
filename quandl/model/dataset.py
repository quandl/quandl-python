from quandl.operations.get import GetOperation
from quandl.operations.list import ListOperation
from quandl.util import Util
from .model_base import ModelBase
from .data import Data
from .database import Database


class Dataset(GetOperation, ListOperation, ModelBase):

    @classmethod
    def get_path(cls):
        return "%s/metadata" % cls.default_path()

    def data(self, **options):
        # default order to ascending, and respect whatever user passes in
        params = {'database_code': self.database_code,
                  'dataset_code': self.dataset_code, 'order': 'asc'}
        updated_options = Util.merge_options('params', params, **options)
        return Data.all(**updated_options)

    def database(self):
        return Database.get(self.database_code)
