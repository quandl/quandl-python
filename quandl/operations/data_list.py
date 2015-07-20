from quandl.model.data_list import DataList
from .list import ListOperation
from quandl.errors.quandl_error import InvalidDataError


class DataListOperation(ListOperation):
    @classmethod
    def create_list_from_response(cls, data):
        if len(data['dataset_data']['data']) > 0 \
                and len(data['dataset_data']['column_names']) != len(
                    data['dataset_data']['data'][0]):
            raise InvalidDataError(
                'number of column names does not match number of data points in a row!',
                response_data=data)
        values = data['dataset_data'].pop('data')
        metadata = data['dataset_data']
        return DataList(cls, values, metadata)

    @classmethod
    def list_path(cls):
        return "datasets/:database_code/:dataset_code/data"
