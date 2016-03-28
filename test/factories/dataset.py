import factory
import six


class DatasetFactory(factory.Factory):

    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)
    database_id = factory.Sequence(lambda n: n)
    database_code = factory.Sequence(lambda n: 'DATABASE_CODE{0}'.format(n))
    dataset_code = factory.Sequence(lambda n: 'DATASET_CODE{0}'.format(n))
    name = 'National Stock Exchange of India'
    description = 'Stock and index data from the National Stock Exchange of India. '
    frequency = 'daily'
    column_names = [six.u('Date'), six.u('column.1'), six.u('column.2'), six.u('column.3')]
    type = 'Time Series'
    premium = False
    refreshed_at = '2015-07-24T02:39:40.624Z'
    newest_available_date = '2015-07-23'
    oldest_available_date = '2014-01-01'
