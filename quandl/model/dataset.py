from quandl.operations.get import GetOperation
from quandl.operations.list import ListOperation
from quandl.util import Util
from .model_base import ModelBase
from .data import Data
from .data_list import DataList
import quandl.model.database
from quandl.errors.quandl_error import NotFoundError


class Dataset(GetOperation, ListOperation, ModelBase):

    @classmethod
    def get_path(cls):
        return "%s/metadata" % cls.default_path()

    @classmethod
    def get_code_from_meta(cls, metadata):
        return "%s/%s" % (metadata['database_code'], metadata['dataset_code'])

    def __init__(self, code, raw_data=None, **options):
        ModelBase.__init__(self, code, raw_data)

        parsed_code = self.code.split("/")
        if len(parsed_code) < 2:
            raise SyntaxError('Your quandl code is in an invalid format. It should look like '
                              '`DATABASE_CODE/DATASET_CODE`. Please check your code and try again.')

        self.database_code = parsed_code[0]
        self.dataset_code = parsed_code[1]
        self.options = options

    def data(self, **options):
        # handle_not_found_error if set to True will add an empty DataFrame
        # for a non-existent dataset instead of raising an error
        handle_not_found_error = options.pop('handle_not_found_error', False)
        # default order to ascending, and respect whatever user passes in
        params = {
            'database_code': self.database_code,
            'dataset_code': self.dataset_code,
            'order': 'asc'
        }
        updated_options = Util.merge_options('params', params, **options)
        try:
            return Data.all(**updated_options)
        except NotFoundError:
            if handle_not_found_error:
                # return empty data list
                return DataList(Data, [], {'column_names': ['None', 'Not Found']})
            raise

    def database(self):
        return quandl.model.database.Database(self.database_code)
