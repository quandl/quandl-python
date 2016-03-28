import factory
import six


class DatasetDataFactory(factory.Factory):

    class Meta:
        model = dict

    column_names = [six.u('Date'), six.u('column.1'), six.u('column.2'), six.u('column.3')]
    data = [['2015-07-11', 444.3, 10, 3], ['2015-07-13', 433.3, 4, 3],
            ['2015-07-14', 437.5, 3, 3], ['2015-07-15', 440.0, 2, 3]]
    start_date = '2014-02-01'
    end_date = '2015-7-29'
    order = 'asc'
