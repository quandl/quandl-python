from quandl.model.data_list import DataList
from .list import ListOperation
from quandl.errors.quandl_error import (InvalidDataError, ColumnNotFound)
from quandl.message import Message


class DataListOperation(ListOperation):
    @classmethod
    def create_list_from_response(cls, data):
        cls.validate_dataset_data_response(data['dataset_data'])
        values = data['dataset_data'].pop('data')
        metadata = data['dataset_data']
        return DataList(cls, values, metadata)

    @classmethod
    def create_datatable_list_from_response(cls, data):
        if len(data['datatable']['data']) > 0 \
                and len(data['datatable']['columns']) != len(
                    data['datatable']['data'][0]):
            raise InvalidDataError(
                Message.ERROR_COLUMNS_DATA_NOT_MATCHED,
                response_data=data)
        values = data['datatable'].pop('data')
        metadata = {'columns': data['datatable']['columns'],
                    'next_cursor_id': data['meta']['next_cursor_id']}
        return DataList(cls, values, metadata)

    @classmethod
    def list_path(cls):
        return "datasets/:database_code/:dataset_code/data"

    @classmethod
    def validate_dataset_data_response(cls, dataset_data):
        if len(dataset_data['data']) > 0 \
                and len(dataset_data['column_names']) != len(
                    dataset_data['data'][0]):
            raise InvalidDataError(
                Message.ERROR_COLUMNS_DATA_NOT_MATCHED,
                response_data=dataset_data)
        # if column index was requested
        # and data returned nothing
        # and column name is missing, column is None
        if (dataset_data.get('column_index', None) and
            not dataset_data['data'] and
                cls.column_name_missing(dataset_data)):
            raise ColumnNotFound(Message.ERROR_REQUESTED_COLUMN_NOT_EXIST
                                 % dataset_data['column_index'])

    @classmethod
    def column_name_missing(cls, dataset_data):
        for name in dataset_data['column_names']:
            if name is None:
                return True
        return False
