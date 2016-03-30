import factory


class DatatableMetaFactory(factory.Factory):

    class Meta:
        model = dict

    next_cursor_id = 'abc123'
