from .data_list import DataList


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
        numpy_results = self.to_numpy()
        numpy_dtype_names = numpy_results.dtype.names
        numpy_dtypes = numpy_results.dtype.fields.items()

        if [dtype for _, dtype in numpy_dtypes if dtype[0].str == '<M8[ns]']:
            python_compatible_dtypes = []
            for name in numpy_dtype_names:
                print(name)
                print('Adding', name, numpy_results.dtype[name].str)
                if numpy_results.dtype[name].str == '<M8[ns]':
                    python_compatible_dtypes.append((name, '<M8[ms]'))
                else:
                    python_compatible_dtypes.append((name, numpy_results.dtype[name].str))

            print(python_compatible_dtypes)
            return numpy_results.astype(python_compatible_dtypes).tolist()
        else:
            return numpy_results.tolist()

    def _column_names(self):
        return self.to_numpy().dtype.names
