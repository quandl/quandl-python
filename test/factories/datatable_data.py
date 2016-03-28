import factory
import six


class DatatableDataFactory(factory.Factory):

    class Meta:
        model = dict
    columns = [{six.u('name'): six.u('per_end_date'), six.u('type'): six.u('Date')},
               {six.u('name'): six.u('ticker'), six.u('type'): six.u('String')},
               {six.u('name'): six.u('tot_oper_exp'), six.u('type'): six.u('BigDecimal(11,4)')}]
    data = [['2015-07-11', 'AAPL', 456.9], ['2015-07-13', 433.3],
            ['2015-07-14', 'AAPL', 419.1], ['2015-07-15', 476.5]]
