import factory


class DatatableFactory(factory.Factory):

    class Meta:
        model = dict
    id = factory.Sequence(lambda n: n)
    vendor_code = factory.Sequence(lambda n: 'VENDOR_CODE{0}'.format(n))
    datatable_code = factory.Sequence(lambda n: 'DATATABLE_CODE{0}'.format(n))
    name = factory.Sequence(lambda n: 'DATATABLE{0}'.format(n))
