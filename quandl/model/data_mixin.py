import pandas as pd


class DataMixin(object):
    # DataFrame will respect order of input list of list
    def to_pandas(self, keep_column_indexes=[]):
        data = self.to_list()
        # ensure pandas gets a list of lists
        if data and isinstance(data, list) and not isinstance(data[0], list):
            data = [data]
        df = pd.DataFrame(data=data, columns=self.column_names)
        # ensure our first column of time series data is of pd.datetime
        df[self.column_names[0]] = df[self.column_names[0]].apply(pd.to_datetime)
        df.set_index(self.column_names[0], inplace=True)
        # unfortunately to_records() cannot handle unicode in 2.7
        df.index.name = str(df.index.name)
        # keep_column_indexes are 0 based, 0 is the first column
        if len(keep_column_indexes) > 0:
            # need to decrement all our indexes by 1 because
            # Date is considered a column by our API, but in pandas,
            # it is the index, so column 0 is the first column after Date index
            keep_column_indexes = list([x - 1 for x in keep_column_indexes])
            df = df[keep_column_indexes]
        return df

    def to_numpy(self):
        return self.to_pandas().to_records()

    def to_csv(self):
        return self.to_pandas().to_csv()
