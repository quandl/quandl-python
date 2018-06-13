from .data_list import DataList
import pandas

class MergedDataList(DataList):

    def __init__(self, klass, values, meta, ascending=True):
        # values is a merged DataFrame
        self.__data_frame = values
        self.__ascending = ascending
        raw_data = self._initialize_raw_data()
        super(MergedDataList, self).__init__(klass, raw_data, meta)

    def to_pandas(self):
        # require ascending flag because merge will sort data into ascending
        if not self.__ascending:
            return self.__data_frame.sort_index(ascending=False)
        return self.__data_frame

    def _initialize_raw_data(self):
        dataframe = self.to_pandas().copy()
        dataframe.insert(0, 'date', pandas.to_datetime(dataframe.index))
        return dataframe.as_matrix()

    def _column_names(self):
        return self.to_numpy().dtype.names
