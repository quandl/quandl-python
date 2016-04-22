import factory


class MetaFactory(factory.Factory):

    class Meta:
        model = dict

    current_page = 1
    next_page = 1
    prev_page = None
    total_pages = 105
    total_count = 2602
    per_page = 25
    current_first_item = 1
    current_last_time = 25
